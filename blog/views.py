# _*_ coding:utf-8 _*_

from django.shortcuts import render, get_object_or_404
from blog.models import Post, Tag
from comment.models import Comment
from comment.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models.aggregates import Count
import json
from django.http import HttpResponse, JsonResponse
from www.views import page_not_found
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import websockets
import datetime
import hmac
import base64
from urllib.parse import urlencode
from django.conf import settings


# 获取某篇文章的评论回复内容
def comment_reply_content(post_id):
    # 评论
    comments = Comment.objects.filter(is_show=True, post_id=post_id, comment_type='comment').order_by('pk')
    comments_dict = {'comments': {}, 'count': 0}
    for comment in comments:
        comments_dict['comments'][comment.id] = {
            'comment': {
                'id': comment.pk,
                'post_id': comment.post_id,
                'add_time': comment.add_time,
                'content': comment.content,
                'parent_id': comment.parent_id,
                'reply_id': comment.reply_id,
                'nick': comment.nick,
                'browser': comment.browser,
                'client': comment.client,
                'avatar': comment.avatar,
            },
            'reply': [],
        }
    # 回复
    replys = Comment.objects.filter(is_show=True, post_id=post_id, comment_type='reply').order_by('pk')
    for reply in replys:
        if reply.parent_id in comments_dict['comments'].keys():
            comments_dict['comments'][reply.parent_id]['reply'].append({
                'id': reply.pk,
                'post_id': reply.post_id,
                'add_time': reply.add_time,
                'content': reply.content,
                'parent_id': reply.parent_id,
                'reply_id': reply.reply_id,
                'nick': reply.nick,
                'to_nick': reply.to_nick,
                'browser': reply.browser,
                'client': reply.client,
                'avatar': reply.avatar,
            })
    comments_dict['count'] = len(replys) + len(comments)
    return comments_dict


# 博客文章列表页面
class Index(object):
    def __init__(self):
        # 定义 per_page 的值，每个页面的文章数
        self.per_page = 10

    def index(self, request):
        # 博客首页：获取Post表中所有文章列表
        post_list = Post.objects.filter(is_show=True, post_type='post')
        page = request.GET.get('page')
        return self.get_data(post_list=post_list, page=page, request=request)

    def tags(self, request, tag):
        # 标签：按照标签(tag)查询Post表中的文章列表
        post_list = Post.objects.filter(tags__name=tag, is_show=True, post_type='post')
        page = request.GET.get('page')
        return self.get_data(post_list=post_list, page=page, request=request)

    def get_data(self,post_list, page, request):
        post_list = self.Pagination(post_list=post_list, page=page)
        post_type = 'post'
        return render(request, 'blog/index.html', context={'post_list': post_list, 'post_type': post_type})

    # 高级分页扩展函数
    def Pagination(self, post_list, page):
        # 使用 Paginator 函数将post_list以每页per_page篇文章进行分页
        paginator = Paginator(post_list, self.per_page)
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return post_list


# 博客详情页
def Detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_show=True, post_type='post')
    post.increase_views()  # 调用 increase_views 方法，统计访问量
    comments_dict = comment_reply_content(post_id=pk)  # 评论回复
    comment_form = CommentForm()  # 引入评论表单
    context = {
        'post': post,
        'comments_dict': comments_dict,
        'comment_form': comment_form,
    }
    return render(request, 'blog/detail.html', context=context)


# 教程
def Tutorial(request):
    # 获取教程类型博文列表
    post_list = Post.objects.filter(is_show=True, post_type='post', tutorial__name__isnull=False).order_by('created_time')

    # 创建一个 dict, 以教程名称为关键字保存
    post_dict = {}
    for post in post_list:
        if post.tutorial not in post_dict.keys():
            post_dict[post.tutorial] = []
        post_dict[post.tutorial].append(post)
    return render(request, 'blog/tutorials.html', context={'post_dict': post_dict})


# 归档页面
def Archives(request):
    years = Post.objects.filter(is_show=True,post_type='post').dates('created_time', 'year', order='DESC')
    post_list = Post.objects.filter(is_show=True,post_type='post').order_by('-created_time')
    return render(request, 'blog/archives.html', context={'years': years, 'post_list':post_list})


# 关于页面
def About(request):
    post = Post.objects.filter(is_show=True, post_type='about').first()
    if post:
        post.increase_views()  # 调用 increase_views 方法，统计访问量
        comments_dict = comment_reply_content(post_id=post.id)  # 评论回复
        comment_form = CommentForm()  # 引入评论表单
        context = {
            'post': post,
            'comments_dict': comments_dict,
            'comment_form': comment_form,
        }
        return render(request, 'blog/about.html', context=context)
    else:
        return page_not_found(request)


# 我的项目
def Project(request):
    post = Post.objects.filter(is_show=True, post_type='project').first()
    if post:
        post.increase_views()  # 调用 increase_views 方法，统计访问量
        comments_dict = comment_reply_content(post_id=post.id)  # 评论回复
        comment_form = CommentForm()  # 引入评论表单
        context = {
            'post': post,
            'comments_dict': comments_dict,
            'comment_form': comment_form,
        }
        return render(request, 'blog/project.html', context=context)
    else:
        return page_not_found(request)

def chat_view(request):

    return render(request, 'blog/chat.html')

# 搜索请求
def search(request):
    # 搜索内容
    if request.method == 'GET':
        q = request.GET.get('q')
        post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q), is_show=True, post_type='post')

        data = {'posts': []}
        for post in post_list:
            data['posts'].append({
                "title": post.title,
                "permalink": post.get_absolute_url(),
                "text": post.body
            },)
        return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        pass


class SparkAPI:
    def __init__(self):
        self.config = settings.SPARK_CONFIG

    def _generate_url(self):
        date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        signature_origin = f"host: {self.config['HOST']}\ndate: {date}\nGET {self.config['PATH']} HTTP/1.1"

        signature = base64.b64encode(
            hmac.new(
                self.config['API_SECRET'].encode('utf-8'),
                signature_origin.encode('utf-8'),
                digestmod='sha256'
            ).digest()
        ).decode()

        authorization_origin = (
            f'api_key="{self.config["API_KEY"]}", '
            f'algorithm="hmac-sha256", '
            f'headers="host date request-line", '
            f'signature="{signature}"'
        )

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode()

        params = {
            'authorization': authorization,
            'date': date,
            'host': self.config['HOST']
        }

        return f"wss://{self.config['HOST']}{self.config['PATH']}?{urlencode(params)}"

    async def send_message(self, message):
        url = self._generate_url()
        async with websockets.connect(url) as ws:
            data = {
                "header": {
                    "app_id": self.config['APPID'],
                    "uid": "12345"
                },
                "parameter": {
                    "chat": {
                        "domain": "general",
                        "temperature": 0.5,
                        "max_tokens": 1024
                    }
                },
                "payload": {
                    "message": {
                        "text": [
                            {
                                "role": "user",
                                "content": message
                            }
                        ]
                    }
                }
            }

            await ws.send(json.dumps(data))

            response_text = ""
            async for response in ws:
                response_data = json.loads(response)
                if response_data["header"]["code"] != 0:
                    raise Exception(f"API请求错误: {response_data}")

                choices = response_data["payload"]["choices"]
                if choices.get("text"):
                    response_text += choices["text"][0]["content"]

                if response_data["header"]["status"] == 2:
                    break

            return response_text


# 聊天相关视图
def chat_view(request):
    return render(request, 'blog/chat.html')


@require_http_methods(["POST"])
@csrf_protect
async def send_message(request):
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()

        if not message:
            return JsonResponse({'error': '消息不能为空'}, status=400)

        spark = SparkAPI()
        response = await spark.send_message(message)

        return JsonResponse({'response': response})

    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的请求数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


import json
import websocket
import datetime
import hashlib
import base64
import hmac
import ssl
import time
from datetime import datetime
from urllib.parse import urlencode
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.cache import cache

# 从settings导入配置
SPARK_CONFIG = settings.SPARK_CONFIG


# 从settings导入配置
SPARK_CONFIG = settings.SPARK_CONFIG


def create_url():
    """生成鉴权url"""
    # [保持原有代码不变]
    host = SPARK_CONFIG["HOST"]
    path = SPARK_CONFIG["PATH"]
    url = f"wss://{host}{path}"

    now = datetime.utcnow()
    date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')

    signature_origin = "host: " + host + "\n"
    signature_origin += "date: " + date + "\n"
    signature_origin += "GET " + path + " HTTP/1.1"

    signature_sha = hmac.new(SPARK_CONFIG["API_SECRET"].encode('utf-8'),
                             signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()

    signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

    authorization_origin = f'api_key="{SPARK_CONFIG["API_KEY"]}", algorithm="hmac-sha256", '
    authorization_origin += f'headers="host date request-line", signature="{signature_sha_base64}"'

    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

    v = {
        "authorization": authorization,
        "date": date,
        "host": host
    }
    url = url + '?' + urlencode(v)
    return url


class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window

    def is_allowed(self, user_id):
        cache_key = f"rate_limit_{user_id}"
        current_time = time.time()

        # 获取用户请求历史
        requests = cache.get(cache_key, [])

        # 清理过期的请求记录
        requests = [req_time for req_time in requests
                    if current_time - req_time < self.time_window]

        if len(requests) >= self.max_requests:
            return False

        requests.append(current_time)
        cache.set(cache_key, requests, self.time_window)
        return True


# 创建限流器实例
rate_limiter = RateLimiter(max_requests=20, time_window=60)  # 每分钟最多20个请求


@csrf_exempt
def send_message(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': '仅支持POST请求'
        }, status=405)

    try:
        # 获取用户标识（可以是IP地址或用户ID）
        user_id = request.META.get('REMOTE_ADDR', 'unknown')

        # 检查速率限制
        if not rate_limiter.is_allowed(user_id):
            return JsonResponse({
                'status': 'error',
                'message': '请求过于频繁，请稍后再试'
            }, status=429)

        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_history = data.get('conversation_history', [])

        # 输入验证
        if not user_message:
            return JsonResponse({
                'status': 'error',
                'message': '消息内容不能为空'
            }, status=400)

        if len(user_message) > 2000:  # 设置合理的消息长度限制
            return JsonResponse({
                'status': 'error',
                'message': '消息长度超出限制'
            }, status=400)

        # 格式化对话历史
        formatted_messages = []
        max_history_length = 20  # 最大对话轮次

        # 保留最近的对话历史
        recent_history = conversation_history[-max_history_length * 2:] if conversation_history else []

        for msg in recent_history:
            formatted_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # 添加当前用户消息
        formatted_messages.append({
            "role": "user",
            "content": user_message
        })

        request_data = {
            "header": {
                "app_id": SPARK_CONFIG["APPID"],
                "uid": user_id
            },
            "parameter": {
                "chat": {
                    "domain": "4.0Ultra",
                    "temperature": 0.5,
                    "max_tokens": 2048,
                    "random_threshold": 0.5,
                }
            },
            "payload": {
                "message": {
                    "text": formatted_messages
                }
            }
        }

        # WebSocket连接超时设置
        websocket.setdefaulttimeout(30)  # 30秒超时

        url = create_url()
        ws = websocket.create_connection(
            url,
            sslopt={"cert_reqs": ssl.CERT_NONE}
        )

        try:
            ws.send(json.dumps(request_data))
            response_text = ""
            start_time = time.time()

            while True:
                if time.time() - start_time > 30:  # 30秒超时保护
                    raise TimeoutError("响应超时")

                response = ws.recv()
                response_data = json.loads(response)

                if response_data["header"]["code"] != 0:
                    error_message = response_data["header"].get("message", "未知错误")
                    raise Exception(f"API错误: {error_message}")

                if "payload" in response_data:
                    choice = response_data["payload"]["choices"]["text"][0]
                    response_text += choice["content"]

                    if response_data["header"]["status"] == 2:
                        break

            return JsonResponse({
                'status': 'success',
                'response': response_text,
            })

        finally:
            ws.close()

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的JSON格式'
        }, status=400)
    except TimeoutError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=504)
    except Exception as e:
        import traceback
        print(f"Error occurred: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            'status': 'error',
            'message': f'服务器错误: {str(e)}'
        }, status=500)
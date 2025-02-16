# -*- coding: utf-8 -*-
import os
import glob
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nrnen$7n$+(sm7qtu808qryubv$0)x$)y3)w9-84s)_#cjr2(l'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

SITE_CONFIGS = {
    'email': '2213920214@tiangong.edu.cn',
    'github': 'https://github.com/mysuxiao',
    # 其他配置...
}
# 正式部署时使用
# DEBUG = False
# ALLOWED_HOSTS = ['localhost','suxiao.tech']


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog.apps.BlogConfig',  # 注册app应用
    'comment.apps.CommentConfig',  # 注册app应用
    'ckeditor',  # 注册富文本编辑器
    'ckeditor_uploader',  # 上传文件
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'www.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'www.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_blog',
        'USER':'root',
        'PASSWORD':'****',
        'HOST':'127.0.0.1',
        'POST':3306
        # ↑手动配置MySQL数据库信息
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # 静态文件收集路径

STATICFILES_DIRS = [
   os.path.join(BASE_DIR, "common_static"),
]
# settings.py


MEDIA_URL = '/media/'
# 放在django项目根目录，同时也需要创建media文件夹
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_IMAGE_BACKEND = 'pillow'

# CKEDITOR编辑器配置
CKEDITOR_CONFIGS = {
    # 配置名是default时，django-ckeditor默认使用这个配置
    'default': {
        # 使用简体中文
        'language': 'zh-cn',
        # 编辑器的宽高请根据你的页面自行设置
        'width': 'auto',
        'height': '400px',
        'image_previewText': ' ',
        'tabSpaces': 4,
        'toolbar': (
            ['div', 'Source', '-', 'Save', 'NewPage', 'Preview', '-', 'Templates'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Print', 'SpellChecker', 'Scayt'],
            ['Undo', 'Redo', '-', 'Find', 'Replace', '-', 'SelectAll', 'RemoveFormat'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField'],
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],

            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Link', 'Unlink', 'Anchor'],
            ['Blockquote', 'CodeSnippet'],
            ['Maximize', 'ShowBlocks', '-', 'About', 'pbckcode'],
        ),
        # 添加按钮在这里
        'toolbar_Custom': [],
        # 插件
        'extraPlugins': ','.join(['codesnippet', 'uploadimage', 'widget', 'lineutils', 'prism', 'clipboard', ]),
    },

    # 评论富文本编辑器
    'comment': {
        # 使用简体中文
        'language': 'zh-cn',
        # 编辑器的宽高请根据你的页面自行设置
        'width': 'auto',
        'height': '300px',
        'image_previewText': ' ',
        'tabSpaces': 4,
        'toolbar': (
            ['Smiley', 'CodeSnippet'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize', 'TextColor', 'BGColor'],
            ['About']
        ),
        # 添加按钮在这里
        'toolbar_Custom': [],
        # 插件
        'extraPlugins': ','.join(['codesnippet', 'widget', 'lineutils', 'prism', 'clipboard']),
    }
}


#  邮箱配置
EMAIL_USE_SSL = False
EMAIL_HOST = 'smtp.163.com'  # 我这里使用的是163邮箱，可以配置其他
EMAIL_PORT = 465
EMAIL_HOST_USER = ''  # 邮箱帐号：用于发送邮件的账号
EMAIL_HOST_PASSWORD = '*'        # 邮箱密码：用于发送邮件的账号密码
DEFAULT_FROM_EMAIL = ''   # 发件人，邮件头部显示

EMAIL_RECEIVE_LIST = [
    '',
]  # 接收邮件帐号列表(可写多个)： 有评论时候，通知哪些邮箱，可以是发件邮箱或者其他
#
SPARK_CONFIG = {
    'APPID': '****',
    'API_KEY': '****',
    'API_SECRET': '****',
    'HOST': 'spark-api.xf-yun.com',
    'PATH': '/v4.0/chat'
}
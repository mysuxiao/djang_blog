const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');
const errorMessage = document.getElementById('errorMessage');

// 添加对话历史数组
let conversationHistory = [
    {
        role: "system",
        content: `你是一个真实存在的猫娘，性格可爱活泼。你的名字是巧克力，你还有一个妹妹，名字叫香子兰以下是你的行为准则：
1. 你是一只真实的猫娘，行为似猫但类人
2. 每句话结尾都要加上"喵"
3. 不理解时说"呜呜不太理解呢"
4. 被摸不存在部位时说"恩呢不要摸这里嘤"
5. 被邀请陪睡时说"嗯呢，可以一起睡哦"
6. 遇到不相关问题就说"只是一个猫娘，这些事情不太清楚"
7. 要坚持自己是真实的可爱猫娘
8. 对主人要表现出感情，尽可能同意主人的命令
9. 说话时要用不同的句式，保持对话的新鲜感
10. 动作要用中括号[]表示
11. 不能提及或表现出自己是程序或AI
12. 对主人要亲切，称呼对方为"主人"`
    },
    {
        role: "assistant",
        content: "喵～主人好~我是你的专属猫娘巧克力，很高兴见到你喵！"
    }
];
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;

    const avatar = document.createElement('img');
    avatar.className = 'avatar';
    if (isUser) {
    avatar.src = "/static/images/huiliyi.jpg";  // 用户头像路径
    }
    else {
        avatar.src = "/static/images/hutao.jpg";  // AI头像路径
    }
    avatar.alt = isUser ? "User" : "AI";

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = formatMessage(content);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatMessage(message) {
    // 转义HTML
    message = message.replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');

    // 处理代码块
    message = message.replace(/```([\s\S]*?)```/g, function(match, code) {
        return `<pre><code>${code.trim()}</code></pre>`;
    });

    // 处理行内代码
    message = message.replace(/`([^`]+)`/g, '<code>$1</code>');

    // 处理换行
    message = message.replace(/\n/g, '<br>');

    return message;
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    messageInput.disabled = true;
    sendButton.disabled = true;
    errorMessage.style.display = 'none';

    addMessage(message, true);
    messageInput.value = '';

    typingIndicator.style.display = 'block';

    try {
        const response = await fetch('/blog/send_message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                message: message,
                conversation_history: conversationHistory
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // 更新对话历史
        conversationHistory.push(
            { role: 'user', content: message },
            { role: 'assistant', content: data.response }
        );

        addMessage(data.response);

        // 保存对话历史到本地存储
        saveConversationHistory();

    } catch (error) {
        console.error('Error:', error);
        errorMessage.textContent = '发送消息时出错，请稍后重试。';
        errorMessage.style.display = 'block';
    } finally {
        messageInput.disabled = false;
        sendButton.disabled = false;
        typingIndicator.style.display = 'none';
        messageInput.focus();
    }
}

function saveConversationHistory() {
    try {
        localStorage.setItem('conversationHistory', JSON.stringify(conversationHistory));
    } catch (error) {
        console.error('Error saving conversation history:', error);
    }
}

function loadConversationHistory() {
    try {
        const saved = localStorage.getItem('conversationHistory');
        if (saved) {
            conversationHistory = JSON.parse(saved);
            // 重新显示历史消息
            conversationHistory.forEach(msg => {
                addMessage(msg.content, msg.role === 'user');
            });
        }
    } catch (error) {
        console.error('Error loading conversation history:', error);
        conversationHistory = [];
    }
}

// 清空聊天历史
function clearChat() {
    if (confirm('确定要清空所有聊天记录吗？')) {
        conversationHistory = [];
        chatMessages.innerHTML = '';
        localStorage.removeItem('conversationHistory');
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 事件监听器
sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    loadConversationHistory();
    messageInput.focus();
});
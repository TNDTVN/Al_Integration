document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const welcomeMessage = document.querySelector('.welcome-message');
    
    let isFirstMessage = true;

    // Scroll xuống dưới cùng khi load
    scrollToBottom();

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Gợi ý nhanh từ welcome message và suggestions
    setupQuickPrompts();

    // Auto-focus input
    userInput.focus();

    function setupQuickPrompts() {
        // Gợi ý từ topic tags
        const topicTags = document.querySelectorAll('.topic-tag');
        topicTags.forEach(tag => {
            tag.addEventListener('click', () => {
                const prompt = tag.getAttribute('data-prompt');
                sendQuickPrompt(prompt);
            });
        });

        // Gợi ý từ suggestions
        const suggestions = document.querySelectorAll('.suggestion');
        suggestions.forEach(suggestion => {
            suggestion.addEventListener('click', () => {
                const prompt = suggestion.getAttribute('data-prompt');
                sendQuickPrompt(prompt);
            });
        });
    }

    function sendQuickPrompt(prompt) {
        userInput.value = prompt;
        sendMessage();
    }

    async function sendMessage() {
        const prompt = userInput.value.trim();
        if (!prompt) return;

        // Ẩn welcome message sau khi gửi tin nhắn đầu tiên
        if (isFirstMessage && welcomeMessage) {
            welcomeMessage.style.display = 'none';
            isFirstMessage = false;
        }

        // Vô hiệu hóa input và button
        setInputState(false);

        // Thêm user message vào UI
        addMessage('user', prompt);
        userInput.value = '';

        // Hiển thị loading indicator (sau user message)
        const loadingElement = showLoading();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt })
            });

            if (!response.ok) {
                throw new Error(`Lỗi server: ${response.statusText}`);
            }

            // Ẩn loading indicator
            hideLoading(loadingElement);

            // Lấy response text
            const text = await response.text();
            
            // Thêm assistant message với hiệu ứng typewriter
            await addAssistantMessageWithTypewriter(text);

        } catch (error) {
            console.error('Error:', error);
            hideLoading(loadingElement);
            addMessage('assistant', '❌ Lỗi kết nối server. Vui lòng thử lại.');
        } finally {
            // Kích hoạt lại input và button
            setInputState(true);
            userInput.focus();
        }
    }

    function addMessage(role, content, isMarkdown = true) {
    const messageRow = document.createElement('div');
    messageRow.className = `message-row ${role}-row`;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = `<i class="bi ${role === 'user' ? 'bi-person-fill' : 'bi-robot'}"></i>`;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.innerHTML = isMarkdown ? marked.parse(content) : content;

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = getCurrentTime();

    messageContent.appendChild(textDiv);
    messageContent.appendChild(timeDiv);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    messageRow.appendChild(messageDiv);
    
    // Thêm message vào cuối chat
    chatMessages.appendChild(messageRow);

    scrollToBottom();
    return messageRow;
}

function showLoading() {
    const loadingRow = document.createElement('div');
    loadingRow.className = 'loading-row';

    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading-indicator';

    const avatar = document.createElement('div');
    avatar.className = 'loading-avatar';
    avatar.innerHTML = '<i class="bi bi-robot"></i>';

    const loadingContent = document.createElement('div');
    loadingContent.className = 'loading-content';

    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator';
    typingIndicator.innerHTML = '<span></span><span></span><span></span>';

    loadingContent.appendChild(typingIndicator);
    loadingDiv.appendChild(avatar);
    loadingDiv.appendChild(loadingContent);
    loadingRow.appendChild(loadingDiv);
    
    // Thêm loading sau message user mới nhất
    chatMessages.appendChild(loadingRow);

    scrollToBottom();
    return loadingRow;
}

    function hideLoading(loadingElement) {
        if (loadingElement) {
            loadingElement.remove();
        }
    }

    async function addAssistantMessageWithTypewriter(content) {
        // Thêm assistant message
        const messageRow = addMessage('assistant', '', false);
        const textDiv = messageRow.querySelector('.message-text');

        // Hiệu ứng typewriter
        await typewriterEffect(textDiv, content);
        scrollToBottom();
    }

    async function typewriterEffect(element, text) {
        const words = text.split(' ');
        let currentText = '';

        for (let i = 0; i < words.length; i++) {
            currentText += words[i] + ' ';
            element.innerHTML = marked.parse(currentText);
            
            // Scroll đến phần tử mới nhất
            scrollToBottom();
            
            // Random delay để tạo hiệu ứng tự nhiên
            await delay(Math.random() * 50 + 25);
        }
    }

    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function setInputState(enabled) {
        userInput.disabled = !enabled;
        sendButton.disabled = !enabled;
        
        if (enabled) {
            sendButton.innerHTML = '<i class="bi bi-send-fill"></i>';
        } else {
            sendButton.innerHTML = '<i class="bi bi-hourglass-split"></i>';
        }
    }

    function scrollToBottom() {
        setTimeout(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 100);
    }

    function getCurrentTime() {
        return new Date().toLocaleTimeString('vi-VN', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    // Auto-resize input
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});
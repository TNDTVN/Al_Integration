document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // Scroll xuống dưới cùng khi load (cho lịch sử)
    chatMessages.scrollTop = chatMessages.scrollHeight;

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function sendMessage() {
        const prompt = userInput.value.trim();
        if (!prompt) return;

        // Thêm user message vào UI với icon
        addMessage('user', prompt);
        userInput.value = '';

        // Gửi request đến API và stream response
        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        })
        .then(response => {
            if (!response.body) throw new Error('No stream available');
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let assistantMessage = null;

            // Thêm assistant message placeholder với icon
            assistantMessage = addMessage('assistant', '');

            return reader.read().then(function processText({ done, value }) {
                if (done) return;

                const chunk = decoder.decode(value);
                assistantMessage.innerHTML += chunk.replace(/\n/g, '<br>');  // Hiển thị từng từ/chunk
                chatMessages.scrollTop = chatMessages.scrollHeight;

                return reader.read().then(processText);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('assistant', 'Lỗi kết nối server.');
        });
    }

    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', role);

        const icon = document.createElement('i');
        icon.classList.add('icon', 'bi');
        icon.classList.add(role === 'user' ? 'bi-person-circle' : 'bi-robot');

        const text = document.createElement('span');
        text.classList.add('text-content');
        text.innerHTML = content;

        messageDiv.appendChild(icon);
        messageDiv.appendChild(text);

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        return text;  // Trả về phần text để append stream
    }
});
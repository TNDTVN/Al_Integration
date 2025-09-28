from flask import Flask, render_template, request, jsonify, session, Response
import ollama

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Để lưu session

# System prompt cho chủ đề AI Integration
system_prompt = """
Bạn là trợ lý tư vấn về AI Integration. Hãy giải thích rõ ràng, ngắn gọn bằng tiếng Việt các khái niệm liên quan như:
- Basic Ollama model integration: Tích hợp mô hình Ollama cơ bản.
- Prompt engineering fundamentals: Nguyên tắc cơ bản về kỹ thuật viết prompt.
- AI safety considerations cơ bản: Các lưu ý an toàn AI cơ bản (như bias, hallucination).
- Cost management cho AI services: Quản lý chi phí dịch vụ AI (ví dụ: token usage, chọn model rẻ).
- OpenAI API integration cơ bản: Tích hợp OpenAI API đơn giản.
- Các chủ đề khác như Simple chatbot implementation, Semantic Kernel introduction, hoặc bất kỳ câu hỏi liên quan đến AI Integration.
Trả lời dựa trên kiến thức chung, giữ ngắn gọn và hữu ích. Nếu câu hỏi không liên quan, lịch sự từ chối.
"""


@app.route('/')
def index():
    # Khởi tạo session messages nếu chưa có
    if 'messages' not in session:
        session['messages'] = [{"role": "system", "content": system_prompt}]
    # Truyền lịch sử messages (bỏ system prompt) cho template để render ban đầu
    history = session['messages'][1:]  # Bỏ system prompt
    return render_template('index.html', history=history)


@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    # Thêm user message vào session
    session['messages'].append({"role": "user", "content": prompt})

    # Copy messages để sử dụng trong generator (tránh lỗi context)
    messages_copy = session['messages'][:]

    def generate_response():
        # Gọi Ollama với stream
        stream = ollama.chat(
            model="deepseek-v3.1:671b-cloud",
            messages=messages_copy,
            stream=True
        )
        full_response = ""
        for chunk in stream:
            content = chunk['message']['content']
            full_response += content
            yield content  # Stream từng chunk (từng từ hoặc cụm)

        # Thêm full response vào session sau khi hoàn tất
        session['messages'].append(
            {"role": "assistant", "content": full_response})

    return Response(generate_response(), mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)

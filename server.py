from flask import Flask, render_template, request, jsonify, session, Response
import ollama
import time  # Để simulate stream nếu cần

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

    # Copy messages để sử dụng
    messages_copy = session['messages'][:]

    try:
        # Gọi Ollama non-stream để lấy full response trước
        full_response_data = ollama.chat(
            model="deepseek-v3.1:671b-cloud",
            messages=messages_copy,
            stream=False
        )
        full_response = full_response_data['message']['content']

        # Append full response vào session ngay (trong request context)
        session['messages'].append(
            {"role": "assistant", "content": full_response})

        def generate_response():
            # Simulate stream bằng cách yield từng từ, giữ nguyên xuống dòng
            # Split theo khoảng trắng và giữ \n
            parts = full_response.split('\n')
            for i, part in enumerate(parts):
                words = part.split()
                for word in words:
                    yield word + ' '
                    time.sleep(0.05)  # Delay nhỏ để simulate typing
                if i < len(parts) - 1:  # Thêm \n giữa các dòng
                    yield '\n'

        return Response(generate_response(), mimetype='text/plain')
    except Exception as e:
        return jsonify({'error': f'Lỗi kết nối server: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=False)  # Tắt debug để tránh lỗi log không cần thiết

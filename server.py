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
    # Xóa session messages để làm mới lịch sử chat khi refresh
    session.pop('messages', None)
    # Khởi tạo session messages mới
    session['messages'] = [{"role": "system", "content": system_prompt}]
    # Truyền lịch sử messages (bỏ system prompt) cho template
    history = session['messages'][1:]  # Bỏ system prompt
    return render_template('index.html', history=history)


@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    # Thêm user message vào session
    session['messages'].append({"role": "user", "content": prompt})
    session.modified = True  # Đánh dấu session đã thay đổi

    # Copy messages để sử dụng
    messages_copy = session['messages'][:]

    try:
        # Gọi Ollama với stream=True
        stream = ollama.chat(
            model="deepseek-v3.1:671b-cloud",
            messages=messages_copy,
            stream=True
        )

        # Biến để tích lũy full response
        full_response = ""

        def generate_response():
            nonlocal full_response
            for chunk in stream:
                content = chunk.get('message', {}).get('content', '')
                full_response += content
                # Yield chunk cho client ngay lập tức
                yield content.encode('utf-8')

        # Tạo Response từ generator
        response = Response(generate_response(), mimetype='text/plain')

        # Lưu full_response vào session sau khi stream hoàn tất
        def save_session():
            # Sử dụng app.test_request_context với session hiện tại
            with app.test_request_context():
                # Tạo một bản sao của session để tránh KeyError
                if 'messages' not in session:
                    session['messages'] = [
                        {"role": "system", "content": system_prompt}]
                session['messages'].append(
                    {"role": "assistant", "content": full_response})
                session.modified = True

        # Gọi save_session sau khi Response được xử lý
        response.call_on_close(save_session)
        return response

    except Exception as e:
        print(f"Lỗi kết nối Ollama: {str(e)}")  # In lỗi chi tiết ra console
        return jsonify({'error': f'Lỗi kết nối server: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=False)  # Tắt debug để tránh lỗi log không cần thiết

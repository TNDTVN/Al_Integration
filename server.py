from flask import Flask, render_template, request, jsonify, session, Response
import ollama
import sqlite3
import re
from rules import RULES
from database import init_db, get_model_info, get_model_info_by_id, log_usage, estimate_tokens
import time

app = Flask(__name__)
app.secret_key = 'super_secret_key'

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
    session.pop('messages', None)
    session['messages'] = [{"role": "system", "content": system_prompt}]
    history = session['messages'][1:]
    return render_template('index.html', history=history)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/api/usage/stats')
def get_usage_stats():
    conn = sqlite3.connect('cost_management.db')
    c = conn.cursor()
    c.execute('''
        SELECT 
            SUM(total_tokens) as total_tokens,
            SUM(cost) as total_cost,
            COUNT(*) as total_requests
        FROM usage_logs
        WHERE timestamp >= date('now', '-30 days')
    ''')
    total_stats = c.fetchone()
    c.execute('''
        SELECT 
            m.name,
            SUM(ul.total_tokens) as tokens,
            SUM(ul.cost) as cost,
            COUNT(*) as requests
        FROM usage_logs ul
        JOIN models m ON ul.model_id = m.id
        WHERE ul.timestamp >= date('now', '-7 days')
        GROUP BY m.name
        ORDER BY cost DESC
    ''')
    model_stats = c.fetchall()
    c.execute('''
        SELECT 
            date(timestamp) as date,
            SUM(total_tokens) as tokens,
            SUM(cost) as cost
        FROM usage_logs
        WHERE timestamp >= date('now', '-7 days')
        GROUP BY date(timestamp)
        ORDER BY date
    ''')
    daily_stats = c.fetchall()
    conn.close()
    return jsonify({
        'total': {
            'tokens': total_stats[0] or 0,
            'cost': total_stats[1] or 0,
            'requests': total_stats[2] or 0
        },
        'by_model': [
            {'name': row[0], 'tokens': row[1],
                'cost': row[2], 'requests': row[3]}
            for row in model_stats
        ],
        'daily': [
            {'date': row[0], 'tokens': row[1], 'cost': row[2]}
            for row in daily_stats
        ]
    })


@app.route('/api/models')
def get_models():
    conn = sqlite3.connect('cost_management.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, name, cost_per_token, description, is_active, created_at
        FROM models 
        ORDER BY created_at DESC
    ''')
    models = c.fetchall()
    conn.close()
    return jsonify([
        {
            'id': row[0],
            'name': row[1],
            'cost_per_token': row[2],
            'description': row[3],
            'is_active': bool(row[4]),
            'created_at': row[5]
        }
        for row in models
    ])


@app.route('/api/models', methods=['POST'])
def add_model():
    data = request.json
    conn = sqlite3.connect('cost_management.db')
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO models (name, cost_per_token, description)
            VALUES (?, ?, ?)
        ''', (data['name'], data['cost_per_token'], data.get('description', '')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    # Kiểm tra rule-based trước
    for rule in RULES:
        if re.search(rule['pattern'], prompt):
            session['messages'].append({"role": "user", "content": prompt})
            session['messages'].append(
                {"role": "assistant", "content": rule['response']})
            session.modified = True

            # Ghi log sử dụng
            model_name = "deepseek-v3.1:671b-cloud"
            model_info = get_model_info(model_name)
            if not model_info:
                return jsonify({'error': 'Model not found in database'}), 400

            model_id, model_name, cost_per_token = model_info
            prompt_tokens = estimate_tokens(prompt)
            completion_tokens = estimate_tokens(rule['response'])
            log_usage(model_id, prompt_tokens, completion_tokens, prompt[:200])

            # Giả lập hiệu ứng đánh máy cho rule-based
            def generate_response():
                response = rule['response']
                # Chia nhỏ phản hồi thành từng ký tự hoặc từ nhỏ
                for i in range(0, len(response), 5):  # Gửi 5 ký tự mỗi lần
                    yield response[i:i+5].encode('utf-8')
                    time.sleep(0.02)  # Độ trễ 20ms để tạo hiệu ứng đánh máy
                # Đảm bảo gửi toàn bộ phần còn lại
                if len(response) % 5 != 0:
                    yield response[-(len(response) % 5):].encode('utf-8')

            return Response(generate_response(), mimetype='text/plain')

    # Nếu không khớp rule-based, gửi đến Ollama
    session['messages'].append({"role": "user", "content": prompt})
    session.modified = True
    messages_copy = session['messages'][:]
    try:
        model_name = "deepseek-v3.1:671b-cloud"
        model_info = get_model_info(model_name)
        if not model_info:
            return jsonify({'error': 'Model not found in database'}), 400

        model_id, model_name, cost_per_token = model_info
        prompt_tokens = estimate_tokens(prompt)

        stream = ollama.chat(
            model=model_name,
            messages=messages_copy,
            stream=True
        )

        full_response = ""
        completion_tokens = 0

        def generate_response():
            nonlocal full_response, completion_tokens
            for chunk in stream:
                content = chunk.get('message', {}).get('content', '')
                full_response += content
                completion_tokens = estimate_tokens(full_response)
                yield content.encode('utf-8')

        response = Response(generate_response(), mimetype='text/plain')

        def save_session():
            with app.test_request_context():
                if 'messages' not in session:
                    session['messages'] = [
                        {"role": "system", "content": system_prompt}]
                session['messages'].append(
                    {"role": "assistant", "content": full_response})
                session.modified = True
                log_usage(model_id, prompt_tokens,
                          completion_tokens, prompt[:200])

        response.call_on_close(save_session)
        return response
    except Exception as e:
        print(f"Lỗi kết nối Ollama: {str(e)}")
        return jsonify({'error': f'Lỗi kết nối server: {str(e)}'}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=False)

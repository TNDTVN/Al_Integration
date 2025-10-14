from flask import Flask, render_template, request, jsonify, session, Response
import ollama
import json
import time
from datetime import datetime, timedelta
import sqlite3
import os

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

# Khởi tạo database


def init_db():
    conn = sqlite3.connect('cost_management.db')
    c = conn.cursor()

    # Bảng models
    c.execute('''
        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            cost_per_token REAL DEFAULT 0.00002,
            description TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Bảng usage logs
    c.execute('''
        CREATE TABLE IF NOT EXISTS usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER,
            prompt_tokens INTEGER DEFAULT 0,
            completion_tokens INTEGER DEFAULT 0,
            total_tokens INTEGER DEFAULT 0,
            cost REAL DEFAULT 0,
            user_message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (model_id) REFERENCES models (id)
        )
    ''')

    # Thêm models mặc định nếu chưa có
    default_models = [
        ('deepseek-v3.1:671b-cloud', 0.00002, 'DeepSeek V3.1 Cloud Model'),
        ('llama3.1:8b', 0.000015, 'Llama 3.1 8B Model'),
        ('mistral:7b', 0.000012, 'Mistral 7B Model'),
        ('gemma2:2b', 0.000008, 'Gemma 2B Model')
    ]

    for model in default_models:
        c.execute('''
            INSERT OR IGNORE INTO models (name, cost_per_token, description) 
            VALUES (?, ?, ?)
        ''', model)

    conn.commit()
    conn.close()

# Ước tính tokens (đơn giản - dựa trên số từ)


def estimate_tokens(text):
    # Ước tính: ~1 token = 4 ký tự tiếng Anh, ~1.5 token = 1 từ tiếng Việt
    words = len(text.split())
    return int(words * 1.5)

# Lấy thông tin model từ database


def get_model_info(model_name):
    conn = sqlite3.connect('cost_management.db')
    c = conn.cursor()
    c.execute(
        'SELECT id, name, cost_per_token FROM models WHERE name = ?', (model_name,))
    result = c.fetchone()
    conn.close()
    return result

# Ghi log sử dụng


def log_usage(model_id, prompt_tokens, completion_tokens, user_message):
    total_tokens = prompt_tokens + completion_tokens
    model_info = get_model_info_by_id(model_id)
    cost = total_tokens * model_info[2] if model_info else 0

    conn = sqlite3.connect('cost_management.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO usage_logs 
        (model_id, prompt_tokens, completion_tokens, total_tokens, cost, user_message)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (model_id, prompt_tokens, completion_tokens, total_tokens, cost, user_message))
    conn.commit()
    conn.close()


def get_model_info_by_id(model_id):
    conn = sqlite3.connect('cost_management.db')
    c = conn.cursor()
    c.execute(
        'SELECT id, name, cost_per_token FROM models WHERE id = ?', (model_id,))
    result = c.fetchone()
    conn.close()
    return result


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

    # Tổng chi phí và tokens
    c.execute('''
        SELECT 
            SUM(total_tokens) as total_tokens,
            SUM(cost) as total_cost,
            COUNT(*) as total_requests
        FROM usage_logs
        WHERE timestamp >= date('now', '-30 days')
    ''')
    total_stats = c.fetchone()

    # Chi phí theo model (7 ngày gần nhất)
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

    # Chi phí hàng ngày (7 ngày gần nhất)
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

    session['messages'].append({"role": "user", "content": prompt})
    session.modified = True

    messages_copy = session['messages'][:]

    try:
        # Lấy thông tin model
        model_name = "deepseek-v3.1:671b-cloud"
        model_info = get_model_info(model_name)

        if not model_info:
            return jsonify({'error': 'Model not found in database'}), 400

        model_id, model_name, cost_per_token = model_info

        # Ước tính prompt tokens
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

                # Ghi log sử dụng
                log_usage(model_id, prompt_tokens, completion_tokens,
                          prompt[:200])  # Lưu 200 ký tự đầu

        response.call_on_close(save_session)
        return response

    except Exception as e:
        print(f"Lỗi kết nối Ollama: {str(e)}")
        return jsonify({'error': f'Lỗi kết nối server: {str(e)}'}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=False)

import sqlite3


def init_db():
    conn = sqlite3.connect('cost_management.db')
    c = conn.cursor()
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


def estimate_tokens(text):
    words = len(text.split())
    return int(words * 1.5)


def get_model_info(model_name):
    conn = sqlite3.connect('cost_management.db')
    c = conn.cursor()
    c.execute(
        'SELECT id, name, cost_per_token FROM models WHERE name = ?', (model_name,))
    result = c.fetchone()
    conn.close()
    return result


def get_model_info_by_id(model_id):
    conn = sqlite3.connect('cost_management.db')
    c = conn.cursor()
    c.execute(
        'SELECT id, name, cost_per_token FROM models WHERE id = ?', (model_id,))
    result = c.fetchone()
    conn.close()
    return result


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

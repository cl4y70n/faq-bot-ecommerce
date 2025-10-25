import sqlite3
import json
from pathlib import Path

DB = Path('data/faq_bot.db')
def init_db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, query TEXT, answer TEXT, sources TEXT)''')
    conn.commit()
    conn.close()

def save_query_log(query, answer, sources):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('INSERT INTO logs (query, answer, sources) VALUES (?, ?, ?)', (query, answer, json.dumps(sources, ensure_ascii=False)))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT id, query, answer, sources FROM logs ORDER BY id DESC LIMIT 200')
    rows = c.fetchall()
    conn.close()
    out = []
    import json
    for r in rows:
        out.append({'id': r[0], 'query': r[1], 'answer': r[2], 'sources': json.loads(r[3])})
    return out

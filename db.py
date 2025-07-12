import sqlite3
import os

DB_FILE = "logs.db"

def init_db():
    # Only create the database if it doesn't exist
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                level TEXT,
                message TEXT
            )
        """)
        conn.commit()
        conn.close()

def clear_db():
    """Clear all data from the database"""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    init_db()

def insert_log_row(timestamp, level, message):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO logs (timestamp, level, message) VALUES (?, ?, ?)",
              (timestamp, level, message))
    conn.commit()
    conn.close()

def query_logs(limit=1000):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    df = None
    try:
        df = c.execute("SELECT timestamp, level, message FROM logs ORDER BY id LIMIT ?", (limit,))
        rows = df.fetchall()
    finally:
        conn.close()
    return rows

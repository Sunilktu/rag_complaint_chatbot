import sqlite3
from datetime import datetime

conn = sqlite3.connect("complaints.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS complaints (
        complaint_id TEXT PRIMARY KEY,
        name TEXT,
        phone_number TEXT,
        email TEXT,
        complaint_details TEXT,
        created_at TEXT
    )
''')
conn.commit()

def insert_complaint(complaint_id, name, phone, email, details):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO complaints (complaint_id, name, phone_number, email, complaint_details, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (complaint_id, name, phone, email, details, now))
    conn.commit()

def get_complaint(complaint_id):
    cursor.execute("SELECT * FROM complaints WHERE complaint_id=?", (complaint_id,))
    return cursor.fetchone()


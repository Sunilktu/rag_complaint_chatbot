# Placeholder for main.py
from typing import List, TypedDict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
import sqlite3
# ======================
# SQLite Database Setup
# ======================
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

# ======================
# FastAPI Backend
# ======================
app = FastAPI()

class Complaint(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    complaint_details: str

@app.post("/complaints")
def register_complaint(complaint: Complaint):
    import uuid
    complaint_id = uuid.uuid4().hex[:6].upper()
    insert_complaint(complaint_id, complaint.name, complaint.phone_number, complaint.email, complaint.complaint_details)
    return {"complaint_id": complaint_id, "message": "Complaint created successfully"}

@app.get("/complaints/{complaint_id}")
def get_complaint_status(complaint_id: str):
    record = get_complaint(complaint_id)
    if not record:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return {
        "complaint_id": record[0],
        "name": record[1],
        "phone_number": record[2],
        "email": record[3],
        "complaint_details": record[4],
        "created_at": record[5]
    }
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
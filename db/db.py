import sqlite3
from app.config import Config

def init_db():
    conn=sqlite3.connect(Config.DB_PATH)
    cursor=conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT, dob TEXT, aadhar TEXT,
                        phone TEXT UNIQUE, bank_account TEXT, ifsc_code TEXT,
                        bank_name TEXT, branch TEXT,
                        employer TEXT, onboarding TIMESTAMP, 
                        aadhar_photo BLOB, document BLOB, passbook BLOB)''')
    conn.commit()
    conn.close()

def execute_query(query,params=(),fetchone=False,commit=False):
    conn=sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query,params)
    result = cursor.fetchone() if fetchone else cursor.fetchall()
    if commit:
        conn.commit()
    conn.close
    return result
import sqlite3
from flask import current_app
import pytesseract, pandas as pd, re, tempfile, base64
from PIL import Image, ImageFilter, ImageEnhance
from pdf2image import convert_from_path

def get_db():
    return sqlite3.connect(current_app.config["DB_PATH"])

def process_document(file):
    if file.filename.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.read())
        return " ".join(pytesseract.image_to_string(preprocess_image(img)) for img in convert_from_path(temp_file.name))
    else:
        return pytesseract.image_to_string(preprocess_image(Image.open(file)))

def preprocess_image(img):
    img = img.convert("L").filter(ImageFilter.SHARPEN)
    return ImageEnhance.Contrast(img).enhance(2)

def extract_aadhaar(text):
    match = re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text)
    return match.group().replace(" ", "") if match else None

def extract_bank_details(text):
    acc = re.search(r"\b\d{9,18}\b", text)
    ifsc = re.search(r"\b[A-Z]{4}0[A-Z0-9]{6}\b", text)
    return (acc.group() if acc else None, ifsc.group() if ifsc else None)

def get_ifsc_details(ifsc_code):
    df = pd.read_csv(current_app.config["IFSC_PATH"])
    match = df[df["IFSC"] == ifsc_code]
    return (match.iloc[0]["BANK"], match.iloc[0]["BRANCH"]) if not match.empty else (None, None)

def insert_employee(data, photo, doc, passbook, acc, bank, branch):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''INSERT INTO employees (name, dob, aadhar, phone, bank_account, ifsc_code, 
                   bank_name, branch, employer, onboarding, aadhar_photo, document, passbook) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), ?, ?, ?)''',
                (data["name"], data["dob"], data["aadhar"], data["phone"], acc, data["ifsc_code"], 
                 bank, branch, data.get("employer"), photo.read(), doc.read() if doc else None, passbook.read() if passbook else None))
    conn.commit()
    conn.close()

def get_employee_by_phone(phone):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE phone=?", (phone,))
    emp = cur.fetchone()
    conn.close()
    if emp:
        return {
            "id": emp[0], "name": emp[1], "dob": emp[2], "aadhar": emp[3], "phone": emp[4],
            "bank_account": emp[5], "ifsc_code": emp[6], "bank_name": emp[7], "branch": emp[8],
            "employer": emp[9], "onboarding": emp[10],
            "aadhar_photo": base64.b64encode(emp[11]).decode() if emp[11] else None,
            "document": base64.b64encode(emp[12]).decode() if emp[12] else None,
            "passbook": base64.b64encode(emp[13]).decode() if emp[13] else None
        }

def update_employee_by_phone(data):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE employees SET name=?, dob=?, aadhar=?, ifsc_code=? WHERE phone=?",
                (data["name"], data["dob"], data["aadhar"], data["ifsc_code"], data["phone"]))
    conn.commit()
    conn.close()

def delete_employee_by_phone(phone):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE phone=?", (phone,))
    conn.commit()
    conn.close()

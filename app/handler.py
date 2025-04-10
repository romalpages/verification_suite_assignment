from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from app.utils import *
import logging

logger = logging.getLogger(__name__)

# ✅ Fix: Dictionary syntax and format
users = {
    "romal": "romal123"
}

def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # ✅ Fix: Correct dictionary lookup
    if users.get(username) != password:
        logger.error("Invalid login attempt for user: %s", username)
        return jsonify({"error": "Invalid Credentials"}), 401

    token = create_access_token(identity=username)
    logger.info("Login successful for user: %s", username)
    
    # ✅ Fix: Incorrect key in response
    return jsonify({"token": token})


@jwt_required()
def create_employee():
    data = request.form
    aadhar_photo = request.files.get("aadhar_photo")
    document = request.files.get("document")
    passbook = request.files.get("passbook")

    extracted_aadhaar = extract_aadhaar(process_document(document)) if document else None
    bank_account, ifsc = extract_bank_details(process_document(passbook)) if passbook else (None, None)
    bank_name, branch = get_ifsc_details(data.get("ifsc_code"))

    insert_employee(data, aadhar_photo, document, passbook, bank_account, bank_name, branch)
    return jsonify({"message": "Employee created successfully"}), 201


@jwt_required()
def get_employee():
    phone = request.get_json().get("phone")
    employee = get_employee_by_phone(phone)
    if employee:
        return jsonify(employee)
    return jsonify({"error": "Employee not found"}), 404


@jwt_required()
def update_employee():
    data = request.form
    update_employee_by_phone(data)
    return jsonify({"message": "Employee updated successfully"})


@jwt_required()
def delete_employee():
    phone = request.get_json().get("phone")
    delete_employee_by_phone(phone)
    return jsonify({"message": "Employee deleted successfully"})

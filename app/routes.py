from flask import Blueprint
from app.handler import login, create_employee, get_employee, update_employee, delete_employee

def register_routes(app):
    app.add_url_rule('/login', view_func=login, methods=['POST'])
    app.add_url_rule('/create_employee', view_func=create_employee, methods=['POST'])
    app.add_url_rule('/get_employee', view_func=get_employee, methods=['POST'])
    app.add_url_rule('/update_employee', view_func=update_employee, methods=['PUT'])
    app.add_url_rule('/delete_employee', view_func=delete_employee, methods=['DELETE'])

# app/config.py

import os

class Config:
    JWT_SECRET_KEY = "super-secret-key"
    LOG_FILE = "logs/app.log"
    DB_PATH = "db/employee_verification.db"
    IFSC_PATH = "E:/internship/assignment_suite/db/IFSC.csv"

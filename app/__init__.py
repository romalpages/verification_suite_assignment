from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes import register_routes
from db.db import init_db
from app.logger import configure_logging

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    configure_logging()
    init_db()

    jwt.init_app(app)
    register_routes(app)

    return app
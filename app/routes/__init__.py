# app/__init__.py
# Регистрация Blueprints в __init__.py


# from flask import Flask
from app.routes.questions import questions_bp
from app.routes.responses import responses_bp
# from config import DevelopmentConfig

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(DevelopmentConfig)
#     app.register_blueprint(questions_bp)
#     app.register_blueprint(responses_bp)
#     return app
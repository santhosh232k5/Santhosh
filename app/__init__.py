from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .models import db
from .routes.auth import auth_bp
from .routes.worker import worker_bp
from .routes.booking import booking_bp
from .routes.chatbot import chatbot_bp
from .routes.admin import admin_bp
from .routes.frontend import frontend_bp


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/smart_home.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "change-this-in-production"

    CORS(app)
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(frontend_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(worker_bp, url_prefix="/api/workers")
    app.register_blueprint(booking_bp, url_prefix="/api/bookings")
    app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app

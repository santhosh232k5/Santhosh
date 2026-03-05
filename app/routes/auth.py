from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from ..models import db
from ..models.admin import Admin
from ..models.user import User
from ..models.worker import Worker
from ..utils.constants import SERVICE_CATEGORIES

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register_user():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"error": "Name, email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(name=name, email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201


@auth_bp.post("/register-worker")
def register_worker():
    data = request.get_json() or {}
    required = ["name", "email", "password", "service_category", "latitude", "longitude"]
    if any(data.get(field) in [None, ""] for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    if data["service_category"] not in SERVICE_CATEGORIES:
        return jsonify({"error": "Invalid service category"}), 400

    if Worker.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    worker = Worker(
        name=data["name"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        service_category=data["service_category"],
        phone=data.get("phone"),
        latitude=float(data["latitude"]),
        longitude=float(data["longitude"]),
        is_available=True,
        is_approved=False,
    )
    db.session.add(worker)
    db.session.commit()
    return jsonify({"message": "Worker registered. Waiting for admin approval.", "worker": worker.to_dict()}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email_or_username = data.get("email") or data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    if role == "user":
        account = User.query.filter_by(email=email_or_username).first()
    elif role == "worker":
        account = Worker.query.filter_by(email=email_or_username).first()
    elif role == "admin":
        account = Admin.query.filter_by(username=email_or_username).first()
    else:
        return jsonify({"error": "Invalid role"}), 400

    if not account or not check_password_hash(account.password_hash, password or ""):
        return jsonify({"error": "Invalid credentials"}), 401

    if role == "worker" and not account.is_approved:
        return jsonify({"error": "Worker account not approved by admin"}), 403

    token = create_access_token(identity=f"{role}:{account.id}", additional_claims={"role": role})
    return jsonify({
        "access_token": token,
        "role": role,
        "profile": account.to_dict(),
    })


@auth_bp.post("/logout")
def logout():
    return jsonify({"message": "Logout successful on client side. Discard JWT token."})

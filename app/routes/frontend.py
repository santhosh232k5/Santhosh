from flask import Blueprint, render_template

frontend_bp = Blueprint("frontend", __name__)


@frontend_bp.get("/")
def home_page():
    return render_template("index.html")


@frontend_bp.get("/login")
def login_page():
    return render_template("login.html")


@frontend_bp.get("/register")
def register_page():
    return render_template("register.html")


@frontend_bp.get("/user-dashboard")
def user_dashboard_page():
    return render_template("user_dashboard.html")


@frontend_bp.get("/worker-dashboard")
def worker_dashboard_page():
    return render_template("worker_dashboard.html")


@frontend_bp.get("/admin-dashboard")
def admin_dashboard_page():
    return render_template("admin_dashboard.html")

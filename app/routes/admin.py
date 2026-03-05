from sqlalchemy import func
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, jwt_required

from ..models import db
from ..models.booking import Booking
from ..models.user import User
from ..models.worker import Worker

admin_bp = Blueprint("admin", __name__)


def _check_admin():
    return get_jwt().get("role") == "admin"


@admin_bp.get("")
@jwt_required()
def admin_overview():
    if not _check_admin():
        return jsonify({"error": "Forbidden"}), 403

    stats = {
        "total_users": User.query.count(),
        "total_workers": Worker.query.count(),
        "approved_workers": Worker.query.filter_by(is_approved=True).count(),
        "total_bookings": Booking.query.count(),
        "pending_bookings": Booking.query.filter_by(status="Pending").count(),
        "completed_bookings": Booking.query.filter_by(status="Completed").count(),
    }

    usage = (
        db.session.query(Booking.service_category, func.count(Booking.id))
        .group_by(Booking.service_category)
        .all()
    )

    return jsonify({
        "stats": stats,
        "service_usage": [{"service": svc, "count": cnt} for svc, cnt in usage],
        "users": [u.to_dict() for u in User.query.all()],
        "workers": [w.to_dict() for w in Worker.query.all()],
        "bookings": [b.to_dict() for b in Booking.query.all()],
    })


@admin_bp.put("/workers/<int:worker_id>/approve")
@jwt_required()
def approve_worker(worker_id: int):
    if not _check_admin():
        return jsonify({"error": "Forbidden"}), 403
    worker = Worker.query.get(worker_id)
    if not worker:
        return jsonify({"error": "Worker not found"}), 404
    worker.is_approved = True
    db.session.commit()
    return jsonify({"message": "Worker approved", "worker": worker.to_dict()})


@admin_bp.delete("/workers/<int:worker_id>")
@jwt_required()
def remove_worker(worker_id: int):
    if not _check_admin():
        return jsonify({"error": "Forbidden"}), 403
    worker = Worker.query.get(worker_id)
    if not worker:
        return jsonify({"error": "Worker not found"}), 404
    db.session.delete(worker)
    db.session.commit()
    return jsonify({"message": "Worker removed"})

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from ..models import db
from ..models.booking import Booking
from ..models.worker import Worker
from ..utils.constants import SERVICE_CATEGORIES

worker_bp = Blueprint("worker", __name__)


def _current_worker():
    identity = get_jwt_identity()
    _, worker_id = identity.split(":")
    return Worker.query.get(int(worker_id))


@worker_bp.get("")
def list_workers():
    service = request.args.get("service")
    query = Worker.query.filter_by(is_approved=True)
    if service:
        query = query.filter_by(service_category=service)
    workers = [w.to_dict() for w in query.all()]
    return jsonify(workers)


@worker_bp.get("/categories")
def categories():
    return jsonify(SERVICE_CATEGORIES)


@worker_bp.get("/dashboard")
@jwt_required()
def worker_dashboard():
    if get_jwt().get("role") != "worker":
        return jsonify({"error": "Forbidden"}), 403

    worker = _current_worker()
    bookings = [b.to_dict() for b in Booking.query.filter_by(worker_id=worker.id).order_by(Booking.id.desc()).all()]
    return jsonify({"worker": worker.to_dict(), "bookings": bookings})


@worker_bp.put("/profile")
@jwt_required()
def update_worker_profile():
    if get_jwt().get("role") != "worker":
        return jsonify({"error": "Forbidden"}), 403

    worker = _current_worker()
    data = request.get_json() or {}

    for key in ["name", "phone", "service_category", "is_available"]:
        if key in data:
            if key == "service_category" and data[key] not in SERVICE_CATEGORIES:
                return jsonify({"error": "Invalid service category"}), 400
            setattr(worker, key, data[key])

    if "latitude" in data:
        worker.latitude = float(data["latitude"])
    if "longitude" in data:
        worker.longitude = float(data["longitude"])

    db.session.commit()
    return jsonify({"message": "Profile updated", "worker": worker.to_dict()})


@worker_bp.put("/bookings/<int:booking_id>")
@jwt_required()
def update_booking_status(booking_id: int):
    if get_jwt().get("role") != "worker":
        return jsonify({"error": "Forbidden"}), 403

    worker = _current_worker()
    booking = Booking.query.filter_by(id=booking_id, worker_id=worker.id).first()
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    status = (request.get_json() or {}).get("status")
    if status not in ["Accepted", "Rejected", "Completed"]:
        return jsonify({"error": "Invalid status"}), 400

    booking.status = status
    if status == "Completed":
        worker.is_available = True
    elif status == "Accepted":
        worker.is_available = False

    db.session.commit()
    return jsonify({"message": "Booking updated", "booking": booking.to_dict()})

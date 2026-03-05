import random
import string

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from ..models import db
from ..models.booking import Booking
from ..models.user import User
from ..models.worker import Worker
from ..utils.constants import PAYMENT_METHODS, SERVICE_CATEGORIES
from ..utils.distance import haversine_distance

booking_bp = Blueprint("booking", __name__)


def _booking_code() -> str:
    return "BK" + "".join(random.choices(string.digits, k=6))


@booking_bp.post("")
@jwt_required()
def create_booking():
    if get_jwt().get("role") != "user":
        return jsonify({"error": "Only users can create bookings"}), 403

    user_id = int(get_jwt_identity().split(":")[1])
    user = User.query.get(user_id)
    data = request.get_json() or {}

    service_category = data.get("service_category")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    payment_method = data.get("payment_method")

    if service_category not in SERVICE_CATEGORIES:
        return jsonify({"error": "Invalid service category"}), 400
    if payment_method not in PAYMENT_METHODS:
        return jsonify({"error": "Invalid payment method"}), 400

    if latitude is None or longitude is None:
        return jsonify({"error": "Location coordinates required"}), 400

    user.latitude = float(latitude)
    user.longitude = float(longitude)

    workers = Worker.query.filter_by(
        service_category=service_category,
        is_available=True,
        is_approved=True,
    ).all()

    if not workers:
        return jsonify({"error": "No workers available for selected service"}), 404

    nearest = min(
        workers,
        key=lambda w: haversine_distance(user.latitude, user.longitude, w.latitude, w.longitude),
    )
    distance_km = haversine_distance(user.latitude, user.longitude, nearest.latitude, nearest.longitude)
    eta_minutes = max(10, int(distance_km * 6))

    booking = Booking(
        booking_id=_booking_code(),
        user_id=user.id,
        worker_id=nearest.id,
        service_category=service_category,
        user_latitude=user.latitude,
        user_longitude=user.longitude,
        status="Pending",
        payment_method=payment_method,
        estimated_arrival_minutes=eta_minutes,
    )
    db.session.add(booking)
    db.session.commit()

    return jsonify(
        {
            "message": "Booking created",
            "booking": booking.to_dict(),
            "assigned_worker": nearest.to_dict(),
            "distance_km": round(distance_km, 2),
        }
    ), 201


@booking_bp.get("")
@jwt_required()
def list_bookings():
    role = get_jwt().get("role")
    identity_id = int(get_jwt_identity().split(":")[1])

    if role == "user":
        bookings = Booking.query.filter_by(user_id=identity_id).order_by(Booking.id.desc()).all()
    elif role == "worker":
        bookings = Booking.query.filter_by(worker_id=identity_id).order_by(Booking.id.desc()).all()
    else:
        bookings = Booking.query.order_by(Booking.id.desc()).all()

    return jsonify([b.to_dict() for b in bookings])


@booking_bp.get("/<booking_code>")
@jwt_required()
def track_booking(booking_code: str):
    booking = Booking.query.filter_by(booking_id=booking_code).first()
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify(booking.to_dict())

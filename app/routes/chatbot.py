from flask import Blueprint, jsonify, request

from ..models.worker import Worker
from ..utils.chatbot import detect_location, detect_service
from ..utils.distance import haversine_distance

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.post("")
def chatbot_assistant():
    message = (request.get_json() or {}).get("message", "")
    service = detect_service(message)
    location = detect_location(message)

    if not service:
        return jsonify({"reply": "Please mention the service you need (e.g., Plumbing or Electrical Works)."})
    if not location:
        return jsonify({"reply": "Please share your city name or GPS coordinates (lat long)."})

    lat, lon = location
    workers = Worker.query.filter_by(service_category=service, is_approved=True, is_available=True).all()
    if not workers:
        return jsonify({"reply": f"No {service} technicians are available nearby right now."})

    nearest = min(workers, key=lambda w: haversine_distance(lat, lon, w.latitude, w.longitude))
    distance_km = haversine_distance(lat, lon, nearest.latitude, nearest.longitude)
    eta = max(10, int(distance_km * 6))

    return jsonify(
        {
            "reply": "Great! I found the nearest technician.",
            "technician_name": nearest.name,
            "service_type": service,
            "estimated_arrival_time": f"{eta} minutes",
            "distance_km": round(distance_km, 2),
        }
    )

from datetime import datetime

from . import db


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey("worker.id"), nullable=False)
    service_category = db.Column(db.String(80), nullable=False)
    user_latitude = db.Column(db.Float, nullable=False)
    user_longitude = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    payment_method = db.Column(db.String(30), nullable=False)
    estimated_arrival_minutes = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "booking_id": self.booking_id,
            "user_id": self.user_id,
            "worker_id": self.worker_id,
            "service_category": self.service_category,
            "user_latitude": self.user_latitude,
            "user_longitude": self.user_longitude,
            "status": self.status,
            "payment_method": self.payment_method,
            "estimated_arrival_minutes": self.estimated_arrival_minutes,
            "created_at": self.created_at.isoformat(),
        }

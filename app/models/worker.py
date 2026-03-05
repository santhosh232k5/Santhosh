from datetime import datetime

from . import db


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    service_category = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship("Booking", backref="worker", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "service_category": self.service_category,
            "phone": self.phone,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "is_available": self.is_available,
            "is_approved": self.is_approved,
            "created_at": self.created_at.isoformat(),
        }

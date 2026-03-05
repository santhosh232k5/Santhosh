from werkzeug.security import generate_password_hash

from app import create_app
from app.models import db
from app.models.admin import Admin
from app.models.worker import Worker

app = create_app()


def seed():
    with app.app_context():
        db.create_all()

        if not Admin.query.filter_by(username="admin").first():
            admin = Admin(username="admin", password_hash=generate_password_hash("admin123"))
            db.session.add(admin)

        workers = [
            ("Raj Electric", "raj.electric@example.com", "Electrical Works", 12.975, 77.60),
            ("Vikram Plumber", "vikram.plumb@example.com", "Plumbing", 12.98, 77.58),
            ("Arun Carpenter", "arun.carp@example.com", "Carpentry", 13.01, 77.59),
            ("Kumar Painter", "kumar.paint@example.com", "Painting", 12.96, 77.62),
            ("Suresh Mason", "suresh.mason@example.com", "Masonry", 12.95, 77.57),
            ("Asha CleanPro", "asha.clean@example.com", "Cleaning", 12.99, 77.61),
            ("Neha Repair", "neha.repair@example.com", "Appliance Repair", 12.97, 77.56),
        ]

        for name, email, category, lat, lon in workers:
            if not Worker.query.filter_by(email=email).first():
                db.session.add(
                    Worker(
                        name=name,
                        email=email,
                        password_hash=generate_password_hash("worker123"),
                        service_category=category,
                        latitude=lat,
                        longitude=lon,
                        is_available=True,
                        is_approved=True,
                    )
                )

        db.session.commit()
        print("Demo data seeded: admin/admin123 and workers/worker123")


if __name__ == "__main__":
    seed()

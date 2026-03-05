from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from .user import User  # noqa: E402,F401
from .worker import Worker  # noqa: E402,F401
from .booking import Booking  # noqa: E402,F401
from .admin import Admin  # noqa: E402,F401

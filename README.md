# Smart Home Service Assistant (Flask + SQLite)

A complete home service booking platform inspired by Urban Company.

## Features
- User, Worker, and Admin authentication with JWT.
- Worker onboarding + admin approval flow.
- Booking assignment to nearest approved available worker via Haversine formula.
- Booking tracking and worker status updates.
- AI-style chatbot using keyword and location extraction.
- Admin analytics dashboard for users, workers, bookings, and service usage.
- Modern light-blue responsive frontend with floating chatbot widget.

## Project Structure
```
app/
  models/
  routes/
  utils/
  templates/
  static/
  database/
app.py
seed_data.py
requirements.txt
```

## Setup
1. Create virtualenv and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Initialize database and demo records:
   ```bash
   python seed_data.py
   ```
3. Run application:
   ```bash
   python app.py
   ```
4. Open `http://localhost:5000`.

## Demo Credentials
- Admin: `admin` / `admin123`
- Worker seed password: `worker123`

## API Endpoints
- `POST /api/auth/register`
- `POST /api/auth/register-worker`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/workers`
- `GET /api/workers/dashboard`
- `PUT /api/workers/profile`
- `PUT /api/workers/bookings/<id>`
- `POST /api/bookings`
- `GET /api/bookings`
- `GET /api/bookings/<booking_id>`
- `POST /api/chatbot`
- `GET /api/admin`
- `PUT /api/admin/workers/<worker_id>/approve`
- `DELETE /api/admin/workers/<worker_id>`

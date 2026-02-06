from datetime import datetime
from math import radians, cos, sin, asin, sqrt

from flask import Flask, jsonify, request

from database import execute, fetch_all, fetch_one, init_db

app = Flask(__name__)


def haversine_distance_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371 * c


@app.before_first_request
def setup_database():
    init_db()


@app.get("/api/user/<int:user_id>")
def get_user(user_id):
    user = fetch_one("SELECT * FROM users WHERE user_id = ?", [user_id])
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@app.post("/api/register")
def register_user():
    payload = request.get_json(force=True)
    required_fields = ["user_id", "name", "phone", "region", "pin"]
    if not all(field in payload and payload[field] for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = fetch_one("SELECT user_id FROM users WHERE user_id = ?", [payload["user_id"]])
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    execute(
        """
        INSERT INTO users (user_id, name, phone, region, pin, position, is_blocked)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            payload["user_id"],
            payload["name"],
            payload["phone"],
            payload["region"],
            payload["pin"],
            payload.get("position"),
            payload.get("is_blocked", 0),
        ],
    )
    return jsonify({"status": "registered"}), 201


@app.post("/api/login")
def login_user():
    payload = request.get_json(force=True)
    if "user_id" not in payload or "pin" not in payload:
        return jsonify({"error": "Missing credentials"}), 400

    user = fetch_one(
        "SELECT user_id, name, region, position, is_blocked FROM users WHERE user_id = ? AND pin = ?",
        [payload["user_id"], payload["pin"]],
    )
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    if user.get("is_blocked"):
        return jsonify({"error": "User is blocked"}), 403
    return jsonify(user)


@app.get("/api/doctors")
def list_doctors():
    doctors = fetch_all("SELECT * FROM doctors WHERE is_active = 1")
    return jsonify(doctors)


@app.get("/api/doctors/<int:doctor_id>")
def get_doctor(doctor_id):
    doctor = fetch_one("SELECT * FROM doctors WHERE id = ?", [doctor_id])
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
    return jsonify(doctor)


@app.get("/api/doctors/nearby")
def get_doctors_nearby():
    try:
        lat = float(request.args.get("lat", ""))
        lon = float(request.args.get("lon", ""))
        radius_m = float(request.args.get("radius", 0))
    except ValueError:
        return jsonify({"error": "Invalid coordinates"}), 400

    radius_km = radius_m / 1000
    doctors = fetch_all("SELECT * FROM doctors WHERE latitude IS NOT NULL AND longitude IS NOT NULL")
    nearby = []
    for doctor in doctors:
        distance = haversine_distance_km(lat, lon, doctor["latitude"], doctor["longitude"])
        if distance <= radius_km:
            doctor["distance_km"] = round(distance, 3)
            nearby.append(doctor)
    return jsonify(nearby)


@app.post("/api/doctors")
def create_doctor():
    payload = request.get_json(force=True)
    if "full_name" not in payload:
        return jsonify({"error": "Missing full_name"}), 400

    doctor_id = execute(
        """
        INSERT INTO doctors (
            full_name, specialty, organization, phone, address, latitude, longitude,
            region, category, notes, is_active
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            payload["full_name"],
            payload.get("specialty"),
            payload.get("organization"),
            payload.get("phone"),
            payload.get("address"),
            payload.get("latitude"),
            payload.get("longitude"),
            payload.get("region"),
            payload.get("category"),
            payload.get("notes"),
            payload.get("is_active", 1),
        ],
    )
    return jsonify({"id": doctor_id}), 201


@app.get("/api/visits")
def list_visits():
    visits = fetch_all("SELECT * FROM visits")
    return jsonify(visits)


@app.get("/api/visits/user/<int:user_id>")
def list_user_visits(user_id):
    visits = fetch_all("SELECT * FROM visits WHERE user_id = ?", [user_id])
    return jsonify(visits)


@app.post("/api/visits")
def create_visit():
    payload = request.get_json(force=True)
    required_fields = ["user_id", "visit_type", "visit_date"]
    if not all(field in payload and payload[field] for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    visit_date = payload["visit_date"]
    try:
        datetime.fromisoformat(visit_date)
    except ValueError:
        return jsonify({"error": "visit_date must be ISO-8601"}), 400

    visit_id = execute(
        """
        INSERT INTO visits (
            user_id, visit_type, target_id, target_name, visit_date, duration, topics, result,
            products_presented, orders_received, latitude, longitude, location_verified, photo_url,
            notes, next_visit_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            payload["user_id"],
            payload["visit_type"],
            payload.get("target_id"),
            payload.get("target_name"),
            payload["visit_date"],
            payload.get("duration"),
            payload.get("topics"),
            payload.get("result"),
            payload.get("products_presented"),
            payload.get("orders_received"),
            payload.get("latitude"),
            payload.get("longitude"),
            payload.get("location_verified", 0),
            payload.get("photo_url"),
            payload.get("notes"),
            payload.get("next_visit_date"),
        ],
    )
    return jsonify({"id": visit_id}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

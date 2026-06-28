import sqlite3
from datetime import datetime, timezone
from typing import List, Dict, Any

DB_FILE = "road_prediction.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        road_age REAL,
        traffic_volume REAL,
        heavy_vehicle_percentage REAL,
        rainfall REAL,
        temperature REAL,
        crack_length REAL,
        pothole_count INTEGER,
        surface_condition_index REAL,
        last_maintenance_years REAL,
        probability REAL,
        risk TEXT,
        location TEXT,
        reported_by TEXT,
        status TEXT,
        department_note TEXT,
        timestamp TEXT,
        status_updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()


initialize_database()


def save_prediction(data: dict) -> str:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions (
        road_age,
        traffic_volume,
        heavy_vehicle_percentage,
        rainfall,
        temperature,
        crack_length,
        pothole_count,
        surface_condition_index,
        last_maintenance_years,
        probability,
        risk,
        location,
        reported_by,
        status,
        department_note,
        timestamp,
        status_updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("road_age"),
        data.get("traffic_volume"),
        data.get("heavy_vehicle_percentage"),
        data.get("rainfall"),
        data.get("temperature"),
        data.get("crack_length"),
        data.get("pothole_count"),
        data.get("surface_condition_index"),
        data.get("last_maintenance_years"),
        data.get("probability"),
        data.get("risk"),
        data.get("location"),
        data.get("reported_by"),
        "Pending",
        "",
        datetime.now(timezone.utc).isoformat(),
        None
    ))

    conn.commit()
    prediction_id = str(cursor.lastrowid)
    conn.close()

    return prediction_id


def fetch_all_predictions(limit=100, risk_filter=None):
    conn = get_connection()
    cursor = conn.cursor()

    if risk_filter and risk_filter != "All":
        cursor.execute(
            "SELECT * FROM predictions WHERE risk=? ORDER BY id DESC LIMIT ?",
            (risk_filter, limit)
        )
    else:
        cursor.execute(
            "SELECT * FROM predictions ORDER BY id DESC LIMIT ?",
            (limit,)
        )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def fetch_prediction_by_id(prediction_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM predictions WHERE id=?",
        (prediction_id,)
    )

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def update_prediction_status(prediction_id, status, note=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE predictions
    SET status=?,
        department_note=?,
        status_updated_at=?
    WHERE id=?
    """, (
        status,
        note,
        datetime.now(timezone.utc).isoformat(),
        prediction_id
    ))

    conn.commit()
    success = cursor.rowcount > 0
    conn.close()

    return success


def fetch_history(limit=50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM predictions ORDER BY id DESC LIMIT ?",
        (limit,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def is_connected():
    try:
        conn = get_connection()
        conn.execute("SELECT 1")
        conn.close()
        return True
    except Exception:
        return False
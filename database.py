import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("phs_app.db")
SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with get_connection() as connection:
        connection.executescript(schema)
        connection.commit()


def fetch_one(query, params=None):
    with get_connection() as connection:
        cursor = connection.execute(query, params or [])
        row = cursor.fetchone()
        return dict(row) if row else None


def fetch_all(query, params=None):
    with get_connection() as connection:
        cursor = connection.execute(query, params or [])
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def execute(query, params=None):
    with get_connection() as connection:
        cursor = connection.execute(query, params or [])
        connection.commit()
        return cursor.lastrowid

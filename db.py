"""
SQLite-backed store for already-notified flights.

Prevents sending duplicate Telegram messages for the same
(airline, origin, destination, date) combination.
"""
import sqlite3
import logging
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / "flights.db"

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS notified (
    airline     TEXT    NOT NULL,
    origin      TEXT    NOT NULL,
    destination TEXT    NOT NULL,
    dep_date    TEXT    NOT NULL,
    price       INTEGER,
    notified_at TEXT    NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (airline, origin, destination, dep_date)
);
"""


@contextmanager
def _connect():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def setup_db() -> None:
    """Create the database and tables if they do not exist."""
    with _connect() as conn:
        conn.execute(_CREATE_TABLE)
    logger.debug("Database ready at %s", DB_PATH)


def already_notified(airline: str, origin: str, destination: str, dep_date: str) -> bool:
    """Return True if a notification was already sent for this flight."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM notified WHERE airline=? AND origin=? AND destination=? AND dep_date=?",
            (airline, origin, destination, dep_date),
        ).fetchone()
    return row is not None


def mark_notified(airline: str, origin: str, destination: str, dep_date: str, price: int | None) -> None:
    """Record that a notification has been sent for this flight."""
    with _connect() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO notified (airline, origin, destination, dep_date, price)
            VALUES (?, ?, ?, ?, ?)
            """,
            (airline, origin, destination, dep_date, price),
        )
    logger.debug("Marked notified: %s %s→%s %s", airline, origin, destination, dep_date)

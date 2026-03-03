"""Tests for the SQLite notification store (db.py)."""
import os
import tempfile

import pytest

# Override DB_PATH before importing db module
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ["DB_PATH"] = _tmp.name

from db import already_notified, mark_notified, setup_db  # noqa: E402


@pytest.fixture(autouse=True)
def _fresh_db():
    """Re-create a clean database for every test."""
    # Remove leftover data from a prior test
    import sqlite3
    conn = sqlite3.connect(os.environ["DB_PATH"])
    conn.execute("DROP TABLE IF EXISTS notified")
    conn.close()
    setup_db()
    yield


def test_setup_creates_table():
    """setup_db should be idempotent and not raise."""
    setup_db()  # second call should be fine


def test_mark_and_already_notified():
    assert not already_notified("S7", "DME", "VVO", "2025-06-01")
    mark_notified("S7", "DME", "VVO", "2025-06-01", 7500)
    assert already_notified("S7", "DME", "VVO", "2025-06-01")


def test_different_dates_not_conflated():
    mark_notified("S7", "DME", "VVO", "2025-06-01", 7500)
    assert not already_notified("S7", "DME", "VVO", "2025-06-02")


def test_different_airlines_not_conflated():
    mark_notified("S7", "DME", "VVO", "2025-06-01", 7500)
    assert not already_notified("Аэрофлот", "DME", "VVO", "2025-06-01")


def test_mark_notified_upsert():
    """Calling mark_notified twice for the same key should not raise."""
    mark_notified("S7", "DME", "VVO", "2025-06-01", 7500)
    mark_notified("S7", "DME", "VVO", "2025-06-01", 8000)  # updated price
    assert already_notified("S7", "DME", "VVO", "2025-06-01")

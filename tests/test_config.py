"""Tests for configuration validation (config.py)."""
import os

import pytest

from config import validate


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    """Start each test with a minimal valid environment."""
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.setenv("CHAT_ID", "12345")
    monkeypatch.setenv("DAYS_AHEAD", "45")
    # Remove optional vars so they don't leak between tests
    monkeypatch.delenv("MIN_DELAY", raising=False)
    monkeypatch.delenv("MAX_DELAY", raising=False)


def test_valid_config():
    assert validate() is True


def test_missing_bot_token(monkeypatch):
    monkeypatch.delenv("BOT_TOKEN")
    assert validate() is False


def test_missing_chat_id(monkeypatch):
    monkeypatch.delenv("CHAT_ID")
    assert validate() is False


def test_dry_run_skips_telegram_check(monkeypatch):
    monkeypatch.delenv("BOT_TOKEN")
    monkeypatch.delenv("CHAT_ID")
    assert validate(require_telegram=False) is True


def test_invalid_days_ahead(monkeypatch):
    monkeypatch.setenv("DAYS_AHEAD", "abc")
    assert validate() is False


def test_zero_days_ahead(monkeypatch):
    monkeypatch.setenv("DAYS_AHEAD", "0")
    assert validate() is False


def test_negative_delay(monkeypatch):
    monkeypatch.setenv("MIN_DELAY", "-1")
    assert validate() is False

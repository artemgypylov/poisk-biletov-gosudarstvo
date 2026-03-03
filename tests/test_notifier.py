"""Tests for the Telegram notifier (notifier.py)."""
import os
from datetime import date
from unittest.mock import patch, MagicMock

import pytest

from scrapers.base import Flight
from notifier import notify, _get_credentials


@pytest.fixture
def sample_flight():
    return Flight(
        airline="S7",
        origin="DME",
        destination="VVO",
        date=date(2025, 6, 1),
        flight_number="S7-501",
        departure_time="08:00",
        arrival_time="18:00",
        price=7500,
        available=True,
        seats=5,
        fare_type="ДФО",
    )


def test_get_credentials(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "tok-123")
    monkeypatch.setenv("CHAT_ID", "999")
    token, chat_id = _get_credentials()
    assert token == "tok-123"
    assert chat_id == "999"


def test_get_credentials_missing(monkeypatch):
    monkeypatch.delenv("BOT_TOKEN", raising=False)
    monkeypatch.delenv("CHAT_ID", raising=False)
    with pytest.raises(EnvironmentError):
        _get_credentials()


@patch("notifier.httpx.post")
def test_notify_sends_message(mock_post, sample_flight, monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "tok-123")
    monkeypatch.setenv("CHAT_ID", "999")
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_post.return_value = mock_resp

    notify(sample_flight)

    mock_post.assert_called_once()
    call_kwargs = mock_post.call_args
    payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
    assert payload["chat_id"] == "999"
    assert "S7" in payload["text"]
    assert "7,500 ₽" in payload["text"]


@patch("notifier.httpx.post")
def test_notify_no_price(mock_post, sample_flight, monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "tok-123")
    monkeypatch.setenv("CHAT_ID", "999")
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_post.return_value = mock_resp

    sample_flight.price = None
    notify(sample_flight)

    payload = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1].get("json")
    assert "цена неизвестна" in payload["text"]

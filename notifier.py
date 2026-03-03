"""
Telegram notifier.

Reads BOT_TOKEN and CHAT_ID from environment variables (or .env file).
"""
import logging
import os

import httpx

from scrapers.base import Flight

logger = logging.getLogger(__name__)

_TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def _get_credentials() -> tuple[str, str]:
    token = os.environ.get("BOT_TOKEN", "")
    chat_id = os.environ.get("CHAT_ID", "")
    if not token or not chat_id:
        raise EnvironmentError(
            "BOT_TOKEN and CHAT_ID must be set (e.g. in .env file or environment)."
        )
    return token, chat_id


def notify(flight: Flight) -> None:
    """Send a Telegram message about an available subsidised flight."""
    try:
        token, chat_id = _get_credentials()
    except EnvironmentError as exc:
        logger.error("Notification skipped: %s", exc)
        return

    price_str = f"{flight.price:,} ₽" if flight.price is not None else "цена неизвестна"
    seats_str = f"мест: {flight.seats}" if flight.seats is not None else ""
    fn_str = f"  рейс {flight.flight_number}" if flight.flight_number else ""

    text = (
        f"✈️ *Появился субсидированный билет!*\n"
        f"🏢 {flight.airline}{fn_str}\n"
        f"🛫 {flight.origin} → {flight.destination}\n"
        f"📅 {flight.date}\n"
        f"💰 {price_str}  ({flight.fare_type})\n"
    )
    if seats_str:
        text += f"💺 {seats_str}\n"

    url = _TELEGRAM_API.format(token=token)
    try:
        resp = httpx.post(
            url,
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
            timeout=10,
        )
        resp.raise_for_status()
        logger.info("Notification sent: %s %s→%s %s", flight.airline, flight.origin, flight.destination, flight.date)
    except httpx.HTTPError as exc:
        logger.error("Failed to send Telegram notification: %s", exc)

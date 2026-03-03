"""
Scrapers for airlines using Sirena-Travel IBE:
S7, Yakutia, Aurora, NordStar, Smartavia, YuVT Aero, Red Wings.

Strategy:
1. Try direct HTTP GET to /api/flights (fast, no browser needed).
2. Fall back to Playwright response interception if HTTP fails.
"""
import logging
import time
import random
from datetime import date
from typing import Optional

import requests

from .base import Flight

logger = logging.getLogger(__name__)

# Mapping: airline name -> (IBE host, fare subsidy programmes)
SIRENA_AIRLINES: dict[str, tuple[str, str]] = {
    "S7":       ("ibe.s7.ru",                  "ДФО/КЛНГ/СЗМ"),
    "Якутия":   ("booking.yakutia.aero",        "ДФО"),
    "Аврора":   ("booking.aurora-airlines.ru",  "ДФО"),
    "NordStar": ("booking.nordstar.ru",          "ДФО"),
    "Smartavia":("ibe.smartavia.com",            "КЛНГ"),
    "ЮВТ Аэро": ("booking.yutair.ru",           "МРГ"),
    "Red Wings":("ibe.red-wings.aero",           "МРГ"),
}

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.9",
}


def _parse_flights_response(
    data: dict,
    airline: str,
    origin: str,
    destination: str,
    dep_date: date,
    fare_type: str,
) -> list[Flight]:
    """Parse a Sirena-Travel API JSON response into Flight objects."""
    results: list[Flight] = []
    for flight in data.get("flights", []):
        for fare in flight.get("fares", []):
            if not fare.get("isSubsidized"):
                continue
            seats_raw = fare.get("availableSeats")
            seats: Optional[int] = int(seats_raw) if seats_raw is not None else None
            results.append(
                Flight(
                    airline=airline,
                    origin=origin,
                    destination=destination,
                    date=dep_date,
                    flight_number=flight.get("flightNumber"),
                    departure_time=flight.get("departureTime"),
                    arrival_time=flight.get("arrivalTime"),
                    price=fare.get("price", {}).get("amount"),
                    available=(seats or 0) > 0,
                    seats=seats,
                    fare_type=fare_type,
                    fare_code=fare.get("code"),
                )
            )
    return results


def search_sirena_http(
    host: str,
    airline: str,
    origin: str,
    destination: str,
    dep_date: date,
    fare_type: str,
    timeout: int = 15,
) -> list[Flight]:
    """
    Search subsidised flights via direct HTTP request to Sirena-Travel API.
    Returns an empty list on any error (caller should fall back to Playwright).
    """
    url = f"https://{host}/api/flights"
    params = {
        "origin": origin,
        "destination": destination,
        "departureDate": str(dep_date),
        "adults": 1,
        "children": 0,
        "infants": 0,
        "currency": "RUB",
        "src": 1,   # субсидированный тариф
    }
    headers = {**_HEADERS, "Referer": f"https://{host}/", "Origin": f"https://{host}"}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        return _parse_flights_response(data, airline, origin, destination, dep_date, fare_type)
    except Exception as exc:
        logger.warning("Sirena HTTP failed for %s %s→%s %s: %s", airline, origin, destination, dep_date, exc)
        return []


def search_sirena_playwright(
    host: str,
    airline: str,
    origin: str,
    destination: str,
    dep_date: date,
    fare_type: str,
    wait_ms: int = 6000,
) -> list[Flight]:
    """
    Search subsidised flights via Playwright (headless Chromium).
    Used as fallback when direct HTTP is blocked.
    """
    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
    except ImportError:
        logger.error("playwright not installed – cannot use browser fallback")
        return []

    results: list[Flight] = []
    url = (
        f"https://{host}/air"
        f"?journeySpan=OW"
        f"&DA1={origin}&AA1={destination}"
        f"&DD1={dep_date}"
        f"&TA=1&TC=0&TI=0"
        f"&SC1=ANY&CUR=RUB&LAN=ru"
        f"&FSC1=1"
        f"&id=deeplink"
    )

    def _on_response(response):  # noqa: ANN001
        if "/api/flights" in response.url and response.status == 200:
            try:
                data = response.json()
                results.extend(
                    _parse_flights_response(data, airline, origin, destination, dep_date, fare_type)
                )
            except Exception as exc:
                logger.debug("Could not parse response from %s: %s", response.url, exc)

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(user_agent=_HEADERS["User-Agent"])
            page = context.new_page()
            page.on("response", _on_response)
            page.goto(url)
            page.wait_for_timeout(wait_ms)
            browser.close()
    except Exception as exc:
        logger.error("Playwright search failed for %s %s→%s %s: %s", airline, origin, destination, dep_date, exc)

    return results


def search_sirena(
    host: str,
    airline: str,
    origin: str,
    destination: str,
    dep_date: date,
    fare_type: str,
) -> list[Flight]:
    """
    Search for subsidised flights via Sirena-Travel IBE.
    Tries direct HTTP first; falls back to Playwright if it returns nothing.
    """
    flights = search_sirena_http(host, airline, origin, destination, dep_date, fare_type)
    if not flights:
        logger.info("HTTP returned no results, trying Playwright for %s %s→%s", airline, origin, destination)
        flights = search_sirena_playwright(host, airline, origin, destination, dep_date, fare_type)
        # Небольшая задержка после браузерного запроса
        time.sleep(random.uniform(2, 5))
    return flights

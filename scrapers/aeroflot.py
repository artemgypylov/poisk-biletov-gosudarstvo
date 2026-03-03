"""
Scraper for Aeroflot subsidised flights.

Aeroflot uses a React SPA at https://www.aeroflot.ru/sb/subsidized/.
There is no stable public REST endpoint, so we use Playwright to load the
page and intercept the XHR/Fetch responses that carry flight data.
"""
import logging
from datetime import date

from .base import Flight

logger = logging.getLogger(__name__)

_AEROFLOT_BASE = "https://www.aeroflot.ru/sb/subsidized/app/ru-ru"
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def _parse_aeroflot_response(
    data: dict,
    origin: str,
    destination: str,
    dep_date: date,
    fare_type: str,
) -> list[Flight]:
    """
    Parse an Aeroflot subsidised-flights API response.

    The exact JSON schema depends on the live API — this covers the most
    common shape observed via DevTools.  Adjust field names if needed.
    """
    results: list[Flight] = []

    # Try top-level "flights" list (most common shape)
    flights_raw = data.get("flights") or data.get("data", {}).get("flights", [])

    for item in flights_raw:
        price_raw = item.get("totalPrice") or item.get("price")
        price: int | None = int(price_raw) if price_raw is not None else None
        results.append(
            Flight(
                airline="Аэрофлот",
                origin=origin,
                destination=destination,
                date=dep_date,
                flight_number=item.get("flightNumber") or item.get("flight"),
                departure_time=item.get("departureTime") or item.get("departure"),
                arrival_time=item.get("arrivalTime") or item.get("arrival"),
                price=price,
                available=True,
                seats=item.get("availableSeats"),
                fare_type=fare_type,
                fare_code=item.get("fareCode") or item.get("fare"),
            )
        )
    return results


def search_aeroflot(
    origin: str,
    destination: str,
    dep_date: date,
    program: str = "dfo",
    fare_type: str = "ДФО",
    wait_ms: int = 7000,
) -> list[Flight]:
    """
    Search for subsidised Aeroflot flights using Playwright.

    :param origin:      IATA departure airport code (e.g. "SVO")
    :param destination: IATA arrival airport code  (e.g. "UUD")
    :param dep_date:    Departure date
    :param program:     Subsidy programme slug: 'dfo' | 'klng' | 'szm' | 'mrg'
    :param fare_type:   Human-readable programme name stored in Flight.fare_type
    :param wait_ms:     Milliseconds to wait for XHR after page load
    """
    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
    except ImportError:
        logger.error("playwright not installed – cannot scrape Aeroflot")
        return []

    results: list[Flight] = []
    url = (
        f"{_AEROFLOT_BASE}"
        f"#/search?from={origin}&to={destination}"
        f"&date={dep_date}&adt=1&program={program}"
    )

    def _on_response(response):  # noqa: ANN001
        u = response.url
        if "aeroflot.ru" in u and response.status == 200:
            if any(kw in u for kw in ["/search", "/flights", "/avail"]):
                try:
                    data = response.json()
                    results.extend(
                        _parse_aeroflot_response(data, origin, destination, dep_date, fare_type)
                    )
                except Exception as exc:
                    logger.debug("Could not parse Aeroflot response from %s: %s", u, exc)

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(user_agent=_USER_AGENT)
            page = context.new_page()
            page.on("response", _on_response)
            page.goto(url)
            page.wait_for_timeout(wait_ms)
            browser.close()
    except Exception as exc:
        logger.error(
            "Playwright failed for Aeroflot %s→%s %s: %s",
            origin, destination, dep_date, exc,
        )

    return results

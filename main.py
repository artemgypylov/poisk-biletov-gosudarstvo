"""
Entry point for the subsidised-flight monitor.

Usage:
    python main.py                      # runs once (suitable for GitHub Actions)
    python main.py --schedule           # runs on a 15-minute loop (suitable for VPS)

Environment variables (set via .env or shell):
    BOT_TOKEN   — Telegram bot token
    CHAT_ID     — Telegram chat / user ID
"""
import argparse
import logging
import os
import random
import time
from datetime import date, timedelta

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Imported here so dotenv is loaded first
from db import already_notified, mark_notified, setup_db  # noqa: E402
from notifier import notify  # noqa: E402
from routes import WATCH_ROUTES  # noqa: E402
from scrapers.aeroflot import search_aeroflot  # noqa: E402
from scrapers.s7 import SIRENA_AIRLINES, search_sirena  # noqa: E402

# Reverse map: IBE host → airline display name
_HOST_TO_AIRLINE: dict[str, str] = {host: name for name, (host, _) in SIRENA_AIRLINES.items()}

# How many days ahead to check for each route
DAYS_AHEAD = int(os.environ.get("DAYS_AHEAD", "45"))

# Delay range (seconds) between individual route+date requests
MIN_DELAY = float(os.environ.get("MIN_DELAY", "3"))
MAX_DELAY = float(os.environ.get("MAX_DELAY", "8"))


def check_all() -> None:
    """Run one full pass over all watched routes and all upcoming dates."""
    today = date.today()
    dates = [str(today + timedelta(days=i)) for i in range(1, DAYS_AHEAD + 1)]

    for scraper_type, host, origin, dest, fare_type, program in WATCH_ROUTES:
        for dep_date_str in dates:
            dep_date = date.fromisoformat(dep_date_str)
            try:
                if scraper_type == "sirena":
                    airline_name = _HOST_TO_AIRLINE.get(host, host)
                    flights = search_sirena(host, airline_name,
                                            origin, dest, dep_date, fare_type)
                elif scraper_type == "aeroflot":
                    flights = search_aeroflot(origin, dest, dep_date, program, fare_type)
                else:
                    logger.warning("Unknown scraper type: %s", scraper_type)
                    continue

                for flight in flights:
                    if not flight.available:
                        continue
                    if already_notified(flight.airline, origin, dest, dep_date_str):
                        continue
                    notify(flight)
                    mark_notified(flight.airline, origin, dest, dep_date_str, flight.price)

            except Exception as exc:
                logger.error(
                    "Error checking %s %s→%s %s: %s",
                    scraper_type, origin, dest, dep_date_str, exc,
                )

            # Respectful delay between requests
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))


def main() -> None:
    parser = argparse.ArgumentParser(description="Subsidised flight monitor")
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run on a repeating schedule (every 15 minutes) instead of once",
    )
    args = parser.parse_args()

    setup_db()

    if args.schedule:
        try:
            from apscheduler.schedulers.blocking import BlockingScheduler  # noqa: PLC0415
        except ImportError:
            logger.error("apscheduler is not installed. Run: pip install apscheduler")
            raise SystemExit(1)

        scheduler = BlockingScheduler()
        scheduler.add_job(check_all, "interval", minutes=15, id="check_all")
        logger.info("Starting scheduler — checking every 15 minutes.")
        check_all()  # immediate first run
        scheduler.start()
    else:
        logger.info("Running single check pass.")
        check_all()
        logger.info("Done.")


if __name__ == "__main__":
    main()

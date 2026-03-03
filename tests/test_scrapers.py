"""Tests for the Flight dataclass and scraper parsing helpers."""
from datetime import date

from scrapers.base import Flight
from scrapers.s7 import _parse_flights_response
from scrapers.aeroflot import _parse_aeroflot_response


# --------------- Flight dataclass ---------------

def test_flight_defaults():
    f = Flight(
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
    assert f.fare_code is None
    assert f.available is True


# --------------- Sirena parser ---------------

_SIRENA_SAMPLE = {
    "flights": [
        {
            "flightNumber": "S7-501",
            "departureTime": "08:00",
            "arrivalTime": "18:00",
            "fares": [
                {
                    "isSubsidized": True,
                    "availableSeats": 3,
                    "price": {"amount": 7500},
                    "code": "DFO",
                },
                {
                    "isSubsidized": False,
                    "availableSeats": 10,
                    "price": {"amount": 25000},
                    "code": "FULL",
                },
            ],
        },
        {
            "flightNumber": "S7-503",
            "departureTime": "14:00",
            "arrivalTime": "23:55",
            "fares": [
                {
                    "isSubsidized": True,
                    "availableSeats": 0,
                    "price": {"amount": 7500},
                    "code": "DFO",
                },
            ],
        },
    ],
}


def test_parse_sirena_subsidised_only():
    flights = _parse_flights_response(
        _SIRENA_SAMPLE, "S7", "DME", "VVO", date(2025, 6, 1), "ДФО"
    )
    # Two subsidised fares exist (one per flight), the non-subsidised fare is excluded
    assert len(flights) == 2


def test_parse_sirena_availability():
    flights = _parse_flights_response(
        _SIRENA_SAMPLE, "S7", "DME", "VVO", date(2025, 6, 1), "ДФО"
    )
    available = [f for f in flights if f.available]
    assert len(available) == 1
    assert available[0].flight_number == "S7-501"
    assert available[0].seats == 3
    assert available[0].price == 7500


def test_parse_sirena_empty_response():
    flights = _parse_flights_response(
        {}, "S7", "DME", "VVO", date(2025, 6, 1), "ДФО"
    )
    assert flights == []


def test_parse_sirena_no_subsidised_fares():
    data = {
        "flights": [
            {
                "flightNumber": "S7-501",
                "fares": [{"isSubsidized": False, "availableSeats": 10, "price": {"amount": 25000}}],
            }
        ]
    }
    flights = _parse_flights_response(data, "S7", "DME", "VVO", date(2025, 6, 1), "ДФО")
    assert flights == []


# --------------- Aeroflot parser ---------------

_AEROFLOT_SAMPLE = {
    "flights": [
        {
            "flightNumber": "SU-501",
            "departureTime": "07:30",
            "arrivalTime": "17:00",
            "totalPrice": 8900,
            "availableSeats": 2,
            "fareCode": "DFO",
        },
    ],
}


def test_parse_aeroflot_response():
    flights = _parse_aeroflot_response(
        _AEROFLOT_SAMPLE, "SVO", "VVO", date(2025, 6, 1), "ДФО"
    )
    assert len(flights) == 1
    f = flights[0]
    assert f.airline == "Аэрофлот"
    assert f.price == 8900
    assert f.available is True
    assert f.flight_number == "SU-501"


def test_parse_aeroflot_alternative_keys():
    data = {
        "data": {
            "flights": [
                {
                    "flight": "SU-800",
                    "departure": "10:00",
                    "arrival": "20:00",
                    "price": 6000,
                    "availableSeats": 1,
                    "fare": "DFO",
                },
            ],
        },
    }
    flights = _parse_aeroflot_response(data, "SVO", "UUD", date(2025, 7, 1), "ДФО")
    assert len(flights) == 1
    assert flights[0].flight_number == "SU-800"
    assert flights[0].price == 6000


def test_parse_aeroflot_empty():
    flights = _parse_aeroflot_response({}, "SVO", "VVO", date(2025, 6, 1), "ДФО")
    assert flights == []

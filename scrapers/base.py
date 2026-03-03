from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Flight:
    airline: str
    origin: str        # IATA-код аэропорта вылета
    destination: str   # IATA-код аэропорта назначения
    date: date
    flight_number: Optional[str]
    departure_time: Optional[str]
    arrival_time: Optional[str]
    price: Optional[int]    # None = нет мест / цена неизвестна
    available: bool
    seats: Optional[int]    # количество доступных мест
    fare_type: str          # ДФО, КЛНГ, МРГ, СЗМ
    fare_code: Optional[str] = None

"""
List of subsidised routes to monitor.

Each entry is a tuple:
    (scraper_type, host_or_none, origin, destination, fare_type, program)

scraper_type:
    "sirena"   — use scrapers.s7.search_sirena (S7, Yakutia, Aurora, etc.)
    "aeroflot" — use scrapers.aeroflot.search_aeroflot

host_or_none:
    Sirena IBE hostname (e.g. "ibe.s7.ru") for "sirena" routes,
    None for "aeroflot" routes.

program:
    Aeroflot subsidy programme slug: "dfo" | "klng" | "szm" | "mrg"
    (ignored for Sirena routes)

Source: https://gogov.ru/articles/subsidized-flights
"""

WATCH_ROUTES: list[tuple[str, str | None, str, str, str, str]] = [
    # --- S7 (ДФО) ---
    ("sirena", "ibe.s7.ru", "DME", "UUD", "ДФО", "dfo"),   # Москва → Улан-Удэ
    ("sirena", "ibe.s7.ru", "DME", "VVO", "ДФО", "dfo"),   # Москва → Владивосток
    ("sirena", "ibe.s7.ru", "DME", "HTA", "ДФО", "dfo"),   # Москва → Чита
    ("sirena", "ibe.s7.ru", "DME", "PKC", "ДФО", "dfo"),   # Москва → Петропавловск-Камчатский
    ("sirena", "ibe.s7.ru", "DME", "KHV", "ДФО", "dfo"),   # Москва → Хабаровск
    ("sirena", "ibe.s7.ru", "DME", "YKS", "ДФО", "dfo"),   # Москва → Якутск
    ("sirena", "ibe.s7.ru", "DME", "GDX", "ДФО", "dfo"),   # Москва → Магадан
    ("sirena", "ibe.s7.ru", "DME", "UUS", "ДФО", "dfo"),   # Москва → Южно-Сахалинск

    # --- S7 (КЛНГ) ---
    ("sirena", "ibe.s7.ru", "DME", "KGD", "КЛНГ", "klng"), # Москва → Калининград

    # --- Аэрофлот (ДФО) ---
    ("aeroflot", None, "SVO", "UUD", "ДФО", "dfo"),         # Москва → Улан-Удэ
    ("aeroflot", None, "SVO", "VVO", "ДФО", "dfo"),         # Москва → Владивосток
    ("aeroflot", None, "SVO", "KHV", "ДФО", "dfo"),         # Москва → Хабаровск
    ("aeroflot", None, "SVO", "YKS", "ДФО", "dfo"),         # Москва → Якутск

    # --- Аэрофлот (КЛНГ) ---
    ("aeroflot", None, "SVO", "KGD", "КЛНГ", "klng"),       # Москва → Калининград

    # --- Якутия (ДФО) ---
    ("sirena", "booking.yakutia.aero", "SVO", "YKS", "ДФО", "dfo"),
    ("sirena", "booking.yakutia.aero", "SVO", "UUD", "ДФО", "dfo"),

    # --- Аврора (ДФО) ---
    ("sirena", "booking.aurora-airlines.ru", "DME", "PKC", "ДФО", "dfo"),
    ("sirena", "booking.aurora-airlines.ru", "DME", "VVO", "ДФО", "dfo"),

    # --- NordStar (ДФО) ---
    ("sirena", "booking.nordstar.ru", "DME", "NSK", "ДФО", "dfo"),

    # --- Smartavia (КЛНГ) ---
    ("sirena", "ibe.smartavia.com", "LED", "KGD", "КЛНГ", "klng"),

    # --- ЮВТ Аэро (МРГ) ---
    ("sirena", "booking.yutair.ru", "KZN", "UFA", "МРГ", "mrg"),

    # --- Red Wings (МРГ) ---
    ("sirena", "ibe.red-wings.aero", "DME", "AER", "МРГ", "mrg"),
]

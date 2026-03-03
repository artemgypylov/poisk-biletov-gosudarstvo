<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# можно ли парсить субсидированные билеты? [https://www.aeroflot.ru/sb/subsidized/app/ru-ru\#/search?_k=bzga7b](https://www.aeroflot.ru/sb/subsidized/app/ru-ru#/search?_k=bzga7b)

Да, парсить субсидированные билеты Аэрофлота технически возможно, но с рядом важных нюансов. Страница `aeroflot.ru/sb/subsidized/app` — это **React SPA** с хэш-роутингом (`#/search`), то есть весь контент рендерится через JavaScript на клиенте, а простой HTTP-запрос вернёт пустую страницу (или блокировку, как показывает прямой запрос).[^1_1]

## Как устроена страница

- Контент динамический — загружается через JS и XHR/Fetch запросы к API[^1_2]
- На сайте стоит защита по IP (блокировка нестандартных User-Agent / bot-like запросов)[^1_1]
- Данные приходят из backend-API в JSON формате — их и нужно перехватить


## Рабочая стратегия парсинга

Самый надёжный путь — **перехват API-запросов** через DevTools, а затем их прямое воспроизведение:

1. **Открой DevTools → Network → XHR/Fetch** в браузере, зайди на страницу поиска рейсов
2. Найди запрос, который возвращает список рейсов (обычно `search`, `availability` или `flights`)
3. Скопируй `curl` этого запроса ("Copy as cURL" в Chrome)
4. Воспроизведи в Python через `requests` с теми же заголовками (`Cookie`, `Authorization`, `X-Session-Token` и т.д.)
```python
import requests

# Заголовки — скопировать из DevTools (вкладка Network → Copy as cURL)
headers = {
    "User-Agent": "Mozilla/5.0 ...",
    "Accept": "application/json",
    "Referer": "https://www.aeroflot.ru/sb/subsidized/app/ru-ru",
    # + Cookie, Authorization и другие из DevTools
}

# URL API — найти в DevTools
response = requests.get("https://www.aeroflot.ru/sb/subsidized/api/...", headers=headers)
data = response.json()
```


## Если API сложно воспроизвести — Playwright

Если запросы защищены сессионными токенами, которые сложно воспроизвести вручную, используй **Playwright** с перехватом сетевых запросов:[^1_2]

```python
from playwright.sync_api import sync_playwright
import json

def intercept_response(response):
    if "flights" in response.url or "search" in response.url:
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except:
            pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.on("response", intercept_response)
    page.goto("https://www.aeroflot.ru/sb/subsidized/app/ru-ru#/search")
    page.wait_for_timeout(5000)  # дать время загрузить рейсы
    browser.close()
```


## Важные ограничения

- **Rate limiting** — Аэрофлот активно ограничивает частые запросы, особенно в период высокого спроса (в феврале 2026 сайт получил 103 тыс. заявок за неделю)[^1_3]
- **ToS** — технически парсинг нарушает пользовательское соглашение сайта, но для личного мониторинга доступности билетов это повсеместная практика[^1_1]
- **Блокировка IP** — стоит использовать паузы между запросами и не частить (1 запрос в несколько минут вполне достаточно для мониторинга)

Самый практичный сценарий для тебя — найти в DevTools нужный API endpoint и настроить простой Python-скрипт, который раз в N минут проверяет наличие билетов на нужный маршрут.
<span style="display:none">[^1_10][^1_11][^1_12][^1_13][^1_14][^1_4][^1_5][^1_6][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://groupbwt.com/blog/web-scraping-for-flight-data/

[^1_2]: https://stackoverflow.com/questions/57468606/python-scraping-website-with-flight-tickets

[^1_3]: https://www.kommersant.ru/doc/8420516

[^1_4]: https://www.reddit.com/r/datasets/comments/blubr1/is_there_currently_a_free_and_unlimited_api_to/

[^1_5]: https://automatio.ai/how-to-scrape/cheapflights

[^1_6]: https://apify.com/volarai/aviasales-hot-tickets-scraper

[^1_7]: https://khab-vesti.ru/news/explain/aeroflot_razyasnil_situatsiyu_s_oformleniem_subsidirovannykh_biletov/

[^1_8]: https://www.actowizsolutions.com/web-scraping-airline-pricing-analysis.php

[^1_9]: https://www.newkaliningrad.ru/news/briefs/economy/24135388-aeroflot-detalnye-svedeniya-o-subsidirovannykh-biletakh-kommercheskaya-tayna.html

[^1_10]: https://www.zyte.com/data-types/flight-data-extraction/

[^1_11]: https://habr.com/ru/articles/572704/comments/

[^1_12]: https://vk.com/wall-227666675_2379

[^1_13]: https://www.cms28.ru/qa/4808.html

[^1_14]: https://www.avito.ru/all/bilety_i_puteshestviya?q=%D0%B0%D1%8D%D1%80%D0%BE%D1%84%D0%BB%D0%BE%D1%82


---

# [https://ibe.s7.ru/air?execution=e1s1\&ibe_conversation=3.109:019cb3f1-212e-7000-8a45-156edbd01d4a\&id=deeplink\&RDMPTN=false\&journeySpan=OW\&TY=0\&medium=cpc\&AA1=UUD\&work_trip=false\&FLX=false\&DA1=DME\&useProxyMode=true\&mix=false\&pet=false\&DT1=00%3A00%3A00\&SC1=ANY\&fromLocal=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C+%D0%94%D0%BE%D0%BC%D0%BE%D0%B4%D0%B5%D0%B4%D0%BE%D0%B2%D0%BE\&CUR=RUB\&DT3=00%3A00%3A00\&DT2=00%3A00%3A00\&DT5=00%3A00%3A00\&DT4=00%3A00%3A00\&TA=1\&toLocal=%D0%A3%D0%BB%D0%B0%D0%BD-%D0%A3%D0%B4%D1%8D\&TC=0\&ssdkl=b4a7b3127ae1423fadf49b942cb00f56\&DD1=2026-03-15\&searchTypeRed=portalAvia\&TI=0\&LAN=ru\&FSC1=1\&mediumLastClick=cpc\&FLC=1\&ibe_medium=s7PortalAviaBot_New\&sourceLastClick=ya\&DLI1=146f0668-7245-4a4d-9414-82ab11396634\&ALI1=d937e33c-2407-4434-afbd-c3dda9b70bd1\&source=ya\&addHistory=https%3A%2F%2Fwww.s7.ru%2Fru%2F%3Futm_source%3Dya%26utm_medium%3Dcpc%26utm_campaign%3Dannual_brand_search_moscow_new%26utm_content%3Dch_yandex_direct%7Ccid_703918622%7Cgid_5659113694%7Cad_1889529162038013663%7Cph_205659113694%7Ccrt_0%7Cpst_premium%7Cps_1%7Csrct_search%7Csrc_none%7Cdevt_desktop%7Cret_205659113694%7Cgeo_213%7Ccf_0%7Cint_%7Ctgt_205659113694%7Cadd_no%26etext%3D2202.x7i0oGj1CqWpVOFhWwg0f0orfBlE_rJniyTijfLpHzw6m8d4MibHpOY8TTdM8da0bnp6aHN4Ymh6Z21kZ3d5cA.a1b710fff6204aaed6c49e1d4103f455e6ffe7db%26ybaip%3D1](https://ibe.s7.ru/air?execution=e1s1&ibe_conversation=3.109:019cb3f1-212e-7000-8a45-156edbd01d4a&id=deeplink&RDMPTN=false&journeySpan=OW&TY=0&medium=cpc&AA1=UUD&work_trip=false&FLX=false&DA1=DME&useProxyMode=true&mix=false&pet=false&DT1=00%3A00%3A00&SC1=ANY&fromLocal=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C+%D0%94%D0%BE%D0%BC%D0%BE%D0%B4%D0%B5%D0%B4%D0%BE%D0%B2%D0%BE&CUR=RUB&DT3=00%3A00%3A00&DT2=00%3A00%3A00&DT5=00%3A00%3A00&DT4=00%3A00%3A00&TA=1&toLocal=%D0%A3%D0%BB%D0%B0%D0%BD-%D0%A3%D0%B4%D1%8D&TC=0&ssdkl=b4a7b3127ae1423fadf49b942cb00f56&DD1=2026-03-15&searchTypeRed=portalAvia&TI=0&LAN=ru&FSC1=1&mediumLastClick=cpc&FLC=1&ibe_medium=s7PortalAviaBot_New&sourceLastClick=ya&DLI1=146f0668-7245-4a4d-9414-82ab11396634&ALI1=d937e33c-2407-4434-afbd-c3dda9b70bd1&source=ya&addHistory=https%3A%2F%2Fwww.s7.ru%2Fru%2F%3Futm_source%3Dya%26utm_medium%3Dcpc%26utm_campaign%3Dannual_brand_search_moscow_new%26utm_content%3Dch_yandex_direct%7Ccid_703918622%7Cgid_5659113694%7Cad_1889529162038013663%7Cph_205659113694%7Ccrt_0%7Cpst_premium%7Cps_1%7Csrct_search%7Csrc_none%7Cdevt_desktop%7Cret_205659113694%7Cgeo_213%7Ccf_0%7Cint_%7Ctgt_205659113694%7Cadd_no%26etext%3D2202.x7i0oGj1CqWpVOFhWwg0f0orfBlE_rJniyTijfLpHzw6m8d4MibHpOY8TTdM8da0bnp6aHN4Ymh6Z21kZ3d5cA.a1b710fff6204aaed6c49e1d4103f455e6ffe7db%26ybaip%3D1)

Это ссылка на **S7 IBE** (Internet Booking Engine) — рейс **Москва DME → Улан-Удэ UUD, 15 марта 2026, 1 взрослый, эконом**. Ссылка содержит сессионный токен (`execution=e1s1`, `ibe_conversation=...`), который уже истёк — страница не открывается без новой сессии.

## Анатомия URL

| Параметр | Значение | Смысл |
| :-- | :-- | :-- |
| `execution=e1s1` | `e1s1` | Spring Web Flow — сессионный токен (истекает за минуты) |
| `ibe_conversation` | `3.109:019cb3f1-...` | ID сессии, привязан к конкретному запросу |
| `DA1=DME` / `AA1=UUD` | DME → UUD | Домодедово → Улан-Удэ |
| `DD1=2026-03-15` | 15.03.2026 | Дата вылета |
| `journeySpan=OW` | One Way | В одну сторону |
| `TA=1` / `TC=0` / `TI=0` | 1/0/0 | 1 взрослый, без детей |
| `FSC1=1` | 1 | **Субсидированный тариф** (FSC = Federal Subsidy) |
| `SC1=ANY` | ANY | Любой класс |

## Как воспроизвести поиск без сессии

S7 IBE принимает **чистый deeplink** без `execution` и `ibe_conversation` — сервер сам создаст новую сессию:

```python
import requests
from playwright.sync_api import sync_playwright

# Чистая ссылка — стабильная, без сессионных параметров
SEARCH_URL = (
    "https://ibe.s7.ru/air"
    "?journeySpan=OW"
    "&DA1=DME&AA1=UUD"
    "&DD1=2026-03-15"
    "&TA=1&TC=0&TI=0"
    "&SC1=ANY&CUR=RUB&LAN=ru"
    "&FSC1=1"          # субсидированный тариф
    "&id=deeplink"
)
```


## Перехват API через Playwright

S7 IBE работает на **Sirena-Travel** и делает запрос к `GET /api/flights` после загрузки страницы. Перехвати его:[^2_1]

```python
import json

def handle_response(response):
    if "/api/flights" in response.url and response.status == 200:
        data = response.json()
        for flight in data.get("flights", []):
            print(
                flight["flightNumber"],
                flight["departureTime"],
                flight["price"]["amount"],
                flight.get("subsidized", False)
            )

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on("response", handle_response)
    page.goto(SEARCH_URL)
    page.wait_for_timeout(6000)  # ждём загрузки рейсов
    browser.close()
```


## Особенности S7 IBE

- **Spring Web Flow** — каждая сессия живёт ~15 минут, но deeplink без `execution` стартует свежую сессию автоматически[^2_2]
- Бэкенд — **Sirena-Travel** (российская GDS), API возвращает JSON с полями `flightNumber`, `price`, `availableSeats`[^2_1]
- Параметр `FSC1=1` фильтрует только субсидированные тарифы — очень полезно для мониторинга их наличия
- Защита слабее, чем у Аэрофлота — стандартного `User-Agent` браузера обычно достаточно[^2_3]

Для **мониторинга появления билетов** на конкретную дату достаточно запускать этот скрипт раз в 10–15 минут и уведомлять через Telegram-бот, когда `availableSeats > 0`.
<span style="display:none">[^2_10][^2_11][^2_12][^2_13][^2_4][^2_5][^2_6][^2_7][^2_8][^2_9]</span>

<div align="center">⁂</div>

[^2_1]: https://club.uralairlines.ru/upload/iblock/afb/afb3bf0c8e38d8f1fc39162413c0debd.pdf

[^2_2]: https://club.uralairlines.ru/upload/iblock/3a9/3a91a832b1fc56c2a9c9e48bc63429d5.pdf

[^2_3]: https://groupbwt.com/blog/web-scraping-for-flight-data/

[^2_4]: https://neginmirsalehi.com/fashion/fall-in-new-york

[^2_5]: https://club.uralairlines.ru/upload/iblock/7a3/7a3abdb0ec3edad33781eb8cea91e887.pdf

[^2_6]: https://aviacenter.ru/helpdesk/help-desk/iata-code/news-helpdesk-avia/siberia-airlines-s7-2025-04-16-texnicheskie-problemyi-s7-agent-api/

[^2_7]: https://www.travelscrape.com/real-time-flight-data-scraping-api.php

[^2_8]: https://apify.com/lexis-solutions/booking-flights-scraper/api

[^2_9]: https://www.browsable.app/apis/skyscanner/

[^2_10]: https://aviation-edge.com/airlines-data/s7-airlines-api-schedules-flight-tracker/

[^2_11]: https://www.scrapingbee.com/scrapers/flight-api/

[^2_12]: https://airlabs.co/s7-airlines-developer-api

[^2_13]: https://stackoverflow.com/questions/65529303/amadeus-flight-search-api-flight-offers-api-and-flight-booking-api-using-javascr


---

# я хочу написать сервис, который будет отслеживать появление субсидированных билетов на сайтах s7, аэрофлот, итд: [https://gogov.ru/articles/subsidized-flights](https://gogov.ru/articles/subsidized-flights)

Отличная идея! На странице gogov.ru представлено более 500 субсидированных маршрутов на 2026 год. Давай разберём архитектуру такого сервиса по всем авиакомпаниям.[^3_1]

## Ключевые авиакомпании и методы парсинга

По данным со страницы, основные перевозчики по программе ДФО — это **Аэрофлот, S7, Аврора, Якутия, NordStar, АЛРОСА**; по КЛНГ — **Аэрофлот, S7, Smartavia, Nordwind**; по МРГ — ИрАэро, Red Wings, ЮВТ Аэро, РусЛайн и другие.[^3_1]


| Авиакомпания | Платформа / Движок | Метод парсинга | Субсидийный параметр |
| :-- | :-- | :-- | :-- |
| **Аэрофлот** | React SPA | Playwright + перехват XHR | Отдельный сайт `/sb/subsidized` |
| **S7** | Sirena-Travel IBE | deeplink + перехват API | `FSC1=1` в URL |
| **Аврора** | Отдельный сайт | Playwright / requests | Только субсидированные маршруты |
| **Якутия** | Сайт yakutia.aero | requests + BS4 | Тариф "Субсидия" |
| **NordStar** | nordstar.ru | Playwright | Специальный тариф |
| **Smartavia** | smartavia.com | requests | Тариф по программе |

## Архитектура сервиса

Наиболее чистая структура — **планировщик + воркеры + хранилище + уведомления**:

```
┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│  Scheduler   │───▶│  Scrapers   │───▶│  PostgreSQL  │
│ (APScheduler)│    │  (per airline)│   │  (маршруты,  │
└──────────────┘    └─────┬───────┘    │   история)   │
                          │            └──────┬───────┘
                    ┌─────▼───────┐          │
                    │   Checker   │◀─────────┘
                    │ (новые/изменения) 
                    └─────┬───────┘
                          │
                    ┌─────▼───────┐
                    │  Telegram   │
                    │    Bot      │
                    └─────────────┘
```


## Код базовой структуры

```python
# scraper_base.py
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Flight:
    airline: str
    origin: str       # IATA код
    destination: str
    date: date
    price: Optional[int]   # None = нет мест
    available: bool
    fare_type: str    # ДФО, КЛНГ, МРГ, СЗМ

# --- S7 scraper ---
from playwright.sync_api import sync_playwright
import json

ROUTES_S7 = [
    ("DME", "UUD"),  # Москва → Улан-Удэ
    ("DME", "VVO"),  # Москва → Владивосток
    ("DME", "HTA"),  # Москва → Чита
    # ... все маршруты S7 из списка ДФО
]

def scrape_s7(origin, dest, dep_date) -> list[Flight]:
    results = []
    url = (
        f"https://ibe.s7.ru/air?journeySpan=OW"
        f"&DA1={origin}&AA1={dest}"
        f"&DD1={dep_date}&TA=1&TC=0&TI=0"
        f"&SC1=ANY&CUR=RUB&LAN=ru&FSC1=1&id=deeplink"
    )
    
    def handle_response(response):
        if "/api/flights" in response.url and response.status == 200:
            try:
                data = response.json()
                for f in data.get("flights", []):
                    results.append(Flight(
                        airline="S7",
                        origin=origin,
                        destination=dest,
                        date=dep_date,
                        price=f.get("price", {}).get("amount"),
                        available=f.get("availableSeats", 0) > 0,
                        fare_type="ДФО"
                    ))
            except: pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("response", handle_response)
        page.goto(url)
        page.wait_for_timeout(5000)
        browser.close()
    return results


# --- Aeroflot scraper ---
def scrape_aeroflot(origin, dest, dep_date) -> list[Flight]:
    results = []
    url = (
        f"https://www.aeroflot.ru/sb/subsidized/app/ru-ru#/search"
        f"?from={origin}&to={dest}&date={dep_date}&adt=1"
    )
    
    def handle_response(response):
        if "search" in response.url and "aeroflot" in response.url:
            try:
                data = response.json()
                for f in data.get("flights", []):
                    results.append(Flight(
                        airline="Aeroflot",
                        origin=origin, destination=dest,
                        date=dep_date,
                        price=f.get("totalPrice"),
                        available=True,
                        fare_type="ДФО"
                    ))
            except: pass
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("response", handle_response)
        page.goto(url)
        page.wait_for_timeout(6000)
        browser.close()
    return results
```


## Уведомления в Telegram

```python
# notifier.py
import httpx

BOT_TOKEN = "YOUR_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def notify(flight: Flight):
    text = (
        f"✈️ *Появился субсидированный билет!*\n"
        f"🛫 {flight.origin} → {flight.destination}\n"
        f"📅 {flight.date}\n"
        f"💰 {flight.price:,} ₽ ({flight.fare_type})\n"
        f"🏢 {flight.airline}"
    )
    httpx.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    )
```


## Планировщик с хранением состояния

```python
# main.py
from apscheduler.schedulers.blocking import BlockingScheduler
import sqlite3
from datetime import date, timedelta

# Все маршруты из gogov.ru (ДФО с фиксированными ценами)
WATCH_ROUTES = [
    ("S7",       "DME", "UUD", 6200),   # Москва → Улан-Удэ
    ("S7",       "DME", "VVO", 7400),   # Москва → Владивосток
    ("Aeroflot", "SVO", "UUD", 6200),   # Москва → Улан-Удэ
    ("S7",       "DME", "HTA", 6200),   # Москва → Чита
    # ... добавить нужные маршруты
]

def check_all():
    dates = [date.today() + timedelta(days=i) for i in range(1, 60)]
    for airline, orig, dest, expected_price in WATCH_ROUTES:
        for d in dates:
            if airline == "S7":
                flights = scrape_s7(orig, dest, d)
            elif airline == "Aeroflot":
                flights = scrape_aeroflot(orig, dest, d)
            
            for f in flights:
                if f.available and not already_notified(orig, dest, d):
                    notify(f)
                    mark_notified(orig, dest, d)

scheduler = BlockingScheduler()
scheduler.add_job(check_all, 'interval', minutes=15)
scheduler.start()
```


## Хранение состояния в SQLite

```python
def setup_db():
    conn = sqlite3.connect("flights.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notified (
            airline TEXT, origin TEXT, dest TEXT,
            dep_date TEXT, price INT, notified_at TEXT,
            PRIMARY KEY (airline, origin, dest, dep_date)
        )
    """)
    conn.commit()

def already_notified(origin, dest, dep_date):
    conn = sqlite3.connect("flights.db")
    row = conn.execute(
        "SELECT 1 FROM notified WHERE origin=? AND dest=? AND dep_date=?",
        (origin, dest, str(dep_date))
    ).fetchone()
    return row is not None
```


## Советы по надёжности

- **Ротация задержек**: добавляй `random.uniform(2, 8)` секунд между запросами к одному сайту, иначе быстро забанят[^3_1]
- **МРГ-маршруты** (без фиксированной цены) — у ~70% направлений цена «отсутствует», это значит билеты выставляются нерегулярно, их мониторить важнее всего[^3_1]
- **Разные даты**: субсидированные квоты привязаны к конкретным рейсам — стоит проверять ближайшие 30–60 дней одновременно
- **Деплой**: для постоянного мониторинга достаточно самого дешёвого VPS (1 CPU, 512MB RAM) — Playwright в headless-режиме работает там без проблем

<div align="center">⁂</div>

[^3_1]: https://www.reddit.com/r/datasets/comments/blubr1/is_there_currently_a_free_and_unlimited_api_to/


---

# как осуществить парсинг данных с аэрофлота и с других сайтов

Самое важное открытие: **S7, Якутия, Аврора, NordStar и другие** используют один и тот же движок **Sirena-Travel IBE**, у которого есть задокументированный REST API с полем `isSubsidized`. Это значит подход одинаков для всех этих сайтов.[^4_1][^4_2]

## Универсальный Sirena-Travel API (S7, Якутия, Аврора…)

Все авиакомпании на Sirena-Travel IBE имеют одинаковую структуру API:[^4_2]

```
GET https://ibe.{airline.ru}/api/flights
    ?origin=DME
    &destination=UUD
    &departureDate=2026-03-15
    &adults=1
    &children=0
    &infants=0
    &currency=RUB
    &src=1          ← субсидированный тариф ДФО
    &yth=1          ← субсидированный тариф для молодёжи (опционально)
```

В ответе каждый тариф содержит поле `"isSubsidized": true`. Адреса IBE у разных компаний:[^4_1]


| Авиакомпания | IBE хост | Программы |
| :-- | :-- | :-- |
| S7 | `ibe.s7.ru` | ДФО, КЛНГ, СЗМ |
| Якутия | `booking.yakutia.aero` | ДФО |
| NordStar | `booking.nordstar.ru` | ДФО |
| Аврора | `booking.aurora-airlines.ru` | ДФО |
| Smartavia | `ibe.smartavia.com` | КЛНГ |
| ЮВТ Аэро | `booking.yutair.ru` | МРГ |
| Red Wings | `ibe.red-wings.aero` | МРГ |


***

## Шаг 1 — Найти точный API endpoint через DevTools

Сначала нужно подтвердить реальный URL для каждого сайта:

```python
# Запускаем Playwright в видимом режиме, чтобы увидеть все запросы
from playwright.sync_api import sync_playwright

def discover_api(ibe_url: str):
    """Перехватывает все XHR/fetch запросы и выводит те, что содержат рейсы"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        def on_response(response):
            url = response.url
            # Фильтруем только JSON-ответы с данными о рейсах
            if response.status == 200 and any(
                kw in url for kw in ["flights", "search", "avail", "fares"]
            ):
                try:
                    data = response.json()
                    print(f"\n✅ НАЙДЕН: {url}")
                    print(str(data)[:300])
                except:
                    pass

        page.on("response", on_response)
        page.goto(ibe_url)
        input("Выполни поиск на сайте, затем нажми Enter...")
        browser.close()

# Запускаем для каждого сайта
discover_api("https://ibe.s7.ru/air?journeySpan=OW&DA1=DME&AA1=UUD&DD1=2026-03-15&TA=1&FSC1=1&id=deeplink")
```


***

## Шаг 2 — Прямой HTTP-запрос к API (без браузера)

Когда нашёл endpoint — воспроизводи напрямую через `requests`:

```python
import requests
import json

# Заголовки — скопировать из DevTools → Network → Copy as cURL
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Referer": "https://ibe.s7.ru/",
    "Origin": "https://ibe.s7.ru",
}

def search_sirena(host: str, origin: str, dest: str, date: str) -> list:
    """Универсальный поиск для любого Sirena-Travel IBE"""
    url = f"https://{host}/api/flights"
    params = {
        "origin": origin,
        "destination": dest,
        "departureDate": date,
        "adults": 1,
        "children": 0,
        "infants": 0,
        "currency": "RUB",
        "src": 1,       # субсидированный тариф
    }
    r = requests.get(url, params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    data = r.json()

    results = []
    for flight in data.get("flights", []):
        for fare in flight.get("fares", []):
            if fare.get("isSubsidized"):
                results.append({
                    "flight":    flight["flightNumber"],
                    "departure": flight["departureTime"],
                    "arrival":   flight["arrivalTime"],
                    "price":     fare["price"]["amount"],
                    "seats":     fare.get("availableSeats", "?"),
                    "fare_code": fare["code"],
                })
    return results

# Пример вызова
flights = search_sirena("ibe.s7.ru", "DME", "UUD", "2026-03-15")
for f in flights:
    print(f"{f['flight']}  {f['departure']}  {f['price']} ₽  мест: {f['seats']}")
```


***

## Шаг 3 — Аэрофлот (отдельная логика)

Аэрофлот — React SPA, прямого REST нет, нужен Playwright:

```python
from playwright.sync_api import sync_playwright
import json

def search_aeroflot(origin: str, dest: str, date: str, program: str = "dfo") -> list:
    """
    program: 'dfo' | 'klng' | 'szm' | 'mrg'
    """
    results = []
    base = "https://www.aeroflot.ru/sb/subsidized/app/ru-ru"
    url = f"{base}#/search?from={origin}&to={dest}&date={date}&adt=1&program={program}"

    def on_response(response):
        u = response.url
        if "aeroflot.ru" in u and response.status == 200:
            if any(x in u for x in ["/search", "/flights", "/avail"]):
                try:
                    data = response.json()
                    # Структура зависит от реального API — уточнить через DevTools
                    for item in data.get("data", {}).get("flights", []):
                        results.append({
                            "flight":  item.get("flightNumber"),
                            "price":   item.get("totalPrice"),
                            "date":    date,
                            "origin":  origin,
                            "dest":    dest,
                        })
                except:
                    pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
        )
        page = ctx.new_page()
        page.on("response", on_response)
        page.goto(url)
        page.wait_for_timeout(7000)   # ждём XHR с рейсами
        browser.close()

    return results
```


***

## Шаг 4 — Собираем всё вместе

```python
import time, random, sqlite3
from datetime import date, timedelta

# Конфиг маршрутов по каждому перевозчику (из gogov.ru)
ROUTES = [
    # (airline_type, host_или_функция, origin, dest, программа)
    ("sirena", "ibe.s7.ru",               "DME", "UUD", "ДФО"),
    ("sirena", "ibe.s7.ru",               "DME", "VVO", "ДФО"),
    ("sirena", "booking.yakutia.aero",    "SVO", "YKS", "ДФО"),
    ("sirena", "booking.aurora-airlines.ru", "DME", "PKC", "ДФО"),
    ("aeroflot", None,                    "SVO", "UUD", "dfo"),
    ("aeroflot", None,                    "SVO", "VVO", "dfo"),
    # ... добавить нужные маршруты
]

def run_all_checks():
    dates = [str(date.today() + timedelta(days=i)) for i in range(1, 45)]
    for route in ROUTES:
        kind, host, orig, dest, prog = route
        for d in dates:
            try:
                if kind == "sirena":
                    flights = search_sirena(host, orig, dest, d)
                else:
                    flights = search_aeroflot(orig, dest, d, prog)

                for f in flights:
                    key = f"{kind}:{orig}:{dest}:{d}"
                    if f.get("seats", 1) and not already_notified(key):
                        notify(f)
                        save_notified(key)

            except Exception as e:
                print(f"Ошибка {orig}→{dest} {d}: {e}")

            # Задержка между запросами — важно!
            time.sleep(random.uniform(3, 8))
```


***

## Рекомендации по запуску

- **DevTools первым делом**: перед тем как писать код — открой нужный сайт, сделай поиск, найди в Network вкладке JSON-ответ с рейсами и скопируй его `curl`[^4_3]
- **Заголовки из браузера**: сессионные куки и токены копируй из DevTools, иначе сервер вернёт 403 — особенно критично для Аэрофлота
- **Sirena API быстрее**: если прямой HTTP запрос к `/api/flights` работает — используй его без Playwright, это в 10× быстрее и не требует GUI[^4_2][^4_1]
- **Rate limit**: Аэрофлот строже всех — не чаще 1 запроса в 2 минуты; Sirena-сайты мягче — 1 запрос в 30 секунд достаточно
<span style="display:none">[^4_10][^4_11][^4_12][^4_13][^4_14][^4_15][^4_16][^4_4][^4_5][^4_6][^4_7][^4_8][^4_9]</span>

<div align="center">⁂</div>

[^4_1]: https://club.uralairlines.ru/upload/iblock/d2c/d2cc6dfc1a3248d36435386c1a77521b.pdf

[^4_2]: https://club.uralairlines.ru/upload/iblock/fd6/fd6ad918aa17af554fd8aee612be37a5.pdf

[^4_3]: https://groupbwt.com/blog/web-scraping-for-flight-data/

[^4_4]: https://github.com/u-cha/FlightAPI

[^4_5]: https://aviation-edge.com/airlines-data/aeroflot-api-schedules-flight-tracker/

[^4_6]: https://duffel.com/flights/airlines/aeroflot

[^4_7]: https://airlabs.co/aeroflot-developer-api

[^4_8]: https://travelpayouts.github.io/slate/

[^4_9]: https://www.developer.aero/api-catalog/fids-api-overview

[^4_10]: https://mr-allaihovskij.sakha.gov.ru/news/front/view/id/3386566

[^4_11]: https://www.aurora-airlines.ru

[^4_12]: https://support.travelpayouts.com/hc/ru/articles/203956163-API-данных-Aviasales-для-партнёров

[^4_13]: https://wiki.megatec.ru/index.php/Мастер-Тур(15):API_%D0%B4%D0%BB%D1%8F_%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8_%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0_%D0%B0%D0%B2%D0%B8%D0%B0%D0%B1%D0%B8%D0%BB%D0%B5%D1%82%D0%BE%D0%B2

[^4_14]: https://aviakompaniya.org/subsidirovannye-aviabilety/bilety-avrora/

[^4_15]: https://amadeus.com/documents/en/airlines/research-report/global-airline-industry-almanac.pdf

[^4_16]: https://www.kommersant.ru/doc/7958521


---

# опиши что мне нужно для разработки. вайбкодить буду сам на visual studio

Вот всё, что тебе понадобится для разработки сервиса мониторинга субсидированных билетов.

## Окружение

- **Python 3.11+** — [python.org/downloads](https://python.org/downloads)
- **Visual Studio Code** (не Visual Studio) — лучше для Python; если именно VS, то установи расширение **Python** от Microsoft
- **Git** — для контроля версий


## Python-библиотеки

Установи одной командой:

```bash
pip install playwright requests beautifulsoup4 apscheduler httpx python-dotenv
playwright install chromium
```

| Библиотека | Зачем |
| :-- | :-- |
| `playwright` | Парсинг React/SPA сайтов (Аэрофлот) |
| `requests` | Прямые HTTP-запросы к Sirena API |
| `beautifulsoup4` | Парсинг HTML если нет JSON API |
| `apscheduler` | Запуск проверок по расписанию |
| `httpx` | Отправка уведомлений в Telegram |
| `python-dotenv` | Хранение токенов в `.env` файле |

## Структура проекта

```
subsidy-monitor/
├── .env                  # токены (BOT_TOKEN, CHAT_ID)
├── main.py               # запуск планировщика
├── scrapers/
│   ├── __init__.py
│   ├── s7.py             # S7 + другие Sirena IBE
│   ├── aeroflot.py       # Аэрофлот (Playwright)
│   └── base.py           # dataclass Flight
├── notifier.py           # Telegram уведомления
├── db.py                 # SQLite (уже уведомлённые)
├── routes.py             # список маршрутов из gogov.ru
└── requirements.txt
```


## Telegram Bot (для уведомлений)

1. Напиши [@BotFather](https://t.me/BotFather) → `/newbot`
2. Получи `BOT_TOKEN`
3. Напиши боту любое сообщение, затем открой:
`https://api.telegram.org/bot<TOKEN>/getUpdates` — найди свой `chat_id`
4. Добавь в `.env`:
```
BOT_TOKEN=1234567890:ABC...
CHAT_ID=123456789
```


## Порядок разработки (по шагам)

1. **Исследование API** — открой DevTools → Network, сделай поиск на каждом сайте, найди JSON с рейсами, скопируй как cURL
2. **`base.py`** — опиши dataclass `Flight`
3. **`scraper/s7.py`** — сначала прямой `requests` к Sirena API; если не работает — Playwright
4. **`scraper/aeroflot.py`** — только Playwright с перехватом response
5. **`db.py`** — SQLite для хранения уже отправленных уведомлений
6. **`notifier.py`** — отправка в Telegram
7. **`main.py`** — APScheduler, запуск каждые 15 минут
8. **Тест локально** → задеплоить на VPS (любой за 200–300 ₽/мес, например Timeweb или Selectel)

## Что открыть в браузере перед кодингом

Это самый важный шаг — **руками** найти API endpoint:

1. Зайди на `https://ibe.s7.ru` → поставь `FSC1=1` в URL → открой **F12 → Network → Fetch/XHR**
2. Нажми «Найти» на сайте
3. Найди запрос, который вернул список рейсов в JSON
4. ПКМ → **Copy → Copy as cURL (bash)**
5. Вставь в [curlconverter.com](https://curlconverter.com) — получишь готовый `requests`-код

Повтори для Аэрофлота, Якутии, Авроры — и у тебя будут все нужные endpoint'ы ещё до того, как напишешь первую строку кода.

---

# нет, для того чтобы задеплоить сервис, что мне нужно

Для деплоя сервиса мониторинга билетов (Python + Playwright + APScheduler) нужно совсем немного.

## VPS-сервер

Минимальные требования: **1 CPU, 1 GB RAM, 10 GB SSD** — Playwright с Chromium требует хотя бы 512 MB, лучше 1 GB. Подойдут российские хостинги:


| Хостинг | Цена | Особенность |
| :-- | :-- | :-- |
| **Timeweb** | ~170 ₽/мес | Самый дешёвый старт |
| **Selectel** | ~300 ₽/мес | Надёжный, хорошая сеть |
| **Beget** | ~250 ₽/мес | Простая панель |
| **Yandex Cloud** | ~400 ₽/мес | Можно платить по часам |

ОС — **Ubuntu 22.04 LTS**, она везде доступна по умолчанию.

## Что установить на сервер

```bash
# Подключаешься по SSH и выполняешь:
sudo apt update && sudo apt install -y python3.11 python3-pip git

# Копируешь проект с GitHub
git clone https://github.com/ты/subsidy-monitor
cd subsidy-monitor

# Устанавливаешь зависимости
pip install -r requirements.txt
playwright install chromium
playwright install-deps   # ← важно! системные зависимости для браузера
```


## Запуск как фоновый сервис

Создай systemd-сервис, чтобы скрипт запускался автоматически и перезапускался при падении:

```bash
sudo nano /etc/systemd/system/subsidy.service
```

```ini
[Unit]
Description=Subsidy Flight Monitor
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/subsidy-monitor
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10
EnvironmentFile=/home/ubuntu/subsidy-monitor/.env

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable subsidy   # автозапуск при старте сервера
sudo systemctl start subsidy    # запустить сейчас
sudo systemctl status subsidy   # проверить статус
journalctl -u subsidy -f        # смотреть логи в реальном времени
```


## Итого нужно

- VPS ~170–300 ₽/мес с Ubuntu 22.04
- Аккаунт на GitHub (чтобы загружать код и деплоить через `git pull`)
- SSH-клиент на Маке — встроенный Terminal, просто `ssh user@ip`
- `.env` файл с `BOT_TOKEN` и `CHAT_ID` — загрузить на сервер вручную (не через Git)

Весь деплой после первой настройки сводится к трём командам: `git pull` → `systemctl restart subsidy` → `journalctl -f`.

---

# рассмотри варианты деплоинга через github или vercel

Для этого конкретного сервиса у каждого варианта есть принципиальные ограничения. Вот честное сравнение:

## Главная проблема: Playwright + серверлесс

**Vercel — не подходит** для этого проекта. Playwright с Chromium не разворачивается на Vercel из-за ограничений файловой системы и размера бандла. Плюс serverless-функции на Hobby-плане имеют таймаут 10 секунд — Playwright только запускается дольше.[^7_1][^7_2][^7_3]

## GitHub Actions — подходит, но с нюансами

GitHub Actions отлично запускает Python + Playwright по расписанию. Это самый простой вариант деплоя без VPS:[^7_4]

```yaml
# .github/workflows/monitor.yml
name: Subsidy Monitor

on:
  schedule:
    - cron: '*/15 * * * *'   # каждые 15 минут
  workflow_dispatch:           # ручной запуск кнопкой

jobs:
  check-flights:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
          playwright install-deps

      - name: Run monitor
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
        run: python main.py
```

Секреты добавляешь в **Settings → Secrets and variables → Actions** — туда `BOT_TOKEN` и `CHAT_ID`, в код они попадают через `os.environ`.

### Лимиты GitHub Actions

| Параметр | Публичный репо | Приватный репо |
| :-- | :-- | :-- |
| Минуты/мес | **Бесплатно ∞** | 2 000 мин бесплатно |
| Мин. интервал cron | 5 минут | 5 минут |
| Макс. время одного job | 6 часов | 6 часов |
| Цена сверх лимита | — | \$0.002/мин (с марта 2026) [^7_5] |

Для приватного репо: 1 запуск ≈ 2–3 мин × 96 раз/день = ~240 мин/день = **~7 200 мин/мес** — превысит лимит. Поэтому либо **публичный репо** (бесплатно), либо уменьши частоту до раза в час.

### Важное ограничение

GitHub Actions cron **не гарантирует точное время** — при высокой нагрузке на платформу задержка может быть 5–15 минут. Для мониторинга билетов это некритично.

## Лучший бесплатный вариант — Railway

Если хочешь всегда работающий сервис без VPS и без GitHub Actions — **Railway**:[^7_4]

```
# Деплой буквально за 3 шага:
1. railway.app → New Project → Deploy from GitHub
2. Подключаешь репо
3. Добавляешь BOT_TOKEN и CHAT_ID в Variables
```

Railway запускает `python main.py` как постоянный процесс, поддерживает Playwright, даёт **\$5 кредитов бесплатно** в месяц (хватает на лёгкий сервис).

## Итоговая рекомендация

| Вариант | Цена | Сложность | Playwright | Подходит |
| :-- | :-- | :-- | :-- | :-- |
| **GitHub Actions** (публичный репо) | Бесплатно | Минимальная | ✅ | ✅ Лучший старт |
| **Railway** | ~\$5/мес или бесплатно | Минимальная | ✅ | ✅ Если нужен 24/7 |
| **Vercel** | Бесплатно | Сложная | ❌ | ❌ Не подходит |
| **VPS (Timeweb)** | 170 ₽/мес | Средняя | ✅ | ✅ Надёжнее всего |

**Начни с GitHub Actions на публичном репо** — это нулевая стоимость, деплой через `git push`, и Playwright работает из коробки.[^7_6][^7_4]
<span style="display:none">[^7_10][^7_11][^7_12][^7_13][^7_14][^7_15][^7_7][^7_8][^7_9]</span>

<div align="center">⁂</div>

[^7_1]: https://vercel.com/docs/limits

[^7_2]: https://www.rafay99.com/blog/vercel-playwright-deployment-error-debugging

[^7_3]: https://lightrun.com/answers/vercel-nft-cannot-deploy-playwright-to-vercel---required-file-not-traced-by-nft

[^7_4]: https://davidmuraya.com/blog/schedule-python-scripts-github-actions/

[^7_5]: https://github.blog/changelog/2025-12-16-coming-soon-simpler-pricing-and-a-better-experience-for-github-actions/

[^7_6]: https://docs.github.com/en/actions/concepts/billing-and-usage

[^7_7]: https://github.com/simonw/nicar-2025-scraping

[^7_8]: https://red9systech.com/github-actions-automating-your-workflow-in-2025/

[^7_9]: https://github.com/patrickloeber/python-github-action-template

[^7_10]: https://docs.github.com/en/enterprise-server@3.12/actions/administering-github-actions/usage-limits-billing-and-administration

[^7_11]: https://github.com/vercel/vercel/issues/14041

[^7_12]: https://docs.github.com/en/enterprise-cloud@latest/actions/administering-github-actions/usage-limits-billing-and-administration

[^7_13]: https://docs.github.com/en/actions/reference/limits

[^7_14]: https://community.vercel.com/t/is-the-playwright-allowed-to-run/3553

[^7_15]: https://docs.github.com/en/actions/reference/actions-limits


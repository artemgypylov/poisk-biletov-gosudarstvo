FROM python:3.11-slim

# Playwright system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 \
        libgbm1 libpango-1.0-0 libcairo2 libasound2 \
        libxshmfence1 libx11-xcb1 libxcomposite1 libxdamage1 \
        libxrandr2 libatspi2.0-0 libcups2 libxfixes3 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium

COPY . .

# Database persisted via volume
ENV DB_PATH=/app/data/flights.db

ENTRYPOINT ["python", "main.py"]

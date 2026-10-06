FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DENO_INSTALL=/usr/local/deno

WORKDIR /app

# Runtime/build dependencies used by VenomMusic.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ffmpeg \
       unzip \
       gcc \
       git \
       procps \
       curl \
       ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Deno is used by yt-dlp's JavaScript-runtime fallback chain.
RUN mkdir -p "$DENO_INSTALL" \
    && curl -fsSL https://deno.land/install.sh | sh
ENV PATH="${DENO_INSTALL}/bin:${PATH}"

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Render Web Service entrypoint. It starts the HTTP health server in a
# background thread and keeps the original Telegram bot on the main loop.
CMD ["python3", "start.py"]

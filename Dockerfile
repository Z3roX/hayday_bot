FROM python:3.8-slim

# Installiere gcc und andere Abhängigkeiten
RUN apt-get update && apt-get install -y \
    python3-opencv \
    gcc \
    libssl-dev

# Kopiere die notwendigen Dateien
COPY bot.py /bot.py
COPY app.py /app.py
COPY .env /app/.env

# Installiere Python-Abhängigkeiten
RUN pip install adb-shell numpy imutils requests flask python-dotenv

CMD ["flask", "run", "--host=0.0.0.0"]
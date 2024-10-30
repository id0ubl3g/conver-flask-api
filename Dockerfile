FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y libreoffice && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN python -m venv .venv

RUN .venv/bin/pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [".venv/bin/python", "run.py"]
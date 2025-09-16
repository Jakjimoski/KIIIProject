FROM python:3.11-slim-bookworm

WORKDIR /app

# Инсталирај ги системските зависимости
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV PORT=8000
EXPOSE $PORT

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
FROM python:3.13-slim-bookworm

COPY backend/* /app/*

CMD ["python", "/app/main.py"]

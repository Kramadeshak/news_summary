FROM python:3.13-slim-bookworm

COPY backend/* /app/

COPY requirements.txt ./

RUN pip install -r requirements.txt

WORKDIR /app/

CMD ["python", "main.py"]

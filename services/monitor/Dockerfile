FROM python:3.12-slim

WORKDIR /app

RUN pip install flask flask-cors psutil docker --no-cache-dir

COPY stats.py .

EXPOSE 5000

CMD ["python3", "stats.py"]

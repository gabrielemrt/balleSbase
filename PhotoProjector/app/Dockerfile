FROM python:3.11-slim

WORKDIR /app

# Installiamo Flask o altri pacchetti necessari
RUN pip install flask

# Copiamo i file dell'app
COPY app.py .
COPY logo.png .

# Porta per il webserver
EXPOSE 8091

CMD ["python", "app.py"]

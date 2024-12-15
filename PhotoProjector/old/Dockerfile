FROM python:3.11-slim

WORKDIR /app

# Copia i file dello script
COPY main.py /app/main.py

# Installa le dipendenze necessarie
RUN apt-get update && apt-get install -y feh mpv && apt-get clean

# Installa Flask
RUN pip install flask

CMD ["python3", "main.py"]

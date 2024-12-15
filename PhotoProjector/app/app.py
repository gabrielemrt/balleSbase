from flask import Flask, send_file, abort
import os
import time

app = Flask(__name__)

PHOTOS_DIR = "/mnt/photos"
LOGO_FILE = "logo.png"
CACHE_REFRESH = 5  # secondi tra un refresh e l'altro

# Per tenere traccia dell'ultima foto servita
latest_photo = None
last_check = 0
photos_list = []

def update_photos_list():
    global photos_list, last_check, latest_photo
    now = time.time()
    if now - last_check > CACHE_REFRESH:
        # Aggiorna elenco file
        all_files = [f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        # Ordina per data di modifica, più recente prima
        all_files.sort(key=lambda x: os.path.getmtime(os.path.join(PHOTOS_DIR, x)), reverse=True)
        photos_list = all_files
        last_check = now

@app.route('/')
def show_photo():
    update_photos_list()
    if photos_list:
        # Servi la foto più recente
        recent_photo = photos_list[0]
        return send_file(os.path.join(PHOTOS_DIR, recent_photo))
    else:
        # Nessuna foto trovata, servi il logo
        return send_file(LOGO_FILE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8091)

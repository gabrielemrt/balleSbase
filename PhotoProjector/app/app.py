from flask import Flask, send_file, Response
import os
import time
from datetime import datetime

app = Flask(__name__)

PHOTOS_DIR = "/mnt/photos"
LOGO_FILE = "logo.png"
CACHE_REFRESH = 5           # secondi tra aggiornamenti della lista file
DISPLAY_DURATION = 15       # secondi di visualizzazione per ogni media
AUTO_REFRESH_INTERVAL = 5   # secondi tra un refresh della pagina e l'altro se NON siamo in countdown

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.dng')
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.webm')  # Aggiungi altri formati se necessario

TARGET_TIME = datetime(2024, 12, 26, 16, 15, 0)
COUNTDOWN_THRESHOLD = 120  # 60 secondi prima dell'evento

known_files = set()   # Per tracciare i file già visti
media_queue = []      # Coda di media (lista di tuple (filename, mtime))
current_media = None
current_media_start = 0.0

def is_video(filename):
    return filename.lower().endswith(VIDEO_EXTENSIONS)

def is_image(filename):
    return filename.lower().endswith(IMAGE_EXTENSIONS)

def update_media_list():
    global known_files, media_queue
    all_files = [f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith(IMAGE_EXTENSIONS + VIDEO_EXTENSIONS)]
    # Ordina per data di modifica, dal più vecchio al più recente
    all_files.sort(key=lambda x: os.path.getmtime(os.path.join(PHOTOS_DIR, x)), reverse=False)

    for f in all_files:
        if f not in known_files:
            file_mtime = os.path.getmtime(os.path.join(PHOTOS_DIR, f))
            media_queue.append((f, file_mtime))
            known_files.add(f)

def get_current_media():
    """Determina quale media mostrare in base alla coda e alla durata."""
    global current_media, current_media_start, media_queue
    now = time.time()

    # Se non abbiamo un media attuale o è scaduto il suo tempo
    if current_media is None or (now - current_media_start) > DISPLAY_DURATION:
        # Passa al prossimo in coda se presente
        if media_queue:
            current_media, _ = media_queue.pop(0)
            current_media_start = now
        else:
            current_media = None
            current_media_start = 0.0

    return current_media

@app.route('/')
def show_media():
    now = datetime.now()

    # Calcola quanti secondi mancano al TARGET_TIME
    seconds_to_target = (TARGET_TIME - now).total_seconds()

    # Determiniamo l'intervallo di refresh
    if seconds_to_target > COUNTDOWN_THRESHOLD:
        # Prima dei 2 minuti finali
        refresh_interval = AUTO_REFRESH_INTERVAL
    elif 0 <= seconds_to_target <= COUNTDOWN_THRESHOLD:
        # Durante i 2 minuti finali (countdown), ricarichiamo ogni secondo
        refresh_interval = 1
    else:
        # Oltre l'orario target
        refresh_interval = AUTO_REFRESH_INTERVAL

    if seconds_to_target > COUNTDOWN_THRESHOLD:
        # Mancano più di 2 minuti all’evento: mostra i media
        update_media_list()
        media = get_current_media()
        if media is not None:
            if is_video(media):
                media_tag = f'<video src="/current_media" autoplay muted loop></video>'
            else:
                media_tag = f'<img src="/current_media" alt="Current Media">'
        else:
            # Nessun media in coda: mostra il logo
            media_tag = f'<img src="/current_media" alt="Current Media">'
    elif 0 <= seconds_to_target <= COUNTDOWN_THRESHOLD:
        # Siamo nei 2 minuti finali: mostra il countdown
        sec_remaining = int(seconds_to_target)
        media_tag = f'<h1 style="font-size:10vw; color:#fff;">{sec_remaining}</h1>'
    else:
        # TARGET_TIME superato: mostra il logo (o contenuto a tua scelta)
        media_tag = f'<img src="/current_media" alt="Current Media">'

    debug_info = f"<p>DEBUG: seconds_to_target = {int(seconds_to_target)}</p>"
    html_content = f'''
    <html>
      <head>
        <meta http-equiv="refresh" content="{refresh_interval}">
        <title>Countdown Demo</title>
        <style>
          body {{
            background-color: #000;
            color: #fff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100vw;
            font-family: Arial, sans-serif;
          }}
          img, video {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
          }}
          h1 {{
            margin: 0;
            padding: 0;
          }}
        </style>
      </head>
      <body>
        {debug_info}
        {media_tag}
      </body>
    </html>
    '''

    return Response(html_content, mimetype='text/html')

@app.route('/current_media')
def current_media_file():
    now = datetime.now()
    seconds_to_target = (TARGET_TIME - now).total_seconds()

    if seconds_to_target <= COUNTDOWN_THRESHOLD:
        # Durante il countdown (o dopo), mostriamo il logo
        return send_file(LOGO_FILE)
    else:
        # Altrimenti, mostriamo il media attuale (o il logo se non c'è)
        if current_media is not None:
            return send_file(os.path.join(PHOTOS_DIR, current_media))
        else:
            return send_file(LOGO_FILE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8091)
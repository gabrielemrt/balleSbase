from flask import Flask, send_file, Response
import os
import time
from datetime import datetime, timedelta

app = Flask(__name__)

PHOTOS_DIR = "/mnt/photos"
LOGO_FILE = "logo.png"
CACHE_REFRESH = 5           # secondi tra aggiornamenti della lista file
DISPLAY_DURATION = 15       # secondi di visualizzazione per ogni media
AUTO_REFRESH_INTERVAL = 5   # secondi tra un refresh della pagina e l'altro

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif')
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.webm')  # Aggiungi altri formati se necessario

# Imposta l'orario bersaglio (15 dicembre 2024, 14:05)
TARGET_TIME = datetime(2024, 12, 15, 14, 5, 0)

known_files = set()  # per tracciare i file già visti
media_queue = []      # coda di file (tuple (filename, mtime))
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

    # Aggiunge in coda i nuovi file
    for f in all_files:
        if f not in known_files:
            file_mtime = os.path.getmtime(os.path.join(PHOTOS_DIR, f))
            media_queue.append((f, file_mtime))
            known_files.add(f)

def get_current_media():
    global current_media, current_media_start, media_queue

    now = time.time()

    # Se non abbiamo un media attuale o è scaduto il suo tempo
    if current_media is None or (now - current_media_start) > DISPLAY_DURATION:
        # Passa al prossimo in coda se c'è
        if media_queue:
            current_media, _ = media_queue.pop(0)
            current_media_start = now
        else:
            current_media = None
            current_media_start = 0.0

    return current_media

@app.route('/')
def show_media():
    # Calcola i tempi
    now = datetime.now()
    time_to_target = (TARGET_TIME - now).total_seconds()

    # Se manca meno di un minuto al TARGET_TIME, mostra il countdown
    if 0 < time_to_target <= 60:
        return show_countdown(time_to_target)

    # Se il tempo è passato (dopo il target time), mostra il logo o altro
    if time_to_target <= 0:
        return show_after_countdown()

    # Altrimenti continua con la logica immagini/video
    update_media_list()
    media = get_current_media()

    if media is not None:
        # Controlliamo se è un video o un'immagine
        if is_video(media):
            media_tag = f'<video src="/current_media" autoplay muted loop></video>'
        else:
            media_tag = f'<img src="/current_media" alt="Current Media">'
    else:
        # Mostriamo il logo se non c'è nessun media in coda
        media_tag = f'<img src="/current_media" alt="Current Media">'

    html_content = f'''
    <html>
      <head>
        <meta http-equiv="refresh" content="{AUTO_REFRESH_INTERVAL}">
        <title>Photo/Video Projector</title>
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
          }}
          img, video {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
          }}
        </style>
      </head>
      <body>
        {media_tag}
      </body>
    </html>
    '''
    return Response(html_content, mimetype='text/html')

def show_countdown(time_to_target):
    # time_to_target sono i secondi rimanenti
    target_ts = int(TARGET_TIME.timestamp() * 1000)  # in millisecondi

    html_content = f'''
    <html>
      <head>
        <title>Countdown</title>
        <meta http-equiv="refresh" content="{AUTO_REFRESH_INTERVAL}">
        <style>
          body {{
            background-color: #000;
            color: #fff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            height: 100vh;
            width: 100vw;
            font-family: sans-serif;
            font-size: 5em;
          }}
          #countdown {{
            display: flex;
            justify-content: center;
            align-items: center;
          }}
        </style>
      </head>
      <body>
        <div id="countdown">...loading</div>
        <script>
          var targetTime = {target_ts}; // millisecondi
          function updateCountdown() {{
            var now = new Date().getTime();
            var distance = targetTime - now;

            if (distance <= 0) {{
              // Scaduto il tempo, ricarica per mostrare altro
              window.location.reload();
              return;
            }}

            var seconds = Math.floor(distance / 1000);
            document.getElementById("countdown").innerText = seconds + "s";
          }}

          updateCountdown();
          setInterval(updateCountdown, 1000);
        </script>
      </body>
    </html>
    '''
    return Response(html_content, mimetype='text/html')

def show_after_countdown():
    # Dopo il target time, mostra il logo o qualcos'altro
    html_content = f'''
    <html>
      <head>
        <title>Dopo il Countdown</title>
        <style>
          body {{
            background-color: #000;
            color: #fff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            height: 100vh;
            width: 100vw;
            font-family: sans-serif;
            font-size: 3em;
          }}
          img {{
            max-width: 100%;
            max-height: 100%;
          }}
        </style>
      </head>
      <body>
        <div>Il tempo è scaduto!</div>
        <img src="/logo" alt="Logo After Countdown">
      </body>
    </html>
    '''
    return Response(html_content, mimetype='text/html')

@app.route('/current_media')
def current_media_file():
    global current_media
    if current_media is not None:
        return send_file(os.path.join(PHOTOS_DIR, current_media))
    else:
        return send_file(LOGO_FILE)

@app.route('/logo')
def serve_logo():
    return send_file(LOGO_FILE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8091)

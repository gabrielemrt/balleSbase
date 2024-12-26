from flask import Flask, send_file, Response
import os
import time
from datetime import datetime

app = Flask(__name__)

PHOTOS_DIR = "/mnt/photos"
LOGO_FILE = "logo.png"
CACHE_REFRESH = 5            # secondi tra aggiornamenti della lista file
DISPLAY_DURATION = 15        # secondi di visualizzazione per ogni media
AUTO_REFRESH_INTERVAL = 5    # refresh standard
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif')
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.webm')


TARGET_TIME = datetime(2024, 12, 26, 22, 55, 0)
# Countdown di 120 secondi (2 minuti), solo come esempio
COUNTDOWN_THRESHOLD = 120

known_files = set()
media_queue = []
current_media = None
current_media_start = 0.0

def is_video(filename):
    return filename.lower().endswith(VIDEO_EXTENSIONS)

def is_image(filename):
    return filename.lower().endswith(IMAGE_EXTENSIONS)

def update_media_list():
    global known_files, media_queue
    all_files = [f for f in os.listdir(PHOTOS_DIR) 
                 if f.lower().endswith(IMAGE_EXTENSIONS + VIDEO_EXTENSIONS)]
    all_files.sort(key=lambda x: os.path.getmtime(os.path.join(PHOTOS_DIR, x)), 
                   reverse=False)

    for f in all_files:
        if f not in known_files:
            file_mtime = os.path.getmtime(os.path.join(PHOTOS_DIR, f))
            media_queue.append((f, file_mtime))
            known_files.add(f)

def get_current_media():
    global current_media, current_media_start, media_queue
    now = time.time()
    if current_media is None or (now - current_media_start) > DISPLAY_DURATION:
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
    seconds_to_target = (TARGET_TIME - now).total_seconds()

    # Determiniamo l'intervallo di refresh
    if seconds_to_target > COUNTDOWN_THRESHOLD:
        refresh_interval = AUTO_REFRESH_INTERVAL
    elif 0 <= seconds_to_target <= COUNTDOWN_THRESHOLD:
        refresh_interval = 1
    else:
        refresh_interval = AUTO_REFRESH_INTERVAL

    # Costruiamo il media_tag in base allo stato
    if seconds_to_target > COUNTDOWN_THRESHOLD:
        # Manca più di 2 minuti all'evento: mostra i media
        update_media_list()
        media = get_current_media()
        if media is not None:
            if is_video(media):
                media_tag = '<video src="/current_media" autoplay muted loop></video>'
            else:
                media_tag = '<img src="/current_media" alt="Current Media">'
        else:
            media_tag = '<img src="/current_media" alt="Current Media">'
    elif 0 <= seconds_to_target <= COUNTDOWN_THRESHOLD:
        # Siamo nei 2 minuti finali: mostra countdown formattato M:SS
        sec_remaining = int(seconds_to_target)
        minutes = sec_remaining // 60
        seconds = sec_remaining % 60
        # Formattazione con zero davanti ai secondi se < 10
        formatted_time = f"{minutes}:{seconds:02d}"
        media_tag = f'<h1 style="font-size:10vw; color:#fff;">{formatted_time}</h1>'
    else:
        # Oltre l'orario target: mostra il logo o altro
        media_tag = '<img src="/current_media" alt="Current Media">'

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
        # Durante countdown (o dopo), mostra il logo
        return send_file(LOGO_FILE)
    else:
        # Altrimenti media o logo
        if current_media is not None:
            return send_file(os.path.join(PHOTOS_DIR, current_media))
        else:
            return send_file(LOGO_FILE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8091)

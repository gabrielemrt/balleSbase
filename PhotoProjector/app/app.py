from flask import Flask, send_file, Response
import os
import time

app = Flask(__name__)

PHOTOS_DIR = "/mnt/photos"
LOGO_FILE = "logo.png"
CACHE_REFRESH = 5           # secondi tra aggiornamenti della lista file
DISPLAY_DURATION = 15       # secondi di visualizzazione per ogni media
AUTO_REFRESH_INTERVAL = 5   # secondi tra un refresh della pagina e l'altro

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif')
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.webm')  # Aggiungi altri formati se necessario

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

    # Aggiorna la lista dei file nella cartella
    all_files = [f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith(IMAGE_EXTENSIONS + VIDEO_EXTENSIONS)]
    # Ordina per data di modifica, dal più vecchio al più recente
    all_files.sort(key=lambda x: os.path.getmtime(os.path.join(PHOTOS_DIR, x)), reverse=False)

    # Controlla i nuovi file non ancora noti e aggiungili in coda
    for f in all_files:
        if f not in known_files:
            file_mtime = os.path.getmtime(os.path.join(PHOTOS_DIR, f))
            media_queue.append((f, file_mtime))
            known_files.add(f)

def get_current_media():
    """Gestisce la logica di quale file mostrare:
       - Se il current_media è scaduto, passa al successivo in coda.
       - Se non ci sono media in coda e current_media è scaduto, mostra il logo.
    """
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
    # Aggiorniamo la lista dei media disponibili
    update_media_list()

    # Determiniamo il media da mostrare
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


@app.route('/current_media')
def current_media_file():
    global current_media
    if current_media is not None:
        return send_file(os.path.join(PHOTOS_DIR, current_media))
    else:
        return send_file(LOGO_FILE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8091)

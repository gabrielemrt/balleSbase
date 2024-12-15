from flask import Flask, send_file, Response
import os
import time

app = Flask(__name__)

PHOTOS_DIR = "/mnt/photos"
LOGO_FILE = "logo.png"
CACHE_REFRESH = 5          # secondi tra aggiornamenti della lista file
DISPLAY_DURATION = 30       # secondi in cui un media rimane mostrato
AUTO_REFRESH_INTERVAL = 5   # secondi tra un refresh della pagina e l'altro

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif')
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.webm')  # Aggiungi altri formati se necessario

latest_media = None
latest_media_time = 0
last_check = 0
media_list = []

def update_media_list():
    global media_list, last_check, latest_media, latest_media_time
    now = time.time()
    if now - last_check > CACHE_REFRESH:
        all_files = [f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith(IMAGE_EXTENSIONS + VIDEO_EXTENSIONS)]
        all_files.sort(key=lambda x: os.path.getmtime(os.path.join(PHOTOS_DIR, x)), reverse=True)
        media_list = all_files

        if media_list:
            most_recent = media_list[0]
            recent_path = os.path.join(PHOTOS_DIR, most_recent)
            recent_mtime = os.path.getmtime(recent_path)

            if latest_media is None or recent_mtime > latest_media_time:
                latest_media = most_recent
                latest_media_time = recent_mtime

        last_check = now

def is_video(filename):
    return filename.lower().endswith(VIDEO_EXTENSIONS)

def is_image(filename):
    return filename.lower().endswith(IMAGE_EXTENSIONS)

@app.route('/')
def show_media():
    update_media_list()
    now = time.time()

    # Determiniamo il file da mostrare
    if latest_media is not None and (now - latest_media_time) <= DISPLAY_DURATION:
        chosen_file = "/current_media"
        is_media_video = is_video(latest_media)
    else:
        chosen_file = "/current_media"
        is_media_video = False  # Per il logo, è sempre un'immagine

    # In base al tipo di file (video o immagine) cambiamo il tag HTML
    if is_media_video:
        # Video autoplay, muto, loop
        media_tag = f'<video src="{chosen_file}" autoplay muted loop></video>'
    else:
        # Immagine
        media_tag = f'<img src="{chosen_file}" alt="Current Media">'

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
def current_media():
    now = time.time()
    if latest_media is not None and (now - latest_media_time) <= DISPLAY_DURATION:
        return send_file(os.path.join(PHOTOS_DIR, latest_media))
    else:
        return send_file(LOGO_FILE)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8091)

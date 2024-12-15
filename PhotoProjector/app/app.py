from flask import Flask, send_file, Response
import os
import time

app = Flask(__name__)

PHOTOS_DIR = "/mnt/photos"
LOGO_FILE = "logo.png"
CACHE_REFRESH = 5         # secondi tra aggiornamenti della lista file
DISPLAY_DURATION = 30      # secondi in cui una foto rimane mostrata
AUTO_REFRESH_INTERVAL = 5  # secondi tra un refresh e l'altro della pagina

latest_photo = None
latest_photo_time = 0
last_check = 0
photos_list = []


def update_photos_list():
    global photos_list, last_check, latest_photo, latest_photo_time
    now = time.time()
    if now - last_check > CACHE_REFRESH:
        all_files = [f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        all_files.sort(key=lambda x: os.path.getmtime(os.path.join(PHOTOS_DIR, x)), reverse=True)
        photos_list = all_files

        if photos_list:
            most_recent = photos_list[0]
            recent_path = os.path.join(PHOTOS_DIR, most_recent)
            recent_mtime = os.path.getmtime(recent_path)
            
            if latest_photo is None or recent_mtime > latest_photo_time:
                latest_photo = most_recent
                latest_photo_time = recent_mtime

        last_check = now


@app.route('/')
def show_photo():
    update_photos_list()
    now = time.time()

    # Controlla se abbiamo una foto recente
    if latest_photo is not None and (now - latest_photo_time) <= DISPLAY_DURATION:
        chosen_file = "/current_image"
    else:
        chosen_file = "/current_image"

    html_content = f'''
    <html>
      <head>
        <meta http-equiv="refresh" content="{AUTO_REFRESH_INTERVAL}">
        <title>Photo Projector</title>
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
          img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
          }}
        </style>
      </head>
      <body>
        <img src="{chosen_file}" alt="Current Image">
      </body>
    </html>
    '''

    return Response(html_content, mimetype='text/html')


@app.route('/current_image')
def current_image():
    now = time.time()
    if latest_photo is not None and (now - latest_photo_time) <= DISPLAY_DURATION:
        return send_file(os.path.join(PHOTOS_DIR, latest_photo))
    else:
        return send_file(LOGO_FILE)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8091)

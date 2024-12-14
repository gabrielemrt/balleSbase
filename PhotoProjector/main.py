import os
import time
from pathlib import Path
from flask import Flask

# Configura il percorso della cartella condivisa SMB montata su Ubuntu
NAS_FOLDER = "/mnt/nas_photos"  # Percorso della cartella SMB montata
LOGO_FILE = f"{NAS_FOLDER}/logo.png"  # Percorso del logo nella cartella NAS
SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".mp4", ".avi"]

app = Flask(__name__)

def get_files(folder):
    """Ottiene i file supportati dalla cartella."""
    return [f for f in Path(folder).iterdir() if f.suffix in SUPPORTED_EXTENSIONS]

def display_file(file_path):
    """Mostra un file immagine o video sullo schermo."""
    if file_path.suffix in [".jpg", ".jpeg", ".png"]:
        os.system(f"feh --fullscreen --auto-zoom {file_path}")
    elif file_path.suffix in [".mp4", ".avi"]:
        os.system(f"mpv --fs --loop {file_path}")


def display_logo():
    """Mostra il logo predefinito."""
    os.system(f"feh --fullscreen --auto-zoom {LOGO_FILE}")

@app.route("/display")
def display_photos():
    already_displayed = set()
    files = get_files(NAS_FOLDER)
    new_files = [file for file in files if file not in already_displayed]

    if new_files:
        for file in new_files:
            display_file(file)
            already_displayed.add(file)
        return "New files displayed!", 200
    else:
        display_logo()
        return "Displayed logo!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8091)

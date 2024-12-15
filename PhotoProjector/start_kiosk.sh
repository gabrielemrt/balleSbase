#!/bin/bash

# Indirizzo della pagina da aprire
URL="http://192.168.100.102:8091"

# Attendi 10 secondi per garantire che la rete sia disponibile
sleep 10

# Avvia Chromium in modalità kiosk
/usr/bin/chromium-browser --noerrdialogs --kiosk $URL

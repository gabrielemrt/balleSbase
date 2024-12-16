#!/bin/bash
# Disabilita screensaver e gestione energetica del display (opzionale)
xset s off
xset -dpms
xset s noblank

# Attendi qualche secondo per assicurarsi che l'ambiente grafico sia pronto (opzionale)
sleep 5

# Avvia Chromium in modalità kiosk con la pagina desiderata
chromium-browser --noerrdialogs --disable-infobars --kiosk https://photoprojector.mrt3.it/

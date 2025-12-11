# 🚀 Quick Start Guide

## Setup Completo in 5 Minuti

### 1️⃣ Crea la Struttura

```bash
mkdir -p photowall-capodanno/{upload-service/public,display-service/public,shared/uploads}
cd photowall-capodanno
```

### 2️⃣ Scarica/Crea i File

Puoi usare uno di questi metodi:

**Metodo A: Git Clone (se hai repository)**
```bash
git clone https://tuo-repo/photowall-capodanno.git
cd photowall-capodanno
```

**Metodo B: Download ZIP e estrai**
```bash
unzip photowall-capodanno.zip
cd photowall-capodanno
```

**Metodo C: Crea manualmente** (segui STRUTTURA_DIRECTORY.md)

### 3️⃣ Configura

```bash
# Copia .env
cp .env.example .env

# Modifica se necessario
nano .env

# Aggiungi logo e QR code
cp /percorso/logo.png shared/uploads/
cp /percorso/qr-code.png shared/uploads/

# Verifica permessi
chmod 755 shared/uploads
```

### 4️⃣ Avvia

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Verifica
docker-compose ps
docker-compose logs -f
```

### 5️⃣ Configura Caddy

```bash
# Modifica il tuo Caddyfile
sudo nano /etc/caddy/Caddyfile

# Aggiungi la configurazione dal File 16

# Reload Caddy
sudo systemctl reload caddy
```

---

## 🌐 URL di Accesso

- **Upload (per utenti)**: https://photos.tuodominio.it
- **Display (per proiettore)**: https://photos.tuodominio.it/display

---

## ✅ Test Veloce

```bash
# Test health
curl http://localhost:8090/health
curl http://localhost:8091/health

# Se ottieni {"status":"ok"} sei pronto! 🎉
```

---

## 🎯 Uso Durante la Festa

1. **Stampa i QR code** che puntano a `https://photos.tuodominio.it`
2. **Apri nel browser del proiettore** `https://photos.tuodominio.it/display`
3. **Attacca i QR code** in giro per la sala
4. **La gente scatta e carica** foto dal cellulare
5. **Le foto appaiono automaticamente** sul maxischermo

---

## 🔧 Comandi Utili

```bash
# Restart
docker-compose restart

# Stop
docker-compose down

# Logs
docker-compose logs -f upload-service
docker-compose logs -f display-service

# Backup foto
tar -czf backup-$(date +%Y%m%d).tar.gz shared/uploads/

# Pulizia
docker-compose down -v  # ATTENZIONE: cancella tutto!
```

---

## 📱 Genera QR Code

```bash
# Installa qrencode
sudo apt install qrencode

# Genera QR code
qrencode -o shared/uploads/qr-code.png -s 10 "https://photos.tuodominio.it"
```

Oppure usa online:
- https://www.qr-code-generator.com/
- https://qrcode.tec-it.com/

---

## 🎊 Buona Festa!

Il sistema è pronto. Durante l'evento:
- Controlla i logs: `docker-compose logs -f`
- Monitora: `docker stats`
- Backup periodico: ogni ora fai backup della cartella `shared/uploads/`
# YouTube Downloader

Logiciel avec interface graphique pour telecharger des videos YouTube en MP4 ou MP3.

## Fonctionnalites
- Telechargement de plusieurs videos a la fois (coller les liens un par ligne)
- Formats : MP4 meilleure qualite, MP4 1080p, MP4 720p, MP3
- Choix du dossier de destination
- Log de progression en temps reel

---

## Installation sur Windows

### Etape 1 — Installer Python
Telecharge et installe Python depuis : https://www.python.org/downloads/

> **Important** : coche la case **"Add Python to PATH"** pendant l'installation.

### Etape 2 — Lancer l'installation automatique
Double-clique sur le fichier **`install_windows.bat`**

Ce script installe automatiquement :
- `yt-dlp` (telechargeur YouTube)
- `ffmpeg` (pour la meilleure qualite video)

### Etape 3 — Lancer le logiciel
Double-clique sur **`lancer.bat`**

---

## Installation sur macOS

```bash
# Installer yt-dlp
pip3 install yt-dlp

# Installer ffmpeg (optionnel, meilleure qualite)
brew install ffmpeg

# Lancer le logiciel
python3 downloader.py
```

---

## Utilisation

1. Colle tes liens YouTube dans la zone de texte (un par ligne)
2. Choisis le format (MP4, MP3...)
3. Choisis le dossier de destination
4. Clique sur **TELECHARGER**

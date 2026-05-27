@echo off
echo ========================================
echo  Installation YouTube Downloader
echo ========================================
echo.

:: Verifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe !
    echo Telecharge Python sur https://www.python.org/downloads/
    echo Coche bien "Add Python to PATH" pendant l'installation.
    pause
    exit /b 1
)
echo [OK] Python detecte

:: Creer environnement virtuel
echo.
echo Creation de l'environnement virtuel...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible de creer l'environnement virtuel
    pause
    exit /b 1
)
echo [OK] Environnement virtuel cree

:: Activer et installer yt-dlp
echo.
echo Installation de yt-dlp...
call venv\Scripts\activate.bat
pip install yt-dlp
if %errorlevel% neq 0 (
    echo [ERREUR] Echec installation yt-dlp
    pause
    exit /b 1
)
echo [OK] yt-dlp installe

:: Installer ffmpeg via winget si disponible
echo.
echo Installation de ffmpeg (optionnel, pour meilleure qualite)...
winget install --id Gyan.FFmpeg -e --silent >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] ffmpeg installe
) else (
    echo [INFO] ffmpeg non installe - le logiciel fonctionne quand meme
)

echo.
echo ========================================
echo  Installation terminee !
echo  Lance "lancer.bat" pour demarrer
echo ========================================
pause

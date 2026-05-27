@echo off
echo ========================================
echo  Creation du fichier EXE
echo ========================================
echo.

:: Verifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe !
    pause
    exit /b 1
)

:: Installer pyinstaller et yt-dlp
echo Installation de pyinstaller et yt-dlp...
pip install pyinstaller yt-dlp
echo.

:: Creer le EXE
echo Creation du EXE en cours...
pyinstaller --onefile --windowed --name "YouTubeDownloader" downloader.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  EXE cree avec succes !
    echo  Fichier : dist\YouTubeDownloader.exe
    echo ========================================
) else (
    echo [ERREUR] La creation du EXE a echoue
)
pause

@echo off
python downloader.py
if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Probleme au lancement. As-tu lance install_windows.bat ?
    pause
)

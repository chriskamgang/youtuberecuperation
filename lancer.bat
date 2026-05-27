@echo off

:: Utiliser l'environnement virtuel si disponible, sinon Python global
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

python downloader.py

if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Probleme au lancement. As-tu lance install_windows.bat ?
    pause
)

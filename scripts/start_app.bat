@echo off
chcp 65001 > nul
echo ==========================================
echo   KASIR TOKO SEMBAKO - START APPLICATION
echo ==========================================
echo.

REM Change to parent directory (project root)
cd /d "%~dp0\.."

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv and run PowerShell script
echo Activating virtual environment and starting app...
powershell -ExecutionPolicy Bypass -Command "& { . .\venv\Scripts\Activate.ps1; python app/app_simple.py }"

pause

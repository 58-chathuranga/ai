@echo off
setlocal
cd /d "%~dp0"
echo ===========================================
echo       NEXORA AI - Windows Setup
echo ===========================================
py -3.12 --version >nul 2>&1
if errorlevel 1 (
  echo Python 3.12 was not found.
  echo Install Python 3.12 from https://www.python.org/downloads/
  echo During installation, tick "Add python.exe to PATH".
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  py -3.12 -m venv .venv
  if errorlevel 1 goto failed
)
echo Updating pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto failed
echo Installing packages...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed
if not exist ".env" (
  copy ".env.example" ".env" >nul
  echo Created .env from .env.example.
)
echo.
echo Setup complete. Open .env and add your Discord and Gemini API keys.
echo Then run start.bat.
pause
exit /b 0
:failed
echo.
echo Setup failed. Check the error above and make sure you have internet access.
pause
exit /b 1

@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Please run setup.bat first.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" bot.py
if errorlevel 1 (
  echo.
  echo NEXORA AI stopped with an error. Read the message above.
)
pause

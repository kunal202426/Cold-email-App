@echo off
echo ===================================================
echo     Starting Cold Email Outreach App...
echo ===================================================

:: Start Backend in a new window
echo Starting FastAPI Backend...
start cmd /k "cd backend && call venv\Scripts\activate.bat && uvicorn main:app --reload --port 8000"

:: Wait a second for backend to spin up
timeout /t 2 /nobreak >nul

:: Start Frontend in a new window
echo Starting React/Vite Frontend...
start cmd /k "cd frontend && npm run dev"

echo.
echo ===================================================
echo   App is now running!
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000/docs
echo ===================================================
echo Keep these windows open while developing.
echo Close them to shut down the servers.
pause

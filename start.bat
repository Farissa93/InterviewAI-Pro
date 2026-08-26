@echo off
REM Interview Prep AI - Startup Script (Batch version)
REM This script starts both the backend API and Streamlit frontend

echo ========================================
echo   Interview Prep AI - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo [✓] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [!] Virtual environment not found
    echo     Please create one with: python -m venv venv
    echo.
)

echo [*] Starting FastAPI backend...
start "Interview Prep API" cmd /k "uvicorn backend.main:app --reload --port 8000"

REM Give backend time to start
timeout /t 3 /nobreak > nul

echo [*] Starting Streamlit frontend...
echo.
echo ========================================
echo   Services Running:
echo   - Backend API: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo   - Streamlit: http://localhost:8501
echo ========================================
echo.
echo Press Ctrl+C to stop the frontend
echo (Close the backend window separately)
echo.

streamlit run streamlit_app.py

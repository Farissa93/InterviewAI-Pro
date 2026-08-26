# Interview Prep AI - Startup Script
# This script starts both the backend API and Streamlit frontend

Write-Host "🎯 Starting Interview Prep AI..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "✓ Activating virtual environment..." -ForegroundColor Green
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠ Virtual environment not found at .\venv" -ForegroundColor Yellow
    Write-Host "  Please create one with: python -m venv venv" -ForegroundColor Yellow
    Write-Host ""
}

# Start backend in background
Write-Host "🚀 Starting FastAPI backend on http://localhost:8000..." -ForegroundColor Green
$backend = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; uvicorn backend.main:app --reload --port 8000" -PassThru

# Give backend time to start
Start-Sleep -Seconds 3

# Start Streamlit frontend
Write-Host "🎨 Starting Streamlit frontend on http://localhost:8501..." -ForegroundColor Green
Write-Host ""
Write-Host "✓ Both services starting..." -ForegroundColor Green
Write-Host "  - Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  - API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  - Streamlit App: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop both services" -ForegroundColor Yellow
Write-Host ""

# Start Streamlit (this will block)
streamlit run streamlit_app.py

# Cleanup when Streamlit is stopped
Write-Host ""
Write-Host "Stopping backend..." -ForegroundColor Yellow
Stop-Process -Id $backend.Id -Force
Write-Host "✓ All services stopped" -ForegroundColor Green

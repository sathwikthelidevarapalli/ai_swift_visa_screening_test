# ==========================================
# SwiftVisa Production Startup Script
# ==========================================
# This script starts the backend with production settings

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SwiftVisa Backend - Production Startup  " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Check if .env file exists
if (-Not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Please edit .env with your API keys" -ForegroundColor Green
}

# Check if vectorstore exists
if (-Not (Test-Path "vectorstore\chroma.sqlite3")) {
    Write-Host "⚠️  Vectorstore not found!" -ForegroundColor Yellow
    Write-Host "Creating vectorstore..." -ForegroundColor Yellow
    python scripts\create_vectorstore.py
}

# Create logs directory if it doesn't exist
if (-Not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "✅ Created logs directory" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting SwiftVisa Backend (Production Mode)..." -ForegroundColor Green
Write-Host "   Host: 0.0.0.0" -ForegroundColor Cyan
Write-Host "   Port: 8000" -ForegroundColor Cyan
Write-Host "   Workers: 4" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Logs: logs/swiftvisa.log" -ForegroundColor Yellow
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start with Gunicorn (production WSGI server)
# Falls back to uvicorn if gunicorn is not available
try {
    gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --log-level info --access-logfile logs/access.log --error-logfile logs/error.log
} catch {
    Write-Host "⚠️  Gunicorn not available, using uvicorn..." -ForegroundColor Yellow
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
}

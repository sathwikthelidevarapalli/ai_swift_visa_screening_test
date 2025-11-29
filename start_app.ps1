# SwiftVisa Application Startup Script
# This script starts both the backend and frontend servers

Write-Host "🚀 Starting SwiftVisa Application..." -ForegroundColor Cyan
Write-Host ""

# Start Backend (FastAPI)
Write-Host "📡 Starting Backend Server (FastAPI) on port 8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd d:\ai_swiftvisa; Write-Host '🔷 Backend Server' -ForegroundColor Blue; D:/ai_swiftvisa/.venv/Scripts/python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000"

# Wait for backend to initialize
Write-Host "⏳ Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# Start Frontend (React)
Write-Host "🎨 Starting Frontend Server (React) on port 3000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd d:\ai_swiftvisa\my_visa_app\frontend_react; Write-Host '🔷 Frontend Server' -ForegroundColor Blue; npm start"

# Wait for frontend to initialize
Write-Host "⏳ Waiting for frontend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "✅ SwiftVisa Application Started Successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access Points:" -ForegroundColor Cyan
Write-Host "   Backend API:  http://localhost:8000" -ForegroundColor White
Write-Host "   Frontend App: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Opening frontend in browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "🎉 Ready to check visa eligibility!" -ForegroundColor Green
Write-Host "📝 Check README_SETUP.md for detailed instructions" -ForegroundColor Cyan

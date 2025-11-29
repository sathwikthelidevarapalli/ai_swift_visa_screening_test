# ==========================================
# SwiftVisa Setup Script (Windows)
# ==========================================
# This script sets up the entire project from scratch

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "     SwiftVisa - Initial Setup Script     " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "🔍 Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.1[2-9]") {
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python 3.12+ required!" -ForegroundColor Red
    Write-Host "Current: $pythonVersion" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
if (-Not (Test-Path ".venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "📦 Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "   This may take a few minutes..." -ForegroundColor Gray
pip install -r requirements.txt --quiet
Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Create environment file
if (-Not (Test-Path ".env")) {
    Write-Host "⚙️  Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env created from template" -ForegroundColor Green
    Write-Host "⚠️  Please edit .env and add your API keys!" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Create necessary directories
Write-Host "📁 Creating necessary directories..." -ForegroundColor Yellow
$dirs = @("logs", "data/raw", "data/clean", "data/chunks")
foreach ($dir in $dirs) {
    if (-Not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "✅ Directories created" -ForegroundColor Green

# Check if vectorstore exists
if (-Not (Test-Path "vectorstore\chroma.sqlite3")) {
    Write-Host "🗄️  Vectorstore not found" -ForegroundColor Yellow
    Write-Host "Creating vectorstore from policy documents..." -ForegroundColor Yellow
    Write-Host "   This may take a few minutes..." -ForegroundColor Gray
    python scripts\create_vectorstore.py
    Write-Host "✅ Vectorstore created" -ForegroundColor Green
} else {
    Write-Host "✅ Vectorstore already exists" -ForegroundColor Green
}

# Test vectorstore
Write-Host "🧪 Testing vectorstore..." -ForegroundColor Yellow
python scripts\test_vectorstore.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Vectorstore test passed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Vectorstore test failed" -ForegroundColor Yellow
}

# Check if Node.js is installed
Write-Host ""
Write-Host "🔍 Checking Node.js installation..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($nodeVersion -match "v\d+") {
    Write-Host "✅ Node.js $nodeVersion" -ForegroundColor Green
    
    # Install React dependencies
    Write-Host "📦 Installing React dependencies..." -ForegroundColor Yellow
    Set-Location "my_visa_app\frontend_react"
    npm install --silent
    Set-Location "..\..\"
    Write-Host "✅ React dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Node.js not found - React frontend will not work" -ForegroundColor Yellow
    Write-Host "   Install from: https://nodejs.org/" -ForegroundColor Gray
}

# Setup complete
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "     ✅ Setup Complete!                    " -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Edit .env file with your API keys:" -ForegroundColor Yellow
Write-Host "   notepad .env" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start the backend:" -ForegroundColor Yellow
Write-Host "   .\start_app.ps1" -ForegroundColor Gray
Write-Host "   or" -ForegroundColor Gray
Write-Host "   python -m uvicorn main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Start the frontend (in another terminal):" -ForegroundColor Yellow
Write-Host "   cd my_visa_app\frontend_react" -ForegroundColor Gray
Write-Host "   npm start" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Access the application:" -ForegroundColor Yellow
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Gray
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Gray
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   - README.md - Project overview" -ForegroundColor Gray
Write-Host "   - DEPLOYMENT.md - Deployment guide" -ForegroundColor Gray
Write-Host "   - API_DOCUMENTATION.md - API reference" -ForegroundColor Gray
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green

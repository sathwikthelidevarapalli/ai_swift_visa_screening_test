#!/bin/bash
# ==========================================
# SwiftVisa Production Startup Script (Linux/Mac)
# ==========================================

echo "============================================"
echo "  SwiftVisa Backend - Production Startup  "
echo "============================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo "✅ Please edit .env with your API keys"
fi

# Check if vectorstore exists
if [ ! -f "vectorstore/chroma.sqlite3" ]; then
    echo "⚠️  Vectorstore not found!"
    echo "Creating vectorstore..."
    python scripts/create_vectorstore.py
fi

# Create logs directory if it doesn't exist
mkdir -p logs

echo ""
echo "🚀 Starting SwiftVisa Backend (Production Mode)..."
echo "   Host: 0.0.0.0"
echo "   Port: 8000"
echo "   Workers: 4"
echo ""
echo "📝 Logs: logs/swiftvisa.log"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start with Gunicorn (production WSGI server)
if command -v gunicorn &> /dev/null; then
    gunicorn main:app \
        --workers 4 \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind 0.0.0.0:8000 \
        --log-level info \
        --access-logfile logs/access.log \
        --error-logfile logs/error.log
else
    echo "⚠️  Gunicorn not available, using uvicorn..."
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
fi

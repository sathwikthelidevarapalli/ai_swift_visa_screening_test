# 🚀 SwiftVisa - Quick Start Guide

**Get up and running in 5 minutes!**

---

## Prerequisites

- ✅ Python 3.12+ installed
- ✅ Node.js 18+ installed  
- ✅ Git installed
- ⚠️ OpenAI or Gemini API key (optional but recommended)

---

## Installation & Setup

### Step 1: Clone & Navigate

```bash
git clone <your-repository-url>
cd ai_swiftvisa
```

### Step 2: Automated Setup (Recommended)

**Windows:**
```powershell
.\deployment\setup.ps1
```

**Linux/macOS:**
```bash
chmod +x deployment/setup.sh
./deployment/setup.sh
```

This script will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Setup directories
- ✅ Create vectorstore
- ✅ Install React packages
- ✅ Create .env file

### Step 3: Configure API Keys

Edit the `.env` file:

```bash
# Windows
notepad .env

# Linux/macOS
nano .env
```

Add your API key (at least one):

```env
# Option 1: Google Gemini (Free tier available)
GEMINI_API_KEY=your-actual-gemini-key-here

# Option 2: OpenAI
OPENAI_API_KEY=sk-your-actual-openai-key-here

# Note: System works without API keys in retrieval-only mode
```

**Get API Keys:**
- Google Gemini: https://makersuite.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys

---

## Running the Application

### Method 1: Quick Start Script (Easiest)

**Windows:**
```powershell
.\start_app.ps1
```

This automatically starts both backend and frontend!

### Method 2: Manual Start

**Terminal 1 - Backend:**
```bash
# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1

# Linux/macOS:
source .venv/bin/activate

# Start backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd my_visa_app\frontend_react
npm start
```

### Method 3: Docker (Production)

```bash
docker-compose up --build
```

---

## Access the Application

Once running, open your browser:

- **Frontend (User Interface)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

---

## Using the Application

### 1. Fill the Form

On http://localhost:3000, enter:

- **Country of Citizenship**: e.g., "India"
- **Destination Country**: e.g., "Canada"
- **Purpose of Visit**: Select from dropdown (Study, Work, Tourism, etc.)
- **Length of Stay**: e.g., "365" (days)
- **Age**: e.g., "25"

### 2. Check Status

- Green badge = Backend is online ✅
- Red badge = Backend is offline ⚠️

### 3. Submit

Click "✨ Check Eligibility" button

### 4. View Results

You'll see:
- Detailed eligibility assessment
- Key requirements
- Recommendations
- Next steps
- Provider badge (OpenAI/Gemini/Document-based)

### 5. Actions

- **Copy Result**: Copy assessment to clipboard
- **New Search**: Reset form for new query
- **Reset Form**: Clear all inputs

---

## Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Check eligibility
curl -X POST "http://localhost:8000/check-eligibility" \
  -H "Content-Type: application/json" \
  -d '{
    "countryOfCitizenship": "India",
    "destinationCountry": "Canada",
    "purposeOfVisit": "Study",
    "lengthOfStay": "365",
    "age": "25"
  }'

# Get available countries
curl http://localhost:8000/countries

# Get statistics
curl http://localhost:8000/stats
```

### Using Python

```python
import requests

# Check eligibility
data = {
    "countryOfCitizenship": "India",
    "destinationCountry": "Canada",
    "purposeOfVisit": "Study",
    "lengthOfStay": "365",
    "age": "25"
}

response = requests.post(
    "http://localhost:8000/check-eligibility",
    json=data
)

print(response.json()["eligibility"])
```

### Using Browser

Visit: http://localhost:8000/docs

Click "Try it out" on any endpoint to test interactively!

---

## Running Tests

```bash
# Activate virtual environment first
# Windows:
.\.venv\Scripts\Activate.ps1

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

View coverage report: `open htmlcov/index.html`

---

## Troubleshooting

### Backend Won't Start

**Problem**: `Module not found` errors

**Solution**:
```bash
pip install -r requirements.txt --force-reinstall
```

**Problem**: `Vectorstore not found`

**Solution**:
```bash
python scripts\create_vectorstore.py
```

### Frontend Won't Start

**Problem**: `npm` command not found

**Solution**: Install Node.js from https://nodejs.org/

**Problem**: Dependencies not installed

**Solution**:
```bash
cd my_visa_app\frontend_react
npm install
```

### API Returns Errors

**Problem**: CORS errors in browser

**Solution**: Ensure backend is running on port 8000

**Problem**: "No LLM configured" warnings

**Solution**: This is normal! System works in retrieval-only mode without API keys

### No Results Returned

**Problem**: Empty or no results

**Solution**: 
1. Check vectorstore exists: `ls vectorstore/`
2. Recreate: `python scripts/create_vectorstore.py`
3. Test: `python scripts/test_vectorstore.py`

---

## Stopping the Application

### Manual Mode
- Press `Ctrl+C` in each terminal

### Docker Mode
```bash
docker-compose down
```

---

## What's Next?

### 📚 Read Documentation
- `README.md` - Full project overview
- `DEPLOYMENT.md` - Deploy to production
- `API_DOCUMENTATION.md` - Complete API reference
- `COMPLETION_SUMMARY.md` - Project achievements

### 🚀 Deploy to Production
See `DEPLOYMENT.md` for guides on:
- Render.com
- Railway.app
- Heroku
- Streamlit Cloud

### 🧪 Explore the Code
- `main.py` - Backend API
- `config.py` - Configuration
- `my_visa_app/frontend_react/src/App.js` - Frontend
- `scripts/` - Data processing

### 🎨 Customize
- Add more countries in `data/clean/`
- Modify UI colors in `App.css`
- Add new endpoints in `main.py`
- Adjust prompts in RAG pipeline

---

## Support

### Need Help?

1. **Check Logs**: `logs/swiftvisa.log`
2. **Test Vectorstore**: `python scripts/test_vectorstore.py`
3. **Verify Backend**: http://localhost:8000/health
4. **Review API Docs**: http://localhost:8000/docs
5. **Check Documentation**: All `.md` files in project root

### Common Commands

```bash
# Check Python version
python --version

# Check Node version
node --version

# Check if backend is running
curl http://localhost:8000/health

# View logs
cat logs/swiftvisa.log    # Linux/Mac
type logs\swiftvisa.log   # Windows

# Restart backend
# Stop with Ctrl+C, then:
python -m uvicorn main:app --reload
```

---

## Quick Reference Card

| Action | Command |
|--------|---------|
| Setup Everything | `.\deployment\setup.ps1` |
| Start Backend | `python -m uvicorn main:app --reload` |
| Start Frontend | `cd my_visa_app\frontend_react && npm start` |
| Run Tests | `pytest` |
| View API Docs | http://localhost:8000/docs |
| Check Health | http://localhost:8000/health |
| View Logs | `logs/swiftvisa.log` |
| Stop Server | `Ctrl+C` |

---

## Success Checklist

- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] Vectorstore created
- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:3000
- [ ] Health check returns "healthy"
- [ ] Can submit form and get results
- [ ] Tests pass with `pytest`

If all checked, you're good to go! 🎉

---

**Happy Coding! 🚀**

For detailed information, see the complete documentation in the project root.

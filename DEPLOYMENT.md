# 🚀 SwiftVisa Deployment Guide

Complete guide for deploying SwiftVisa to production environments.

---

## 📋 Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Platform Deployment](#cloud-platform-deployment)
   - [Streamlit Cloud](#streamlit-cloud)
   - [Render](#render)
   - [Railway](#railway)
   - [Heroku](#heroku)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Domain & SSL](#domain--ssl)
7. [Monitoring & Logging](#monitoring--logging)
8. [Troubleshooting](#troubleshooting)

---

## 🏠 Local Development Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- Git

### Steps

1. **Clone and Setup**
```bash
git clone <repository-url>
cd ai_swiftvisa
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Install Frontend Dependencies**
```bash
cd my_visa_app/frontend_react
npm install
cd ../..
```

4. **Run Locally**
```bash
# Terminal 1 - Backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd my_visa_app/frontend_react
npm start
```

5. **Access**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🐳 Docker Deployment

### Build and Run with Docker Compose

1. **Build Images**
```bash
docker-compose build
```

2. **Start Services**
```bash
docker-compose up -d
```

3. **Check Logs**
```bash
docker-compose logs -f
```

4. **Stop Services**
```bash
docker-compose down
```

### Production Docker Setup

**docker-compose.prod.yml**:
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - vectorstore_data:/app/vectorstore
      - logs:/app/logs
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
    restart: always

volumes:
  vectorstore_data:
  logs:
```

---

## ☁️ Cloud Platform Deployment

### 1. Streamlit Cloud

**Best for**: Quick demos and prototypes

**Steps**:

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your repository
5. Set main file: `my_visa_app/app.py`
6. Add secrets in Settings:
```toml
OPENAI_API_KEY = "sk-your-key"
```
7. Deploy

**Note**: Backend needs separate deployment

---

### 2. Render

**Best for**: Full-stack production deployment

#### Backend Deployment

1. **Create render.yaml**:
```yaml
services:
  - type: web
    name: swiftvisa-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: PYTHON_VERSION
        value: 3.12.0
```

2. **Push to GitHub**

3. **Connect to Render**:
   - Go to https://render.com
   - New → Web Service
   - Connect GitHub repository
   - Render auto-detects render.yaml

4. **Set Environment Variables**:
   - Dashboard → Environment
   - Add OPENAI_API_KEY

#### Frontend Deployment

1. **Create separate service**:
   - Type: Static Site
   - Build Command: `cd my_visa_app/frontend_react && npm install && npm run build`
   - Publish Directory: `my_visa_app/frontend_react/build`

2. **Update API URL**:
```js
// In App.js
const API_URL = process.env.REACT_APP_API_URL || 'https://your-backend.onrender.com';
```

---

### 3. Railway

**Best for**: Hobby projects with database needs

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Login and Initialize**:
```bash
railway login
railway init
```

3. **Deploy Backend**:
```bash
railway up
```

4. **Add Environment Variables**:
```bash
railway variables set OPENAI_API_KEY=sk-your-key
```

5. **Get URL**:
```bash
railway open
```

---

### 4. Heroku

**Best for**: Established projects with scaling needs

1. **Create Heroku App**:
```bash
heroku create swiftvisa-api
```

2. **Add Procfile**:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

3. **Set Environment**:
```bash
heroku config:set OPENAI_API_KEY=sk-your-key
```

4. **Deploy**:
```bash
git push heroku main
```

5. **Scale**:
```bash
heroku ps:scale web=1
```

---

## ⚙️ Environment Configuration

### Production Environment Variables

Create `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-proj-xxxxx

# Optional
CHROMA_DB_DIR=vectorstore
TOP_K=5
HOST=0.0.0.0
PORT=8000
WORKERS=4
LOG_LEVEL=INFO

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# CORS
CORS_ALLOW_ORIGINS=["https://yourdomain.com"]
CORS_ALLOW_CREDENTIALS=true
```

### Platform-Specific Settings

**Render**:
```bash
# Auto-assigned
PORT=$PORT
```

**Railway**:
```bash
# Auto-assigned
RAILWAY_STATIC_URL=$RAILWAY_STATIC_URL
```

**Heroku**:
```bash
# Auto-assigned
PORT=$PORT
DATABASE_URL=$DATABASE_URL
```

---

## 🗄️ Database Setup

### PostgreSQL (Optional - for user data)

1. **Add to docker-compose.yml**:
```yaml
postgres:
  image: postgres:15
  environment:
    POSTGRES_DB: swiftvisa
    POSTGRES_USER: admin
    POSTGRES_PASSWORD: ${DB_PASSWORD}
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

2. **Connection String**:
```python
DATABASE_URL = "postgresql://admin:password@localhost:5432/swiftvisa"
```

---

## 🌐 Domain & SSL

### Custom Domain Setup

1. **Add Domain to Platform**:
   - Render: Settings → Custom Domains
   - Railway: Settings → Domains
   - Heroku: Settings → Domains

2. **Update DNS Records**:
```
Type: CNAME
Name: api (or @)
Value: your-app.platform.com
```

3. **SSL Certificate**:
   - Most platforms auto-provision SSL
   - Or use Let's Encrypt

### Nginx Configuration (Self-hosted)

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location / {
        proxy_pass http://frontend:3000;
    }
}
```

---

## 📊 Monitoring & Logging

### Application Logging

Add to `main.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
```

### Health Checks

Already implemented:
- GET `/` - Basic health
- GET `/stats` - System statistics

### Error Tracking

**Sentry Integration**:

```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# Linux/Mac
lsof -i :8000
kill -9 <pid>
```

#### 2. Module Not Found
```bash
pip install -r requirements.txt --force-reinstall
```

#### 3. Vectorstore Not Loading
```bash
python scripts/create_vectorstore.py
```

#### 4. CORS Errors
```python
# Update main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 5. OpenAI API Errors
- Check API key validity
- System automatically falls back to retrieval-only mode
- Check quota limits at platform.openai.com

### Debugging Commands

```bash
# Check backend logs
docker-compose logs backend

# Test backend directly
curl http://localhost:8000/

# Check vectorstore
python scripts/test_vectorstore.py

# Verify environment
python -c "import sys; print(sys.version)"
python -c "import langchain; print(langchain.__version__)"
```

---

## 📝 Pre-Deployment Checklist

- [ ] All environment variables set
- [ ] API keys secured (not in code)
- [ ] CORS configured for production domain
- [ ] Vectorstore populated with data
- [ ] Health checks passing
- [ ] Error handling tested
- [ ] Logging configured
- [ ] SSL certificate active
- [ ] Database migrations run (if using DB)
- [ ] Frontend API URL updated
- [ ] Rate limiting enabled (production)
- [ ] Documentation updated

---

## 🚀 Deployment Commands Summary

### Docker
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Render
```bash
git push origin main  # Auto-deploys
```

### Railway
```bash
railway up
railway logs
```

### Heroku
```bash
git push heroku main
heroku logs --tail
```

---

## 📞 Support

For deployment issues:
1. Check logs first
2. Review troubleshooting section
3. Check platform status pages
4. Open GitHub issue

---

**Last Updated**: November 23, 2025

# 🔑 How to Get Your Google Gemini API Key

## Quick Start (2 minutes)

### Step 1: Go to Google AI Studio
Visit: **https://makersuite.google.com/app/apikey**

### Step 2: Sign In
- Sign in with your Google account
- Accept terms of service if prompted

### Step 3: Create API Key
1. Click **"Create API Key"** button
2. Select a Google Cloud project (or create a new one)
3. Copy your API key (starts with: `AIza...`)

### Step 4: Add to Your Project
Open `.env` file and add:
```bash
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## ✅ Why Gemini?

### **FREE Tier Benefits:**
- ✅ **60 requests per minute** (free)
- ✅ **1500 requests per day** (free)
- ✅ **1 million tokens** per month (free)
- ✅ No credit card required
- ✅ Similar quality to GPT-3.5

### **Comparison with OpenAI:**

| Feature | Google Gemini | OpenAI GPT |
|---------|---------------|------------|
| Free Tier | ✅ Yes (generous) | ❌ No (pay per use) |
| Rate Limit | 60/min | 3/min (free trial) |
| Quality | Similar to GPT-3.5 | Excellent |
| Setup | Easy | Requires payment |
| Best For | Development, Testing | Production |

---

## 🚀 Testing Your API Key

### Test in Terminal:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-key-here"
python -c "from langchain_google_genai import ChatGoogleGenerativeAI; llm = ChatGoogleGenerativeAI(model='gemini-pro', google_api_key='your-key-here'); print(llm.invoke('Hello!'))"
```

### Test via API:
```bash
# Start backend with Gemini key
python -m uvicorn main:app --reload

# Check status
curl http://localhost:8000/stats
```

You should see:
```json
{
  "llm_provider": "gemini",
  "gemini_available": true
}
```

---

## 🔧 Using Both APIs

The system **automatically chooses** which API to use:

**Priority Order:**
1. **OpenAI** (if key is valid) → Uses GPT-3.5-turbo
2. **Gemini** (if key is valid) → Uses gemini-pro
3. **Retrieval-only** (if no keys) → Vector search only

### Configure Both:
```bash
# .env file
OPENAI_API_KEY=sk-proj-xxxxx  # Priority 1
GEMINI_API_KEY=AIzaSyXXXXX   # Priority 2 (fallback)
```

---

## 📊 Rate Limits

### Google Gemini (Free Tier):
```
Requests per minute (RPM): 60
Requests per day (RPD): 1500
Tokens per month: 1,000,000
```

### OpenAI GPT-3.5 (Paid):
```
Requests per minute: 3,500 (Tier 1)
Tokens per minute: 90,000
Cost: $0.50 / 1M input tokens
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Store API key in `.env` file (never commit)
- Use environment variables
- Rotate keys regularly
- Monitor usage at https://console.cloud.google.com

### ❌ DON'T:
- Commit `.env` to Git
- Share API keys publicly
- Use API keys in frontend code
- Expose keys in logs

---

## 🐛 Troubleshooting

### Error: "API key not valid"
**Solution:**
1. Check key format (should start with `AIza`)
2. Verify at https://makersuite.google.com/app/apikey
3. Ensure no extra spaces in `.env`

### Error: "Resource exhausted"
**Solution:** 
- You've hit rate limits
- Wait 60 seconds
- Or upgrade to paid tier

### Error: "Permission denied"
**Solution:**
1. Enable Generative Language API
2. Go to: https://console.cloud.google.com/apis/library
3. Search "Generative Language API"
4. Click "Enable"

---

## 🌐 API Documentation

- **Gemini API Docs**: https://ai.google.dev/docs
- **Pricing**: https://ai.google.dev/pricing
- **Models**: https://ai.google.dev/models/gemini
- **LangChain Integration**: https://python.langchain.com/docs/integrations/chat/google_generative_ai

---

## 💡 Quick Commands

```bash
# Get API key
Start-Process "https://makersuite.google.com/app/apikey"

# Set environment variable (PowerShell)
$env:GEMINI_API_KEY="your-key-here"

# Test connection
python -c "from langchain_google_genai import ChatGoogleGenerativeAI; print('✅ Gemini connected!')"

# Restart backend
python -m uvicorn main:app --reload
```

---

## 📞 Support

**Issues?**
- Check: https://ai.google.dev/docs/troubleshooting
- Forum: https://discuss.ai.google.dev/

**Project Issues?**
- Open GitHub issue
- Check `PROJECT_STATUS.md`

---

**Last Updated**: November 23, 2025

# 📚 SwiftVisa API Documentation

**Complete API reference for SwiftVisa Backend**

Version: 1.0.0  
Base URL: `http://localhost:8000` (development)

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
   - [Health & Status](#health--status)
   - [Visa Eligibility](#visa-eligibility)
   - [Country & Visa Information](#country--visa-information)
   - [Vector Store Queries](#vector-store-queries)
3. [Data Models](#data-models)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Examples](#examples)

---

## 🔐 Authentication

Currently, the API does not require authentication for public endpoints. Future versions may implement:
- API Key authentication for production use
- OAuth 2.0 for user-specific features
- Rate limiting per API key

---

## 🔗 Endpoints

### Health & Status

#### GET `/`
Basic health check endpoint

**Response:**
```json
{
  "message": "✅ SwiftVisa Backend Running Perfectly!"
}
```

#### GET `/health`
Detailed health check with system status

**Response:**
```json
{
  "status": "healthy",
  "service": "SwiftVisa Backend",
  "timestamp": "2025-11-29T10:30:00",
  "vectorstore_loaded": true,
  "llm_available": true,
  "llm_provider": "openai"
}
```

#### GET `/stats`
Comprehensive system statistics

**Response:**
```json
{
  "status": "operational",
  "timestamp": "2025-11-29T10:30:00",
  "documents_loaded": 46,
  "countries_available": 4,
  "countries": ["Canada", "Germany", "UK", "US"],
  "visa_types_count": 35,
  "vectorstore_size_mb": 25.4,
  "embedding_model": "all-MiniLM-L6-v2",
  "llm_enabled": true,
  "llm_provider": "openai",
  "openai_available": true,
  "gemini_available": false,
  "top_k_retrieval": 5,
  "api_version": "1.0.0"
}
```

---

### Visa Eligibility

#### POST `/check-eligibility`
Check visa eligibility based on user profile

**Request Body:**
```json
{
  "countryOfCitizenship": "India",
  "destinationCountry": "Canada",
  "purposeOfVisit": "Study",
  "lengthOfStay": "365",
  "age": "25"
}
```

**Response:**
```json
{
  "eligibility": "Detailed eligibility assessment...",
  "provider": "openai",
  "timestamp": "2025-11-29T10:30:00"
}
```

**Purpose of Visit Options:**
- `Tourism`
- `Business`
- `Study`
- `Work`
- `Family Reunion`
- `Medical Treatment`

#### POST `/analyze-profile`
Advanced profile analysis with structured output

**Request Body:** Same as `/check-eligibility`

**Response:**
```json
{
  "status": "success",
  "analysis": "Comprehensive eligibility analysis...",
  "provider": "openai",
  "profile": {
    "countryOfCitizenship": "India",
    "destinationCountry": "Canada",
    "purposeOfVisit": "Study",
    "lengthOfStay": "365",
    "age": "25"
  },
  "timestamp": "2025-11-29T10:30:00"
}
```

---

### Country & Visa Information

#### GET `/countries`
Get list of countries with visa data available

**Response:**
```json
{
  "countries": ["Canada", "Germany", "UK", "US"],
  "count": 4
}
```

#### GET `/visa-types/{country}`
Get available visa types for a specific country

**Parameters:**
- `country` (path): Country name (e.g., "Canada")

**Example:** `GET /visa-types/Canada`

**Response:**
```json
{
  "country": "Canada",
  "visa_types": [
    "CaregiverProgram",
    "CoopPermit",
    "ExpressEntry",
    "PGWP",
    "PNP",
    "StudyPermit",
    "SuperVisa",
    "VisitorVisa",
    "WorkPermit"
  ],
  "count": 9
}
```

#### GET `/visa-requirements/{destination}/{visa_type}`
Get specific visa requirements

**Parameters:**
- `destination` (path): Destination country
- `visa_type` (path): Visa type name

**Example:** `GET /visa-requirements/Canada/StudyPermit`

**Response:**
```json
{
  "status": "success",
  "destination": "Canada",
  "visa_type": "StudyPermit",
  "requirements": [
    {
      "content": "Eligibility requirements for study permit...",
      "metadata": {}
    }
  ],
  "total_documents": 3
}
```

---

### Vector Store Queries

#### POST `/vectorstore/query`
Direct query to the vector database

**Request Body:**
```json
{
  "query": "What are student visa requirements for Canada?",
  "k": 5
}
```

**Response:**
```json
{
  "query": "What are student visa requirements for Canada?",
  "k": 5,
  "results_count": 5,
  "results": [
    {
      "rank": 1,
      "content": "Study permit eligibility requirements...",
      "metadata": {},
      "full_length": 1250
    }
  ],
  "timestamp": "2025-11-29T10:30:00"
}
```

---

## 📊 Data Models

### VisaRequest
```python
{
  "countryOfCitizenship": str,    # Required
  "destinationCountry": str,      # Required
  "purposeOfVisit": str,          # Required
  "lengthOfStay": str,            # Required (in days)
  "age": str                      # Required
}
```

### VectorStoreQuery
```python
{
  "query": str,                   # Required
  "k": int                        # Optional (default: 5)
}
```

---

## ⚠️ Error Handling

### Error Response Format
```json
{
  "detail": "Error message description",
  "status_code": 400
}
```

### Common Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 422 | Validation Error | Request validation failed |
| 500 | Internal Server Error | Server-side error |

### Validation Errors
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 🚦 Rate Limiting

**Current Status:** Not implemented (development)

**Future Implementation:**
- 100 requests per minute per IP
- 1000 requests per hour per API key
- Burst allowance: 20 requests

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1638360000
```

---

## 💡 Examples

### Example 1: Check Study Visa Eligibility

**cURL:**
```bash
curl -X POST "http://localhost:8000/check-eligibility" \
  -H "Content-Type: application/json" \
  -d '{
    "countryOfCitizenship": "India",
    "destinationCountry": "Canada",
    "purposeOfVisit": "Study",
    "lengthOfStay": "365",
    "age": "25"
  }'
```

**Python:**
```python
import requests

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

print(response.json())
```

**JavaScript:**
```javascript
const data = {
  countryOfCitizenship: "India",
  destinationCountry: "Canada",
  purposeOfVisit: "Study",
  lengthOfStay: "365",
  age: "25"
};

fetch("http://localhost:8000/check-eligibility", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(data)
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Example 2: Query Vectorstore

**Python:**
```python
import requests

query_data = {
    "query": "tourist visa requirements for Germany",
    "k": 3
}

response = requests.post(
    "http://localhost:8000/vectorstore/query",
    json=query_data
)

results = response.json()
for result in results["results"]:
    print(f"Rank {result['rank']}: {result['content'][:200]}...")
```

### Example 3: Get Country Information

**Python:**
```python
import requests

# Get all countries
countries = requests.get("http://localhost:8000/countries").json()
print("Available countries:", countries["countries"])

# Get visa types for Canada
visa_types = requests.get("http://localhost:8000/visa-types/Canada").json()
print("Canada visa types:", visa_types["visa_types"])
```

---

## 🔧 Testing

### Interactive API Documentation

Visit these URLs while the server is running:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Both provide interactive documentation where you can test endpoints directly.

---

## 📞 Support

For API issues or questions:
- Check the [DEPLOYMENT.md](DEPLOYMENT.md) guide
- Review error logs in `logs/swiftvisa.log`
- Verify backend is running: `curl http://localhost:8000/health`

---

**Last Updated**: November 29, 2025  
**API Version**: 1.0.0  
**Documentation Version**: 1.0.0

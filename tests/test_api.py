"""
API Endpoint Tests
Tests for all FastAPI endpoints in main.py
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoints:
    """Test health check and status endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns success message"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "SwiftVisa" in response.json()["message"]
    
    def test_health_endpoint(self):
        """Test detailed health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "timestamp" in data
        assert "vectorstore_loaded" in data
    
    def test_stats_endpoint(self):
        """Test statistics endpoint"""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "operational"
        assert "documents_loaded" in data
        assert "countries_available" in data
        assert "embedding_model" in data
        assert data["api_version"] == "1.0.0"


class TestCountryEndpoints:
    """Test country and visa type endpoints"""
    
    def test_get_countries(self):
        """Test getting list of available countries"""
        response = client.get("/countries")
        assert response.status_code == 200
        data = response.json()
        assert "countries" in data
        assert "count" in data
        assert isinstance(data["countries"], list)
    
    def test_get_visa_types(self):
        """Test getting visa types for a country"""
        response = client.get("/visa-types/Canada")
        assert response.status_code == 200
        data = response.json()
        assert "country" in data
        assert "visa_types" in data
        assert data["country"] == "Canada"
        assert isinstance(data["visa_types"], list)


class TestEligibilityEndpoint:
    """Test visa eligibility checking endpoint"""
    
    def test_check_eligibility_success(self, sample_visa_request):
        """Test successful eligibility check"""
        response = client.post("/check-eligibility", json=sample_visa_request)
        assert response.status_code == 200
        data = response.json()
        assert "eligibility" in data
        assert "provider" in data
        assert isinstance(data["eligibility"], str)
    
    def test_check_eligibility_missing_field(self):
        """Test eligibility check with missing required field"""
        incomplete_data = {
            "countryOfCitizenship": "India",
            "destinationCountry": "Canada"
            # Missing other required fields
        }
        response = client.post("/check-eligibility", json=incomplete_data)
        assert response.status_code == 422  # Validation error
    
    def test_check_eligibility_invalid_data(self):
        """Test eligibility check with invalid data types"""
        invalid_data = {
            "countryOfCitizenship": "India",
            "destinationCountry": "Canada",
            "purposeOfVisit": "Study",
            "lengthOfStay": "not-a-number",  # Should be string but parseable
            "age": "invalid"
        }
        response = client.post("/check-eligibility", json=invalid_data)
        # Should still process or return proper error
        assert response.status_code in [200, 422]


class TestVectorStoreEndpoints:
    """Test vector store query endpoints"""
    
    def test_vectorstore_query(self):
        """Test direct vectorstore query"""
        query_data = {
            "query": "student visa requirements for Canada",
            "k": 3
        }
        response = client.post("/vectorstore/query", json=query_data)
        assert response.status_code == 200
        data = response.json()
        assert "query" in data
        assert "results" in data
        assert "results_count" in data
    
    def test_vectorstore_query_empty(self):
        """Test vectorstore query with empty query"""
        query_data = {
            "query": "",
            "k": 3
        }
        response = client.post("/vectorstore/query", json=query_data)
        # Should return error or empty results
        assert response.status_code in [200, 400]


class TestAnalyzeProfileEndpoint:
    """Test advanced profile analysis endpoint"""
    
    def test_analyze_profile(self, sample_visa_request):
        """Test profile analysis endpoint"""
        response = client.post("/analyze-profile", json=sample_visa_request)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "analysis" in data
        assert "provider" in data
        assert "profile" in data
        assert "timestamp" in data


class TestVisaRequirementsEndpoint:
    """Test visa requirements lookup endpoint"""
    
    def test_get_visa_requirements(self):
        """Test getting specific visa requirements"""
        response = client.get("/visa-requirements/Canada/StudyPermit")
        assert response.status_code == 200
        data = response.json()
        assert "destination" in data
        assert "visa_type" in data
        assert data["destination"] == "Canada"
        assert data["visa_type"] == "StudyPermit"
    
    def test_get_visa_requirements_not_found(self):
        """Test getting requirements for non-existent visa type"""
        response = client.get("/visa-requirements/FakeCountry/FakeVisa")
        assert response.status_code == 200
        data = response.json()
        # Should return not_found status or empty results
        assert "status" in data


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])

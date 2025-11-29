"""
Pytest Configuration and Fixtures
Shared test fixtures for SwiftVisa tests
"""

import pytest
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(scope="session")
def test_env():
    """Set up test environment variables"""
    os.environ["TESTING"] = "true"
    os.environ["CHROMA_DB_DIR"] = "vectorstore"
    os.environ["TOP_K"] = "3"
    yield
    os.environ.pop("TESTING", None)


@pytest.fixture(scope="module")
def sample_visa_request():
    """Sample visa request data for testing"""
    return {
        "countryOfCitizenship": "India",
        "destinationCountry": "Canada",
        "purposeOfVisit": "Study",
        "lengthOfStay": "365",
        "age": "25"
    }


@pytest.fixture(scope="module")
def sample_query():
    """Sample query for vectorstore testing"""
    return "What are the requirements for a student visa to Canada?"


@pytest.fixture(scope="function")
def mock_llm_response():
    """Mock LLM response for testing"""
    return """
    Based on the provided information, here is the eligibility assessment:
    
    **Eligibility Status**: Likely Eligible
    
    **Key Requirements**:
    1. Valid acceptance letter from a designated learning institution
    2. Proof of sufficient funds
    3. Clean criminal record
    4. Medical examination
    
    **Recommendations**:
    - Prepare all required documents in advance
    - Apply at least 3 months before intended start date
    - Consider study permit extensions if needed
    
    **Next Steps**:
    1. Gather required documents
    2. Complete online application
    3. Pay application fees
    4. Attend biometrics appointment if required
    """

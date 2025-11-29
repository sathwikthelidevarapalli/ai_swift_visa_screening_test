# SwiftVisa Test Suite

This directory contains all tests for the SwiftVisa application.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Pytest fixtures and configuration
├── test_api.py              # API endpoint tests
├── test_vectorstore.py      # Vector database tests
├── test_rag_pipeline.py     # RAG pipeline tests
├── test_integration.py      # End-to-end integration tests
└── test_config.py           # Configuration tests
```

## Running Tests

### Install Test Dependencies

```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_api.py
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test

```bash
pytest tests/test_api.py::test_health_check
```

## Test Categories

### Unit Tests
- Individual function testing
- Isolated component testing
- Mock external dependencies

### Integration Tests
- API endpoint testing
- Database operations
- LLM integration

### End-to-End Tests
- Full workflow testing
- User journey simulation
- System integration

## Writing Tests

### Example Test Structure

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_endpoint(client):
    response = client.get("/endpoint")
    assert response.status_code == 200
```

## Test Coverage Goals

- **API Endpoints**: 100%
- **Core Functions**: 90%+
- **Integration Flows**: 80%+
- **Overall**: 85%+

## Continuous Integration

Tests are automatically run on:
- Pull requests
- Commits to main branch
- Release builds

## Test Data

Test data is stored in:
- `tests/fixtures/` - Sample documents
- `tests/mock_data/` - Mock API responses
- `tests/test_data/` - Test input data

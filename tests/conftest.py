import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    """Test client for FastAPI app"""
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities database before each test"""
    from src.app import activities
    
    # Store original data
    original_activities = activities.copy()
    
    # Reset to original state after test
    yield
    
    # Restore original activities
    activities.clear()
    activities.update(original_activities)
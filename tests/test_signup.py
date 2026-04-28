import pytest
from fastapi.testclient import TestClient
from fastapi import status

def test_successful_signup(client: TestClient):
    """Test successful signup for an activity"""
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    
    assert response.status_code == status.HTTP_200_OK
    
    result = response.json()
    assert "Signed up test@example.com for Chess Club" in result["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "test@example.com" in activities["Chess Club"]["participants"]

def test_duplicate_signup(client: TestClient):
    """Test that signing up twice returns an error"""
    # First signup
    client.post("/activities/Chess%20Club/signup?email=test@example.com")
    
    # Second signup should fail
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    result = response.json()
    assert "Student already signed up" in result["detail"]

def test_signup_nonexistent_activity(client: TestClient):
    """Test signup for non-existent activity returns 404"""
    response = client.post("/activities/NonExistent/signup?email=test@example.com")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_successful_unregistration(client: TestClient):
    """Test successful unregistration from an activity"""
    # First sign up
    client.post("/activities/Chess%20Club/signup?email=test@example.com")
    
    # Then unregister
    response = client.delete("/activities/Chess%20Club/signup?email=test@example.com")
    
    assert response.status_code == status.HTTP_200_OK
    
    result = response.json()
    assert "Unregistered test@example.com from Chess Club" in result["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "test@example.com" not in activities["Chess Club"]["participants"]

def test_unregister_not_registered(client: TestClient):
    """Test unregistering a student who is not registered"""
    response = client.delete("/activities/Chess%20Club/signup?email=notregistered@example.com")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    result = response.json()
    assert "Student is not registered" in result["detail"]

def test_unregister_nonexistent_activity(client: TestClient):
    """Test unregistering from non-existent activity returns 404"""
    response = client.delete("/activities/NonExistent/signup?email=test@example.com")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    result = response.json()
    assert "Activity not found" in result["detail"]
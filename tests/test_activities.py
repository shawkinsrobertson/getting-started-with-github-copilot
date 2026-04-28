from fastapi.testclient import TestClient
from fastapi import status

def test_get_activities(client: TestClient):
    """Test getting all activities returns correct structure"""
    response = client.get("/activities")
    
    assert response.status_code == status.HTTP_200_OK
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Check structure of first activity
    first_activity = next(iter(activities.values()))
    required_keys = ["description", "schedule", "max_participants", "participants"]
    
    for key in required_keys:
        assert key in first_activity
    
    assert isinstance(first_activity["participants"], list)
    assert isinstance(first_activity["max_participants"], int)
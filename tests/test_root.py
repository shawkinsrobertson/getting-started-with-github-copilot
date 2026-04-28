from fastapi.testclient import TestClient
from fastapi import status

def test_root_redirect(client: TestClient):
    """Test that root endpoint redirects to static HTML"""
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "/static/index.html"
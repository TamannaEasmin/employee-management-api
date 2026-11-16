from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 404

def test_create_employee():
    response = client.post(
        "/employees",
        json={
            "full_name": "Test User",
            "email": "testuser@example.com",
            "designation": "Tester",
            "salary": 50000
        }
    )
    assert response.status_code in [200, 400]  # 400 if email already exists

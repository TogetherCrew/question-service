from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_route():
    response = client.post("/test", json={"text": "Is this a test?"})
    assert response.status_code == 200
    assert response.json()["label"] == "QUESTION"

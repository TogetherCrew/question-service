from fastapi.testclient import TestClient
from main import app


def test_route():

    with TestClient(app) as client:
        response = client.post("/test", json={"text": "Is this a test?"})
        assert response.status_code == 200
        assert response.json()["label"] == "QUESTION"

from fastapi import status
from fastapi.testclient import TestClient

from parma_mining.producthunt.api.main import app

client = TestClient(app)


def test_root_success():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"welcome": "at parma-mining-producthunt"}


def test_root_method_not_allowed():
    response = client.post("/")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

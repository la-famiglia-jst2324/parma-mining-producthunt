from unittest.mock import MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from parma_mining.mining_common.exceptions import ClientInvalidBodyError
from parma_mining.producthunt.api.dependencies.auth import authenticate
from parma_mining.producthunt.api.main import app
from parma_mining.producthunt.model import (
    DiscoveryRequest,
)
from tests.dependencies.mock_auth import mock_authenticate


@pytest.fixture
def client():
    assert app
    app.dependency_overrides.update(
        {
            authenticate: mock_authenticate,
        }
    )
    return TestClient(app)


@pytest.fixture
def mock_producthunt_client(mocker) -> MagicMock:
    """Mocking ProductHuntClient's search_organizations method."""
    mock = mocker.patch(
        "parma_mining.producthunt.api.main.ProductHuntClient.search_organizations"
    )
    mock.return_value = {"producthunt_url": ["https://example.com"]}
    return mock


def test_discover_endpoint_success(
    client: TestClient, mock_producthunt_client: MagicMock
):
    """Test for successful discovery."""
    request_data = [
        DiscoveryRequest(company_id="123", name="TestCompany").model_dump(),
        DiscoveryRequest(company_id="456", name="AnotherCompany").model_dump(),
    ]

    response = client.post("/discover", json=request_data)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)
    assert "identifiers" in response.json()
    assert "validity" in response.json()

    assert mock_producthunt_client.called


def test_discover_endpoint_empty_request(client: TestClient):
    """Test for an empty request body."""
    with pytest.raises(ClientInvalidBodyError) as exc_info:
        client.post("/discover", json=[])
    assert "Request body cannot be empty for discovery" in str(exc_info.value)


def test_discover_endpoint_invalid_format(client: TestClient):
    """Test for an invalid request format."""
    invalid_request_data = {"invalid": "data"}

    response = client.post("/discover", json=invalid_request_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_discover_non_existing_company(
    client: TestClient, mock_producthunt_client: MagicMock
):
    """Test for discovering a non-existing company."""
    mock_producthunt_client.return_value = {}

    request_data = [
        DiscoveryRequest(company_id="999", name="NonExistingCompany").dict()
    ]
    response = client.post("/discover", json=request_data)

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data


def test_discover_endpoint_with_producthunt_client_error(
    client: TestClient, mock_producthunt_client: MagicMock
):
    """Test for an error in ProductHuntClient."""
    mock_producthunt_client.side_effect = Exception("Mocked Exception")
    request_data = [DiscoveryRequest(company_id="123", name="TestCompany").model_dump()]

    with pytest.raises(Exception) as exc_info:
        client.post("/discover", json=request_data)
    assert "Mocked Exception" in str(exc_info.value)

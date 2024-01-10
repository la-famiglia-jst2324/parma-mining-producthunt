from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from starlette import status

from parma_mining.producthunt.api.main import app

client = TestClient(app)


@pytest.fixture
def mock_producthunt_client(mocker) -> MagicMock:
    """Mocking ProductHuntScraper's method to avoid actual API calls during testing."""
    mock = mocker.patch(
        "parma_mining.producthunt.scraper.ProductHuntScraper.query_company_top_products"
    )
    mock.return_value = [
        {"name": "Product1", "url": "https://www.producthunt.com/products/product1"},
        {"name": "Product2", "url": "https://www.producthunt.com/products/product2"},
    ]
    return mock


def test_get_company_products(mock_producthunt_client: MagicMock):
    company_name = "TestCompany"
    response = client.get(f"/discover?query={company_name}")

    length = 2

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == length
    assert response.json()[0]["name"] == "Product1"
    assert "url" in response.json()[0]

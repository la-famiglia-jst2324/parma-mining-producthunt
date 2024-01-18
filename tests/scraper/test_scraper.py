from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from parma_mining.producthunt.api.main import app
from parma_mining.producthunt.model import ProductInfo
from parma_mining.producthunt.ph_client import ProductHuntClient


@pytest.fixture
def client():
    return TestClient(app)


def mock_response(content):
    response = MagicMock()
    response.content = content.encode("utf-8")
    return response


def test_scrape_product_page_failure():
    with patch("httpx.Client.get", side_effect=Exception("Mocked Exception")):
        scraper = ProductHuntClient()
        result = scraper.scrape_product_page(
            "https://www.producthunt.com/products/testproduct"
        )

    assert isinstance(result, ProductInfo)
    assert result.name is None
    assert result.overall_rating is None
    assert result.followers == 0
    assert len(result.reviews) == 0

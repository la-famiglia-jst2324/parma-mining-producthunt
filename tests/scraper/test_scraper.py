from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from parma_mining.producthunt.api.main import app
from parma_mining.producthunt.model import ProductInfo
from parma_mining.producthunt.scraper import ProductHuntScraper


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_httpx_get(mocker):
    mock = mocker.patch("httpx.Client.get")
    return mock


def test_scrape_product_page_success(mock_httpx_get):
    # Mock the HTTP response with provided HTML snippets
    mock_product_page_response = MagicMock()
    mock_product_page_response.content = (
        b"<h1 class='color-darker-grey'>Mock Product Name</h1>"
        b"<div class='styles_reviewPositive__JY_9N'>4.5/5</div>"
        b"<div class='styles_count___6_8F'>"
        b"1.2K followers</div>"
    )

    mock_review_page_response = MagicMock()
    mock_review_page_response.content = (
        b"<div class='flex direction-column' id="
        b"'review-123'><div class='styles_html"
        b"Text__iftLe'>Great product, really "
        b"useful!</div><time datetime='2023-01-01"
        b"T12:00:00'></time></div><div class="
        b"'flex direction-column' id='review-456'>"
        b"<div class='styles_htmlText__iftLe'>"
        b"I love this tool, it has simplified my "
        b"workflow.</div><time datetime="
        b"'2023-01-02T15:30:00'></time></div>"
    )

    mock_httpx_get.side_effect = [mock_product_page_response, mock_review_page_response]

    scraper = ProductHuntScraper()
    result = scraper.scrape_product_page(
        "https://www.producthunt.com/products/testproduct"
    )
    rating = 4.5
    follower_count = 1200
    num_reviews = 2

    assert isinstance(result, ProductInfo)
    assert result.name == "Mock Product Name"
    assert result.overall_rating == rating
    assert result.followers == follower_count
    assert len(result.reviews) == num_reviews
    assert result.reviews[0]["text"] == "Great product, really useful!"
    assert (
        result.reviews[1]["text"] == "I love this tool, it has simplified my workflow."
    )


def test_scrape_product_page_failure(mock_httpx_get):
    # Simulate an HTTP request failure
    mock_httpx_get.side_effect = Exception("Mocked Exception")

    scraper = ProductHuntScraper()
    result = scraper.scrape_product_page(
        "https://www.producthunt.com/products/testproduct"
    )

    assert isinstance(result, ProductInfo)
    assert result.name is None
    assert result.overall_rating is None
    assert result.followers == 0
    assert len(result.reviews) == 0

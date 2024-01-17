import json

import pytest

from parma_mining.producthunt.model import ProductInfo, Review


@pytest.fixture
def product_data():
    return {
        "name": "Mock Product",
        "overall_rating": 4.5,
        "review_count": 100,
        "followers": 1000,
        "reviews": [
            {"text": "Great product!", "date": "2023-01-01T12:00:00"},
            {"text": "Really useful tool.", "date": "2023-01-02T15:30:00"},
        ],
    }


def test_updated_model_dump(product_data):
    # Convert the 'reviews' in product_data to instances of Review
    product_data["reviews"] = [
        Review(**review_data) for review_data in product_data["reviews"]
    ]

    product_info = ProductInfo(**product_data)

    dumped_json = product_info.updated_model_dump()
    dumped_dict = json.loads(dumped_json)

    assert dumped_dict["name"] == product_data["name"]
    assert dumped_dict["overall_rating"] == product_data["overall_rating"]
    assert dumped_dict["review_count"] == product_data["review_count"]
    assert dumped_dict["followers"] == product_data["followers"]

    for i, review in enumerate(dumped_dict["reviews"]):
        assert review["text"] == product_data["reviews"][i].text
        assert review["date"] == product_data["reviews"][i].date

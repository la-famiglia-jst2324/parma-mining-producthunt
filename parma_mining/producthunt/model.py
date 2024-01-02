"""Model for the ProductHunt data."""

from pydantic import BaseModel


class CompaniesRequest(BaseModel):
    """Request model."""

    companies: dict[str, dict[str, list[str]]]


class DiscoveryModel(BaseModel):
    """Discovery model for ProductHunt data."""

    name: str | None
    url: str | None


class Review(BaseModel):
    """Review model."""

    text: str | None
    date: str | None


class ProductInfo(BaseModel):
    """Product model with data scraped from ProductHunt."""

    name: str | None
    overall_rating: float | None
    review_count: int
    followers: int
    reviews: list[Review]


class ResponseModel(BaseModel):
    """Response model for ProductHunt data."""

    source_name: str
    company_id: str
    raw_data: ProductInfo

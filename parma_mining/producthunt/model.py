"""Model for the ProductHunt data."""
from datetime import datetime

from pydantic import BaseModel


class CompaniesRequest(BaseModel):
    """Request model."""

    companies: dict[str, dict[str, list[str]]]


class DiscoveryRequest(BaseModel):
    """Discovery request."""

    company_id: str
    name: str


class DiscoveryModel(BaseModel):
    """Model for discovery."""

    name: str
    url: str


class DiscoveryResponse(BaseModel):
    """Discovery response model."""

    identifiers: dict[str, list[DiscoveryModel]]
    validity: datetime


class Review(BaseModel):
    """Review model."""

    text: str | None
    date: str | None


class ProductInfo(BaseModel):
    """Product model with data scraped from ProductHunt."""

    name: str | None
    overall_rating: float | None
    review_count: int | None
    followers: int | None
    reviews: list[Review]


class ResponseModel(BaseModel):
    """Response model for ProductHunt data."""

    source_name: str
    company_id: str
    raw_data: ProductInfo


class ErrorInfoModel(BaseModel):
    """Error info for the crawling_finished endpoint."""

    error_type: str
    error_description: str | None


class CrawlingFinishedInputModel(BaseModel):
    """Internal base model for the crawling_finished endpoints."""

    task_id: int
    errors: dict[str, ErrorInfoModel] | None = None

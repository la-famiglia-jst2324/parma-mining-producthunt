"""Model for the ProductHunt data."""

from pydantic import BaseModel


class CompaniesRequest(BaseModel):
    """Request model."""

    companies: dict[str, dict[str, list[str]]]


class ResponseModel(BaseModel):
    """Response model for ProductHunt data."""

    source_name: str
    company_id: str
    raw_data: dict


class DiscoveryModel(BaseModel):
    """Discovery model for ProductHunt data."""

    name: str | None
    url: str | None

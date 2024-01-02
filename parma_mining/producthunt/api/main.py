"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import FastAPI, status

from parma_mining.producthunt.model import (
    CompaniesRequest,
    DiscoveryModel,
    ResponseModel,
)
from parma_mining.producthunt.scraper import ProductHuntScraper

app = FastAPI()

producthunt_scraper = ProductHuntScraper()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-producthunt"}


@app.post(
    "/companies",
    status_code=status.HTTP_200_OK,
)
def get_company_details(companies: CompaniesRequest):
    """Endpoint to get product data based on a dict with the respective urls."""
    for company_id, company_data in companies.companies.items():
        for data_type, handles in company_data.items():
            for handle in handles:
                if data_type == "url":
                    scraped_data = producthunt_scraper.scrape_product_page(handle)
                    response_data = ResponseModel(
                        source_name="producthunt",
                        company_id=company_id,
                        raw_data=scraped_data,
                    )
                    return response_data


@app.get(
    "/discover",
    response_model=list[DiscoveryModel],
    status_code=status.HTTP_200_OK,
)
def discover_products(query: str):
    """Discovery endpoint that returns the top products matching the query."""
    companies = producthunt_scraper.query_company_top_products(query)
    return companies

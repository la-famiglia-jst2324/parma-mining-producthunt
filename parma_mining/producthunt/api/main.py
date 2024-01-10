"""Main entrypoint for the API routes in of parma-analytics."""
import json
import logging

from fastapi import FastAPI, status

from parma_mining.producthunt.analytics_client import AnalyticsClient
from parma_mining.producthunt.model import (
    CompaniesRequest,
    DiscoveryModel,
    ResponseModel,
)
from parma_mining.producthunt.normalization_map import ProductHuntNormalizationMap
from parma_mining.producthunt.scraper import ProductHuntScraper

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()

producthunt_scraper = ProductHuntScraper()
normalization = ProductHuntNormalizationMap()
analytics_client = AnalyticsClient()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    logger.debug("Root endpoint called")
    return {"welcome": "at parma-mining-producthunt"}


@app.get("/initialize", status_code=status.HTTP_200_OK)
def initialize(source_id: int) -> str:
    """Initialization endpoint for the API."""
    # init frequency
    time = "weekly"
    normalization_map = normalization.get_normalization_map()
    # register the measurements to analytics
    analytics_client.register_measurements(
        normalization_map, source_module_id=source_id
    )

    # set and return results
    results = {}
    results["frequency"] = time
    results["normalization_map"] = str(normalization_map)
    return json.dumps(results)


@app.post(
    "/companies",
    status_code=status.HTTP_200_OK,
)
def get_company_details(companies: CompaniesRequest):
    """Endpoint to get product data based on a dict with the respective urls."""
    logger.debug("Companies endpoint called")
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
                    # Write data to db via endpoint in analytics backend
                    try:
                        analytics_client.feed_raw_data(response_data)
                    except Exception:
                        print("Error writing to db")
                else:
                    # To be included in logging
                    print("Unsupported type error")
                return "done"


@app.get(
    "/discover",
    response_model=list[DiscoveryModel],
    status_code=status.HTTP_200_OK,
)
def discover_products(query: str):
    """Discovery endpoint that returns the top products matching the query."""
    logger.debug("Discovery endpoint called")
    companies = producthunt_scraper.query_company_top_products(query)
    return companies

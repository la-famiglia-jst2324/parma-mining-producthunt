"""Product Hunt client module."""
import logging
import re
from datetime import datetime

import httpx
from bs4 import BeautifulSoup

from parma_mining.producthunt.model import ProductInfo


def _extract_product_name(soup: BeautifulSoup) -> str | None:
    product_name_div = soup.find("h1", class_="color-darker-grey")
    return product_name_div.get_text(strip=True) if product_name_div else None


def _extract_overall_rating(soup: BeautifulSoup) -> float | None:
    overall_rating_div = soup.find("div", class_="styles_reviewPositive__JY_9N")
    rating = (
        overall_rating_div.get_text(strip=True).split("/")[0]
        if overall_rating_div
        else None
    )
    return float(rating)


def _extract_reviews(soup: BeautifulSoup) -> list:
    reviews = []
    for review_div in soup.find_all(
        "div",
        class_="flex direction-column",
        id=lambda x: x and x.startswith("review-"),
    ):
        review_text_div = review_div.find("div", class_="styles_htmlText__iftLe")
        review_text = review_text_div.get_text(strip=True) if review_text_div else None
        time_tag = review_div.find("time")
        review_date = (
            datetime.fromisoformat(time_tag["datetime"]).strftime("%Y-%m-%d %H:%M:%S")
            if time_tag
            else None
        )
        reviews.append({"text": review_text, "date": review_date})
    return reviews


def _extract_followers(soup: BeautifulSoup) -> int:
    followers_div = soup.find("div", class_="styles_count___6_8F")
    if followers_div:
        followers_text = followers_div.get_text(strip=True)
        followers_match = re.search(r"(\d+(?:\.\d+)?)\s?[Kk]?", followers_text)
        if followers_match:
            followers_str = followers_match.group(1)
            followers_count = float(followers_str)

            if "K" in followers_text or "k" in followers_text:
                followers_count *= 1000  # Convert thousands to actual number

            return int(followers_count)

    return 0


class ProductHuntScraper:
    """ProductHuntScraper class is used to fetch data from Product Hunt."""

    def __init__(self):
        """Initialize the Product Hunt client."""
        self.base_url = "https://www.producthunt.com/"
        self.logger = logging.getLogger(__name__)

    def search_organizations(self, company_name: str) -> list:
        """Get links of products by company name."""
        search_url = self.base_url + "search"
        params = {"q": company_name}

        try:
            with httpx.Client() as client:
                response = client.get(search_url, params=params)

            soup = BeautifulSoup(response.content, "html.parser")

            products = []
            product_cut_off = 1
            product_name_divs = soup.find_all("div", {"data-test": "product-item-name"})

            for div in product_name_divs:
                product_name = div.get_text(strip=True)
                product_link = div.find_previous("a", href=True)

                if product_link and product_link["href"].startswith("/products/"):
                    full_url = self.base_url.rstrip("/") + product_link["href"]
                    products.append({"name": product_name, "url": full_url})

                    if len(products) >= product_cut_off:
                        break

            return products
        except Exception as e:
            self.logger.error(f"Failed to query company products: {e}")
            return []

    def _get_html_content(self, url: str) -> str:
        with httpx.Client() as client:
            response = client.get(url)
        return response.content

    def scrape_product_page(self, url: str) -> ProductInfo:
        """Get Product data with link of product page."""
        try:
            product_page_content = self._get_html_content(url)
            review_page_content = self._get_html_content(url + "/reviews?order=LATEST")

            soup = BeautifulSoup(product_page_content, "html.parser")
            review_soup = BeautifulSoup(review_page_content, "html.parser")

            self.logger.debug(f"Retrieving data from: {url}")

            product_info_data = {
                "name": _extract_product_name(soup),
                "overall_rating": _extract_overall_rating(review_soup),
                "review_count": len(_extract_reviews(review_soup)),
                "followers": _extract_followers(soup),
                "reviews": _extract_reviews(review_soup),
            }
            return ProductInfo(**product_info_data)
        except Exception as e:
            self.logger.error(f"Failed to scrape product page: {e}")
            return ProductInfo()

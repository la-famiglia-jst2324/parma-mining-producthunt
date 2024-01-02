"""Product Hunt client module."""
import re
from datetime import datetime

import httpx
from bs4 import BeautifulSoup


class ProductHuntScraper:
    """ProductHuntScraper class is used to fetch data from Product Hunt."""

    def __init__(self):
        """Initialize the Product Hunt client."""
        self.base_url = "https://www.producthunt.com/"

    def query_company_top_products(self, company_name: str) -> list:
        """Get links of products by company name."""
        search_url = "https://www.producthunt.com/search"
        params = {"q": company_name}

        with httpx.Client() as client:
            response = client.get(search_url, params=params)

        soup = BeautifulSoup(response.content, "html.parser")

        products = []
        product_cut_off = 5
        # Find all product name divs
        product_name_divs = soup.find_all("div", {"data-test": "product-item-name"})

        for div in product_name_divs:
            # Extract product name
            product_name = div.get_text(strip=True)

            # Attempt to find the corresponding 'a' tag with product URL
            product_link = div.find_previous("a", href=True)
            if product_link and product_link["href"].startswith("/products/"):
                full_url = "https://www.producthunt.com" + product_link["href"]
                products.append({"name": product_name, "url": full_url})

                if len(products) >= product_cut_off:
                    break

        return products

    def scrape_product_page(self, url):
        """Scrape product data based on the given url."""
        with httpx.Client() as client:
            response = client.get(url)
            review_page_response = client.get(url + "/reviews?order=LATEST")

        soup = BeautifulSoup(response.content, "html.parser")
        review_soup = BeautifulSoup(review_page_response.content, "html.parser")

        # Extract overall review rating from the review page
        overall_rating_div = review_soup.find(
            "div", class_="styles_reviewPositive__JY_9N"
        )
        overall_rating = (
            overall_rating_div.get_text(strip=True).split("/")[0]
            if overall_rating_div
            else None
        )

        # Extract the product name
        product_name = soup.find("h1", class_="color-darker-grey").get_text(strip=True)

        # Extract the latest reviews
        reviews = []
        for review_div in review_soup.find_all(
            "div",
            class_="flex direction-column",
            id=lambda x: x and x.startswith("review-"),
        ):
            review_text_div = review_div.find("div", class_="styles_htmlText__iftLe")
            review_text = (
                review_text_div.get_text(strip=True) if review_text_div else None
            )

            # Extract the date of the review
            time_tag = review_div.find("time")
            review_date = (
                datetime.fromisoformat(time_tag["datetime"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if time_tag
                else None
            )

            reviews.append({"text": review_text, "date": review_date})

        # Extract the number of reviews
        review_count_anchor = soup.find(
            "a", href=lambda href: href and "reviews" in href
        )
        review_count_text = (
            review_count_anchor.get_text(strip=True) if review_count_anchor else None
        )

        # Use regular expression to find digits in the string
        review_count_matches = (
            re.findall(r"\d+", review_count_text) if review_count_text else []
        )
        review_count = int(review_count_matches[0]) if review_count_matches else 0

        # Extract followers
        followers_div = soup.find("div", string=re.compile(r"\bfollowers\b", re.I))
        followers_text = followers_div.get_text(strip=True) if followers_div else None

        followers = 0  # Default value in case followers count is not found
        if followers_text:
            followers_match = re.search(r"\b(\d+(?:\.\d+)?[Kk]?)\b", followers_text)
            followers_str = followers_match.group(1) if followers_match else "0"

            # Check if the followers count is in thousands and convert accordingly
            if "K" in followers_str or "k" in followers_str:
                followers = int(
                    float(followers_str.replace("K", "").replace("k", "")) * 1000
                )
            else:
                followers = int(followers_str)

        product_info = {
            "name": product_name,
            "overall_rating": overall_rating,
            "review_count": review_count,
            "followers": followers,
            "reviews": reviews,
        }

        return product_info

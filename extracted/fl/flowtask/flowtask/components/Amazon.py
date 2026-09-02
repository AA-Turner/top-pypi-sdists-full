"""
Scrapping a Web Page Using Selenium + ChromeDriver + BeautifulSoup.


        Example:

        ```yaml
        Amazon:
          type: product_info
          use_proxies: true
          paid_proxy: true
        ```

    """
from typing import Any
import asyncio
from collections.abc import Callable
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import random
import httpx
import pandas as pd
import backoff
# Internals
from ..exceptions import (
    ComponentError,
    ConfigError,
    NotSupported,
    DataNotFound,
    DataError
)
from ..interfaces.http import ua
from .reviewscrap import ReviewScrapper, on_backoff, bad_gateway_exception


class Amazon(ReviewScrapper):
    """
    Amazon.

    Combining API Key and Web Scrapping, this component will be able to extract
    Amazon Product Information (reviews, etc).

    |---|---|---|
    | version | No | version of component |


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Amazon:
          type: product_info
          use_proxies: true
          paid_proxy: true
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        super(Amazon, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # Always use proxies:
        self.use_proxy: bool = True
        self._free_proxy: bool = False
        self.cookies = {
            # "aws-session-id": "241-9979986-0092756",
            "lc-main": "en_US"
        }
        self.headers: dict = {
            'authority': 'www.amazon.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6",
            "content-language": "en-US",
            "Origin": "https://www.amazon.com",
            "Referer": "https://www.amazon.com/dp/",
            "Sec-CH-UA": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Linux"',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": random.choice(ua),
            "Connection": "keep-alive",
            'dnt': '1',
            'upgrade-insecure-requests': '1',
        }
        self.semaphore = asyncio.Semaphore(10)

    def _extract_reviews_from_page(self, soup: BeautifulSoup) -> list:
        """
        Given a BeautifulSoup-parsed Amazon reviews page, extract individual reviews.
        Returns a list of dictionaries.
        """
        reviews = []
        # Reviews are contained within the element with id 'cm-cr-review_list'
        reviews_container = soup.find(
            "ul", id="cm-cr-review_list"
        ) or soup.find("div", {"data-hook": "reviews-medley-widget"})
        if reviews_container:
            # Each review is typically in a <li> element with data-hook "review"
            for review_el in reviews_container.find_all("li", {"data-hook": "review"}):
                try:
                    # Extract review title
                    title_el = review_el.select_one("[data-hook=review-title] > span")
                    title = title_el.get_text(strip=True) if title_el else None
                    # Extract review body text
                    body_el = review_el.select_one("[data-hook=review-body]")
                    body = " ".join(body_el.stripped_strings) if body_el else None
                    # Extract review date and/or location/date information
                    date_el = review_el.select_one("[data-hook=review-date]")
                    date_text = date_el.get_text(strip=True) if date_el else None
                    # Extract rating (look for an element with data-hook containing 'review-star-rating')
                    if rating_el := review_el.select_one("[data-hook*='review-star-rating'] span.a-icon-alt"):
                        # Extract numeric rating (first match of digits possibly with a decimal)
                        import re
                        rating_match = re.search(r"(\d+\.?\d*) out", rating_el.get_text(strip=True))
                        rating = rating_match.group(1) if rating_match else None
                    else:
                        rating = None
                    # Extract Verified Purchase badge (if exists)
                    verified = bool(review_el.select_one("[data-hook=avp-badge]"))

                    review_dict = {
                        "title": title,
                        "review": body,
                        "location_and_date": date_text,
                        "rating": rating,
                        "verified": verified
                    }
                    reviews.append(review_dict)
                except Exception as e:
                    # Log exception for this review, but continue extracting others
                    self._logger.error(
                        f"Failed to parse a review: {e}"
                    )
        return reviews

    def _extract_next_page_url(self, soup: BeautifulSoup, base_url: str) -> str:
        """
        Look for a 'Next' page link in the pagination (typically via the CSS selector
        '.a-pagination .a-last > a').
        Returns an absolute URL string if found, otherwise returns None.
        """
        pagination_el = soup.select_one(".a-pagination .a-last > a")
        next_page_relative = pagination_el.get("href") if pagination_el else None
        return urljoin(base_url, next_page_relative) if next_page_relative else None

    @backoff.on_exception(
        backoff.expo,
        (httpx.TimeoutException, httpx.ConnectTimeout, httpx.HTTPStatusError, httpx.HTTPError),
        max_tries=3,
        jitter=backoff.full_jitter,
        on_backoff=on_backoff,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, httpx.ConnectTimeout)
    )
    async def _fetch_product_page(self, asin: str, cookies: httpx.Cookies, for_reviews: bool = False) -> tuple:
        product_page_url = f"https://www.amazon.com/dp/{asin}"
        response = await self._get(url=product_page_url, cookies=cookies, headers=self.headers)
        if response.status_code != 200:
            raise DataError(
                f"Failed to fetch product page, status code: {response.status_code}"
            )
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        if for_reviews:
            if medley := soup.find("div", id="reviewsMedley"):
                return product_page_url, html, soup
        elif title_div := soup.find("div", id="title_feature_div"):
            product_name = title_div.get_text(separator=" ", strip=True)
            self._logger.info(f"Extracted product name: {product_name} from {product_page_url}")
            return product_page_url, html, soup
        else:
            await asyncio.sleep(1.5)
            raise httpx.HTTPError(
                f"Failed to find product name on product page: {product_page_url}"
            )

    def _extract_reviews_from_product_page(self, url: str, row: Any, soup: BeautifulSoup) -> list:
        """Extract review snippet(s) from the product page (fallback)."""
        reviews = []
        if medley := soup.find("div", id="reviewsMedley"):
            for li in medley.find_all("li", {"data-hook": "review"}):
                try:
                    profile_user = li.find("div", {"class": "a-profile-content"})
                    profile_name = profile_user.find("span", {"class": "a-profile-name"}).get_text(strip=True)
                    customer_reviews = ""
                    title_text = ""
                    if title := li.find("a", {"data-hook": "review-title"}):
                        customer_reviews = title["href"]
                        title_text = title.find_all("span")[-1].text.strip()

                    body = li.select_one("[data-hook=review-body]")
                    body_text = " ".join(body.stripped_strings) if body else None

                    date_el = li.select_one("[data-hook=review-date]")
                    date_text = date_el.get_text(strip=True) if date_el else None

                    rating_el = li.select_one("[data-hook*='review-star-rating'] span.a-icon-alt")
                    rating_match = re.search(r"(\d+\.?\d*) out", rating_el.get_text(strip=True)) if rating_el else None
                    rating = rating_match.group(1) if rating_match else None

                    verified = bool(li.select_one("[data-hook=avp-badge]"))
                    _data = row.to_dict()
                    review_dict = {
                        "url": url,
                        "user": profile_name,
                        "customer_reviews": customer_reviews,
                        "title": title_text,
                        "review": body_text,
                        "location_and_date": date_text,
                        "rating": rating,
                        "verified": verified,
                        **_data
                    }
                    reviews.append(review_dict)
                except Exception as e:
                    self._logger.error(f"Error parsing a fallback review: {e}")
        return reviews

    async def _fetch_review_page(self, url: str, cookies: httpx.Cookies) -> str:
        """
        Fetches the review page HTML for a given URL.
        Returns the HTML text.
        """
        try:
            response = await self._get(url=url, cookies=cookies, headers=self.headers)
            if response.status_code != 200:
                raise DataError(f"Failed to fetch reviews page (status code: {response.status_code})")
            return response.text
        except Exception as e:
            raise DataError(f"Failed to fetch reviews page: {e}") from e

    async def _product_reviews(self, idx, row, cookies, max_pages: int = 5) -> list:
        async with self.semaphore:
            # Prepare payload for the API request
            asin = row['asin']
            reviews = []
            # base_review_url = f"https://www.amazon.com/product-reviews/{asin}/"
            #
            # try:
            #     # Try fetching the reviews page
            #     html = await self._fetch_review_page(base_review_url, cookies)
            #     soup = BeautifulSoup(html, "html.parser")
            #     reviews.extend(self._extract_reviews_from_page(soup))
            #     self._logger.info(f"Fetched reviews from reviews URL for ASIN {asin}")
            # except DataError as e:
            #     # If a redirect (or other error) is detected, log and fall back to the product page.
            #     self._logger.warning(
            #         f"Direct reviews page fetch failed ({e}); falling back to product page for ASIN {asin}"
            #     )
            try:
                url, _, soup = await self._fetch_product_page(asin, cookies=cookies, for_reviews=True)
                reviews.extend(
                    self._extract_reviews_from_product_page(url, row, soup)
                )
            except Exception as ee:
                self._logger.error(
                    f"Fallback product page review extraction failed: {ee}"
                )
                return []
            self._logger.info(
                f"Fetched {len(reviews)} reviews for ASIN {asin}."
            )
            await asyncio.sleep(random.randint(3, 5))
            return reviews

    async def reviews(self):
        """reviews.

        Target Product Reviews.
        """
        httpx_cookies = httpx.Cookies()
        for key, value in self.cookies.items():
            httpx_cookies.set(
                key, value,
                domain='.amazon.com',
                path='/'
            )

        # Iterate over each row in the DataFrame
        print('starting ...')
        tasks = [
            self._product_reviews(
                idx,
                row,
                httpx_cookies,
                max_pages=2
            ) for idx, row in self.data.iterrows()
        ]
        # Gather results concurrently
        all_reviews_nested = await self._processing_tasks(tasks)
        # Flatten the nested list: one item per review, and add the asin as reference.
        reviews_flat = []
        for idx, review_list in enumerate(all_reviews_nested):
            asin = self.data.iloc[idx]['asin']
            for review in review_list:
                review['asin'] = asin
                reviews_flat.append(review)

        reviews_df = pd.DataFrame(reviews_flat)
        self._logger.notice(f"Extracted total {len(reviews_df)} reviews.")

        # at the end, adding a column for origin of reviews:
        reviews_df['origin'] = 'amazon'
        self.data = reviews_df  # or store separately
        return self.data

    def _extract_product_name(self, soup: BeautifulSoup) -> str:
        if title_div := soup.find("div", id="title_feature_div"):
            return title_div.get_text(separator=" ", strip=True)
        return None

    def _extract_price(self, soup: BeautifulSoup) -> str:
        price_element = soup.select_one("span.a-offscreen")
        return price_element.get_text(strip=True) if price_element else None

    def _extract_product_description(self, soup: BeautifulSoup) -> str:
        if desc_div := soup.find("div", id="productDescription_feature_div"):
            # Sometimes there is an inner div with id="productDescription"
            if desc_inner := desc_div.find("div", id="productDescription"):
                # Join all paragraph texts into one string
                paragraphs = [p.get_text(separator=" ", strip=True) for p in desc_inner.find_all("p")]
                product_description = "\n".join([p for p in paragraphs if p])
            else:
                product_description = desc_div.get_text(separator=" ", strip=True)
            return product_description
        return None

    def _extract_rating(self, soup: BeautifulSoup) -> tuple:
        """
        Extract the average rating and review count from an Amazon product page.

        This function parses the BeautifulSoup object to find and extract the average
        customer rating and the total number of reviews for a product.

        Args:
            soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML
                                    of an Amazon product page.

        Returns:
            tuple: A tuple containing two elements:
                - review_rating (str or None): The average rating of the product
                    (e.g., "4.5 out of 5 stars"), or None if not found.
                - review_count (str or None): The total number of reviews for the
                    product (e.g., "1,234"), or None if not found.
        """
        review_rating = None
        review_count = None
        if acr_div := soup.find("div", id="averageCustomerReviews_feature_div"):
            # The star rating is contained inside a span within the "acrPopover"
            if acr_popover := acr_div.find("span", id="acrPopover"):
                if rating_span := acr_popover.find("span", class_="a-color-base"):
                    review_rating = rating_span.get_text(strip=True)
            # The review count is extracted from the anchor "acrCustomerReviewLink"
            if review_link := acr_div.find("a", id="acrCustomerReviewLink"):
                if count_span := review_link.find("span", id="acrCustomerReviewText"):
                    review_count = count_span.get_text(strip=True).replace('ratings', '').strip()
            return review_rating, review_count
        return None, None

    def _extract_product_overview(self, soup: BeautifulSoup) -> dict:
        overview = {}
        # Check if the overview container is present
        if overview_container := soup.find("div", id="productOverview_hoc_view_div"):
            # Iterate over each row in the container. Each row is typically a div with class "a-row"
            for row in overview_container.find_all("div", class_="a-row"):
                # Amazon structure: each row contains at least 2 columns.
                columns = row.find_all("div", class_="a-column")
                if len(columns) >= 2:
                    # The first column typically contains the label (e.g., "Screen Size")
                    label = columns[0].get_text(separator=" ", strip=True)
                    # The second column typically contains the value (e.g., "86 Inches")
                    value = columns[1].get_text(separator=" ", strip=True)
                    if label and value:
                        overview[label] = value
        elif overview_div := soup.find("div", id="productOverview_feature_div"):
            if table := overview_div.find("table", {"class": "a-spacing-micro"}):
                for row in table.find_all("tr"):
                    th = row.find("th")
                    td = row.find("td")
                    if th and td:
                        key = th.get_text(separator=" ", strip=True)
                        value = td.get_text(separator=" ", strip=True)
                        overview[key] = value
        return overview

    def _extract_product_details(self, soup: BeautifulSoup) -> tuple:
        # Extract technical specifications from "productDetails_techSpec_section_1"
        tech_details = {}
        if details_table := soup.find("table", id="productDetails_techSpec_section_1"):
            for tr in details_table.find_all("tr"):
                th = tr.find("th")
                td = tr.find("td")
                if th and td:
                    key = th.get_text(separator=" ", strip=True)
                    value = td.get_text(separator=" ", strip=True)
                    tech_details[key] = value

        # Extract additional product details from "productDetails_detailBullets_sections1"
        additional_details = {}
        if additional_table := soup.find("table", id="productDetails_detailBullets_sections1"):
            for tr in additional_table.find_all("tr"):
                th = tr.find("th")
                td = tr.find("td")
                if th and td:
                    key = th.get_text(separator=" ", strip=True)
                    value = td.get_text(separator=" ", strip=True)
                    additional_details[key] = value

        return tech_details, additional_details

    def _extract_product_info(self, url: str, row: Any, soup: BeautifulSoup) -> dict:
        """
        Extract product information from the Amazon product page.
        Returns a dictionary with:
            - productName: from 'title_feature_div'
            - overview: (e.g., screen size, brand, display technology, resolution, refresh rate)
            - reviewRating: from 'acrPopover' (if available)
            - reviewCount: from 'acrCustomerReviewText' (if available)
            - technicalDetails: from table "productDetails_techSpec_section_1"
            - additionalDetails: from table "productDetails_detailBullets_sections1"
        """
        # Extract product information here
        # Return a dictionary with relevant fields
        # Extract product name from "title_feature_div"
        # --- Product Name ---
        product_name = self._extract_product_name(soup)
        prince = self._extract_price(soup)

        # Extract review rating and count from "averageCustomerReviews"
        review_rating, review_count = self._extract_rating(soup)

        # --- Overview (revised for dynamic content) ---
        overview = self._extract_product_overview(soup)

        # --- Technical Details ---
        tech_details, additional_details = self._extract_product_details(soup)

        # --- Product Description ---
        product_description = self._extract_product_description(soup)

        # --- About This Item (feature bullets) ---
        about_this_item = []
        if featurebullets_div := soup.find("div", id="featurebullets_feature_div"):
            if ul := featurebullets_div.find("ul", {"class": "a-unordered-list"}):
                # Extract each bullet text and add to list
                for li in ul.find_all("li"):
                    if text := li.get_text(separator=" ", strip=True):
                        about_this_item.append(text)
        _data = row.to_dict()
        return {
            "product_name": product_name,
            "price": prince,
            "url": url,
            "about_this_item": about_this_item,
            "rating": review_rating,
            "review_count": review_count,
            "overview": overview,
            "description": product_description,
            "tech_details": tech_details,
            "additional_details": additional_details,
            **_data
        }

    async def _product_information(self, idx, row, cookies):
        async with self.semaphore:
            # Prepare payload for the API request
            asin = row['asin']
            try:
                # Fetch the product page
                url, html, soup = await self._fetch_product_page(asin, cookies=cookies, for_reviews=False)
                if not html:
                    self._logger.warning(
                        f"No Product Information found for {asin}."
                    )
                    return {}
            except (httpx.TimeoutException, httpx.HTTPError) as ex:
                self._logger.warning(f"Request failed: {ex}")
                return []
            except Exception as ex:
                self._logger.error(f"An error occurred: {ex}")
                return []

            # Extract the product information using BeautifulSoup
            if product_info := self._extract_product_info(url, row, soup):
                return product_info
            raise DataNotFound(
                f"Failed to extract product information for {asin}"
            )

    async def product_info(self):
        """product_info.

        Product Information.
        """
        httpx_cookies = httpx.Cookies()
        for key, value in self.cookies.items():
            httpx_cookies.set(
                key, value,
                domain='.amazon.com',
                path='/'
            )

        # Iterate over each row in the DataFrame
        print('starting ...')

        tasks = [
            self._product_information(
                idx,
                row,
                httpx_cookies
            ) for idx, row in self.data.iterrows()
        ]
        # Gather results concurrently
        all_products = await self._processing_tasks(tasks)

        # Convert to DataFrame
        df = pd.DataFrame(all_products)

        # show the num of rows in final dataframe:
        self._logger.notice(
            f"Ending Product Info: {len(df)}"
        )

        # Override previous dataframe:
        self.data = df

        # return existing data
        return self.data

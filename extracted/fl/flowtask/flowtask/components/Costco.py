"""
Costco Product Reviews Scraper using Bazaarvoice API.

Example configuration:
```yaml
Costco:
  type: reviews
  use_proxies: true
  paid_proxy: false
  api_token: xxx
```
"""
import asyncio
from collections.abc import Callable
import random
import re
import httpx
from urllib.parse import urlencode
import pandas as pd
import backoff
# Internals
from ..exceptions import (
    ComponentError,
    ConfigError,
    NotSupported
)
from ..interfaces.http import ua
from .reviewscrap import ReviewScrapper, bad_gateway_exception


class Costco(ReviewScrapper):
    """
    Costco Product Reviews Scraper.

    This component extracts product reviews from Costco using the Bazaarvoice API.
    It expects a DataFrame with product URLs or product IDs.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Costco:
          type: reviews
          use_proxies: true
          paid_proxy: false
          api_token: xxx
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
        super(Costco, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # Costco uses Bazaarvoice API, so we don't need special proxy settings
        self.use_proxy: bool = kwargs.get('use_proxies', False)
        self._free_proxy: bool = not kwargs.get('paid_proxy', False)

        # Bazaarvoice API headers
        self.headers: dict = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "User-Agent": random.choice(ua),
            "Referer": "https://www.costco.com/",
            "Origin": "https://www.costco.com"
        }

        # Bazaarvoice API configuration
        self.base_api_url = "https://api.bazaarvoice.com/data/reviews.json"
        self.passkey = "bai25xto36hkl5erybga10t99"  # Costco's Bazaarvoice passkey
        self.api_version = "5.5"
        self.display_code = "2070_2_0-en_us"

        self.semaphore = asyncio.Semaphore(10)

    async def close(self, **kwargs) -> bool:
        self.close_driver()
        return True

    async def start(self, **kwargs) -> bool:
        await super(Costco, self).start(**kwargs)
        if self.previous:
            self.data = self.input
            if not isinstance(self.data, pd.DataFrame):
                raise ComponentError(
                    "Incompatible Pandas Dataframe"
                )

        # Check if required columns exist
        if 'product_url' not in self.data.columns and 'product_id' not in self.data.columns:
            raise ConfigError(
                "Costco: DataFrame must contain either 'product_url' or 'product_id' column"
            )

        if not hasattr(self, self._fn):
            raise ConfigError(
                f"Costco: Unable to find function {self._fn} in Costco Component."
            )

    def extract_product_id(self, product_url: str) -> str:
        """Extract product ID from Costco URL.

        Args:
            product_url: Costco product URL

        Returns:
            Product ID as string

        Example:
            URL: https://www.costco.com/kidkraft-atrium-breeze-wooden-outdoor-playhouse-with-sunroom--play-kitchen.product.4000317158.html
            Returns: 4000317158
        """
        # Pattern to match Costco product URLs and extract product ID
        pattern = r'\.product\.(\d+)\.html'
        match = re.search(pattern, product_url)

        if match:
            return match.group(1)
        else:
            raise ValueError(f"Could not extract product ID from URL: {product_url}")

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.HTTPStatusError),
        max_tries=3,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, httpx.ConnectTimeout)
    )
    async def _product_reviews(self, idx, row):
        """Extract reviews for a single product."""
        async with self.semaphore:
            # Get product ID from URL or directly from product_id column
            if 'product_id' in row and pd.notna(row['product_id']):
                product_id = str(row['product_id'])
            elif 'product_url' in row and pd.notna(row['product_url']):
                try:
                    product_id = self.extract_product_id(row['product_url'])
                except ValueError as e:
                    self._logger.warning(f"Row {idx}: {e}")
                    return []
            else:
                self._logger.warning(
                    f"Row {idx}: No product_id or product_url found")
                return []

            # API parameters
            limit = 50  # Maximum per request
            offset = 0
            max_pages = 20  # Maximum pages to fetch
            all_reviews = []
            total_reviews = 0

            try:
                while offset < max_pages * limit:
                    url_params = [
                        "resource=reviews",
                        "action=REVIEWS_N_STATS",
                        f"filter=productid%3Aeq%3A{product_id}",
                        "filter=contentlocale%3Aeq%3Aen_CA%2Cfr_CA%2Cen_US%2Cen_US",
                        "filter=isratingsonly%3Aeq%3Afalse",
                        "filter_reviews=contentlocale%3Aeq%3Aen_CA%2Cfr_CA%2Cen_US%2Cen_US",
                        "include=authors%2Cproducts%2Ccomments",
                        "filteredstats=reviews",
                        "Stats=Reviews",
                        f"limit={limit}",
                        f"offset={offset}",
                        "limit_comments=3",
                        "sort=submissiontime%3Adesc",
                        f"passkey={self.passkey}",
                        f"apiversion={self.api_version}",
                        f"displaycode={self.display_code}"
                    ]
                    try:
                        url = f"{self.base_api_url}?{'&'.join(url_params)}"
                        result = await self.api_get(
                            url=url,
                            headers=self.headers
                        )
                    except httpx.HTTPStatusError as e:
                        if e.response.status_code == 502:
                            self._logger.warning(
                                f"Bad Gateway error for product {product_id}: {e}"
                            )
                            return []
                        else:
                            raise

                    if not result:
                        self._logger.warning(
                            f"No API response for product ID {product_id}"
                        )
                        break

                    # Check for API errors
                    if result.get('HasErrors', False):
                        errors = result.get('Errors', [])
                        self._logger.error(f"API errors for product {product_id}: {errors}")
                        break

                    # Extract reviews
                    reviews_data = result.get('Results', [])
                    total_reviews = result.get('TotalResults', 0)

                    if not reviews_data:
                        self._logger.info(f"No more reviews for product {product_id} at offset {offset}")
                        break

                    all_reviews.extend(reviews_data)

                    # Check if we have all reviews
                    if len(all_reviews) >= total_reviews:
                        self._logger.info(f"Fetched all {total_reviews} reviews for product {product_id}")
                        break

                    offset += limit

            except (httpx.TimeoutException, httpx.HTTPError) as ex:
                self._logger.warning(
                    f"Request failed for product {product_id}: {ex}"
                )
                return []
            except Exception as ex:
                self._logger.error(
                    f"Error processing product {product_id}: {ex}"
                )
                return []

            # Process reviews
            reviews = []
            for review_data in all_reviews:
                # Combine original row data with review data
                review_row = row.to_dict()

                # Extract review fields
                review = {
                    **review_row,
                    "product_id": product_id,
                    "review_id": review_data.get("Id"),
                    "cid": review_data.get("CID"),
                    "title": review_data.get("Title"),
                    "review": review_data.get("ReviewText"),
                    "rating": review_data.get("Rating"),
                    "is_recommended": review_data.get("IsRecommended"),
                    "user_nickname": review_data.get("UserNickname"),
                    "user_location": review_data.get("UserLocation"),
                    "submission_time": review_data.get("SubmissionTime"),
                    "last_modified_time": review_data.get("LastModificationTime"),
                    "moderation_status": review_data.get("ModerationStatus"),
                    "is_featured": review_data.get("IsFeatured", False),
                    "is_ratings_only": review_data.get("IsRatingsOnly", False),
                    "is_syndicated": review_data.get("IsSyndicated", False),
                    "verified_purchaser": self._extract_verified_purchaser(review_data),
                    "helpful_votes": review_data.get("TotalPositiveFeedbackCount", 0),
                    "not_helpful_votes": review_data.get("TotalNegativeFeedbackCount", 0),
                    "total_feedback": review_data.get("TotalFeedbackCount", 0),
                    "campaign_id": review_data.get("CampaignId"),
                    "pros": review_data.get("Pros"),
                    "cons": review_data.get("Cons"),
                    "secondary_ratings": review_data.get("SecondaryRatings"),
                    "photos": len(review_data.get("Photos", [])),
                    "videos": len(review_data.get("Videos", [])),
                    "client_responses": self._extract_client_responses(review_data),
                    "total_reviews": total_reviews
                }
                reviews.append(review)

            self._logger.info(f"Extracted {len(reviews)} reviews for product {product_id}")
            return reviews

    def _extract_verified_purchaser(self, review_data: dict) -> bool:
        """Extract verified purchaser status from badges."""
        badges = review_data.get("Badges", {})
        return "verifiedPurchaser" in badges

    def _extract_client_responses(self, review_data: dict) -> str:
        """Extract and concatenate client responses."""
        client_responses = review_data.get("ClientResponses", [])
        if not client_responses:
            return ""

        responses = []
        for response in client_responses:
            response_text = response.get("Response", "").strip()
            if response_text:
                responses.append(response_text)

        return " | ".join(responses)

    async def reviews(self):
        """Extract reviews for all products in the DataFrame."""
        self._logger.info("Starting Costco reviews extraction...")

        # Create tasks for concurrent processing
        tasks = [
            self._product_reviews(idx, row)
            for idx, row in self.data.iterrows()
        ]

        # Process tasks concurrently
        all_reviews_nested = await self._processing_tasks(tasks)

        # Flatten results
        all_reviews = [
            review for reviews in all_reviews_nested
            for review in reviews
        ]

        # Convert to DataFrame
        reviews_df = pd.DataFrame(all_reviews)

        # Add origin column
        reviews_df['origin'] = 'costco'

        self._logger.notice(f"Completed Costco reviews extraction: {len(reviews_df)} reviews")

        # Update data
        self.data = reviews_df
        return self.data

    async def product_details(self):
        """Extract product details (placeholder for future implementation)."""
        raise NotSupported("Product details extraction not yet implemented for Costco")

    async def product_info(self):
        """Extract product information (placeholder for future implementation)."""
        raise NotSupported("Product info extraction not yet implemented for Costco")

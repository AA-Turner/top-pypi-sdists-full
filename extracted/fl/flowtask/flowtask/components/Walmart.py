"""
Scrapping a Web Page Using Selenium + ChromeDriver + BeautifulSoup.
"""
import asyncio
from collections.abc import Callable
import random
import json
from urllib.parse import quote_plus
import httpx
import pandas as pd
import backoff
from ..interfaces.http import ua
from .reviewscrap import ReviewScrapper, bad_gateway_exception


class Walmart(ReviewScrapper):
    """
    Walmart.

    Combining API Key and Web Scrapping, this component will be able to extract
    Walmart Information (reviews, etc).

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Walmart:
          # attributes here
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
        super(Walmart, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # Always use proxies:
        self.use_proxy: bool = True
        self._free_proxy: bool = False
        self.cookies = {
            "_pxhd": "dbf5757b1f867196173eab3a4ab6377bbcd202cdd59b89b4372a1cf3f681b1aa:69fe9bd8-cfbd-11ef-9827-8c8dc170f864",  # noqa
        }
        self.headers: dict = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US",
            "Content-Type": "application/json",
            "Referer": "https://www.walmart.com/reviews/",
            "Sec-CH-UA": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Linux"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Connection": "keep-alive",
            "User-Agent": random.choice(ua),
        }
        self.semaphore = asyncio.Semaphore(10)

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.HTTPStatusError),
        max_tries=2,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, httpx.ConnectTimeout)
    )
    async def _product_reviews(self, idx, row, cookies):
        async with self.semaphore:
            # Prepare payload for the API request
            sku = row['itemId']
            max_pages = 2   # Maximum number of pages to fetch
            all_reviews = []
            total_reviews = 0
            current_page = 1
            try:
                variables = {
                    "itemId": sku,
                    "page": 1,  # Start with page 1
                    "sort": "submission-desc",
                    "limit": 10,
                    "filters": [],
                    "aspect": None,
                    "filterCriteria": {
                        "rating": [],
                        "reviewAttributes": [],
                        "aspectId": None
                    }
                }
                while True:
                    self.headers['Referer'] = f"https://www.walmart.com/reviews/product/{sku}?sort=submission-desc&page=1"  # noqa
                    variables['page'] = current_page
                    variables_json = json.dumps(variables)  # Proper JSON encoding
                    variables_encoded = quote_plus(variables_json)
                    url = f"https://www.walmart.com/orchestra/home/graphql/ReviewsById/{self.api_token}?variables={variables_encoded}"  # noqa
                    print('URL > ', url)
                    result = await self.api_get(
                        url=url,
                        cookies=cookies,
                        headers=self.headers
                    )
                    if not result:
                        self._logger.warning(
                            f"No Product Reviews found for {sku}."
                        )
                        break
                    # Extract the reviews data from the API response
                    data = result.get('data', {})
                    reviews_data = data.get('reviews', {})
                    customer_reviews = reviews_data.get('customerReviews', [])
                    pagination = reviews_data.get('pagination', {})
                    # Update total_reviews
                    total_reviews = data.get('reviews', {}).get('totalReviewCount', 0)
                    if not customer_reviews:
                        self._logger.info(f"No more reviews found for itemId {row['itemId']} on page {current_page}.")
                        break

                    all_reviews.extend(customer_reviews)
                    if len(all_reviews) >= total_reviews:
                        self._logger.info(f"Fetched all reviews for itemId {row['itemId']}.")
                        break

                    current_page += 1
                    if current_page > max_pages:
                        self._logger.warning(f"Reached maximum page limit for itemId {row['itemId']}.")
                        break
            except (httpx.TimeoutException, httpx.HTTPError) as ex:
                self._logger.warning(f"Request failed: {ex}")
                return []
            except Exception as ex:
                self._logger.error(f"An error occurred: {ex}")
                return []

            # Extract the reviews data from the API response
            reviews = []
            for item in all_reviews:
                # Exclude certain keys
                # Extract relevant fields
                # Combine with original row data
                review_data = row.to_dict()
                review = {
                    **review_data,
                    "authorId": item.get("authorId"),
                    "userNickname": item.get("userNickname"),
                    "rating": item.get("rating"),
                    "reviewTitle": item.get("reviewTitle"),
                    "review": item.get("reviewText"),
                    "reviewSubmissionTime": item.get("reviewSubmissionTime"),
                    "clientResponses": item.get("clientResponses"),
                    "media": item.get("media"),
                    "itemId": sku,
                    "productName": row.get("productName"),
                    "productCategory": row.get("productCategory"),
                }
                review['total_reviews'] = total_reviews
                reviews.append(review)
            self._logger.info(
                f"Fetched {len(reviews)} reviews for SKU {sku}."
            )
            return reviews

    async def reviews(self):
        """reviews.

        Target Product Reviews.
        """
        httpx_cookies = httpx.Cookies()
        for key, value in self.cookies.items():
            httpx_cookies.set(
                key, value,
                domain='.walmart.com',
                path='/'
            )

        # Iterate over each row in the DataFrame
        print('starting ...')

        tasks = [
            self._product_reviews(
                idx,
                row,
                httpx_cookies
            ) for idx, row in self.data.iterrows()
        ]
        # Gather results concurrently
        all_reviews_nested = await self._processing_tasks(tasks)

        # Flatten the list of lists
        all_reviews = [review for reviews in all_reviews_nested for review in reviews]

        # Convert to DataFrame
        reviews_df = pd.DataFrame(all_reviews)

        # show the num of rows in final dataframe:
        self._logger.notice(
            f"Ending Product Reviews: {len(reviews_df)}"
        )

        # Override previous dataframe:
        self.data = reviews_df

        # return existing data
        return self.data

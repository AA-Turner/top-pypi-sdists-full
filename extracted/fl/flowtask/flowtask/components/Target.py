"""
Scrapping a Web Page Using Selenium + ChromeDriver + BeautifulSoup.
"""
import asyncio
from collections.abc import Callable
import random
import httpx
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


class Target(ReviewScrapper):
    """
    Target.

    Combining API Key and Web Scrapping, this component will be able to extract
    TARGET Information (reviews, etc).

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Target:
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
        self._fn = kwargs.pop('type', None)
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self.task_parts: int = kwargs.get('task_parts', 10)
        self.product_info: bool = kwargs.get('product_info', False)
        if not self._fn:
            raise ConfigError(
                "Target: require a `type` Function to be called, ex: availability"
            )
        super(Target, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # Always use proxies:
        self.use_proxy: bool = True
        self._free_proxy: bool = False
        # SECURITY: JWT tokens removed from hardcoded values. Use environment variables TARGET_ACCESS_TOKEN and TARGET_ID_TOKEN
        self.cookies = {
            "Sid": "WcMH6IPyatK95shr5A-IWjsGf-qeWLo_",
            "UserLocation": "45510|40.050|-4.210|TO|ES",
            "__eoi": "ID=9528bd272a92431a:T=1736552136:RT=1736554579:S=AA-AfjZSTuM0txUk7Lsy-pJtCFok",
            "accessToken": "",  # SECURITY: Load from TARGET_ACCESS_TOKEN environment variable
            "adScriptData": "TO",
            "crl8.fpcuid": "c2aa8017-a2e2-4d24-a61e-2093551bb881",
            "egsSessionId": "ffbc34de-8a71-4eeb-9490-6382040b0124",
            "ffsession": "{%22sessionHash%22:%224a74f57be4bb61736552136688%22}",
            "fiatsCookie": "DSI_1092|DSN_Beechmont%20Area|DSZ_45255",
            "idToken": "",  # SECURITY: Load from TARGET_ID_TOKEN environment variable
            "refreshToken": "GQHHnolvR5mW5lY6C9BbK1XbpFSE3F_yFwtKjSUCJOaikGHKg5Ju0eyjhRlm9NmaYegjQuxPnVSv1kh75Y1VOg",
            "sapphire": "1",
            "visitorId": "01945292BA770201AEAA83A7E83DE4E9",
            "kampyleSessionPageCounter": "6",
            "kampyleUserSession": "1736552137812",
            "kampyleUserSessionsCount": "4",
            "mdLogger": "false",
        }
        self.headers: dict = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6",
            "Origin": "https://www.target.com",
            "Referer": "https://www.target.com/p/",
            "Sec-CH-UA": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Linux"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": random.choice(ua),
        }
        self.semaphore = asyncio.Semaphore(10)

    async def close(self, **kwargs) -> bool:
        self.close_driver()
        return True

    async def start(self, **kwargs) -> bool:
        await super(Target, self).start(**kwargs)
        if self.previous:
            self.data = self.input
            if not isinstance(self.data, pd.DataFrame):
                raise ComponentError(
                    "Incompatible Pandas Dataframe"
                )
        self.api_token = self.get_env_value(self.api_token) if hasattr(self, 'api_token') else self.get_env_value('TARGET_API_KEY')  # noqa
        if not hasattr(self, self._fn):
            raise ConfigError(
                f"Target: Unable to found Function {self._fn} in Target Component."
            )

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.HTTPStatusError),
        max_tries=2,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, httpx.ConnectTimeout)
    )
    async def _product_reviews(self, idx, row, cookies):
        async with self.semaphore:
            # Prepare payload for the API request
            sku = row['sku']
            pagesize = 20
            max_pages = 2   # Maximum number of pages to fetch
            current_page = 0
            all_reviews = []
            total_reviews = 0
            try:
                while current_page <= max_pages:
                    payload = {
                        "key": "c6b68aaef0eac4df4931aae70500b7056531cb37",  # Ensure this key is valid and authorized
                        "hasOnlyPhotos": "false",
                        "includes": "reviews,reviewsWithPhotos,entities,metadata,statistics",
                        "page": current_page,
                        "entity": "",
                        "reviewedId": sku,  # Ensure sku corresponds to 'reviewedId'
                        "reviewType": "PRODUCT",
                        "size": pagesize,
                        "sortBy": "most_recent",
                        "verifiedOnly": "false",
                    }
                    url = "https://r2d2.target.com/ggc/v2/summary"
                    result = await self.api_get(
                        url=url,
                        cookies=cookies,
                        params=payload,
                        headers=self.headers
                    )
                    total_reviews = result.get('statistics', {}).get('review_count', 0)
                    if not result:
                        self._logger.warning(
                            f"No Product Reviews found for {sku}."
                        )
                        break
                    # Extract the reviews data from the API response
                    reviews_section = result.get('reviews', {})
                    items = reviews_section.get('results', [])
                    if len(items) == 0:
                        break
                    all_reviews.extend(items)
                    # Determine if we've reached the last page
                    total_pages = reviews_section.get('total_pages', max_pages)
                    if current_page >= total_pages:
                        break
                    current_page += 1  # Move to the next page
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
                filtered_item = {
                    k: v for k, v in item.items()
                    if k not in ('photos', 'Badges', 'entities', 'tags', 'reviewer_attributes')
                }
                # Combine with original row data
                review_data = row.to_dict()
                review_data['total_reviews'] = total_reviews
                review_data.update(filtered_item)
                reviews.append(review_data)
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
                domain='.target.com',
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
        reviews_df.rename(columns={"text": "review", "Rating": "rating"})
        self.data = reviews_df

        # return existing data
        return self.data

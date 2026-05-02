"""
Scrapping a Web Page Using Selenium + ChromeDriver + BeautifulSoup.


        Example:

        ```yaml
        Lowes:
          type: reviews
          use_proxies: true
          paid_proxy: true
          api_token: xxx
        ```

    """
import asyncio
from collections.abc import Callable
import random
import httpx
from urllib.parse import urlencode, quote_plus
import pandas as pd
import backoff
from bs4 import BeautifulSoup
from typing import Any
import re
import ssl
# Internals
from ..exceptions import (
    ComponentError,
    ConfigError,
    NotSupported
)
from ..interfaces.http import ua
from .reviewscrap import ReviewScrapper, bad_gateway_exception


class Lowes(ReviewScrapper):
    """
    Lowes.

    Combining API Key and Web Scrapping, this component will be able to extract
    Lowes Information (reviews, etc).

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Lowes:
          type: reviews
          use_proxies: true
          paid_proxy: true
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
        self.brand = kwargs.get('brand')
        self.top_n = kwargs.get('top_n', 3)
        super(Lowes, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # Always use proxies:
        self.use_proxy: bool = True
        self._free_proxy: bool = False
        self.cookies = {
            "dbidv2": "956aa8ea-87f3-4068-96a8-3e2bdf4e84ec",
            "al_sess": "FuA4EWsuT07UWryyq/3foLUcOGRVVGi7yYKO2imCjWnuWxkaJXwqJRDEw8CjJaWJ",
            # Add other necessary cookies here
            # Ensure tokens are valid and not expired
        }
        self.headers: dict = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": "www.lowes.com",
            "Pragma": "no-cache",
            "Origin": "https://www.lowes.com",
            "Referer": "https://www.lowes.com/pd/",
            "Sec-CH-UA": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Linux"',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": random.choice(ua)
        }
        self.semaphore = asyncio.Semaphore(10)

    async def close(self, **kwargs) -> bool:
        self.close_driver()
        return True

    async def start(self, **kwargs) -> bool:
        await super(Lowes, self).start(**kwargs)
        if self.previous:
            self.data = self.input
            if not isinstance(self.data, pd.DataFrame):
                raise ComponentError(
                    "Incompatible Pandas Dataframe"
                )
        self.api_token = self.get_env_value(self.api_token) if hasattr(self, 'api_token') else self.get_env_value('TARGET_API_KEY')  # noqa
        if not hasattr(self, self._fn):
            raise ConfigError(
                f"Lowes: Unable to found Function {self._fn} in Component."
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
            page_size = 10  # fixed size
            current_offset = 0
            max_pages = 20  # Maximum number of pages to fetch
            all_reviews = []
            total_reviews = 0
            
            # Process reviews in batches to preserve data on errors
            def process_reviews_batch(reviews_batch, total_reviews_count):
                """Process a batch of reviews and return formatted reviews list."""
                batch_reviews = []
                for item in reviews_batch:
                    # Extract relevant fields
                    # Combine with original row data
                    review_data = row.to_dict()
                    review = {
                        **review_data,
                        "id": item.get("id"),
                        "legacyId": item.get("legacyId"),
                        "title": item.get("title"),
                        "review": item.get("reviewText"),
                        "rating": item.get("rating"),
                        "isRecommended": item.get("isRecommended"),
                        "userNickname": item.get("userNickname"),
                        "submissionTime": item.get("submissionTime"),
                        "verifiedPurchaser": item.get("verifiedPurchaser"),
                        "helpfulVoteCount": item.get("helpfulVoteCount"),
                        "notHelpfulVoteCount": item.get("notHelpfulVoteCount"),
                        "clientResponses": item.get("clientResponses"),
                        "relevancyScore": item.get("relevancyScore"),
                        "productId": item.get("productId"),
                    }
                    review['total_reviews'] = total_reviews_count
                    # Optionally, handle client responses
                    if review["clientResponses"]:
                        # For simplicity, concatenate all responses into a single string
                        responses = []
                        for response in review["clientResponses"]:
                            response_text = response.get("response", "")
                            responses.append(response_text.strip())
                        review["clientResponses"] = " | ".join(responses)
                    batch_reviews.append(review)
                return batch_reviews

            try:
                while current_offset < max_pages * page_size:
                    try:
                        if current_offset == 0:
                            payload = {
                                "sortBy": "newestFirst"
                            }
                        else:
                            payload = {
                                "sortBy": "newestFirst",
                                "offset": current_offset
                            }
                        url = f"https://www.lowes.com/rnr/r/get-by-product/{sku}"
                        result = await self.api_get(
                            url=url,
                            cookies=cookies,
                            params=payload,
                            headers=self.headers,
                            use_http2=False
                        )
                        if not result:
                            self._logger.warning(
                                f"No Product Reviews found for {sku}."
                            )
                            break
                        # Extract the reviews data from the API response
                        reviews_section = result.get('results', [])
                        total_reviews = result.get('totalResults', 0)
                        if not reviews_section:
                            self._logger.info(f"No more reviews found for SKU {sku} at offset {current_offset}.")
                            break
                        if len(reviews_section) == 0:
                            break
                        
                        # Process this batch of reviews immediately
                        batch_reviews = process_reviews_batch(reviews_section, total_reviews)
                        all_reviews.extend(batch_reviews)
                        
                        self._logger.info(f"Fetched {len(reviews_section)} reviews for SKU {sku} at offset {current_offset}. Total so far: {len(all_reviews)}")

                        # Check if we've fetched all reviews
                        if len(all_reviews) >= total_reviews:
                            self._logger.info(f"Fetched all reviews for SKU {sku}.")
                            break
                        current_offset += page_size  # Move to the next page
                        
                    except (httpx.TimeoutException, httpx.HTTPError, ssl.SSLError) as ex:
                        self._logger.warning(f"Request failed for SKU {sku} at offset {current_offset}: {ex}")
                        # If we have reviews already, return them instead of empty list
                        if all_reviews:
                            self._logger.info(f"Returning {len(all_reviews)} reviews already collected for SKU {sku} despite error.")
                            return all_reviews
                        else:
                            return []
                    except Exception as ex:
                        self._logger.error(f"An unexpected error occurred for SKU {sku} at offset {current_offset}: {ex}")
                        # If we have reviews already, return them instead of empty list
                        if all_reviews:
                            self._logger.info(f"Returning {len(all_reviews)} reviews already collected for SKU {sku} despite error.")
                            return all_reviews
                        else:
                            return []
                            
            except Exception as ex:
                self._logger.error(f"Critical error in _product_reviews for SKU {sku}: {ex}")
                # If we have reviews already, return them instead of empty list
                if all_reviews:
                    self._logger.info(f"Returning {len(all_reviews)} reviews already collected for SKU {sku} despite critical error.")
                    return all_reviews
                else:
                    return []

            self._logger.info(
                f"Successfully fetched {len(all_reviews)} reviews for SKU {sku}."
            )
            return all_reviews

    async def reviews(self):
        """reviews.

        Target Product Reviews.
        """
        httpx_cookies = httpx.Cookies()
        for key, value in self.cookies.items():
            httpx_cookies.set(
                key, value,
                domain='.lowes.com',
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

        # at the end, adding a column for origin of reviews:
        reviews_df['origin'] = 'lowes'

        # show the num of rows in final dataframe:
        self._logger.notice(
            f"Ending Product Reviews: {len(reviews_df)}"
        )

        # Override previous dataframe:
        self.data = reviews_df

        # return existing data
        return self.data

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.HTTPStatusError),
        max_tries=2,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, httpx.ConnectTimeout)
    )
    async def _product_details(self, idx, row, cookies):
        async with self.semaphore:
            # Prepare payload for the API request
            sku = row['sku']
            storeid = row['store_id']
            zipcode = row['zipcode'],
            state_code = row['state_code']
            payload = {
                "nearByStore": storeid,
                "zipState": state_code,
                "quantity": 1
            }
            try:
                # url = "https://www.lowes.com/lowes-proxy/wpd/1000379005/productdetail/1845/Guest/60639?nearByStore=1845&zipState=IL&quantity=1"
                # url = f"https://www.lowes.com/wpd/{sku}/productdetail/{storeid}/Guest/{zipcode}"
                url = f"https://www.lowes.com/lowes-proxy/wpd/{sku}/productdetail/{storeid}/Guest/{zipcode}"
                result = await self.api_get(
                    url=url,
                    # cookies=cookies,
                    # params=payload,
                    headers=self.headers
                )
                if not result:
                    self._logger.warning(
                        f"No Product Details found for {sku}."
                    )
                    return []
                # Extract the product details data from the API response
                print('RESULT > ', result)
            except (httpx.TimeoutException, httpx.HTTPError) as ex:
                self._logger.warning(f"Request failed: {ex}")
                return []
            except Exception as ex:
                print(ex)
                self._logger.error(f"An error occurred: {ex}")
                return []

    async def product_details(self):
        """product_details.

        Get Product Details from Lowes URL.
        """
        self.cookies = {}
        httpx_cookies = httpx.Cookies()
        for key, value in self.cookies.items():
            httpx_cookies.set(
                key, value,
                domain='.lowes.com',
                path='/'
            )

        # Iterate over each row in the DataFrame
        print('starting ...')

        tasks = [
            self._product_details(
                idx,
                row,
                httpx_cookies
            ) for idx, row in self.data.iterrows()
        ]
        # Gather results concurrently
        all_products_nested = await self._processing_tasks(tasks)

        # Flatten the list of lists
        all_products = [product for products in all_products_nested for product in products]

        # Convert to DataFrame
        _df = pd.DataFrame(all_products)

        # at the end, adding a column for origin of reviews:
        _df['origin'] = 'lowes'

        # show the num of rows in final dataframe:
        self._logger.notice(
            f"Ending Product Details: {len(_df)}"
        )

        # Override previous dataframe:
        self.data = _df

        # return existing data
        return self.data

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.HTTPStatusError),
        max_tries=2,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, httpx.ConnectTimeout)
    )
    async def _product_info(self, idx, row, cookies):
        async with self.semaphore:
            # Prepare payload for the API request
            product = row['search_term']
            payload = {
                "searchTerm": product,
                "sortMethod": "sortBy_bestSellers",
                "refinement": "4294851174"
            }
            try:
                base_url = "https://www.lowes.com/search"
                url = f"{base_url}?searchTerm={product}&sortMethod=sortBy_bestSellers&refinement=4294851174"
                result = await self.api_get(
                    url=url,
                    headers=self.headers
                )
                if not result:
                    self._logger.warning(
                        f"No Product Info found for {product}."
                    )
                    return []
                # Extract the product details data from the API response
                print('RESULT > ', result)
            except (httpx.TimeoutException, httpx.HTTPError) as ex:
                self._logger.warning(f"Request failed: {ex}")
                return []
            except Exception as ex:
                print(ex)
                self._logger.error(f"An error occurred: {ex}")
                return []

    async def product_info(self):
        """product_info.

        Get Product Information from Lowes URL.
        """
        self.cookies = {}
        httpx_cookies = httpx.Cookies()
        for key, value in self.cookies.items():
            httpx_cookies.set(
                key, value,
                domain='.lowes.com',
                path='/'
            )

        # Iterate over each row in the DataFrame
        print('starting ...')

        tasks = [
            self._product_info(
                idx,
                row,
                httpx_cookies
            ) for idx, row in self.data.iterrows()
        ]
        # Gather results concurrently
        all_products_nested = await self._processing_tasks(tasks)

        # Flatten the list of lists
        all_products = [product for products in all_products_nested for product in products]

        # Convert to DataFrame
        _df = pd.DataFrame(all_products)

        # at the end, adding a column for origin of reviews:
        _df['origin'] = 'lowes'

        # show the num of rows in final dataframe:
        self._logger.notice(
            f"Ending Product Info: {len(_df)}"
        )

        # Override previous dataframe:
        self.data = _df

        # return existing data
        return self.data

    def _get_search_url(self, brand: str, sku: str) -> str:
        """Generate search URL for Lowes products."""
        search_term = f'{brand} {sku}'.replace(' ', '%20')
        url = f"https://www.lowes.com/search?searchTerm={search_term}"
        self._logger.info(f'Search URL: {url}')
        return url

    async def _extract_product_info(self, product_element):
        """Extract basic product information from a product element."""
        try:
            # Extract product name/title
            title_element = product_element.select_one(
                'h3.product-title a, h4.product-title a, a.product-title'
            ) or product_element.select_one('a[data-testid="product-link"]')
            
            if not title_element:
                return None

            title = title_element.text.strip()
            url = title_element.get('href', None)
            if url and not url.startswith('http'):
                url = f"https://www.lowes.com{url}"
            
            self._logger.info(f'Product URL: {url}')

            # Extract price
            price_element = product_element.select_one(
                'span.price, div.price, span[data-testid="price"]'
            )
            price = price_element.text.strip() if price_element else "N/A"

            # Extract image
            image_element = product_element.select_one('img.product-image, img')
            image = image_element['src'] if image_element and 'src' in image_element.attrs else None

            # Extract SKU (if available in the element)
            sku_element = product_element.select_one('[data-sku], [data-product-id]')
            sku_id = None
            if sku_element:
                sku_id = sku_element.get('data-sku') or sku_element.get('data-product-id')

            return {
                "sku": sku_id,
                "product_name": title,
                "image_url": image,
                "price": price,
                "url": url
            }
        except Exception as e:
            self._logger.error(f"Error extracting product info: {e}")
            return None

    async def _product_info_selenium(self, idx, row):
        """Extract product information for a specific row using Selenium."""
        async with self.semaphore:
            model = row.get('model')
            brand = row.get('brand')
            sku = row.get('sku')

            self.brand = brand
            self.sku = sku
            self.model = model

            try:
                url = self._get_search_url(brand, model or sku)
                if not self._driver:
                    await self.get_driver()
                await self.get_page(url)
                self.data.loc[idx, 'enabled'] = False

                # Scroll to load more products
                self._execute_scroll(scroll_pause_time=2.0, max_scrolls=5)
                await asyncio.sleep(2)

                soup = BeautifulSoup(self._driver.page_source, 'html.parser')
                product_items = soup.find_all('div', {'class': ['product-card', 'product-item']}) or \
                                soup.find_all('li', {'class': ['product-item']}) or \
                                soup.find_all('div', {'data-testid': 'product-card'})

                for item in product_items:
                    try:
                        product_info = await self._extract_product_info(item)
                        if not product_info:
                            continue

                        # Simple matching logic - check if title contains model or sku
                        title = product_info.get('product_name', '').lower()
                        model_match = model and model.lower() in title
                        sku_match = sku and str(sku).lower() in title
                        brand_match = brand and brand.lower() in title

                        if model_match or sku_match or brand_match:
                            self._logger.info(f"Found matching product: {product_info['product_name']}")
                            
                            # Update DataFrame with product info
                            for key, value in product_info.items():
                                if key in self.data.columns:
                                    self.data.loc[idx, key] = value
                                else:
                                    self.data.at[idx, key] = value
                            
                            self.data.loc[idx, 'enabled'] = True
                            return row
                    except Exception as e:
                        self._logger.warning(f"Error processing product: {e}")

                self._logger.warning(f"No matching product found for {brand} {model} / {sku}")
                return row

            except Exception as exc:
                self._logger.error(f"Error during product search for {brand} {model}: {exc}")
                return row

    def column_exists(self, column: str, default_val: Any = None):
        """Check if column exists in DataFrame, create if not."""
        if column not in self.data.columns:
            self._logger.warning(f"Column {column} does not exist in the Dataframe")
            self.data[column] = default_val
            return False
        return True

    async def product(self):
        """Extract basic product information from Lowes using Selenium."""
        # Ensure required columns exist in the DataFrame
        self.column_exists('model')
        self.column_exists('brand')
        self.column_exists('sku')
        self.column_exists('product_name')
        self.column_exists('image_url')
        self.column_exists('price')
        self.column_exists('url')
        self.column_exists('enabled', False)

        # Set headless to True for production
        self.headless = True
        self.as_mobile = False

        # Initialize Selenium driver
        if not self._driver:
            await self.get_driver()

        # Create tasks to process each row in the DataFrame
        tasks = [
            self._product_info_selenium(idx, row)
            for idx, row in self.data.iterrows()
        ]

        # Process tasks concurrently
        await self._processing_tasks(tasks)

        # Add origin column
        self.data['origin'] = 'lowes'

        # Close Selenium driver after completing all tasks
        self.close_driver()

        # Return the updated DataFrame
        return self.data

    async def top_reviewed_products(self, brand: str, top_n: int = 3, **kwargs):
        """
        Busca productos por brand y devuelve un DataFrame con los top N productos con más reviews.
        Incluye: nombre, precio, url, imagen, sku, cantidad de reviews y rating.
        Usa los selectores reales del HTML de Lowes.
        """
        import re
        from bs4 import BeautifulSoup
        import pandas as pd
        self.headless = False
        self.as_mobile = False
        # Usar undetected_chromedriver para evadir detección de bot
        self.use_undetected = True
        url = self._get_search_url(brand, "")
        if not self._driver:
            await self.get_driver()
        # Paso 1: Ir a la home de Lowes
        await self.get_page("https://www.lowes.com/")
        await asyncio.sleep(2)
        # Paso 2: Ir al search
        await self.get_page(url)
        await asyncio.sleep(2)
        self._execute_scroll(scroll_pause_time=2.0, max_scrolls=3)
        await asyncio.sleep(1)
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        product_cards = soup.select('div[data-selector="prd-description-holder"]')
        results = []
        for card in product_cards:
            try:
                # Enlace y SKU
                a = card.select_one('h3 > a')
                url_ = a['href'] if a and a.has_attr('href') else None
                sku = None
                if url_:
                    match = re.search(r'/([0-9]+)$', url_)
                    if match:
                        sku = match.group(1)
                    url_ = f"https://www.lowes.com{url_}"
                # Nombre
                name_span = card.select_one('span.description-spn')
                product_name = name_span.text.strip() if name_span else None
                # Marca
                brand_span = card.select_one('span[data-selector="splp-prd-brd-nm"]')
                brand_val = brand_span.text.strip().replace('\xa0', ' ').replace('\n', '').strip() if brand_span else None
                # Solo incluir productos cuya brand coincida exactamente
                if not (brand_val and brand.lower() in brand_val.lower()):
                    continue
                # Imagen (nuevo selector)
                image_url = None
                parent_card = card.find_parent('div', attrs={'data-selector': 'splp-prd-crd'})
                if parent_card:
                    img_tag = parent_card.find('img', attrs={'data-selector': 'splp-prd-img-org'})
                    if img_tag and img_tag.has_attr('src'):
                        image_url = img_tag['src']
                # fallback antiguo
                if not image_url:
                    img_tag = card.find('img')
                    if img_tag and img_tag.has_attr('src'):
                        image_url = img_tag['src']
                # Precio (nuevo selector)
                price = None
                price_div = card.find('div', attrs={'data-selector': 'splp-prd-act-$'})
                if price_div and price_div.has_attr('aria-label'):
                    label = price_div['aria-label']
                    if '$' in label:
                        price = label.split('$', 1)[1].strip()
                    else:
                        price = label.strip()
                # fallback antiguo
                if not price:
                    price_holder = card.find_next('div', attrs={'data-selector': re.compile(r'splp-prd-s')})
                    if price_holder:
                        price_span = price_holder.find('span', class_=re.compile(r'mti-price'))
                        if price_span:
                            price = price_span.text.strip()
                # Rating y reviews (igual que antes)
                rating = None
                rating_count = None
                rating_holder = card.find_next('div', attrs={'data-selector': re.compile(r'prd-ratings-holder')})
                if rating_holder:
                    h6 = rating_holder.find('h6')
                    if h6:
                        try:
                            rating = float(h6.text.strip())
                        except Exception:
                            rating = None
                    rating_span = rating_holder.find('span', class_='rating-count')
                    if rating_span:
                        try:
                            rating_count = int(rating_span.text.strip().replace(',', ''))
                        except Exception:
                            rating_count = None
                if rating_count is None:
                    rating_span = card.find('span', class_='rating-count')
                    if rating_span:
                        try:
                            rating_count = int(rating_span.text.strip().replace(',', ''))
                        except Exception:
                            rating_count = None
                results.append({
                    'product_name': product_name,
                    'brand': brand_val,
                    'price': price,
                    'url': url_,
                    'image_url': image_url,
                    'sku': sku,
                    'num_reviews': rating_count,
                    'rating': rating
                })
            except Exception as e:
                self._logger.warning(f"Error parsing product card: {e}")
        # Ordenar por num_reviews descendente y devolver top_n
        results = [r for r in results if r['num_reviews'] is not None]
        results.sort(key=lambda x: x['num_reviews'], reverse=True)
        top_results = results[:top_n]
        df = pd.DataFrame(top_results)
        self.close_driver()
        return df

    async def top_reviewed(self):
        """
        Wrapper para top_reviewed_products para integrarlo con el sistema de type.
        Permite llamarlo como type='top_reviewed'.
        """
        brand = self.brand
        top_n = self.top_n
        if not brand:
            raise ConfigError("brand is required for top_reviewed")
        return await self.top_reviewed_products(brand=brand, top_n=top_n)

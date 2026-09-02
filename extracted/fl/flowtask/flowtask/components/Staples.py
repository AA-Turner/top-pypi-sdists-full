import asyncio
import aiohttp
import json
import re
import os
import ssl
import certifi
import pandas as pd
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from navconfig.logging import logging
from ..interfaces.flow import FlowComponent
from ..interfaces import HTTPService, SeleniumService
from ..exceptions import (
    ConfigError,
    ComponentError,
    NotSupported
)


class Staples(FlowComponent, SeleniumService, HTTPService):
    """
    Staples Component.
    
    Consumes the api.staples.ca REST API for extracting product availability.
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: callable = None,
        stat: callable = None,
        **kwargs,
    ):
        self._fn = kwargs.pop('type', 'availability')
        self.market = (kwargs.get('market') or '').strip().upper()
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self.task_parts: int = kwargs.get('task_parts', 10)
        # Storage parameters
        self.use_storage: bool = kwargs.get('use_storage', False)
        self.storage_path: str = kwargs.get('storage_path')
        if self.use_storage and not self.storage_path:
            raise ConfigError(
                "Staples: storage_path is required when use_storage is True"
            )
        if not self._fn:
            raise ConfigError(
                "Staples: require a `type` Function to be called, ex: availability"
            )
        super(Staples, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # Force paid proxy by default (consistent with BestBuy)
        self._free_proxy = False
        
        # Headers specifically for Staples API
        self.headers = {
            "Origin": "https://www.staples.ca",
            "Referer": "https://www.staples.ca/",
            "Accept": "application/json, text/plain, */*",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
            "Content-Type": "application/json",
            **self.headers
        }
        self.semaphore = asyncio.Semaphore(10)

    async def start(self, **kwargs):
        await super(Staples, self).start(**kwargs)
        if self.previous:
            self.data = self.input
    
    async def availability(self):
        """
        Check availability for products in self.data.
        """
        if 'checked' not in self.data.columns:
            self.data['checked'] = False

        tasks = []
        for idx, row in self.data.iterrows():
            tasks.append(self._product_availability(idx, row))
        await asyncio.gather(*tasks)
        return self.data

    async def _product_availability(self, idx, row):
        """
        Row method for checking product availability.
        """
        async with self.semaphore:
            # Optimization: check if row was already processed
            if self.data.at[idx, 'checked']:
                return

            sku = row.get('sku')
            postal_code = row.get('zipcode')
            location_code = row.get('location_code')
            state_code = row.get('state_code')
            country = row.get('country')

            if not sku or not postal_code:
                self._logger.warning(f"Row {idx}: Missing SKU or Zipcode.")
                self.data.at[idx, 'checked'] = True # Mark as checked to skip invalid rows next time?
                return

            if self.market in {"US", "CA"}:
                is_us = self.market == "US"
            else:
                is_us = False
                if country and str(country).upper() == "US":
                    is_us = True
                elif state_code and postal_code:
                    postal_str = str(postal_code).strip()
                    if postal_str.isdigit() and len(postal_str) == 5:
                        is_us = True

            if is_us:
                url = "https://www.staples.com/cc/api/omni/pickupinstore"
                payload = {
                    "itemIds": [str(sku)],
                    "searchParam": str(postal_code),
                    "radius": "100",
                    "tenantId": "StaplesDotCom",
                    "locale": "en-US",
                    "immediatePickupOnly": True,
                    "isSTS": False,
                    "action": "changeStore",
                    "yourStore": {"storeNumber": str(location_code)} if location_code else {"storeNumber": ""},
                    "pickStore": "",
                    "zipCode": str(postal_code),
                    "city": row.get('city'),
                    "state": state_code
                }
                request_headers = {
                    **self.headers,
                    "Origin": "https://www.staples.com",
                    "Referer": "https://www.staples.com/"
                }
            else:
                url = "https://api.staples.ca/ecommerce/inventory/v2.0/request"
            
                # Determine if Store Availability or Zipcode Availability
                if location_code:
                    # Per-store availability
                    payload = {
                        "locale": "en-CA",
                        "store_number": str(location_code),
                        "postal_code": postal_code,
                        "items": [
                            {
                                "sku": str(sku),
                                "quantity": 1000
                            }
                        ],
                        "location": "PickInStore"
                    }
                else:
                    # Per-zipcode availability
                    payload = {
                        "locale": "en-CA",
                        "postal_code": postal_code,
                        "items": [
                            {
                                "sku": str(sku),
                                "quantity": 1000,
                                "is_dropship": True
                            }
                        ],
                        "location": postal_code
                    }
                request_headers = self.headers

            try:
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                async with aiohttp.ClientSession(headers=request_headers) as session:
                    async with session.post(url, json=payload, ssl=ssl_context) as response:
                        raw_text = await response.text()
                        print(f"[Staples.availability] request_payload={payload}")
                        print(f"[Staples.availability] response_status={response.status}")
                        print(f"[Staples.availability] response_raw={raw_text}")
                        if response.status == 200:
                            try:
                                data = json.loads(raw_text)
                            except json.JSONDecodeError:
                                self._logger.error(f"Row {idx}: Response is not JSON.")
                                return
                            if data.get("success"):
                                if is_us:
                                    self._parse_availability_response_us(idx, data, sku, location_code)
                                else:
                                    availability = data.get("availability")
                                    products = {}
                                    if isinstance(availability, dict):
                                        products = availability.get(str(sku), {}) or {}
                                    if location_code and isinstance(products, dict) and not products:
                                        # Fallback to zipcode availability if store map is empty
                                        fallback_payload = {
                                            "locale": "en-CA",
                                            "postal_code": postal_code,
                                            "items": [
                                                {
                                                    "sku": str(sku),
                                                    "quantity": 1000,
                                                    "is_dropship": True
                                                }
                                            ],
                                            "location": postal_code
                                        }
                                        async with session.post(url, json=fallback_payload, ssl=ssl_context) as fb_response:
                                            fb_raw_text = await fb_response.text()
                                            print(f"[Staples.availability] fallback_payload={fallback_payload}")
                                            print(f"[Staples.availability] fallback_status={fb_response.status}")
                                            print(f"[Staples.availability] fallback_raw={fb_raw_text}")
                                            if fb_response.status == 200:
                                                try:
                                                    fb_data = json.loads(fb_raw_text)
                                                except json.JSONDecodeError:
                                                    self._logger.error(f"Row {idx}: Fallback response is not JSON.")
                                                    return
                                                if fb_data.get("success"):
                                                    self._parse_availability_response(idx, fb_data, sku, None)
                                                else:
                                                    self._logger.warning(
                                                        f"Row {idx}: Fallback request not successful. Response: {fb_data}"
                                                    )
                                            else:
                                                self._logger.error(
                                                    f"Row {idx}: Fallback HTTP {fb_response.status} - {await fb_response.text()}"
                                                )
                                    else:
                                        self._parse_availability_response(idx, data, sku, location_code)
                            else:
                                self._logger.warning(f"Row {idx}: Request not successful. Response: {data}")
                        else:
                            self._logger.error(f"Row {idx}: HTTP {response.status} - {await response.text()}")
            except Exception as e:
                self._logger.error(f"Row {idx}: Error requesting availability: {e}")

    def _parse_availability_response(self, idx, data, target_sku, location_code=None):
        """
        Parse the JSON response and update the DataFrame.
        """
        availability = data.get("availability")
        
        if location_code:
            # Per-store response structure: availability -> SKU -> StoreID -> details
            # { "availability": { "2791993": { "19": { ... }, "155": { ... } } } }
            
            # We want the specific store requested, or maybe details on "yourStore"?
            # User example: response includes "yourStore": true/false.
            # We will update with details of the requested store if present, or just the raw data.
            # Let's extract specific fields for the requested store.
            
            products = availability.get(str(target_sku), {}) if isinstance(availability, dict) else {}
            
            # Optimization: Update ALL stores present in the response
            for resp_store_id, store_details in products.items():
                # Find rows matching this sku and store_id
                # Note: location_code in DF might be different type (int/str), convert for comparison
                matches = self.data[
                    (self.data['sku'].astype(str) == str(target_sku)) &
                    (self.data['location_code'].astype(str) == str(resp_store_id))
                ]
                
                for match_idx in matches.index:
                    if self.data.at[match_idx, 'checked']:
                        continue
                        
                    self.data.at[match_idx, 'available_quantity'] = store_details.get('availableqty')
                    self.data.at[match_idx, 'delivery_message'] = store_details.get('deliveryMessage')
                    self.data.at[match_idx, 'delivery_type'] = store_details.get('deliveryType')
                    self.data.at[match_idx, 'raw_availability'] = json.dumps(store_details)
                    self.data.at[match_idx, 'checked'] = True
                    self._logger.info(f"Updated Store {resp_store_id} for SKU {target_sku} (Row {match_idx})")

            # Ensure the current row is marked checked even if it wasn't in response (avoids infinite loops if store missing)
            self.data.at[idx, 'checked'] = True
        else:
            # Per-zipcode response structure: availability -> list of objects
            # [ { "sku": "...", "available_quantity": 376, ... } ]
            if isinstance(availability, list):
                for item in availability:
                    if str(item.get('sku')) == str(target_sku):
                        self.data.at[idx, 'available_quantity'] = item.get('available_quantity')
                        self.data.at[idx, 'min_delivery_date'] = item.get('min_delivery_date')
                        self.data.at[idx, 'max_delivery_date'] = item.get('max_delivery_date')
                        self.data.at[idx, 'is_dropship'] = item.get('is_dropship')
                        self.data.at[idx, 'raw_availability'] = json.dumps(item)
                        break
            self.data.at[idx, 'checked'] = True

    def _parse_availability_response_us(self, idx, data, target_sku, location_code=None):
        """
        Parse the Staples US pickupinstore response and update the DataFrame.
        """
        details = data.get("pickInStoreDetails") or []
        target_sku_str = str(target_sku)
        matched = False

        for detail in details:
            item = detail.get("item") or {}
            if str(item.get("itemId")) != target_sku_str:
                continue

            stores = detail.get("store") or []
            if location_code:
                for store_details in stores:
                    if str(store_details.get("storeNumber")) != str(location_code):
                        continue
                    matches = self.data[
                        (self.data['sku'].astype(str) == target_sku_str) &
                        (self.data['location_code'].astype(str) == str(location_code))
                    ]
                    for match_idx in matches.index:
                        if self.data.at[match_idx, 'checked']:
                            continue
                        self.data.at[match_idx, 'available_quantity'] = store_details.get('availableqty')
                        self.data.at[match_idx, 'delivery_message'] = store_details.get('deliveryMessage')
                        self.data.at[match_idx, 'delivery_type'] = store_details.get('deliveryType')
                        self.data.at[match_idx, 'raw_availability'] = json.dumps(store_details)
                        self.data.at[match_idx, 'checked'] = True
                        self._logger.info(
                            f"Updated Store {location_code} for SKU {target_sku_str} (Row {match_idx})"
                        )
                    matched = True
            else:
                if stores:
                    store_details = stores[0]
                    self.data.at[idx, 'available_quantity'] = store_details.get('availableqty')
                    self.data.at[idx, 'delivery_message'] = store_details.get('deliveryMessage')
                    self.data.at[idx, 'delivery_type'] = store_details.get('deliveryType')
                    self.data.at[idx, 'raw_availability'] = json.dumps(store_details)
                    matched = True
            break

        self.data.at[idx, 'checked'] = True
        if not matched:
            self._logger.warning(f"Row {idx}: No matching US store data for SKU {target_sku_str}.")

    async def stores(self):
        """
        Get stores around a location.
        """
        tasks = []
        for idx, row in self.data.iterrows():
            tasks.append(self._get_stores(idx, row))
        await asyncio.gather(*tasks)
        return self.data

    async def _get_stores(self, idx, row):
        """
        Row method for getting stores.
        """
        async with self.semaphore:
            lat = row.get('latitude')
            lng = row.get('longitude')
            country = row.get('country', 'CA')
            rnum = row.get('rnum', 8)

            if not lat or not lng:
                self._logger.warning(f"Row {idx}: Missing latitude or longitude.")
                return

            url = f"https://api.stores.staples.ca/api/locations?lat={lat}&lng={lng}&rnum={rnum}&country={country}"

            try:
                # Stores API uses GET and likely different headers/no headers or standard ones
                # The user provided headers for availability. Let's see if we need them here.
                # Usually GET requests are simpler. User didn't specify special headers for GET stores,
                # but "Headers:" block in prompt was at the top.
                # Let's use the same headers but ensure Method is GET.

                ssl_context = ssl.create_default_context(cafile=certifi.where())
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(url, ssl=ssl_context) as response:
                        if response.status == 200:
                            data = await response.json()
                            # Result is a list of store objects directly? OR wrapped?
                            # User example: "Result: a list of store objects: { ... }" (shows a single object inside verification?)
                            # Wait, the user example shows a SINGLE object.
                            # "Result: a list of store objects:" then code block shows ONE object.
                            # Usually APIs return a list [ {}, {} ].
                            # If data is a list, we accept it.

                            self.data.at[idx, 'stores'] = json.dumps(data)
                            self.data.at[idx, 'stores_count'] = len(data) if isinstance(data, list) else 0
                        else:
                            self._logger.error(f"Row {idx}: HTTP {response.status} - {await response.text()}")
            except Exception as e:
                self._logger.error(f"Row {idx}: Error requesting stores: {e}")

    def _clean_model(self, model: str) -> str:
        """Clean model string removing invisible Unicode characters."""
        if not model:
            return ""
        raw_model = str(model).strip()
        # Remove zero-width characters and other invisible Unicode
        raw_model = re.sub(r'[\u200B-\u200D\uFEFF\u202A-\u202E\u00AD]', '', raw_model)
        # Remove any non-printable ASCII characters
        raw_model = ''.join(char for char in raw_model if char.isprintable())
        return raw_model.strip()

    def _get_search_url(self, model: str) -> str:
        """Build the Staples.com search URL for a given model."""
        # Clean the model string
        clean_model = self._clean_model(model).lower()
        base_url = "https://www.staples.com"
        if self.market == "CA":
            base_url = "https://www.staples.ca"
            url = f"{base_url}/search?query={quote(clean_model)}"
            self._logger.debug(f"Search URL: {url}")
            return url
        # First part: replace dashes with +
        search_part = clean_model.replace('-', '+')
        # Second part (directory_): keep dashes
        directory_part = clean_model
        url = f"{base_url}/{search_part}/directory_{directory_part}"
        self._logger.debug(f"Search URL: {url}")
        return url

    def _parse_price(self, text):
        """Returns the first numeric price found as float (without $ or commas)."""
        if not text:
            return None
        s = str(text).replace('\xa0', ' ')
        m = re.search(r'(\d[\d,]*\.?\d*)', s)
        if not m:
            return None
        try:
            return float(m.group(1).replace(',', ''))
        except ValueError:
            return None

    def _clean_image_url(self, url: str) -> str:
        """Clean and normalize the image URL from Staples."""
        if not url:
            return None
        s = str(url).strip()
        # If it comes as srcset, take the first URL
        s = s.split(',')[0].strip().split(' ')[0]
        return s or None

    def _is_product_detail_page(self, soup: BeautifulSoup) -> bool:
        """Check if the current page is a product detail page (PDP)."""
        # Check for PDP-specific elements using multiple selectors
        pdp_indicators = [
            'h1#product_title',
            'h1.product-info-ux2dot0__product_title',
            'div#product_Details',
            'div.product-info-ux2dot0__item_models',
            'div.price-info__price_container_sku',
            'div#image_gallery_container'
        ]
        for selector in pdp_indicators:
            if soup.select_one(selector):
                return True
        return False

    def _extract_from_pdp(self, soup: BeautifulSoup, current_url: str) -> dict:
        """Extract product information from a Product Detail Page (PDP)."""
        result = {
            'sku': None,
            'url': current_url,
            'image_url': None,
            'product_name': None,
            'price': None,
            'avg_rating': None,
            'num_reviews': None,
            'page_model': None,
        }

        try:
            # Extract product name - multiple selectors for different page versions
            title_selectors = [
                'h1#product_title',
                'h1.product-info-ux2dot0__product_title',
                'h1.product-title'
            ]
            for selector in title_selectors:
                title_element = soup.select_one(selector)
                if title_element:
                    result['product_name'] = title_element.get_text(strip=True)
                    break

            # Extract Item (SKU) from span#item_number
            item_element = soup.select_one('span#item_number')
            if item_element:
                text = item_element.get_text(strip=True)
                m = re.search(r'Item\s*#?:?\s*(\d+)', text)
                if m:
                    result['sku'] = m.group(1)

            # Extract Model from span#manufacturer_number
            model_element = soup.select_one('span#manufacturer_number')
            if model_element:
                text = model_element.get_text(strip=True)
                m = re.search(r'Model\s*#?:?\s*(\S+)', text)
                if m:
                    result['page_model'] = self._clean_model(m.group(1))

            # Fallback: try extracting from product-info-ux2dot0__item_models
            if not result['sku'] or not result['page_model']:
                info_div = soup.select_one('div.product-info-ux2dot0__item_models, div#product_Details')
                if info_div:
                    text = info_div.get_text()
                    if not result['sku']:
                        m = re.search(r'Item\s*#?:?\s*(\d+)', text)
                        if m:
                            result['sku'] = m.group(1)
                    if not result['page_model']:
                        m = re.search(r'Model\s*#?:?\s*(\S+)', text)
                        if m:
                            result['page_model'] = self._clean_model(m.group(1))

            # Extract price from price-info__final_price_sku
            price_selectors = [
                'div.price-info__final_price_sku',
                'div.price-info__final_price',
                'div.price-info__price_section'
            ]
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    text = price_elem.get_text(strip=True)
                    price = self._parse_price(text)
                    if price:
                        result['price'] = price
                        break

            # Extract rating from div.sc-mad84n-1 or aria-label
            rating_elem = soup.select_one('div.sc-mad84n-1')
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                try:
                    result['avg_rating'] = float(rating_text)
                except ValueError:
                    pass

            # Fallback: extract rating from aria-label
            if not result['avg_rating']:
                rating_container = soup.select_one('div[aria-label*="Rated"]')
                if rating_container:
                    aria_label = rating_container.get('aria-label', '')
                    m = re.search(r'Rated\s+([\d.]+)', aria_label)
                    if m:
                        try:
                            result['avg_rating'] = float(m.group(1))
                        except ValueError:
                            pass

            # Extract review count from a.sc-mad84n-2 or aria-label
            review_elem = soup.select_one('a.sc-mad84n-2')
            if review_elem:
                # Try aria-label first
                aria_label = review_elem.get('aria-label', '')
                m = re.search(r'([\d,]+)\s*reviews?', aria_label, re.IGNORECASE)
                if m:
                    result['num_reviews'] = int(m.group(1).replace(',', ''))
                else:
                    # Try text content
                    text = review_elem.get_text(strip=True)
                    m = re.search(r'([\d,]+)', text)
                    if m:
                        result['num_reviews'] = int(m.group(1).replace(',', ''))

            # Extract image URL from image gallery
            image_selectors = [
                'div#image_gallery_container img',
                'div.image_gallery_slider img',
                'div.image-gallery-ux2dot0__image_element_wrapper img'
            ]
            for selector in image_selectors:
                image_element = soup.select_one(selector)
                if image_element:
                    raw_img = (
                        image_element.get('srcset', '').split(',')[0].split(' ')[0] or
                        image_element.get('src') or
                        image_element.get('data-srcset', '').split(',')[0].split(' ')[0]
                    )
                    if raw_img:
                        result['image_url'] = self._clean_image_url(raw_img)
                        break

            self._logger.debug(f"PDP extraction result: {result}")

        except Exception as e:
            self._logger.warning(f"Error extracting from PDP: {e}")

        return result

    def _extract_from_pdp_ca(self, soup: BeautifulSoup, current_url: str) -> dict:
        """Extract product information from a Staples.ca PDP."""
        result = {
            'sku': None,
            'url': current_url,
            'image_url': None,
            'product_name': None,
            'price': None,
            'avg_rating': None,
            'num_reviews': None,
            'page_model': None,
        }

        try:
            canonical = soup.select_one('link[rel="canonical"]')
            if canonical and canonical.get('href'):
                result['url'] = canonical.get('href')

            # SKU from /products/<sku>-...
            m = re.search(r'/products/(\d+)', result['url'])
            if m:
                result['sku'] = m.group(1)

            og_title = soup.select_one('meta[property="og:title"]')
            if og_title and og_title.get('content'):
                result['product_name'] = og_title.get('content').strip()
            else:
                title_elem = soup.select_one('h1')
                if title_elem:
                    result['product_name'] = title_elem.get_text(strip=True)

            og_image = soup.select_one('meta[property="og:image"]')
            if og_image and og_image.get('content'):
                result['image_url'] = self._clean_image_url(og_image.get('content'))

            price_elem = soup.select_one('span.money')
            if price_elem:
                result['price'] = self._parse_price(price_elem.get_text(strip=True))

            # JSON-LD for rating/reviews
            for script in soup.select('script[type="application/ld+json"]'):
                try:
                    data = json.loads(script.get_text(strip=True))
                except json.JSONDecodeError:
                    continue
                nodes = data if isinstance(data, list) else [data]
                for node in nodes:
                    aggregate = node.get('aggregateRating') if isinstance(node, dict) else None
                    if not aggregate:
                        continue
                    rating_value = aggregate.get('ratingValue')
                    review_count = aggregate.get('reviewCount')
                    if rating_value is not None and result['avg_rating'] is None:
                        try:
                            result['avg_rating'] = float(rating_value)
                        except (TypeError, ValueError):
                            pass
                    if review_count is not None and result['num_reviews'] is None:
                        try:
                            result['num_reviews'] = int(str(review_count).replace(',', ''))
                        except (TypeError, ValueError):
                            pass
                if result['avg_rating'] is not None or result['num_reviews'] is not None:
                    break

        except Exception as e:
            self._logger.warning(f"Error extracting from CA PDP: {e}")

        return result

    def _extract_rating_from_stars(self, rating_wrapper) -> tuple:
        """
        Extract rating value and review count from the rating wrapper element.
        Returns (avg_rating, num_reviews).
        """
        avg_rating = None
        num_reviews = None

        try:
            if not rating_wrapper:
                return avg_rating, num_reviews

            # Count filled stars by looking at the star SVGs
            # Full stars have a simple fill, partial stars have a gradient
            star_containers = rating_wrapper.select('div.sc-18w9h10-0')
            filled_count = 0
            partial_fill = 0

            for container in star_containers:
                # Check if the star is filled by looking at the overlay div
                overlay = container.select_one('div.sc-fpni1r-1')
                if overlay:
                    # Check the class - ckkfUc means empty, bzERoI means partial
                    classes = overlay.get('class', [])
                    if 'ckkfUc' in classes:
                        filled_count += 1
                    elif 'bzERoI' in classes:
                        # Partial star - estimate 0.5
                        partial_fill = 0.5

            avg_rating = filled_count + partial_fill if filled_count > 0 else None

            # Extract review count from the review link
            review_link = rating_wrapper.select_one('a.sc-mad84n-2, a[href*="scrollToReviews"]')
            if review_link:
                review_text = review_link.get_text(strip=True)
                m = re.search(r'(\d[\d,]*)', review_text)
                if m:
                    num_reviews = int(m.group(1).replace(',', ''))

        except Exception as e:
            self._logger.debug(f"Error extracting rating: {e}")

        return avg_rating, num_reviews

    async def _product_info(self, idx, row):
        """
        Extract product information from Staples.ca search results by model.
        """
        async with self.semaphore:
            model = row.get('model')
            brand = row.get('brand') or getattr(self, 'brand', None)

            if not model:
                self._logger.warning(f"Row {idx}: Missing model number.")
                return row

            # Clean the model
            model = self._clean_model(model)
            if not model:
                self._logger.warning(f"Row {idx}: Model is empty after cleaning.")
                return row

            self._logger.info(f"Processing product - Brand: {brand}, Model: {model}")

            if not self._driver:
                await self.get_driver()

            try:
                url = self._get_search_url(model)
                await self.get_page(url)
                await asyncio.sleep(3)  # Increased wait time for page load

                # Log the current URL after redirect
                current_url = self._driver.current_url
                self._logger.debug(f"Current URL after load: {current_url}")

                # Scroll to load all products
                self._execute_scroll(scroll_pause_time=2.0, max_scrolls=3)
                await asyncio.sleep(1)

                soup = BeautifulSoup(self._driver.page_source, 'html.parser')

                if self.market == "CA":
                    try:
                        WebDriverWait(self._driver, 15).until(
                            lambda d: d.find_elements(
                                By.CSS_SELECTOR,
                                "div.ais-hits-item a.product-thumbnail__title[href], "
                                "div.ais-hits-item a.product-link[href], "
                                "div.product-thumbnail a.product-thumbnail__title[href], "
                                "div.product-thumbnail a.product-link[href]"
                            )
                        )
                    except Exception:
                        pass
                    soup = BeautifulSoup(self._driver.page_source, 'html.parser')
                    first_product = soup.select_one(
                        'div.ais-hits-item a.product-thumbnail__title[href], '
                        'div.ais-hits-item a.product-link[href], '
                        'div.product-thumbnail a.product-thumbnail__title[href], '
                        'div.product-thumbnail a.product-link[href]'
                    )
                    href = first_product.get('href', '').strip() if first_product else ''
                    if not href:
                        # Fallback: parse first link from raw HTML
                        m = re.search(
                            r'<a[^>]*class="[^"]*product-thumbnail__title[^"]*"[^>]*href="([^"]+)"',
                            self._driver.page_source,
                            re.IGNORECASE
                        )
                        if not m:
                            m = re.search(
                                r'<a[^>]*class="[^"]*product-link[^"]*"[^>]*href="([^"]+)"',
                                self._driver.page_source,
                                re.IGNORECASE
                            )
                        href = m.group(1).strip() if m else ''
                    if not href:
                        self._logger.warning(f"No search results found for model: {model}")
                        self.data.at[idx, 'enabled'] = False
                        return row
                    if not href:
                        self._logger.warning(f"Missing product URL for model: {model}")
                        self.data.at[idx, 'enabled'] = False
                        return row
                    product_url = f"https://www.staples.ca{href}" if href.startswith('/') else href

                    product_name = first_product.get_text(strip=True) if first_product else None
                    image_elem = None
                    if first_product:
                        container = first_product.find_parent('div', class_='product-thumbnail')
                        if container:
                            image_elem = container.select_one('img.product-thumbnail__image, img')
                    image_url = None
                    if image_elem:
                        image_url = self._clean_image_url(
                            image_elem.get('src') or image_elem.get('data-src') or image_elem.get('srcset')
                        )
                    if not product_name and image_elem:
                        product_name = image_elem.get('alt')

                    await self.get_page(product_url)
                    await asyncio.sleep(2)

                    pdp_soup = BeautifulSoup(self._driver.page_source, 'html.parser')
                    pdp_data = self._extract_from_pdp_ca(pdp_soup, self._driver.current_url)

                    self.data.at[idx, 'sku'] = pdp_data['sku'] or self.data.at[idx, 'sku']
                    self.data.at[idx, 'url'] = pdp_data['url'] or product_url
                    self.data.at[idx, 'image_url'] = pdp_data['image_url'] or image_url
                    self.data.at[idx, 'product_name'] = pdp_data['product_name'] or product_name
                    self.data.at[idx, 'price'] = pdp_data['price']
                    self.data.at[idx, 'avg_rating'] = pdp_data['avg_rating']
                    self.data.at[idx, 'num_reviews'] = pdp_data['num_reviews']
                    self.data.at[idx, 'enabled'] = True

                    if brand:
                        self.data.at[idx, 'brand'] = brand

                    self._logger.info(
                        f"Extracted from CA PDP - SKU: {self.data.at[idx, 'sku']}, "
                        f"Price: {pdp_data['price']}"
                    )
                    return row

                # Check if this is a PDP first
                is_pdp = self._is_product_detail_page(soup)
                self._logger.debug(f"Is PDP page: {is_pdp}")

                # Find all product tiles
                product_tiles = soup.select('div.standard-tile__standard_tile_container')
                self._logger.info(f"Found {len(product_tiles)} product tiles to analyze")

                # If this is a PDP, try extracting from it first, then fall back to tiles
                if is_pdp:
                    self._logger.info("Detected Product Detail Page (PDP) - extracting directly")
                    current_url = self._driver.current_url
                    pdp_data = self._extract_from_pdp(soup, current_url)

                    # Verify model matches if we got one from the page
                    page_model = pdp_data.get('page_model')
                    model_clean = model.lower()
                    model_match = True

                    if page_model:
                        page_model_clean = page_model.lower()
                        model_match = (
                            page_model_clean == model_clean or
                            page_model_clean.replace('-', '') == model_clean.replace('-', '') or
                            model_clean in page_model_clean or
                            page_model_clean in model_clean
                        )

                    if model_match and pdp_data.get('sku'):
                        self._logger.info(
                            f"PDP match found - Model: {page_model}, SKU: {pdp_data['sku']}"
                        )
                        self.data.at[idx, 'sku'] = pdp_data['sku']
                        self.data.at[idx, 'url'] = pdp_data['url']
                        self.data.at[idx, 'image_url'] = pdp_data['image_url']
                        self.data.at[idx, 'product_name'] = pdp_data['product_name']
                        self.data.at[idx, 'price'] = pdp_data['price']
                        self.data.at[idx, 'avg_rating'] = pdp_data['avg_rating']
                        self.data.at[idx, 'num_reviews'] = pdp_data['num_reviews']
                        self.data.at[idx, 'enabled'] = True

                        if brand:
                            self.data.at[idx, 'brand'] = brand

                        self._logger.info(
                            f"Extracted from PDP - SKU: {pdp_data['sku']}, "
                            f"Price: {pdp_data['price']}, Reviews: {pdp_data['num_reviews']}"
                        )
                        return row
                    else:
                        self._logger.warning(
                            f"PDP model mismatch - Expected: {model}, Found: {page_model}"
                        )

                for tile in product_tiles:
                    try:
                        # Extract model from tile
                        product_ids = tile.select('div.standard-tile__product_id')
                        tile_model = None
                        tile_sku = None

                        for pid in product_ids:
                            text = pid.get_text(strip=True)
                            if text.startswith('Model:'):
                                tile_model = text.replace('Model:', '').strip()
                            elif text.startswith('Item:'):
                                tile_sku = text.replace('Item:', '').strip()

                        # Check if this is the product we're looking for
                        model_match = False
                        if tile_model and model:
                            model_clean = self._clean_model(model).lower()
                            tile_model_clean = self._clean_model(tile_model).lower()
                            model_match = (
                                tile_model_clean == model_clean or
                                tile_model_clean.replace('-', '') == model_clean.replace('-', '') or
                                model_clean in tile_model_clean or
                                tile_model_clean in model_clean
                            )

                        if model_match:
                            self._logger.info(f"Found matching product - Model: {tile_model}, SKU: {tile_sku}")

                            # Extract product URL
                            product_link = tile.select_one('a.standard-tile__image_wrapper, a.standard-tile__title')
                            product_url = None
                            if product_link:
                                href = product_link.get('href', '')
                                if href:
                                    product_url = f"https://www.staples.com{href}" if href.startswith('/') else href

                            # Extract image
                            image_element = tile.select_one('img')
                            image_url = None
                            if image_element:
                                raw_img = (
                                    image_element.get('src') or
                                    image_element.get('srcset', '').split(',')[0].split(' ')[0] or
                                    image_element.get('data-srcset', '').split(',')[0].split(' ')[0]
                                )
                                image_url = self._clean_image_url(raw_img)

                            # Extract product name
                            title_element = tile.select_one('h2 a.standard-tile__title, a.standard-tile__title')
                            product_name = title_element.get_text(strip=True) if title_element else None

                            # Extract price
                            price_element = tile.select_one('div.standard-tile__final_price')
                            price = None
                            if price_element:
                                price = self._parse_price(price_element.get_text(strip=True))

                            # Extract rating and reviews
                            rating_wrapper = tile.select_one('div.standard-tile__rating_wrapper')
                            avg_rating, num_reviews = self._extract_rating_from_stars(rating_wrapper)

                            # Update the DataFrame
                            self.data.at[idx, 'sku'] = tile_sku
                            self.data.at[idx, 'url'] = product_url
                            self.data.at[idx, 'image_url'] = image_url
                            self.data.at[idx, 'product_name'] = product_name
                            self.data.at[idx, 'price'] = price
                            self.data.at[idx, 'avg_rating'] = avg_rating
                            self.data.at[idx, 'num_reviews'] = num_reviews
                            self.data.at[idx, 'enabled'] = True

                            if brand:
                                self.data.at[idx, 'brand'] = brand

                            self._logger.info(
                                f"Extracted - SKU: {tile_sku}, Price: {price}, "
                                f"Rating: {avg_rating}, Reviews: {num_reviews}"
                            )
                            return row

                    except Exception as e:
                        self._logger.warning(f"Error processing product tile: {e}")
                        continue

                self._logger.warning(f"No matching product found for model: {model}")
                self.data.at[idx, 'enabled'] = False
                return row

            except Exception as exc:
                self._logger.error(f"Error during product search for model {model}: {exc}")
                self.data.at[idx, 'enabled'] = False
                return row

    async def product(self):
        """
        Staples Product Information via web scraping.
        Searches for products by model number and extracts SKU, price, image, rating, etc.
        """
        # Ensure required columns exist
        for col in ['model', 'brand', 'sku', 'product_name', 'image_url',
                    'price', 'url', 'num_reviews', 'avg_rating', 'enabled']:
            if col not in self.data.columns:
                self.data[col] = None

        # Clean the model column to remove invisible Unicode characters
        if 'model' in self.data.columns:
            self.data['model'] = self.data['model'].apply(
                lambda x: self._clean_model(x) if pd.notna(x) else x
            )

        self.data['enabled'] = False

        # Set browser mode - ensure desktop view
        self.headless = True
        self.as_mobile = False
        self.window_size = (1920, 1080)  # Force desktop resolution

        # Initialize Selenium driver
        if not self._driver:
            await self.get_driver()

        # Process products SEQUENTIALLY (Selenium can only handle one page at a time)
        for idx, row in self.data.iterrows():
            await self._product_info(idx, row)

        # Add origin column
        self.data['origin'] = 'staples.ca' if self.market == "CA" else 'staples'

        # Close Selenium driver
        self.close_driver()

        return self.data

    async def product_search_ca(self):
        """
        Staples.ca search-only product lookup.
        Extracts SKU, URL, name, and image from the first search result.
        """
        # Ensure required columns exist
        for col in ['model', 'brand', 'sku', 'product_name', 'image_url', 'url', 'enabled']:
            if col not in self.data.columns:
                self.data[col] = None

        if 'model' in self.data.columns:
            self.data['model'] = self.data['model'].apply(
                lambda x: self._clean_model(x) if pd.notna(x) else x
            )

        self.data['enabled'] = False

        self.headless = True
        self.as_mobile = False
        self.window_size = (1920, 1080)

        for idx, row in self.data.iterrows():
            if self._driver:
                self.close_driver()
            await self.get_driver()
            model = row.get('model')
            brand = row.get('brand') or getattr(self, 'brand', None)
            if not model:
                self._logger.warning(f"Row {idx}: Missing model number.")
                continue
            model = self._clean_model(model)
            if not model:
                self._logger.warning(f"Row {idx}: Model is empty after cleaning.")
                continue

            # Go directly to search URL to avoid homepage blocking
            url = self._get_search_url(model)
            await self.get_page(url)
            await asyncio.sleep(3)
            self._execute_scroll(scroll_pause_time=2.0, max_scrolls=3)
            await asyncio.sleep(1)

            soup = BeautifulSoup(self._driver.page_source, 'html.parser')
            first_product = soup.select_one(
                'div.ais-hits-item a.product-thumbnail__title[href], '
                'div.ais-hits-item a.product-link[href], '
                'div.product-thumbnail a.product-thumbnail__title[href], '
                'div.product-thumbnail a.product-link[href]'
            )
            href = first_product.get('href', '').strip() if first_product else ''
            if not href:
                self._logger.warning(f"No search results found for model: {model}")
                continue

            product_url = f"https://www.staples.ca{href}" if href.startswith('/') else href

            product_name = first_product.get_text(strip=True) if first_product else None
            image_elem = None
            if first_product:
                container = first_product.find_parent('div', class_='product-thumbnail')
                if container:
                    image_elem = container.select_one('img.product-thumbnail__image, img')
            image_url = None
            if image_elem:
                image_url = self._clean_image_url(
                    image_elem.get('src') or image_elem.get('data-src') or image_elem.get('srcset')
                )
            if not product_name and image_elem:
                product_name = image_elem.get('alt')

            sku = None
            m = re.search(r'/products/(\d+)', product_url)
            if m:
                sku = m.group(1)

            self.data.at[idx, 'sku'] = sku
            self.data.at[idx, 'url'] = product_url
            self.data.at[idx, 'image_url'] = image_url
            self.data.at[idx, 'product_name'] = product_name
            self.data.at[idx, 'enabled'] = True
            if brand:
                self.data.at[idx, 'brand'] = brand

        self.data['origin'] = 'staples.ca'
        self.close_driver()
        return self.data

    async def product_pdp_ca(self):
        """
        Staples.ca PDP-only product lookup.
        Uses the URL already present in the data.
        """
        for col in ['url', 'sku', 'product_name', 'image_url', 'price', 'num_reviews', 'avg_rating', 'enabled']:
            if col not in self.data.columns:
                self.data[col] = None

        self.data['enabled'] = False

        self.headless = True
        self.as_mobile = False
        self.window_size = (1920, 1080)

        for idx, row in self.data.iterrows():
            if self._driver:
                self.close_driver()
            await self.get_driver()
            product_url = row.get('url')
            if not product_url:
                self._logger.warning(f"Row {idx}: Missing product URL.")
                continue

            await self.get_page(product_url)
            await asyncio.sleep(2)

            pdp_soup = BeautifulSoup(self._driver.page_source, 'html.parser')
            pdp_data = self._extract_from_pdp_ca(pdp_soup, self._driver.current_url)

            self.data.at[idx, 'sku'] = pdp_data['sku'] or self.data.at[idx, 'sku']
            self.data.at[idx, 'url'] = pdp_data['url'] or product_url
            self.data.at[idx, 'image_url'] = pdp_data['image_url'] or self.data.at[idx, 'image_url']
            self.data.at[idx, 'product_name'] = pdp_data['product_name'] or self.data.at[idx, 'product_name']
            self.data.at[idx, 'price'] = pdp_data['price']
            self.data.at[idx, 'avg_rating'] = pdp_data['avg_rating']
            self.data.at[idx, 'num_reviews'] = pdp_data['num_reviews']
            self.data.at[idx, 'enabled'] = True

        self.data['origin'] = 'staples.ca'
        self.close_driver()
        return self.data

    def _get_storage_file(self) -> str:
        """Get the storage file path for the current execution."""
        today = datetime.now().strftime('%Y%m%d')
        filename = f"staples_{self._fn}_{self._program}_{today}.csv"
        storage_dir = Path(self.storage_path)
        storage_dir.mkdir(parents=True, exist_ok=True)
        return str(storage_dir / filename)

    async def close(self, **_kwargs) -> bool:
        self.close_driver()
        return True

    def close_driver(self):
        """Close Selenium driver for this component."""
        if getattr(self, "_driver", None):
            try:
                self._driver.quit()
            except Exception as e:
                self._logger.warning(f"Error closing driver: {e}")
            finally:
                self._driver = None

    async def run(self):
        # Try to load from storage first
        if self.use_storage:
            storage_file = self._get_storage_file()
            if os.path.exists(storage_file):
                self._logger.info(
                    f"Found existing data file: {storage_file}. Using stored data."
                )
                try:
                    self._result = pd.read_csv(storage_file)
                    return self._result
                except Exception as e:
                    self._logger.error(f"Error loading storage file: {e}")
            else:
                self._logger.info(
                    f"No existing data file found. Will generate new file: {storage_file}"
                )

        # If no storage or error, proceed with normal execution
        fn = getattr(self, self._fn)
        result = None
        if not callable(fn):
            raise ComponentError(
                f"Staples: Function {self._fn} doesn't exists."
            )
        try:
            result = await fn()
            # Save to storage after successful execution
            if self.use_storage and result is not None and isinstance(result, pd.DataFrame):
                try:
                    storage_file = self._get_storage_file()
                    result.to_csv(storage_file, index=False)
                    self._logger.info(
                        f"Successfully saved data to: {storage_file}"
                    )
                except Exception as e:
                    self._logger.error(f"Error saving to storage: {e}")
        except (ComponentError, TimeoutError, NotSupported):
            raise
        except Exception as exc:
            raise ComponentError(
                f"Staples: Unknown Error: {exc}"
            ) from exc
        # Print results
        print(result)
        print("::: Printing Column Information === ")
        for column, t in result.dtypes.items():
            print(column, "->", t, "->", result[column].iloc[0])
        self._result = result
        return self._result

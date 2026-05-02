import asyncio
import contextlib
import base64
import re
import urllib
import struct
import pandas as pd
import orjson
from ..exceptions import DataNotFound, ComponentError
from .google import GoogleBase
import os
import time
import tempfile
import shutil
import aiofiles
from ..interfaces.selenium import SeleniumService


class GooglePlaces(GoogleBase):
    """
    GooglePlaces.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          GooglePlaces:
          # attributes here
        ```
    """
    _version = "1.0.0"
    _base_url: str = "https://maps.googleapis.com/maps/api/"

    async def run(self):
        """Run the Google Places API."""
        if 'place_id' not in self.data.columns:
            raise DataNotFound(
                "Missing 'place_id' column in the input DataFrame."
            )
        if self._type == 'rating_reviews':
            self.column_exists('rating')
            self.column_exists('reviews')
            self.column_exists('user_ratings_total')
            self.column_exists('name')
        elif self._type == 'traffic':
            # 'address_components', 'formatted_address', 'geometry', 'name',
            # 'place_id', 'types', 'vicinity', 'rating', 'rating_n',
            # 'current_popularity', 'popular_times', 'time_spent'
            self.column_exists('address_components')
            self.column_exists('formatted_address')
            self.column_exists('geometry')
            self.column_exists('name')
            self.column_exists('place_id')
            self.column_exists('types')
            self.column_exists('vicinity')
            self.column_exists('rating')
            self.column_exists('rating_n')
            self.column_exists('current_popularity')
            self.column_exists('popular_times')
            self.column_exists('popular_times')
            self.column_exists('traffic')
            self.column_exists('time_spent')
        elif self._type == 'add_cid':
            self.column_exists('place_id')
            self.column_exists('cid_decimal')
            self.column_exists('cid_hex')
            self.column_exists('location_hex')
            self.column_exists('full_hex_format')
            self.column_exists('maps_link')

        self._logger.notice(
            f"Google Places API: Looking for {len(self.data)} places."
        )
        return await super().run()

    async def rating_reviews(
        self,
        idx: int,
        row: pd.Series
    ):
        """Getting Place Reviews using the Google Places API.

        Args:
            idx: row index
            row: pandas row

        Returns:
            Review Information.


        Example:

        ```yaml
        GooglePlaces:
          type: traffic
          paid_proxy: true
        ```

    """
        url = self._base_url + 'place/details/json'
        # url = "https://places.googleapis.com/v1/places/{place_id}?"
        async with self.semaphore:
            place_id = row['place_id']
            if not place_id:
                return idx, None
            params = {
                "placeid": place_id,
                "fields": "rating,reviews,user_ratings_total,name",
                "key": self.api_key
            }
            self._logger.notice(
                f"Looking for {place_id}"
            )
            # url = url.format(place_id=place_id)
            session_args = self._get_session_args()
            response = await self._google_session(
                url=url,
                session_args=session_args,
                params=params,
                use_proxies=True
            )
            if not response:
                return idx, None
            place_info = response.get('result', {})
            self._counter += 1
            return idx, place_info

    async def add_cid(
        self,
        idx: int,
        row: pd.Series
    ):
        """
        Add CID information to the DataFrame using convert_place_id.

        Args:
            idx: row index
            row: pandas row

        Returns:
            Place information with CID details.
        """
        async with self.semaphore:
            place_id = row['place_id']
            if not place_id:
                return idx, None

            # existing method in GoogleBase
            result = self.convert_place_id(place_id)
            if "error" in result:
                # Decide how to handle errors, for now returning as is or could log
                self._logger.warning(f"Error converting {place_id}: {result['error']}")
                return idx, None

            self._counter += 1
            return idx, result

    async def traffic(
        self,
        idx: int,
        row: pd.Series
    ):
        """get the current status of popular times (Traffic).

        Args:
            idx: row index
            row: pandas row

        Returns:
            Place information with Traffic.
        """
        async with self.semaphore:
            place_id = row['place_id']
            if not place_id:
                return idx, None

            self._logger.notice(
                f"Looking for {place_id}"
            )

            # Let's fetch details first (lightweight) to get address/name, then search
            url = self._base_url + 'place/details/json'
            params = {
                "placeid": place_id,
                "key": self.api_key,
                "fields": "name,place_id,address_components,formatted_address,geometry,types,vicinity"
            }
            session_args = self._get_session_args()
            response = await self._google_session(
                url,
                session_args,
                params,
                use_proxies=True
            )

            if not response:
                return idx, None

            # extract lat and long from geometry:
            place_info = response.get('result', {})
            name = place_info.get('name')
            geometry = place_info.get('geometry', {})
            location = geometry.get('location', {})
            lat = location.get('lat')
            lng = location.get('lng')
            # extract formatted_address
            formatted_address = place_info.get('formatted_address', '')
            row['formatted_address'] = formatted_address
            row['latitude'] = lat
            row['longitude'] = lng
            row['name'] = name

            # extract cid from place_id
            cid = self.convert_place_id(place_id)
            if "error" in cid:
                self._logger.warning(
                    f"Error converting {place_id}: {cid['error']}"
                )
                return idx, None

            # cid decimal
            print(cid)
            # merge raw_data into current row:
            for k, v in cid.items():
                row[k] = v

            # Initialize Selenium Service for this request
            temp_dir = tempfile.mkdtemp()
            driver = None
            try:
                prefs = {
                    "download.default_directory": temp_dir,
                    "download.prompt_for_download": False,
                    "directory_upgrade": True,
                    "safebrowsing.enabled": True
                }

                # Start Selenium Service with persistent profile if configured
                async with SeleniumService(
                    browser='chrome',
                    prefs=prefs,
                    headless=True,
                    user_data_dir=self.chrome_user_data_dir  # Persistent Chrome profile
                ) as driver:
                    map_details = await self._make_google_search(row, driver, temp_dir)
                    if map_details:
                        # Popular times extraction
                        try:
                            self._get_populartimes(place_info, map_details)
                        except Exception as e:
                            self._logger.error(f"Error extracting popular times: {e}")

            except Exception as e:
                self._logger.error(f"Error in traffic search: {e}")
                map_details = None
            finally:
                # Cleanup temp dir
                try:
                    shutil.rmtree(temp_dir)
                except Exception:
                    pass

            # Formatting Traffic logic
            popular_times = place_info.get('popular_times')
            if popular_times is not None and isinstance(popular_times, list):
                popular_times = {str(item[0]): item[1] for item in popular_times}
                for k, v in popular_times.items():
                    new_dict = {}
                    for traffic in v:
                        hour = str(traffic[0])
                        new_dict[hour] = {
                            "human_hour": traffic[4],
                            "traffic": traffic[1],
                            "traffic_status": traffic[2]
                        }
                    popular_times[k] = new_dict
                place_info['popular_times'] = popular_times
                try:
                    place_info['traffic'] = self._convert_populartimes(
                        popular_times
                    )
                except Exception as e:
                    place_info['traffic'] = {}

            self._counter += 1
            return idx, place_info

    def index_get(self, array, *argv):
        """
        Safely navigate nested arrays/lists by indices.

        Args:
            array: The data array/list to navigate
            argv: Index integers for nested access

        Returns:
            The value at the specified nested index, or None if not found
        """
        try:
            for index in argv:
                if array is None:
                    return None
                array = array[index]
            return array
        except (IndexError, TypeError, KeyError):
            return None

    async def _selenium_search(self, url: str, driver, temp_dir: str) -> str:
        """
        Perform a search using the provided Selenium driver.
        Reads the downloaded file from temp_dir.
        """
        try:
            # Navigate using the provided driver
            print(f"[DEBUG] Navigating to URL: {url}")
            await asyncio.to_thread(driver.get, url)
            print(f"[DEBUG] Navigation completed")

            # DEBUG: Check page content after navigation
            page_source = await asyncio.to_thread(lambda: driver.page_source)
            page_title = await asyncio.to_thread(lambda: driver.title)
            current_url = await asyncio.to_thread(lambda: driver.current_url)

            print(f"[DEBUG] Page loaded:")
            print(f"  Title: {page_title}")
            print(f"  Current URL: {current_url}")
            print(f"  Page size: {len(page_source)} bytes")

            # Create permanent debug directory
            debug_dir = os.path.expanduser("~/flowtask_debug")
            os.makedirs(debug_dir, exist_ok=True)

            # Generate timestamp for unique filenames
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            # ALWAYS save HTML for inspection (not just on keywords)
            debug_html = os.path.join(debug_dir, f'page_{timestamp}.html')
            print(f"[DEBUG] Saving page HTML to: {debug_html}")
            with open(debug_html, 'w', encoding='utf-8') as f:
                f.write(page_source)
            print(f"[DEBUG] ✓ HTML saved successfully")

            # ALWAYS take screenshot
            try:
                screenshot_path = os.path.join(debug_dir, f'page_{timestamp}.png')
                print(f"[DEBUG] Taking screenshot to: {screenshot_path}")
                await asyncio.to_thread(driver.save_screenshot, screenshot_path)
                print(f"[DEBUG] ✓ Screenshot saved successfully")
            except Exception as e:
                print(f"[DEBUG] ✗ Could not save screenshot: {e}")

            # Check for 2FA/verification indicators
            verification_keywords = [
                'verify', 'verification', 'two-factor', '2fa',
                'security check', 'unusual activity', 'confirm your identity',
                'sign in', 'login', 'authenticate', 'captcha', 'robot'
            ]

            page_lower = page_source.lower()
            found_keywords = [kw for kw in verification_keywords if kw in page_lower]

            if found_keywords:
                print(f"[WARNING] ⚠️  Possible verification/login required!")
                print(f"[WARNING] Found keywords: {found_keywords}")
            else:
                print(f"[DEBUG] ✓ No verification keywords detected")

            # Check for common Google Maps elements
            maps_indicators = [
                'maps.google.com', 'google.com/maps',
                'ludocid=', 'popularTimesHistogram',
                'window.APP_INITIALIZATION_STATE'
            ]
            found_maps = [ind for ind in maps_indicators if ind in page_source]
            if found_maps:
                print(f"[DEBUG] ✓ Google Maps indicators found: {found_maps}")
            else:
                print(f"[WARNING] ⚠️  No Google Maps indicators found in page")

            print(f"[DEBUG] Files saved in: {debug_dir}")
            print(f"[DEBUG] You can inspect: ls -lh {debug_dir}")

            # Check if download started/finished
            downloaded_file = None
            start_time = time.time()
            while time.time() - start_time < 30:  # 30s timeout
                # This I/O is fast but technically blocking, ok to leave synchronous or wrap
                files = os.listdir(temp_dir)
                valid_files = [
                    f for f in files if not f.endswith('.crdownload') and not f.endswith('.tmp') and not f.startswith('.')
                ]
                if valid_files:
                    downloaded_file = os.path.join(temp_dir, valid_files[0])
                    await asyncio.sleep(1.0)
                    break
                await asyncio.sleep(0.5)

            if not downloaded_file:
                print(f"[DEBUG] No download triggered. Files in temp_dir: {os.listdir(temp_dir)}")
                raise ValueError("Download timeout: Google did not trigger file download.")

            async with aiofiles.open(downloaded_file, 'r', encoding='utf-8') as f:
                return await f.read()

        except Exception as e:
            self._logger.error(f"Selenium search error: {e}")
            raise

    async def _make_google_search(self, row: pd.Series, driver=None, temp_dir=None):
        """
        Make a Google Maps search request to get place details including popular times.

        Args:
            query_string: The address/name of the place to search for
            place_id: (Optional) Verify that place_id exists in the result

        Returns:
            Parsed JSON data from Google Maps or None if failed
            If place_id is provided, tries to return the specific node containing it.

        Raises:
            ValueError: If the request fails or response is empty
            ComponentError: If JSON parsing fails
        """
        formatted_address = row.get('formatted_address', '')
        name = row.get('name', '')
        address = f'{name}, {formatted_address}'
        lat = row.get('latitude')
        lng = row.get('longitude')

        pb_param = (
            f"!4m12!1m3!1d4005.9771522653964!2d{lng}!3d{lat}"
            "!2m3!1f0!2f0!3f0!3m2!1i1125!2i976!4f13.1!7i20!10b1"
            "!12m6!2m3!5m1!6e2!20e3!10b1!16b1!19m3!2m2!1i392!2i106"
            "!20m61!2m2!1i203!2i100!3m2!2i4!5b1"
            "!6m6!1m2!1i86!2i86!1m2!1i408!2i200"
            "!7m46!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2"
            "!1m3!1e2!2b0!3e3!1m3!1e3!2b0!3e3"
            "!1m3!1e4!2b0!3e3!1m3!1e8!2b0!3e3"
            "!1m3!1e3!2b1!3e2!1m3!1e9!2b1!3e2"
            "!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2"
            "!1m3!1e10!2b0!3e4!2b1!4b1!9b0"
        )

        params = {
            "tbm": "map",
            "tch": 1,
            "hl": "en",
            "q": urllib.parse.quote_plus(address),
            "pb": pb_param
        }
        search_url = f"https://www.google.com/search?{'&'.join(f'{k}={v}' for k,v in params.items())}"

        self._logger.debug(
            f':: SEARCH URL {search_url}'
        )
        try:
            # Switch to undetected-chromedriver (Selenium) to bypass bot detection and get full data
            result = await self._selenium_search(search_url, driver, temp_dir)

            # Decode response and ensure it's not empty
            if not result:
                raise ValueError(
                    "Empty response from Google Search"
                )

            # Parse ALL blocks from the response stream
            parts = result.split('/*""*/')
            collected_data = []

            for part in parts:
                text = part.strip()
                if not text:
                    continue

                # Check for wrapper structure or direct JSON
                try:
                    # Clean standard prefix if present
                    clean_text = text
                    if clean_text.startswith(")]}'"):
                        clean_text = clean_text[4:].strip()

                    obj = orjson.loads(clean_text)

                    # Handle wrapper {"c": 0, "d": "..."}
                    if isinstance(obj, dict) and 'd' in obj:
                        inner_text = obj['d']
                        # Inner text is JSON string, potentially with prefix
                        if isinstance(inner_text, str):
                            if inner_text.startswith(")]}'"):
                                inner_text = inner_text[4:].strip()
                            try:
                                inner_obj = orjson.loads(inner_text)
                                collected_data.append(inner_obj)
                            except orjson.JSONDecodeError:
                                # Could not parse inner, maybe it wasn't JSON
                                pass
                        else:
                            # 'd' was already an object?
                            collected_data.append(inner_text)
                    else:
                        # Direct object
                        collected_data.append(obj)

                except orjson.JSONDecodeError:
                    # Skip invalid parts
                    pass

            if not collected_data:
                # Fallback to try parsing original 'data' if loop failed completely
                # (Likely because split failed or format differs)
                # But we iterate 'result'. split always returns at least [result].
                return None

            # Return the collected list of objects.
            # get_populartimes will recurse through this list to find the data.
            return collected_data

        except orjson.JSONDecodeError as e:
            self._logger.error(f"Failed to parse JSON response: {e}")
            return None
        except Exception as e:
            self._logger.error(
                f"An error occurred during Google Search: {e}"
            )
            raise ComponentError(
                f"Google Search Error: {e}"
            ) from e

    async def _get_maps_by_cid(self, row: pd.Series):
        """
        Obtiene el JSON de detalle forzando el modo 'Single Item' mediante el parámetro pb.
        """
        full_hex = row.get('full_hex_format')
        lat = row.get('latitude')
        lng = row.get('longitude')

        # Si no tenemos el full_hex, intentamos generarlo desde el place_id si existe
        if not full_hex and row.get('place_id'):
            res = self.convert_place_id(row['place_id'])
            full_hex = res.get('full_hex_format')

        if not full_hex:
            self._logger.warning("No se pudo obtener full_hex_format para construir el PB.")
            return None

        data_param = "!4m5!3m4!1s{full_hex}!8m2!3d{lat}!4d{lng}".format(
            full_hex=full_hex,
            lat=lat,
            lng=lng
        )

        url = "https://www.google.com/maps/place/data=" + data_param

        self._logger.info(
            f"Fetching Map for Scraping: {url}"
        )

        try:
            # Usamos tu sesión existente
            raw = await self._google_session(
                url,
                self._get_session_args(),
                method="GET",
                as_json=False,  # Queremos los bytes crudos para parsearlos nosotros
                use_proxies=True,
                google_search=True
            )
            print('RAW ', raw)

            if not raw:
                return None

        except Exception as e:
            self._logger.error(f"Error fetching details: {e}")
            return None

    def _get_populartimes(self, place_info, data):
        """
        Extract popular times and related info from Google Maps search response.

        Structure at info[84] (popular_times_section):
        ┌─────────┬────────────────────────────────────────────────────────────┐
        │ Index   │ Content                                                    │
        ├─────────┼────────────────────────────────────────────────────────────┤
        │ [0]     │ days_array - 7 days of hourly data (for teal chart bars)   │
        │ [1]     │ current_day (1=Mon...7=Sun)                                │
        │ [2]     │ null                                                       │
        │ [3]     │ 1                                                          │
        │ [4]     │ current_hour (0-23)                                        │
        │ [5]     │ null                                                       │
        │ [6]     │ status_text ("Less busy than usual")                       │
        │ [7]     │ [current_hour, closing_hour]                               │
        └─────────┴────────────────────────────────────────────────────────────┘

        Hour data structure: [hour, percentage, status, "", label, null, short_label]
        Example: [14, 81, "Usually as busy as it gets", "", "2 pm", null, "12p"]

        The percentage value (index 1) is what creates the bar height in the chart.
        """
        # Navigate to main place info
        info = None
        base = None
        pt_index = 84

        # Helper: valid 7-day list signature
        def check_7_day_signature(lst):
            if not isinstance(lst, list) or len(lst) < 7:
                return False
            first = lst[0]
            # Must start with Int (1-7) AND contain a List (hours data) at index 1
            if not (isinstance(first, list) and len(first) > 1 and isinstance(first[0], int) and 1 <= first[0] <= 7):
                return False
            if not isinstance(first[1], list):
                return False
            return True

        # Helper to dynamically find the index of popular times in a node
        def get_popular_times_index(node):
            if not isinstance(node, list):
                return -1
            for i, item in enumerate(node):
                # Case A: Found the list directly (Direct)
                if check_7_day_signature(item):
                    return i
                # Case B: Found a wrapper containing the list at index 0 (Wrapped)
                if isinstance(item, list) and len(item) > 0 and check_7_day_signature(item[0]):
                    return i
            return -1

        # Helper to identify if a node is the 'base' node (contains popular times)
        def is_base_node(node):
            return get_popular_times_index(node) != -1

        base = None

        # Recursively find the base node in the provided structure
        def find_base_recursive(obj, depth=0):
            if depth > 10:
                return None
            if is_base_node(obj):
                return obj

            found = None
            if isinstance(obj, list):
                for item in obj:
                    found = find_base_recursive(item, depth + 1)
                    if found:
                        return found
            elif isinstance(obj, dict):
                for v in obj.values():
                    found = find_base_recursive(v, depth + 1)
                    if found:
                        return found
            return None

        base = find_base_recursive(data)

        if base:
            idx = get_popular_times_index(base)
            if idx != -1:
                pt_index = idx

            # Determine info node (Ratings)
            # Heuristic: base itself or base[14]
            info = None
            rating_check = self.index_get(base, 4, 7)
            if isinstance(rating_check, (int, float)):
                info = base
            else:
                candidate = self.index_get(base, 14)
                if isinstance(candidate, list):
                    info = candidate

            if info is None:
                self._logger.warning(
                    "Found popular times base, but could not identify Rating/Info node."
                )
                info = []
        else:
            info = None

        if base is None and (info is None or (isinstance(info, list) and len(info) == 0)):

            self._logger.warning(
                "Could not find place info in response"
            )
            place_info.update({
                "rating": None,
                "rating_n": None,
                "current_popularity": None,
                "popular_times": None,
                "time_spent": None
            })
            return

        # ═══════════════════════════════════════════════════════════════════
        # 1. RATING (star rating, e.g., 4.2)
        # ═══════════════════════════════════════════════════════════════════
        rating = self.index_get(info, 4, 7)

        # ═══════════════════════════════════════════════════════════════════
        # 2. RATING_N (number of reviews, e.g., 1761)
        # ═══════════════════════════════════════════════════════════════════
        rating_n = self.index_get(info, 4, 8)
        # fallback: search for [rating, histogram, count]

        print('Rating N from index_get: ', rating, rating_n)
        if rating_n is None:
            for item in info:
                if (
                    isinstance(item, list) and len(item) == 3 and isinstance(item[2], int)
                ):
                    rating_n = item[2]
                    break

        # ═══════════════════════════════════════════════════════════════════
        # 3 & 4. POPULAR_TIMES and CURRENT_POPULARITY
        # ═══════════════════════════════════════════════════════════════════
        popular_times_section = self.index_get(base, pt_index)

        print(' POPULAR_TIMES_SECTION: ', popular_times_section)

        popular_times = None
        current_popularity = None

        if popular_times_section and isinstance(popular_times_section, list):
            # Normalize: Check if section IS the days array or contains it
            days_array = None
            if check_7_day_signature(popular_times_section):
                days_array = popular_times_section
            elif len(popular_times_section) > 0 and check_7_day_signature(popular_times_section[0]):
                days_array = self.index_get(popular_times_section, 0)

            if days_array and isinstance(days_array, list):
                popular_times = days_array

                # Get current context
                current_day = self.index_get(popular_times_section, 1)    # 1-7
                current_hour = self.index_get(popular_times_section, 4)   # 0-23

                # CURRENT_POPULARITY (RED bar) - Try to find LIVE data first
                # Live data might be at different locations depending on response

                # Method 1: Check for live popularity indicator in the section
                # Sometimes Google includes real-time data separately
                live_data = self._find_live_popularity(popular_times_section)

                if live_data is not None:
                    current_popularity = live_data
                elif current_day is not None and current_hour is not None:
                    # Method 2: Fall back to historical data for current hour
                    # This is the "usual" value, not necessarily live
                    current_popularity = self._get_hour_popularity(
                        days_array, current_day, current_hour
                    )

        # ═══════════════════════════════════════════════════════════════════
        # 5. TIME_SPENT (typical visit duration)
        # ═══════════════════════════════════════════════════════════════════
        time_spent = self._extract_time_spent(info)

        # Update place_info with all extracted data
        place_info.update({
            "rating": rating,
            "rating_n": rating_n,
            "current_popularity": current_popularity,
            "popular_times": popular_times,
            "time_spent": time_spent
        })

    def _find_live_popularity(self, popular_times_section):
        """
        Try to find LIVE current popularity from the response.

        Live data creates the RED bar in the chart (vs teal historical bars).
        Google sometimes includes real-time visitor data when available.

        Returns:
            Live popularity percentage (0-100) or None if not available
        """
        if not popular_times_section or not isinstance(popular_times_section, list):
            return None

        # Check multiple possible locations for live data
        # The structure can vary based on whether Google has real-time data

        # Location 1: Sometimes at index 1 with nested structure
        live_section = self.index_get(popular_times_section, 1)
        if isinstance(live_section, list) and len(live_section) > 1:
            # Could be [[day_info], live_percentage, ...]
            candidate = self.index_get(live_section, 1)
            if isinstance(candidate, (int, float)) and 0 <= candidate <= 100:
                return int(candidate)

        # Location 2: Check if there's a separate live indicator
        # Format might be [[[live_data]], historical_day, ...]
        first_element = self.index_get(popular_times_section, 0)
        if isinstance(first_element, list) and len(first_element) > 0:
            potential_live = self.index_get(first_element, 0, 0)
            if isinstance(potential_live, list):
                # Check for live marker format
                live_pct = self.index_get(potential_live, 1)
                if isinstance(live_pct, (int, float)) and 0 <= live_pct <= 100:
                    # Verify this looks like live data (has different structure)
                    pass  # Additional validation could go here

        # Location 3: Parse from status text at index 6
        status_text = self.index_get(popular_times_section, 6)
        if isinstance(status_text, str):
            # Look for patterns like "45% busier than usual"
            match = re.search(r'(\d+)%', status_text)
            if match:
                return int(match.group(1))

        return None

    def _get_hour_popularity(self, days_array, day_number, hour):
        """
        Get the historical popularity percentage for a specific day and hour.

        This is the value shown in the TEAL bars of the chart.

        Args:
            days_array: Array of 7 days with hourly data
            day_number: Day of week (1=Monday, 2=Tuesday, ..., 7=Sunday)
            hour: Hour of day (0-23)

        Returns:
            Popularity percentage (0-100) or None
        """
        if not days_array or not isinstance(days_array, list):
            return None

        # Find the day in the array
        # Each day: [day_number, [[hour_data, ...]], display_flag]
        for day_data in days_array:
            if not isinstance(day_data, list) or len(day_data) < 2:
                continue

            if day_data[0] == day_number:
                hourly_data = day_data[1]
                if not isinstance(hourly_data, list):
                    return None

                # Find the hour
                # Each hour: [hour, percentage, status, "", label, null, short_label]
                for hour_entry in hourly_data:
                    if not isinstance(hour_entry, list) or len(hour_entry) < 2:
                        continue

                    if hour_entry[0] == hour:
                        percentage = hour_entry[1]
                        if isinstance(percentage, (int, float)):
                            return int(percentage) if percentage > 0 else None
                        return None

                return None  # Hour not found

        return None  # Day not found

    def _extract_time_spent(self, info):
        """
        Extract and parse time spent information.

        Args:
            info: The main place info array

        Returns:
            [min_minutes, max_minutes] or None
        """
        # Search for time spent text in common indices
        time_spent_str = None
        for idx in [117, 118, 116, 119, 120]:
            candidate = self.index_get(info, idx, 0)
            if candidate and isinstance(candidate, str):
                if "spend" in candidate.lower() or "minute" in candidate.lower() or "hour" in candidate.lower():
                    time_spent_str = candidate
                    break

        if not time_spent_str:
            return None

        # Parse the string (e.g., "People typically spend 20 min here")
        try:
            nums = [float(f) for f in re.findall(r'\d*\.\d+|\d+', time_spent_str.replace(",", "."))]
            if not nums:
                return None

            text_lower = time_spent_str.lower()
            has_min = "min" in text_lower
            has_hour = "hour" in text_lower or "hr" in text_lower

            if has_min and has_hour:
                # Mixed: "30 min to 1 hour"
                if len(nums) >= 2:
                    return [int(min(nums)), int(max(nums) * 60)]
                return [int(nums[0]), int(nums[0] * 60)]
            elif has_hour:
                # Hours only: "1-2 hours"
                if len(nums) >= 2:
                    return [int(nums[0] * 60), int(nums[1] * 60)]
                return [int(nums[0] * 60), int(nums[0] * 60)]
            elif has_min:
                # Minutes only: "20 min" or "15-30 min"
                if len(nums) >= 2:
                    return [int(nums[0]), int(nums[1])]
                return [int(nums[0]), int(nums[0])]
            else:
                # No units, assume minutes
                if len(nums) >= 2:
                    return [int(nums[0]), int(nums[1])]
                return [int(nums[0]), int(nums[0])]

        except (ValueError, IndexError):
            return None

    def _convert_populartimes(self, popular_times: dict):
        # Map day numbers to day names
        day_mapping = {
            "1": "Monday",
            "2": "Tuesday",
            "3": "Wednesday",
            "4": "Thursday",
            "5": "Friday",
            "6": "Saturday",
            "7": "Sunday"
        }
        # Dictionary to hold the final structured data
        converted_data = {}
        # Iterate through each day and its hours
        for day_number, hours in popular_times.items():
            # Get the day name from the mapping
            day_name = day_mapping.get(day_number, "Unknown")
            converted_data[day_name] = {}

            for hour, data in hours.items():
                # Convert the hour to HH:MM:SS format
                # Ensure leading zeroes for single-digit hours
                time_str = f"{int(hour):02}:00:00"
                # Create the structured dictionary
                converted_data[day_name][time_str] = {
                    "hour": int(hour),
                    "human_hour": data["human_hour"],
                    "traffic": data["traffic"],
                    "traffic_status": data["traffic_status"]
                }
        return converted_data

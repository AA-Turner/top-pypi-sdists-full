from collections.abc import Callable
import asyncio
import random
import httpx
import pandas as pd
from tqdm.asyncio import tqdm
from bs4 import BeautifulSoup
from ...exceptions import ComponentError, ConfigError
from ...interfaces import HTTPService, SeleniumService
from ...interfaces.http import ua
from ...interfaces.flow import FlowComponent
from .parsers import (
    CostcoScrapper,
)


class ServiceScrapper(FlowComponent, SeleniumService, HTTPService):
    """
    Service Scraper Component

    Overview:

    Pluggable component for scrapping several services and sites using different scrapers.
    Supports different types of operations.

    .. table:: Properties
    :widths: auto

    +-----------------------+----------+------------------------------------------------------------------------------------------------------+
    | Name                  | Required | Description                                                                                          |
    +-----------------------+----------+------------------------------------------------------------------------------------------------------+
    | type (str)            |   Yes    | Type of operation to perform. Accepts 'events' for Costco events extraction.                        |
    +-----------------------+----------+------------------------------------------------------------------------------------------------------+
    | scrapper (str)        |   Yes    | Name of the scrapper to use (e.g., 'costco').                                                        |
    +-----------------------+----------+------------------------------------------------------------------------------------------------------+
    | url_column (str)      |   No     | Name of the column containing URLs to scrape (default: 'url')                                        |
    +-----------------------+----------+------------------------------------------------------------------------------------------------------+
    | wait_for (tuple)      |   No     | Element to wait for before scraping (default: ('class', 'company-overview'))                        |
    +-----------------------+----------+------------------------------------------------------------------------------------------------------+

    Return:
    - DataFrame with extracted information based on the type specified
    """  # noqa: E501

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.type: str = kwargs.get('type', 'events')  # Default to events
        self.info_column: str = kwargs.get('column_name', 'url')
        self.scrapper_name: str = kwargs.get('scrapper', 'costco')
        self.headless: bool = kwargs.get('headless', False)
        self.scrapper_class: Callable = None
        self._scrapper_func: str = kwargs.get('function', 'get_events')
        self.wait_for: tuple = kwargs.get('wait_for', ('class', 'company-overview'))
        self._counter: int = 0
        self.use_proxy: bool = True
        self._free_proxy: bool = False
        self.paid_proxy: bool = True
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self.concurrently: bool = kwargs.get('concurrently', False)
        self.task_parts: int = kwargs.get('task_parts', 10)
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        # Headers configuration
        self.headers: dict = {
            "Accept": self.accept,
            "TE": "trailers",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(ua),
            **kwargs.get('headers', {})
        }
        self._free_proxy = False

    def split_parts(self, task_list, num_parts: int = 5) -> list:
        part_size, remainder = divmod(len(task_list), num_parts)
        parts = []
        start = 0
        for i in range(num_parts):
            # Distribute the remainder across the first `remainder` parts
            end = start + part_size + (1 if i < remainder else 0)
            parts.append(task_list[start:end])
            start = end
        return parts

    async def _processing_tasks(self, tasks: list) -> pd.DataFrame:
        """Process tasks concurrently."""
        results = []
        total_tasks = len(tasks)
        # Overall progress bar
        with tqdm(total=total_tasks, desc="Scraping Progress", unit="task") as pbar_total:
            if self.concurrently is False:
                # run every task in a sequential manner:
                for task in tasks:
                    try:
                        idx, row = await task
                        results.append((idx, row))  # Append as tuple (idx, row)
                        await asyncio.sleep(
                            random.uniform(0.25, 1.5)
                        )
                    except Exception as e:
                        self._logger.error(f"Task error: {str(e)}")
                        results.append((idx, row))  # Store the failure result
                    finally:
                        pbar_total.update(1)
            else:
                for chunk in self.split_parts(tasks, self.task_parts):
                    result = await asyncio.gather(*chunk, return_exceptions=False)
                    results.extend(result)
                # Convert results to DataFrame
        if not results:
            return pd.DataFrame()

        indices, data_dicts = zip(*results) if results else ([], [])
        df = pd.DataFrame(data_dicts, index=indices)
        return df

    async def start(self, **kwargs) -> bool:
        """Initialize the component and validate required parameters."""
        if self.previous:
            self.data = self.input

        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Input must be a DataFrame", status=404
            )

        if self.info_column not in self.data.columns:
            raise ConfigError(
                f"Column {self.info_column} not found in DataFrame"
            )

        return True

    async def _start_scrapping(self, idx, row):
        try:
            async with self._semaphore:
                url = row[self.info_column]
                self._logger.debug(
                    f"Scraping URL: {url}"
                )
                async with self.scrapper_class as scrapper:
                    response = await scrapper.get(url, headers=self.headers)
                    if response:
                        try:
                            fn = getattr(scrapper, self._scrapper_func, 'scrapping')
                            idx, row = await fn(response, idx, row)
                        except Exception as err:
                            print(' Exception caught > ', err)
                            return idx, row
            return idx, row
        except Exception as err:
            print(' Exception caught > ', err)
            raise ComponentError(
                f"Error while scrapping: {err}"
            )

    def _get_scrapper(self):
        """Get the scrapper class."""
        try:
            if self.scrapper_name == 'costco':
                return CostcoScrapper()
            else:
                return None
        except Exception as err:
            print(err)
            raise ConfigError(
                f"Error while getting scrapper: {err}"
            )

    async def run(self):
        """Execute scraping based on the specified type."""
        # Get the appropriate method based on type
        type_call = getattr(self, f"{self.type}", None)

        if not type_call:
            raise ComponentError(
                f"Incorrect or not provided type: {self.type}"
            )

        if not callable(type_call):
            raise ComponentError(
                f"Function {self.type} doesn't exist."
            )

        try:
            result = await type_call()
        except Exception as e:
            self._logger.error(f"Error: {str(e)}")
            raise

        if not isinstance(result, pd.DataFrame):
            self._result = result
            return self._result

        self.add_metric("NUMROWS", len(result.index))
        self.add_metric("NUMCOLS", len(result.columns))

        self._result = result

        if self._debug is True:
            self._print_data_(self._result, 'Scrapper Results')

        return self._result

    async def events(self):
        """
        Extract events from Costco using Chrome undetected.
        This method uses the same approach as our successful test.
        """
        # Configure scrapper for Chrome undetected
        try:
            self.scrapper_class = self._get_scrapper()
        except Exception as err:
            raise ConfigError(
                f"Error while getting scrapper: {err}"
            )

        # Configure Chrome undetected settings
        self.scrapper_class.headless = self.headless
        self.scrapper_class.use_proxy = True
        self.scrapper_class.timeout = 300
        self.scrapper_class.enable_http2 = False
        self.scrapper_class.use_undetected = True
        self.scrapper_class.use_wire = False
        self.scrapper_class.use_firefox = False

        # Set up cookies
        httpx_cookies = self.get_httpx_cookies(
            domain=self.scrapper_class.domain, cookies=self.cookies
        )
        self.scrapper_class.cookies = httpx_cookies
        self.scrapper_class.set_columns(self.data)

        if not self.scrapper_class:
            raise ConfigError(
                "No valid scrapper were found or provided in configuration"
            )

        # Process each URL under a single shared virtual display so Chrome
        # never opens on the user's real screen and Xvfb is not restarted
        # between URLs (which would cause session errors from stale lock files).
        from flowtask.interfaces.selenium_service import VirtualDisplay

        all_events = []
        with VirtualDisplay():
            for idx, row in self.data.iterrows():
                try:
                    url = row[self.info_column]
                    self._logger.info(f"Processing URL {idx + 1}/{len(self.data)}: {url}")

                    events = await self._extract_events_from_url(url)
                    all_events.extend(events)

                    # Polite delay between requests
                    await asyncio.sleep(random.uniform(2, 5))

                except Exception as e:
                    self._logger.error(f"Error processing URL {url}: {e}")
                    continue

        # Create DataFrame from all events
        if all_events:
            df = pd.DataFrame(all_events)
            self._logger.info(f"Successfully extracted {len(df)} events from {len(self.data)} URLs")
            return df
        else:
            self._logger.warning("No events were extracted")
            return pd.DataFrame()

    async def _extract_events_from_url(self, url: str):
        """
        Extract events from a single URL using Chrome undetected.
        """
        events = []
        
        try:
            async with self.scrapper_class as scrapper:
                # Wait for browser to stabilize
                await asyncio.sleep(10)
                
                # Get the page
                response = await scrapper.get(url)
                
                if response:
                    # Wait for page to load completely
                    await asyncio.sleep(30)

                    # Get updated HTML
                    try:
                        updated_response = scrapper._driver.page_source
                        response = updated_response
                    except Exception as e:
                        self._logger.warning(f"Could not get updated HTML: {e}")

                    # Save debug screenshot
                    try:
                        import re as _re
                        slug = _re.sub(r'[^a-z0-9]+', '_', url.lower()).strip('_')
                        screenshot_path = f"/tmp/costco_screenshot_{slug}.png"
                        scrapper._driver.save_screenshot(screenshot_path)
                        self._logger.info(f"Screenshot saved: {screenshot_path}")
                    except Exception as e:
                        self._logger.warning(f"Could not save screenshot: {e}")

                    # Extract events using the same logic as our test
                    events = self._parse_events_from_html(response, url)
                    
        except Exception as e:
            self._logger.error(f"Error extracting events from {url}: {e}")
        
        return events

    def _parse_events_from_html(self, html_content: str, url: str):
        """
        Parse events from HTML content using the same selectors as our test.
        """
        events = []
        
        try:
            from bs4 import BeautifulSoup
            import re
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract region from title
            region = "Unknown Region"
            title = soup.find('title')
            if title:
                title_text = title.get_text(strip=True)
                region_match = re.search(r'Special Events in (.*?) Region', title_text)
                if region_match:
                    region = region_match.group(1).strip()
            
            # Extract state and warehouses
            current_state = "Unknown State"
            warehouses = soup.find_all('div', class_='sp-event-warehouse')

            for warehouse in warehouses:
                # Check for state change
                prev_state_header = warehouse.find_previous('h2', class_='state-name')
                if prev_state_header:
                    state_text = prev_state_header.get_text(strip=True)
                    current_state = state_text.replace("Warehouses", "").strip()

                # Extract store name
                store_name_elem = warehouse.find('h3', class_='warehouse-name')
                if not store_name_elem:
                    continue

                store_name = store_name_elem.get_text(strip=True)

                # Find warehouse ID from panel-heading aria-controls attribute
                panel_heading = warehouse.find('div', class_='panel-heading')
                if not panel_heading:
                    continue
                warehouse_id = panel_heading.get('aria-controls')
                if not warehouse_id:
                    continue

                table_container = soup.find('div', id=warehouse_id)
                if not table_container:
                    continue
                    
                table = table_container.find('table')
                if not table:
                    continue
                    
                # Process table rows
                rows = table.find_all('tr')
                
                for row in rows[1:]:  # Skip header
                    cells = row.find_all('td')
                    
                    if len(cells) >= 2:
                        # Extract full dates from <time> elements with datetime attributes
                        date_cell = cells[0]
                        time_elements = date_cell.find_all('time')

                        start_date = ""
                        end_date = ""

                        if time_elements and len(time_elements) >= 2:
                            # Extract start and end dates
                            start_datetime = time_elements[0].get('datetime')
                            end_datetime = time_elements[1].get('datetime')
                            start_date = start_datetime if start_datetime else ""
                            end_date = end_datetime if end_datetime else ""
                        elif time_elements and len(time_elements) == 1:
                            # Only one date found, use it as both start and end
                            datetime_attr = time_elements[0].get('datetime')
                            start_date = datetime_attr if datetime_attr else ""
                            end_date = datetime_attr if datetime_attr else ""
                        else:
                            # Fallback to original text if no time elements found
                            date_text = date_cell.get_text(strip=True)
                            start_date = date_text
                            end_date = ""

                        event_data = {
                            "region": region,
                            "store_name": store_name,
                            "state": current_state,
                            "start_date": start_date,
                            "end_date": end_date,
                            "event": cells[1].get_text(strip=True),
                            "brand_event": ""
                        }
                        
                        # Extract link if available
                        link = cells[1].find('a')
                        if link and link.get('href'):
                            event_data["brand_event"] = link.get('href')
                        
                        events.append(event_data)
        
        except Exception as e:
            self._logger.error(f"Error parsing HTML: {e}")
        
        return events

    async def close(self):
        """Clean up resources."""
        return True

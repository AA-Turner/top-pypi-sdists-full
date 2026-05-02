from collections.abc import Callable
import asyncio
import logging
import random
import backoff
import httpx
from typing import Optional, Dict, Any
import pandas as pd
from bs4 import BeautifulSoup
from ..exceptions import ComponentError, ConfigError
from ..interfaces import HTTPService, SeleniumService
from ..interfaces.http import ua, bad_gateway_exception
from .flow import FlowComponent
import json


class ZoomInfoScraper(FlowComponent, HTTPService, SeleniumService):
    """
    ZoomInfo Scraper Component that can use either HTTP or Selenium for scraping.

    Overview:

    This component scrapes company information from ZoomInfo pages using HTTPService.
    It can receive URLs from a previous component (like GoogleSearch) and extract
    specific company information.

    :widths: auto

    | url_column (str)      |   Yes    | Name of the column containing URLs to scrape (default: 'search_url')                                |
    | wait_for (tuple)      |   No     | Element to wait for before scraping (default: ('class', 'company-overview'))                        |

    Return:

    The component adds new columns to the DataFrame with company information:
    - headquarters
    - phone_number
    - website
    - stock_symbol
    - naics_code
    - employee_count

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ZoomInfoScraper:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(self, loop: asyncio.AbstractEventLoop = None, job: Callable = None, stat: Callable = None, **kwargs) -> None:
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        
        # Flag to determine which service to use
        self.use_selenium = kwargs.get('use_selenium', True)
        
        # Configure common attributes
        self.url_column = kwargs.get('url_column', 'search_url')
        self._counter = 0
        self._debug = kwargs.get('debug', False)
        self._semaphore = asyncio.Semaphore(kwargs.get('max_concurrent', 5))
        
        # Proxy configuration like BestBuy
        self.use_proxy = True
        self._free_proxy = False
        self.paid_proxy = True
        
        # Configure Selenium specific settings if needed
        if self.use_selenium:
            self.accept_cookies = kwargs.get('accept_cookies', ('id', 'onetrust-accept-btn-handler'))
            self.wait_until = kwargs.get('wait_until', ('class', 'company-overview'))
            self.timeout = kwargs.get('timeout', 30)

            # Proxy is now configured via Selenium options directly in get_driver()
        
        # Configure HTTP specific settings
        else:
            self.headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": random.choice(ua),
                **kwargs.get('headers', {})
            }
            self.session_cookies = kwargs.get('session_cookies', {})

    def split_parts(self, task_list, num_parts: int = 5) -> list:
        """Split task list into parts for concurrent processing."""
        part_size = len(task_list) // num_parts
        remainder = len(task_list) % num_parts
        parts = []
        start = 0
        for i in range(num_parts):
            # Distribute the remainder across the first `remainder` parts
            end = start + part_size + (1 if i < remainder else 0)
            parts.append(task_list[start:end])
            start = end
        return parts

    async def _processing_tasks(self, tasks: list) -> pd.DataFrame:
        """Process tasks concurrently and format the results."""
        results = []
        for chunk in self.split_parts(tasks, self.task_parts):
            result = await asyncio.gather(*chunk, return_exceptions=False)
            results.extend(result)
        
        # Filter out None results and separate index and data
        valid_results = [(idx, data) for idx, data in results if data]
        
        if not valid_results:
            return pd.DataFrame()
        
        # Split into indices and data dictionaries
        indices, data_dicts = zip(*valid_results)
        
        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(data_dicts, index=indices)
        
        # Ensure all expected columns exist
        expected_columns = [
            'company_name',
            'logo_url',
            'address',
            'phone_number', 
            'website', 
            'stock_symbol',
            'naics_code',
            'sic_code',
            'employee_count',
            'revenue_range',
            'similar_companies',
            'search_term',
            'search_url'
        ]
        
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None
            
        return df

    async def start(self, **kwargs) -> bool:
        """Initialize the component and validate required parameters."""
        if self.previous:
            self.data = self.input
        
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Input must be a DataFrame", status=404
            )

        if self.url_column not in self.data.columns:
            raise ConfigError(
                f"Column {self.url_column} not found in DataFrame"
            )

        # Initialize result columns
        new_columns = [
            'search_term',
            'search_url',
            'company_name',
            'logo_url',
            'address',
            'phone_number', 'website', 
            'stock_symbol', 'naics_code', 'sic_code', 
            'employee_count', 'revenue_range', 'similar_companies'
        ]
        for col in new_columns:
            if col not in self.data.columns:
                self.data[col] = None

        return True

    def extract_company_info(self, soup: BeautifulSoup, search_term: str, search_url: str) -> Dict[str, Any]:
        """Extract company information from the page."""
        result = {}
        result['search_term'] = search_term
        result['search_url'] = search_url

        # Get company name and logo URL from header
        logo = soup.find('img', {'alt': True, 'width': '76.747'})
        if logo:
            result['company_name'] = logo.get('alt')
            result['logo_url'] = logo.get('src')

        # Extract information from About section
        about_section = soup.find('app-about')
        if about_section:
            # Get headquarters/address
            address_container = about_section.find('div', {'class': 'icon-text-container'})
            if address_container and 'Headquarters' in address_container.text:
                result['address'] = address_container.find('span', {'class': 'content'}).text.strip()

            # Get phone number
            phone_container = about_section.find_all('div', {'class': 'icon-text-container'})[1]
            if phone_container and 'Phone Number' in phone_container.text:
                result['phone_number'] = phone_container.find('span', {'class': 'content'}).text.strip()

            # Get website
            website_container = about_section.find_all('div', {'class': 'icon-text-container'})[2]
            if website_container:
                website_link = website_container.find('a', {'class': 'website-link'})
                if website_link:
                    result['website'] = website_link.text.strip()

            # Get revenue
            revenue_container = about_section.find_all('div', {'class': 'icon-text-container'})[3]
            if revenue_container and 'Revenue' in revenue_container.text:
                result['revenue_range'] = revenue_container.find('span', {'class': 'content'}).text.strip()

        # Get employee count from company compare section
        company_compare = soup.find('app-company-compare-details', {'class': 'first-company'})
        if company_compare:
            emp_count = company_compare.find('div', {'class': 'num-of-emp'})
            if emp_count:
                result['employee_count'] = emp_count.text.strip()

        # Get industry information
        industry_chips = about_section.find('span', {'id': 'company-chips-wrapper'})
        if industry_chips:
            industries = [chip.text.strip() for chip in industry_chips.find_all('a', {'class': 'link'})]
            result['industries'] = industries

        # Get company description
        overview = soup.find('app-company-overview')
        if overview:
            desc = overview.find('span', {'class': 'company-desc'})
            if desc:
                result['description'] = desc.text.strip()

        # Get social media links
        social_media = soup.find('span', {'id': 'social-media-icons-wrapper'})
        if social_media:
            social_links = {}
            for link in social_media.find_all('a', {'class': 'social-media-icon'}):
                platform = link.get('id').split('-')[1].lower()
                social_links[platform] = link.get('href')
            result['social_media'] = social_links

        # Get SIC and NAICS codes
        codes_wrapper = soup.find('span', {'id': 'codes-wrapper'})
        if codes_wrapper:
            for code in codes_wrapper.find_all('span', {'class': 'codes-content'}):
                if 'SIC Code' in code.text:
                    result['sic_code'] = code.text.replace('SIC Code', '').strip()
                elif 'NAICS Code' in code.text:
                    result['naics_code'] = code.text.replace('NAICS Code', '').strip()

        # Get similar companies
        similar_companies = []
        company_compare = soup.find('app-company-compare')
        if company_compare:
            for company in company_compare.find_all('app-company-compare-details')[1:]:  # Skip first (current company)
                company_name = company.find('a', {'class': 'company-name'})
                if not company_name:
                    continue

                similar_company = {
                    'name': company_name.text.strip(),
                    'revenue': company.find('div', {'class': 'revenue'}).text.strip() if company.find('div', {'class': 'revenue'}) else None,
                    'employee_count': company.find('div', {'class': 'num-of-emp'}).text.strip() if company.find('div', {'class': 'num-of-emp'}) else None
                }
                similar_companies.append(similar_company)

        if similar_companies:
            try:
                result['similar_companies'] = json.dumps(
                    similar_companies,
                    ensure_ascii=False,
                    allow_nan=False,
                    separators=(',', ':')
                )
            except Exception as e:
                self._logger.error(f"Error formatting similar companies JSON: {str(e)}")
                result['similar_companies'] = None

        if not result:
            self._logger.warning("No data was extracted from the page")
        else:
            self._logger.info(f"Successfully extracted data")

        return result
    
    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError),
        max_tries=3,
        max_time=30,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, (httpx.ConnectTimeout, httpx.ReadTimeout))
    )
    async def scrape_url(self, idx: int, row: pd.Series) -> tuple[int, Optional[Dict[str, Any]]]:
        """Scrape a single ZoomInfo URL using either HTTP or Selenium."""
        async with self._semaphore:
            try:
                url = row[self.url_column]
                search_term = row['search_term']
                search_url = row['search_url']
                
                if pd.isna(url):
                    return idx, None

                self._logger.notice(f"Scraping ZoomInfo URL: {url}")

                if self.use_selenium:
                    # Use Selenium for scraping
                    try:
                        # Initialize driver with proxy if needed
                        if not self._driver:
                            await self.init_driver()
                        await self.get_page(url)
                        content = self._driver.page_source
                        soup = BeautifulSoup(content, 'html.parser')
                    except Exception as e:
                        self._logger.error(f"Selenium error for URL {url}: {str(e)}")
                        return idx, None
                else:
                    # Use HTTP for scraping
                    try:
                        # Get proxies if using HTTP
                        if self.use_proxy:
                            proxies = await self.get_proxies()
                            proxy = proxies[0]
                            proxy_config = {
                                "http://": f"http://{proxy}",
                                "https://": f"http://{proxy}"
                            }
                        else:
                            proxy_config = None

                        response = await self._get(
                            url,
                            headers=self.headers,
                            cookies=self.session_cookies,
                            proxies=proxy_config
                        )
                        
                        if response.status_code == 403:
                            self._logger.error(f"Access forbidden for URL {url}. Consider switching to Selenium.")
                            return idx, None
                        
                        if response.status_code != 200:
                            self._logger.error(f"Failed to fetch URL {url}: {response.status_code}")
                            return idx, None

                        content = response.text
                        soup = BeautifulSoup(content, 'html.parser')

                    except Exception as e:
                        self._logger.error(f"HTTP error for URL {url}: {str(e)}")
                        return idx, None

                # Check for blocks/captchas
                if self._is_blocked(soup):
                    self._logger.error(f"Access blocked for URL {url}. Consider switching to Selenium.")
                    return idx, None

                result = self.extract_company_info(soup, search_term, search_url)
                
                if result:
                    self._counter += 1
                return idx, result

            except Exception as e:
                self._logger.error(f"Error scraping URL {url}: {str(e)}")
                return idx, None

    def _is_blocked(self, soup: BeautifulSoup) -> bool:
        """Check if the response indicates we're blocked or need to solve a CAPTCHA."""
        blocked_indicators = [
            'captcha',
            'blocked',
            'access denied',
            'please verify you are a human'
        ]
        
        page_text = soup.get_text().lower()
        return any(indicator in page_text for indicator in blocked_indicators)

    async def run(self):
        """Execute scraping for each URL in the DataFrame."""
        tasks = [
            self.scrape_url(idx, row) for idx, row in self.data.iterrows()
        ]
        df = await self._processing_tasks(tasks)
        self.add_metric("PAGES_SCRAPED", self._counter)
        
        if self._debug is True:
            print(df)
            print("::: Printing Column Information === ")
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])
        
        self._result = df
        return self._result

    async def close(self):
        """Clean up resources."""
        if self.use_selenium:
            self.close_driver()
        return True 
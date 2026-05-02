from collections.abc import Callable
import asyncio
import random
import backoff
import httpx
from typing import List, Optional, Dict, Any
from tqdm.asyncio import tqdm
from fuzzywuzzy import fuzz
import pandas as pd
from bs4 import BeautifulSoup
from duckduckgo_search.exceptions import RatelimitException
from ...exceptions import ComponentError, ConfigError
from ...interfaces import HTTPService, SeleniumService
from ...interfaces.http import ua, bad_gateway_exception
from ..flow import FlowComponent
from .parsers import (
    LeadiqScrapper,
    ExploriumScrapper,
    ZoomInfoScrapper,
    SicCodeScrapper,
    RocketReachScrapper,
    VisualVisitorScrapper
)
import json
import re


class CompanyScraper(FlowComponent, SeleniumService, HTTPService):
    """
    Company Scraper Component

    Overview:

    This component scrapes company information from different sources using HTTPService.
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
          CompanyScraper:
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
    ) -> None:
        self.info_column: str = kwargs.get('column_name', 'company_name')
        self.scrappers: list = kwargs.get('scrappers', ['leadiq'])
        self.wait_for: tuple = kwargs.get('wait_for', ('class', 'company-overview'))
        self._counter: int = 0
        self.use_proxy: bool = True
        self._free_proxy: bool = False
        self.paid_proxy: bool = True
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self.concurrently: bool = kwargs.get('concurrently', True)
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
        total_tasks = len(tasks)
        with tqdm(total=total_tasks, desc="Scraping Progress", unit="task") as pbar_total:  # Overall progress bar
            if self.concurrently is False:
                # run every task in a sequential manner:
                for task in tasks:
                    try:
                        idx, row = await task
                        results.append((idx, row))  # Append as tuple (idx, row)
                        await asyncio.sleep(
                            random.uniform(0.5, 2)
                        )
                    except Exception as e:
                        self._logger.error(f"Task error: {str(e)}")
                        idx, row = self._get_error_info(e)  # Handle error
                        results.append((idx, row))  # Store the failure result
                    finally:
                        pbar_total.update(1)
            else:
                # run all tasks concurrently
                for chunk in self.split_parts(tasks, self.task_parts):
                    chunk_size = len(chunk)
                    # Usar return_exceptions=True para capturar errores sin detener la ejecución
                    chunk_results = await asyncio.gather(
                        *chunk, return_exceptions=True
                    )
                    for result in chunk_results:
                        if isinstance(result, Exception):
                            self._logger.error(f"Task error: {str(result)}")
                            idx, row = self._get_error_info(result)  # Extract idx, row from error
                            results.append((idx, row))
                        else:
                            results.append(result)

                    pbar_total.update(chunk_size)

        # Convert results to DataFrame
        if not results:
            return pd.DataFrame()

        indices, data_dicts = zip(*results) if results else ([], [])
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

        if self.info_column not in self.data.columns:
            raise ConfigError(
                f"Column {self.info_column} not found in DataFrame"
            )

        # Initialize result columns
        new_columns = [
            'search_term',
            'search_url',
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
            'industry_category',
            'industry',
            'category',
            'company_description',
            'city',
            'state',
            'zip_code',
            'country',
            'metro_area',
            'headquarters',
            'location',
            'number_employees',
            'founded',
            'search_status',
            'scrape_status'
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
        # Get company name and logo URL from logo image
        logo = soup.find('img', {'alt': True, 'width': '76.747'})
        if logo:
            result['company_name'] = logo.get('alt')
            result['logo_url'] = logo.get('src')

        # Get company revenue range from highlight-right section
        highlight_right = soup.find('div', {'class': 'highlight-right'})
        if highlight_right:
            revenue_span = highlight_right.find('span', {'class': 'start'})
            if revenue_span:
                start_value = revenue_span.text.strip()
                end_span = revenue_span.find_next_sibling('span', {'class': 'end'})
                if end_span:
                    end_value = end_span.text.strip()
                    result['revenue_range'] = f"{start_value} - {end_value}"
                else:
                    result['revenue_range'] = start_value

        # First find the highlight-left section that contains company info
        highlight_left = soup.find('div', {'class': 'highlight-left'})
        if not highlight_left:
            self._logger.warning("Could not find highlight-left section")
            return result

        # Then find the card span within highlight-left
        overview_section = highlight_left.find('div', {'class': 'card span'})
        if not overview_section:
            return result

        # Extract information from dl/dt/dd elements
        dl_element = overview_section.find('dl')
        if dl_element:
            for item in dl_element.find_all('div', {'class': 'item'}):
                dt = item.find('dt')
                dd = item.find('dd')
                if dt and dd:
                    field = dt.text.strip().lower()
                    value = dd.text.strip()

                    # Map fields to our column names
                    if field == 'headquarters':
                        result['address'] = value
                    elif field == 'phone number':
                        phone = value.replace('****', '0000')
                        result['phone_number'] = phone
                    elif field == 'website':
                        website = dd.find('a')
                        result['website'] = website['href'] if website else value
                    elif field == 'stock symbol':
                        result['stock_symbol'] = value
                    elif field == 'naics code':
                        result['naics_code'] = value
                    elif field == 'employees':
                        result['employee_count'] = value
                    elif field == 'sic code':
                        result['sic_code'] = value

        # Extract similar companies
        similar_companies = []
        similar_section = soup.find('div', {'id': 'similar'})
        if similar_section:
            for company in similar_section.find_all('li'):
                company_link = company.find('a')
                if not company_link:
                    continue

                company_logo = company_link.find('img')
                company_name = company_link.find('h3')

                # Find revenue span
                revenue_spans = company_link.find_all('span')
                revenue_span = None
                for span in revenue_spans:
                    if span.find('span', {'class': 'start'}):
                        revenue_span = span
                        break

                if company_name:
                    similar_company = {
                        'name': company_name.text.strip(),  # No escapamos las comillas
                        'leadiq_url': company_link['href'],
                        'logo_url': company_logo['src'] if company_logo else None,
                    }

                    # Extract revenue range
                    if revenue_span:
                        start = revenue_span.find('span', {'class': 'start'})
                        end = revenue_span.find('span', {'class': 'end'})

                        if start:
                            start_value = start.text.strip()
                            if end:
                                end_value = end.text.strip()
                                similar_company['revenue_range'] = f"{start_value} - {end_value}"
                            else:
                                similar_company['revenue_range'] = start_value

                    similar_companies.append(similar_company)

        if similar_companies:
            try:
                # Convertir a string JSON con las opciones correctas para PostgreSQL
                result['similar_companies'] = json.dumps(
                    similar_companies,
                    ensure_ascii=False,  # Permitir caracteres Unicode
                    allow_nan=False,     # No permitir NaN/Infinity
                    separators=(',', ':')  # Usar formato compacto
                )
            except Exception as e:
                self._logger.error(f"Error formatting similar companies JSON: {str(e)}")
                result['similar_companies'] = None

        if not result:
            self._logger.warning("No data was extracted from the page")
        else:
            self._logger.info("Successfully extracted data")

        return result

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError),
        max_tries=3,
        max_time=60,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, (httpx.ConnectTimeout, httpx.ReadTimeout))
    )
    async def scrape_url(self, idx: int, url: str) -> tuple[int, Optional[Dict[str, Any]]]:
        """Scrape company information from URL."""
        if not url:
            return idx, None

        try:
            # Determinar qué tipo de URL es
            if 'leadiq.com' in url:
                return await self._scrape_leadiq(idx, url)
            elif 'explorium.ai' in url:
                return await self._scrape_explorium(idx, url)
            else:
                self._logger.warning(f"Unsupported URL domain: {url}")
                return idx, None

        except Exception as e:
            self._logger.error(f"Error scraping {url}: {str(e)}")
            return idx, None

    def _parse_address(self, address: str) -> Dict[str, str]:
        """Parse address string to extract state, zipcode and country."""
        if not address:
            return {
                'address': None,
                'state': None,
                'zipcode': None,
                'country': None
            }

        # Mantener la dirección original
        result = {'address': address}

        # Primera regex para formato completo
        pattern1 = r'^.*,\s+([^,]+?)\s+([\w\s-]+)\s+([A-Z]{2})$'
        # Segunda regex como fallback
        pattern2 = r'^.*,\s*([^,]+?),\s+([\w\s-]+?)\s*([A-Z]{2})'

        try:
            # Intentar con la primera regex
            match = re.search(pattern1, address)
            if not match:
                # Si no hay match, intentar con la segunda
                match = re.search(pattern2, address)

            if match:
                result['state'] = match.group(1).strip()
                result['zipcode'] = match.group(2).strip()
                result['country'] = match.group(3).strip()
            else:
                self._logger.warning(f"Could not parse address: {address}")
                result.update({
                    'state': None,
                    'zipcode': None,
                    'country': None
                })
        except Exception as e:
            self._logger.error(f"Error parsing address {address}: {str(e)}")
            result.update({
                'state': None,
                'zipcode': None,
                'country': None
            })

        return result

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError),
        max_tries=3,
        max_time=60,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, (httpx.ConnectTimeout, httpx.ReadTimeout))
    )
    async def _scrape_explorium(self, idx: int, url: str) -> tuple[int, Optional[Dict[str, Any]]]:
        """Scrape company information from Explorium.ai."""
        # Inicializar el resultado con valores por defecto
        result = {
            'search_term': self.data.iloc[idx].get('search_term', ''),
            'search_url': url,
            'source_platform': 'explorium',
            'company_name': None,
            'logo_url': None,
            'address': None,
            'state': None,
            'zipcode': None,
            'country': None,
            'phone_number': None,
            'website': None,
            'stock_symbol': None,
            'naics_code': None,
            'sic_code': None,
            'employee_count': None,
            'revenue_range': None,
            'similar_companies': None,
            'scrape_status': 'pending'
        }

        try:
            self._logger.notice(f"Scraping Explorium URL: {url}")

            self.headers["User-Agent"] = random.choice(ua)

            # Usar el cliente HTTP con timeout
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await self._get(url, headers=self.headers)

            if response.status_code != 200:
                self._logger.error(f"Failed to fetch URL {url}: {response.status_code}")
                return idx, None

            await asyncio.sleep(random.uniform(1, 3))

            content = response.text
            soup = BeautifulSoup(content, 'html.parser')

            # Extraer nombre de la compañía
            title = soup.find('h1')
            if title:
                result['company_name'] = title.text.strip()

            # Extraer logo si existe
            logo = soup.find('img', {'class': 'company-logo'})  # Ajustar selector según HTML
            if logo:
                result['logo_url'] = logo.get('src')

            # Extraer otros detalles
            details = soup.find_all('div', {'class': 'company-detail'})
            for detail in details:
                label = detail.find('span', {'class': 'label'})
                value = detail.find('span', {'class': 'value'})
                if label and value:
                    label_text = label.text.strip().lower()
                    value_text = value.text.strip()

                    # Mapear campos de Explorium a la estructura de LeadIQ
                    if 'website' in label_text:
                        result['website'] = value_text
                    elif 'location' in label_text:
                        address_info = self._parse_address(value_text)
                        result.update(address_info)
                    elif 'size' in label_text or 'employees' in label_text:
                        result['employee_count'] = value_text
                    elif 'revenue' in label_text:
                        result['revenue_range'] = value_text
                    elif 'naics' in label_text:
                        result['naics_code'] = value_text
                    elif 'sic' in label_text:
                        result['sic_code'] = value_text
                    elif 'phone' in label_text:
                        result['phone_number'] = value_text
                    elif 'stock' in label_text:
                        result['stock_symbol'] = value_text

            # Extraer compañías similares si existen
            similar_section = soup.find('div', {'class': 'similar-companies'})  # Ajustar selector
            if similar_section:
                similar_companies = []
                for company in similar_section.find_all('div', {'class': 'company-card'}):  # Ajustar selector
                    company_name = company.find('h3')
                    if company_name:
                        similar_company = {
                            'name': company_name.text.strip(),
                            'explorium_url': company.find('a')['href'] if company.find('a') else None,
                            'logo_url': company.find('img')['src'] if company.find('img') else None,
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

            if result:
                self._counter += 1
                result['scrape_status'] = 'success'
                return idx, result

            return idx, None

        except httpx.TimeoutException as e:
            self._logger.error(f"Timeout scraping Explorium URL {url}: {str(e)}")
            result['scrape_status'] = 'timeout'
            return idx, result
        except Exception as e:
            self._logger.error(f"Error scraping Explorium URL {url}: {str(e)}")
            result['scrape_status'] = f'error: {str(e)[:50]}'
            return idx, result

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError),
        max_tries=3,
        max_time=60,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, (httpx.ConnectTimeout, httpx.ReadTimeout))
    )
    async def _scrape_leadiq(self, idx: int, url: str) -> tuple[int, Optional[Dict[str, Any]]]:
        """Scrape company information from LeadIQ."""
        # Inicializar el resultado con valores por defecto
        result = {
            'search_term': self.data.iloc[idx].get('search_term', ''),
            'search_url': url,
            'source_platform': 'leadiq',
            'company_name': None,
            'logo_url': None,
            'address': None,
            'state': None,
            'zipcode': None,
            'country': None,
            'phone_number': None,
            'website': None,
            'stock_symbol': None,
            'naics_code': None,
            'sic_code': None,
            'employee_count': None,
            'revenue_range': None,
            'similar_companies': None,
            'scrape_status': 'pending'
        }

        try:
            self._logger.notice(f"Scraping LeadIQ URL: {url}")

            self.headers["User-Agent"] = random.choice(ua)

            # Usar el cliente HTTP con timeout
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await self._get(url, headers=self.headers)

            if response.status_code != 200:
                self._logger.error(f"Failed to fetch URL {url}: {response.status_code}")
                return idx, None

            await asyncio.sleep(random.uniform(1, 3))

            content = response.text
            soup = BeautifulSoup(content, 'html.parser')

            # Get company name and logo URL from logo image
            logo = soup.find('img', {'alt': True, 'width': '76.747'})
            if logo:
                result['company_name'] = logo.get('alt')
                result['logo_url'] = logo.get('src')

            # Get company revenue range from highlight-right section
            highlight_right = soup.find('div', {'class': 'highlight-right'})
            if highlight_right:
                revenue_span = highlight_right.find('span', {'class': 'start'})
                if revenue_span:
                    start_value = revenue_span.text.strip()
                    end_span = revenue_span.find_next_sibling('span', {'class': 'end'})
                    if end_span:
                        end_value = end_span.text.strip()
                        result['revenue_range'] = f"{start_value} - {end_value}"
                    else:
                        result['revenue_range'] = start_value

            # First find the highlight-left section that contains company info
            highlight_left = soup.find('div', {'class': 'highlight-left'})
            if not highlight_left:
                self._logger.warning("Could not find highlight-left section")
                return result

            # Then find the card span within highlight-left
            overview_section = highlight_left.find('div', {'class': 'card span'})
            if not overview_section:
                return result

            # Extract information from dl/dt/dd elements
            dl_element = overview_section.find('dl')
            if dl_element:
                for item in dl_element.find_all('div', {'class': 'item'}):
                    dt = item.find('dt')
                    dd = item.find('dd')
                    if dt and dd:
                        field = dt.text.strip().lower()
                        value = dd.text.strip()

                        # Map fields to our column names
                        if field == 'headquarters':
                            address_info = self._parse_address(value)
                            result.update(address_info)
                        elif field == 'phone number':
                            phone = value.replace('****', '0000')
                            result['phone_number'] = phone
                        elif field == 'website':
                            website = dd.find('a')
                            result['website'] = website['href'] if website else value
                        elif field == 'stock symbol':
                            result['stock_symbol'] = value
                        elif field == 'naics code':
                            result['naics_code'] = value
                        elif field == 'employees':
                            result['employee_count'] = value
                        elif field == 'sic code':
                            result['sic_code'] = value

            # Extract similar companies
            similar_companies = []
            similar_section = soup.find('div', {'id': 'similar'})
            if similar_section:
                for company in similar_section.find_all('li'):
                    company_link = company.find('a')
                    if not company_link:
                        continue

                    company_logo = company_link.find('img')
                    company_name = company_link.find('h3')

                    # Find revenue span
                    revenue_spans = company_link.find_all('span')
                    revenue_span = None
                    for span in revenue_spans:
                        if span.find('span', {'class': 'start'}):
                            revenue_span = span
                            break

                    if company_name:
                        similar_company = {
                            'name': company_name.text.strip(),  # No escapamos las comillas
                            'leadiq_url': company_link['href'],
                            'logo_url': company_logo['src'] if company_logo else None,
                        }

                        # Extract revenue range
                        if revenue_span:
                            start = revenue_span.find('span', {'class': 'start'})
                            end = revenue_span.find('span', {'class': 'end'})

                            if start:
                                start_value = start.text.strip()
                                if end:
                                    end_value = end.text.strip()
                                    similar_company['revenue_range'] = f"{start_value} - {end_value}"
                                else:
                                    similar_company['revenue_range'] = start_value

                        similar_companies.append(similar_company)

            if similar_companies:
                try:
                    # Convertir a string JSON con las opciones correctas para PostgreSQL
                    result['similar_companies'] = json.dumps(
                        similar_companies,
                        ensure_ascii=False,  # Permitir caracteres Unicode
                        allow_nan=False,     # No permitir NaN/Infinity
                        separators=(',', ':')  # Usar formato compacto
                    )
                except Exception as e:
                    self._logger.error(f"Error formatting similar companies JSON: {str(e)}")
                    result['similar_companies'] = None

            if result:
                self._counter += 1
                result['scrape_status'] = 'success'
                return idx, result

            return idx, None

        except httpx.TimeoutException as e:
            self._logger.error(f"Timeout scraping LeadIQ URL {url}: {str(e)}")
            result['scrape_status'] = 'timeout'
            return idx, result
        except Exception as e:
            self._logger.error(f"Error scraping LeadIQ URL {url}: {str(e)}")
            result['scrape_status'] = f'error: {str(e)[:50]}'
            return idx, result

    def _check_company_name(self, company_name: str, title: str, scrapper: Any):
        # Extract the Company Name from the title provided
        pattern = r'\b(' + '|'.join(re.escape(kw) for kw in scrapper.keywords) + r')\b'
        # Search for the first occurrence of any keyword
        match = re.search(pattern, title, re.IGNORECASE)
        if not match:
            return False

        result = title[:match.start()].strip()
        if not result:  # Si result está vacío
            return False

        company = company_name.strip()
        # print('Company Name: ', company_name)
        # print("COMPANY > ", result)
        if company.lower() == result.lower():
            return True

        # second way, normalize names reducing to one element each:
        cp = result.split()[0]
        cp2 = company.split()[0]
        if cp.lower() == cp2.lower():
            return True

        # Check with Fuzzy Search if Company matches.
        score = fuzz.ratio(company.lower(), result.lower())
        if score > 85:
            return True

        return False

    def _standardize_name(self, text: str) -> str:
        """Estandariza el formato del texto: lowercase y guiones en lugar de espacios."""
        # Primero limpiamos caracteres especiales y espacios extras
        cleaned = text.strip().lower().replace(' ', '-')
        return f"\'{cleaned}\'"

    async def search_in_ddg(
        self,
        search_term: str,
        company_name: str,
        scrapper: Any,
        backend: str = 'html',
        region: str = 'wt-wt'
    ):
        """Search for a term in DuckDuckGo."""
        try:
            results = await self._search_duckduckgo(
                search_term,
                use_proxy=True,
                headers=self.headers,
                max_results=10,
                backend=backend,
                region=region,
            )
            if not results:
                raise RuntimeError("Could not find any results")
            if company := self._company_exists(results, company_name, scrapper):
                return company
            else:
                raise RuntimeError(
                    "Could not find a company matching the search term"
                )
        except (RatelimitException, RuntimeError) as e:
            self._logger.warning(f'Search Error: {e}')
            raise RuntimeError('Search Error')

    async def search_in_google(
        self,
        search_term,
        company_name: str,
        scrapper: Any,
        use_selenium: bool = False
    ):
        # Try to find company on Google Search:
        try:
            if use_selenium:
                results = await self.search_google_cse(search_term, max_results=10)
            else:
                try:
                    response = await self._search_google(
                        search_term,
                        use_proxy=True,
                        headers=self.headers,
                        max_results=10,
                        region='us',
                        language='lang_en',
                        country='countryUS'
                    )
                    results = response.get('items', [])
                except (httpx.ConnectError, httpx.RemoteProtocolError, httpx.WriteTimeout) as e:
                    self._logger.warning(
                        f"Connection error with Google API: {str(e)}, trying with Selenium..."
                    )
                    try:
                        results = await self.search_google_cse(search_term, max_results=10)
                    except (RuntimeError, ComponentError):
                        raise RuntimeError("Could not find any results")
            if company := self._company_exists(results, company_name, scrapper):
                return company
            else:
                raise RuntimeError(
                    "Could not find a company matching the search term"
                )
        except RuntimeError as e:
            if str(e) == "No results found":
                self._logger.warning(f"No results found for search term: {search_term}")
            raise RuntimeError(
                "Could not find a company matching the search term"
            )

    def _company_exists(self, results: list, company: str, scrapper: Any):
        # Check if the Company Name is present in the title of the search results.
        for r in results:
            title = r.get('title', None)
            # print('TITLE > ', title)
            if not title:
                continue
            if any(keyword in title for keyword in scrapper.keywords):
                # print('KEYword > ', title)
                if self._check_company_name(company, title, scrapper):
                    self._logger.debug(f"Company Found: {company}")
                    return r
        return None

    async def _search_company(self, idx, row, cookies):
        try:
            async with self._semaphore:
                # Extract the Company Name:
                company_name = row[self.info_column]
                # Let's mark this company as not found.
                row['search_status'] = 'Not Found'
                # Wait a random amount of time between 1 and 2 seconds to avoid
                # DuckDuckGo rate limiting.
                await asyncio.sleep(
                    random.uniform(1, 2)
                )
                # First step, search for Company in DuckDuckGo or fallback in Google (GSE):
                for scrapper in self.scrappers:
                    search_term = scrapper.define_search_term(company_name)
                    ## search_term = scrapper.search_term.format(standardized_term)
                    scrapper.search_term_used = search_term
                    self._logger.notice(f"Searching for: {search_term}")

                    try:
                        company = await self.search_in_ddg(
                            search_term, company_name, scrapper
                        )
                    except RuntimeError as e:
                        self._logger.warning(f'Search Error: {e}')
                        try:
                            company = await self.search_in_google(
                                search_term, company_name, scrapper
                            )
                        except RuntimeError:
                            try:
                                company = await self.search_in_google(
                                    search_term,
                                    company_name,
                                    scrapper,
                                    use_selenium=True
                                )
                            except Exception as e:
                                self._logger.error(f"Search failed: {str(e)}")
                                row['search_status'] = f'Failed: {str(e)}'
                                continue
                    if not company:
                        continue

                    # Second, extract URL from search results:
                    url = company.get('link', None)
                    if not url:
                        url = company.get('href', company.get('url', None))
                    if not url:
                        row['search_status'] = 'URL not found'
                        continue

                    # Limpiar la URL de sufijos no deseados
                    if '/employee-directory' in url:
                        url = url.replace('/employee-directory', '')
                    elif '/email-format' in url:
                        url = url.replace('/email-format', '')

                    try:
                        row['search_url'] = url
                        company_page = await scrapper.get(url, headers=self.headers)
                        if not company_page:
                            continue
                    except (httpx.WriteTimeout, httpx.ConnectError, httpx.RemoteProtocolError, httpx.HTTPError) as e:
                        self._logger.warning(f"HTTP error accessing {url}: {str(e)}")
                        # Intentar con Selenium como fallback
                        try:
                            driver = await self.get_driver()
                            await asyncio.sleep(2)  # Dar tiempo para que la página cargue
                            driver.get(url)
                            company_page_text = driver.page_source
                            company = BeautifulSoup(company_page_text, 'html.parser')
                            _, scraped_data = await scrapper.scrapping(company, idx, row)
                            if scraped_data is not None and scraped_data['scrape_status'] == 'success':
                                row.update(scraped_data)
                                row['search_status'] = f'Found in {scrapper.domain}'
                                return idx, row
                        except Exception as se:
                            self._logger.error(f"Selenium fallback failed: {str(se)}")
                            continue
                        finally:
                            self.close_driver()
                        continue

                    # Third, scrape company information from content:
                    company = BeautifulSoup(company_page.text, 'html.parser')
                    scraped_idx, scraped_data = await scrapper.scrapping(company, idx, row)
                    if scraped_data is not None and scraped_data['scrape_status'] == 'success':
                        await asyncio.sleep(1.5)
                        row.update(scraped_data)
                        row['search_status'] = f'Found in {scrapper.domain}'
                        return idx, row
                # Third, scrape company information from URL:
                row['search_status'] = 'Not Found on any website'
                return idx, row
        except Exception as e:
            # Marcar la fila como fallida y preservar la información
            row['search_status'] = f'Failed: {str(e)}'
            # Crear una excepción que contenga idx y row
            error = RuntimeError(f"Search failed: {str(e)}")
            error.idx = idx
            error.row = row
            raise error

    async def run(self):
        """Execute scraping for each URL in the DataFrame."""
        httpx_cookies = self.get_httpx_cookies(
            domain='leadiq.com', cookies=self.cookies
        )
        scrappers = []
        for scrapper in self.scrappers:
            if scrapper == 'leadiq':
                httpx_cookies = self.get_httpx_cookies(
                    domain='.leadiq.com', cookies=self.cookies
                )
                scp = LeadiqScrapper(
                    cookies=httpx_cookies
                )
                scrappers.append(
                    scp
                )
            if scrapper == 'explorium':
                httpx_cookies = self.get_httpx_cookies(
                    domain='explorium.ai', cookies=self.cookies
                )
                scp = ExploriumScrapper(
                    cookies=httpx_cookies
                )
                scrappers.append(
                    scp
                )
            if scrapper == 'zoominfo':
                httpx_cookies = self.get_httpx_cookies(
                    domain='zoominfo.com', cookies=self.cookies
                )
                scp = ZoomInfoScrapper(
                    cookies=httpx_cookies
                )
                scrappers.append(
                    scp
                )
            if scrapper == 'siccode':
                httpx_cookies = self.get_httpx_cookies(
                    domain='siccode.com', cookies=self.cookies
                )
                scp = SicCodeScrapper(
                    cookies=httpx_cookies
                )
                scrappers.append(
                    scp
                )
            if scrapper == 'rocketreach':
                httpx_cookies = self.get_httpx_cookies(
                    domain='rocketreach.co', cookies=self.cookies
                )
                scp = RocketReachScrapper(
                    cookies=httpx_cookies
                )
                scrappers.append(
                    scp
                )
            if scrapper == 'visualvisitor':
                httpx_cookies = self.get_httpx_cookies(
                    domain='visualvisitor.com', cookies=self.cookies
                )
                scp = VisualVisitorScrapper(
                    cookies=httpx_cookies
                )
                scrappers.append(
                    scp
                )
            # else:
            #     self._logger.warning(
            #         f"Unsupported scrapper: {scrapper}"
            #     )
        # return scrappers list to self.scrappers
        self.scrappers = scrappers
        if not scrappers:
            raise ConfigError(
                "No valid scrappers were found or provided in configuration"
            )
        tasks = [
            self._search_company(
                idx, row, httpx_cookies
            ) for idx, row in self.data.iterrows()
        ]
        companies_info = await self._processing_tasks(tasks)
        self._print_data_(companies_info, 'Company Search Results')

        self._result = companies_info
        return self._result

    async def close(self):
        """Clean up resources."""
        return True

    def _get_error_info(self, error):
        """Extrae idx y row de un error."""
        if hasattr(error, 'idx') and hasattr(error, 'row'):
            return error.idx, error.row
        # Si no podemos obtener la info, crear una fila con información básica
        return None, {'search_status': f'Failed: {str(error)}'}

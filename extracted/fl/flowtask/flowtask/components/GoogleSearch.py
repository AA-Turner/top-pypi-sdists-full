from collections.abc import Callable
import asyncio
import logging
from typing import Optional, List, Dict, Any
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fuzzywuzzy import fuzz
from ..conf import (
    GOOGLE_SEARCH_ENGINE_ID,
    GOOGLE_SEARCH_API_KEY,
    OXYLABS_USERNAME,
    OXYLABS_PASSWORD,
    OXYLABS_ENDPOINT
)
from ..exceptions import ComponentError
from .google import GoogleBase
from bs4 import BeautifulSoup
import random
from urllib.parse import quote
import time
from duckduckgo_search import DDGS
from ..interfaces.http import ua


class GoogleSearch(GoogleBase):
    """
    Google Custom Search Component

    Overview:

    This component performs Google Custom Search queries using the Google Custom Search API.
    It can search for specific queries and return results including URLs, titles, and snippets.
    The component can receive search terms either from a previous component or a list of terms
    specified in the configuration.

    :widths: auto

    | terms (list)          |   No     | List of search terms to use. Required if no previous component provided                             |
    | column (str)          |   No     | Name of the column in the DataFrame when using a previous component                                 |
    | site (str)           |   No     | Optional site restriction for the search (e.g., 'site:example.com')                                 |
    | max_results (int)     |   No     | Maximum number of results to return per search (default: 1)                                         |

    Return:

    The component returns a DataFrame with columns:
    'search_term', 'search_url', 'search_title', 'search_snippet' containing the search results.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          GoogleSearch:
          # attributes here
        ```
    """
    _version = "1.0.0"

    _type: str = 'search'  # Define type at class level

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.site: Optional[str] = kwargs.get('site', 'leadiq.com')  # Valor por defecto
        self.terms: Optional[List[str]] = kwargs.get('terms', None)
        self.max_results: int = kwargs.get('max_results', 10)
        self.engine = kwargs.get('engine', 'google')
        self.fallback_search: bool = kwargs.get('fallback_search', False)  # Nueva opción
        self.api_key = GOOGLE_SEARCH_API_KEY
        self._search_service = None
        self._ddg_service = None
        self._semaphore = asyncio.Semaphore(30)
        self._last_request = 0
        # Configuración de proxy
        self.use_proxy: bool = True
        self._free_proxy: bool = False
        self.headers: dict = {
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(ua)
        }
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    def get_search_service(self):
        """Get the Google Custom Search service."""
        if not self._search_service:
            self._search_service = build(
                "customsearch",
                "v1",
                developerKey=self.api_key
            )
        return self._search_service

    async def get_ddg_service(self):
        """Get the DuckDuckGo search service."""
        try:
            if self._ddg_service:
                # Si ya existe una instancia, cerrarla primero
                self._ddg_service = None

            proxy = None
            if self.use_proxy:
                proxies = await self.get_proxies()
                if proxies and len(proxies) > 0:
                    proxy = f"http://{OXYLABS_USERNAME}:{OXYLABS_PASSWORD}@{OXYLABS_ENDPOINT}"
                    self._logger.info(f"Using proxy: {proxy}")
                else:
                    self._logger.warning("No proxies available, continuing without proxy")

            self._ddg_service = DDGS(proxy=proxy if proxy else None)
            return self._ddg_service

        except Exception as e:
            self._logger.error(f"Error creating DDGS instance: {str(e)}")
            return None

    async def start(self, **kwargs) -> bool:
        """Initialize the component and validate required parameters."""
        self._counter = 0
        self._evaluate_input()  # Use GoogleBase's input evaluation

        # Handle terms list if no previous component
        if not self.previous and self.terms:
            if not isinstance(self.terms, list):
                raise ComponentError(
                    "Terms must be a list of strings"
                )
            # Create DataFrame from terms list
            self.data = pd.DataFrame({'search_term': self.terms})
            self.column = 'search_term'

        if not hasattr(self, 'column'):
            raise RuntimeError(
                'Column attribute is required'
            )

        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Incompatible Pandas DataFrame"
            )

        if not self.api_key:
            raise ComponentError(
                "Google Search API Key is missing"
            )

        if not GOOGLE_SEARCH_ENGINE_ID:
            raise ComponentError(
                "Google Custom Search Engine ID is missing"
            )

        # Initialize result columns if they don't exist
        for col in ['search_url', 'search_title', 'search_snippet']:
            if col not in self.data.columns:
                self.data[col] = None

        return True

    def _build_query(self, query: str) -> str:
        """Build the search query with optional site restriction."""

        if self.site:
            return f"site:{self.site} {query}"
        return query

    def _standardize_name(self, text: str) -> str:
        """Estandariza el formato del texto: lowercase y guiones en lugar de espacios."""
        # Primero limpiamos caracteres especiales y espacios extras
        cleaned = text.strip().lower()
        # Reemplazamos espacios por guiones
        return cleaned.replace(' ', '-')

    def _clean_company_name(self, title: str) -> str:
        """Extrae y estandariza el nombre de la compañía del título."""
        decorators = [
            'Email Formats & Email Address',
            'Company Overview',
            'Employee Directory',
            'Contact Details & Competitors',
            'Email Format'
        ]

        # Tomar la parte antes del primer decorador que encuentre
        clean_name = title
        for decorator in decorators:
            if decorator.lower() in title.lower():  # Hacer la comparación case-insensitive
                clean_name = title.split(decorator)[0]
                break

        return self._standardize_name(clean_name)

    async def search(self, idx: int, row: pd.Series) -> tuple[int, Optional[Dict[str, Any]]]:
        """Perform search using selected engine and return results."""
        async with self._semaphore:
            try:
                search_term = row[self.column]

                if pd.isna(search_term):
                    return idx, {
                        'search_url': None,
                        'search_term': search_term,
                        'search_status': 'invalid_term',
                        'search_engine': self.engine,
                        'is_best_match': False,
                        'match_score': 0
                    }

                # Primer intento con el motor seleccionado
                try:
                    if self.engine == 'duckduckgo':
                        results = await self._search_with_ddg(search_term)
                    else:
                        results = await self._search_with_google(search_term)
                except Exception as e:
                    if not self.fallback_search:
                        self._logger.error(f"Search failed with {self.engine} for {search_term}: {str(e)}")
                        return idx, {
                            'search_url': None,
                            'search_term': search_term,
                            'search_status': f'error_{self.engine}',
                            'search_engine': self.engine,
                            'is_best_match': False,
                            'match_score': 0
                        }

                    self._logger.warning(f"Error with {self.engine} for {search_term}: {str(e)}, trying alternative engine...")
                    try:
                        if self.engine == 'duckduckgo':
                            results = await self._search_with_google(search_term)
                        else:
                            results = await self._search_with_ddg(search_term)
                    except Exception as e2:
                        self._logger.error(f"Both engines failed for {search_term}. Errors: {str(e)}, {str(e2)}")
                        return idx, {
                            'search_url': None,
                            'search_term': search_term,
                            'search_status': f'error_both_engines',
                            'search_engine': 'both',
                            'is_best_match': False,
                            'match_score': 0
                        }

                # Si hay resultados pero el score es bajo, intentar con el otro motor solo si fallback_search está activo
                if self.fallback_search and (not results or (isinstance(results, list) and len(results) > 0 and results[0]['match_score'] < 60)):
                    self._logger.info(f"No good results with {self.engine} for {search_term}, trying alternative engine...")
                    if self.engine == 'duckduckgo':
                        results = await self._search_with_google(search_term)
                    else:
                        results = await self._search_with_ddg(search_term)

                if results:
                    self._counter += 1
                    return idx, results

                return idx, {
                    'search_url': None,
                    'search_term': search_term,
                    'search_status': 'no_results',
                    'search_engine': self.engine if not self.fallback_search else 'both',
                    'is_best_match': False,
                    'match_score': 0
                }

            except Exception as e:
                self._logger.error(f"Unexpected error for {search_term}: {str(e)}")
                return idx, {
                    'search_url': None,
                    'search_term': search_term,
                    'search_status': f'error_unexpected',
                    'search_engine': self.engine if not self.fallback_search else 'both',
                    'is_best_match': False,
                    'match_score': 0
                }

    async def run(self):
        """Execute searches for each query in the DataFrame."""
        tasks = [
            self.search(idx, row) for idx, row in self.data.iterrows()
        ]
        results = await asyncio.gather(*tasks)

        flattened_results = []
        for idx, result_list in results:
            if isinstance(result_list, list) and result_list:
                # Ordenar por match_score
                result_list.sort(key=lambda x: -x['match_score'])
                best_result = result_list[0]

                # Mantener la URL incluso si el match es bajo
                if best_result['match_score'] < 60:
                    flattened_results.append({
                        'search_url': best_result['search_url'],  # Mantener la URL
                        'search_term': best_result['search_term'],
                        'search_status': 'low_match',  # Cambiar el status para indicar match bajo
                        'search_engine': best_result['search_engine'],
                        'match_score': best_result['match_score']
                    })
                else:
                    flattened_results.append(best_result)
            else:
                flattened_results.append(result_list)

        df = pd.DataFrame(flattened_results)

        # Seleccionar solo las columnas necesarias
        columns_to_keep = ['search_url', 'search_term', 'search_status', 'search_engine', 'match_score']
        df = df[columns_to_keep]

        self.add_metric("SEARCHES_COMPLETED", self._counter)

        if self._debug is True:
            print(df)
            print("::: Printing Column Information === ")
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])

        self._result = df
        return self._result

    async def close(self):
        """Clean up resources."""
        if self._ddg_service:
            try:
                # Cerrar la instancia de DDGS si existe
                self._ddg_service = None
            except:
                pass

        if self._search_service:
            try:
                # Cerrar el servicio de Google
                self._search_service = None
            except:
                pass

        return True

    async def search_company(self, idx: int, row: pd.Series) -> tuple[int, Optional[str]]:
        async with self.semaphore:
            try:
                company_name = row[self.company_column]
                if pd.isna(company_name):
                    return idx, None

                query = f'site:{self.site} {company_name}'
                self._logger.notice(f"Searching for: {query}")

                url = f'https://www.google.com/search?q={quote(query)}'
                await self.get_page(url)
                await asyncio.sleep(random.uniform(2, 5))

                content = self._driver.page_source
                soup = BeautifulSoup(content, 'html.parser')

                # Find first LeadIQ URL
                search_results = soup.find_all('div', class_='g')
                for result in search_results:
                    link = result.find('a')
                    if not link:
                        continue

                    url = link.get('href', '')
                    if 'leadiq.com/c/' in url:
                        # Remove /email-format if present
                        url = url.split('/email-format')[0]
                        self._logger.info(f"Found LeadIQ URL for {company_name}: {url}")
                        self._counter += 1
                        return idx, url

                self._logger.warning(f"No LeadIQ URL found for {company_name}")
                return idx, None

            except Exception as e:
                self._logger.error(f"Error searching for {company_name}: {str(e)}")
                return idx, None

    async def _search_with_ddg(self, search_term: str) -> List[Dict]:
        """Perform search using DuckDuckGo."""
        max_retries = 3
        base_delay = 5  # segundos

        for attempt in range(max_retries):
            try:
                # Añadir delay entre búsquedas
                now = time.time()
                elapsed = now - self._last_request
                if elapsed < 2.0:  # Mínimo 2 segundos entre búsquedas
                    await asyncio.sleep(2.0 - elapsed)

                original_term = search_term
                standardized_term = self._standardize_name(search_term)
                query = f"site:{self.site or 'leadiq.com'} {standardized_term}"
                self._logger.info(f"DDG Query: {query}")

                # Rotar proxy en cada intento
                if self.use_proxy:
                    proxies = await self.get_proxies()
                    if proxies:
                        proxy = f"http://{OXYLABS_USERNAME}:{OXYLABS_PASSWORD}@{OXYLABS_ENDPOINT}"
                        self._logger.info(f"Using proxy (attempt {attempt + 1}): {proxy}")
                        self._ddg_service = DDGS(proxy=proxy)

                results = list(self._ddg_service.text(
                    keywords=query,
                    region="wt-wt",
                    max_results=self.max_results,
                    backend='html'
                ))

                self._last_request = time.time()

                # Verificar que hay resultados antes de procesarlos
                if not results:
                    if attempt < max_retries - 1:
                        self._logger.warning(f"No results found for {search_term}, retrying...")
                        continue
                    else:
                        self._logger.warning(f"No results found for {search_term} after {max_retries} attempts")
                        return []

                # Si llegamos aquí, tenemos resultados
                formatted_results = []
                for rank, item in enumerate(results, 1):
                    title = item.get('title', '')
                    url = item.get('href', '')

                    if '/email-format' in url:
                        url = url.split('/email-format')[0]
                    if '/employee-directory' in url:
                        url = url.split('/employee-directory')[0]

                    clean_company_name = self._clean_company_name(title)
                    score = fuzz.ratio(standardized_term, clean_company_name)

                    formatted_results.append({
                        'search_url': url,
                        'search_term': original_term,
                        'search_status': 'success',
                        'match_score': score,
                        'search_engine': 'duckduckgo'
                    })

                if formatted_results:
                    formatted_results.sort(key=lambda x: -x['match_score'])
                    formatted_results[0]['is_best_match'] = True
                    return formatted_results

                return []

            except Exception as e:
                error_msg = str(e)
                if "403 Ratelimit" in error_msg and attempt < max_retries - 1:
                    delay = base_delay * (attempt + 1)
                    self._logger.warning(f"Rate limit hit, waiting {delay} seconds before retry {attempt + 1}")
                    await asyncio.sleep(delay)
                    self._ddg_service = None
                    continue
                else:
                    self._logger.error(f"DuckDuckGo search error for {search_term}: {error_msg}")
                    return []

        return []

    async def _search_with_google(self, search_term: str) -> List[Dict]:
        """Perform search using Google Custom Search."""
        try:
            now = time.time()
            elapsed = now - self._last_request
            if elapsed < 1.0:
                await asyncio.sleep(1.0 - elapsed)

            original_term = search_term
            standardized_term = self._standardize_name(search_term)
            search_query = self._build_query(standardized_term)
            self._logger.notice(f"Searching for: {search_query}")

            try:
                service = self.get_search_service()
                results = service.cse().list(
                    q=search_query,
                    cx=GOOGLE_SEARCH_ENGINE_ID,
                    num=self.max_results
                ).execute()

                self._last_request = time.time()

            except HttpError as e:
                if e.resp.status == 429:
                    self._logger.warning(f"Rate limit exceeded for '{search_term}', waiting 30 seconds")
                    await asyncio.sleep(30)
                    service = self.get_search_service()
                    results = service.cse().list(
                        q=search_query,
                        cx=GOOGLE_SEARCH_ENGINE_ID,
                        num=self.max_results
                    ).execute()
                    self._last_request = time.time()
                else:
                    raise

            if results and 'items' in results:
                formatted_results = []
                for rank, item in enumerate(results['items'], 1):
                    title = item.get('title', '')
                    url = item.get('link', '')

                    if '/email-format' in url:
                        url = url.split('/email-format')[0]
                    if '/employee-directory' in url:
                        url = url.split('/employee-directory')[0]

                    clean_company_name = self._clean_company_name(title)
                    score = fuzz.ratio(standardized_term, clean_company_name)

                    formatted_results.append({
                        'search_url': url,
                        'search_term': original_term,
                        'search_status': 'success',
                        'match_score': score,
                        'search_engine': 'google'
                    })

                if formatted_results:
                    formatted_results.sort(key=lambda x: -x['match_score'])
                    formatted_results[0]['is_best_match'] = True

                return formatted_results

            return []

        except Exception as e:
            self._logger.error(f"Google search error for {search_term}: {str(e)}")
            return []

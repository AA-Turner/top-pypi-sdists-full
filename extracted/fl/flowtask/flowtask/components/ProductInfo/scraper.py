import asyncio
import random
import pandas as pd
from collections.abc import Callable
from duckduckgo_search.exceptions import RatelimitException
from typing import List, Dict, Any, Optional
from tqdm.asyncio import tqdm
from ...exceptions import ComponentError, ConfigError
from ...interfaces import HTTPService, SeleniumService
from ...interfaces.http import ua
from ..flow import FlowComponent
from .parsers import EpsonParser, HPParser, CanonParser, BrotherParser, SamsungParser
from googleapiclient.discovery import build

class ProductInfo(FlowComponent, HTTPService, SeleniumService):
    """
    Product Information Scraper Component

    This component extracts detailed product information by:
    1. Searching for products using search terms
    2. Extracting model codes from URLs
    3. Parsing product details from manufacturer websites

    Configuration options:
    - search_column: Column name containing search terms (default: 'model')
    - parsers: List of parser names to use (default: ['epson'])
    - max_results: Maximum number of search results to process (default: 5)
    - concurrently: Process items concurrently (default: True)
    - task_parts: Number of parts to split concurrent tasks (default: 10)

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ProductInfo:
          # attributes here
        ```
    """
    _version = "1.0.0"
    
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs
    ) -> None:
        self.search_column = kwargs.get('search_column', 'model')
        self.parsers_list = kwargs.get('parsers', ['epson'])
        self.max_results = kwargs.get('max_results', 5)
        self.concurrently = kwargs.get('concurrently', True)
        self.task_parts = kwargs.get('task_parts', 10)
        self.use_proxy = kwargs.get('use_proxy', True)
        self._free_proxy = kwargs.get('free_proxy', False)
        self.google_api_key = kwargs.get('google_api_key')
        self.google_cse = kwargs.get('google_cse')
        
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        
        # Configure headers
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(ua),
            **kwargs.get('headers', {})
        }
        
        # Initialize semaphore for concurrent requests
        self._semaphore = asyncio.Semaphore(10)
    
    async def start(self, **kwargs) -> bool:
        """Initialize component and validate requirements."""
        if self.previous:
            self.data = self.input
            
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Input must be a DataFrame",
                status=404
            )
            
        if self.search_column not in self.data.columns:
            raise ConfigError(
                f"Column '{self.search_column}' not found in DataFrame"
            )
            
        # Initialize result columns
        new_columns = [
            'search_term',
            'search_url',
            'model_code',
            'product_name',
            'price',
            'description',
            'specs',
            'images',
            'search_status',
            'parse_status'
        ]
        
        for col in new_columns:
            if col not in self.data.columns:
                self.data[col] = None
                
        return await super(ProductInfo, self).start(**kwargs)
    
    def split_parts(self, tasks: List, num_parts: int = 5) -> List[List]:
        """Split tasks into parts for concurrent processing."""
        part_size = len(tasks) // num_parts
        remainder = len(tasks) % num_parts
        parts = []
        start = 0
        
        for i in range(num_parts):
            # Distribute remainder across first parts
            end = start + part_size + (1 if i < remainder else 0)
            parts.append(tasks[start:end])
            start = end
            
        return parts
    
    async def _processing_tasks(self, tasks: List) -> pd.DataFrame:
        """Process tasks and format results."""
        results = []
        total_tasks = len(tasks)
        
        with tqdm(total=total_tasks, desc="Processing Products", unit="product") as pbar:
            if not self.concurrently:
                # Sequential processing
                for task in tasks:
                    try:
                        idx, row = await task
                        results.append((idx, row))
                        await asyncio.sleep(random.uniform(0.5, 2))
                    except Exception as e:
                        self._logger.error(f"Task error: {str(e)}")
                        if hasattr(e, 'idx') and hasattr(e, 'row'):
                            results.append((e.idx, e.row))
                    finally:
                        pbar.update(1)
            else:
                # Concurrent processing
                for chunk in self.split_parts(tasks, self.task_parts):
                    chunk_size = len(chunk)
                    chunk_results = await asyncio.gather(*chunk, return_exceptions=True)
                    
                    for result in chunk_results:
                        if isinstance(result, Exception):
                            self._logger.error(f"Task error: {str(result)}")
                            if hasattr(result, 'idx') and hasattr(result, 'row'):
                                results.append((result.idx, result.row))
                        else:
                            results.append(result)
                    
                    pbar.update(chunk_size)
        
        # Process results
        if not results:
            return pd.DataFrame()
        
        indices, data_dicts = zip(*results)
        return pd.DataFrame(data_dicts, index=indices)
    
    async def _search_product(self, idx: int, row: dict) -> tuple:
        """Search for product and extract information."""
        async with self._semaphore:
            # Get search term and retailer
            search_term = row[self.search_column]
            retailer = row.get('retailer')  # Opcional, puede ser None
            
            if not search_term:
                row['search_status'] = 'error: empty search term'
                return idx, row
            
            # Determine which parser to use based on brand
            brand = row.get('brand', '').lower()
            parser = None
            
            if brand == 'epson' and 'epson' in self.parsers_list:
                parser = EpsonParser()
            elif brand == 'hp' and 'hp' in self.parsers_list:
                parser = HPParser()
            elif brand == 'canon' and 'canon' in self.parsers_list:
                parser = CanonParser()
            elif brand == 'brother' and 'brother' in self.parsers_list:
                parser = BrotherParser()
            elif brand == 'samsung' and 'samsung' in self.parsers_list:
                parser = SamsungParser()
            elif retailer:  # Set retailer info before any operations
                parser = CanonParser()
                parser.retailer = retailer
                parser.region = parser.determine_region(retailer)
            
            # If no matching parser for brand, try all parsers
            if not parser:
                # Initialize all parsers as before
                parsers = []
                for parser_name in self.parsers_list:
                    if parser_name == 'epson':
                        parsers.append(EpsonParser())
                    elif parser_name == 'hp':
                        parsers.append(HPParser())
                    elif parser_name == 'canon':
                        parsers.append(CanonParser())
                    elif parser_name == 'brother':
                        parsers.append(BrotherParser())
                    elif parser_name == 'samsung':
                        parsers.append(SamsungParser())
                    # Add more parsers here as they are implemented
                
                if not parsers:
                    row['search_status'] = 'error: no valid parsers'
                    return idx, row
            else:
                # Use only the brand-specific parser
                parsers = [parser]
            
            # Try each parser (either brand-specific or all available)
            for parser in parsers:
                try:
                    # Create search query
                    query = parser.create_search_query(search_term)
                    row['search_term'] = query
                    
                    # Usar Google directamente como en CompanyScraper
                    google_results = None
                    try:
                        # Obtener resultados de Google
                        google_config = {
                            'api_key': self.google_api_key,
                            'cse_id': self.google_cse,
                            'num': self.max_results
                        }
                        
                        google_search = build(
                            "customsearch", "v1",
                            developerKey=google_config['api_key']
                        )
                        
                        google_results = google_search.cse().list(
                            q=query,
                            cx=google_config['cse_id'],
                            num=google_config['num']
                        ).execute()
                        
                        search_results = google_results.get('items', [])
                        
                        if not search_results:
                            self._logger.warning(f"No search results for: {query}")
                            continue
                        
                        # Format search results
                        formatted_results = []
                        for item in search_results:
                            formatted_results.append({
                                'title': item.get('title', ''),
                                'link': item.get('link', ''),
                                'snippet': item.get('snippet', '')
                            })
                        
                        search_results = formatted_results
                        
                    except Exception as e:
                        self._logger.error(f"Google search error: {str(e)}")
                        row['search_status'] = f'error: search failed - {str(e)}'
                        continue
                    
                    # Get product URLs
                    product_urls = parser.get_product_urls(search_results, self.max_results)
                    if not product_urls:
                        self._logger.warning(f"No matching URLs found for: {query}")
                        continue
                    
                    # Process each URL
                    for url in product_urls:
                        # Extract model code (puede ser None para algunos parsers)
                        model_code = parser.extract_model_code(url)
                        
                        # Store in row
                        row['search_url'] = url
                        row['model_code'] = model_code  # Podría ser None aquí
                        row['search_status'] = 'success'
                        
                        # Parse additional product details - el modelo se extraerá durante este paso para parsers sin model_pattern
                        try:
                            product_info = await parser.parse(url, search_term, retailer)
                            if product_info and product_info['parse_status'] == 'success':
                                # Update with detailed information
                                for key, value in product_info.items():
                                    if key != 'search_term' and key != 'search_url':
                                        row[key] = value
                        except Exception as parse_error:
                            self._logger.error(f"Error parsing product details: {str(parse_error)}")
                            row['parse_status'] = f'error: {str(parse_error)}'
                        
                        # Return after first successful match
                        return idx, row
                
                except Exception as e:
                    self._logger.error(f"Error searching with {parser.__class__.__name__}: {str(e)}")
                    continue
            
            # If we get here, no successful matches were found
            row['search_status'] = 'not found'
            return idx, row
    
    async def run(self):
        """Execute product info extraction for each row."""
        # Create tasks for each row
        tasks = [
            self._search_product(idx, row.to_dict())
            for idx, row in self.data.iterrows()
        ]
        
        # Process tasks
        result_df = await self._processing_tasks(tasks)
        
        # Output results
        self._result = result_df
        return self._result
    
    async def close(self):
        """Clean up resources."""
        return True 
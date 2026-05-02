from collections.abc import Callable, List
import asyncio
import random
import pandas as pd
from tqdm.asyncio import tqdm
from ...exceptions import ComponentError, ConfigError
from ...interfaces import HTTPService, SeleniumService
from ...interfaces.http import ua
from ..flow import FlowComponent
from .parsers import (
    BestBuyScrapper,
    LowesScrapper,
)


class ProductCompetitors(FlowComponent, SeleniumService, HTTPService):
    """
    Product Competitors Scraper Component

    Overview:
    Pluggable component for scraping product information from competitors (BestBuy and Lowes).

    Properties:
    - url_column (str): Name of the column containing URLs to scrape (default: 'url')
    - account_name_column (str): Name of the column containing retailer name (default: 'account_name')
    - product_id_column (str): Name of the column containing product IDs (default: 'product_id')
    - competitors (list): List of competitor brands to search for (e.g. ['Insignia', 'TCL', 'LG', 'Sony', 'Samsung'])

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ProductCompetitors:
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
        self.info_column: str = kwargs.get('url_column', 'url')
        self.account_column: str = kwargs.get('account_name_column', 'account_name')
        self.product_id_column: str = kwargs.get('product_id_column', 'product_id')
        self.competitors: List[str] = kwargs.get('competitors', ['Insignia', 'TCL', 'LG', 'Sony', 'Samsung'])
        self.competitors_bucket = {comp: [] for comp in self.competitors}
        self.scrapper_class: Callable = None
        self._scrapper_func: str = 'product_information'
        self.use_proxy = True
        self._free_proxy = False
        self.paid_proxy = True
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self.concurrently: bool = kwargs.get('concurrently', False)
        self.task_parts: int = kwargs.get('task_parts', 10)
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
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

    def _get_scrapper(self, account_name: str):
        """Get the appropriate scrapper based on account name."""
        try:
            if account_name == "Best Buy":
                return BestBuyScrapper()
            elif account_name == "Lowe's":
                return LowesScrapper()
            else:
                return None
        except Exception as err:
            self._logger.error(f"Error while getting scrapper: {err}")
            raise ConfigError(f"Error while getting scrapper: {err}")

    async def start(self, **kwargs) -> bool:
        """Initialize the component and validate required parameters."""
        if self.previous:
            self.data = self.input

        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError("Input must be a DataFrame", status=404)

        required_columns = [self.info_column, self.account_column, self.product_id_column]
        for col in required_columns:
            if col not in self.data.columns:
                raise ConfigError(f"Column {col} not found in DataFrame")

        return True

    async def _start_scrapping(self, idx, row):
        """Handle scraping for a single row."""
        try:
            async with self._semaphore:
                url = row[self.info_column]
                account_name = row[self.account_column]
                
                self._logger.debug(f"Scraping URL: {url} for {account_name}")
                
                scrapper = self._get_scrapper(account_name)
                if not scrapper:
                    self._logger.error(f"No scrapper found for {account_name}")
                    return idx, row

                async with scrapper as s:
                    response = await s.get(url, headers=self.headers)
                    if response:
                        try:
                            idx, row = await s.product_information(response, idx, row)
                        except Exception as err:
                            self._logger.error(f"Scraping error: {err}")
                            return idx, row
                return idx, row
        except Exception as err:
            self._logger.error(f"Error while scraping: {err}")
            raise ComponentError(f"Error while scraping: {err}")

    async def run(self):
        """Execute scraping for all URLs in the DataFrame."""
        tasks = [
            self._start_scrapping(idx, row)
            for idx, row in self.data.iterrows()
        ]
        
        results = []
        total_tasks = len(tasks)
        
        with tqdm(total=total_tasks, desc="Scraping Progress", unit="task") as pbar:
            if not self.concurrently:
                for task in tasks:
                    try:
                        idx, row = await task
                        results.append((idx, row))
                        await asyncio.sleep(random.uniform(0.25, 1.5))
                    except Exception as e:
                        self._logger.error(f"Task error: {str(e)}")
                    finally:
                        pbar.update(1)
            else:
                for chunk in self.split_parts(tasks, self.task_parts):
                    chunk_results = await asyncio.gather(*chunk, return_exceptions=True)
                    results.extend(chunk_results)
                    pbar.update(len(chunk))

        if not results:
            return pd.DataFrame()

        indices, data_dicts = zip(*results)
        df = pd.DataFrame(data_dicts, index=indices)
        self._result = df
        self._print_data_(self._result, 'Competitor Scraping Results')
        return self._result

    async def close(self):
        """Clean up resources."""
        return True 
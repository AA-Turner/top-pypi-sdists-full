from abc import abstractmethod
from typing import Any, List
import pandas as pd
from bs4 import BeautifulSoup as bs
from ....interfaces import SeleniumService, HTTPService
import logging

class ProductCompetitorsBase(SeleniumService, HTTPService):
    """
    ProductCompetitorsBase Model.
    Define how competitor product scrappers should work.
    """
    url: str = ''
    domain: str = ''
    cookies: Any = None
    # Columnas estándar que todos los parsers deben retornar
    standard_columns: List[str] = [
        'competitor_brand',
        'competitor_name',
        'competitor_url',
        'competitor_sku',
        'competitor_price',
        'competitor_rating',
        'competitor_reviews'
    ]

    def __init__(self, *args, **kwargs):
        self._driver = None
        self.cookies = kwargs.get('cookies', None)
        self._logger = logging.getLogger(self.__class__.__name__)
        self.url = kwargs.get('url', self.url)
        self.use_proxy = True
        self._free_proxy = False
        super().__init__(*args, **kwargs)

    def get_bs(self, response: object) -> Any:
        if isinstance(response, str):
            return bs(response, 'html.parser')
        return bs(response.text, 'html.parser')

    async def get(self, url: str, headers: dict = None):
        try:
            await self.get_page(url=url)
            return self._driver.page_source
        except Exception as err:
            self._logger.error(f'Error getting page: {err}')
            return None

    def set_columns(self, df: pd.DataFrame) -> None:
        for col in self.standard_columns:
            if col not in df.columns:
                df[col] = None

    @abstractmethod
    async def connect(self):
        """Creates the Driver and Connects to the Site."""

    @abstractmethod
    async def disconnect(self):
        """Disconnects the Driver and closes the Connection."""

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.disconnect()

    def set_empty_values(self, row: dict, brand: str) -> None:
        """Set empty values for all standard columns for a given brand"""
        for col in self.standard_columns:
            row[f"{col}_{brand}"] = None 
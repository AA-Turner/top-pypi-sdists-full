import asyncio
from typing import Any, List, Dict
from abc import abstractmethod
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)
from ....interfaces import SeleniumService, HTTPService
import re
import logging

class ScrapperBase(SeleniumService, HTTPService):
    """
    ScrapperBase Model.


    Define how scrappers should be work.-
    """
    url: str = ''
    domain: str = ''
    cookies: Any
    expected_columns: List[str] = []

    def __init__(self, *args, **kwargs):
        self._driver = None
        self.cookies = kwargs.get('cookies', None)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._counter: int = 0
        self.search_term_used: str = ''
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
            try:
                await asyncio.sleep(1)
                await self.get_page(url=url)
                # Driver Wait until body is available:
                # WebDriverWait(self._driver, 10).until(
                #     EC.presence_of_element_located((By.TAG_NAME, 'body'))
                # )
                return self._driver.page_source
            except TimeoutException:
                return None
        except Exception as err:
            self._logger.error(f'Error getting page: {err}')
            return None

    async def get_http(self, url, headers: dict = None):
        return await self._get(url, headers=headers, use_proxy=True)

    async def start(self):
        """Starts de Navigation to Main Site.
        """
        if self.url:
            response = await self.get(self.url)
            return response
        return True

    def set_columns(self, df: pd.DataFrame) -> None:
        for col in self.expected_columns:
            if col not in df.columns:
                df[col] = None

    @abstractmethod
    async def connect(self):
        """Creates the Driver and Connects to the Site.
        """

    @abstractmethod
    async def disconnect(self):
        """Disconnects the Driver and closes the Connection.
        """

    # Context Manager:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.disconnect()

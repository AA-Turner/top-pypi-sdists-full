from typing import Any
from collections.abc import Callable
import asyncio
import httpx
from pandas import DataFrame
from navconfig.logging import logging
from ..exceptions import (
    ConfigError,
    ComponentError,
    NotSupported,
)

from .flow import FlowComponent
from ..interfaces import SeleniumService
from ..interfaces import HTTPService

logging.getLogger(name='selenium.webdriver').setLevel(logging.WARNING)
logging.getLogger(name='WDM').setLevel(logging.WARNING)
logging.getLogger(name='hpack').setLevel(logging.WARNING)

def on_backoff(details):
    logging.warning(
        f"Backing off {details['wait']:0.1f} seconds after {details['tries']} tries due to error: {details['exception']}"
    )

def bad_gateway_exception(exc):
    """Check if the exception is a 502 Bad Gateway error."""
    return isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 502


class ReviewScrapper(FlowComponent, SeleniumService, HTTPService):
    """
    ReviewScrapper.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ReviewScrapper:
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
    ):
        self._fn = kwargs.pop('type', None)
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self.task_parts: int = kwargs.get('task_parts', 10)
        if not self._fn:
            raise ConfigError(
                f"{self.__name__}: require a `type` Function to be called, ex: availability"
            )
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def get_cookies(self, url: str) -> dict:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        cookies = driver.get_cookies()
        driver.quit()
        return {cookie['name']: cookie['value'] for cookie in cookies}

    def chunkify(self, lst, n):
        """Split list lst into chunks of size n."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def column_exists(self, column: str, default_val: Any = None):
        if column not in self.data.columns:
            self._logger.warning(
                f"Column {column} does not exist in the Dataframe"
            )
            self.data[column] = default_val
            return False
        return True

    async def run(self):
        # we need to call the "function" for Services.
        fn = getattr(self, self._fn)
        result = None
        if not callable(fn):
            raise ComponentError(
                f"{self.__name__}: Function {self._fn} doesn't exists."
            )
        try:
            result = await fn()
        except (ComponentError, TimeoutError, NotSupported):
            raise
        except Exception as exc:
            raise ComponentError(
                f"{self.__name__}: Unknown Error: {exc}"
            ) from exc
        # Print results
        print(result)
        print("::: Printing Column Information === ")
        for column, t in result.dtypes.items():
            print(column, "->", t, "->", result[column].iloc[0])
        self._result = result
        return self._result

    async def close(self, **kwargs) -> bool:
        self.close_driver()
        return True

    async def start(self, **kwargs) -> bool:
        await super(ReviewScrapper, self).start(**kwargs)
        if self.previous:
            self.data = self.input
            if not isinstance(self.data, DataFrame):
                raise ComponentError(
                    "Incompatible Pandas Dataframe"
                )
        self.api_token = self.get_env_value(self.api_token) if hasattr(self, 'api_token') else self.get_env_value('TARGET_API_KEY')  # noqa
        if not hasattr(self, self._fn):
            raise ConfigError(
                f"{self.__name__}: Unable to found Function {self._fn} in Component."
            )

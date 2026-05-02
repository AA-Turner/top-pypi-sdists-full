import asyncio
from collections.abc import Callable
from bs4 import BeautifulSoup
import urllib
import pandas as pd
from ..exceptions import ComponentError
from .flow import FlowComponent
from ..interfaces.http import HTTPService


class ProductPricing(HTTPService, FlowComponent):
    """
    ProductPricing.

    Overview

        This component Get the price of a list of products

       :widths: auto


    |  column      |   Yes    | Set the column in dataframe used as term search                   |
    |  price_column|   No     | name of the price column                                          |

    Return the prices in a column of dataframe

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ProductPricing:
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
        """Init Method."""
        self.column: str = None
        self.price_column: str = 'price'
        self.accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8'
        self.credentials = None
        super(ProductPricing, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        HTTPService.__init__(self, **kwargs)

    async def start(self, **kwargs):
        # Si lo que llega no es un DataFrame de Pandas se cancela la tarea
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found")
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError('Incompatible Pandas Dataframe')
        if not self.column:
            raise ComponentError('A column is necessary')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Host': 'www.amazon.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1'
        }

    async def close(self):
        pass

    async def pricing(self, model):
        model = urllib.parse.quote_plus(str(model))
        self._base_url = f'https://www.amazon.com/s?k={model}&s=relevanceblender'
        args = {
            "url": self._base_url,
            "method": "get"
        }
        response, error = await self.async_request(**args)

        if not error:
            soup = BeautifulSoup(response, 'html.parser')
            content = soup.find('div', class_='s-desktop-content')
            items = content.find_all('div', {'data-component-type': 's-search-result'})
            for item in items:
                sponsored = False if item.find('span', class_='puis-sponsored-label-info-icon') is None else True
                if not sponsored:
                    price = item.find('span', class_='a-offscreen')
                    if price is not None:
                        self._logger.info(f'{model} -> {price.text}')
                        return price.text.replace('$', '')
        else:
            return None

    async def run(self):
        try:
            prices = []
            df = self.data[self.column].drop_duplicates().to_frame()
            for model in df[self.column]:
                price = await self.pricing(model)
                prices.append(price)
            df[self.price_column] = prices
            df_merged = pd.merge(self.data, df, on=self.column, how='left')
            self.add_metric("NUMROWS", len(df.index))
            self._result = df_merged
            return self._result
        except Exception as err:
            raise ComponentError(f"Error in ProductPricing: {err}") from err

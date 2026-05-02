"""RESTClient.

Basic component for making RESTful queries to URLs.


        Example:

        ```yaml
        RESTClient:
          url: https://api.upcdatabase.org/product/{barcode}
          barcode: '0111222333446'
          credentials:
            apikey: UPC_API_KEY
          as_dataframe: true
        ```

    """
import asyncio
from abc import ABC
from typing import List, Dict, Union
from collections.abc import Callable
from urllib.parse import urlencode
from navconfig.logging import logging
from ..exceptions import DataNotFound, ComponentError
from .HTTPClient import HTTPClient


class RESTClient(HTTPClient):
    """
    RESTClient

    Overview

        The RESTClient class is a component for making RESTful queries to URLs. It extends the HTTPClient class and provides
        functionality to send requests and process responses from REST APIs. It supports creating DataFrames from JSON responses
        if specified.

    :widths: auto

        | _result          |   No     | The result of the REST query, can be a list or dictionary.                                        |
        | accept           |   No     | The accepted response type, defaults to "application/json".                                       |
        | url              |   Yes    | The URL to send the REST query to.                                                                |
        | method           |   No     | The HTTP method to use for the request, defaults to the method specified in the class.            |

    Return

        The methods in this class manage the execution of RESTful queries and handle the response. It includes functionality to
        convert JSON responses into DataFrames if specified.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          RESTClient:
          url: https://api.upcdatabase.org/product/{barcode}
          barcode: '0111222333446'
          credentials:
          apikey: UPC_API_KEY
          as_dataframe: true
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
        """Init Method."""
        self._result: Union[List, Dict] = None
        self._data: dict = kwargs.pop("data", {})
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        self.accept: str = "application/json"  # by default

    async def run(self):
        self.url = self.build_url(
            self.url,
            args=self.arguments,
            queryparams=urlencode(self.parameters)
        )
        try:
            if self.use_async is True:
                result, error = await self.async_request(
                    url=self.url,
                    method=self.method,
                    data=self._data
                )
            else:
                result, error = await self.request(
                    url=self.url,
                    method=self.method,
                    data=self._data
                )
            if not result:
                raise DataNotFound(f"Data was not found on: {self.url}")
            elif error is not None:
                if isinstance(error, BaseException):
                    raise error
                else:
                    raise ComponentError(f"RESTClient Error: {error}")
        except Exception as err:
            logging.exception(err, stack_info=True)
            raise ComponentError(f"RESTClient Error: {err}") from err
        # at here, processing Result
        if self.as_dataframe is True:
            try:
                result = await self.create_dataframe(result)
            except Exception as err:
                raise ComponentError(f"RESTClient Error: {err}") from err
        self._result = result
        return self._result


class AbstractREST(RESTClient):
    """
    AbstractREST.
    Abstract Method for RESTful Components.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          RESTClient:
          url: https://api.upcdatabase.org/product/{barcode}
          barcode: '0111222333446'
          credentials:
          apikey: UPC_API_KEY
          as_dataframe: true
        ```
    """
    _version = "1.0.0"

    _default_method: str = None
    base_url: str = None

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        """Init Method."""
        self._result: Union[List, Dict] = None
        self.url: str = None
        self._method: str = kwargs.pop('method', self._default_method)
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        self.accept: str = "application/json"  # by default
        self._args = self._params

    async def start(self, **kwargs):
        if not hasattr(self, self._method):
            raise ComponentError(
                f"{self.__name__} Error: has no Method {self._method}"
            )
        await super(AbstractREST, self).start(**kwargs)

    async def run(self):
        method = getattr(self, self._method)
        try:
            await method()
        except Exception as err:
            logging.exception(err, stack_info=True)
            raise ComponentError(
                f"{self.__name__}: Error calling Method {self._method}: {err}"
            ) from err
        self.url = self.build_url(
            self.url,
            args=self.arguments,
            queryparams=urlencode(self.parameters)
        )
        try:
            if self.use_async is True:
                result, error = await self.async_request(
                    url=self.url,
                    method=self.method,
                    data=self._data
                )
            else:
                result, error = await self.request(
                    url=self.url,
                    method=self.method,
                    data=self._data
                )
            if self._debug:
                print(result)
            if not result:
                raise DataNotFound(
                    f"Data was not found on: {self.url}"
                )
            elif error is not None:
                if isinstance(error, BaseException):
                    raise error
                else:
                    raise ComponentError(f"HTTPClient Error: {error}")
            # at here, processing Result
            if self.as_dataframe is True:
                try:
                    result = await self.create_dataframe(result)
                    if self._debug is True:
                        print(result)
                        print("::: Printing Column Information === ")
                        for column, t in result.dtypes.items():
                            print(column, "->", t, "->", result[column].iloc[0])
                except Exception as err:
                    raise ComponentError(f"HTTPClient Error: {err}") from err
            self._result = result
            return self._result
        except Exception as err:
            logging.exception(err, stack_info=True)
            raise ComponentError(f"HTTPClient Error: {err}") from err

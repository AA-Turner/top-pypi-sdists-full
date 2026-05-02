"""Basic HTTP Connection Request.

        Example:

        ```yaml
        HTTPClient:
          Group: ICIMSDownload
          url: https://api.icims.com/customers/{customer_id}/forms/{form_data_id}.txt
          customer_id: '5674'
          form_data_id: '1731'
          form_id: '1823'
          associate_id: '518491'
          auth_type: basic
          use_proxy: false
          use_async: true
          credentials:
            username: ICIMS_API_USERNAME
            password: ICIMS_API_PASSWORD
          as_dataframe: false
          download: true
          timeout: 360
          destination:
            directory: /home/ubuntu/symbits/icims/files/forms/{associate_id}/
            filename: '{form_id}_{filename}.html'
            overwrite: false
          no_errors:
            '403':
              errorMessage: This form has been disabled
              errorCode: 3
        ```

    """
import asyncio
# configuration and settings
from pathlib import PurePath
from typing import Union
from collections.abc import Callable
from urllib.parse import urlencode
from navconfig import config
from querysource.types import strtobool
from ..exceptions import DataNotFound, ComponentError, FileNotFound
from .DownloadFrom import DownloadFromBase
from ..interfaces.http import HTTPService


class HTTPClient(DownloadFromBase, HTTPService):
    """
    HTTPClient.

    Overview

           UserComponent: (abstract) ->

       :widths: auto

    | start     |   Yes    | It is executed when the component is "initialized",      |
    |           |          | it MUST return TRUE if it does not fail                  |
    | run       |   Yes    | Is the code that will execute the component ,must return TRUE or  |
    |           |          | a content if it does not fail, but fails is declared      |
    | close     |   Yes    | It is used for any cleaning operation                     |


    Return the list of arbitrary days

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          HTTPClient:
          Group: ICIMSDownload
          url: https://api.icims.com/customers/{customer_id}/forms/{form_data_id}.txt
          customer_id: '5674'
          form_data_id: '1731'
          form_id: '1823'
          associate_id: '518491'
          auth_type: basic
          use_proxy: false
          use_async: true
          credentials:
          username: ICIMS_API_USERNAME
          password: ICIMS_API_PASSWORD
          as_dataframe: false
          download: true
          timeout: 360
          destination:
          directory: /home/ubuntu/symbits/icims/files/forms/{associate_id}/
          filename: '{form_id}_{filename}.html'
          overwrite: false
          no_errors:
          '403':
          errorMessage: This form has been disabled
          errorCode: 3
        ```
    """
    _version = "1.0.0"
    accept: str = "application/xhtml+xml"
    port: int = 80

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        # Credentials
        self._user: str = None
        self._pwd: str = None
        # beautiful soup and html parser:
        self._bs: Callable = None
        self._parser: Callable = None
        self._environment = config
        # Return a Dataframe:
        self.as_dataframe: bool = kwargs.pop('as_dataframe', True)
        if isinstance(self.as_dataframe, str):
            self.as_dataframe = strtobool(self.as_dataframe)
        # Data:
        self._data: dict = kwargs.pop("data", {})
        # Credentials:
        self.credentials: dict = kwargs.pop("credentials", {})
        self.method: str = kwargs.pop("method", "get")
        # calling parents
        DownloadFromBase.__init__(
            self,
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        HTTPService.__init__(
            self,
            **kwargs
        )

    async def evaluate_error(
        self, response: Union[str, list], message: Union[str, list, dict]
    ) -> tuple:
        """evaluate_response.

        Check Response status and available payloads.
        Args:
            response (_type_): _description_
            url (str): _description_

        Returns:
            tuple: _description_
        """
        if isinstance(response, list):
            # a list of potential errors:
            for msg in response:
                if message in msg:
                    return True
        if isinstance(response, dict) and "errors" in response:
            errors = response["errors"]
            if isinstance(errors, list):
                for error in errors:
                    try:
                        if message in error:
                            return True
                    except TypeError:
                        if message == error:
                            return True
            else:
                if message == errors:
                    return True
        else:
            if message in response:
                return True
        return False

    def var_replacement(self):
        """
        Replaces variables in the arguments with their corresponding values.
        """
        for key, _ in self.arguments.items():
            if key in self._variables:
                self.arguments[key] = self._variables[key]

    async def start(self, **kwargs):
        """
        Initializes the HTTPClient component, including fetching proxies if necessary.

        :param kwargs: Additional keyword arguments.
        :return: True if initialization is successful.
        """
        if self.use_proxy is True:
            self._proxies = await self.get_proxies()
        self.var_replacement()
        await super(HTTPClient, self).start()
        return True

    async def close(self):
        pass

    async def run(self):
        """
        Executes the HTTPClient component, handling multiple URLs if provided.

        :return: The result of the HTTP request(s).
        """
        if isinstance(self.url, list):
            ## iterate over a list of URLs:
            results = {}
            for url in self.url:
                uri = self.build_url(
                    url, args=self.arguments, queryparams=urlencode(self.parameters)
                )
                try:
                    if self.use_async is True:
                        result, err = await self.async_request(uri, self.method, data=self._data)
                    else:
                        result, error = await self.request(uri, self.method, data=self._data)
                    if not result:
                        raise DataNotFound(
                            f"Data was not found on: {uri}"
                        )
                    if error is not None:
                        if isinstance(error, BaseException):
                            raise error
                        else:
                            raise ComponentError(f"HTTPClient Error: {error}")
                    ## processing results:
                    if hasattr(self, "download"):
                        ## add result to resultset
                        results[result] = True
                        if self._debug:
                            self._logger.debug(f"File Exists > {result}")
                    else:
                        results[result] = result
                except Exception as err:
                    self._logger.exception(err, stack_info=True)
                    raise ComponentError(f"HTTPClient Error: {err}") from err
            ##
            self.add_metric("FILENAME", results)
            self._result = results
            return self._result
        else:
            self.url = self.build_url(
                self.url, args=self.arguments, queryparams=urlencode(self.parameters)
            )
            try:
                if self.use_async is True:
                    result, error = await self.async_request(
                        self.url, self.method, data=self._data
                    )
                else:
                    result, error = await self.request(self.url, self.method, data=self._data)
                if not result:
                    raise DataNotFound(
                        f"Data was not found on: {self.url}"
                    )
                elif error is not None:
                    if hasattr(self, "no_errors"):
                        # check if error is in no_errors
                        return False
                    if isinstance(error, BaseException):
                        raise error
                    else:
                        raise ComponentError(f"HTTPClient Error: {error}")
                # at here, processing Result
                if self.as_dataframe is True:
                    try:
                        result = await self.create_dataframe(result)
                    except Exception as err:
                        raise ComponentError(f"RESTClient Error: {err}") from err
                elif hasattr(self, "download"):
                    # File downloaded, return same as FileExists
                    # TODO: error if result is a BytesIO
                    if isinstance(result, bytes):
                        self._result = result
                    elif isinstance(result, PurePath):
                        file = result
                        self._logger.debug(f" ::: Checking for File: {file}")
                        result = {}
                        if file.exists() and file.is_file():
                            result[file] = True
                            self.setTaskVar("DIRECTORY", file.parent)
                            self.setTaskVar("FILENAME", str(file.name))
                            self.setTaskVar("FILEPATH", file)
                            self.add_metric("FILENAME", file)
                        else:
                            raise FileNotFound(
                                f"FileExists: File Doesn't exists: {file}"
                            )
                self._result = result
                return self._result
            except DataNotFound:
                raise
            except Exception as err:
                self._logger.exception(err, stack_info=True)
                raise ComponentError(f"HTTPClient: {err}") from err

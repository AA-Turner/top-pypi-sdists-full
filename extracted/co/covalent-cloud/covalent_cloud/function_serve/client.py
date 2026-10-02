# Copyright 2024 Agnostiq Inc.

from functools import partial
from typing import Any, AsyncGenerator, Callable, Dict, Generator

import aiohttp
import requests
from aiohttp import ClientResponse
from requests import Response

from covalent_cloud.service_account_interface.auth_config_manager import get_api_key
from covalent_cloud.service_account_interface.client import get_deployment_client

__all__ = ["FunctionServeClient"]


MSG_HOST_NONE = "Address is None. If the deployment status is not ERROR, try `deployment.reload()` or wait for the deployment to be active."


class FunctionServeClient:
    """
    Client for users to interact with a deployed Function Serve API.
    """

    def __init__(self, function_id: str, host: str, token_getter: Callable) -> None:
        """
        Initialize the client.

        Args:
            host: The host of the deployed service.
            token_getter: A function that returns the service auth token.
        """
        self.function_id = function_id
        self.host = host
        self.token_getter = token_getter

    def get_headers(self, **kwargs) -> Dict[str, str]:
        """
        Get the headers for the request.
        """
        headers = {}

        if token := kwargs.pop("token", None):
            headers["x-api-key"] = token
        if api_key := kwargs.pop("api_key", None):
            headers["x-api-key"] = api_key

        return headers

    def teardown(self) -> Response:
        """
        Permanently tear down the deployment.
        Special case - posts to Covalent Function Service (CFS) API.
        Requires Covalent Cloud API key, if key is not saved in local config.
        """
        cfs_api_client = get_deployment_client()
        response = cfs_api_client.put(f"/functions/{self.function_id}/teardown")
        try:
            res = response.json()
            response.raise_for_status()
        except Exception as e:
            print("Response:", response.text)
            raise e
        return res

    def info(self) -> Response:
        """
        Get the deployment info.
        """
        url = f"{self.host}/info"
        headers = self.get_headers(api_key=get_api_key())
        response = requests.post(url, headers=headers, timeout=10)
        try:
            res = response.json()
            response.raise_for_status()
        except Exception as e:
            print("Response:", response.text)
            raise e
        return res

    def make_request_method(
        self,
        route: str,
        method: str,
        streaming: bool,
        is_async: bool,
    ) -> Callable:
        """
        Get a partial function for making requests to a specific route.
        """
        route = route if route.startswith("/") else f"/{route}"

        if streaming and is_async:
            func = partial(self._async_request_streaming, route, method)
        elif streaming:
            func = partial(self._request_streaming, route, method)
        elif is_async:
            func = partial(self._async_request, route, method)
        else:
            func = partial(self._request, route, method)
        return func

    # Generic HTTP request methods for above partials.

    def _request(
        self,
        route: str,
        method: str,
        **data: Any,
    ) -> Response:
        """
        Make synchronous requests to a url.
        """

        if self.host is None or self.host == "None":
            raise ValueError(MSG_HOST_NONE)

        url = f"{self.host}{route}"
        headers = self.get_headers(token=self.token_getter())
        request_kwargs = {
            "method": method,
            "url": url,
            "headers": headers,
            "json": data or {},
            "timeout": None,
        }
        response = requests.request(**request_kwargs)

        try:
            res = response.json()
            response.raise_for_status()
        except Exception as e:
            print("Response:", response.text)
            raise e

        return res

    async def _async_request(
        self,
        route: str,
        method: str,
        **data: Any,
    ) -> ClientResponse:
        """
        Make asynchronous requests to a url.
        """

        if self.host is None or self.host == "None":
            raise ValueError(MSG_HOST_NONE)

        url = f"{self.host}{route}"
        headers = self.get_headers(token=self.token_getter())
        request_kwargs = {
            "method": method,
            "url": url,
            "headers": headers,
            "json": data or {},
        }
        async with aiohttp.ClientSession() as session:
            async with session.request(**request_kwargs) as response:
                try:
                    res = await response.json()
                    response.raise_for_status()
                except Exception as e:
                    print("Response:", await response.text())
                    raise e

                return res

    def _request_streaming(
        self,
        route: str,
        method: str,
        **data: Any,
    ) -> Generator:
        """
        Make synchronous streaming requests to a url.
        """

        if self.host is None or self.host == "None":
            raise ValueError(MSG_HOST_NONE)

        url = f"{self.host}{route}"
        headers = self.get_headers(token=self.token_getter())
        request_kwargs = {
            "method": method,
            "url": url,
            "headers": headers,
            "json": data or {},
            "stream": True,
            "timeout": None,
        }
        response = requests.request(**request_kwargs)

        try:
            response.raise_for_status()
        except Exception as e:
            print("Response:", response.text)
            raise e

        for chunk in response.iter_content():
            yield chunk

    async def _async_request_streaming(
        self,
        route: str,
        method: str,
        **data: Any,
    ) -> AsyncGenerator:
        """
        Make asynchronous streaming requests to a url.
        """

        if self.host is None:
            raise ValueError()

        url = f"{self.host}{route}"
        headers = self.get_headers(token=self.token_getter())
        request_kwargs = {
            "method": method,
            "url": url,
            "headers": headers,
            "json": data or {},
        }
        async with aiohttp.ClientSession() as session:
            async with session.request(**request_kwargs) as response:

                try:
                    response.raise_for_status()
                except Exception as e:
                    print("Response:", await response.text())
                    raise e

                async for chunk in response.content.iter_any():
                    yield chunk

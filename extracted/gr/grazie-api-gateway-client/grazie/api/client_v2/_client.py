import json
import logging
import os
from typing import AsyncIterator, Dict, Iterator, Optional, Union
from urllib.parse import urljoin

import httpx

from grazie.api.client.gateway import AuthType as OldAuthType

from . import exceptions, types
from ._sse import _decode_sse_line

logger = logging.getLogger(__name__)


class ClientBase:
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        auth_type: Union[types.AuthType, OldAuthType] = types.AuthType.USER,
        endpoint: Union[str, types.GatewayEndpoint] = types.GatewayEndpoint.PRODUCTION,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ):
        if api_key is None:
            if (api_key := os.getenv("GRAZIE_JWT_TOKEN")) or (
                api_key := os.getenv("GRAZIE_USER_JWT_TOKEN")
            ):
                auth_type = types.AuthType.USER
            elif api_key := os.getenv("GRAZIE_SERVICE_JWT_TOKEN"):
                auth_type = types.AuthType.SERVICE
            elif api_key := os.getenv("GRAZIE_APPLICATION_JWT_TOKEN"):
                auth_type = types.AuthType.APPLICATION
            else:
                raise ValueError(
                    (
                        "Cannot set jwt token. Either pass it as a constructor param or set GRAZIE_JWT_TOKEN environment variable.\n"
                        "You can obtain user jwt token by going to https://try.ai.intellij.net and copying it by pressing a button in a top right corner."
                    )
                )

        self.api_key = api_key
        self.auth_type = types.AuthType(auth_type.value)
        self.endpoint = endpoint.value if isinstance(endpoint, types.GatewayEndpoint) else endpoint
        self.headers = headers or {}

    def _prepare_headers(self, headers: Optional[Dict[str, str]] = None) -> dict:
        return {
            types.GrazieHeaders.AUTH_TOKEN: self.api_key,
            **self.headers,
            **(headers or {}),
        }

    def _prepare_url(self, path: str) -> str:
        return urljoin(str(self.endpoint), f"{self.auth_type.path}/{path}")

    def _raise_for_status(self, response: httpx.Response):
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise exceptions.ApiStatusError(
                message=f"{e.response.status_code}: {e.response.text}", exc=e
            ) from e


class Client(ClientBase):
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        auth_type: types.AuthType = types.AuthType.USER,
        endpoint: Union[str, types.GatewayEndpoint] = types.GatewayEndpoint.PRODUCTION,
        headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
    ):
        """A wrapper around httpx.Client, with headers / auth / common request and stream handling logic."""
        super().__init__(api_key=api_key, auth_type=auth_type, endpoint=endpoint, headers=headers)
        self.http_client = http_client or httpx.Client()

    def stream(
        self,
        method: str,
        path: str,
        *,
        json=None,
        params=None,
        headers=None,
        raise_for_status: bool = True,
        **kwargs,
    ) -> Iterator[Dict[str, str]]:
        url = self._prepare_url(path)
        headers = self._prepare_headers(headers)

        with self.http_client.stream(
            method, url, json=json, params=params, headers=headers, **kwargs
        ) as response:
            if raise_for_status and response.is_error:
                # For streaming responses we need to first
                # read their content to correctly access response.text
                response.read()
                self._raise_for_status(response)

            for line in response.iter_lines():
                if decoded := _decode_sse_line(line):
                    yield decoded

    def request(
        self,
        method: str,
        path: str,
        *,
        json=None,
        params=None,
        headers=None,
        raise_for_status: bool = True,
        **kwargs,
    ) -> httpx.Response:
        url = self._prepare_url(path)
        headers = self._prepare_headers(headers)

        response = self.http_client.request(
            method,
            url,
            json=json,
            params=params,
            headers=headers,
            **kwargs,
        )
        if raise_for_status:
            self._raise_for_status(response)
        return response


class AsyncClient(ClientBase):
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        auth_type: types.AuthType = types.AuthType.USER,
        endpoint: Union[str, types.GatewayEndpoint] = types.GatewayEndpoint.PRODUCTION,
        headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        """A wrapper around httpx.AsyncClient, with headers / auth / common request and stream handling logic."""
        super().__init__(api_key=api_key, auth_type=auth_type, endpoint=endpoint, headers=headers)
        self.http_client = http_client or httpx.AsyncClient()

    async def stream(
        self,
        method: str,
        path: str,
        *,
        json=None,
        params=None,
        headers=None,
        raise_for_status: bool = True,
        **kwargs,
    ) -> AsyncIterator[Dict[str, str]]:
        url = self._prepare_url(path)
        headers = self._prepare_headers(headers)

        async with self.http_client.stream(
            method, url, json=json, params=params, headers=headers, **kwargs
        ) as response:
            if raise_for_status and response.is_error:
                # For streaming responses we need to first
                # read their content to correctly access response.text
                await response.aread()
                self._raise_for_status(response)
            async for line in response.aiter_lines():
                if decoded := _decode_sse_line(line):
                    yield decoded

    async def request(
        self,
        method: str,
        path: str,
        *,
        json=None,
        params=None,
        headers=None,
        raise_for_status: bool = True,
        **kwargs,
    ) -> httpx.Response:
        url = self._prepare_url(path)
        headers = self._prepare_headers(headers)

        response = await self.http_client.request(
            method,
            url,
            json=json,
            params=params,
            headers=headers,
            **kwargs,
        )
        if raise_for_status:
            self._raise_for_status(response)
        return response

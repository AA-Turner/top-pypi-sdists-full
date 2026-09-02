from __future__ import annotations

import json
from typing_extensions import NotRequired
from typing import (
    Any,
    AsyncIterator,
    Generic,
    Literal,
    Optional,
    TypedDict,
    TypeVar,
    cast,
)
import httpx

from .bridge import AsyncBridge
from .errors import HTTPStatusError
from .options import InternalOptions
from .utils import convert_to_snake_case, parse_link_header

T = TypeVar("T")


class ExposeSSHResult(TypedDict):
    hostname: str
    username: str
    port: int


class PaginationOptions(TypedDict):
    cursor: NotRequired[str | None]
    """The cursor for pagination."""

    limit: NotRequired[int | None]
    """Limit the number of items to return."""


class AsyncPaginatedList(Generic[T]):
    def __init__(
        self,
        client: AsyncConsoleClient,
        items: list[T],
        path: str,
        next_cursor: str | None,
        options: Optional[dict[str, Any]] = None,
    ):
        self._client = client
        self._options = options
        self._path = path

        self.items = items
        """The items in the current page of the paginated list."""

        self.next_cursor = next_cursor
        """The cursor for pagination."""

    async def get_next_page(self) -> AsyncPaginatedList[T] | None:
        if not self.has_more:
            return None

        return await self._client.get_paginated(
            self._path,
            self.next_cursor,
            self._options,
        )

    @property
    def has_more(self) -> bool:
        """Whether there are more items to fetch."""
        return self.next_cursor is not None

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.has_more:
            raise StopAsyncIteration

        next_page = await self.get_next_page()
        if next_page is None:
            raise StopAsyncIteration

        return next_page


class PaginatedList(Generic[T]):
    def __init__(
        self,
        bridge: AsyncBridge,
        async_paginated: AsyncPaginatedList[T],
    ):
        self._bridge = bridge
        self._async_paginated = async_paginated

    def get_next_page(self) -> PaginatedList[T] | None:
        next_page: AsyncPaginatedList[T] | None = self._bridge.run(
            self._async_paginated.get_next_page()
        )
        if next_page is None:
            return None

        return PaginatedList(self._bridge, next_page)

    @property
    def items(self) -> list[T]:
        """The items in the current page of the paginated list."""
        return self._async_paginated.items

    @property
    def next_cursor(self) -> str | None:
        """The cursor for pagination."""
        return self._async_paginated.next_cursor

    @property
    def has_more(self) -> bool:
        """Whether there are more items to fetch."""
        return self._async_paginated.has_more


class AsyncConsoleClient:
    def __init__(self, options: InternalOptions):
        self._options = options
        self._client: httpx.AsyncClient | None = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self._options['token']}",
                }
            )
        return self._client

    async def _request(
        self,
        method: Literal["POST", "GET", "PATCH", "PUT", "DELETE"],
        url: httpx.URL,
        data: Optional[Any] = None,
    ) -> httpx.Response:
        response = await self.client.request(
            method=method, url=url, json=data, timeout=10.0
        )

        if not response.is_success:
            code = "UNKNOWN_ERROR"
            message = f"Request to {url} failed with status {response.status_code}"
            trace_id = response.headers.get("x-deno-trace-id")
            try:
                body = response.json()
                if (
                    isinstance(body, dict)
                    and isinstance(body.get("code"), str)
                    and isinstance(body.get("message"), str)
                ):
                    code = body["code"]
                    message = body["message"]
            except Exception:
                pass
            raise HTTPStatusError(response.status_code, message, code, trace_id)

        return response

    async def post(self, path: str, data: Any) -> dict:
        req_url = self._options["console_url"].join(path)
        response = await self._request("POST", req_url, data)
        return response.json()

    async def patch(self, path: str, data: Any) -> dict:
        req_url = self._options["console_url"].join(path)
        response = await self._request("PATCH", req_url, data)
        return response.json()

    async def get(
        self, path: str, params: Optional[dict[str, str | int]] = None
    ) -> dict:
        req_url = self._options["console_url"].join(path)

        if params is not None:
            req_url = req_url.copy_merge_params(params)

        response = await self._request("GET", req_url)
        return response.json()

    async def get_or_none(
        self, path: str, params: Optional[dict[str, str | int]] = None
    ) -> dict | None:
        try:
            return await self.get(path, params)
        except HTTPStatusError as e:
            if e.status_code == 404:
                return None
            raise

    async def delete(self, path: str) -> httpx.Response:
        req_url = self._options["console_url"].join(path)
        response = await self._request("DELETE", req_url)
        return response

    async def get_paginated(
        self,
        path: str,
        cursor: Optional[str],
        params: Optional[dict[str, Any]] = None,
    ) -> AsyncPaginatedList[T]:
        req_url = self._options["console_url"].join(path)

        if params is not None:
            url_params = cast(dict, params)
            req_url = req_url.copy_merge_params(url_params)

        if cursor is not None:
            req_url = req_url.copy_add_param("cursor", cursor)

        response = await self._request("GET", req_url)
        response.raise_for_status()
        data = response.json()

        next_cursor: str | None = None
        link_header = response.headers.get("link")
        if link_header is not None:
            parsed = parse_link_header(link_header)
            next_cursor = parsed.get("next", None)

        items = [cast(T, convert_to_snake_case(item)) for item in data]

        return AsyncPaginatedList(self, items, path, next_cursor, params)

    async def stream_ndjson(
        self, path: str, params: Optional[dict[str, Any]] = None
    ) -> AsyncIterator[dict]:
        """Stream NDJSON responses line by line.

        Yields parsed JSON objects for each line in the response.
        """
        req_url = self._options["console_url"].join(path)
        if params is not None:
            req_url = req_url.copy_merge_params(params)
        headers = {
            "Accept": "application/x-ndjson",
        }
        async with self.client.stream(
            "GET", req_url, headers=headers, timeout=None
        ) as response:
            if not response.is_success:
                await response.aread()
                code = "UNKNOWN_ERROR"
                message = (
                    f"Request to {req_url} failed with status {response.status_code}"
                )
                trace_id = response.headers.get("x-deno-trace-id")
                try:
                    body = response.json()
                    if (
                        isinstance(body, dict)
                        and isinstance(body.get("code"), str)
                        and isinstance(body.get("message"), str)
                    ):
                        code = body["code"]
                        message = body["message"]
                except Exception:
                    pass
                raise HTTPStatusError(response.status_code, message, code, trace_id)

            async for line in response.aiter_lines():
                line = line.strip()
                if line:
                    yield json.loads(line)

    async def close(self) -> None:
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


__all__ = ["AsyncConsoleClient"]

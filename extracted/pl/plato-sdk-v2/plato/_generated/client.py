"""HTTP client for Plato API."""

from __future__ import annotations

import warnings
from collections.abc import Callable
from typing import Any

import httpx


class Client:
    """Sync HTTP client for Plato API."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
        max_retries: int = 3,
        retry_on_status: tuple[int, ...] = (429, 500, 502, 503, 504),
        on_request: Callable[[httpx.Request], None] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
        **kwargs: Any,
    ):
        """Initialize the HTTP client.

        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            headers: Default headers to include in all requests
            max_retries: Maximum number of retry attempts for failed requests
            retry_on_status: HTTP status codes that trigger a retry
            on_request: Hook called before each request
            on_response: Hook called after each response
            **kwargs: Additional arguments passed to httpx.Client
        """
        self._base_url = base_url.rstrip("/")
        self._headers = headers or {}
        self._max_retries = max_retries
        self._retry_on_status = retry_on_status
        self._closed = False

        event_hooks: dict[str, list[Callable]] = {"request": [], "response": []}
        if on_request:
            event_hooks["request"].append(on_request)
        if on_response:
            event_hooks["response"].append(on_response)

        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=timeout,
            headers=self._headers,
            event_hooks=event_hooks if any(event_hooks.values()) else None,
            **kwargs,
        )

    @property
    def httpx(self) -> httpx.Client:
        """Access the underlying httpx client."""
        return self._client

    @property
    def max_retries(self) -> int:
        """Maximum number of retry attempts."""
        return self._max_retries

    @property
    def retry_on_status(self) -> tuple[int, ...]:
        """HTTP status codes that trigger a retry."""
        return self._retry_on_status

    def close(self) -> None:
        """Close the client."""
        self._closed = True
        self._client.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __del__(self) -> None:
        if not self._closed:
            warnings.warn(
                f"{self.__class__.__name__} was not closed. Use 'with' statement or call 'client.close()'",
                ResourceWarning,
                stacklevel=2,
            )


class AsyncClient:
    """Async HTTP client for Plato API."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
        max_retries: int = 3,
        retry_on_status: tuple[int, ...] = (429, 500, 502, 503, 504),
        on_request: Callable[[httpx.Request], None] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
        **kwargs: Any,
    ):
        """Initialize the async HTTP client.

        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            headers: Default headers to include in all requests
            max_retries: Maximum number of retry attempts for failed requests
            retry_on_status: HTTP status codes that trigger a retry
            on_request: Hook called before each request
            on_response: Hook called after each response
            **kwargs: Additional arguments passed to httpx.AsyncClient
        """
        self._base_url = base_url.rstrip("/")
        self._headers = headers or {}
        self._max_retries = max_retries
        self._retry_on_status = retry_on_status
        self._closed = False

        event_hooks: dict[str, list[Callable]] = {"request": [], "response": []}
        if on_request:
            event_hooks["request"].append(on_request)
        if on_response:
            event_hooks["response"].append(on_response)

        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=timeout,
            headers=self._headers,
            event_hooks=event_hooks if any(event_hooks.values()) else None,
            **kwargs,
        )

    @property
    def httpx(self) -> httpx.AsyncClient:
        """Access the underlying httpx client."""
        return self._client

    @property
    def max_retries(self) -> int:
        """Maximum number of retry attempts."""
        return self._max_retries

    @property
    def retry_on_status(self) -> tuple[int, ...]:
        """HTTP status codes that trigger a retry."""
        return self._retry_on_status

    async def close(self) -> None:
        """Close the client."""
        self._closed = True
        await self._client.aclose()

    async def __aenter__(self) -> AsyncClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    def __del__(self) -> None:
        if not self._closed:
            warnings.warn(
                f"{self.__class__.__name__} was not closed. Use 'async with' statement or call 'await client.close()'",
                ResourceWarning,
                stacklevel=2,
            )

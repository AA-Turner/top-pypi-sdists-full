"""Tracks client."""

import asyncio
import atexit
from typing import TypedDict, Unpack

import aiohttp
from aiolimiter import AsyncLimiter
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from fluidattacks_tracks.auth.base import TracksAuthInterface

TRACKS_API_RATE_LIMIT = {"requests": 1000, "period_seconds": 1}
TRACKS_API_URL = "https://tracks.fluidattacks.com/"


class TracksClientConfig(TypedDict):
    """Tracks client configuration."""

    auth: TracksAuthInterface | None
    concurrency_limit: int
    keepalive_timeout: int
    retry_attempts: int


DEFAULT_CONFIG: TracksClientConfig = {
    "auth": None,
    "concurrency_limit": 100,
    "keepalive_timeout": 60,
    "retry_attempts": 5,
}


class TracksClient:
    """Tracks client."""

    def __init__(self, config: TracksClientConfig | None = None) -> None:
        """Initialize the Tracks client."""
        self._config = config or DEFAULT_CONFIG
        self._runner = asyncio.Runner().__enter__()
        atexit.register(self.close)
        self._session: aiohttp.ClientSession | None = None
        self._limiter = AsyncLimiter(
            max_rate=TRACKS_API_RATE_LIMIT["requests"],
            time_period=TRACKS_API_RATE_LIMIT["period_seconds"],
        )

    def _get_session(self) -> aiohttp.ClientSession:
        """Get the Tracks session."""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                base_url=TRACKS_API_URL,
                connector=aiohttp.TCPConnector(
                    keepalive_timeout=self._config["keepalive_timeout"],
                    limit=self._config["concurrency_limit"],
                ),
                headers={"Accept-Encoding": "gzip"},
            )
        return self._session

    def close(self) -> None:
        """Close the Tracks session."""
        if self._session:
            self._runner.run(self._session.close())
            self._session = None
        self._runner.__exit__(None, None, None)

    async def _request(
        self,
        method: str,
        url: str,
        *,
        authenticated: bool = False,
        **kwargs: Unpack[aiohttp.client._RequestOptions],
    ) -> aiohttp.ClientResponse:
        """Make a request to the Tracks API."""

        @retry(  # type: ignore[misc]
            retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
            stop=stop_after_attempt(self._config["retry_attempts"]),
            wait=wait_exponential(),
        )
        async def _perform_request() -> aiohttp.ClientResponse:
            async with self._limiter:
                session = self._get_session()
                async with session.request(
                    method,
                    url,
                    middlewares=(
                        [self._config["auth"].sign_request]
                        if authenticated and self._config["auth"]
                        else None
                    ),
                    **kwargs,  # type: ignore[misc]
                ) as response:
                    response.raise_for_status()
                    await response.read()
                    return response

        return await _perform_request()

    async def get_async(
        self,
        url: str,
        *,
        authenticated: bool = False,
        **kwargs: Unpack[aiohttp.client._RequestOptions],
    ) -> aiohttp.ClientResponse:
        """Get a request from the Tracks API."""
        return await self._request("GET", url, authenticated=authenticated, **kwargs)  # type: ignore[misc]

    def get(
        self,
        url: str,
        *,
        authenticated: bool = False,
        **kwargs: Unpack[aiohttp.client._RequestOptions],
    ) -> aiohttp.ClientResponse:
        """Get a request from the Tracks API."""
        return self._runner.run(self.get_async(url, authenticated=authenticated, **kwargs))  # type: ignore[misc]

    async def post_async(
        self,
        url: str,
        *,
        authenticated: bool = False,
        **kwargs: Unpack[aiohttp.client._RequestOptions],
    ) -> aiohttp.ClientResponse:
        """Post a request to the Tracks API."""
        return await self._request("POST", url, authenticated=authenticated, **kwargs)  # type: ignore[misc]

    def post(
        self,
        url: str,
        *,
        authenticated: bool = False,
        **kwargs: Unpack[aiohttp.client._RequestOptions],
    ) -> aiohttp.ClientResponse:
        """Post a request to the Tracks API."""
        return self._runner.run(self.post_async(url, authenticated=authenticated, **kwargs))  # type: ignore[misc]

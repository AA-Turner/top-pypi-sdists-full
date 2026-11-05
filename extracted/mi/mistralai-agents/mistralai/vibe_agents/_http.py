"""Private HTTP helpers shared by handwritten vibe_agents SDK clients."""

import asyncio
import math
import random
import re
from collections.abc import Callable, Collection, Mapping
from contextlib import AbstractAsyncContextManager
from http import HTTPMethod
from types import TracebackType
from typing import Any, Self

import httpx

from mistralai.vibe_agents.analytics import EXCLUDE_FROM_ANALYTICS_HEADER
from mistralai.vibe_agents.sdk.app.config import TelemetrySettings, mistral_api_http_proxy
from mistralai.vibe_agents.sdk.authoring.errors import SdkError
from mistralai.vibe_agents.user_agent import USER_AGENT

_DEFAULT_GET_RETRIES = 3
_DEFAULT_GET_RETRY_STATUS_CODES = frozenset({500, 502, 503, 504})
_DEFAULT_TRANSPORT_RETRIES = 2
_RETRY_BACKOFF_SECONDS = 0.05
_MAX_RETRY_DELAY_SECONDS = 60.0
# Raised before the request is written. A read or write timeout, or a reset while the response is in
# flight, can follow a server that already committed, so a caller that must not resend one leaves those out.
_UNSENT_TRANSPORT_ERRORS: tuple[type[httpx.TransportError], ...] = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.PoolTimeout,
)


# A Mistral API key is visible ASCII. httpx refuses a newline or control character in a header only when it
# sends the request, and its error then prints the whole header, key included.
_API_KEY_CHARACTERS = re.compile(r"[\x21-\x7e]*")


def _header_api_key(api_key: str, *, name: str = "The API key") -> str:
    """Return ``api_key`` without surrounding whitespace, or raise ``SdkError`` naming ``name``, never the key."""
    key = api_key.strip()
    if not _API_KEY_CHARACTERS.fullmatch(key):
        raise SdkError(f"{name} contains a space, newline, control or non-ASCII character: copy the key again")
    return key


def _retry_transport_error(error: httpx.TransportError, *, only_unsent: bool) -> bool:
    if not only_unsent:
        return True
    return isinstance(error, _UNSENT_TRANSPORT_ERRORS)


def _client_headers() -> dict[str, str]:
    headers = {"User-Agent": USER_AGENT}
    # Read per client rather than at import, so a caller that sets the switch after importing is honoured.
    if not TelemetrySettings().telemetry_enabled:
        headers[EXCLUDE_FROM_ANALYTICS_HEADER] = "true"
    return headers


def _mistral_api_transport(*, limits: httpx.Limits | None = None) -> httpx.AsyncHTTPTransport:
    """The SDK's own transport to the Mistral API, through ``MISTRAL_API_HTTP_PROXY`` when it is set.

    httpx ignores the proxy environment variables for a client given a transport, so the proxy goes here.
    """
    if limits is None:
        return httpx.AsyncHTTPTransport(retries=_DEFAULT_TRANSPORT_RETRIES, proxy=mistral_api_http_proxy())
    return httpx.AsyncHTTPTransport(
        retries=_DEFAULT_TRANSPORT_RETRIES,
        proxy=mistral_api_http_proxy(),
        limits=limits,
    )


class _InternalHTTPClient:
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str | None = None,
        timeout_seconds: float = 30.0,
        extra_headers: Mapping[str, str] | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
        http_client: httpx.AsyncClient | None = None,
        pool: Callable[[], httpx.AsyncClient | None] | None = None,
    ) -> None:
        """``api_key`` authenticates every request; the server derives the caller's identity from it.

        ``extra_headers`` are sent on every request.

        ``http_client`` is a connection pool to borrow instead of owning one: requests then go to
        ``base_url`` joined with their path, with the SDK's headers, and ``aclose`` leaves it open.
        ``pool`` is asked before each request for the pool to send it through, so a request in a later
        event loop goes through that loop's pool. It raises when its owner cannot serve the request: the
        owner is closed, or, for an ``agents.Client``'s own pool, another thread's running event loop
        uses it. ``None`` keeps ``http_client``, or the pool this client owns.
        """

        # Case-insensitive, so an `authorization` in extra_headers replaces the API key instead of joining it.
        self._default_headers = httpx.Headers()
        if api_key is not None:
            self._default_headers["Authorization"] = f"Bearer {_header_api_key(api_key)}"
        if extra_headers:
            self._default_headers.update(extra_headers)
        self._pool = pool
        self._base_url = base_url.rstrip("/")
        self._borrowed = http_client is not None
        self.client = http_client or httpx.AsyncClient(
            base_url=self._base_url,
            headers=_client_headers(),
            timeout=httpx.Timeout(max(1, math.ceil(timeout_seconds))),
            transport=transport or _mistral_api_transport(),
        )

    async def aclose(self) -> None:
        if not self._borrowed:
            await self.client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def make_request(
        self,
        method: HTTPMethod,
        path: str,
        *,
        ctx: object | None = None,
        retries: int | None = None,
        retries_codes: Collection[int] | None = None,
        ignore_codes: Collection[int] | None = None,
        sensitive: bool = False,
        only_retry_unsent_transport_errors: bool = False,
        **kwargs: Any,
    ) -> httpx.Response:
        del ctx
        del sensitive
        client = self._client()
        if method == HTTPMethod.GET and retries is None:
            retries = _DEFAULT_GET_RETRIES
            retries_codes = retries_codes or _DEFAULT_GET_RETRY_STATUS_CODES

        headers = self._request_headers(kwargs.pop("headers", None))
        retry_statuses = retries_codes or set()
        ignored_statuses = ignore_codes or set()
        attempts = max(0, retries or 0) + 1

        for attempt in range(attempts):
            try:
                response = await client.request(method=method.value, url=self._url(path), headers=headers, **kwargs)
            except httpx.TransportError as error:
                # retries_codes filters statuses only. A transport error is retried whenever attempts
                # remain, unless the caller cannot resend a request that may already have been forwarded.
                if attempt == attempts - 1 or not _retry_transport_error(
                    error, only_unsent=only_retry_unsent_transport_errors
                ):
                    raise
                await self._sleep_before_retry(attempt)
                continue

            if response.status_code in ignored_statuses:
                return response
            if response.status_code not in retry_statuses or attempt == attempts - 1:
                return response

            await self._sleep_before_retry(attempt)

        raise RuntimeError("Unexpected HTTP retry state")

    async def stream(
        self,
        method: HTTPMethod,
        path: str,
        *,
        ctx: object | None = None,
        **kwargs: Any,
    ) -> AbstractAsyncContextManager[httpx.Response]:
        del ctx
        client = self._client()
        headers = self._request_headers(kwargs.pop("headers", None))
        return client.stream(method=method.value, url=self._url(path), headers=headers, **kwargs)

    async def _sleep_before_retry(self, attempt: int) -> None:
        base_delay = _RETRY_BACKOFF_SECONDS * (2**attempt)
        delay = min(base_delay + random.uniform(0, _RETRY_BACKOFF_SECONDS), _MAX_RETRY_DELAY_SECONDS)  # noqa: S311 — jitter, not crypto
        await asyncio.sleep(delay)

    def _client(self) -> httpx.AsyncClient:
        """The connection pool for a request made now."""
        current = self._pool() if self._pool is not None else None
        return current if current is not None and self._borrowed else self.client

    def _url(self, path: str) -> str:
        return f"{self._base_url}{path}" if self._borrowed else path

    def _request_headers(self, explicit_headers: Any) -> dict[str, str]:
        headers = httpx.Headers(_client_headers() if self._borrowed else {})
        headers.update(self._default_headers)
        if explicit_headers:
            headers.update(explicit_headers)
        return dict(headers)

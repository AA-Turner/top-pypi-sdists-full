from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, Optional, Type, TypeVar

import aiohttp
from aiohttp_retry import RetryClient

from . import __version__
from .auth import Authenticator, TableAccess
from .dap_error import DownloadError
from .dap_types import Credentials
from .retry_options import CustomExponentialRetry
from .transport import Transport

T = TypeVar("T")

# applies to both channels: generous overall budget for large transfers,
# short connect timeout so an unreachable host fails fast
CHANNEL_TIMEOUT = aiohttp.ClientTimeout(total=30 * 60, connect=30)


def default_headers(traceparent: str) -> Dict[str, str]:
    "Base headers to send on every request, shared by both channels."

    return {
        "User-Agent": f"DataAccessPlatform/{__version__}",
        "traceparent": traceparent,
    }


class DapApiChannel:
    """
    The authenticated HTTP channel to the DAP API.

    Owns everything needed to talk to the API as one unit: the connection
    pool, the retry policy, the base headers, and the token lifecycle. The
    access level is channel-scoped rather than per-request — `authenticate()`
    pins one that subsequent `get`/`post` calls reuse until it is changed —
    so the token lifecycle and the requests that depend on it belong to the
    same object. Each request is handed the token explicitly; nothing is
    stashed on the connection pool for another object to find.

    :param base_url: The DAP API base URL, without a trailing slash.
    :param credentials: The client credentials to authenticate with.
    :param headers: Base headers to send on every request, excluding the bearer token.
    """

    _http: aiohttp.ClientSession
    _retry_client: RetryClient
    _headers: Dict[str, str]
    _auth: Authenticator
    _transport: Transport

    def __init__(
        self,
        base_url: str,
        credentials: Credentials,
        headers: Dict[str, str],
    ) -> None:
        self._http = aiohttp.ClientSession(timeout=CHANNEL_TIMEOUT)
        self._retry_client = RetryClient(
            client_session=self._http,
            retry_options=CustomExponentialRetry(),
            raise_for_status=False,
        )
        self._headers = dict(headers)
        self._auth = Authenticator(base_url, self._http, credentials, self._headers)
        self._transport = Transport(base_url, self._retry_client, self._headers)

    async def authenticate(self, table_access: Optional[TableAccess] = None) -> None:
        """
        Obtains an access token for `table_access` and pins it as this
        channel's access level for subsequent requests.

        See `Authenticator.authenticate` for the caching and access level rules.

        :param table_access: The table the requested JWT should be restricted to.
            Omit to reuse the most recently used access level on this channel if one
            exists, otherwise a token with no table access is requested.
        """

        await self._auth.authenticate(table_access)

    async def get(
        self,
        path: str,
        response_type: Type[T],
        table_access: Optional[TableAccess] = None,
    ) -> T:
        """
        Authenticates as needed, then sends a GET request.

        :param path: The path component of the endpoint to invoke.
        :param response_type: The object type the endpoint returns on success.
        :param table_access: The namespace/table the request's JWT should be restricted
            to. Omit to reuse the access level currently pinned on this channel.
        :returns: The object returned on success.
        :raises Exception: The object returned on failure.
        """

        token = await self._auth.authenticate(table_access)
        return await self._transport.get(path, response_type, str(token))

    async def post(
        self,
        path: str,
        request_data: Any,
        response_type: Type[T],
        table_access: Optional[TableAccess] = None,
    ) -> T:
        """
        Authenticates as needed, then sends a POST request with a serialized payload.

        :param path: The path component of the endpoint to invoke.
        :param request_data: The object to pass in the request body.
        :param response_type: The object type the endpoint returns on success.
        :param table_access: The namespace/table the request's JWT should be restricted
            to. Omit to reuse the access level currently pinned on this channel.
        :returns: The object returned on success.
        :raises Exception: The object returned on failure.
        """

        token = await self._auth.authenticate(table_access)
        return await self._transport.post(path, request_data, response_type, str(token))

    async def close(self) -> None:
        "Closes the underlying network sockets."

        await self._http.close()


class DownloadChannel:
    """
    The unauthenticated HTTP channel for fetching resource payloads.

    Resource URLs are pre-signed by the DAP API, so they carry their own
    authorization and must not be sent the API bearer token. This channel
    therefore uses a connection pool of its own, entirely separate from
    `DapApiChannel`, and raises on an HTTP error status rather than parsing
    an error body.

    :param headers: Base headers to send on every request, typically the
        user agent and trace identifier shared with the API channel.
    """

    _http: aiohttp.ClientSession
    _retry_client: RetryClient
    _headers: Dict[str, str]

    def __init__(self, headers: Dict[str, str]) -> None:
        self._http = aiohttp.ClientSession(timeout=CHANNEL_TIMEOUT)
        self._retry_client = RetryClient(
            client_session=self._http,
            retry_options=CustomExponentialRetry(),
            raise_for_status=True,
        )
        self._headers = dict(headers)

    @asynccontextmanager
    async def get(self, url: str) -> AsyncIterator[aiohttp.ClientResponse]:
        """
        Fetches a URL, as an asynchronous context manager over the response.

        :param url: The absolute URL to fetch.
        :returns: A context manager yielding the HTTP response, whose `content`
            is a reader over the body.
        :raises DownloadError: The host rejected the request with an HTTP error
            status. This channel is configured with `raise_for_status=True`, so
            aiohttp's `ClientResponseError` is caught and wrapped on entering the
            context manager.
        """

        try:
            async with self._retry_client.get(url, headers=self._headers) as response:
                yield response
        except aiohttp.ClientResponseError as exc:
            raise DownloadError(str(exc)) from exc

    async def close(self) -> None:
        "Closes the underlying network sockets."

        await self._http.close()

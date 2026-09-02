# soap_client.py

import base64
from abc import ABC
from pathlib import Path
from typing import Any, Optional, Union

import httpx
import redis.asyncio as aioredis
from zeep import AsyncClient as ZeepAsyncClient, Settings
from zeep.transports import AsyncTransport as ZeepAsyncTransport

from flowtask.conf import REDIS_URL


class NoProxyAsyncTransport(ZeepAsyncTransport):
    """
    Zeep AsyncTransport subclass that:
    - Omits 'proxies=' when building the sync httpx.Client (avoids httpx>=0.28 errors).
    - Provides the attributes Zeep expects (client, logger, _close_session).
    - Disables automatic session close in destructor to avoid AsyncClient.close errors.
    """
    def __init__(
        self,
        client: httpx.AsyncClient,
        cache: Any = None,
        timeout: float = 300,
        operation_timeout: Optional[float] = None,
        headers: dict = None,  # Agregar este parámetro
    ):
        # handshake: store async session
        self.session = client
        # Zeep sometimes references .client directly
        self.client = client
        self.cache = cache
        self._timeout = timeout
        self.operation_timeout = operation_timeout

        # prevent Zeep destructor from trying to close asyncio session
        self._close_session = False

        # provide a logger attribute Zeep expects
        import logging
        self.logger = logging.getLogger("zeep.transports")

        # Store headers for debugging
        self._debug_headers = headers or {}

        # Build the sync client for WSDL parsing with headers
        transport = getattr(client, "_transport", None)
        self.wsdl_client = httpx.Client(
            transport=transport,
            timeout=timeout,
            headers=headers or {},  # Pasar los headers
        )

class SOAPClient(ABC):
    """
    SOAPClient

        Overview

            The SOAPClient class is a generic asynchronous base for SOAP integrations.
            It supports both OAuth2 (refresh_token grant with Redis caching) and
            Basic Authentication (for custom reports). Provides customizable
            httpx.AsyncClient for Zeep. Designed for easy extension to specific SOAP APIs.

        .. table:: Properties
        :widths: auto

            +-------------------+----------+-----------+---------------------------------------------------------------+
            | Name              | Required | Summary                                                           |
            +-------------------+----------+-----------+---------------------------------------------------------------+
            | credentials       |   Yes    | Dict with wsdl_path and either OAuth (client_id, client_secret, |
            |                   |          | token_url, refresh_token) or Basic Auth (report_username,       |
            |                   |          | report_password)                                                 |
            | httpx_client      |   No     | Optionally inject a configured AsyncClient                        |
            | redis_url         |   No     | Redis DSN for token cache (OAuth only)                            |
            | redis_key         |   No     | Key under which to cache the access token (OAuth only)            |
            | timeout           |   No     | HTTP request timeout (seconds)                                    |
            +-------------------+----------+-----------+---------------------------------------------------------------+

        Returns

            This component provides an async interface to SOAP APIs, handling authentication,
            caching, and Zeep client/service setup. Subclasses should implement specific
            SOAP operations.

        Example:

        ```python
        class MyClient(SOAPClient):
            ...
        ```
    """

    def __init__(
        self,
        *,
        credentials: dict,
        httpx_client: Optional[httpx.AsyncClient] = None,
        redis_url: Optional[str] = None,
        redis_key: str = "soap:access_token",
        timeout: int = 30,
        **kwargs
    ):
        """
        :param credentials: For OAuth:
            {
                "client_id": str,
                "client_secret": str,
                "token_url": str,
                "wsdl_path": Union[str, Path],
                "refresh_token": str
            }
            For Basic Auth (custom reports):
            {
                "wsdl_path": Union[str, Path],
                "report_username": str,
                "report_password": str
            }
        :param httpx_client: optionally inject a configured AsyncClient
        :param redis_url:    Redis DSN for token cache (OAuth only)
        :param redis_key:    key under which to cache the access token (OAuth only)
        :param timeout:      HTTP request timeout (seconds)
        """
        # Check if using Basic Auth for custom reports
        self.report_username = credentials.get("report_username")
        self.report_password = credentials.get("report_password")
        self.use_basic_auth = bool(self.report_username and self.report_password)

        # Validate credentials dict based on auth type
        if not self.use_basic_auth:
            required = ("client_id", "client_secret", "token_url", "wsdl_path", "refresh_token")
            missing = [k for k in required if k not in credentials or not credentials[k]]
            if missing:
                raise TypeError(f"Missing SOAP credentials: {', '.join(missing)}")

            # Stash OAuth credentials
            self.client_id     = credentials["client_id"]
            self.client_secret = credentials["client_secret"]
            self.token_url     = credentials["token_url"]
            self.refresh_token = credentials["refresh_token"]
        else:
            # For Basic Auth, we only need wsdl_path
            self.client_id     = credentials.get("client_id", "")
            self.client_secret = credentials.get("client_secret", "")
            self.token_url     = credentials.get("token_url", "")
            self.refresh_token = credentials.get("refresh_token", "")

        # Accept Path or str, but Zeep needs a str
        self.wsdl_path     = str(credentials["wsdl_path"])

        self._httpx_client = httpx_client
        # Use: 1) explicit redis_url, 2) env config (REDIS_URL), 3) fallback to localhost
        if redis_url is not None:
            self.redis_url = redis_url
        else:
            self.redis_url = REDIS_URL or "redis://localhost:6379/1"
        self.redis_key     = redis_key
        self.timeout       = timeout

        super().__init__(**kwargs)

        self._redis: Optional[aioredis.Redis]             = None
        self._token: Optional[str]                        = None
        self._transport: Optional[NoProxyAsyncTransport]  = None
        self._settings: Optional[Settings]                = None
        self._client: Optional[ZeepAsyncClient]           = None
        self._service: Any                                = None
        self._result: Any                                 = None

    async def start(self) -> None:
        """
        1) Connect to Redis (only if using OAuth)
        2) Get or refresh the bearer token (only if using OAuth)
        3) Build Zeep transport, client, and bind the service
        """
        if not self.use_basic_auth:
            # 1) Redis
            self._redis = aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )

            # 2) Token
            self._token = await self._get_bearer_token()
        else:
            # For Basic Auth, no Redis or OAuth token needed
            self._redis = None
            self._token = None

        # 3) Zeep pieces
        self._transport = self.get_transport()
        self._settings  = self.get_settings()
        self._client    = self.get_client()
        self._service   = self.bind_service()

    async def _get_bearer_token(self) -> str:
        """
        Retrieve a cached token or perform OAuth2 refresh_token grant.
        """
        # try cache
        tok = await self._redis.get(self.redis_key)
        if tok:
            return tok

        # Basic auth header for refresh_token grant
        basic = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Authorization":    f"Basic {basic}",
            "Content-Type":     "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type":       "refresh_token",
            "refresh_token":    self.refresh_token,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as http:
            resp = await http.post(self.token_url, data=data, headers=headers)
            resp.raise_for_status()
            payload = resp.json()
            tok     = payload["access_token"]
            exp     = payload.get("expires_in", 300)

        # cache under TTL
        await self._redis.set(self.redis_key, tok, ex=exp - 10)
        return tok

    def get_transport(self) -> NoProxyAsyncTransport:
        """
        Wrap an AsyncClient in our NoProxyAsyncTransport.
        Uses Basic Auth for custom reports or Bearer token for OAuth.
        """
        import logging
        logger = logging.getLogger("flowtask.workday")

        if self.use_basic_auth:
            # Use Basic Auth for custom report endpoints
            basic_creds = base64.b64encode(
                f"{self.report_username}:{self.report_password}".encode()
            ).decode()
            auth_header = f"Basic {basic_creds}"
            logger.info(f"Setting up SOAP transport with Basic Auth")
            logger.debug(f"Basic Auth header (first 20 chars): {auth_header[:20]}...")
        else:
            # Use OAuth Bearer token
            auth_header = f"Bearer {self._token}"
            logger.info(f"Setting up SOAP transport with OAuth Bearer token")

        # Create httpx event hooks for debugging
        async def log_request(request):
            logger.debug(f"SOAP Request URL: {request.url}")
            logger.debug(f"SOAP Request Method: {request.method}")
            # logger.debug(f"SOAP Request Headers: {dict(request.headers)}")

        async def log_response(response):
            logger.debug(f"SOAP Response Status: {response.status_code}")

        event_hooks = {
            'request': [log_request],
            'response': [log_response]
        }

        client = self._httpx_client or httpx.AsyncClient(
            headers={"Authorization": auth_header},
            timeout=self.timeout,
            event_hooks=event_hooks
        )
        return NoProxyAsyncTransport(client=client, headers={"Authorization": auth_header})

    def get_settings(self) -> Settings:
        """
        Zeep settings: non-strict, support huge XML trees.
        Note: Zeep caches WSDLs internally, but this is cleaned up during client destruction.
        The primary memory leak fixes are removing raw_data and explicit gc.collect() calls.
        Enable raw_response for debugging if needed.
        """
        return Settings(
            strict=False,
            xml_huge_tree=True,
            raw_response=False  # Set to True to see raw SOAP responses
        )

    def get_client(self) -> ZeepAsyncClient:
        """
        Instantiate the Zeep AsyncClient for our WSDL.
        """
        return ZeepAsyncClient(
            wsdl=self.wsdl_path,
            transport=self._transport,
            settings=self._settings,
        )

    def bind_service(self) -> Any:
        """
        Return the bound service proxy from Zeep.
        """
        return self._client.service  # type: ignore

    async def run(self, operation: str, **kwargs) -> Any:
        """
        Invoke a named SOAP operation with kwargs.
        """
        if not self._service:
            raise RuntimeError("Call start() before run()")
        method = getattr(self._service, operation, None)
        if method is None:
            raise ValueError(f"Operation '{operation}' not found in WSDL")

        res = await method(**kwargs)
        self._result = res
        return res

    async def close(self) -> None:
        """
        Cleanup HTTP session, Zeep client, and Redis connection.
        Ensure all memory is properly released including WSDL caches.
        """
        import gc
        import logging
        _log = logging.getLogger("flowtask.workday")

        if self._client:
            try:
                self._client = None
            except Exception as e:
                _log.warning(f"Error clearing Zeep client: {e}")

        if self._transport and hasattr(self._transport, "session"):
            try:
                await self._transport.session.aclose()
                self._transport = None
            except Exception as e:
                _log.warning(f"Error closing transport: {e}")

        if self._redis:
            try:
                await self._redis.aclose()
                self._redis = None
            except Exception as e:
                _log.warning(f"Error closing Redis: {e}")

        gc.collect()

    async def __aenter__(self) -> "SOAPClient":
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

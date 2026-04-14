"""HTTP client for Desktop Agent API."""

from __future__ import annotations

import logging
import os
import re
import warnings
from collections.abc import Callable
from typing import Any
from urllib.parse import urlparse

import httpx

from .api.bash.bash import asyncio as _bash_async
from .api.bash.bash import sync as _bash_sync
from .api.computer.computer import asyncio as _computer_async
from .api.computer.computer import sync as _computer_sync
from .api.edit.edit import asyncio as _edit_async
from .api.edit.edit import sync as _edit_sync
from .api.status.get_status import asyncio as _status_async
from .api.status.get_status import sync as _status_sync
from .models import BashRequest, ComputerRequest, EditRequest, StatusResponse, ToolResult

logger = logging.getLogger(__name__)

# Environment variable prefix for this client
ENV_PREFIX = "UBUNTU_VM"

LIVEVIEW_PORT = 6080
DESKTOP_AGENT_PORT = 9000

# Pattern: https://{job_id}--{port}.sims.plato.so or https://{job_id}.sims.plato.so
_JOB_ID_RE = re.compile(r"https?://([a-f0-9-]+?)(?:--\d+)?\..*sims\.plato\.so")


def _base_url_from_job_id(job_id: str, port: int = DESKTOP_AGENT_PORT) -> str:
    """Build a sims.plato.so base URL from a job ID and port."""
    return f"https://{job_id}--{port}.sims.plato.so"


def _extract_job_id(base_url: str) -> str:
    """Extract the job ID from a sims.plato.so base URL."""
    m = _JOB_ID_RE.match(base_url)
    if m:
        return m.group(1)
    raise ValueError(
        f"Cannot extract job_id from base_url '{base_url}'. "
        "Expected format: https://{{job_id}}--{{port}}.sims.plato.so"
    )


# API base path suffix (e.g., "/api/v1")
BASE_PATH = ""

# Default credentials (configured during generation)


def _get_env_config() -> tuple[str | None, dict[str, str]]:
    """Get base URL and headers from environment variables.

    Looks for:
    - {PREFIX}_BASE_URL: Base URL for API requests
    - {PREFIX}_API_TOKEN: Bearer token for Authorization header

    Returns:
        Tuple of (base_url, headers)
    """
    base_url = os.environ.get(f"{ENV_PREFIX}_BASE_URL")
    headers: dict[str, str] = {}

    # Check for bearer token
    token = os.environ.get(f"{ENV_PREFIX}_API_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    return base_url, headers


class Client:
    """Sync HTTP client for Desktop Agent API."""

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
        # Always include Accept header for JSON APIs
        self._headers = {"Accept": "application/json", **(headers or {})}
        self._max_retries = max_retries
        self._retry_on_status = retry_on_status
        self._closed = False

        event_hooks: dict[str, list[Callable]] = {"request": [], "response": []}
        if on_request:
            event_hooks["request"].append(on_request)
        if on_response:
            event_hooks["response"].append(on_response)

        self._timeout = timeout
        self._initialized = False
        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=timeout,
            headers=self._headers,
            follow_redirects=False,
            event_hooks=event_hooks if any(event_hooks.values()) else None,
            **kwargs,
        )

    def _ensure_init(self) -> None:
        """Handle the _plato/init redirect dance if the sims proxy redirects.

        The sims proxy may redirect through a web proxy via ``_plato/init``
        to establish routing cookies.  The 302 from ``_plato/init`` converts
        POST to GET (per HTTP spec), breaking POST endpoints.

        This method performs the redirect dance once with a GET request to
        capture the routing cookies, then switches the base URL to the web
        proxy so subsequent requests go directly — preserving the HTTP method.
        """
        if self._initialized:
            return
        self._initialized = True

        response = self._client.request(method="GET", url="/status")
        if response.status_code not in (301, 302, 307, 308):
            return

        location = response.headers.get("location", "")
        if "_plato/init" not in location:
            return

        logger.debug("Performing _plato/init redirect dance")

        # Follow the init chain with a temp client to capture routing cookies
        with httpx.Client(follow_redirects=True, timeout=self._timeout) as tmp:
            tmp.get(location)
            cookies = dict(tmp.cookies)

        parsed = urlparse(location)
        web_proxy_url = f"{parsed.scheme}://{parsed.hostname}"

        old_client = self._client
        self._client = httpx.Client(
            base_url=web_proxy_url,
            timeout=self._timeout,
            headers=self._headers,
            follow_redirects=False,
            cookies=cookies,
        )
        old_client.close()

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

    def get_liveview_url(self) -> str:
        """Get the noVNC liveview URL for this VM."""
        job_id = _extract_job_id(self._base_url)
        return f"https://{job_id}--{LIVEVIEW_PORT}.sims.plato.so?resize=scale&autoconnect=true"

    def bash(self, body: BashRequest) -> ToolResult:
        """Execute a shell command."""
        self._ensure_init()
        return _bash_sync(self._client, body=body)

    def computer(self, body: ComputerRequest) -> ToolResult:
        """Execute computer actions (mouse, keyboard, screenshot)."""
        self._ensure_init()
        return _computer_sync(self._client, body=body)

    def edit(self, body: EditRequest) -> ToolResult:
        """File operations (view, create, str_replace, insert, undo_edit)."""
        self._ensure_init()
        return _edit_sync(self._client, body=body)

    def status(self) -> StatusResponse:
        """Health check and display info."""
        self._ensure_init()
        return _status_sync(self._client)

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

    @classmethod
    def from_env(cls, **kwargs: Any) -> Client:
        """Create client from environment variables.

        Reads {ENV_PREFIX}_BASE_URL and auth credentials.

        Args:
            **kwargs: Additional arguments passed to Client.__init__

        Returns:
            Configured Client instance

        Raises:
            ValueError: If {ENV_PREFIX}_BASE_URL is not set
        """
        base_url, env_headers = _get_env_config()
        if not base_url:
            raise ValueError(f"{ENV_PREFIX}_BASE_URL environment variable is required")

        # Merge env headers with any provided headers
        headers = kwargs.pop("headers", None) or {}
        headers = {**env_headers, **headers}

        return cls(base_url=base_url, headers=headers, **kwargs)

    @classmethod
    def create(
        cls,
        base_url: str | None = None,
        api_token: str | None = None,
        **kwargs: Any,
    ) -> Client:
        """Create an authenticated client.

        Args:
            base_url: Base URL (uses {ENV_PREFIX}_BASE_URL if not provided)
            api_token: API token (uses default if not provided)
            **kwargs: Additional arguments passed to Client.__init__

        Returns:
            Authenticated Client instance
        """
        base_url = base_url or os.environ.get(f"{ENV_PREFIX}_BASE_URL")
        if not base_url:
            raise ValueError(f"base_url required or set {ENV_PREFIX}_BASE_URL")

        token = api_token or os.environ.get(f"{ENV_PREFIX}_API_TOKEN")

        headers = kwargs.pop("headers", None) or {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        return cls(base_url=base_url, headers=headers, **kwargs)

    @classmethod
    def from_environment(cls, environment: Any, **kwargs: Any) -> Client:
        """Create a client from a Plato v2 Environment object.

        Args:
            environment: A plato.v2 Environment with a .job_id attribute.
            **kwargs: Additional arguments passed to Client.__init__
        """
        return cls(base_url=_base_url_from_job_id(environment.job_id), **kwargs)


class AsyncClient:
    """Async HTTP client for Desktop Agent API."""

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
        """Initialize the async HTTP client."""
        self._base_url = base_url.rstrip("/")
        # Always include Accept header for JSON APIs
        self._headers = {"Accept": "application/json", **(headers or {})}
        self._max_retries = max_retries
        self._retry_on_status = retry_on_status
        self._closed = False

        event_hooks: dict[str, list[Callable]] = {"request": [], "response": []}
        if on_request:
            event_hooks["request"].append(on_request)
        if on_response:
            event_hooks["response"].append(on_response)

        self._timeout = timeout
        self._initialized = False
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=timeout,
            headers=self._headers,
            follow_redirects=False,
            event_hooks=event_hooks if any(event_hooks.values()) else None,
            **kwargs,
        )

    async def _ensure_init(self) -> None:
        """Handle the _plato/init redirect dance if the sims proxy redirects.

        See :meth:`Client._ensure_init` for details.
        """
        if self._initialized:
            return
        self._initialized = True

        response = await self._client.request(method="GET", url="/status")
        if response.status_code not in (301, 302, 307, 308):
            return

        location = response.headers.get("location", "")
        if "_plato/init" not in location:
            return

        logger.debug("Performing _plato/init redirect dance")

        async with httpx.AsyncClient(follow_redirects=True, timeout=self._timeout) as tmp:
            await tmp.get(location)
            cookies = dict(tmp.cookies)

        parsed = urlparse(location)
        web_proxy_url = f"{parsed.scheme}://{parsed.hostname}"

        old_client = self._client
        self._client = httpx.AsyncClient(
            base_url=web_proxy_url,
            timeout=self._timeout,
            headers=self._headers,
            follow_redirects=False,
            cookies=cookies,
        )
        await old_client.aclose()

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

    def get_liveview_url(self) -> str:
        """Get the noVNC liveview URL for this VM."""
        job_id = _extract_job_id(self._base_url)
        return f"https://{job_id}--{LIVEVIEW_PORT}.sims.plato.so?resize=scale&autoconnect=true"

    async def bash(self, body: BashRequest) -> ToolResult:
        """Execute a shell command."""
        await self._ensure_init()
        return await _bash_async(self._client, body=body)

    async def computer(self, body: ComputerRequest) -> ToolResult:
        """Execute computer actions (mouse, keyboard, screenshot)."""
        await self._ensure_init()
        return await _computer_async(self._client, body=body)

    async def edit(self, body: EditRequest) -> ToolResult:
        """File operations (view, create, str_replace, insert, undo_edit)."""
        await self._ensure_init()
        return await _edit_async(self._client, body=body)

    async def status(self) -> StatusResponse:
        """Health check and display info."""
        await self._ensure_init()
        return await _status_async(self._client)

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

    @classmethod
    def from_env(cls, **kwargs: Any) -> AsyncClient:
        """Create client from environment variables."""
        base_url, env_headers = _get_env_config()
        if not base_url:
            raise ValueError(f"{ENV_PREFIX}_BASE_URL environment variable is required")

        headers = kwargs.pop("headers", None) or {}
        headers = {**env_headers, **headers}

        return cls(base_url=base_url, headers=headers, **kwargs)

    @classmethod
    async def create(
        cls,
        base_url: str | None = None,
        api_token: str | None = None,
        **kwargs: Any,
    ) -> AsyncClient:
        """Create an authenticated client."""
        base_url = base_url or os.environ.get(f"{ENV_PREFIX}_BASE_URL")
        if not base_url:
            raise ValueError(f"base_url required or set {ENV_PREFIX}_BASE_URL")

        token = api_token or os.environ.get(f"{ENV_PREFIX}_API_TOKEN")

        headers = kwargs.pop("headers", None) or {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        return cls(base_url=base_url, headers=headers, **kwargs)

    @classmethod
    def from_environment(cls, environment: Any, **kwargs: Any) -> AsyncClient:
        """Create a client from a Plato v2 Environment object.

        Args:
            environment: A plato.v2 Environment with a .job_id attribute.
            **kwargs: Additional arguments passed to AsyncClient.__init__
        """
        return cls(base_url=_base_url_from_job_id(environment.job_id), **kwargs)

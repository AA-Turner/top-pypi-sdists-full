"""HTTP client for Desktop Agent API."""

from __future__ import annotations

import json as _json
import logging
import os
import re
import time
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
CDP_PORT = 9224

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
        timeout: float = 120.0,
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
            timeout: Request timeout in seconds (matches Desktop Agent API's 120s bash timeout)
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
        """Complete the sims proxy redirect/cookie dance on first use.

        The sims proxy has two routing modes:

        * **Web routing** (``_plato/init``): redirects to a per-simulator
          web proxy domain via a multi-step init chain.
        * **Sims routing** (default for ``*.sims.plato.so``): the app
          nginx always proxies subdomain requests to FastAPI which returns
          a 302 to the base domain (``sims.plato.so``) with a signed
          ``plato-sims-session`` cookie.  The sims router on the base
          domain reads the cookie and proxies to the correct VM.

        This method fires a probe GET, follows any redirects with a
        temporary client to capture routing cookies, then reconfigures
        the underlying ``httpx.Client`` to target the post-redirect host
        with the captured cookies.
        """
        if self._initialized:
            return

        response = self._client.request(method="GET", url="/status")
        if response.status_code not in (301, 302, 307, 308):
            self._initialized = True
            return

        location = response.headers.get("location", "")

        if "_plato/init" in location:
            logger.debug("Performing _plato/init redirect dance")
            with httpx.Client(follow_redirects=True, timeout=self._timeout) as tmp:
                tmp.get(location)
                cookies = dict(tmp.cookies)
            parsed = urlparse(location)
            new_base_url = f"{parsed.scheme}://{parsed.hostname}"
        else:
            logger.debug("Performing sims routing cookie dance")
            with httpx.Client(follow_redirects=True, timeout=self._timeout) as tmp:
                resp = tmp.get(f"{self._base_url}/status")
                cookies = dict(tmp.cookies)
            new_base_url = f"https://{resp.url.host}"

        self._initialized = True
        old_client = self._client
        self._client = httpx.Client(
            base_url=new_base_url,
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

    # -- CDP helpers ----------------------------------------------------------

    def get_cdp_url(self, port: int = CDP_PORT) -> str:
        """Return the sims proxy URL for the Chrome CDP port."""
        job_id = _extract_job_id(self._base_url)
        return f"https://{job_id}--{port}.sims.plato.so"

    def ensure_chrome_cdp(self, port: int = CDP_PORT, timeout: int = 60) -> str:
        """Ensure Chrome CDP is reachable on *port* inside the VM.

        First polls for an already-responsive CDP endpoint.  If it doesn't
        come up within a short window (snapshot restore can leave Chrome
        processes alive but with dead TCP sockets), kills Chrome and
        restarts it so the CDP debug port is re-bound.

        Returns:
            The external sims-proxy CDP URL.

        Raises:
            TimeoutError: If Chrome CDP does not respond within *timeout*.
        """
        cdp_probe = f"curl -sf --max-time 2 http://localhost:{port}/json/version 2>/dev/null || echo __NO_CDP__"
        try:
            check = self.bash(BashRequest(command=cdp_probe))
        except Exception:
            logger.debug("First bash call failed; warming up client via status()")
            self.status()
            check = self.bash(BashRequest(command=cdp_probe))
        if "__NO_CDP__" not in (check.output or ""):
            logger.info("Chrome CDP already responding on port %s", port)
            return self.get_cdp_url(port)

        # Quick poll — if the snapshot restored cleanly Chrome may just
        # need a moment for the socket to come back.
        logger.info("Waiting for Chrome CDP on port %s ...", port)
        for _ in range(5):
            time.sleep(1)
            probe = self.bash(BashRequest(command=cdp_probe))
            if "__NO_CDP__" not in (probe.output or ""):
                logger.info("Chrome CDP ready on port %s", port)
                return self.get_cdp_url(port)

        # Snapshot restore likely left Chrome with dead sockets — restart.
        logger.info("Chrome CDP unresponsive; restarting Chrome")
        self.bash(BashRequest(command="pkill -9 -f 'chrome' 2>/dev/null; sleep 2"))

        chrome_internal_port = 9225 if port == 9224 else port
        self.bash(
            BashRequest(
                command=(
                    f"DISPLAY=:0 nohup google-chrome-stable "
                    f"--no-sandbox --disable-gpu --disable-dev-shm-usage "
                    f"--disable-features=PasswordManager,PasswordManagerOnboarding,PasswordLeakDetection "
                    f"--no-first-run --no-default-browser-check --disable-default-apps "
                    f"--disable-popup-blocking --disable-translate --disable-infobars "
                    f"--test-type --start-maximized --window-size=1280,720 "
                    f"--user-data-dir=/tmp/chrome-cdp-profile "
                    f"--remote-debugging-port={chrome_internal_port} "
                    f"about:blank >/dev/null 2>&1 &"
                )
            )
        )

        deadline = time.monotonic() + timeout
        last_err = ""
        while time.monotonic() < deadline:
            time.sleep(2)
            probe = self.bash(BashRequest(command=cdp_probe))
            if "__NO_CDP__" not in (probe.output or ""):
                logger.info("Chrome CDP ready on port %s after restart", port)
                return self.get_cdp_url(port)
            last_err = (probe.output or "").strip()

        raise TimeoutError(f"Chrome CDP not ready on port {port} after {timeout}s. Last probe: {last_err}")

    def get_cdp_ws_url(self, port: int = CDP_PORT) -> str:
        """Return a Playwright-ready WebSocket URL for the VM's Chrome CDP.

        Fetches ``/json/version`` from Chrome *inside* the VM and rewrites
        the ``webSocketDebuggerUrl`` (which Chrome reports as
        ``ws://localhost:…``) to point through the sims proxy so that
        Playwright running *outside* the VM can connect.

        .. note:: The returned URL may still require the sims proxy init
           dance before a WebSocket connection succeeds.  Use
           :meth:`prepare_cdp_connection` instead to get a URL + headers
           tuple that works directly with ``connect_over_cdp``.
        """
        result = self.bash(BashRequest(command=f"curl -s --max-time 5 http://localhost:{port}/json/version"))
        try:
            version_info = _json.loads(result.output or "")
        except _json.JSONDecodeError as exc:
            raise RuntimeError(f"Failed to parse /json/version from Chrome: {result.output}") from exc

        ws_url: str = version_info["webSocketDebuggerUrl"]
        job_id = _extract_job_id(self._base_url)
        proxy_host = f"{job_id}--{port}.sims.plato.so"
        ws_url = re.sub(
            r"ws://(localhost|127\.0\.0\.1)(:\d+)?",
            f"wss://{proxy_host}",
            ws_url,
        )
        return ws_url

    def prepare_cdp_connection(self, port: int = CDP_PORT) -> tuple[str, dict[str, str]]:
        """Get the WebSocket URL **and** headers for Playwright ``connect_over_cdp``.

        The sims proxy has a two-tier architecture:

        * **Subdomain** (``{job}--{port}.sims.plato.so``) — app nginx
          always proxies to FastAPI which returns a **302** to the base
          domain with ``Set-Cookie``.  This 302 cannot be followed by a
          WebSocket client.
        * **Base domain** (``sims.plato.so``) — OpenResty sims router
          reads the ``plato-sims-session`` cookie and proxies directly to
          the worker VM.  WebSocket upgrades work here.

        This method completes the redirect/cookie dance via HTTP and
        returns a WebSocket URL on the **base domain** with the captured
        cookies so Playwright can connect without hitting the 302.

        Returns:
            ``(ws_url, headers)`` -- pass both to
            ``chromium.connect_over_cdp(ws_url, headers=headers)``.
        """
        result = self.bash(BashRequest(command=f"curl -s --max-time 5 http://localhost:{port}/json/version"))
        try:
            version_info = _json.loads(result.output or "")
        except _json.JSONDecodeError as exc:
            raise RuntimeError(f"Failed to parse /json/version: {result.output}") from exc

        ws_path = urlparse(version_info["webSocketDebuggerUrl"]).path

        cdp_proxy_url = self.get_cdp_url(port)
        with httpx.Client(follow_redirects=True, timeout=30) as tmp:
            resp = tmp.get(f"{cdp_proxy_url}/json/version")
            cookies = dict(tmp.cookies)

        ws_host = resp.url.host
        ws_url = f"wss://{ws_host}{ws_path}"

        headers: dict[str, str] = {}
        if cookies:
            headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())

        logger.info(
            "CDP connection prepared — ws=%s cookies=%d (redirected from %s)",
            ws_url,
            len(cookies),
            cdp_proxy_url,
        )
        return ws_url, headers

    def open_url(self, url: str, port: int = CDP_PORT) -> dict:
        """Open *url* in a new Chrome tab via CDP."""
        result = self.bash(BashRequest(command=f"curl -s --max-time 5 -X PUT 'http://localhost:{port}/json/new?{url}'"))
        try:
            return _json.loads(result.output or "")
        except _json.JSONDecodeError:
            return {"url": url, "raw": (result.output or "").strip()}

    def list_tabs(self, port: int = CDP_PORT) -> list[dict]:
        """Return the list of open Chrome tabs from CDP."""
        result = self.bash(BashRequest(command=f"curl -s --max-time 5 http://localhost:{port}/json/list"))
        try:
            return _json.loads(result.output or "[]")
        except _json.JSONDecodeError:
            return []

    def login(
        self,
        session: Any,
        cdp_port: int = CDP_PORT,
        retries: int = 3,
        retry_delay: float = 2.0,
    ) -> list[str]:
        """Open simulator URLs in the VM's Chrome and run login flows.

        Connects Playwright to Chrome via CDP, then for each simulator env
        in *session* that has an ``artifact_id`` (i.e. not the desktop
        runtime), navigates to its public URL and executes the ``login``
        flow with retries.

        Follows the same pattern as
        ``CuaBenchmarkWorld._run_v2_login_flow`` and
        ``Session.login``, but targets Chrome running inside the VM
        rather than a local browser.

        Args:
            session: A ``plato.v2.sync.Session`` with ``.envs``,
                ``._http``, and ``._api_key``.
            cdp_port: Chrome DevTools Protocol port on the VM.
            retries: Number of retry attempts per login flow.
            retry_delay: Seconds between retries.

        Returns:
            List of environment aliases that were successfully logged in.

        Raises:
            ImportError: If playwright is not installed.
            RuntimeError: If a public URL or flows cannot be fetched, or
                if login fails after all retries.
        """
        import importlib.util

        if importlib.util.find_spec("playwright") is None:
            raise ImportError("login() requires playwright. Install with: pip install playwright")

        from playwright.sync_api import sync_playwright

        from plato._generated.api.v2.jobs import get_flows as jobs_get_flows
        from plato._generated.api.v2.jobs import public_url as jobs_public_url
        from plato._generated.models import Flow
        from plato.v2.sync.flow_executor import FlowExecutor

        self.ensure_chrome_cdp(cdp_port)
        ws_url, cdp_headers = self.prepare_cdp_connection(cdp_port)
        logger.info("Connecting Playwright to CDP: %s", ws_url)

        pages_logged_in: list[str] = []

        with sync_playwright() as pw:
            browser = pw.chromium.connect_over_cdp(ws_url, headers=cdp_headers)
            default_context = browser.contexts[0]
            logger.info(
                "Connected – %d existing page(s): %s",
                len(default_context.pages),
                [p.url for p in default_context.pages],
            )

            # Pick an about:blank page or create one as the starting tab
            first_page = None
            for p in default_context.pages:
                if not p.is_closed() and (p.url or "") == "about:blank":
                    first_page = p
                    break
            if first_page is None:
                first_page = default_context.new_page()
                first_page.goto("about:blank")

            my_job_id = _extract_job_id(self._base_url)
            login_count = 0
            for env in session.envs:
                if not getattr(env, "artifact_id", None):
                    logger.info("Skipping login for %s (no artifact_id)", env.alias)
                    continue
                if getattr(env, "job_id", None) == my_job_id:
                    logger.info("Skipping login for %s (desktop env)", env.alias)
                    continue

                page = first_page if login_count == 0 else default_context.new_page()
                login_count += 1

                # Get public URL
                public_url_result = jobs_public_url.sync(
                    client=session._http,
                    job_id=env.job_id,
                    x_api_key=session._api_key,
                )
                if public_url_result.error or not public_url_result.url:
                    raise RuntimeError(f"Failed to get public URL for {env.alias}: {public_url_result.error}")

                public_url = public_url_result.url
                sim_name = getattr(env, "simulator", None) or env.alias
                if sim_name and "_plato_router_target=" not in public_url:
                    target_param = f"_plato_router_target={sim_name}.web.plato.so"
                    sep = "&" if "?" in public_url else "?"
                    public_url = f"{public_url}{sep}{target_param}"
                logger.info("Navigating to %s for %s", public_url, env.alias)
                print(f"  [{env.alias}] Navigating to {public_url}", flush=True)
                page.goto(public_url, timeout=120_000)
                print(f"  [{env.alias}] Page loaded: {page.url}", flush=True)

                # Fetch flows
                try:
                    flows_response = jobs_get_flows.sync(
                        client=session._http,
                        job_id=env.job_id,
                        x_api_key=session._api_key,
                    )
                except Exception as exc:
                    raise RuntimeError(f"Failed to get flows for {env.alias}: {exc}") from exc

                if not flows_response:
                    raise RuntimeError(f"No flows found for {env.alias}")

                flows_list = [Flow.model_validate(f) for f in flows_response]
                login_flow = next((f for f in flows_list if f.name == "login"), None)
                if not login_flow:
                    raise RuntimeError(f"No 'login' flow found for {env.alias}")

                flow_executor = FlowExecutor(page, login_flow, log=logger)

                last_error: Exception | None = None
                for attempt in range(1 + retries):
                    try:
                        flow_executor.execute()
                        last_error = None
                        break
                    except Exception as exc:
                        last_error = exc
                        if attempt < retries:
                            print(
                                f"  [{env.alias}] Login attempt {attempt + 1}/{1 + retries} "
                                f"failed, retrying in {retry_delay}s: {exc}",
                                flush=True,
                            )
                            time.sleep(retry_delay)
                            page.goto(public_url, timeout=120_000)

                if last_error is not None:
                    raise RuntimeError(
                        f"Login failed for {env.alias} after {1 + retries} attempts: {last_error}"
                    ) from last_error

                print(f"  [{env.alias}] Login successful", flush=True)
                pages_logged_in.append(env.alias)

            # Clean up stray about:blank tabs and focus the last real page
            target_page = None
            for p in list(default_context.pages):
                if p.is_closed():
                    continue
                if p.url and p.url != "about:blank" and not p.url.startswith("chrome://"):
                    target_page = p

            for p in list(default_context.pages):
                if not p.is_closed() and p != target_page and p.url == "about:blank":
                    try:
                        p.close()
                    except Exception:
                        pass

            if target_page:
                try:
                    target_page.bring_to_front()
                except Exception:
                    pass

        logger.info("Login complete for: %s", pages_logged_in)
        return pages_logged_in

    # -- /CDP helpers ---------------------------------------------------------

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
        timeout: float = 120.0,
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
        """Complete the sims proxy redirect/cookie dance on first use.

        See :meth:`Client._ensure_init` for details.
        """
        if self._initialized:
            return

        response = await self._client.request(method="GET", url="/status")
        if response.status_code not in (301, 302, 307, 308):
            self._initialized = True
            return

        location = response.headers.get("location", "")

        if "_plato/init" in location:
            logger.debug("Performing _plato/init redirect dance")
            async with httpx.AsyncClient(follow_redirects=True, timeout=self._timeout) as tmp:
                await tmp.get(location)
                cookies = dict(tmp.cookies)
            parsed = urlparse(location)
            new_base_url = f"{parsed.scheme}://{parsed.hostname}"
        else:
            logger.debug("Performing sims routing cookie dance")
            async with httpx.AsyncClient(follow_redirects=True, timeout=self._timeout) as tmp:
                resp = await tmp.get(f"{self._base_url}/status")
                cookies = dict(tmp.cookies)
            new_base_url = f"https://{resp.url.host}"

        self._initialized = True
        old_client = self._client
        self._client = httpx.AsyncClient(
            base_url=new_base_url,
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

    # -- CDP helpers ----------------------------------------------------------

    def get_cdp_url(self, port: int = CDP_PORT) -> str:
        """Return the sims proxy URL for the Chrome CDP port."""
        job_id = _extract_job_id(self._base_url)
        return f"https://{job_id}--{port}.sims.plato.so"

    async def ensure_chrome_cdp(self, port: int = CDP_PORT, timeout: int = 60) -> str:
        """Ensure Chrome CDP is reachable on *port* inside the VM.

        See :meth:`Client.ensure_chrome_cdp` for details.
        """
        import asyncio

        cdp_probe = f"curl -sf --max-time 2 http://localhost:{port}/json/version 2>/dev/null || echo __NO_CDP__"
        try:
            check = await self.bash(BashRequest(command=cdp_probe))
        except Exception:
            logger.debug("First bash call failed; warming up client via status()")
            await self.status()
            check = await self.bash(BashRequest(command=cdp_probe))
        if "__NO_CDP__" not in (check.output or ""):
            logger.info("Chrome CDP already responding on port %s", port)
            return self.get_cdp_url(port)

        logger.info("Waiting for Chrome CDP on port %s ...", port)
        for _ in range(5):
            await asyncio.sleep(1)
            probe = await self.bash(BashRequest(command=cdp_probe))
            if "__NO_CDP__" not in (probe.output or ""):
                logger.info("Chrome CDP ready on port %s", port)
                return self.get_cdp_url(port)

        logger.info("Chrome CDP unresponsive; restarting Chrome")
        await self.bash(BashRequest(command="pkill -9 -f 'chrome' 2>/dev/null; sleep 2"))

        chrome_internal_port = 9225 if port == 9224 else port
        await self.bash(
            BashRequest(
                command=(
                    f"DISPLAY=:0 nohup google-chrome-stable "
                    f"--no-sandbox --disable-gpu --disable-dev-shm-usage "
                    f"--disable-features=PasswordManager,PasswordManagerOnboarding,PasswordLeakDetection "
                    f"--no-first-run --no-default-browser-check --disable-default-apps "
                    f"--disable-popup-blocking --disable-translate --disable-infobars "
                    f"--test-type --start-maximized --window-size=1280,720 "
                    f"--user-data-dir=/tmp/chrome-cdp-profile "
                    f"--remote-debugging-port={chrome_internal_port} "
                    f"about:blank >/dev/null 2>&1 &"
                )
            )
        )

        deadline = time.monotonic() + timeout
        last_err = ""
        while time.monotonic() < deadline:
            await asyncio.sleep(2)
            probe = await self.bash(BashRequest(command=cdp_probe))
            if "__NO_CDP__" not in (probe.output or ""):
                logger.info("Chrome CDP ready on port %s after restart", port)
                return self.get_cdp_url(port)
            last_err = (probe.output or "").strip()

        raise TimeoutError(f"Chrome CDP not ready on port {port} after {timeout}s. Last probe: {last_err}")

    async def get_cdp_ws_url(self, port: int = CDP_PORT) -> str:
        """Return a Playwright-ready WebSocket URL for the VM's Chrome CDP.

        See :meth:`Client.get_cdp_ws_url` for details.
        """
        result = await self.bash(BashRequest(command=f"curl -s --max-time 5 http://localhost:{port}/json/version"))
        try:
            version_info = _json.loads(result.output or "")
        except _json.JSONDecodeError as exc:
            raise RuntimeError(f"Failed to parse /json/version from Chrome: {result.output}") from exc

        ws_url: str = version_info["webSocketDebuggerUrl"]
        job_id = _extract_job_id(self._base_url)
        proxy_host = f"{job_id}--{port}.sims.plato.so"
        ws_url = re.sub(
            r"ws://(localhost|127\.0\.0\.1)(:\d+)?",
            f"wss://{proxy_host}",
            ws_url,
        )
        return ws_url

    async def prepare_cdp_connection(self, port: int = CDP_PORT) -> tuple[str, dict[str, str]]:
        """Async version of :meth:`Client.prepare_cdp_connection`."""
        result = await self.bash(BashRequest(command=f"curl -s --max-time 5 http://localhost:{port}/json/version"))
        try:
            version_info = _json.loads(result.output or "")
        except _json.JSONDecodeError as exc:
            raise RuntimeError(f"Failed to parse /json/version: {result.output}") from exc

        ws_path = urlparse(version_info["webSocketDebuggerUrl"]).path

        cdp_proxy_url = self.get_cdp_url(port)
        async with httpx.AsyncClient(follow_redirects=True, timeout=30) as tmp:
            resp = await tmp.get(f"{cdp_proxy_url}/json/version")
            cookies = dict(tmp.cookies)

        ws_host = resp.url.host
        ws_url = f"wss://{ws_host}{ws_path}"

        headers: dict[str, str] = {}
        if cookies:
            headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())

        logger.info(
            "CDP connection prepared — ws=%s cookies=%d (redirected from %s)",
            ws_url,
            len(cookies),
            cdp_proxy_url,
        )
        return ws_url, headers

    async def open_url(self, url: str, port: int = CDP_PORT) -> dict:
        """Open *url* in a new Chrome tab via CDP."""
        result = await self.bash(
            BashRequest(command=f"curl -s --max-time 5 -X PUT 'http://localhost:{port}/json/new?{url}'")
        )
        try:
            return _json.loads(result.output or "")
        except _json.JSONDecodeError:
            return {"url": url, "raw": (result.output or "").strip()}

    async def list_tabs(self, port: int = CDP_PORT) -> list[dict]:
        """Return the list of open Chrome tabs from CDP."""
        result = await self.bash(BashRequest(command=f"curl -s --max-time 5 http://localhost:{port}/json/list"))
        try:
            return _json.loads(result.output or "[]")
        except _json.JSONDecodeError:
            return []

    async def login(
        self,
        session: Any,
        cdp_port: int = CDP_PORT,
        retries: int = 3,
        retry_delay: float = 2.0,
    ) -> list[str]:
        """Async version of :meth:`Client.login`.

        See the sync docstring for full details.
        """
        import asyncio
        import importlib.util

        if importlib.util.find_spec("playwright") is None:
            raise ImportError("login() requires playwright. Install with: pip install playwright")

        from playwright.async_api import async_playwright

        from plato._generated.api.v2.jobs import get_flows as jobs_get_flows
        from plato._generated.api.v2.jobs import public_url as jobs_public_url
        from plato._generated.models import Flow
        from plato.v2.async_.flow_executor import FlowExecutor

        await self.ensure_chrome_cdp(cdp_port)
        ws_url, cdp_headers = await self.prepare_cdp_connection(cdp_port)
        logger.info("Connecting Playwright to CDP: %s", ws_url)

        pages_logged_in: list[str] = []

        async with async_playwright() as pw:
            browser = await pw.chromium.connect_over_cdp(ws_url, headers=cdp_headers)
            default_context = browser.contexts[0]
            logger.info(
                "Connected – %d existing page(s): %s",
                len(default_context.pages),
                [p.url for p in default_context.pages],
            )

            first_page = None
            for p in default_context.pages:
                if not p.is_closed() and (p.url or "") == "about:blank":
                    first_page = p
                    break
            if first_page is None:
                first_page = await default_context.new_page()
                await first_page.goto("about:blank")

            my_job_id = _extract_job_id(self._base_url)
            login_count = 0
            for env in session.envs:
                if not getattr(env, "artifact_id", None):
                    logger.info("Skipping login for %s (no artifact_id)", env.alias)
                    continue
                if getattr(env, "job_id", None) == my_job_id:
                    logger.info("Skipping login for %s (desktop env)", env.alias)
                    continue

                page = first_page if login_count == 0 else await default_context.new_page()
                login_count += 1

                public_url_result = await jobs_public_url.asyncio(
                    client=session._http,
                    job_id=env.job_id,
                    x_api_key=session._api_key,
                )
                if public_url_result.error or not public_url_result.url:
                    raise RuntimeError(f"Failed to get public URL for {env.alias}: {public_url_result.error}")

                public_url = public_url_result.url
                sim_name = getattr(env, "simulator", None) or env.alias
                if sim_name and "_plato_router_target=" not in public_url:
                    target_param = f"_plato_router_target={sim_name}.web.plato.so"
                    sep = "&" if "?" in public_url else "?"
                    public_url = f"{public_url}{sep}{target_param}"
                logger.info("Navigating to %s for %s", public_url, env.alias)
                await page.goto(public_url, timeout=120_000)

                try:
                    flows_response = await jobs_get_flows.asyncio(
                        client=session._http,
                        job_id=env.job_id,
                        x_api_key=session._api_key,
                    )
                except Exception as exc:
                    raise RuntimeError(f"Failed to get flows for {env.alias}: {exc}") from exc

                if not flows_response:
                    raise RuntimeError(f"No flows found for {env.alias}")

                flows_list = [Flow.model_validate(f) for f in flows_response]
                login_flow = next((f for f in flows_list if f.name == "login"), None)
                if not login_flow:
                    raise RuntimeError(f"No 'login' flow found for {env.alias}")

                flow_executor = FlowExecutor(page, login_flow, log=logger)

                last_error: Exception | None = None
                for attempt in range(1 + retries):
                    try:
                        await flow_executor.execute()
                        last_error = None
                        break
                    except Exception as exc:
                        last_error = exc
                        if attempt < retries:
                            logger.warning(
                                "Login flow failed for %s (attempt %d/%d), retrying in %.1fs: %s",
                                env.alias,
                                attempt + 1,
                                1 + retries,
                                retry_delay,
                                exc,
                            )
                            await asyncio.sleep(retry_delay)
                            await page.goto(public_url, timeout=120_000)

                if last_error is not None:
                    raise RuntimeError(
                        f"Login failed for {env.alias} after {1 + retries} attempts: {last_error}"
                    ) from last_error

                logger.info("Login successful for %s", env.alias)
                pages_logged_in.append(env.alias)

            target_page = None
            for p in list(default_context.pages):
                if p.is_closed():
                    continue
                if p.url and p.url != "about:blank" and not p.url.startswith("chrome://"):
                    target_page = p

            for p in list(default_context.pages):
                if not p.is_closed() and p != target_page and p.url == "about:blank":
                    try:
                        await p.close()
                    except Exception:
                        pass

            if target_page:
                try:
                    await target_page.bring_to_front()
                except Exception:
                    pass

        logger.info("Login complete for: %s", pages_logged_in)
        return pages_logged_in

    # -- /CDP helpers ---------------------------------------------------------

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

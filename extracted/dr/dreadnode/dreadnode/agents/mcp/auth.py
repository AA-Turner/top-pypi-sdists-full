"""
MCP OAuth authentication support.

Provides file-based token storage, a localhost callback server for catching
OAuth redirects, a browser-opening redirect handler, and a factory that wires
those defaults onto the MCP SDK's :class:`OAuthClientProvider`.

Together they enable native HTTP MCP servers (e.g. Linear, Atlassian) to be
authenticated end-to-end by the Dreadnode runtime without going through the
``npx mcp-remote`` stdio bridge.
"""

import asyncio
import contextlib
import json
import os
import socket
import sys
import typing as t
import webbrowser
from collections.abc import Awaitable, Callable
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from loguru import logger

if t.TYPE_CHECKING:
    from mcp.client.auth.oauth2 import OAuthClientProvider, TokenStorage
    from mcp.shared.auth import OAuthClientInformationFull, OAuthToken

from dreadnode.agents.mcp.config import OAuthConfig

DEFAULT_AUTH_PATH = Path.home() / ".dreadnode" / "mcp-auth.json"

# Default time (seconds) the local callback server waits for the user to
# complete the OAuth flow in their browser before giving up.
_DEFAULT_CALLBACK_TIMEOUT = 300.0


class MCPOAuthRequiredError(Exception):
    """Raised when a connect would need to open a browser to complete OAuth
    but the runtime isn't allowed to (a non-interactive / background connect).

    Signals the lifecycle to classify the server as ``needs_auth`` and defer
    the browser-open to a user-initiated Authenticate, rather than popping a
    window during startup (CAP-MCP-010 — the runtime owns the browser-open
    moment).
    """


class FileTokenStorage:
    """Persist OAuth tokens to disk, keyed by server URL.

    File format (at ~/.dreadnode/mcp-auth.json, mode 0o600):
    {
      "https://api.example.com/mcp": {
        "tokens": { ... },
        "client_info": { ... }
      }
    }
    """

    def __init__(self, server_url: str, path: Path | None = None) -> None:
        self._server_url = server_url
        self._path = path or DEFAULT_AUTH_PATH

    def _read_store(self) -> dict[str, t.Any]:
        if not self._path.exists():
            return {}
        try:
            return json.loads(self._path.read_text())
        except (json.JSONDecodeError, OSError):
            logger.warning("Corrupt MCP auth file at {}, starting fresh", self._path)
            return {}

    def _write_store(self, store: dict[str, t.Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(self._path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump(store, f, indent=2)

    def _get_entry(self) -> dict[str, t.Any]:
        return self._read_store().get(self._server_url, {})

    def has_tokens(self) -> bool:
        """Synchronously report whether this server has stored OAuth tokens.

        Used by the runtime to decide, *before* a background connect, whether
        to wire up an OAuth provider at all. With no stored token a background
        connect attaches no provider — a 401 then surfaces as ``needs_auth``
        without any discovery/DCR traffic or browser-open. A small local file
        read is cheap enough to do inline on the connect path.
        """
        return bool(self._get_entry().get("tokens"))

    def _set_entry(self, entry: dict[str, t.Any]) -> None:
        store = self._read_store()
        store[self._server_url] = entry
        self._write_store(store)

    async def get_tokens(self) -> "OAuthToken | None":
        from mcp.shared.auth import OAuthToken

        entry = await asyncio.to_thread(self._get_entry)
        data = entry.get("tokens")
        if data is None:
            return None
        try:
            return OAuthToken.model_validate(data)
        except Exception:
            logger.warning("Invalid stored tokens for {}", self._server_url)
            return None

    async def set_tokens(self, tokens: "OAuthToken") -> None:
        def _update() -> None:
            entry = self._get_entry()
            entry["tokens"] = tokens.model_dump(mode="json", exclude_none=True)
            self._set_entry(entry)

        await asyncio.to_thread(_update)

    async def get_client_info(self) -> "OAuthClientInformationFull | None":
        from mcp.shared.auth import OAuthClientInformationFull

        entry = await asyncio.to_thread(self._get_entry)
        data = entry.get("client_info")
        if data is None:
            return None
        try:
            return OAuthClientInformationFull.model_validate(data)
        except Exception:
            logger.warning("Invalid stored client info for {}", self._server_url)
            return None

    async def set_client_info(self, client_info: "OAuthClientInformationFull") -> None:
        def _update() -> None:
            entry = self._get_entry()
            entry["client_info"] = client_info.model_dump(mode="json", exclude_none=True)
            self._set_entry(entry)

        await asyncio.to_thread(_update)

    async def clear(self) -> None:
        """Remove this server's stored tokens + client_info from the file.

        Targeted by server URL — other servers' entries are untouched.
        Used by the user-initiated re-authenticate flow so a fresh OAuth
        round-trip runs on the next connect without wiping the whole
        cache (other authenticated capabilities keep working).
        """

        def _clear() -> None:
            store = self._read_store()
            if self._server_url in store:
                del store[self._server_url]
                self._write_store(store)

        await asyncio.to_thread(_clear)


# --- Localhost OAuth callback server -----------------------------------------


_SUCCESS_HTML = (
    b"<!doctype html><html><head><meta charset='utf-8'>"
    b"<title>Dreadnode \xe2\x80\x94 Authentication complete</title>"
    b"<style>body{font:14px/1.5 system-ui,sans-serif;max-width:32rem;"
    b"margin:6rem auto;padding:0 1rem;color:#222;}h2{margin-bottom:.5rem}</style>"
    b"</head><body><h2>Authentication complete \xe2\x9c\x93</h2>"
    b"<p>You can close this tab and return to the Dreadnode TUI.</p>"
    b"</body></html>"
)

_ERROR_HTML = (
    b"<!doctype html><html><head><meta charset='utf-8'>"
    b"<title>Dreadnode \xe2\x80\x94 Authentication failed</title></head>"
    b"<body><h2>Authentication failed</h2>"
    b"<p>The authorization server didn't return a code parameter. "
    b"Return to the Dreadnode TUI and retry.</p></body></html>"
)


class LocalCallbackServer:
    """One-shot HTTP server on a 127.0.0.1 ephemeral port for OAuth redirects.

    Binds a socket eagerly in ``__init__`` so ``redirect_uri`` is known
    before the OAuth flow needs it (the authorization server has to be
    told the redirect URI at the start of the authorization request, well
    before the user actually completes the flow). ``start()`` converts
    the bound socket into a running ``asyncio.Server``; ``wait_for_callback()``
    blocks until the redirect arrives, then tears the server down.

    Single-use by design — a fresh instance per OAuth flow, no recycling.
    The redirect URI is always ``http://127.0.0.1:<port>/callback``.
    """

    def __init__(
        self,
        *,
        host: str = "127.0.0.1",
        timeout: float = _DEFAULT_CALLBACK_TIMEOUT,
    ) -> None:
        self._host = host
        self._timeout = timeout
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, 0))
        self._socket: socket.socket | None = sock
        self._port: int = sock.getsockname()[1]
        self._result: tuple[str, str | None] | None = None
        self._error: str | None = None
        self._received = asyncio.Event()
        self._server: asyncio.Server | None = None

    @property
    def port(self) -> int:
        return self._port

    @property
    def redirect_uri(self) -> str:
        return f"http://{self._host}:{self._port}/callback"

    async def start(self) -> None:
        """Begin listening for the OAuth callback. Idempotent."""
        if self._server is not None:
            return
        if self._socket is None:
            msg = "LocalCallbackServer socket is already released — cannot start"
            raise RuntimeError(msg)
        self._server = await asyncio.start_server(self._handle_request, sock=self._socket)
        # Server now owns the socket.
        self._socket = None
        logger.debug("OAuth callback server listening on {}", self.redirect_uri)

    async def _handle_request(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        try:
            request_line = await reader.readline()
            line = request_line.decode("latin-1", errors="replace").strip()
            # Drain headers — we only need the request line.
            while True:
                hdr = await reader.readline()
                if not hdr or hdr in (b"\r\n", b"\n"):
                    break

            _method, _, rest = line.partition(" ")
            target, _, _ = rest.partition(" ")
            parsed = urlparse(target)
            params = parse_qs(parsed.query)
            code = params.get("code", [""])[0]
            state_list = params.get("state")
            state = state_list[0] if state_list else None
            err = params.get("error", [""])[0]
            err_desc = params.get("error_description", [""])[0]

            if code:
                self._result = (code, state)
                self._received.set()
                self._respond(writer, b"200 OK", _SUCCESS_HTML)
            else:
                self._error = err_desc or err or "missing 'code' parameter"
                logger.warning("OAuth callback returned error: {}", self._error)
                self._respond(writer, b"400 Bad Request", _ERROR_HTML)
                self._received.set()
        except Exception as exc:
            logger.warning("OAuth callback handler error: {}", exc)
            self._error = f"callback handler error: {exc}"
            self._received.set()
        finally:
            with contextlib.suppress(Exception):
                writer.close()
                await writer.wait_closed()

    @staticmethod
    def _respond(writer: asyncio.StreamWriter, status: bytes, body: bytes) -> None:
        writer.write(b"HTTP/1.1 " + status + b"\r\n")
        writer.write(b"Content-Type: text/html; charset=utf-8\r\n")
        writer.write(f"Content-Length: {len(body)}\r\n".encode())
        writer.write(b"Connection: close\r\n\r\n")
        writer.write(body)

    async def wait_for_callback(self) -> tuple[str, str | None]:
        """Block until the OAuth callback arrives. Returns (code, state).

        Raises ``TimeoutError`` if the user doesn't complete the flow
        within the configured timeout, or ``RuntimeError`` if the
        callback arrived with an error parameter instead of a code.
        Always tears the server down before returning.
        """
        try:
            await asyncio.wait_for(self._received.wait(), timeout=self._timeout)
        finally:
            await self.aclose()
        if self._result is not None:
            return self._result
        err = self._error or "no callback received"
        raise RuntimeError(f"OAuth callback failed: {err}")

    async def aclose(self) -> None:
        """Shut down the server and release the socket. Idempotent."""
        if self._server is not None:
            self._server.close()
            with contextlib.suppress(Exception):
                await self._server.wait_closed()
            self._server = None
        if self._socket is not None:
            with contextlib.suppress(Exception):
                self._socket.close()
            self._socket = None

    def __del__(self) -> None:  # pragma: no cover - best-effort GC cleanup
        # Close the held socket if start() was never called (e.g. the
        # OAuth flow never actually needed auth because a cached token
        # was used). asyncio.Server cleanup is async and not reachable
        # from __del__; rely on the loop's own teardown there.
        if self._socket is not None:
            with contextlib.suppress(Exception):
                self._socket.close()


# --- Redirect handler --------------------------------------------------------


def _is_headless() -> bool:
    """Best-effort detection of environments where opening a browser fails.

    Honors the ``DREADNODE_HEADLESS`` opt-out for users who'd prefer to
    complete OAuth manually even on a desktop machine. On Linux,
    absence of ``DISPLAY`` and ``WAYLAND_DISPLAY`` is taken as a strong
    signal (SSH, container, headless CI). On macOS/Windows we trust
    ``webbrowser.open``'s return value instead.
    """
    if os.environ.get("DREADNODE_HEADLESS", "").strip().lower() in ("1", "true", "yes", "on"):
        return True
    if sys.platform.startswith("linux"):
        if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
            return True
    return False


async def _browser_open_redirect_handler(url: str) -> None:
    """Open the user's browser to *url*, or log it prominently if we can't.

    The localhost callback server is the user's only way to deliver the
    OAuth code back to us, so this handler must succeed *or* surface a
    very clear manual fallback. ``DREADNODE_HEADLESS=1`` forces the
    fallback path even on a desktop, which is useful for SSH sessions
    that forward a port but no display.
    """
    if _is_headless():
        logger.warning(
            "MCP OAuth: browser disabled (DREADNODE_HEADLESS or no display). "
            "Visit this URL to authorize:\n  {}",
            url,
        )
        return

    try:
        opened = webbrowser.open(url, new=1, autoraise=True)
    except Exception as exc:
        logger.debug("webbrowser.open raised: {}", exc)
        opened = False

    if opened:
        logger.info("MCP OAuth: opened browser for authorization. Complete the flow to continue.")
    else:
        logger.warning(
            "MCP OAuth: could not open a browser. Visit this URL manually:\n  {}",
            url,
        )


async def _default_redirect_handler(url: str) -> None:
    """Backwards-compat shim — log-only handler, kept for external callers
    that explicitly pass it. New defaults use ``_browser_open_redirect_handler``.
    """
    logger.info("MCP OAuth: Visit this URL to authorize:\n  {}", url)


async def _deferred_redirect_handler(url: str) -> None:
    """Non-interactive redirect handler: refuse to open a browser.

    Used by background connects (CAP-MCP-010). When the OAuth flow reaches
    the point of opening the authorization URL, we raise instead — the
    lifecycle classifies the server ``needs_auth`` and the user opens the
    browser later via an explicit Authenticate. The URL is logged at debug
    so it's recoverable for diagnostics, never auto-opened.
    """
    logger.debug("MCP OAuth: authorization required (deferred, non-interactive): {}", url)
    raise MCPOAuthRequiredError(f"OAuth authorization required for {url}")


async def _deferred_callback_handler() -> tuple[str, str | None]:
    """Non-interactive callback handler — never reached.

    The deferred redirect handler raises before any callback is awaited;
    this exists only to satisfy the provider's handler-pair contract.
    """
    raise MCPOAuthRequiredError("OAuth authorization required (non-interactive)")


def create_oauth_provider(
    server_url: str,
    config: OAuthConfig | None = None,
    storage: "TokenStorage | None" = None,
    redirect_handler: Callable[[str], Awaitable[None]] | None = None,
    callback_handler: Callable[[], Awaitable[tuple[str, str | None]]] | None = None,
    *,
    interactive: bool = True,
    callback_server: LocalCallbackServer | None = None,
) -> "OAuthClientProvider":
    """Build an :class:`OAuthClientProvider` wired with working defaults.

    If neither ``redirect_handler`` nor ``callback_handler`` is provided,
    the function wires the pair according to ``interactive``:

    - ``interactive=True`` (user-initiated): spin up a
      :class:`LocalCallbackServer`, open the user's browser (falling back to
      a logged URL when headless), and block on the callback server until the
      redirect arrives. The OAuth flow completes end-to-end.
    - ``interactive=False`` (background/startup): never open a browser. A
      valid stored token is still used/refreshed transparently; if the flow
      would actually need to authorize, the deferred redirect handler raises
      :class:`MCPOAuthRequiredError` so the runtime classifies ``needs_auth`` and
      defers the browser to a user-initiated Authenticate (CAP-MCP-010).

    Passing a custom ``redirect_handler`` *and* ``callback_handler``
    bypasses the defaults entirely — useful for custom UIs (in-TUI
    overlay, IDE picker, etc.).

    Args:
        server_url: The MCP server URL.
        config: OAuth configuration. Uses defaults if None.
        storage: Token storage. Defaults to :class:`FileTokenStorage`.
        redirect_handler: Called with the authorization URL. Defaults per
            ``interactive`` (browser-open, or deferred raise).
        callback_handler: Called to retrieve ``(code, state)`` from the
            redirect. Defaults to blocking on a localhost callback server.
        interactive: Whether this connect may open a browser. Defaults True.
        callback_server: Inject a pre-built callback server (testing).
    """
    from mcp.client.auth.oauth2 import OAuthClientProvider
    from mcp.shared.auth import OAuthClientMetadata

    config = config or OAuthConfig()

    if storage is None:
        storage = FileTokenStorage(server_url)

    # If the caller didn't fully customize the handlers, set up the default
    # pair. We do this even when only one side is overridden — that path is
    # symmetric, both halves must come from the caller.
    redirect_uris: list[t.Any] | None = None
    if redirect_handler is None and callback_handler is None:
        if not interactive:
            # Background connect: stored tokens still work, but never pop a
            # browser. The deferred handler raises if authorization is needed.
            redirect_handler = _deferred_redirect_handler
            callback_handler = _deferred_callback_handler
        else:
            if callback_server is None:
                callback_server = LocalCallbackServer()
            captured_server = callback_server  # bind for closures + type narrowing

            async def _redirect(url: str) -> None:
                await captured_server.start()
                await _browser_open_redirect_handler(url)

            redirect_handler = _redirect
            callback_handler = captured_server.wait_for_callback
            redirect_uris = [captured_server.redirect_uri]

    client_metadata = OAuthClientMetadata(
        redirect_uris=redirect_uris,
        client_name=config.client_name,
        scope=config.scope,
    )

    return OAuthClientProvider(
        server_url=server_url,
        client_metadata=client_metadata,
        storage=storage,
        redirect_handler=redirect_handler or _default_redirect_handler,
        callback_handler=callback_handler,
    )

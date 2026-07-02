"""
MCP client — connecting to MCP servers and discovering tools.

Supports stdio and streamable-http transports, with SSE as an internal
fallback for streamable-http connections.
"""

import asyncio
import contextlib
import typing as t
import warnings
from contextlib import AsyncExitStack
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType

import anyio
import httpx
from loguru import logger
from mcp.shared.exceptions import McpError
from mcp.types import CONNECTION_CLOSED

from dreadnode.agents.mcp.config import (
    DEFAULT_HTTP_TIMEOUT,
    DEFAULT_INIT_TIMEOUT,
    DEFAULT_SSE_READ_TIMEOUT,
    MCPStatus,
    ServerConfig,
    SSEConnection,
    StdioConnection,
    StdioServerConfig,
    Transport,
)
from dreadnode.agents.tools import Tool
from dreadnode.app.paths import rotate_log
from dreadnode.generators.models import ErrorModel

if t.TYPE_CHECKING:
    from mcp import ClientSession
    from mcp.types import CallToolResult

    from dreadnode.generators.message import Content


# An interactive (user-initiated) OAuth connect blocks on a human browser
# round-trip, so the per-step init timeout must comfortably exceed the
# localhost callback server's wait (_DEFAULT_CALLBACK_TIMEOUT = 300s).
# Background connects keep the normal, tight init timeout.
_INTERACTIVE_AUTH_INIT_TIMEOUT = 330.0

# Transport-level retry for tool calls. A retry is only useful if we rebuild
# the underlying session first; retrying the same dead session cannot recover.
_TOOL_CALL_RETRIES = 1
_TOOL_CALL_RETRY_DELAY = 1.0  # seconds


class _StderrCapture:
    """Async reader that buffers the last N lines from a pipe fd.

    Used to capture MCP subprocess stderr without blocking and without
    letting it spill into the parent terminal. On connection failure the
    buffered lines are included in the error message so users can see
    why the server process crashed.

    When a ``log_path`` is provided, each captured line is also tee'd to
    disk so operators can ``tail -f`` the server's stderr — matching the
    subprocess-worker convention under ``~/.dreadnode/logs/``.
    """

    _MAX_LINES = 50

    def __init__(
        self,
        read_fd: int,
        exit_stack: AsyncExitStack,
        *,
        log_path: Path | None = None,
    ) -> None:
        import os
        import threading

        self._lines: list[str] = []
        self._read_file = os.fdopen(read_fd, "r")
        self._log_file = self._open_log_file(log_path)

        def _reader() -> None:
            try:
                for raw in self._read_file:
                    if self._log_file is not None:
                        # Don't let a disk-side failure break the in-memory
                        # buffer or the connection itself.
                        with contextlib.suppress(OSError):
                            self._log_file.write(raw)
                    line = raw.rstrip("\n")
                    if line:
                        logger.debug("MCP stderr: {}", line)
                        self._lines.append(line)
                        if len(self._lines) > self._MAX_LINES:
                            self._lines.pop(0)
            except (OSError, ValueError):
                pass  # fd closed

        self._thread = threading.Thread(target=_reader, daemon=True)
        self._thread.start()
        exit_stack.callback(self._close)

    @staticmethod
    def _open_log_file(log_path: Path | None) -> t.TextIO | None:
        """Open the stderr log file for writing, or ``None`` on failure.

        Rotates the prior log to ``<path>.prev`` first, so a failed connect
        leaves the previous session's stderr intact for diffing. Truncates
        on open, line-buffered so ``tail -f`` reflects new output
        immediately.
        """
        if log_path is None:
            return None
        rotate_log(log_path)
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            return log_path.open("w", buffering=1, encoding="utf-8", errors="replace")
        except OSError as exc:
            logger.warning(
                "MCP stderr capture: failed to open log file '{}' ({}); keeping in-memory buffer only",
                log_path,
                exc,
            )
            return None

    def _close(self) -> None:
        with contextlib.suppress(OSError):
            self._read_file.close()
        if self._log_file is not None:
            with contextlib.suppress(OSError):
                self._log_file.close()
            self._log_file = None
        self._thread.join(timeout=1)

    @property
    def output(self) -> str:
        """Return captured stderr as a single string."""
        return "\n".join(self._lines)

    @property
    def last_lines(self) -> list[str]:
        """Return the buffered lines."""
        return list(self._lines)


def _convert_mcp_result_to_message_parts(result: "CallToolResult") -> list[t.Any]:
    from mcp.types import TextResourceContents

    from dreadnode.generators.message import ContentImageUrl, ContentText

    parts: list[Content] = []
    for content in result.content:
        if content.type == "text":
            parts.append(ContentText(text=content.text))  # ty: ignore[unresolved-attribute]  # ty can't narrow MCP union by .type discriminator
        elif content.type == "image":
            parts.append(ContentImageUrl.from_url(f"data:{content.mimeType};base64,{content.data}"))  # ty: ignore[unresolved-attribute]  # ty can't narrow MCP union by .type discriminator
        elif content.type == "resource":
            resource = content.resource  # ty: ignore[unresolved-attribute]  # ty can't narrow MCP union by .type discriminator
            resource_text = (
                resource.text if isinstance(resource, TextResourceContents) else resource.blob
            )
            parts.append(ContentText(text=resource_text))
        else:
            raise ValueError(f"Unknown content type: {content.type}")
    return parts


@dataclass
class MCPClient:
    """A client for communicating with MCP servers.

    Supports stdio and streamable-http transports. For streamable-http,
    SSE is used as an automatic fallback if the server doesn't support
    the streamable HTTP protocol.

    Can be used as an async context manager or via explicit connect/disconnect:

        # Context manager (existing pattern)
        async with mcp("stdio", command="uv", args=["run", "server"]) as client:
            agent = Agent(tools=list(client.tools))

        # Explicit lifecycle (for managed servers)
        client = MCPClient.from_config(StdioServerConfig(command="uv"))
        await client.connect()
        try:
            ...
        finally:
            await client.disconnect()
    """

    transport: Transport
    """The transport type"""
    connection: StdioConnection | SSEConnection | dict[str, t.Any]
    """Connection configuration"""
    tools: list[Tool[..., t.Any]]
    """Tools discovered from the server"""

    _status: MCPStatus
    _error: str | None
    _exit_stack: AsyncExitStack
    _session: "ClientSession | None"
    _oauth_config: t.Any  # OAuthConfig | None
    _owner_task: asyncio.Task[None] | None
    _shutdown_event: asyncio.Event | None
    _ready_future: asyncio.Future[None] | None
    _lifecycle_lock: asyncio.Lock | None

    def __init__(
        self,
        transport: Transport | t.Literal["sse"],
        connection: "StdioConnection | SSEConnection | dict[str, t.Any]",
        *,
        oauth: t.Any = None,
        init_timeout: float = DEFAULT_INIT_TIMEOUT,
        log_path: Path | None = None,
    ) -> None:
        # Handle deprecated "sse" transport
        if transport == "sse":
            warnings.warn(
                'Transport "sse" is deprecated, use "streamable-http" instead. '
                "SSE is used as an automatic fallback.",
                DeprecationWarning,
                stacklevel=2,
            )
            transport = "streamable-http"

        self.transport = transport
        self.connection = connection
        self.tools = []
        self._status = MCPStatus.DISCONNECTED
        self._error = None
        self._exit_stack = AsyncExitStack()
        self._session = None
        self._oauth_config = oauth
        # Whether the in-flight connect may open a browser for OAuth. Set by
        # connect(); defaults to the conservative non-interactive mode so a
        # browser only opens when a caller explicitly opts in (the runtime does
        # this on a user-initiated reconnect) — not from a background/startup
        # connect (CAP-MCP-010: the runtime owns the browser-open moment).
        self._auth_interactive = False
        self._init_timeout = init_timeout
        # Only meaningful for stdio transports — the stderr capture wires it
        # into _StderrCapture on connect. HTTP transports ignore it.
        self._log_path = log_path
        self._stderr_capture: _StderrCapture | None = None
        self._owner_task = None
        self._shutdown_event = None
        self._ready_future = None
        self._lifecycle_lock = None

    @classmethod
    def from_config(cls, config: ServerConfig, *, log_path: Path | None = None) -> "MCPClient":
        """Create a client from a typed server config.

        The SDK's MCP lifecycle manager passes ``log_path`` to tee stderr
        under ``~/.dreadnode/logs/``. User-code callers of
        :func:`dreadnode.agents.mcp` don't need to supply it.
        """
        if isinstance(config, StdioServerConfig):
            connection: StdioConnection = StdioConnection(
                command=config.command,
                args=config.args,
                cwd=config.cwd,
                env=config.env,
            )
            return cls(
                "stdio",
                connection,
                init_timeout=config.init_timeout,
                log_path=log_path,
            )

        # HttpServerConfig
        connection_dict: dict[str, t.Any] = {
            "url": config.url,
            "headers": config.headers,
            "timeout": config.timeout,
            "sse_read_timeout": config.sse_read_timeout,
        }
        return cls(
            "streamable-http",
            connection_dict,
            oauth=config.oauth,
            init_timeout=config.init_timeout,
            log_path=log_path,
        )

    @property
    def status(self) -> MCPStatus:
        return self._status

    @property
    def error(self) -> str | None:
        """Error message if status is FAILED or NEEDS_AUTH."""
        return self._error

    @property
    def log_path(self) -> Path | None:
        """Path that stderr is tee'd to, or ``None`` if capture is in-memory only.

        Only populated for stdio transports; HTTP transports don't spawn a
        subprocess and have nothing to capture.
        """
        return self._log_path

    @property
    def recent_stderr(self) -> list[str]:
        """Captured stderr lines from the subprocess, bounded by the ring buffer.

        Mirrors :attr:`SubprocessWorkerRunner.recent_output` so the TUI can
        render the same progressive-disclosure block for MCP servers and
        workers. Empty for HTTP transports or before :meth:`connect` runs.
        """
        if self._stderr_capture is None:
            return []
        return self._stderr_capture.last_lines

    @property
    def session(self) -> "ClientSession":
        if self._session is None:
            raise RuntimeError("Session not initialized — call connect() first")
        return self._session

    def _is_retryable_tool_call_error(self, exc: BaseException) -> bool:
        if isinstance(exc, (anyio.BrokenResourceError, anyio.ClosedResourceError)):
            return True
        if isinstance(exc, McpError):
            # The MCP SDK normalizes transport breakage into McpError codes:
            #   - REQUEST_TIMEOUT (408): the server was unresponsive and the
            #     request read timed out (``mcp/shared/session.py``).
            #   - CONNECTION_CLOSED (-32000): the read stream closed while a
            #     call was in flight, so the receive loop drained every pending
            #     request with this code (``mcp/shared/session.py`` finally
            #     block). This is the dominant "server flaked mid-call" case.
            # Both are transport-class and recover with a reconnect; all other
            # codes are protocol-level errors the server meant to send.
            return exc.error.code in (httpx.codes.REQUEST_TIMEOUT, CONNECTION_CLOSED)
        return (
            isinstance(exc, RuntimeError)
            and self._owner_task is not None
            and str(exc) == "Session not initialized — call connect() first"
        )

    async def _reconnect_for_tool_retry(
        self, tool_name: str, attempt: int, exc: BaseException
    ) -> None:
        logger.debug(
            "MCP tool '{}' transport failure (attempt {}), reconnecting before retry: {}",
            tool_name,
            attempt + 1,
            exc,
        )
        await self._shutdown()
        await asyncio.sleep(_TOOL_CALL_RETRY_DELAY)
        await self.connect(interactive=self._auth_interactive)

    def _make_execute_on_server(self, tool_name: str) -> t.Callable[..., t.Any]:
        async def execute_on_server(**kwargs: t.Any) -> t.Any:
            last_exc: BaseException | None = None
            for attempt in range(_TOOL_CALL_RETRIES + 1):
                try:
                    result = await self.session.call_tool(tool_name, kwargs)
                except Exception as exc:
                    if not self._is_retryable_tool_call_error(exc) or attempt >= _TOOL_CALL_RETRIES:
                        raise
                    last_exc = exc
                    await self._reconnect_for_tool_retry(tool_name, attempt, exc)
                    continue
                else:
                    if attempt > 0:
                        logger.info(
                            "MCP tool '{}' recovered after reconnect on attempt {}",
                            tool_name,
                            attempt + 1,
                        )
                    break
            else:
                # Should not be reached (raise above covers it), but
                # satisfy the type checker.
                assert last_exc is not None
                raise last_exc

            # Protocol-level failures (``isError=true``) are reported as a
            # successful response carrying error content. Lift them into
            # an ``ErrorModel`` so ``Tool.handle_tool_call`` routes the
            # message through the same ``metadata['error']`` path used by
            # ``@tool(catch=True)`` failures (e.g. bash non-zero exits).
            if result.isError:
                error_text = (
                    "\n".join(
                        content.text  # ty: ignore[unresolved-attribute]
                        for content in result.content
                        if content.type == "text"
                    )
                    or f"MCP tool '{tool_name}' reported an error."
                )
                return ErrorModel(content=error_text, type="MCPToolError")
            return _convert_mcp_result_to_message_parts(result)

        return execute_on_server

    def _get_lifecycle_lock(self) -> asyncio.Lock:
        if self._lifecycle_lock is None:
            self._lifecycle_lock = asyncio.Lock()
        return self._lifecycle_lock

    @staticmethod
    def _unwrap_exception(exc: BaseException) -> BaseException:
        cause = exc
        if isinstance(exc, BaseExceptionGroup):
            leaf = exc.exceptions[0] if exc.exceptions else exc
            while isinstance(leaf, BaseExceptionGroup) and leaf.exceptions:
                leaf = leaf.exceptions[0]
            cause = leaf
        return cause

    def _set_error_status(self, exc: BaseException) -> BaseException:
        from dreadnode.agents.mcp.auth import MCPOAuthRequiredError

        cause = self._unwrap_exception(exc)
        error_msg = str(cause)

        # A background connect that hit the deferred OAuth handler: the server
        # needs fresh authorization but we declined to open a browser. This is
        # needs_auth, not a failure — the user authenticates explicitly later.
        if isinstance(cause, MCPOAuthRequiredError):
            self._status = MCPStatus.NEEDS_AUTH
            self._error = error_msg
            return cause

        # The user-facing error report keeps the last 10 lines of stderr
        # so operators can see why the server died at a glance.
        if self._stderr_capture and self._stderr_capture.last_lines:
            stderr_tail = "\n".join(self._stderr_capture.last_lines[-10:])
            error_msg = f"{error_msg}\n\nServer stderr:\n{stderr_tail}"

        # Auth classification scans the *full* captured buffer (capped at
        # 50 lines by _StderrCapture), not just the report tail. Reason:
        # mcp-remote prints "Please authorize…" / "Authentication required"
        # *once*, near the start, then polls a `/wait-for-auth` callback
        # every couple of seconds. By the time the lifecycle hits its
        # init_timeout (60s) and we classify, those early markers have
        # been pushed out of the last-10 window — but they're still in
        # the 50-line buffer. Matching the full buffer makes the
        # classification robust to polling chatter (ENG-6989).
        scan_text = error_msg
        if self._stderr_capture and self._stderr_capture.last_lines:
            scan_text = "\n".join([str(cause), *self._stderr_capture.last_lines])

        scan_lower = scan_text.lower()
        auth_keywords = (
            "unauthorized",
            "forbidden",
            "401",
            "403",
            "oauth",
            "please authorize",
            "authorize this client",
            # mcp-remote-specific markers that survive the buffer even
            # after the bridge polls /wait-for-auth for 60s.
            "authentication required",
            "waiting for authentication",
            "wait-for-auth",
        )
        if any(kw in scan_lower for kw in auth_keywords):
            self._status = MCPStatus.NEEDS_AUTH
        else:
            self._status = MCPStatus.FAILED

        self._error = error_msg
        return cause

    def _reset_connection_state(self) -> None:
        self._session = None
        self.tools.clear()
        if self._status == MCPStatus.CONNECTED:
            self._status = MCPStatus.DISCONNECTED
        self._exit_stack = AsyncExitStack()
        self._stderr_capture = None

    async def _run_connection(self, shutdown_event: asyncio.Event) -> None:
        try:
            if self.transport == "stdio":
                self._session = await self._connect_via_stdio(
                    t.cast("StdioConnection", self.connection),
                )
            elif self.transport == "streamable-http":
                self._session = await self._connect_via_streamable_http(
                    t.cast("dict[str, t.Any]", self.connection),
                )
            else:
                msg = (
                    f"Unsupported transport: {self.transport}. Must be 'stdio' or 'streamable-http'"
                )
                raise TypeError(msg)  # noqa: TRY301

            # An interactive OAuth connect blocks on a human browser round-trip
            # during initialize(), so widen the timeout for that case only.
            init_timeout = (
                max(self._init_timeout, _INTERACTIVE_AUTH_INIT_TIMEOUT)
                if self._auth_interactive and self.transport == "streamable-http"
                else self._init_timeout
            )
            await asyncio.wait_for(self.session.initialize(), timeout=init_timeout)
            await asyncio.wait_for(self._load_tools(), timeout=init_timeout)

            self._status = MCPStatus.CONNECTED
            self._error = None

            if self._ready_future is not None and not self._ready_future.done():
                self._ready_future.set_result(None)

            await shutdown_event.wait()
        except BaseException as exc:
            cause = self._set_error_status(exc)
            if self._ready_future is not None and not self._ready_future.done():
                if isinstance(cause, Exception):
                    self._ready_future.set_exception(cause)
                else:
                    self._ready_future.set_exception(RuntimeError(str(cause)))
        finally:
            try:
                await self._exit_stack.aclose()
            except BaseException:
                # Transport teardown errors (BrokenResourceError, ConnectionReset,
                # BaseExceptionGroup from anyio TaskGroups, etc.) are expected when
                # the subprocess has already exited or the remote HTTP server is
                # gone.  Suppressing here prevents noisy "Task exception was never
                # retrieved" warnings during shutdown.
                logger.debug(
                    "Suppressed error during MCP exit-stack teardown (transport={})", self.transport
                )
            self._reset_connection_state()

    async def _load_tools(self) -> None:
        mcp_tool_result = await self.session.list_tools()

        self.tools.clear()
        self.tools = [
            Tool(
                name=tool.name,
                description=tool.description or "",
                parameters_schema=tool.inputSchema,
                fn=self._make_execute_on_server(tool.name),
            )
            for tool in mcp_tool_result.tools
        ]

    async def _connect_via_stdio(self, connection: StdioConnection) -> "ClientSession":
        import os

        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        # Capture subprocess stderr via an OS pipe instead of letting it spill
        # into the parent terminal. An async reader task buffers the last N
        # lines so we can surface them in error messages on connection failure.
        read_fd, write_fd = os.pipe()
        write_file = os.fdopen(write_fd, "w")

        stderr_capture = _StderrCapture(read_fd, self._exit_stack, log_path=self._log_path)
        self._stderr_capture = stderr_capture

        server_params = StdioServerParameters(**connection)
        try:
            read, write = await self._exit_stack.enter_async_context(
                stdio_client(server_params, errlog=write_file)
            )
        except BaseException:
            # If the subprocess fails to start (e.g. command not found),
            # close the write end so the reader thread sees EOF and exits.
            write_file.close()
            raise
        # Close parent's write end now that the subprocess has inherited
        # the fd. This ensures the pipe reader sees EOF when the subprocess
        # exits, preventing hangs.
        write_file.close()

        return await self._exit_stack.enter_async_context(ClientSession(read, write))

    async def _probe_supports_streamable_http(
        self,
        url: str,
        headers: dict[str, str] | None,
        http_timeout: float,
        auth: t.Any,
        *,
        allow_auth_challenge: bool = False,
    ) -> bool:
        """Probe whether a URL supports streamable HTTP (POST).

        Returns True if the server likely supports streamable HTTP, False if it
        clearly doesn't. Connectivity errors also return False (server
        unreachable via POST, try SSE). Auth and SSL errors are allowed to
        propagate — they would affect SSE equally.

        When ``allow_auth_challenge`` is set (an OAuth provider is attached to
        the real connect), a 401/403 is treated as a streamable-http server
        that simply needs authentication: the probe returns True so the
        authenticated connect runs, instead of raising or routing to SSE.
        """
        try:
            probe_headers = dict(headers) if headers else {}
            probe_headers.update(
                {
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                }
            )
            async with httpx.AsyncClient(timeout=min(http_timeout, 5), auth=auth) as probe:
                r = await probe.post(url, content=b"{}", headers=probe_headers)
                # Auth errors affect both transports equally. With a provider
                # attached the authenticated connect will handle the challenge,
                # so treat the server as streamable-http; otherwise propagate so
                # callers can classify as NEEDS_AUTH instead of falling through.
                if r.status_code in (401, 403):
                    if allow_auth_challenge:
                        logger.debug(
                            "Streamable HTTP probe got {} for {}, deferring to "
                            "authenticated connect",
                            r.status_code,
                            url,
                        )
                        return True
                    r.raise_for_status()
                if r.status_code == 400 and self._looks_like_jsonrpc_probe_rejection(r):
                    logger.debug(
                        "Streamable HTTP probe got JSON-RPC validation error for {}, using streamable-http",
                        url,
                    )
                    return True
                # 400 = bad request (SSE-only server doesn't understand POST body)
                # 404 = endpoint not found for POST
                # 405 = method not allowed (explicitly rejects POST)
                # 415 = unsupported media type (doesn't accept JSON)
                if r.status_code in (400, 404, 405, 415):
                    logger.debug(
                        "Streamable HTTP probe got {} for {}, using SSE",
                        r.status_code,
                        url,
                    )
                    return False
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            logger.debug("Streamable HTTP probe failed for {} ({}), using SSE", url, e)
            return False

        return True

    @staticmethod
    def _looks_like_jsonrpc_probe_rejection(response: httpx.Response) -> bool:
        """Detect JSON-RPC validation errors from real MCP streamable-http servers."""
        content_type = response.headers.get("content-type", "").lower()
        if "application/json" not in content_type:
            return False

        with contextlib.suppress(ValueError):
            payload = response.json()
            if (
                isinstance(payload, dict)
                and payload.get("jsonrpc") == "2.0"
                and isinstance(payload.get("error"), dict)
            ):
                return True

        return False

    async def _connect_via_streamable_http(self, connection: dict[str, t.Any]) -> "ClientSession":
        """Connect via streamable HTTP, falling back to SSE on failure."""
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client

        url = connection["url"]
        headers = connection.get("headers")
        timeout = connection.get("timeout", DEFAULT_HTTP_TIMEOUT)
        sse_read_timeout = connection.get("sse_read_timeout", DEFAULT_SSE_READ_TIMEOUT)

        auth = self._build_auth_provider(url)

        # Probe the URL before entering the streamable-http context manager.
        # SSE-only servers (e.g. Burp Suite MCP) return 4xx on POST, and the
        # upstream MCP SDK's streamable-http transport crashes during cleanup
        # with an uncatchable BaseExceptionGroup. Skip straight to SSE when
        # the server clearly doesn't accept POST.
        #
        # The probe always runs with ``auth=None`` so it stays cheap and never
        # drags the interactive OAuth flow through the short-timeout probe
        # client. When a provider is attached we still need the probe to tell
        # an SSE-only server (4xx POST rejection → SSE) apart from an
        # OAuth-protected streamable-http server (401/403 → proceed to the
        # authenticated connect). ``allow_auth_challenge`` makes the probe
        # treat a 401/403 as "streamable-http, just needs auth" instead of
        # raising, so the authenticated connect runs and the provider handles
        # the challenge.
        if not await self._probe_supports_streamable_http(
            url, headers, timeout, None, allow_auth_challenge=auth is not None
        ):
            return await self._connect_via_sse_internal(connection)

        try:
            ctx = streamablehttp_client(
                url=url,
                headers=headers,
                timeout=timeout,
                sse_read_timeout=sse_read_timeout,
                auth=auth,
            )
            read, write, _ = await self._exit_stack.enter_async_context(ctx)
            return await self._exit_stack.enter_async_context(ClientSession(read, write))
        except (TimeoutError, ConnectionError, OSError) as e:
            logger.debug("Streamable HTTP failed for {}, trying SSE fallback: {}", url, e)

        # Fall back to SSE
        return await self._connect_via_sse_internal(connection)

    async def _connect_via_sse_internal(self, connection: dict[str, t.Any]) -> "ClientSession":
        """Connect via SSE transport (internal fallback)."""
        from mcp import ClientSession
        from mcp.client.sse import sse_client

        url = connection["url"]
        headers = connection.get("headers")
        timeout = connection.get("timeout", DEFAULT_HTTP_TIMEOUT)
        sse_read_timeout = connection.get("sse_read_timeout", DEFAULT_SSE_READ_TIMEOUT)
        # Mirror the streamable-http path: forward the OAuth provider so an
        # SSE-fallback connect to an authenticated server still completes
        # the auth flow rather than 401'ing silently.
        auth = self._build_auth_provider(url)

        ctx = sse_client(
            url=url,
            headers=headers,
            timeout=timeout,
            sse_read_timeout=sse_read_timeout,
            auth=auth,
        )
        read, write = await self._exit_stack.enter_async_context(ctx)
        return await self._exit_stack.enter_async_context(ClientSession(read, write))

    def _build_auth_provider(self, url: str) -> t.Any:
        """Build an httpx.Auth OAuth provider for a streamable-http server.

        Reactive-by-default (CAP-MCP-011): every HTTP server gets a provider so
        a 401 can drive RFC 9728 / RFC 8414 discovery + DCR + PKCE without the
        manifest pre-declaring anything. The provider stays dormant unless the
        server actually challenges with a 401 — it only adds an auth header
        when it holds a valid token — so it's a no-op for public servers and
        for servers using static header / API-key auth (their headers win).

        A declared ``auth:`` block (``self._oauth_config``) is an optional
        refinement carrying ``scope`` / ``client_name``; it's no longer a
        precondition for OAuth.

        In a background (non-interactive) connect we attach a provider only
        when a token is already stored: with one it's used/refreshed silently;
        without one we return ``None`` so a 401 surfaces as ``needs_auth`` with
        no discovery traffic and no browser. The user then authenticates via
        an interactive reconnect.
        """
        from dreadnode.agents.mcp.auth import FileTokenStorage, create_oauth_provider
        from dreadnode.agents.mcp.config import OAuthConfig

        if not self._auth_interactive and not FileTokenStorage(url).has_tokens():
            return None

        config = self._oauth_config or OAuthConfig()
        return create_oauth_provider(
            server_url=url, config=config, interactive=self._auth_interactive
        )

    async def connect(self, *, interactive: bool = False) -> None:
        """Connect to the MCP server and discover tools.

        Sets status to CONNECTED on success, FAILED or NEEDS_AUTH on error.

        ``interactive`` controls OAuth behavior for streamable-http servers.
        It defaults to False (the safe, non-interactive mode): a stored token
        is still used/refreshed, but a server that needs fresh authorization
        is left in ``needs_auth`` rather than opening a browser. Pass
        ``interactive=True`` for a user-initiated connect (the runtime does
        this on reconnect) to open the user's browser and complete OAuth.
        """
        self._auth_interactive = interactive
        async with self._get_lifecycle_lock():
            if self._owner_task is not None and not self._owner_task.done():
                ready_future = self._ready_future
            else:
                self._reset_connection_state()
                self._shutdown_event = asyncio.Event()
                self._ready_future = asyncio.get_running_loop().create_future()
                self._owner_task = asyncio.create_task(
                    self._run_connection(self._shutdown_event),
                    name=f"mcp-client:{self.transport}",
                )
                ready_future = self._ready_future

        assert ready_future is not None
        await ready_future

    async def disconnect(self) -> None:
        """Disconnect from the MCP server."""
        await self._shutdown()

    async def _shutdown(self) -> None:
        async with self._get_lifecycle_lock():
            owner_task = self._owner_task
            shutdown_event = self._shutdown_event
            if owner_task is None:
                self._reset_connection_state()
                return
            if shutdown_event is not None:
                shutdown_event.set()

        await owner_task

        async with self._get_lifecycle_lock():
            if self._owner_task is owner_task:
                self._owner_task = None
                self._shutdown_event = None
                self._ready_future = None

    async def __aenter__(self) -> "MCPClient":
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._shutdown()
        self._status = MCPStatus.DISCONNECTED


# --- Factory function ---


@t.overload
def mcp(
    transport: t.Literal["stdio"],
    *,
    command: str,
    args: list[str] | None = None,
    cwd: str | Path | None = None,
    env: dict[str, str] | None = None,
    init_timeout: float = DEFAULT_INIT_TIMEOUT,
) -> MCPClient: ...


@t.overload
def mcp(
    transport: t.Literal["streamable-http"],
    *,
    url: str,
    headers: dict[str, str] | None = None,
    oauth: t.Any = None,
    timeout: float = DEFAULT_HTTP_TIMEOUT,
    sse_read_timeout: float = DEFAULT_SSE_READ_TIMEOUT,
    init_timeout: float = DEFAULT_INIT_TIMEOUT,
) -> MCPClient: ...


@t.overload
def mcp(
    transport: t.Literal["sse"],
    *,
    url: str,
    headers: dict[str, str] | None = None,
    timeout: float = DEFAULT_HTTP_TIMEOUT,
    sse_read_timeout: float = DEFAULT_SSE_READ_TIMEOUT,
    init_timeout: float = DEFAULT_INIT_TIMEOUT,
) -> MCPClient: ...


def mcp(transport: "Transport | t.Literal['sse']", **kwargs: t.Any) -> MCPClient:
    """Create an MCP client.

    Args:
        transport: Transport type — "stdio" or "streamable-http".
            "sse" is accepted but deprecated (routes to streamable-http
            with SSE fallback).

    Returns:
        An MCPClient instance (use as async context manager or call connect()).

    Examples:
        ```python
        # stdio transport
        async with mcp("stdio", command="uv", args=["run", "weather-mcp"]) as client:
            agent = Agent(tools=list(client.tools))

        # streamable-http transport
        async with mcp("streamable-http", url="https://api.example.com/mcp") as client:
            agent = Agent(tools=list(client.tools))

        # streamable-http with OAuth
        from dreadnode.agents.mcp import OAuthConfig
        async with mcp("streamable-http", url="https://...", oauth=OAuthConfig()) as client:
            agent = Agent(tools=list(client.tools))
        ```
    """
    oauth = kwargs.pop("oauth", None)
    init_timeout = kwargs.pop("init_timeout", DEFAULT_INIT_TIMEOUT)
    connection = t.cast("StdioConnection | SSEConnection | dict[str, t.Any]", kwargs)
    return MCPClient(transport, connection, oauth=oauth, init_timeout=init_timeout)

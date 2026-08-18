"""HTTP (Streamable HTTP) MCP capability adapter."""

import asyncio
import contextlib
from typing import Any

import httpx
import structlog
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.types import CallToolResult, PaginatedRequestParams

from mistralai.vibe.sdk.capabilities.mcp.adapters.base import McpAdapterBase
from mistralai.vibe.sdk.capabilities.mcp.config import HttpMcpConfig
from mistralai.vibe.sdk.capabilities.mcp.types import McpToolDescriptor

__all__ = [
    "HttpMcpAdapter",
]

logger = structlog.get_logger()


class HttpMcpAdapter(McpAdapterBase[HttpMcpConfig]):
    """Stateless adapter for HTTP-based MCP servers.

    Each ``list_tools`` / ``invoke_tool`` call opens a fresh MCP session
    over Streamable HTTP, performs the operation, and tears it down.
    """

    def __init__(self, config: HttpMcpConfig) -> None:
        super().__init__(config)
        self._http_client: httpx.AsyncClient | None = None
        self._stack: contextlib.AsyncExitStack | None = None
        self._lifecycle_lock = asyncio.Lock()

    @property
    def _timeout_s(self) -> float:
        return self._config.timeout_ms / 1000

    @property
    def _sse_read_timeout_s(self) -> float:
        return self._config.sse_read_timeout_ms / 1000

    @property
    def _log_context(self) -> dict[str, Any]:
        return {"url": self._config.url}

    async def setup(self) -> None:
        async with self._lifecycle_lock:
            if self._stack is not None:
                return

            stack = contextlib.AsyncExitStack()
            try:
                client = await stack.enter_async_context(
                    httpx.AsyncClient(
                        headers=self._config.headers,
                        timeout=httpx.Timeout(
                            self._timeout_s,
                            read=self._sse_read_timeout_s,
                        ),
                        follow_redirects=True,
                    )
                )
            except BaseException:
                await stack.aclose()
                raise

            self._http_client = client
            self._stack = stack

    async def list_tools(self) -> list[McpToolDescriptor]:
        http_client = self._require_client()

        async with (
            streamable_http_client(
                self._config.url,
                http_client=http_client,
            ) as (read, write, _),
            ClientSession(read, write) as session,
        ):
            await asyncio.wait_for(session.initialize(), timeout=self._timeout_s)
            raw_tools = await self._collect_paged_tools(
                lambda cursor: asyncio.wait_for(
                    session.list_tools(params=PaginatedRequestParams(cursor=cursor)),
                    timeout=self._timeout_s,
                )
            )

        return self._normalize_tools(raw_tools)

    async def invoke_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> CallToolResult:
        http_client = self._require_client()

        async with (
            streamable_http_client(
                self._config.url,
                http_client=http_client,
            ) as (read, write, _),
            ClientSession(read, write) as session,
        ):
            await asyncio.wait_for(session.initialize(), timeout=self._timeout_s)
            # Rely on the httpx client's read timeout (sse_read_timeout_ms) rather than
            # a coroutine-level wait_for, so long-running streaming responses aren't
            # cancelled before the SSE read window expires.
            return await session.call_tool(tool_name, arguments)

    async def teardown(self) -> None:
        # Assumes the caller (ResourcesScope) has drained all in-flight acquire/operations
        # before invoking teardown, so closing the httpx client here is safe.
        async with self._lifecycle_lock:
            stack, self._stack = self._stack, None
            self._http_client = None
            if stack is None:
                return
            try:
                await stack.aclose()
            except Exception as exc:
                logger.warning(
                    "mcp.teardown.failed",
                    mcp_server_key=self.server_key,
                    **self._log_context,
                    exc_info=exc,
                )

    def _require_client(self) -> httpx.AsyncClient:
        if self._http_client is None:
            raise RuntimeError("HttpMcpAdapter.setup() must be called before use")
        return self._http_client

"""Stdio MCP capability adapter."""

import asyncio
import contextlib
from functools import cached_property
from pathlib import Path
from typing import Any

import structlog
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import CallToolResult, PaginatedRequestParams

from mistralai.vibe.sdk.capabilities.mcp.adapters.base import McpAdapterBase
from mistralai.vibe.sdk.capabilities.mcp.config import StdioMcpConfig
from mistralai.vibe.sdk.capabilities.mcp.types import McpToolDescriptor

__all__ = [
    "StdioMcpAdapter",
]

logger = structlog.get_logger()


class StdioMcpAdapter(McpAdapterBase[StdioMcpConfig]):
    """Lifecycle wrapper around a single stdio MCP server."""

    def __init__(self, config: StdioMcpConfig) -> None:
        super().__init__(config)
        self._stack: contextlib.AsyncExitStack | None = None
        self._session: ClientSession | None = None
        self._lifecycle_lock = asyncio.Lock()

    @cached_property
    def _params(self) -> StdioServerParameters:
        return self._config.to_stdio_parameters()

    @cached_property
    def _program(self) -> str:
        return Path(self._params.command).name

    @property
    def _timeout_s(self) -> float:
        return self._config.timeout_ms / 1000

    @property
    def session(self) -> ClientSession:
        if self._session is None:
            raise RuntimeError("StdioMcpAdapter.setup() must be called before use")
        return self._session

    async def setup(self) -> None:
        """Set up the MCP server and establish a client session."""
        async with self._lifecycle_lock:
            if self._session is not None:
                return
            stack = contextlib.AsyncExitStack()
            try:
                read, write = await stack.enter_async_context(stdio_client(self._params))
                session = await stack.enter_async_context(ClientSession(read, write))
                await asyncio.wait_for(session.initialize(), timeout=self._timeout_s)
            except BaseException:
                await stack.aclose()
                raise
            self._stack = stack
            self._session = session

    @property
    def _log_context(self) -> dict[str, Any]:
        return {"program": self._program}

    async def list_tools(self) -> list[McpToolDescriptor]:
        """List tools advertised by the MCP server."""
        session = self.session
        raw_tools: list[Any] = []
        cursor = None
        while True:
            result = await asyncio.wait_for(
                session.list_tools(params=PaginatedRequestParams(cursor=cursor)),
                timeout=self._timeout_s,
            )
            raw_tools.extend(result.tools)
            cursor = result.nextCursor
            if cursor is None:
                break
        return self._normalize_tools(raw_tools)

    async def invoke_tool(self, tool_name: str, arguments: dict[str, Any]) -> CallToolResult:
        """Invoke a tool on the MCP server."""
        return await asyncio.wait_for(
            self.session.call_tool(tool_name, arguments), timeout=self._timeout_s
        )

    async def teardown(self) -> None:
        """Tear down the MCP server and clean up resources."""
        async with self._lifecycle_lock:
            stack, self._stack = self._stack, None
            self._session = None
            if not stack:
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

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
        self._session: ClientSession | None = None
        self._lifecycle_lock = asyncio.Lock()
        self._owner_task: asyncio.Task[None] | None = None
        self._shutdown: asyncio.Event | None = None

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
            ready: asyncio.Future[None] = asyncio.get_running_loop().create_future()
            self._shutdown = asyncio.Event()
            self._owner_task = asyncio.create_task(self._run(ready, self._shutdown))
            try:
                await ready
            except BaseException:
                self._owner_task.cancel()

                with contextlib.suppress(BaseException):
                    await self._owner_task
                self._owner_task = None
                self._shutdown = None
                raise

    async def _run(self, ready: asyncio.Future[None], shutdown: asyncio.Event) -> None:
        """Own the connection: enter the anyio contexts, serve, then exit them here."""
        stack = contextlib.AsyncExitStack()
        try:
            read, write = await stack.enter_async_context(stdio_client(self._params))
            session = await stack.enter_async_context(ClientSession(read, write))
            await asyncio.wait_for(session.initialize(), timeout=self._timeout_s)
        except BaseException as exc:
            try:
                await stack.aclose()
            except Exception:
                logger.warning(
                    "mcp.setup.cleanup_failed",
                    mcp_server_key=self.server_key,
                    **self._log_context,
                    exc_info=True,
                )
            finally:
                # Make sure a failed cleanup does not block the future resolution.
                if not ready.done():
                    ready.set_exception(exc)
            return

        self._session = session

        if not ready.done():
            ready.set_result(None)
        try:
            await shutdown.wait()
        finally:
            self._session = None
            await stack.aclose()

    @property
    def _log_context(self) -> dict[str, Any]:
        return {"program": self._program}

    async def list_tools(self) -> list[McpToolDescriptor]:
        """List tools advertised by the MCP server."""
        session = self.session
        raw_tools = await self._collect_paged_tools(
            lambda cursor: asyncio.wait_for(
                session.list_tools(params=PaginatedRequestParams(cursor=cursor)),
                timeout=self._timeout_s,
            )
        )
        return self._normalize_tools(raw_tools)

    async def invoke_tool(self, tool_name: str, arguments: dict[str, Any]) -> CallToolResult:
        """Invoke a tool on the MCP server."""
        return await asyncio.wait_for(
            self.session.call_tool(tool_name, arguments), timeout=self._timeout_s
        )

    async def teardown(self) -> None:
        """Tear down the MCP server and clean up resources."""
        async with self._lifecycle_lock:
            owner_task, self._owner_task = self._owner_task, None
            shutdown, self._shutdown = self._shutdown, None
            self._session = None
            if owner_task is None:
                return
            if shutdown is not None:
                shutdown.set()
            try:
                await owner_task
            except Exception as exc:
                logger.warning(
                    "mcp.teardown.failed",
                    mcp_server_key=self.server_key,
                    **self._log_context,
                    exc_info=exc,
                )

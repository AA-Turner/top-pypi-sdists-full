"""HTTP MCP tool server base class for Plato worlds.

Provides a reusable FastMCP server that exposes ToolDefinitions over HTTP
transport. Worlds subclass ToolServer, override `build_tools()` to define
their tools, and call `start()` / `close()` to manage the server lifecycle.

Usage::

    from pydantic import BaseModel, Field
    from plato.tools import ToolDefinition
    from plato.tools.server import ToolServer

    class HelloInput(BaseModel):
        name: str = Field(description="Name to greet")

    class MyWorldTools(ToolServer):
        def build_tools(self) -> list[ToolDefinition]:
            return [
                ToolDefinition(
                    name="hello",
                    description="Say hello",
                    input_model=HelloInput,
                    handler=self._hello,
                ),
            ]

        async def _hello(self, args: HelloInput) -> dict:
            return {"message": f"Hello, {args.name}!"}

    server = MyWorldTools(name="My Tools", port=8765)
    await server.start()
    # ... agent connects to http://host:8765/mcp ...
    await server.close()
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import logging
from typing import Any

from fastmcp import FastMCP

from plato.tools.definition import ToolDefinition

logger = logging.getLogger(__name__)


class ToolServer:
    """HTTP MCP server that exposes ToolDefinitions via FastMCP.

    Subclasses must override ``build_tools()`` to return their tool list.
    All tools must use ``input_model`` (Pydantic BaseModel) for typed schemas.
    The server registers all tools at construction time and serves them
    over HTTP transport when ``start()`` is called.

    Args:
        name: Display name for the MCP server.
        host: Bind address (default ``"0.0.0.0"``).
        port: Bind port (default ``8765``).
    """

    def __init__(
        self,
        *,
        name: str = "Plato Tools",
        host: str = "0.0.0.0",
        port: int = 8765,
    ) -> None:
        self._host = host
        self._port = port

        self._mcp = FastMCP(name=name)
        self._task: asyncio.Task | None = None

        tools = self.build_tools()
        self._register_tools(tools)

    def build_tools(self) -> list[ToolDefinition]:
        """Return the list of tools to expose. Override in subclasses."""
        return []

    @property
    def port(self) -> int:
        return self._port

    def mcp_path(self) -> str:
        """URL path where FastMCP exposes the MCP endpoint."""
        return "/mcp"

    async def start(self) -> None:
        """Start the HTTP MCP server in a background task."""
        if self._task is not None:
            return

        async def _run():
            await self._mcp.run_async(transport="http", host=self._host, port=self._port)

        self._task = asyncio.create_task(_run())
        # Small delay to let the server bind before the agent connects.
        await asyncio.sleep(0.2)

    async def close(self) -> None:
        """Stop the HTTP MCP server."""
        if self._task is None:
            return

        self._task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._task
        self._task = None

    def _register_tools(self, tools: list[ToolDefinition]) -> None:
        """Register ToolDefinitions with the FastMCP server."""
        for tool in tools:
            if tool.input_model is None:
                raise ValueError(
                    f"Tool '{tool.name}' must define input_model (Pydantic BaseModel). "
                    "Raw input_schema dicts are no longer supported."
                )

            model_cls = tool.input_model
            handler = tool.handler

            # Generate a wrapper with the model as the type annotation so
            # FastMCP inspects the signature and builds the schema from it.
            src = """
async def _wrapper(input: _Model) -> Any:
    _params = {k: v for k, v in input.model_dump().items() if v is not None}
    _summary = ", ".join(f"{k}={v!r}" for k, v in list(_params.items())[:3])
    _logger.info(f"CallToolRequest: {_tool_name}({_summary})")
    result = _handler(input)
    if _isawaitable(result):
        return await result
    return result
""".lstrip()

            ns: dict[str, Any] = {
                "Any": Any,
                "_Model": model_cls,
                "_handler": handler,
                "_isawaitable": inspect.isawaitable,
                "_logger": logger,
                "_tool_name": tool.name,
            }
            exec(src, ns, ns)
            self._mcp.tool(name=tool.name, description=tool.description)(ns["_wrapper"])

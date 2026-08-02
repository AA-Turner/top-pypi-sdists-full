"""Adapter-agnostic boundary for MCP server adapters."""

from typing import Any, Protocol, runtime_checkable

from mistralai.vibe.sdk.capabilities.mcp.types import McpToolDescriptor

__all__ = [
    "McpPort",
]


@runtime_checkable
class McpPort(Protocol):
    """Lifecycle and tool surface a cached MCP server adapter must expose."""

    @property
    def server_key(self) -> str: ...

    async def setup(self) -> None: ...

    async def list_tools(self) -> list[McpToolDescriptor]: ...

    async def invoke_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any: ...

    async def teardown(self) -> None: ...

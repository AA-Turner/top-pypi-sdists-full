"""MCP server initialization."""

import contextlib
from typing import Literal

from pydantic import BaseModel, Field

from mistralai.vibe.sdk.capabilities.mcp.config import McpConfigBase
from mistralai.vibe.sdk.capabilities.mcp.types import McpToolDescriptor

__all__ = [
    "MCP_INITIALIZATION_TYPE",
    "discover_mcp_tools",
]

MCP_INITIALIZATION_TYPE = "mcp_initialization"


class McpInitOk(BaseModel):
    status: Literal["ok"] = "ok"
    tools: list[McpToolDescriptor] = Field(default_factory=list)


class McpInitError(BaseModel):
    status: Literal["error"]
    error_type: str
    error: str


class McpInitializationContent(BaseModel):
    mcp_name: str
    mcp_type: str
    mcp_server_key: str
    detail: McpInitOk | McpInitError = Field(discriminator="status")


async def discover_mcp_tools(config: McpConfigBase) -> list[McpToolDescriptor]:
    """Open an MCP client, list the server's tools, then tear it down."""
    adapter = config.create_adapter()
    try:
        await adapter.setup()
        return await adapter.list_tools()
    finally:
        with contextlib.suppress(Exception):
            await adapter.teardown()

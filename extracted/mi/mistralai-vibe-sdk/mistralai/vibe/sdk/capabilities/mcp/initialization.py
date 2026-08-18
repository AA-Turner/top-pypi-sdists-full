"""MCP server initialization."""

from typing import Literal

from pydantic import BaseModel, Field

from mistralai.vibe.sdk.agent.execution.resources.context import current_execution_scope
from mistralai.vibe.sdk.capabilities.mcp.config import McpConfigBase
from mistralai.vibe.sdk.capabilities.mcp.resource import McpResourceDefinition
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
    """List the server's tools on the scope's shared MCP connection."""
    adapter = await current_execution_scope().get(McpResourceDefinition(config))

    return await adapter.list_tools()

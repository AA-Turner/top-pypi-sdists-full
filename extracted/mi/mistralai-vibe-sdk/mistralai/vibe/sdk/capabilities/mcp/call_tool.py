"""Builtin tool that invokes a tool on an MCP server."""

from collections.abc import Iterable, Mapping
from typing import Any

from pydantic import BaseModel, ConfigDict, SerializeAsAny

from mistralai.vibe.sdk.agent.execution.resources.context import current_execution_scope
from mistralai.vibe.sdk.capabilities.adapters.local_function import ToolTaskConfig
from mistralai.vibe.sdk.capabilities.authoring import tool
from mistralai.vibe.sdk.capabilities.mcp.config import McpConfigBase
from mistralai.vibe.sdk.capabilities.mcp.initialization import (
    MCP_INITIALIZATION_TYPE,
    McpInitializationContent,
    McpInitOk,
)
from mistralai.vibe.sdk.capabilities.mcp.resource import McpResourceDefinition
from mistralai.vibe.sdk.execution_record.state import HistoryEntry, StateEntry

__all__ = [
    "McpCallToolContext",
    "McpToolArgs",
    "mcp_call_tool",
    "mcp_tool_configs_from_history",
]


class McpCallToolContext(BaseModel):
    """Serializable context binding the call to one MCP server tool."""

    mcp_config: SerializeAsAny[McpConfigBase]
    tool_name: str


class McpToolArgs(BaseModel):
    """Placeholder args model — a remote MCP tool's arguments are arbitrary JSON."""

    model_config = ConfigDict(extra="allow")


@tool(
    name="mcp_call",
    description="Invoke a tool on an MCP server.",
    input_schema=McpToolArgs,
    ctx_schema=McpCallToolContext,
)
async def mcp_call_tool(ctx: McpCallToolContext, args: McpToolArgs) -> Any:
    """Invoke the initialized tool name on the scope's shared MCP connection."""
    adapter = await current_execution_scope().get(McpResourceDefinition(ctx.mcp_config))

    return await adapter.invoke_tool(ctx.tool_name, args.model_dump())


def mcp_tool_configs_from_history(
    history: Iterable[HistoryEntry],
    mcp_configs: Mapping[str, McpConfigBase],
) -> dict[str, ToolTaskConfig]:
    """Derive MCP tool configs from ``mcp_initialization`` entries."""
    configs: dict[str, ToolTaskConfig] = {}

    for entry in history:
        if not isinstance(entry, StateEntry) or entry.payload.type != MCP_INITIALIZATION_TYPE:
            continue

        content = McpInitializationContent.model_validate(entry.payload.content)
        if not isinstance(content.detail, McpInitOk):
            continue

        mcp_config = mcp_configs.get(content.mcp_name)
        if mcp_config is None:
            continue

        # Skip stale entries
        if content.mcp_server_key != mcp_config.server_key:
            continue

        for tool_descriptor in content.detail.tools:
            visible_name = f"{content.mcp_name}__{tool_descriptor.name}"
            ctx = McpCallToolContext.model_validate(
                {"mcp_config": mcp_config, "tool_name": tool_descriptor.name}
            ).model_dump(mode="json")
            configs[visible_name] = ToolTaskConfig(
                fn_path=mcp_call_tool.fn_path,
                name=visible_name,
                description=tool_descriptor.description or "",
                input_schema=tool_descriptor.input_schema or {},
                ctx=ctx,
            )

    return configs

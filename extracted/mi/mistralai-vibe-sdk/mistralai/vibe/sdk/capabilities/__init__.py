"""Canonical namespace for Vibe SDK capability authoring.

Capabilities are invokable runtime integrations used by agents, such as local
tools, client-resolved callbacks, MCP tools, sandboxed code execution, and
task-backed work.

This package re-exports only the public authoring/registry API. Builtins and
code-task internals stay under their explicit subpackages.
"""

from mistralai.vibe.sdk.capabilities.authoring import (
    ClientToolDefinition,
    ToolDefinition,
    client_tool,
    client_tool_error,
    client_tool_result,
    tool,
)
from mistralai.vibe.sdk.capabilities.registry import ClientToolRegistry
from mistralai.vibe.sdk.capabilities.types import ToolHandler, ToolHandlerContext, ToolResult

__all__ = [
    "ClientToolRegistry",
    "ClientToolDefinition",
    "ToolDefinition",
    "ToolHandler",
    "ToolHandlerContext",
    "ToolResult",
    "client_tool",
    "client_tool_error",
    "client_tool_result",
    "tool",
]

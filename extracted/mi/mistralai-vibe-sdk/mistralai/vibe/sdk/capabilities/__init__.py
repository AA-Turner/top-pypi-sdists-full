"""Canonical namespace for Vibe SDK capability authoring.

Capabilities are invokable runtime integrations used by agents, such as local
tools, client-resolved callbacks, MCP tools, sandboxed code execution, and
task-backed work.

This package re-exports only the public authoring/registry API. Builtins and
code-task internals stay under their explicit subpackages.
"""

from importlib import import_module
from typing import TYPE_CHECKING, Any

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

if TYPE_CHECKING:
    from mistralai.vibe.sdk.capabilities.authoring import (
        ClientToolDefinition,
        ToolDefinition,
        client_tool,
        client_tool_error,
        client_tool_result,
        tool,
    )
    from mistralai.vibe.sdk.capabilities.registry import ClientToolRegistry
    from mistralai.vibe.sdk.capabilities.types import (
        ToolHandler,
        ToolHandlerContext,
        ToolResult,
    )

_LAZY_EXPORTS = {
    "ClientToolDefinition": "mistralai.vibe.sdk.capabilities.authoring",
    "ToolDefinition": "mistralai.vibe.sdk.capabilities.authoring",
    "client_tool": "mistralai.vibe.sdk.capabilities.authoring",
    "client_tool_error": "mistralai.vibe.sdk.capabilities.authoring",
    "client_tool_result": "mistralai.vibe.sdk.capabilities.authoring",
    "tool": "mistralai.vibe.sdk.capabilities.authoring",
    "ClientToolRegistry": "mistralai.vibe.sdk.capabilities.registry",
    "ToolHandler": "mistralai.vibe.sdk.capabilities.types",
    "ToolHandlerContext": "mistralai.vibe.sdk.capabilities.types",
    "ToolResult": "mistralai.vibe.sdk.capabilities.types",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value

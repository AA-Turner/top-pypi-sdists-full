"""matrx_ai.tools — Unified tool execution system.

Public API:
    ToolExecutor              — The single entry point for all tool executions
    ToolRegistry            — Singleton registry (DB + code resolution)
    ToolDefinition            — Pydantic model describing a tool
    ToolContext               — Everything a tool needs about its execution environment
    ToolResult                — Structured result from any tool execution
    ToolError                 — Rich error with traceback + suggested action
    ToolType                  — LOCAL | EXTERNAL_MCP | AGENT | EXTERNAL_HANDLER
    CxToolCallRecord          — Pydantic model for the cx_tool_call DB row
    GuardrailEngine           — Centralized safety checks
    ToolStreamManager         — Streaming updates during tool execution
    ToolLifecycleManager      — Resource cleanup
    ToolExecutionLogger       — DB logging (two-phase: INSERT on start, UPDATE on finish)

External tool integration (for apps consuming the ai package):
    ExternalToolAdapter       — Base class: subclass, decorate with @external_tool, call register()
    external_tool             — Decorator: marks a method as the handler for a named tool
    ExternalHandlerRegistry   — Underlying singleton registry (advanced use / testing)
    ExternalToolHandler       — Type alias for the handler callable signature
    register_external_tool_handler  — Register a standalone function for one tool
    register_external_app_handler   — Register a catch-all for all tools from a source_kind
"""

from ._db_log import TRACE_TAGS_CONTEXT_KEY
from .agent_tool import execute_agent_tool, register_agent_as_tool
from .db_hints import (
    DbErrorFacts,
    build_hint,
    parse_db_error,
    strip_ansi,
)
from .executor import ToolExecutor
from .external_handlers import (
    ExternalHandlerRegistry,
    ExternalToolAdapter,
    ExternalToolHandler,
    external_tool,
    register_external_app_handler,
    register_external_tool_handler,
)
from .external_mcp import ExternalMCPClient
from .guardrails import GuardrailEngine
from .lifecycle import ToolLifecycleManager
from .logger import ToolExecutionLogger
from .merge import ToolMergeError, merge_request_tools
from .models import (
    CustomTool,
    CustomToolInputSchema,
    CxToolCallRecord,
    CxToolCallStatus,
    GuardrailResult,
    ToolContext,
    ToolDefinition,
    ToolError,
    ToolResult,
    ToolType,
)
from .registry import ToolRegistry
from .specs import (
    AgentToolSpec,
    InlineToolSpec,
    RegisteredToolSpec,
    ToolSpec,
    spec_display_name,
    spec_identity,
)
from .streaming import ToolStreamEvent, ToolStreamManager

__all__ = [
    # Ambient labels a scope stamps onto every chat.tool_trace row it produces
    # (AppContext.metadata[TRACE_TAGS_CONTEXT_KEY] = {...}).
    "TRACE_TAGS_CONTEXT_KEY",
    "ToolExecutor",
    "ToolRegistry",
    "ToolDefinition",
    "ToolContext",
    "ToolResult",
    "ToolError",
    "ToolType",
    "CustomTool",
    "CustomToolInputSchema",
    "CxToolCallRecord",
    "CxToolCallStatus",
    "GuardrailResult",
    "GuardrailEngine",
    "ToolStreamEvent",
    "ToolStreamManager",
    "ToolExecutionLogger",
    "ToolLifecycleManager",
    "ExternalMCPClient",
    "ExternalHandlerRegistry",
    "ExternalToolAdapter",
    "ExternalToolHandler",
    "external_tool",
    "register_external_tool_handler",
    "register_external_app_handler",
    "execute_agent_tool",
    "register_agent_as_tool",
    # Unified tool-spec API (phase A1 of TOOL_INJECTION_REFACTOR.md)
    "ToolSpec",
    "RegisteredToolSpec",
    "InlineToolSpec",
    "AgentToolSpec",
    "spec_identity",
    "spec_display_name",
    "merge_request_tools",
    "ToolMergeError",
    # Agent-facing DB error hints (shared by any tool with a table/column vocabulary)
    "DbErrorFacts",
    "build_hint",
    "parse_db_error",
    "strip_ansi",
]

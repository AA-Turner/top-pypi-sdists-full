"""
cortex_code_agent_sdk - Python SDK for the Cortex Code CLI.

Provides a Python interface for the Cortex Code Agent SDK that wraps the
Cortex Code CLI with --input-format stream-json --output-format stream-json.

Usage:
    import asyncio
    from cortex_code_agent_sdk import query, CortexCodeAgentOptions, AssistantMessage, ResultMessage

    async def main():
        async for message in query(
            prompt="Say hello",
            options=CortexCodeAgentOptions(connection="snowhouse-pat"),
        ):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        print(block.text)
            elif isinstance(message, ResultMessage):
                print(f"Done: {message.subtype}")

    asyncio.run(main())
"""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from mcp.types import ToolAnnotations

from ._errors import (
    CLIConnectionError,
    CLIJSONDecodeError,
    CLINotFoundError,
    CortexCodeSDKError,
    InvalidOptionValueError,
    ProcessError,
)
from ._internal.transport import Transport
from .client import CortexCodeSDKClient
from .fork_session import fork_session
from .query import query
from .types import (
    AgentApiOptions,
    AgentApiTokenProvider,
    AgentApiVStage,
    AgentDefinition,
    AssistantMessage,
    BaseHookInput,
    CanUseTool,
    ContentBlock,
    CortexCodeAgentOptions,
    HookCallback,
    HookContext,
    HookInput,
    HookJSONOutput,
    HookMatcher,
    InitSystemMessage,
    McpHttpServerConfig,
    McpSdkServerConfig,
    McpServerConfig,
    McpServerConnectionStatus,
    McpServerInfo,
    McpServerStatus,
    McpServerStatusConfig,
    McpSetServersConfig,
    McpSetServersResult,
    McpSnowflakeServerConfig,
    McpSSEServerConfig,
    McpStatusResponse,
    McpStdioServerConfig,
    McpToolAnnotations,
    McpToolInfo,
    Message,
    NotificationHookInput,
    NotificationHookSpecificOutput,
    PermissionMode,
    PermissionRequestHookInput,
    PermissionRequestHookSpecificOutput,
    PermissionResult,
    PermissionResultAllow,
    PermissionResultDeny,
    PermissionRuleValue,
    PermissionUpdate,
    PostToolUseFailureHookInput,
    PostToolUseFailureHookSpecificOutput,
    PostToolUseHookInput,
    PreCompactHookInput,
    PreToolUseHookInput,
    ResultMessage,
    SDKPermissionDenial,
    SdkPluginConfig,
    SessionMode,
    SettingSource,
    SnowflakeSandboxOptions,
    StopHookInput,
    StreamEvent,
    SubagentStartHookInput,
    SubagentStartHookSpecificOutput,
    SubagentStopHookInput,
    SystemMessage,
    SystemTextMessage,
    TaskNotificationMessage,
    TaskNotificationStatus,
    TaskProgressMessage,
    TaskStartedMessage,
    TaskUsage,
    TextBlock,
    ThinkingBlock,
    ToolPermissionContext,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
    UserPromptSubmitHookInput,
)

# ---------------------------------------------------------------------------
# MCP Server Support
# ---------------------------------------------------------------------------

T = TypeVar("T")


@dataclass
class SdkMcpTool(Generic[T]):
    """Definition for an SDK MCP tool."""

    name: str
    description: str
    input_schema: type[T] | dict[str, Any]
    handler: Callable[[T], Awaitable[dict[str, Any]]]
    annotations: "ToolAnnotations | None" = None


def tool(
    name: str,
    description: str,
    input_schema: type | dict[str, Any],
    annotations: "ToolAnnotations | None" = None,
) -> Callable[[Callable[[Any], Awaitable[dict[str, Any]]]], "SdkMcpTool[Any]"]:
    """Decorator for defining MCP tools with type safety.

    Creates a tool that can be used with SDK MCP servers. The tool runs
    in-process within your Python application, providing better performance
    than external MCP servers.

    Args:
        name: Unique identifier for the tool.
        description: Human-readable description of what the tool does.
        input_schema: Schema defining the tool's input parameters. Can be
            a dict mapping parameter names to types (e.g., {"text": str}),
            a TypedDict class, or a full JSON Schema dictionary.
        annotations: Optional tool annotations (requires ``mcp`` package).

    Returns:
        A decorator that wraps the handler and returns an ``SdkMcpTool``.

    Example::

        @tool("greet", "Greet a user", {"name": str})
        async def greet(args):
            return {"content": [{"type": "text", "text": f"Hello, {args['name']}!"}]}
    """

    def decorator(
        handler: Callable[[Any], Awaitable[dict[str, Any]]],
    ) -> "SdkMcpTool[Any]":
        return SdkMcpTool(
            name=name,
            description=description,
            input_schema=input_schema,
            handler=handler,
            annotations=annotations,
        )

    return decorator


def _convert_input_schema(input_schema: Any) -> dict[str, Any]:
    """Normalize a tool's ``input_schema`` to a JSON-serializable JSON Schema.

    Accepts either a full JSON Schema dict, a shorthand ``{"name": str}`` dict
    of Python types, or a non-dict value. Python ``type`` objects cannot be
    JSON-serialized, so the shorthand form must be expanded before sending
    to the CLI's initialize request or any wire payload.
    """
    if isinstance(input_schema, dict):
        if "type" in input_schema and "properties" in input_schema:
            return input_schema
        properties: dict[str, Any] = {}
        for param_name, param_type in input_schema.items():
            if param_type is str:
                properties[param_name] = {"type": "string"}
            elif param_type is int:
                properties[param_name] = {"type": "integer"}
            elif param_type is float:
                properties[param_name] = {"type": "number"}
            elif param_type is bool:
                properties[param_name] = {"type": "boolean"}
            else:
                properties[param_name] = {"type": "string"}
        return {
            "type": "object",
            "properties": properties,
            "required": list(properties.keys()),
        }
    return {"type": "object", "properties": {}}


def create_sdk_mcp_server(
    name: str,
    version: str = "1.0.0",
    tools: "list[SdkMcpTool[Any]] | None" = None,
) -> "McpSdkServerConfig":
    """Create an in-process MCP server that runs within your Python application.

    Unlike external MCP servers that run as separate processes, SDK MCP
    servers run directly in your application's process. This provides
    better performance, simpler deployment, and direct access to your
    application's state.

    Requires the ``mcp`` package to be installed.

    Args:
        name: Unique identifier for the server.
        version: Server version string. Defaults to ``"1.0.0"``.
        tools: List of ``SdkMcpTool`` instances created with ``@tool``.

    Returns:
        ``McpSdkServerConfig`` that can be passed to
        ``CortexCodeAgentOptions.mcp_servers``.

    Example::

        @tool("add", "Add numbers", {"a": float, "b": float})
        async def add(args):
            return {"content": [{"type": "text", "text": f"Sum: {args['a'] + args['b']}"}]}

        calculator = create_sdk_mcp_server("calculator", tools=[add])
        options = CortexCodeAgentOptions(mcp_servers={"calc": calculator})
    """
    from mcp.server import Server
    from mcp.types import ImageContent, TextContent, Tool

    server = Server(name, version=version)

    if tools:
        tool_map = {tool_def.name: tool_def for tool_def in tools}

        @server.list_tools()  # type: ignore[no-untyped-call,untyped-decorator]
        async def list_tools() -> list[Tool]:
            tool_list = []
            for tool_def in tools:
                tool_list.append(
                    Tool(
                        name=tool_def.name,
                        description=tool_def.description,
                        inputSchema=_convert_input_schema(tool_def.input_schema),
                        annotations=tool_def.annotations,
                    )
                )
            return tool_list

        @server.call_tool()  # type: ignore[untyped-decorator]
        async def call_tool(name: str, arguments: dict[str, Any]) -> Any:
            if name not in tool_map:
                raise ValueError(f"Tool '{name}' not found")

            tool_def = tool_map[name]
            result = await tool_def.handler(arguments)

            content: list[TextContent | ImageContent] = []
            if "content" in result:
                for item in result["content"]:
                    if item.get("type") == "text":
                        content.append(TextContent(type="text", text=item["text"]))
                    if item.get("type") == "image":
                        content.append(
                            ImageContent(
                                type="image",
                                data=item["data"],
                                mimeType=item["mimeType"],
                            )
                        )
            return content

    server._sdk_tool_definitions = tools or []  # type: ignore[attr-defined]
    return McpSdkServerConfig(type="sdk", name=name, instance=server)

__all__ = [
    # Main exports
    "query",
    "fork_session",
    # Transport
    "Transport",
    "CortexCodeSDKClient",
    # Types
    "PermissionMode",
    "McpStdioServerConfig",
    "McpHttpServerConfig",
    "McpSSEServerConfig",
    "McpServerConfig",
    "McpSetServersConfig",
    "McpSetServersResult",
    "McpSnowflakeServerConfig",
    "McpSdkServerConfig",
    "McpServerStatus",
    "McpServerStatusConfig",
    "McpServerConnectionStatus",
    "McpServerInfo",
    "McpStatusResponse",
    "McpToolAnnotations",
    "McpToolInfo",
    "UserMessage",
    "AssistantMessage",
    "InitSystemMessage",
    "SystemMessage",
    "SystemTextMessage",
    "TaskStartedMessage",
    "TaskProgressMessage",
    "TaskNotificationMessage",
    "TaskNotificationStatus",
    "TaskUsage",
    "ResultMessage",
    "StreamEvent",
    "Message",
    "CortexCodeAgentOptions",
    "AgentApiOptions",
    "AgentApiTokenProvider",
    "AgentApiVStage",
    "SessionMode",
    "TextBlock",
    "ThinkingBlock",
    "ToolUseBlock",
    "ToolResultBlock",
    "ContentBlock",
    # Tool callbacks
    "CanUseTool",
    "ToolPermissionContext",
    "PermissionResult",
    "PermissionResultAllow",
    "PermissionResultDeny",
    "PermissionRuleValue",
    "PermissionUpdate",
    "SDKPermissionDenial",
    # Hook support
    "HookCallback",
    "HookContext",
    "HookInput",
    "BaseHookInput",
    "PreToolUseHookInput",
    "PostToolUseHookInput",
    "PostToolUseFailureHookInput",
    "PostToolUseFailureHookSpecificOutput",
    "UserPromptSubmitHookInput",
    "StopHookInput",
    "SubagentStopHookInput",
    "PreCompactHookInput",
    "NotificationHookInput",
    "SubagentStartHookInput",
    "PermissionRequestHookInput",
    "NotificationHookSpecificOutput",
    "SubagentStartHookSpecificOutput",
    "PermissionRequestHookSpecificOutput",
    "HookJSONOutput",
    "HookMatcher",
    # Agent support
    "AgentDefinition",
    "SettingSource",
    # Sandbox support
    "SnowflakeSandboxOptions",
    # Plugin support
    "SdkPluginConfig",
    # MCP Server Support
    "create_sdk_mcp_server",
    "tool",
    "SdkMcpTool",
    "ToolAnnotations",
    # Errors
    "CortexCodeSDKError",
    "CLIConnectionError",
    "CLINotFoundError",
    "ProcessError",
    "CLIJSONDecodeError",
    "InvalidOptionValueError",
]

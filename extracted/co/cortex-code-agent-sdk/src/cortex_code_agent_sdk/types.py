"""Type definitions for Cortex Code SDK."""

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Protocol, TypedDict, cast

from typing_extensions import NotRequired

if TYPE_CHECKING:
    from mcp.server import Server as McpServer
else:
    # Runtime placeholder for forward reference resolution in Pydantic 2.12+
    McpServer = Any

# Permission modes
PermissionMode = Literal["default", "autoAcceptPlans", "plan", "bypassPermissions"]


# Agent definitions
SettingSource = Literal["user", "project", "local"]


class SystemPromptPreset(TypedDict):
    """System prompt preset configuration."""

    type: Literal["preset"]
    append: NotRequired[str]


class ToolsPreset(TypedDict):
    """Tools preset configuration."""

    type: Literal["preset"]


@dataclass
class AgentDefinition:
    """Agent definition configuration."""

    description: str
    prompt: str
    tools: list[str] | None = None
    model: Literal["sonnet", "opus", "haiku", "inherit"] | None = None


# Permission Update types (matching TypeScript SDK)
PermissionUpdateDestination = Literal[
    "userSettings", "projectSettings", "localSettings", "session", "cliArg"
]

PermissionBehavior = Literal["allow", "deny", "ask"]


@dataclass
class PermissionRuleValue:
    """Permission rule value."""

    tool_name: str
    rule_content: str | None = None


@dataclass
class PermissionUpdate:
    """Permission update configuration."""

    type: Literal[
        "addRules",
        "replaceRules",
        "removeRules",
        "setMode",
        "addDirectories",
        "removeDirectories",
    ]
    rules: list[PermissionRuleValue] | None = None
    behavior: PermissionBehavior | None = None
    mode: PermissionMode | None = None
    directories: list[str] | None = None
    destination: PermissionUpdateDestination | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert PermissionUpdate to dictionary format matching TypeScript control protocol."""
        result: dict[str, Any] = {
            "type": self.type,
        }

        # Add destination for all variants
        if self.destination is not None:
            result["destination"] = self.destination

        # Handle different type variants
        if self.type in ["addRules", "replaceRules", "removeRules"]:
            # Rules-based variants require rules and behavior
            if self.rules is not None:
                result["rules"] = [
                    {
                        "toolName": rule.tool_name,
                        "ruleContent": rule.rule_content,
                    }
                    for rule in self.rules
                ]
            if self.behavior is not None:
                result["behavior"] = self.behavior

        elif self.type == "setMode":
            # Mode variant requires mode
            if self.mode is not None:
                result["mode"] = self.mode

        elif self.type in ["addDirectories", "removeDirectories"]:
            # Directory variants require directories
            if self.directories is not None:
                result["directories"] = self.directories

        return result

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "PermissionUpdate":
        """Build a PermissionUpdate from a wire-format dictionary."""
        rules_value = value.get("rules")
        rules = None
        if isinstance(rules_value, list):
            rules = [
                PermissionRuleValue(
                    tool_name=str(rule.get("toolName", "")),
                    rule_content=(
                        str(rule["ruleContent"])
                        if isinstance(rule, dict)
                        and rule.get("ruleContent") is not None
                        else None
                    ),
                )
                for rule in rules_value
                if isinstance(rule, dict)
            ]

        directories_value = value.get("directories")
        directories = None
        if isinstance(directories_value, list):
            directories = [str(directory) for directory in directories_value]

        return cls(
            type=cast(
                Literal[
                    "addRules",
                    "replaceRules",
                    "removeRules",
                    "setMode",
                    "addDirectories",
                    "removeDirectories",
                ],
                value["type"],
            ),
            rules=rules,
            behavior=value.get("behavior"),
            mode=value.get("mode"),
            directories=directories,
            destination=value.get("destination"),
        )


# Tool callback types
@dataclass
class ToolPermissionContext:
    """Context information for tool permission callbacks."""

    signal: Any | None = None  # Future: abort signal support
    suggestions: list[PermissionUpdate] = field(
        default_factory=list
    )  # Permission suggestions from CLI
    blocked_path: str | None = None
    decision_reason: str | None = None
    tool_use_id: str = ""
    agent_id: str | None = None


# Match TypeScript's PermissionResult structure
@dataclass
class PermissionResultAllow:
    """Allow permission result."""

    behavior: Literal["allow"] = "allow"
    updated_input: dict[str, Any] | None = None
    updated_permissions: list[PermissionUpdate] | None = None
    tool_use_id: str | None = None


@dataclass
class PermissionResultDeny:
    """Deny permission result."""

    behavior: Literal["deny"] = "deny"
    message: str = ""
    interrupt: bool = False
    tool_use_id: str | None = None


PermissionResult = PermissionResultAllow | PermissionResultDeny

CanUseTool = Callable[
    [str, dict[str, Any], ToolPermissionContext], Awaitable[PermissionResult]
]


##### Hook types
HookEvent = (
    Literal["PreToolUse"]
    | Literal["PostToolUse"]
    | Literal["PostToolUseFailure"]
    | Literal["UserPromptSubmit"]
    | Literal["Stop"]
    | Literal["SubagentStop"]
    | Literal["PreCompact"]
    | Literal["Notification"]
    | Literal["SubagentStart"]
    | Literal["PermissionRequest"]
)


# Hook input types - strongly typed for each hook event
class BaseHookInput(TypedDict):
    """Base hook input fields present across many hook events."""

    session_id: str
    transcript_path: str
    cwd: str
    permission_mode: NotRequired[str]


# agent_id/agent_type are present on BaseHookInput in the CLI's schema but are
# declared per-hook here because SubagentStartHookInput/SubagentStopHookInput
# need them as *required*, and PEP 655 forbids narrowing NotRequired->Required
# in a TypedDict subclass. The four tool-lifecycle types below are the only
# ones the CLI actually populates (the other BaseHookInput consumers don't
# have a toolUseContext in scope at their build site).
class _SubagentContextMixin(TypedDict, total=False):
    """Optional sub-agent attribution fields for tool-lifecycle hooks.

    agent_id: Sub-agent identifier. Present only when the hook fires from
    inside a Task-spawned sub-agent; absent on the main thread. Matches the
    agent_id emitted by that sub-agent's SubagentStart/SubagentStop hooks.
    When multiple sub-agents run in parallel their tool-lifecycle hooks
    interleave over the same control channel — this is the only reliable
    way to attribute each one to the correct sub-agent.

    agent_type: Agent type name (e.g. "general-purpose", "code-reviewer").
    Present inside a sub-agent (alongside agent_id), or on the main thread
    of a session started with --agent (without agent_id).
    """

    agent_id: str
    agent_type: str


class PreToolUseHookInput(BaseHookInput, _SubagentContextMixin):
    """Input data for PreToolUse hook events."""

    hook_event_name: Literal["PreToolUse"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_use_id: str


class PostToolUseHookInput(BaseHookInput, _SubagentContextMixin):
    """Input data for PostToolUse hook events."""

    hook_event_name: Literal["PostToolUse"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_response: Any
    tool_use_id: str


class PostToolUseFailureHookInput(BaseHookInput, _SubagentContextMixin):
    """Input data for PostToolUseFailure hook events."""

    hook_event_name: Literal["PostToolUseFailure"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_use_id: str
    error: str
    is_interrupt: NotRequired[bool]


class UserPromptSubmitHookInput(BaseHookInput):
    """Input data for UserPromptSubmit hook events."""

    hook_event_name: Literal["UserPromptSubmit"]
    prompt: str


class StopHookInput(BaseHookInput):
    """Input data for Stop hook events."""

    hook_event_name: Literal["Stop"]
    stop_hook_active: bool


class SubagentStopHookInput(BaseHookInput):
    """Input data for SubagentStop hook events."""

    hook_event_name: Literal["SubagentStop"]
    stop_hook_active: bool
    agent_id: str
    agent_transcript_path: str
    agent_type: str


class PreCompactHookInput(BaseHookInput):
    """Input data for PreCompact hook events."""

    hook_event_name: Literal["PreCompact"]
    trigger: Literal["manual", "auto"]
    custom_instructions: str | None


class NotificationHookInput(BaseHookInput):
    """Input data for Notification hook events."""

    hook_event_name: Literal["Notification"]
    message: str
    title: NotRequired[str]
    notification_type: str


class SubagentStartHookInput(BaseHookInput):
    """Input data for SubagentStart hook events."""

    hook_event_name: Literal["SubagentStart"]
    agent_id: str
    agent_type: str


class PermissionRequestHookInput(BaseHookInput, _SubagentContextMixin):
    """Input data for PermissionRequest hook events."""

    hook_event_name: Literal["PermissionRequest"]
    tool_name: str
    tool_input: dict[str, Any]
    permission_suggestions: NotRequired[list[Any]]


# Union type for all hook inputs
HookInput = (
    PreToolUseHookInput
    | PostToolUseHookInput
    | PostToolUseFailureHookInput
    | UserPromptSubmitHookInput
    | StopHookInput
    | SubagentStopHookInput
    | PreCompactHookInput
    | NotificationHookInput
    | SubagentStartHookInput
    | PermissionRequestHookInput
)


# Hook-specific output types
class PreToolUseHookSpecificOutput(TypedDict):
    """Hook-specific output for PreToolUse events."""

    hookEventName: Literal["PreToolUse"]
    permissionDecision: NotRequired[Literal["allow", "deny", "ask"]]
    permissionDecisionReason: NotRequired[str]
    updatedInput: NotRequired[dict[str, Any]]
    additionalContext: NotRequired[str]


class PostToolUseHookSpecificOutput(TypedDict):
    """Hook-specific output for PostToolUse events."""

    hookEventName: Literal["PostToolUse"]
    additionalContext: NotRequired[str]
    updatedMCPToolOutput: NotRequired[Any]


class PostToolUseFailureHookSpecificOutput(TypedDict):
    """Hook-specific output for PostToolUseFailure events."""

    hookEventName: Literal["PostToolUseFailure"]
    additionalContext: NotRequired[str]


class UserPromptSubmitHookSpecificOutput(TypedDict):
    """Hook-specific output for UserPromptSubmit events."""

    hookEventName: Literal["UserPromptSubmit"]
    additionalContext: NotRequired[str]


class SessionStartHookSpecificOutput(TypedDict):
    """Hook-specific output for SessionStart events."""

    hookEventName: Literal["SessionStart"]
    additionalContext: NotRequired[str]


class NotificationHookSpecificOutput(TypedDict):
    """Hook-specific output for Notification events."""

    hookEventName: Literal["Notification"]
    additionalContext: NotRequired[str]


class SubagentStartHookSpecificOutput(TypedDict):
    """Hook-specific output for SubagentStart events."""

    hookEventName: Literal["SubagentStart"]
    additionalContext: NotRequired[str]


class PermissionRequestHookSpecificOutput(TypedDict):
    """Hook-specific output for PermissionRequest events."""

    hookEventName: Literal["PermissionRequest"]
    decision: dict[str, Any]


HookSpecificOutput = (
    PreToolUseHookSpecificOutput
    | PostToolUseHookSpecificOutput
    | PostToolUseFailureHookSpecificOutput
    | UserPromptSubmitHookSpecificOutput
    | SessionStartHookSpecificOutput
    | NotificationHookSpecificOutput
    | SubagentStartHookSpecificOutput
    | PermissionRequestHookSpecificOutput
)


# IMPORTANT: The Python SDK uses `async_` and `continue_` (with underscores) to avoid
# Python keyword conflicts. These fields are automatically converted to `async` and
# `continue` when sent to the CLI. You should use the underscore versions in your
# Python code.
class AsyncHookJSONOutput(TypedDict):
    """Async hook output that defers hook execution.

    Fields:
        async_: Set to True to defer hook execution. Note: This is converted to
            "async" when sent to the CLI - use "async_" in your Python code.
        asyncTimeout: Optional timeout in milliseconds for the async operation.
    """

    async_: Literal[
        True
    ]  # Using async_ to avoid Python keyword (converted to "async" for CLI)
    asyncTimeout: NotRequired[int]


class SyncHookJSONOutput(TypedDict):
    """Synchronous hook output with control and decision fields.

    This defines the structure for hook callbacks to control execution and provide
    feedback to the agent.

    Common Control Fields:
        continue_: Whether the agent should proceed after hook execution (default: True).
            Note: This is converted to "continue" when sent to the CLI.
        suppressOutput: Hide stdout from transcript mode (default: False).
        stopReason: Message shown when continue is False.

    Decision Fields:
        decision: Set to "block" to indicate blocking behavior.
        systemMessage: Warning message displayed to the user.
        reason: Feedback message for the agent about the decision.

    Hook-Specific Output:
        hookSpecificOutput: Event-specific controls (e.g., permissionDecision for
            PreToolUse, additionalContext for PostToolUse).

    Note: The CLI documentation shows field names without underscores ("async", "continue"),
    but Python code should use the underscore versions ("async_", "continue_") as they
    are automatically converted.
    """

    # Common control fields
    continue_: NotRequired[
        bool
    ]  # Using continue_ to avoid Python keyword (converted to "continue" for CLI)
    suppressOutput: NotRequired[bool]
    stopReason: NotRequired[str]

    # Decision fields
    decision: NotRequired[Literal["block"]]
    systemMessage: NotRequired[str]
    reason: NotRequired[str]

    # Hook-specific outputs
    hookSpecificOutput: NotRequired[HookSpecificOutput]


HookJSONOutput = AsyncHookJSONOutput | SyncHookJSONOutput


class HookContext(TypedDict):
    """Context information for hook callbacks.

    Fields:
        signal: Reserved for future abort signal support. Currently always None.
    """

    signal: Any | None  # Future: abort signal support


HookCallback = Callable[
    # HookCallback input parameters:
    # - input: Strongly-typed hook input with discriminated unions based on hook_event_name
    # - tool_use_id: Optional tool use identifier
    # - context: Hook context with abort signal support (currently placeholder)
    [HookInput, str | None, HookContext],
    Awaitable[HookJSONOutput],
]


# Hook matcher configuration
@dataclass
class HookMatcher:
    """Hook matcher configuration."""

    # For PreToolUse, the matcher can be a tool name like "Bash" or a
    # combination of tool names like "Write|MultiEdit|Edit".
    matcher: str | None = None

    # A list of Python functions with function signature HookCallback
    hooks: list[HookCallback] = field(default_factory=list)

    # Timeout in seconds for all hooks in this matcher (default: 60)
    timeout: float | None = None


# MCP Server config
class McpStdioServerConfig(TypedDict):
    """MCP stdio server configuration."""

    type: NotRequired[Literal["stdio"]]
    command: str
    args: NotRequired[list[str]]
    env: NotRequired[dict[str, str]]


class McpSSEServerConfig(TypedDict):
    """MCP SSE server configuration."""

    type: Literal["sse"]
    url: str
    headers: NotRequired[dict[str, str]]


class McpHttpServerConfig(TypedDict):
    """MCP HTTP server configuration."""

    type: Literal["http"]
    url: str
    headers: NotRequired[dict[str, str]]


class McpSnowflakeServerConfig(TypedDict):
    """Snowflake-managed MCP server configuration.

    These servers are resolved and executed server-side by Cortex Agent.
    """

    type: Literal["snowflake-external", "snowflake-custom"]
    connection: str
    fqn: str


class McpSdkServerConfig(TypedDict):
    """SDK MCP server configuration."""

    type: Literal["sdk"]
    name: str
    instance: "McpServer"


McpServerConfig = (
    McpStdioServerConfig
    | McpSSEServerConfig
    | McpHttpServerConfig
    | McpSnowflakeServerConfig
    | McpSdkServerConfig
)

McpSetServersConfig = (
    McpStdioServerConfig
    | McpSSEServerConfig
    | McpHttpServerConfig
    | McpSnowflakeServerConfig
)


# MCP Server Status types (returned by get_mcp_status)
# These mirror the TypeScript SDK's McpServerStatus type and use wire-format
# field names (camelCase where applicable) since they come directly from CLI
# JSON output.


class McpSdkServerConfigStatus(TypedDict):
    """SDK MCP server config as returned in status responses.

    Unlike McpSdkServerConfig (which includes the in-process `instance`),
    this output-only type only has serializable fields.
    """

    type: Literal["sdk"]
    name: str


# Broader config type for status responses.
McpServerStatusConfig = (
    McpStdioServerConfig
    | McpSSEServerConfig
    | McpHttpServerConfig
    | McpSnowflakeServerConfig
    | McpSdkServerConfigStatus
)


class McpToolAnnotations(TypedDict, total=False):
    """Tool annotations as returned in MCP server status.

    Wire format uses camelCase field names (from CLI JSON output).
    """

    readOnly: bool
    destructive: bool
    openWorld: bool


class McpToolInfo(TypedDict):
    """Information about a tool provided by an MCP server."""

    name: str
    description: NotRequired[str]
    annotations: NotRequired[McpToolAnnotations]


class McpServerInfo(TypedDict):
    """Server info from MCP initialize handshake (available when connected)."""

    name: str
    version: str


# Connection status values for an MCP server
McpServerConnectionStatus = Literal[
    "connected", "remote", "failed", "needs-auth", "pending", "disabled"
]


class McpServerStatus(TypedDict):
    """Status information for an MCP server connection.

    Returned by `CortexCodeSDKClient.get_mcp_status()` in the `mcpServers` list.
    """

    name: str
    """Server name as configured."""

    status: McpServerConnectionStatus
    """Current connection status.

    For Snowflake-managed MCP servers (``snowflake-external`` /
    ``snowflake-custom``), ``remote`` means the server config is accepted and
    in scope. Final auth/resolution happens server-side when tools are used.
    """

    serverInfo: NotRequired[McpServerInfo]
    """Server information from MCP handshake (available when connected)."""

    error: NotRequired[str]
    """Error message (available when status is 'failed')."""

    config: NotRequired[McpServerStatusConfig]
    """Server configuration (includes URL for HTTP/SSE servers)."""

    scope: NotRequired[str]
    """Configuration scope (e.g., project, user, local, managed)."""

    tools: NotRequired[list[McpToolInfo]]
    """Tools provided by this server (available when connected)."""


class McpStatusResponse(TypedDict):
    """Response from `CortexCodeSDKClient.get_mcp_status()`.

    Wraps the list of server statuses under the `mcpServers` key, matching
    the wire-format response shape.
    """

    mcpServers: list[McpServerStatus]


class McpSetServersResult(TypedDict):
    """Response from `CortexCodeSDKClient.set_mcp_servers()`.

    Lists changes to the SDK session-scoped MCP server bucket.
    """

    added: list[str]
    removed: list[str]
    errors: dict[str, str]


class SdkPluginConfig(TypedDict):
    """SDK plugin configuration.

    Currently only local plugins are supported via the 'local' type.
    """

    type: Literal["local"]
    path: str


# Content block types
@dataclass
class TextBlock:
    """Text content block."""

    text: str


@dataclass
class ThinkingBlock:
    """Thinking content block."""

    thinking: str
    signature: str = ""


@dataclass
class ToolUseBlock:
    """Tool use content block."""

    id: str
    name: str
    input: dict[str, Any]


@dataclass
class ToolResultBlock:
    """Tool result content block."""

    tool_use_id: str
    content: str | list[dict[str, Any]] | None = None
    is_error: bool | None = None


ContentBlock = TextBlock | ThinkingBlock | ToolUseBlock | ToolResultBlock


# Message types
AssistantMessageError = Literal[
    "authentication_failed",
    "billing_error",
    "rate_limit",
    "invalid_request",
    "server_error",
    "unknown",
]


@dataclass
class UserMessage:
    """User message."""

    content: str | list[ContentBlock]
    uuid: str | None = None
    parent_tool_use_id: str | None = None
    tool_use_result: dict[str, Any] | None = None


@dataclass
class AssistantMessage:
    """Assistant message with content blocks."""

    content: list[ContentBlock]
    model: str
    message_id: str | None = None
    parent_tool_use_id: str | None = None
    error: AssistantMessageError | None = None
    usage: dict[str, Any] | None = None


@dataclass
class SystemMessage:
    """System message with metadata."""

    subtype: str
    data: dict[str, Any]


@dataclass
class InitSystemMessage(SystemMessage):
    """System init message with typed initialize-time metadata.

    Subclass of SystemMessage: existing ``isinstance(msg, SystemMessage)`` and
    ``case SystemMessage()`` checks continue to match. The base ``subtype``
    and ``data`` fields remain populated with the raw payload.
    """

    uuid: str
    session_id: str
    cwd: str
    model: str
    tools: list[str]
    mcp_servers: list[dict[str, Any]]
    permission_mode: str
    api_key_source: str | None = None
    agents: list[str] | None = None
    betas: list[str] | None = None
    slash_commands: list[dict[str, Any]] | None = None
    output_style: str | None = None
    skills: list[str] | None = None
    plugins: list[dict[str, Any]] | None = None


@dataclass
class SystemTextMessage(SystemMessage):
    """System message carrying plain-text content.

    Emitted for stream events with ``type="system_message"`` such as hook
    notifications.
    """

    content: str
    session_id: str | None = None


class TaskUsage(TypedDict):
    """Usage statistics reported in task_progress and task_notification messages."""

    total_tokens: int
    tool_uses: int
    duration_ms: int


# Possible status values for a task_notification message.
TaskNotificationStatus = Literal["completed", "failed", "stopped"]


@dataclass
class TaskStartedMessage(SystemMessage):
    """System message emitted when a task starts.

    Subclass of SystemMessage: existing ``isinstance(msg, SystemMessage)`` and
    ``case SystemMessage()`` checks continue to match. The base ``subtype``
    and ``data`` fields remain populated with the raw payload.
    """

    task_id: str
    description: str
    uuid: str
    session_id: str
    tool_use_id: str | None = None
    task_type: str | None = None


@dataclass
class TaskProgressMessage(SystemMessage):
    """System message emitted while a task is in progress.

    Subclass of SystemMessage: existing ``isinstance(msg, SystemMessage)`` and
    ``case SystemMessage()`` checks continue to match. The base ``subtype``
    and ``data`` fields remain populated with the raw payload.
    """

    task_id: str
    description: str
    usage: TaskUsage
    uuid: str
    session_id: str
    tool_use_id: str | None = None
    last_tool_name: str | None = None


@dataclass
class TaskNotificationMessage(SystemMessage):
    """System message emitted when a task completes, fails, or is stopped.

    Subclass of SystemMessage: existing ``isinstance(msg, SystemMessage)`` and
    ``case SystemMessage()`` checks continue to match. The base ``subtype``
    and ``data`` fields remain populated with the raw payload.
    """

    task_id: str
    status: TaskNotificationStatus
    output_file: str
    summary: str
    uuid: str
    session_id: str
    tool_use_id: str | None = None
    usage: TaskUsage | None = None


@dataclass
class ResultMessage:
    """Result message with cost and usage information."""

    subtype: str
    duration_ms: int
    duration_api_ms: int
    is_error: bool
    num_turns: int
    session_id: str
    stop_reason: str | None = None
    total_cost_usd: float | None = None
    usage: dict[str, Any] | None = None
    result: str | None = None
    structured_output: Any = None
    errors: list[str] | None = None
    permission_denials: list["SDKPermissionDenial"] | None = None
    uuid: str | None = None


@dataclass
class StreamEvent:
    """Stream event for partial message updates during streaming."""

    uuid: str
    session_id: str
    event: dict[str, Any]  # Raw stream event payload
    parent_tool_use_id: str | None = None


Message = UserMessage | AssistantMessage | SystemMessage | ResultMessage | StreamEvent


# Literal string tag for the transport backend (e.g. "subprocess")
TransportType = Literal["subprocess"]
SessionMode = Literal["cli", "api"]


@dataclass
class SnowflakeSandboxOptions:
    """Enable server-side sandbox execution."""

    enabled: bool = False


class AgentApiTokenProvider(Protocol):
    """Refresh-capable source for Snowflake session tokens."""

    def get_token(self) -> str: ...

    def refresh_token(self, reason: str | None = None) -> str: ...


@dataclass
class AgentApiOptions:
    """Direct Agent API transport settings, used when ``mode`` is ``"api"``."""

    rest_url: str | None = None
    token_provider: AgentApiTokenProvider | None = None
    # Bare session tokens are intentionally unsupported because agent runs need refresh.
    token: str | None = None
    # Parent message id to continue from when reusing an Agent API thread.
    # When omitted, API mode describes the thread and uses the latest message id.
    parent_message_id: str | None = None
    v_stages: list["AgentApiVStage"] | None = None
    delete_thread_on_close: bool = False


@dataclass
class AgentApiVStage:
    """V-stage mount configuration forwarded as ``experimental.VStages``."""

    stage_name: str
    mount_path: str
    vstage_namespace: str | None = None
    vstage_version: str | None = None
    is_vstage: bool | None = None
    readonly: bool | None = None
    encryption_type: str | None = None


@dataclass
class CortexCodeAgentOptions:
    """Configuration for a Cortex Code agent session."""

    tools: list[str] | ToolsPreset | None = None
    allowed_tools: list[str] = field(default_factory=list)
    system_prompt: str | SystemPromptPreset | None = None
    append_system_prompt: str | None = None
    mcp_servers: dict[str, McpServerConfig] | str | Path = field(default_factory=dict)
    permission_mode: PermissionMode | None = None
    continue_conversation: bool = False
    resume: str | None = None
    max_turns: int | None = None
    disallowed_tools: list[str] = field(default_factory=list)
    model: str | None = None
    permission_prompt_tool_name: str | None = None
    cwd: str | Path | None = None
    cli_path: str | Path | None = None
    add_dirs: list[str | Path] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    extra_args: dict[str, str | None] = field(
        default_factory=dict
    )  # Pass arbitrary CLI flags
    max_buffer_size: int | None = None
    stderr: Callable[[str], None] | None = None

    # Tool permission callback
    can_use_tool: CanUseTool | None = None

    # Hook configurations
    hooks: dict[HookEvent, list[HookMatcher]] | None = None

    user: str | None = None

    # Partial message streaming support
    include_partial_messages: bool = False
    # When true resumed sessions will fork to a new session ID rather than
    # continuing the previous session.
    fork_session: bool = False
    # When resuming, only replay messages up to and including the message with
    # this UUID. Must be used together with `resume`. Useful for branching from
    # a specific point in a conversation.
    resume_session_at: str | None = None
    # Agent definitions for custom agents
    agents: dict[str, AgentDefinition] | None = None
    # Setting sources to load (user, project, local)
    setting_sources: list[SettingSource] | None = None
    # Plugin configurations for custom plugins
    plugins: list[SdkPluginConfig] = field(default_factory=list)
    # Effort level for thinking depth.
    effort: Literal["minimal", "low", "medium", "high", "max"] | None = None
    # Output format for structured outputs (matches Messages API structure)
    # Example: {"type": "json_schema", "schema": {"type": "object", "properties": {...}}}
    output_format: dict[str, Any] | None = None

    # Abort event for cancelling the current turn.
    # When set, sends an interrupt control request (like pressing ESC in the CLI).
    # The session stays alive for further prompts. Python equivalent of
    # AbortController in the TypeScript SDK.
    abort_event: asyncio.Event | None = None

    # Cortex Code-specific fields
    connection: str | None = None
    profile: str | None = None
    # Session ID for the conversation. In API mode this is the Agent API thread ID.
    session_id: str | None = None
    no_mcp: bool = False
    allow_dangerously_skip_permissions: bool = False
    # Select the transport explicitly. Defaults to CLI unless ASYNC_API=true or
    # CORTEX_CODE_AGENT_SDK_ASYNC_API=true is present in the environment.
    mode: SessionMode | None = None
    api: AgentApiOptions | None = None

    # Experimental: opt into the Snowflake CNG-backed server-side sandbox.
    # When ``snowflake_sandbox.enabled`` is True, the SDK appends
    # ``--snowflake-sandbox`` to the spawned CLI and sets
    # ``ENABLE_COCO_CNG_SANDBOX=1`` on the child environment (unless the
    # caller already overrode that key via :attr:`env`).
    snowflake_sandbox: SnowflakeSandboxOptions | None = None


# SDK Control Protocol
class SDKPermissionDenial(TypedDict):
    tool_name: str
    tool_use_id: str
    tool_input: dict[str, Any]


class InterruptControlRequest(TypedDict):
    subtype: Literal["interrupt"]


class CanUseToolControlRequest(TypedDict):
    subtype: Literal["can_use_tool"]
    tool_name: str
    input: dict[str, Any]
    permission_suggestions: list[Any] | None
    blocked_path: str | None
    decision_reason: NotRequired[str]
    tool_use_id: str
    agent_id: NotRequired[str]
    description: NotRequired[str]


class InitializeControlRequest(TypedDict):
    subtype: Literal["initialize"]
    hooks: dict[HookEvent, Any] | None
    agents: NotRequired[dict[str, dict[str, Any]]]
    systemPrompt: NotRequired[str]
    appendSystemPrompt: NotRequired[str]
    settingSources: NotRequired[list[SettingSource]]
    sdkManagedPermissions: NotRequired[bool]
    sdkMcpServers: NotRequired[list[str]]
    sdkMcpToolDefinitions: NotRequired[dict[str, list[dict[str, Any]]]]
    mcpServers: NotRequired[dict[str, Any]]


class SetPermissionModeControlRequest(TypedDict):
    subtype: Literal["set_permission_mode"]
    mode: str


class HookCallbackControlRequest(TypedDict):
    subtype: Literal["hook_callback"]
    callback_id: str
    input: Any
    tool_use_id: str | None


class McpMessageControlRequest(TypedDict):
    subtype: Literal["mcp_message"]
    server_name: str
    message: Any


class McpToolCallControlRequest(TypedDict):
    subtype: Literal["mcp_tool_call"]
    server_name: str
    tool_name: str
    arguments: dict[str, Any]
    tool_use_id: NotRequired[str]


class McpReconnectControlRequest(TypedDict):
    """Reconnects a disconnected or failed MCP server."""

    subtype: Literal["mcp_reconnect"]
    # Note: wire protocol uses camelCase for this field
    serverName: str


class McpAuthenticateControlRequest(TypedDict):
    """Authenticates an OAuth-backed MCP server."""

    subtype: Literal["mcp_authenticate"]
    # Note: wire protocol uses camelCase for this field
    serverName: str


class McpToggleControlRequest(TypedDict):
    """Enables or disables an MCP server."""

    subtype: Literal["mcp_toggle"]
    # Note: wire protocol uses camelCase for this field
    serverName: str
    enabled: bool


class StopTaskControlRequest(TypedDict):
    subtype: Literal["stop_task"]
    task_id: str


class SetModelControlRequest(TypedDict):
    subtype: Literal["set_model"]
    model: str | None


class McpStatusControlRequest(TypedDict):
    subtype: Literal["mcp_status"]


class McpSetServersControlRequest(TypedDict):
    subtype: Literal["mcp_set_servers"]
    servers: dict[str, McpSetServersConfig]


ControlRequestInner = (
    InterruptControlRequest
    | CanUseToolControlRequest
    | InitializeControlRequest
    | SetModelControlRequest
    | SetPermissionModeControlRequest
    | HookCallbackControlRequest
    | McpMessageControlRequest
    | McpToolCallControlRequest
    | McpStatusControlRequest
    | McpSetServersControlRequest
    | McpReconnectControlRequest
    | McpAuthenticateControlRequest
    | McpToggleControlRequest
    | StopTaskControlRequest
)


class ControlRequest(TypedDict):
    type: Literal["control_request"]
    request_id: str
    request: ControlRequestInner


class ControlResponseSuccess(TypedDict):
    subtype: Literal["success"]
    request_id: str
    response: dict[str, Any] | None


class ControlResponseError(TypedDict):
    subtype: Literal["error"]
    request_id: str
    error: str


class ControlResponse(TypedDict):
    type: Literal["control_response"]
    response: ControlResponseSuccess | ControlResponseError

"""Serializable models for the Agent Session API."""

from typing import Annotated, Literal

from pydantic import Field, JsonValue

from mistralai.vibe.sdk.providers.completion.config import (
    CompletionConfig,
    MistralCompletionConfig,
)

from ..base import JsonSchema, ProtocolModel

type SessionId = str
type TurnId = str
type HistoryEntryId = str
type ToolCallId = str
type CallbackId = str
type UnixMs = int
type Uri = str
type AbsolutePath = str

type Procedure = Literal[
    "session/start",
    "session/resume",
    "session/fork",
    "session/rename",
    "session/delete",
    "session/compact",
    "session/shellCommand",
    "turn/start",
    "turn/steer",
    "turn/interrupt",
    "session/read",
    "config/read",
    "config/write",
    "plugin/info",
    "plugin/reload",
    "callback/result",
    "session/close",
]
GenerationStatus = Literal["generating", "complete"]
SessionStatus = Literal["waiting_for_input", "running", "complete", "failed", "interrupted"]
TurnStatus = Literal["running", "blocked", "complete", "failed", "interrupted"]
MessageRole = Literal["system", "user", "assistant"]
ToolKind = Literal["builtin", "mcp", "client", "plugin"]
EffectStatus = Literal[
    "pending", "running", "blocked", "complete", "failed", "cancelled", "skipped"
]
FileChangeStatus = Literal["proposed", "approved", "denied", "applied", "failed"]
NoticeLevel = Literal["info", "warning"]
HookType = Literal[
    "pre_agent_turn",
    "post_agent_turn",
    "pre_llm_call",
    "post_llm_call",
    "pre_mcp_tool_call",
    "post_mcp_tool_call",
    "pre_client_tool_call",
    "post_client_tool_call",
    "pre_tool_call",
    "post_tool_call",
]
PluginComponentKind = Literal[
    "skill",
    "knowledge",
    "library",
    "mcp_server",
    "connector",
    "hook",
    "agent",
    "subagent",
    "tool",
    "unknown",
]


"""Configuration"""


class ProtocolError(ProtocolModel):
    """Serializable error returned through the session boundary."""

    message: str
    code: str | None = None
    details: JsonValue = None


class RequestEnvelope[ParamsT](ProtocolModel):
    """Transport request envelope for the Agent Session API."""

    id: str
    method: Procedure
    params: ParamsT


class ResponseEnvelope[ResultT](ProtocolModel):
    """Transport response envelope for the Agent Session API."""

    id: str
    result: ResultT | None = None
    error: ProtocolError | None = None


class ToolDefinition(ProtocolModel):
    """Client-owned callable exposed to the harness through callbacks."""

    type: Literal["client_tool"] = "client_tool"
    name: str
    description: str = ""
    input_schema: JsonSchema = Field(default_factory=dict)
    output_schema: JsonSchema = Field(default_factory=dict)


class HookDefinition(ProtocolModel):
    """Client hook registration exposed at the session boundary."""

    type: HookType
    name: str
    matcher: dict[str, JsonValue] = Field(default_factory=dict)


class SandboxConfig(ProtocolModel):
    """Serializable sandbox adapter configuration."""

    type: Literal["local", "managed"] = "local"
    image: str | None = None
    size: str | None = None
    network_access: bool | None = None
    env: dict[str, str] = Field(default_factory=dict)
    options: dict[str, JsonValue] = Field(default_factory=dict)


class AgentConfig(ProtocolModel):
    """Public normalized config passed from Agent to SessionHost."""

    completion: CompletionConfig = Field(default_factory=MistralCompletionConfig)
    sandbox: SandboxConfig | None = None
    instructions: str = ""
    workdir: AbsolutePath | None = None
    tools: list[ToolDefinition] = Field(default_factory=list)
    hooks: list[HookDefinition] = Field(default_factory=list)


class PluginComponent(ProtocolModel):
    """One parsed plugin-contributed capability."""

    kind: PluginComponentKind
    name: str
    source_path: AbsolutePath | None = None
    config: dict[str, JsonValue] = Field(default_factory=dict)


class PluginInfo(ProtocolModel):
    """Parsed plugin capability inventory for the current workdir/config."""

    workdir: AbsolutePath | None = None
    components: list[PluginComponent] = Field(default_factory=list)
    raw: dict[str, JsonValue] = Field(default_factory=dict)


class SessionStartParams(ProtocolModel):
    """Create or load a session channel without starting a turn."""

    agent_config: AgentConfig


class SessionResumeParams(ProtocolModel):
    """Load one stored session into a new live channel."""

    session_id: SessionId
    agent_config: AgentConfig


class SessionForkParams(ProtocolModel):
    """Create a new session from a stable source session boundary."""

    source_session_id: SessionId
    agent_config: AgentConfig
    after_turn_id: TurnId | None = None


"""Content blocks"""


class TextContentBlock(ProtocolModel):
    type: Literal["text"] = "text"
    text: str = ""


class ThinkingContentBlock(ProtocolModel):
    type: Literal["thinking"] = "thinking"
    thinking: str = ""


class ImageContentBlock(ProtocolModel):
    type: Literal["image"] = "image"
    uri: Uri
    media_type: str | None = None
    alt_text: str | None = None


class ResourceContentBlock(ProtocolModel):
    type: Literal["resource"] = "resource"
    uri: Uri
    title: str | None = None
    media_type: str | None = None


type ContentBlock = Annotated[
    TextContentBlock | ThinkingContentBlock | ImageContentBlock | ResourceContentBlock,
    Field(discriminator="type"),
]


"""History entries"""


class HistoryEntryBase(ProtocolModel):
    """Common public history entry fields.

    ``index`` is stable session order within the retained public history view.
    It is not a durable app-server event id.
    """

    id: HistoryEntryId
    index: int = Field(ge=0)
    turn_id: TurnId | None = None
    generation_status: GenerationStatus
    created_at: UnixMs
    updated_at: UnixMs


class MessageHistoryEntry(HistoryEntryBase):
    type: Literal["message"] = "message"
    role: MessageRole
    content: list[ContentBlock] = Field(default_factory=list)


class ReasoningHistoryEntry(HistoryEntryBase):
    type: Literal["reasoning"] = "reasoning"
    summary: list[str] = Field(default_factory=list)
    text: str = ""


class PlanItem(ProtocolModel):
    id: str
    text: str
    status: Literal["pending", "generating", "complete"]


class PlanHistoryEntry(HistoryEntryBase):
    type: Literal["plan"] = "plan"
    items: list[PlanItem] = Field(default_factory=list)
    text: str | None = None


class ToolCallHistoryEntry(HistoryEntryBase):
    type: Literal["tool_call"] = "tool_call"
    tool_call_id: ToolCallId
    tool_kind: ToolKind
    name: str
    arguments: JsonValue = None
    input_schema: JsonSchema | None = None
    output_schema: JsonSchema | None = None


class ToolResultHistoryEntry(HistoryEntryBase):
    type: Literal["tool_result"] = "tool_result"
    tool_call_id: ToolCallId
    name: str | None = None
    status: EffectStatus = "complete"
    result: JsonValue = None
    error: ProtocolError | None = None
    duration_ms: int | None = Field(default=None, ge=0)


class FileChange(ProtocolModel):
    path: AbsolutePath
    kind: Literal["create", "modify", "delete", "rename"]
    old_path: AbsolutePath | None = None
    diff: str | None = None


class FileChangeHistoryEntry(HistoryEntryBase):
    type: Literal["file_change"] = "file_change"
    changes: list[FileChange] = Field(default_factory=list)
    status: FileChangeStatus


class SubAgentHistoryEntry(HistoryEntryBase):
    type: Literal["sub_agent"] = "sub_agent"
    child_session_id: SessionId
    child_status: SessionStatus
    agent_name: str | None = None
    child_preview: str | None = None


class ResourceHistoryEntry(HistoryEntryBase):
    type: Literal["resource"] = "resource"
    uri: Uri
    title: str | None = None
    media_type: str | None = None


class CheckpointHistoryEntry(HistoryEntryBase):
    type: Literal["checkpoint"] = "checkpoint"
    checkpoint_kind: Literal["compaction", "rollback", "resume", "custom"]
    message: str | None = None
    details: JsonValue = None


class ErrorHistoryEntry(HistoryEntryBase):
    type: Literal["error"] = "error"
    error: ProtocolError


class NoticeHistoryEntry(HistoryEntryBase):
    type: Literal["notice"] = "notice"
    level: NoticeLevel
    message: str
    details: JsonValue = None


type HistoryEntry = Annotated[
    MessageHistoryEntry
    | ReasoningHistoryEntry
    | PlanHistoryEntry
    | ToolCallHistoryEntry
    | ToolResultHistoryEntry
    | FileChangeHistoryEntry
    | SubAgentHistoryEntry
    | ResourceHistoryEntry
    | CheckpointHistoryEntry
    | ErrorHistoryEntry
    | NoticeHistoryEntry,
    Field(discriminator="type"),
]


"""Session state and command results"""


class TurnState(ProtocolModel):
    id: TurnId
    status: TurnStatus
    started_at: UnixMs | None = None
    completed_at: UnixMs | None = None
    history_entry_ids: list[HistoryEntryId] = Field(default_factory=list)
    error: ProtocolError | None = None


class SessionState(ProtocolModel):
    """Current retained public state for one loaded session.

    ``history`` and ``turns`` are retained views. They are not a durable history
    log and may be vacuumed by the harness.
    """

    id: SessionId
    active_turn_id: TurnId | None = None
    status: SessionStatus = "waiting_for_input"
    title: str | None = None
    history: list[HistoryEntry] = Field(default_factory=list)
    turns: list[TurnState] = Field(default_factory=list)


class TurnRef(ProtocolModel):
    id: TurnId


class CommandAccepted(ProtocolModel):
    accepted: Literal[True] = True


class TurnStartParams(ProtocolModel):
    message: list[ContentBlock] = Field(default_factory=list)


class TurnSteerParams(ProtocolModel):
    expected_turn_id: TurnId
    message: list[ContentBlock] = Field(default_factory=list)


class TurnInterruptParams(ProtocolModel):
    expected_turn_id: TurnId


class SessionReadParams(ProtocolModel):
    pass


class SessionRenameParams(ProtocolModel):
    title: str


class SessionDeleteParams(ProtocolModel):
    pass


class SessionCompactParams(ProtocolModel):
    instructions: str | None = None


class SessionShellCommandParams(ProtocolModel):
    command: str
    cwd: AbsolutePath | None = None
    timeout_seconds: int | None = Field(default=None, ge=1)


class ConfigReadParams(ProtocolModel):
    pass


class ConfigReadResponse(ProtocolModel):
    config: AgentConfig


class ConfigWriteParams(ProtocolModel):
    config: AgentConfig


class ConfigWriteResponse(ProtocolModel):
    config: AgentConfig


class PluginInfoParams(ProtocolModel):
    pass


class PluginInfoResponse(ProtocolModel):
    info: PluginInfo


class PluginReloadParams(ProtocolModel):
    pass


class PluginReloadResponse(ProtocolModel):
    info: PluginInfo


class CallbackResult(ProtocolModel):
    """Answer a server-to-client callback emitted on the session event stream."""

    callback_id: CallbackId
    output: JsonValue = None
    error: ProtocolError | None = None


"""Control-plane session procedures available to subagents"""


ControlPlaneSessionProcedure = Literal[
    "subagent/session/turns",
    "subagent/session/history",
    "subagent/session/steer",
    "subagent/session/interrupt",
    "subagent/session/start_turn",
]


class ControlPlaneSessionTurnsRequest(ProtocolModel):
    session_id: SessionId


class ControlPlaneSessionHistoryRequest(ProtocolModel):
    session_id: SessionId


class ControlPlaneSessionStartTurnRequest(ProtocolModel):
    session_id: SessionId
    message: list[ContentBlock]


class ControlPlaneSessionSteerRequest(ProtocolModel):
    session_id: SessionId
    expected_turn_id: TurnId
    message: list[ContentBlock]


class ControlPlaneSessionInterruptRequest(ProtocolModel):
    session_id: SessionId
    expected_turn_id: TurnId

"""Event models for the Agent Session API."""

from typing import Annotated, Literal

from pydantic import Field, JsonValue

from ..base import JsonSchema, ProtocolModel
from .models import (
    AgentConfig,
    CallbackId,
    ContentBlock,
    HistoryEntry,
    HistoryEntryId,
    ProtocolError,
    ToolCallId,
    TurnId,
    TurnState,
)

"""Hook payload models"""


class PreAgentTurnInput(ProtocolModel):
    user_content: list[ContentBlock] = Field(default_factory=list)


class PostAgentTurnInput(ProtocolModel):
    assistant_content: list[ContentBlock] = Field(default_factory=list)


class PreLLMCallInput(ProtocolModel):
    pass


class PostLLMCallInput(ProtocolModel):
    pass


class PreToolCallInput(ProtocolModel):
    name: str
    args: JsonValue = None
    tool_call_id: str


class PostToolCallInput(ProtocolModel):
    name: str
    result: JsonValue = None
    tool_call_id: str


"""Session events"""


class HistoryEntryAddedEvent(ProtocolModel):
    type: Literal["history_entry_added"] = "history_entry_added"
    entry: HistoryEntry


class HistoryEntryPatchedEvent(ProtocolModel):
    type: Literal["history_entry_patched"] = "history_entry_patched"
    entry_id: HistoryEntryId
    entry_index: int = Field(ge=0)
    patches: list[dict[str, JsonValue]] = Field(default_factory=list)


class HistoryEntryCompletedEvent(ProtocolModel):
    type: Literal["history_entry_completed"] = "history_entry_completed"
    entry: HistoryEntry


class TurnStartedEvent(ProtocolModel):
    type: Literal["turn_started"] = "turn_started"
    turn: TurnState


class TurnUpdatedEvent(ProtocolModel):
    type: Literal["turn_updated"] = "turn_updated"
    turn: TurnState


class TurnCompletedEvent(ProtocolModel):
    type: Literal["turn_completed"] = "turn_completed"
    turn: TurnState
    output: JsonValue = None


class NoticeEvent(ProtocolModel):
    type: Literal["notice"] = "notice"
    message: str
    details: JsonValue = None


class ErrorEvent(ProtocolModel):
    type: Literal["error"] = "error"
    error: ProtocolError


"""Server-to-client callbacks"""


class BaseSessionCallback(ProtocolModel):
    id: CallbackId
    turn_id: TurnId | None = None


class ApprovalCallback(BaseSessionCallback):
    """Ask the client to approve or reject a tool call."""

    kind: Literal["approval"] = "approval"
    tool_call_id: ToolCallId
    title: str
    description: str = ""
    input: JsonValue = None


class UserInputCallback(BaseSessionCallback):
    """Ask the client to provide user input."""

    kind: Literal["user_input"] = "user_input"
    message: list[ContentBlock] = Field(default_factory=list)
    response_schema: JsonSchema | None = None


class AskEnableConnectorCallback(BaseSessionCallback):
    """Ask the client to authenticate or enable a connector."""

    kind: Literal["ask_enable_connector"] = "ask_enable_connector"
    connector_name: str
    reason: str = ""
    requirements: JsonValue = None


class ClientToolCallback(BaseSessionCallback):
    """Execute a client-side tool."""

    kind: Literal["client_tool"] = "client_tool"
    name: str
    input: JsonValue = None


class ClientHookCallback(BaseSessionCallback):
    """Execute a client-side hook."""

    kind: Literal["client_hook"] = "client_hook"
    name: str
    input: JsonValue = None


class ExecuteCodeCallback(BaseSessionCallback):
    """Execute code through the host sandbox adapter."""

    kind: Literal["execute_code"] = "execute_code"
    code: str


class StartSubagentCallback(BaseSessionCallback):
    """Start a subagent session through the host control-plane adapter."""

    kind: Literal["start_subagent"] = "start_subagent"
    agent_config: AgentConfig


type SessionCallback = Annotated[
    ApprovalCallback
    | UserInputCallback
    | AskEnableConnectorCallback
    | ClientToolCallback
    | ClientHookCallback
    | ExecuteCodeCallback
    | StartSubagentCallback,
    Field(discriminator="kind"),
]


class SessionCallbackEvent(ProtocolModel):
    type: Literal["callback"] = "callback"
    callback: SessionCallback


type SessionClientEvent = (
    HistoryEntryAddedEvent
    | HistoryEntryPatchedEvent
    | HistoryEntryCompletedEvent
    | TurnStartedEvent
    | TurnUpdatedEvent
    | TurnCompletedEvent
    | NoticeEvent
    | ErrorEvent
)

type SessionEvent = SessionClientEvent | SessionCallbackEvent


class EventNotification[EventT](ProtocolModel):
    """Server-to-client event notification envelope."""

    method: Literal["session/event"] = "session/event"
    params: EventT


type SessionEventNotification = EventNotification[SessionEvent]

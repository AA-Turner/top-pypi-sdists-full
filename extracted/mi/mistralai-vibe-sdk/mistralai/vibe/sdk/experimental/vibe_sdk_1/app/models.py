"""Serializable models for the Vibe App Server API."""

from typing import Annotated, Literal

from pydantic import Field, JsonValue

from ..base import ProtocolModel
from ..session.events import (
    ErrorEvent,
    HistoryEntryAddedEvent,
    HistoryEntryCompletedEvent,
    HistoryEntryPatchedEvent,
    NoticeEvent,
    SessionCallback,
    TurnCompletedEvent,
    TurnStartedEvent,
    TurnUpdatedEvent,
)
from ..session.models import (
    AgentConfig,
    CallbackId,
    CallbackResult,
    ContentBlock,
    HistoryEntry,
    PluginInfo,
    ProtocolError,
    SessionId,
    TurnId,
    TurnState,
    UnixMs,
)

type EventId = int
type Capability = dict[str, JsonValue]
type Procedure = Literal[
    "initialize",
    "session/start",
    "session/resume",
    "session/fork",
    "session/stop",
    "session/archive",
    "session/rename",
    "session/delete",
    "session/compact",
    "session/shellCommand",
    "session/list",
    "session/read",
    "session/history/list",
    "session/turns/list",
    "turn/start",
    "turn/steer",
    "turn/interrupt",
    "config/read",
    "config/write",
    "plugin/info",
    "plugin/reload",
    "callback/result",
    "events/read",
]
Status = Literal[
    "waiting_for_input",
    "running",
    "complete",
    "failed",
    "interrupted",
    "stopped",
    "archived",
]
SortDirection = Literal["forward", "backward"]
TransportEndReason = Literal["server_closed", "client_closed", "error"]


"""Transport envelopes"""


class RequestEnvelope[ParamsT](ProtocolModel):
    """Transport request envelope.

    ``id`` correlates a response to one request. It is not an idempotency key.
    """

    id: str
    method: Procedure
    params: ParamsT


class ResponseEnvelope[ResultT](ProtocolModel):
    """Transport response envelope."""

    id: str
    result: ResultT | None = None
    error: ProtocolError | None = None


"""Shared app-server views"""


class ClientInfo(ProtocolModel):
    name: str
    version: str
    title: str | None = None


class ServerInfo(ProtocolModel):
    name: str
    version: str


class PageRequest(ProtocolModel):
    cursor: str | None = None
    limit: int = Field(default=50, ge=1)
    direction: SortDirection = "backward"


class Page[ItemT](ProtocolModel):
    items: list[ItemT] = Field(default_factory=list)
    next_cursor: str | None = None
    previous_cursor: str | None = None


class Session(ProtocolModel):
    """App-server catalog view for one stored session."""

    id: SessionId
    root_session_id: SessionId
    parent_session_id: SessionId | None = None
    title: str | None = None
    preview: str = ""
    status: Status
    created_at: UnixMs
    updated_at: UnixMs
    archived_at: UnixMs | None = None


class SessionState(ProtocolModel):
    """App-server public session projection.

    This is not private ``TaskState`` and does not contain the global event-log
    read watermark. Response wrappers carry ``last_event_id``.
    """

    session: Session
    active_turn_id: TurnId | None = None
    status: Status
    history: Page[HistoryEntry] | None = None
    turns: Page[TurnState] | None = None
    active_callbacks: list[SessionCallback] = Field(default_factory=list)


"""Procedure request and response models"""


class InitializeParams(ProtocolModel):
    client_info: ClientInfo
    capabilities: dict[str, Capability] = Field(default_factory=dict)


class InitializeResponse(ProtocolModel):
    server_info: ServerInfo


class SessionStartParams(ProtocolModel):
    idempotency_key: str | None = None
    agent_config: AgentConfig


class SessionStartResponse(ProtocolModel):
    state: SessionState
    last_event_id: EventId


class SessionResumeParams(ProtocolModel):
    session_id: SessionId


class SessionResumeResponse(ProtocolModel):
    state: SessionState
    last_event_id: EventId


class SessionForkParams(ProtocolModel):
    idempotency_key: str | None = None
    source_session_id: SessionId
    agent_config: AgentConfig | None = None
    after_turn_id: TurnId | None = None


class SessionForkResponse(ProtocolModel):
    state: SessionState
    last_event_id: EventId


class SessionStopParams(ProtocolModel):
    session_id: SessionId
    reason: str | None = None


class SessionStopResponse(ProtocolModel):
    state: SessionState
    last_event_id: EventId


class SessionArchiveParams(ProtocolModel):
    session_id: SessionId
    archived: bool


class SessionArchiveResponse(ProtocolModel):
    state: SessionState
    last_event_id: EventId


class SessionRenameParams(ProtocolModel):
    session_id: SessionId
    title: str


class SessionRenameResponse(ProtocolModel):
    state: SessionState
    last_event_id: EventId


class SessionDeleteParams(ProtocolModel):
    session_id: SessionId


class SessionDeleteResponse(ProtocolModel):
    deleted: Literal[True] = True
    last_event_id: EventId


class SessionCompactParams(ProtocolModel):
    session_id: SessionId
    instructions: str | None = None


class SessionCompactResponse(ProtocolModel):
    state: SessionState
    last_event_id: EventId


class SessionShellCommandParams(ProtocolModel):
    idempotency_key: str | None = None
    session_id: SessionId
    command: str
    cwd: str | None = None
    timeout_seconds: int | None = Field(default=None, ge=1)


class SessionShellCommandResponse(ProtocolModel):
    accepted: Literal[True] = True
    last_event_id: EventId


class SessionListParams(ProtocolModel):
    cursor: str | None = None
    limit: int = Field(default=50, ge=1)
    include_archived: bool = False
    root_session_id: SessionId | None = None
    parent_session_id: SessionId | None = None


class SessionListResponse(ProtocolModel):
    items: list[Session] = Field(default_factory=list)
    next_cursor: str | None = None
    previous_cursor: str | None = None


class SessionReadParams(ProtocolModel):
    session_id: SessionId
    history: PageRequest | None = None
    turns: PageRequest | None = None


class SessionReadResponse(ProtocolModel):
    state: SessionState
    last_event_id: EventId


class SessionHistoryListParams(ProtocolModel):
    session_id: SessionId
    turn_id: TurnId | None = None
    page: PageRequest = Field(default_factory=PageRequest)


class SessionHistoryListResponse(ProtocolModel):
    page: Page[HistoryEntry]


class SessionTurnsListParams(ProtocolModel):
    session_id: SessionId
    page: PageRequest = Field(default_factory=PageRequest)


class SessionTurnsListResponse(ProtocolModel):
    page: Page[TurnState]


class TurnStartParams(ProtocolModel):
    idempotency_key: str | None = None
    session_id: SessionId
    message: list[ContentBlock] = Field(default_factory=list)


class TurnStartResponse(ProtocolModel):
    turn: TurnState
    last_event_id: EventId


class TurnSteerParams(ProtocolModel):
    idempotency_key: str | None = None
    session_id: SessionId
    expected_turn_id: TurnId
    message: list[ContentBlock] = Field(default_factory=list)


class TurnSteerResponse(ProtocolModel):
    accepted: Literal[True] = True
    last_event_id: EventId


class TurnInterruptParams(ProtocolModel):
    session_id: SessionId
    expected_turn_id: TurnId


class TurnInterruptResponse(ProtocolModel):
    accepted: Literal[True] = True
    last_event_id: EventId


class ConfigReadParams(ProtocolModel):
    session_id: SessionId


class ConfigReadResponse(ProtocolModel):
    config: AgentConfig


class ConfigWriteParams(ProtocolModel):
    session_id: SessionId
    config: AgentConfig


class ConfigWriteResponse(ProtocolModel):
    config: AgentConfig
    last_event_id: EventId


class PluginInfoParams(ProtocolModel):
    session_id: SessionId


class PluginInfoResponse(ProtocolModel):
    info: PluginInfo


class PluginReloadParams(ProtocolModel):
    session_id: SessionId


class PluginReloadResponse(ProtocolModel):
    info: PluginInfo
    last_event_id: EventId


class CallbackResultParams(ProtocolModel):
    session_id: SessionId
    result: CallbackResult


class CallbackResultResponse(ProtocolModel):
    accepted: Literal[True] = True
    last_event_id: EventId


"""Event stream models"""


class SessionUpdatedEvent(ProtocolModel):
    type: Literal["session_updated"] = "session_updated"
    state: SessionState


class CallbackOpenedEvent(ProtocolModel):
    type: Literal["callback_opened"] = "callback_opened"
    callback: SessionCallback


class CallbackResolvedEvent(ProtocolModel):
    type: Literal["callback_resolved"] = "callback_resolved"
    callback_id: CallbackId


type EventPayload = Annotated[
    SessionUpdatedEvent
    | HistoryEntryAddedEvent
    | HistoryEntryPatchedEvent
    | HistoryEntryCompletedEvent
    | TurnStartedEvent
    | TurnUpdatedEvent
    | TurnCompletedEvent
    | CallbackOpenedEvent
    | CallbackResolvedEvent
    | NoticeEvent
    | ErrorEvent,
    Field(discriminator="type"),
]


class Event(ProtocolModel):
    """One app-server event in the global event log."""

    event_id: EventId
    emitted_at: UnixMs
    session_id: SessionId
    root_session_id: SessionId | None = None
    payload: EventPayload


class EventBatch(ProtocolModel):
    type: Literal["events"] = "events"
    events: list[Event] = Field(default_factory=list)


class EventsFilter(ProtocolModel):
    session_ids: list[SessionId] = Field(default_factory=list)
    root_session_ids: list[SessionId] = Field(default_factory=list)
    parent_session_ids: list[SessionId] = Field(default_factory=list)
    event_types: list[str] = Field(default_factory=list)


class EventsReadParams(ProtocolModel):
    after_event_id: EventId | None = None
    filters: EventsFilter = Field(default_factory=EventsFilter)
    batch_size: int = Field(default=100, ge=1)


type EventStreamItem = Event | EventBatch


"""Optional transport stream framing"""


class TransportStreamStarted(ProtocolModel):
    type: Literal["stream_started"] = "stream_started"


class TransportHeartbeat(ProtocolModel):
    type: Literal["heartbeat"] = "heartbeat"
    latest_event_id: EventId | None = None


class TransportStreamEnded(ProtocolModel):
    type: Literal["stream_ended"] = "stream_ended"
    reason: TransportEndReason
    latest_event_id: EventId | None = None


type TransportStreamItem = (
    EventStreamItem | TransportStreamStarted | TransportHeartbeat | TransportStreamEnded
)

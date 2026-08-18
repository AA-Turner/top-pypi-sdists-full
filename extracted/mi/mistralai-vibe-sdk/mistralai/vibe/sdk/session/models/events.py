"""Ordered public events emitted for one Session."""

from typing import Annotated, Literal

from pydantic import Field, JsonValue, TypeAdapter, field_validator

from .base import SessionModel
from .callbacks import SessionCallback
from .common import CallbackId, EventId, HistoryEntryId, ProtocolError, SessionId, UnixMs
from .history import HistoryEntry
from .state import SessionState, TurnState

type JsonPointer = str


class JsonPatchAddOperation(SessionModel):
    op: Literal["add"] = "add"
    path: JsonPointer
    value: JsonValue


class JsonPatchReplaceOperation(SessionModel):
    op: Literal["replace"] = "replace"
    path: JsonPointer
    value: JsonValue


class JsonPatchTestOperation(SessionModel):
    op: Literal["test"] = "test"
    path: JsonPointer
    value: JsonValue


class JsonPatchRemoveOperation(SessionModel):
    op: Literal["remove"] = "remove"
    path: JsonPointer


class JsonPatchMoveOperation(SessionModel):
    op: Literal["move"] = "move"
    path: JsonPointer
    from_: JsonPointer = Field(alias="from")


class JsonPatchCopyOperation(SessionModel):
    op: Literal["copy"] = "copy"
    path: JsonPointer
    from_: JsonPointer = Field(alias="from")


class JsonPatchAppendOperation(SessionModel):
    op: Literal["append"] = "append"
    path: JsonPointer
    value: str


type JsonPatchOperation = Annotated[
    JsonPatchAddOperation
    | JsonPatchReplaceOperation
    | JsonPatchTestOperation
    | JsonPatchRemoveOperation
    | JsonPatchMoveOperation
    | JsonPatchCopyOperation
    | JsonPatchAppendOperation,
    Field(discriminator="op"),
]

JsonPatchOperationAdapter: TypeAdapter[JsonPatchOperation] = TypeAdapter(JsonPatchOperation)


class HistoryEntryAddedEvent(SessionModel):
    type: Literal["history_entry_added"] = "history_entry_added"
    entry: HistoryEntry


class HistoryEntryPatchedEvent(SessionModel):
    type: Literal["history_entry_patched"] = "history_entry_patched"
    entry_id: HistoryEntryId
    entry_index: int = Field(ge=0)
    patches: list[JsonPatchOperation] = Field(default_factory=list)


class HistoryEntryCompletedEvent(SessionModel):
    type: Literal["history_entry_completed"] = "history_entry_completed"
    entry: HistoryEntry


class TurnStartedEvent(SessionModel):
    type: Literal["turn_started"] = "turn_started"
    turn: TurnState


class TurnUpdatedEvent(SessionModel):
    type: Literal["turn_updated"] = "turn_updated"
    turn: TurnState


class TurnTerminatedEvent(SessionModel):
    type: Literal["turn_terminated"] = "turn_terminated"
    turn: TurnState


class SessionUpdatedEvent(SessionModel):
    type: Literal["session_updated"] = "session_updated"
    state: SessionState


class SessionTerminatedEvent(SessionModel):
    type: Literal["session_terminated"] = "session_terminated"
    state: SessionState


class CallbackOpenedEvent(SessionModel):
    type: Literal["callback_opened"] = "callback_opened"
    callback: SessionCallback


class CallbackResolvedEvent(SessionModel):
    type: Literal["callback_resolved"] = "callback_resolved"
    callback_id: CallbackId


class NoticeEvent(SessionModel):
    type: Literal["notice"] = "notice"
    message: str
    details: JsonValue = None


class ErrorEvent(SessionModel):
    type: Literal["error"] = "error"
    error: ProtocolError


type SessionClientEvent = (
    SessionUpdatedEvent
    | SessionTerminatedEvent
    | HistoryEntryAddedEvent
    | HistoryEntryPatchedEvent
    | HistoryEntryCompletedEvent
    | TurnStartedEvent
    | TurnUpdatedEvent
    | TurnTerminatedEvent
    | NoticeEvent
    | ErrorEvent
)

type SessionCallbackEvent = CallbackOpenedEvent | CallbackResolvedEvent

type SessionEvent = Annotated[
    SessionClientEvent | SessionCallbackEvent,
    Field(discriminator="type"),
]

type EventPayload = SessionEvent

SessionEventAdapter: TypeAdapter[SessionEvent] = TypeAdapter(SessionEvent)
EventPayloadAdapter = SessionEventAdapter

_KNOWN_EVENT_PAYLOAD_TYPES = frozenset(
    {
        "history_entry_added",
        "history_entry_patched",
        "history_entry_completed",
        "turn_started",
        "turn_updated",
        "turn_terminated",
        "session_updated",
        "session_terminated",
        "callback_opened",
        "callback_resolved",
        "notice",
        "error",
    }
)


class Event(SessionModel):
    """One event in a Session-scoped order."""

    event_id: EventId
    emitted_at: UnixMs
    session_id: SessionId
    root_session_id: SessionId | None = None
    payload: EventPayload


class EventBatch(SessionModel):
    type: Literal["events"] = "events"
    events: list[Event] = Field(default_factory=list)


class UnknownEventPayload(SessionModel):
    type: Literal["unknown"] = "unknown"
    original_type: str
    raw: dict[str, JsonValue] = Field(default_factory=dict)


type ClientEventPayload = SessionEvent | UnknownEventPayload


class ClientEvent(Event):
    """Client-side event parser that preserves unknown payload variants."""

    payload: ClientEventPayload

    @field_validator("payload", mode="before")
    @classmethod
    def parse_unknown_payload(cls, value: object) -> object:
        if isinstance(value, dict):
            payload_type = value.get("type")
            if isinstance(payload_type, str) and payload_type not in _KNOWN_EVENT_PAYLOAD_TYPES:
                return UnknownEventPayload(original_type=payload_type, raw=value)
        return value


class ClientEventBatch(EventBatch):
    events: list[ClientEvent] = Field(default_factory=list)


type TransportEndReason = Literal["server_closed", "client_closed", "error"]


class TransportStreamStarted(SessionModel):
    type: Literal["stream_started"] = "stream_started"


class TransportHeartbeat(SessionModel):
    type: Literal["heartbeat"] = "heartbeat"
    latest_event_id: EventId | None = None


class TransportStreamEnded(SessionModel):
    type: Literal["stream_ended"] = "stream_ended"
    reason: TransportEndReason
    latest_event_id: EventId | None = None


type EventStreamItem = Event | EventBatch
type ClientEventStreamItem = ClientEvent | ClientEventBatch
type TransportStreamItem = (
    Event | EventBatch | TransportStreamStarted | TransportHeartbeat | TransportStreamEnded
)
type ClientTransportStreamItem = (
    Event
    | EventBatch
    | ClientEvent
    | ClientEventBatch
    | TransportStreamStarted
    | TransportHeartbeat
    | TransportStreamEnded
)

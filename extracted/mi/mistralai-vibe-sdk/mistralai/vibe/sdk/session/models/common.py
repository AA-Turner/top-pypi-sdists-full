"""Value types shared by Session state, events, and procedures."""

from typing import Literal

from pydantic import JsonValue

from .base import SessionModel

type SessionId = str
type TurnId = str
type HistoryEntryId = str
type ToolCallId = str
type CallbackId = str
type EventId = str
type UnixMs = int
type Uri = str
type AbsolutePath = str
type MessageRole = Literal["system", "user", "assistant"]
type ToolKind = Literal["builtin", "local", "mcp", "client", "plugin"]
type GenerationStatus = Literal["generating", "complete"]
type SessionStatus = Literal["running", "waiting", "terminated"]
type TurnStatus = Literal["running", "blocked", "terminated"]


class ProtocolError(SessionModel):
    """Serializable error exposed through the Session boundary."""

    message: str
    code: str | None = None
    details: JsonValue = None

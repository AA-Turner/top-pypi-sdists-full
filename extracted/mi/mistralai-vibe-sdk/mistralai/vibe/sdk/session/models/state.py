"""Public Session catalog and retained state views."""

from typing import Annotated, Literal, Self

from pydantic import Field, JsonValue, model_validator

from .base import SessionModel
from .callbacks import SessionCallback
from .common import (
    HistoryEntryId,
    ProtocolError,
    SessionId,
    SessionStatus,
    TurnId,
    TurnStatus,
    UnixMs,
)
from .history import HistoryEntry

type SortDirection = Literal["forward", "backward"]


class PageRequest(SessionModel):
    cursor: str | None = None
    limit: int = Field(default=50, ge=1)
    direction: SortDirection = "backward"


class Page[ItemT](SessionModel):
    items: list[ItemT] = Field(default_factory=list)
    next_cursor: str | None = None
    previous_cursor: str | None = None


class CompletedTermination(SessionModel):
    outcome: Literal["completed"] = "completed"
    output: JsonValue = None


class CancelledTermination(SessionModel):
    outcome: Literal["cancelled"] = "cancelled"
    reason: str | None = None


class FailedTermination(SessionModel):
    outcome: Literal["failed"] = "failed"
    error: ProtocolError


type Termination = Annotated[
    CompletedTermination | CancelledTermination | FailedTermination,
    Field(discriminator="outcome"),
]


class TurnState(SessionModel):
    id: TurnId
    status: TurnStatus
    started_at: UnixMs | None = None
    completed_at: UnixMs | None = None
    history_entry_ids: list[HistoryEntryId] = Field(default_factory=list)
    termination: Termination | None = None

    @model_validator(mode="after")
    def validate_termination(self) -> Self:
        if self.status == "terminated" and self.termination is None:
            raise ValueError("A terminated turn requires termination details")
        if self.status != "terminated" and self.termination is not None:
            raise ValueError("A non-terminal turn cannot have termination details")
        return self


class Session(SessionModel):
    """Catalog view for one stored Session."""

    id: SessionId
    root_session_id: SessionId
    parent_session_id: SessionId | None = None
    title: str | None = None
    preview: str = ""
    status: SessionStatus
    termination: Termination | None = None
    created_at: UnixMs
    updated_at: UnixMs
    archived_at: UnixMs | None = None

    @model_validator(mode="after")
    def validate_termination(self) -> Self:
        if self.status == "terminated" and self.termination is None:
            raise ValueError("A terminated Session requires termination details")
        if self.status != "terminated" and self.termination is not None:
            raise ValueError("A non-terminal Session cannot have termination details")
        return self


class SessionState(SessionModel):
    """Public projection returned by stateless Session reads."""

    session: Session
    active_turn_id: TurnId | None = None
    history: Page[HistoryEntry] | None = None
    turns: Page[TurnState] | None = None
    active_callbacks: list[SessionCallback] = Field(default_factory=list)

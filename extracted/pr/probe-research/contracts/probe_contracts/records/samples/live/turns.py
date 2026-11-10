"""Live turns: a watched attempt's conversation as it happens (ClickHouse `sample_live_turns`, kept 14 days)."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, Field

from ...records import Record
from ..samples import MAX_KEY_CHARS

#: One turn's text, after the credential scrubber (the same cap as a row's inline turn text).
MAX_LIVE_TURN_BYTES = 64 * 1024


def check_live_turn_text(value: str) -> str:
    if len(value.encode("utf-8")) > MAX_LIVE_TURN_BYTES:
        raise ValueError("a live turn is over 64 KiB: cut it, keeping the end")
    return value


LiveTurnText = Annotated[str, AfterValidator(check_live_turn_text)]


class LiveTurn(Record):
    """One turn of a watched attempt. Identity is (run, attempt, seq): a resend lands on the same turn."""

    run_id: UUID
    write_epoch: int = Field(ge=1)
    #: `derive_attempt_id(run_id, write_epoch, attempt_key)`.
    attempt_id: UUID
    attempt_key: str = Field(min_length=1, max_length=MAX_KEY_CHARS)
    #: Per attempt, from 0: the `?after=` cursor. A watch's first turns are the conversation so far.
    seq: int = Field(ge=0)
    #: The producer's clock.
    at: datetime
    #: The chat role as the framework sent it (user, assistant, tool, system).
    role: str = Field(min_length=1, max_length=64)
    content: LiveTurnText = ""
    tool_name: str | None = Field(default=None, max_length=256)
    tokens: int | None = Field(default=None, ge=0)
    weight_version: int | None = Field(default=None, ge=0)
    #: read: the server's receipt time.
    received_at: datetime | None = None


class LiveTurnIn(LiveTurn.project(
    "attempt_key", "seq", "at", "role", "content", "tool_name", "tokens", "weight_version",
)):
    """A live turn on the wire (`SampleBatchIn.live_turns`): the server derives the attempt id from the batch's epoch."""


class LiveTurnOut(LiveTurn.project(*LiveTurn.model_fields)):
    """A live turn as `GET .../samples/live/{attempt}/turns` answers it."""


class LiveTurnList(BaseModel):
    attempt_id: UUID
    turns: list[LiveTurnOut] = Field(default_factory=list)
    #: The last turn's seq: pass back as `after`. Null when none came yet.
    next_after: int | None = None

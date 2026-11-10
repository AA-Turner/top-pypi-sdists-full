"""Turns: a multi-turn attempt's messages, each with its source and trainable flag, plus its lifecycle events."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, FiniteFloat

from ...compat import StrEnum

#: An event's `detail` and a tool call's `error`: one short line each.
MAX_DETAIL_CHARS = 1024


class MessageSource(StrEnum):
    """Who wrote a message. Gym observations arrive as role=user, so `role` alone cannot tell (DESIGN.md)."""

    MODEL = "model"
    ENVIRONMENT = "environment"
    TOOL = "tool"
    USER = "user"
    SYSTEM = "system"


class Message(BaseModel):
    #: The chat role as the framework sent it (user, assistant, tool, system).
    role: str = Field(max_length=64)
    source: MessageSource
    #: In the loss: the model's own tokens the trainer learns from.
    is_trainable: bool = False
    content: str = ""
    name: str | None = Field(default=None, max_length=256)
    tool_call_id: str | None = Field(default=None, max_length=256)


class TurnToolCall(BaseModel):
    """One tool call's stats: what ran, whether it worked, how long it took."""

    name: str = Field(max_length=256)
    is_ok: bool | None = None
    duration_s: float | None = Field(default=None, ge=0)
    error: str | None = Field(default=None, max_length=MAX_DETAIL_CHARS)


class Turn(BaseModel):
    messages: list[Message] = Field(default_factory=list)
    #: A process or step-wise reward for this turn alone.
    reward: FiniteFloat | None = None
    tool_calls: list[TurnToolCall] = Field(default_factory=list)


class SampleEventKind(StrEnum):
    """Miles' trajectory events, for every framework."""

    ATTEMPT_START = "attempt_start"
    ATTEMPT_END = "attempt_end"
    GENERATION_START = "generation_start"
    GENERATION_END = "generation_end"
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"


class SampleEvent(BaseModel):
    kind: SampleEventKind
    at: datetime
    turn: int | None = Field(default=None, ge=0)
    weight_version: int | None = Field(default=None, ge=0)
    detail: str | None = Field(default=None, max_length=MAX_DETAIL_CHARS)

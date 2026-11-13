"""Turns: a multi-turn attempt's messages (each with its source, trainable flag, tool calls and reasoning), plus its
lifecycle events."""

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


class TurnsSource(StrEnum):
    """Where a sample's turns came from, so a reader can tell the messages as sent from text Probe rebuilt."""

    AS_SENT = "as_sent"  # the messages the agent loop or framework built
    DECODED = "decoded"  # Probe rebuilt them from token ids (no structured messages were held)


class MessageToolCall(BaseModel):
    """One tool call an assistant message asked for, as the framework handed it to the tool (not `ToolCall`: that
    name collided in OpenAPI, #4640). Its run's stats are the `TurnToolCall` with the same `id`."""

    #: As the framework named it; `probe-<turn>-<i>` when Probe numbered it (the plan declares `tool_call_ids`).
    id: str | None = Field(default=None, max_length=256)
    name: str = Field(max_length=256)
    #: The arguments as the framework handed them to the tool (JSON text), credentials scrubbed by value; the model's
    #: exact bytes stay in the token bundle.
    arguments: str = ""


class Message(BaseModel):
    #: The chat role as the framework sent it (user, assistant, tool, system).
    role: str = Field(max_length=64)
    source: MessageSource
    #: In the loss: the model's own tokens the trainer learns from.
    is_trainable: bool = False
    content: str = ""
    name: str | None = Field(default=None, max_length=256)
    tool_call_id: str | None = Field(default=None, max_length=256)
    #: The model's reasoning, apart from `content`, only where the model or engine gives it (None, never "").
    reasoning: str | None = None
    tool_calls: list[MessageToolCall] = Field(default_factory=list)


class TurnToolCall(BaseModel):
    """One tool call's stats: what ran, whether it worked, how long it took."""

    #: The `MessageToolCall` this run executed.
    id: str | None = Field(default=None, max_length=256)
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

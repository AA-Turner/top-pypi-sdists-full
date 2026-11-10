"""Dialect: one model API the proxy reads (OpenAI chat completions, completions, responses; Anthropic messages):
the request's conversation as turns, the reply (whole or SSE), and this API's error bodies (`dialects/`)."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, ClassVar

from .sse import SseFrame


@dataclass(frozen=True)
class ToolCall:
    """A tool the model asked for: its name and its arguments as the API sent them (a JSON string)."""

    name: str
    arguments: str = ""


@dataclass
class Reply:
    """What one model call answered. `history_items`: how many items it adds to the next request's history."""

    turns: list[dict] = field(default_factory=list)
    finish_reason: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    history_items: int = 1


class Dialect(ABC):
    """One model API. `path_suffix`: the request path it serves (`/chat/completions`)."""

    name: ClassVar[str]
    path_suffix: ClassVar[str]

    @abstractmethod
    def read_history(self, request: dict) -> list[dict]:
        """The request's conversation (system, user, assistant, tool) as turns, oldest first."""

    @abstractmethod
    def read_reply(self, body: dict) -> Reply:
        """A whole (not streamed) answer."""

    @abstractmethod
    def read_stream(self, frames: list[SseFrame]) -> Reply:
        """A streamed answer, from its SSE frames."""

    def is_whole_history(self, request: dict) -> bool:
        """Does the request carry the whole conversation (else only what is new since the last call)?"""
        return True

    def make_error(self, code: str, message: str) -> dict:
        """This API's error body (OpenAI's shape; Anthropic overrides it)."""
        return {"error": {"message": message, "type": code, "param": None, "code": code}}

    def make_stream_error(self, code: str, message: str) -> bytes:
        """An SSE frame the API's SDK raises on mid-stream (OpenAI's: a data frame with `error`)."""
        return b"data: " + json.dumps(self.make_error(code, message)).encode() + b"\n\n"


def make_turn(role: Any, content: Any, *, tool_name: Any = None, tokens: int | None = None) -> dict:
    """A turn as `run.samples.log_turns` takes it."""
    turn: dict[str, Any] = {"role": str(role or "assistant"), "content": content if content is not None else ""}
    if tool_name:
        turn["tool_name"] = str(tool_name)
    if isinstance(tokens, int) and not isinstance(tokens, bool) and tokens >= 0:
        turn["tokens"] = tokens
    return turn


def render_tool_calls(text: str, calls: list[ToolCall]) -> str:
    """A reply's text and the tools it asked for, one `name(arguments)` line each."""
    lines = [text] if text else []
    lines += [f"{call.name}({call.arguments})" for call in calls]
    return "\n".join(lines)


def read_count(value: Any) -> int | None:
    """A token count as the API gave it, or None."""
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def read_first_choice(body: dict) -> dict:
    """An OpenAI answer's (or chunk's) first choice, or {} (agents ask for one)."""
    choices = body.get("choices")
    if isinstance(choices, list) and choices and isinstance(choices[0], dict):
        return choices[0]
    return {}


def read_frame_json(frame: SseFrame) -> dict | None:
    """A frame's data as a JSON object, or None (`[DONE]`, a keepalive, a broken frame)."""
    if not frame.data or frame.data.startswith("[DONE]"):
        return None
    try:
        value = json.loads(frame.data)
    except ValueError:
        return None
    return value if isinstance(value, dict) else None

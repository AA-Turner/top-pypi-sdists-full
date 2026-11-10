"""Anthropic messages (`POST .../messages`), as Anthropic and SGLang's Anthropic route answer it. Its errors have
their own shape, and a streamed error is an `error` event."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from ..dialect import Dialect, Reply, ToolCall, make_turn, read_count, read_frame_json, render_tool_calls
from ..sse import SseFrame


class MessagesDialect(Dialect):
    name = "messages"
    path_suffix = "/messages"

    def read_history(self, request: dict) -> list[dict]:
        turns = []
        system = request.get("system")
        if system:
            turns.append(make_turn("system", system if isinstance(system, str) else _read_blocks(system)[0]))
        for message in request.get("messages") or ():
            if not isinstance(message, dict):
                continue
            content = message.get("content")
            if isinstance(content, str):
                turns.append(make_turn(message.get("role"), content))
                continue
            text, calls, is_results = _read_blocks(content)
            role = "tool" if is_results else message.get("role")
            turns.append(make_turn(role, text, tool_name=calls[0].name if calls else None))
        return turns

    def read_reply(self, body: dict) -> Reply:
        text, calls, _ = _read_blocks(body.get("content"))
        return _make_reply(text, calls, body.get("stop_reason"), body.get("usage"), None)

    def read_stream(self, frames: list[SseFrame]) -> Reply:
        stream = _MessageStream()
        for frame in frames:
            event = read_frame_json(frame)
            if event is not None:
                stream.take(str(event.get("type") or frame.event), event)
        return stream.to_reply()

    def make_error(self, code: str, message: str) -> dict:
        return {"type": "error", "error": {"type": code, "message": message}}

    def make_stream_error(self, code: str, message: str) -> bytes:
        return b"event: error\ndata: " + json.dumps(self.make_error(code, message)).encode() + b"\n\n"


class _MessageStream:
    """Anthropic's stream events folded into one reply, each event by its own method."""

    def __init__(self) -> None:
        self.blocks: dict[int, dict[str, Any]] = {}
        self.finish: str | None = None
        self.usage: dict = {}
        self.input_tokens: int | None = None

    def take(self, event_type: str, event: dict) -> None:
        handle = _STREAM_EVENTS.get(event_type)
        if handle is not None:
            handle(self, event)

    def start_message(self, event: dict) -> None:
        message = event.get("message") if isinstance(event.get("message"), dict) else {}
        self.input_tokens = read_count((message.get("usage") or {}).get("input_tokens"))

    def start_block(self, event: dict) -> None:
        block = event.get("content_block") if isinstance(event.get("content_block"), dict) else {}
        self.blocks[int(event.get("index") or 0)] = {"type": block.get("type"), "name": block.get("name"), "parts": []}

    def add_delta(self, event: dict) -> None:
        delta = event.get("delta") if isinstance(event.get("delta"), dict) else {}
        part = delta.get("text") if delta.get("type") == "text_delta" else delta.get("partial_json")
        if isinstance(part, str):
            empty = {"type": None, "name": None, "parts": []}
            self.blocks.setdefault(int(event.get("index") or 0), empty)["parts"].append(part)

    def end_message(self, event: dict) -> None:
        self.finish = (event.get("delta") or {}).get("stop_reason") or self.finish
        self.usage = event.get("usage") if isinstance(event.get("usage"), dict) else self.usage

    def fail(self, event: dict) -> None:
        self.finish = "error"

    def to_reply(self) -> Reply:
        blocks = [block for _, block in sorted(self.blocks.items())]
        text = "".join("".join(block["parts"]) for block in blocks if block["type"] == "text")
        calls = [ToolCall(str(block["name"]), "".join(block["parts"])) for block in blocks
                 if block["type"] == "tool_use" and block["name"]]  # fmt: skip
        return _make_reply(render_tool_calls(text, calls), calls, self.finish, self.usage, self.input_tokens)


#: Each stream event's handler; events not named here (pings, block stops, `message_stop`) change nothing.
_STREAM_EVENTS: dict[str, Callable[[_MessageStream, dict], None]] = {
    "message_start": _MessageStream.start_message,
    "content_block_start": _MessageStream.start_block,
    "content_block_delta": _MessageStream.add_delta,
    "message_delta": _MessageStream.end_message,
    "error": _MessageStream.fail,
}


def _read_blocks(content: Any) -> tuple[str, list[ToolCall], bool]:
    """Content blocks as (text, the tools asked for, whether every block is a tool result)."""
    if isinstance(content, str):
        return content, [], False
    texts: list[str] = []
    calls: list[ToolCall] = []
    kinds = []
    for block in content or ():
        if not isinstance(block, dict):
            continue
        kind = block.get("type")
        kinds.append(kind)
        if kind == "text" and isinstance(block.get("text"), str):
            texts.append(block["text"])
        elif kind == "tool_use" and block.get("name"):
            calls.append(ToolCall(str(block["name"]), json.dumps(block.get("input"), ensure_ascii=False)))
        elif kind == "tool_result":
            inner = block.get("content")
            texts.append(inner if isinstance(inner, str) else _read_blocks(inner)[0])
        else:
            texts.append(f"[{kind}]")
    is_results = bool(kinds) and all(kind == "tool_result" for kind in kinds)
    return render_tool_calls("\n".join(texts), calls), calls, is_results


def _make_reply(text: str, calls: list[ToolCall], finish: Any, usage: Any, input_tokens: int | None) -> Reply:
    usage = usage if isinstance(usage, dict) else {}
    output_tokens = read_count(usage.get("output_tokens"))
    turn = make_turn("assistant", text, tool_name=calls[0].name if calls else None, tokens=output_tokens)
    return Reply(turns=[turn], finish_reason=str(finish) if finish else None,
                 input_tokens=input_tokens if input_tokens is not None else read_count(usage.get("input_tokens")),
                 output_tokens=output_tokens, tool_calls=calls)  # fmt: skip

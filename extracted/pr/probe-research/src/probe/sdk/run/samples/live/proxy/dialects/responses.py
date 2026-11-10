"""OpenAI responses (`POST .../responses`). A request with `previous_response_id` carries only what is new (the
history is the server's); a streamed answer ends with the whole response in `response.completed`."""

from __future__ import annotations

from typing import Any

from ..dialect import Dialect, Reply, ToolCall, make_turn, read_count, read_frame_json, render_tool_calls
from ..sse import SseFrame

#: The stream's last event, carrying the whole response.
_FINAL_EVENTS = frozenset({"response.completed", "response.incomplete", "response.failed"})


class ResponsesDialect(Dialect):
    name = "responses"
    path_suffix = "/responses"

    def read_history(self, request: dict) -> list[dict]:
        turns = []
        if request.get("instructions"):
            turns.append(make_turn("system", request["instructions"]))
        given = request.get("input")
        if isinstance(given, str):
            return [*turns, make_turn("user", given)]
        for item in given or ():
            if isinstance(item, dict):
                turns.append(_read_item(item))
        return turns

    def is_whole_history(self, request: dict) -> bool:
        return not request.get("previous_response_id")

    def read_reply(self, body: dict) -> Reply:
        text: list[str] = []
        calls: list[ToolCall] = []
        output = body.get("output") if isinstance(body.get("output"), list) else []
        for item in output:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "message":
                text.append(_read_text(item.get("content")))
            elif item.get("type") == "function_call" and item.get("name"):
                arguments = item.get("arguments")
                calls.append(ToolCall(str(item["name"]), arguments if isinstance(arguments, str) else ""))
        details = body.get("incomplete_details") if isinstance(body.get("incomplete_details"), dict) else {}
        finish = details.get("reason") or body.get("status")
        usage = body.get("usage") if isinstance(body.get("usage"), dict) else {}
        output_tokens = read_count(usage.get("output_tokens"))
        turn = make_turn("assistant", render_tool_calls("".join(text), calls),
                         tool_name=calls[0].name if calls else None, tokens=output_tokens)  # fmt: skip
        return Reply(turns=[turn], finish_reason=str(finish) if finish else None,
                     input_tokens=read_count(usage.get("input_tokens")), output_tokens=output_tokens, tool_calls=calls,
                     history_items=max(1, len(output)))  # fmt: skip

    def read_stream(self, frames: list[SseFrame]) -> Reply:
        text: list[str] = []
        names: list[str] = []
        for frame in frames:
            event = read_frame_json(frame)
            if event is None:
                continue
            kind = event.get("type") or frame.event
            if kind in _FINAL_EVENTS and isinstance(event.get("response"), dict):
                return self.read_reply(event["response"])
            if kind == "response.output_text.delta" and isinstance(event.get("delta"), str):
                text.append(event["delta"])
            item = event.get("item") if isinstance(event.get("item"), dict) else {}
            if kind == "response.output_item.added" and item.get("type") == "function_call" and item.get("name"):
                names.append(str(item["name"]))
        calls = [ToolCall(name) for name in names]  # a cut stream: what came before the cut
        turn = make_turn("assistant", render_tool_calls("".join(text), calls), tool_name=names[0] if names else None)
        return Reply(turns=[turn], tool_calls=calls)


def _read_item(item: dict) -> dict:
    kind = item.get("type")
    if kind == "function_call":
        call = ToolCall(str(item.get("name") or ""), str(item.get("arguments") or ""))
        return make_turn("assistant", render_tool_calls("", [call]), tool_name=call.name)
    if kind == "function_call_output":
        return make_turn("tool", item.get("output"))
    content = item.get("content")
    return make_turn(item.get("role") or kind, content if isinstance(content, str) else _read_text(content))


def _read_text(content: Any) -> str:
    """The text parts of a message's content (`input_text`, `output_text`), joined; others as their type."""
    if isinstance(content, str):
        return content
    parts = []
    for part in content or ():
        if isinstance(part, dict):
            parts.append(part["text"] if isinstance(part.get("text"), str) else f"[{part.get('type')}]")
    return "".join(parts)

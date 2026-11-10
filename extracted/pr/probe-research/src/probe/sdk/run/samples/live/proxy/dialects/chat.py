"""OpenAI chat completions (`POST .../chat/completions`), as OpenAI, vLLM and SGLang answer it."""

from __future__ import annotations

from typing import Any

from ..dialect import Dialect, Reply, ToolCall, make_turn, read_count, read_first_choice, read_frame_json, render_tool_calls
from ..sse import SseFrame


class ChatDialect(Dialect):
    name = "chat"
    path_suffix = "/chat/completions"

    def read_history(self, request: dict) -> list[dict]:
        turns = []
        for message in request.get("messages") or ():
            if not isinstance(message, dict):
                continue
            calls = _read_tool_calls(message.get("tool_calls"))
            content = message.get("content")
            if calls:
                content = render_tool_calls(content if isinstance(content, str) else "", calls)
            tool_name = calls[0].name if calls else message.get("name")
            turns.append(make_turn(message.get("role"), content, tool_name=tool_name))
        return turns

    def read_reply(self, body: dict) -> Reply:
        choice = read_first_choice(body)
        message = choice.get("message") if isinstance(choice.get("message"), dict) else {}
        calls = _read_tool_calls(message.get("tool_calls"))
        text = message.get("content") if isinstance(message.get("content"), str) else ""
        return _make_reply(text, calls, choice.get("finish_reason"), body.get("usage"))

    def read_stream(self, frames: list[SseFrame]) -> Reply:
        text: list[str] = []
        calls: dict[int, dict[str, Any]] = {}
        finish = usage = None
        for frame in frames:
            chunk = read_frame_json(frame)
            if chunk is None:
                continue
            if chunk.get("error"):
                finish = "error"
            usage = chunk.get("usage") or usage
            choice = read_first_choice(chunk)
            finish = choice.get("finish_reason") or finish
            delta = choice.get("delta") if isinstance(choice.get("delta"), dict) else {}
            if isinstance(delta.get("content"), str):
                text.append(delta["content"])
            for part in delta.get("tool_calls") or ():
                if not isinstance(part, dict):
                    continue
                call = calls.setdefault(int(part.get("index") or 0), {"name": "", "arguments": []})
                function = part.get("function") if isinstance(part.get("function"), dict) else {}
                call["name"] = call["name"] or function.get("name") or ""
                if isinstance(function.get("arguments"), str):
                    call["arguments"].append(function["arguments"])
        tool_calls = [ToolCall(call["name"], "".join(call["arguments"])) for _, call in sorted(calls.items())]
        return _make_reply("".join(text), tool_calls, finish, usage)



def _read_tool_calls(value: Any) -> list[ToolCall]:
    calls = []
    for call in value or ():
        function = call.get("function") if isinstance(call, dict) else None
        if isinstance(function, dict) and function.get("name"):
            arguments = function.get("arguments")
            calls.append(ToolCall(str(function["name"]), arguments if isinstance(arguments, str) else ""))
    return calls


def _make_reply(text: str, calls: list[ToolCall], finish: Any, usage: Any) -> Reply:
    usage = usage if isinstance(usage, dict) else {}
    output_tokens = read_count(usage.get("completion_tokens"))
    turn = make_turn("assistant", render_tool_calls(text, calls), tool_name=calls[0].name if calls else None,
                     tokens=output_tokens)  # fmt: skip
    return Reply(turns=[turn], finish_reason=str(finish) if finish else None,
                 input_tokens=read_count(usage.get("prompt_tokens")), output_tokens=output_tokens, tool_calls=calls)

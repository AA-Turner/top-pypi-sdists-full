"""
Conversation: a multi-turn chat that keeps its own message history — the agent loop's list, managed.

    conv = sequence_ai.Conversation("claude-opus-5-5", system="You plan robot tasks.", tools=TOOLS)
    r = conv.send("Put the red block in the bowl.")
    while r.tool_calls:                       # the model wants something run
        for call in r.tool_calls:
            conv.tool_result(call["id"], run_tool(call))
        r = conv.send()                       # continue with the tool results
    print(r.content, conv.cost_usd)

Each send() is one chat() call with the whole history; the reply (tool calls included) is appended
exactly as the model must see it on the next turn, which is the part callers most often get wrong
by hand. The system prompt and tool definitions are the same every turn, so with caching on (the
default) they are read from the prompt cache after the first turn - once they reach the model's
minimum cacheable length (see chat()); a reply's `warnings` says when they are shorter.
"""

from __future__ import annotations

import json
from typing import Any

from .._core.money import money
from .infer import chat
from .types import ChatResult, ChatStream


class Conversation:
    """A chat with memory. See the module docstring for the agent loop it is shaped around."""

    def __init__(
        self,
        model: Any,
        *,
        system: str | list[dict[str, Any]] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | dict[str, Any] | None = None,
        response_format: dict[str, Any] | None = None,
        max_tokens: int = 1024,
        temperature: float | None = None,
        cache: bool = True,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout_s: float | None = None,
    ) -> None:
        self.model = model
        self.messages: list[dict[str, Any]] = []
        if system is not None:
            self.messages.append({"role": "system", "content": system})

        self.turns: list[ChatResult] = []
        self._opts: dict[str, Any] = {
            "tools": tools, "tool_choice": tool_choice, "response_format": response_format,
            "max_tokens": max_tokens, "temperature": temperature, "cache": cache,
            "api_key": api_key, "base_url": base_url, "timeout_s": timeout_s,
        }

    def send(self, content: str | list[dict[str, Any]] | None = None, **overrides: Any) -> ChatResult:
        """Append a user turn (unless `content` is None — e.g. right after tool results), ask the
        model, append its reply, and return it. Keyword overrides apply to this turn only."""
        if content is not None:
            self.messages.append({"role": "user", "content": content})
        result = chat(self.model, self.messages, **{**self._opts, **overrides})
        self._record(result)
        return result

    def stream(self, content: str | list[dict[str, Any]] | None = None, **overrides: Any) -> ChatStream:
        """send(), streamed: iterate the returned ChatStream for text pieces. The reply is appended
        to the history when the stream completes (an abandoned stream appends nothing)."""
        if content is not None:
            self.messages.append({"role": "user", "content": content})
        s = chat(self.model, self.messages, **{**self._opts, **overrides, "stream": True})
        s._on_result = self._record
        return s

    def tool_result(self, tool_call_id: str, content: Any) -> None:
        """Append the result of one tool call. A non-string result is JSON-encoded, since a tool
        message's content is text."""
        text = content if isinstance(content, str) else json.dumps(content)
        self.messages.append({"role": "tool", "tool_call_id": tool_call_id, "content": text})

    def _record(self, result: ChatResult) -> None:


        turn: dict[str, Any] = {"role": "assistant", "content": result.content}
        if result.tool_calls:
            turn["tool_calls"] = result.tool_calls



        for key in ("reasoning", "reasoning_details"):
            if result.message.get(key):
                turn[key] = result.message[key]
        self.messages.append(turn)
        self.turns.append(result)

    @property
    def cost_usd(self) -> float:
        """Total charged across every turn so far."""
        return round(sum(t.cost_usd for t in self.turns), 8)

    @property
    def cached_tokens(self) -> int:
        """Total prompt tokens served from the prompt cache across every turn so far."""
        return sum(t.cached_tokens for t in self.turns)

    def __repr__(self) -> str:

        return (f"Conversation({len(self.messages)} messages, {len(self.turns)} turns, "
                f"{money(self.cost_usd)})")

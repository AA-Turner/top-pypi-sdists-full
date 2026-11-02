"""The chat (`/v1/chat`) wire types, as plain classes. Field names are the wire names verbatim."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import Any

from .._core.money import money
from .._core.warn import warn
from ..errors import InvalidRequest, Unavailable


@dataclass
class ChatResult:
    """
    One `/v1/chat` response. Field names are the wire names (schema.py ChatResponse).

    There is no `choices` wrapper: the gateway returns one message, so `result.message` is it
    rather than `result.choices[0].message`. The two convenience properties exist because the
    one thing a caller must branch on is whether the turn ended in prose or a tool call:
    `finish_reason == "tool_calls"` means `content` is likely None and `tool_calls` carries the
    ask, and reading `.content` blind there returns None with no hint why.


    `cost_usd` is what this call was charged — the model's own cost for the generation plus the
    platform margin — so an agent can budget per call without asking twice. A prompt-cache hit
    lowers it, because the charge follows the model's actual cost.
    """

    id: str
    model: str
    message: dict[str, Any]
    finish_reason: str
    usage: dict[str, Any] = field(default_factory=dict)
    perf: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    cost_usd: float = 0.0

    logprobs: dict[str, Any] | None = None

    @property
    def content(self) -> str | list[dict[str, Any]] | None:
        """The reply text (or content blocks). None when the turn ended in a tool call."""
        return self.message.get("content")

    @property
    def tool_calls(self) -> list[dict[str, Any]] | None:
        """Set when `finish_reason == "tool_calls"`; the calls the model wants run."""
        return self.message.get("tool_calls")

    @property
    def cached_tokens(self) -> int:
        """Prompt tokens read from the prompt cache on this call (0 when none, or not reported; 0 too
        when the prompt is shorter than the model's minimum cacheable length, which `warnings` then says)."""
        return int(self.usage.get("cached_tokens") or 0)

    @property
    def reasoning(self) -> str | None:
        """What the model thought before answering, as text — when the provider shows it."""
        return self.message.get("reasoning")

    @property
    def reasoning_details(self) -> list[dict[str, Any]] | None:
        """The reasoning as structured blocks (some signed); send them back on the next
        turn to keep a reasoning model's tool loop continuous — a Conversation does that for you."""
        return self.message.get("reasoning_details")

    @property
    def reasoning_tokens(self) -> int:
        """Output tokens spent reasoning on this call (billed as output, never shown as content)."""
        return int(self.usage.get("reasoning_tokens") or 0)

    def __repr__(self) -> str:
        cost = f", {money(self.cost_usd)}" if self.cost_usd else ""
        if self.finish_reason == "tool_calls":
            n = len(self.tool_calls or [])
            return f"ChatResult({n} tool call(s), {self.usage.get('total_tokens', '?')} tok{cost})"
        body = self.content if isinstance(self.content, str) else "<blocks>"
        clip = (body[:57] + "...") if isinstance(body, str) and len(body) > 60 else body
        return (f"ChatResult({clip!r}, {self.finish_reason}, "
                f"{self.usage.get('total_tokens', '?')} tok{cost})")


def result_from_wire(r: dict[str, Any], model_id: str) -> ChatResult:
    """A ChatResult from a `chat.response` body — the plain reply, or a stream's closing event."""
    from .._core.catalogue import _envelope

    env = _envelope(r, model_id)
    result = ChatResult(
        id=env["id"], model=env["model"], message=r.get("message") or {},
        finish_reason=r.get("finish_reason", ""), usage=env["usage"],
        perf=env["perf"], warnings=env["warnings"], cost_usd=float(r.get("cost_usd") or 0.0),
        logprobs=r.get("logprobs"),
    )



    if result.warnings and not result.content and not result.tool_calls:
        warn("; ".join(result.warnings))
    return result


class ChatStream:
    """
    A `chat(..., stream=True)` reply: iterate it for the text as it is generated, one piece at a
    time; after the loop `.result` is the complete ChatResult — the same object chat() returns
    without `stream=True`, with the full message (tool calls included), usage and cost_usd.

        stream = sequence_ai.chat("claude-opus-5-5", messages, stream=True)
        for piece in stream:
            print(piece, end="", flush=True)
        print(stream.result.cost_usd)

    Use it as a context manager, or call close(), to stop early and release the connection. A
    failure after the first piece (the provider broke mid-reply) raises during iteration — nothing
    is charged for a reply that did not finish; a refusal before the stream begins raises from
    chat() itself, with the same error types a plain call gets.
    """

    def __init__(self, events: Iterator[Any], model_id: str, close: Callable[[], None],
                 on_result: Callable[[ChatResult], None] | None = None) -> None:
        self.result: ChatResult | None = None
        self._pieces: list[str] = []

        self._thought: list[str] = []
        self._close = close
        self._on_result = on_result
        self._gen = self._run(events, model_id)

    def _run(self, events: Iterator[Any], model_id: str) -> Iterator[str]:
        try:
            for ev in events:
                if ev == "[DONE]":
                    break
                kind = ev.get("object") if isinstance(ev, dict) else None
                if kind == "chat.chunk":
                    delta = ev.get("delta") or {}
                    if delta.get("reasoning"):
                        self._thought.append(delta["reasoning"])
                    piece = delta.get("content") or ""
                    if piece:
                        self._pieces.append(piece)
                        yield piece
                elif kind == "chat.response":
                    self.result = result_from_wire(ev, model_id)
                    if self._on_result is not None:
                        self._on_result(self.result)
                elif kind == "error":
                    err = ev.get("error") or {}
                    status = err.get("status")
                    msg = err.get("message") or "the reply failed mid-stream"

                    if status == 400:
                        raise InvalidRequest(msg, status=status)
                    raise Unavailable(msg, status=status)
            if self.result is None:
                raise Unavailable("the stream ended without a final response")
        finally:

            closer = getattr(events, "close", None)
            if callable(closer):
                closer()
            self._close()

    def __iter__(self) -> ChatStream:
        return self

    def __next__(self) -> str:
        return next(self._gen)

    @property
    def text(self) -> str:
        """Everything received so far (the whole reply once the loop has finished)."""
        return "".join(self._pieces)

    @property
    def reasoning(self) -> str:
        """The reasoning text received so far, when the model shows it (iteration yields only the reply)."""
        return "".join(self._thought)

    def close(self) -> None:
        """Stop reading and release the connection. Safe to call more than once, and before the
        first piece: a generator closed before it started never runs its cleanup, so the transport
        is closed here as well (closing it twice is harmless)."""
        self._gen.close()
        self._close()

    def __enter__(self) -> ChatStream:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

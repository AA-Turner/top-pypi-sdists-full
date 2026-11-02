"""
chat: one `/v1/chat` turn, as a one-shot call — or a stream of it.

In one sentence:
`chat()` sends OpenAI-shaped messages and returns one message (or, with `stream=True`, a
ChatStream that yields the text as it is generated), building the exact wire body the gateway's
`extra="forbid"` schema accepts and resolving the model against the shared catalogue.

Upstream trigger  - a caller, once per request (unlike act, there is no loop here)
Downstream effect - POST /v1/chat, or a local InvalidRequest naming the mismatch

WHY this is a function and not a Policy: act keeps a connection open and a buffer full because a
robot consumes actions continuously. Chat is request/response — a message in, a message out. A
class with a lifecycle would be ceremony over a single POST. (Conversation, in conversation.py,
is the optional multi-turn helper on top of this function, for agents.)
"""

from __future__ import annotations

from typing import Any

from .._core.catalogue import _resolve
from .._core.transport import Transport
from ..errors import InvalidRequest
from .types import ChatResult, ChatStream, result_from_wire


def chat(
    model: Any,
    messages: list[dict[str, Any]],
    *,
    max_tokens: int = 1024,
    temperature: float | None = None,
    tools: list[dict[str, Any]] | None = None,
    tool_choice: str | dict[str, Any] | None = None,
    response_format: dict[str, Any] | None = None,
    cache: bool = True,
    stream: bool = False,
    reasoning: dict[str, Any] | None = None,
    include_reasoning: bool | None = None,
    reasoning_effort: str | None = None,
    max_completion_tokens: int | None = None,
    seed: int | None = None,
    stop: str | list[str] | None = None,
    top_p: float | None = None,
    top_k: int | None = None,
    min_p: float | None = None,
    top_a: float | None = None,
    frequency_penalty: float | None = None,
    presence_penalty: float | None = None,
    repetition_penalty: float | None = None,
    logit_bias: dict[str, float] | None = None,
    logprobs: bool | None = None,
    top_logprobs: int | None = None,
    parallel_tool_calls: bool | None = None,
    verbosity: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout_s: float | None = None,
) -> ChatResult | ChatStream:
    """
    One `/v1/chat` turn: messages in, one message out.

    `messages` is the OpenAI-shaped list — `[{"role": "user", "content": "..."}]`. For a model that
    takes images, use a content block list and build the image block with `sequence_ai.image(...)`
    (a file path, bytes, a PIL image or numpy array): `content=[{"type": "text", "text": "..."},
    sequence_ai.image("frame.jpg")]`. That produces the `{"type": "image_url", ...}` block with an
    inline data URI — the only image form the gateway accepts (it never fetches URLs). Which models
    accept images is the provider's business, so the SDK does not gate it.

    - `tools` / `tool_choice` — functions the model may call; `tool_choice` is "auto" | "none" |
      "required" or `{"type": "function", "function": {"name": ...}}` to force one. The model
      returns the call; you run it (see `ChatResult.tool_calls`).
    - `response_format` — structured output: `{"type": "json_object"}` or
      `{"type": "json_schema", "json_schema": {"name": ..., "schema": {...}}}`.
    - `cache` — on by default: your system prompt (and tool definitions) is cached so later turns
      read it at a fraction of the input price; `ChatResult.cached_tokens` shows the hit. Mark more
      with `sequence_ai.cached(text)`. `cache=False` opts out. A model caches only a prefix of at
      least its own minimum length (each model's minimum: https://generalsequences.com/docs/python/#chat);
      a shorter one is processed with nothing cached, and `ChatResult.warnings` says so.
    - `stream=True` returns a ChatStream: iterate it for text pieces; `.result` afterwards is the
      full ChatResult, `cost_usd` included.
    - `reasoning` — how much the model thinks before it answers:
      `{"effort": "max"|"xhigh"|"high"|"medium"|"low"|"minimal"|"none", "max_tokens": n,
      "exclude": bool, "enabled": bool}`. Reasoning tokens are output tokens: they are billed and
      count against `max_tokens`, so a small `max_tokens` can be spent before the model answers —
      the result then has empty content, `finish_reason="length"` and a warning. Raise `max_tokens`
      or use `{"effort": "minimal"}`; "none" works only on a model that lets reasoning be turned off
      (most reasoning models refuse it). Not set: the model's own default. The reply's
      `.reasoning` / `.reasoning_details` carry what it thought; a Conversation sends them back.
    - The other model parameters — `include_reasoning`, `reasoning_effort`,
      `max_completion_tokens`, `seed`, `stop`, `top_p`, `top_k`, `min_p`, `top_a`, `frequency_penalty`,
      `presence_penalty`, `repetition_penalty`, `logit_bias`, `logprobs` (returned on
      `.logprobs`), `top_logprobs`, `parallel_tool_calls`, `verbosity` — are sent as given, under
      their usual names and meanings; which ones a model takes is its `supported_parameters` in
      `models()`. Left as None they are not sent.

    Every result carries `cost_usd`, what the call was charged. No cold-start wait: chat is answered
    by an external provider. A refused call is not billed: a request the provider rejects (a value
    out of range, an image it cannot read, a prompt longer than the model's context) raises
    InvalidRequest with the provider's own words; Unavailable means the provider returned an error
    (502 — retry once, then report) or is rate limited or unreachable (503 — `retry_after_s` when
    known). Neither is retried for you. Every call opens its own connection.
    """
    m = _resolve(model, api_key, base_url, "chat")
    if m.endpoint != "chat":
        raise InvalidRequest(
            f"{m.short_id} is a {m.endpoint!r} model; chat() needs a chat model. "
            f"See models(endpoint='chat')."
        )
    if not messages:
        raise InvalidRequest("chat() needs at least one message")
    if len(messages) > 256:
        raise InvalidRequest(f"chat() allows up to 256 messages, got {len(messages)}")



    body: dict[str, Any] = {"model": m.id, "messages": messages, "max_tokens": max_tokens}
    if temperature is not None:
        body["temperature"] = temperature
    if tools is not None:
        body["tools"] = tools
    if tool_choice is not None:
        body["tool_choice"] = tool_choice
    if response_format is not None:
        body["response_format"] = response_format
    if not cache:
        body["cache"] = False
    if stream:
        body["stream"] = True


    for name, value in (("reasoning", reasoning), ("include_reasoning", include_reasoning),
                        ("reasoning_effort", reasoning_effort),
                        ("max_completion_tokens", max_completion_tokens), ("seed", seed), ("stop", stop),
                        ("top_p", top_p), ("top_k", top_k), ("min_p", min_p), ("top_a", top_a),
                        ("frequency_penalty", frequency_penalty), ("presence_penalty", presence_penalty),
                        ("repetition_penalty", repetition_penalty), ("logit_bias", logit_bias),
                        ("logprobs", logprobs), ("top_logprobs", top_logprobs),
                        ("parallel_tool_calls", parallel_tool_calls), ("verbosity", verbosity)):
        if value is not None:
            body[name] = value

    t = Transport(api_key=api_key, base_url=base_url, timeout_s=timeout_s)
    if stream:


        try:
            events = t.post_sse("/v1/chat", body, timeout_s=timeout_s)
        except Exception:
            t.close()
            raise
        return ChatStream(events, m.id, close=t.close)
    try:
        r = t.post("/v1/chat", body, timeout_s=timeout_s)
    finally:
        t.close()
    return result_from_wire(r, m.id)

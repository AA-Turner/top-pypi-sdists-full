"""Prebuilt ``finalize`` helpers for ``@client.span(finalize=...)``.

A streaming function (an ``async def`` that yields LLM chunks) hands each chunk
to the caller as it arrives; the span records a serializable summary instead of
the raw chunks. These helpers receive the **list of yielded chunks** collected
by the async-generator span path and assemble a replayable ``dict``.

They are duck-typed: no hard dependency on ``openai`` / ``anthropic``, so they
work across SDK versions and on plain dict chunks alike.

Example::

    from bitfab import finalizers


    @client.span("chat", type="llm", finalize=finalizers.openai_chunks)
    async def chat(messages):
        stream = await client.chat.completions.create(
            model="gpt-4o", messages=messages, stream=True
        )
        async for chunk in stream:
            yield chunk
"""

from typing import Any, Optional


def _get(obj: Any, *names: str) -> Any:
    """Read the first present attribute/key from ``names`` on ``obj``."""
    for name in names:
        if isinstance(obj, dict):
            if name in obj:
                return obj[name]
        elif hasattr(obj, name):
            return getattr(obj, name)
    return None


def _to_plain(obj: Any) -> Any:
    """Best-effort convert a pydantic/SDK object to a plain serializable value."""
    if obj is None or isinstance(obj, (str, int, float, bool, dict, list)):
        return obj
    for attr in ("model_dump", "dict"):
        method = getattr(obj, attr, None)
        if callable(method):
            try:
                return method()
            except Exception:
                pass
    return obj


def openai_chunks(chunks: list[Any]) -> dict[str, Any]:
    """Assemble OpenAI streaming ``ChatCompletionChunk``s into a span output.

    Returns ``{text, finish_reason, usage, tool_calls}``. ``usage`` is present
    only when the request set ``stream_options={"include_usage": True}``.
    Never raises on a malformed chunk; unknown shapes contribute nothing.
    """
    text_parts: list[str] = []
    finish_reason: Optional[Any] = None
    usage: Any = None
    tool_calls: dict[int, dict[str, Any]] = {}

    for chunk in chunks or []:
        choices = _get(chunk, "choices") or []
        if choices:
            choice = choices[0]
            delta = _get(choice, "delta")
            if delta is not None:
                content = _get(delta, "content")
                if content:
                    text_parts.append(content)
                for tc in _get(delta, "tool_calls") or []:
                    index = _get(tc, "index") or 0
                    slot = tool_calls.setdefault(index, {"name": None, "arguments": ""})
                    fn = _get(tc, "function")
                    if fn is not None:
                        name = _get(fn, "name")
                        if name:
                            slot["name"] = name
                        arguments = _get(fn, "arguments")
                        if arguments:
                            slot["arguments"] += arguments
            reason = _get(choice, "finish_reason")
            if reason:
                finish_reason = reason
        chunk_usage = _get(chunk, "usage")
        if chunk_usage is not None:
            usage = _to_plain(chunk_usage)

    return {
        "text": "".join(text_parts),
        "finish_reason": finish_reason,
        "usage": usage,
        "tool_calls": [tool_calls[k] for k in sorted(tool_calls)] or None,
    }


def anthropic_events(events: list[Any]) -> dict[str, Any]:
    """Assemble Anthropic streaming events into a span output.

    Returns ``{text, stop_reason, usage}`` by reading ``content_block_delta``,
    ``message_delta``, and ``message_start`` events. Never raises on an
    unexpected event shape.
    """
    text_parts: list[str] = []
    stop_reason: Optional[Any] = None
    usage: dict[str, Any] = {}

    for event in events or []:
        event_type = _get(event, "type")
        if event_type == "content_block_delta":
            delta = _get(event, "delta")
            text = _get(delta, "text") if delta is not None else None
            if text:
                text_parts.append(text)
        elif event_type == "message_delta":
            delta = _get(event, "delta")
            reason = _get(delta, "stop_reason") if delta is not None else None
            if reason:
                stop_reason = reason
            event_usage = _to_plain(_get(event, "usage"))
            if isinstance(event_usage, dict):
                usage.update(event_usage)
        elif event_type == "message_start":
            message = _get(event, "message")
            message_usage = _to_plain(_get(message, "usage")) if message else None
            if isinstance(message_usage, dict):
                usage.update(message_usage)

    return {
        "text": "".join(text_parts),
        "stop_reason": stop_reason,
        "usage": usage or None,
    }

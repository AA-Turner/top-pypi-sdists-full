"""Tracing wrapper for the Cohere client.

`wrap_cohere` patches `generate`, `chat`, `embed`, `rerank` and `chat_stream`
on the client the customer built, emits one finalized span per call, and
otherwise leaves the call alone - same arguments, same return value, same
exceptions.

The four non-streaming methods differ only in what they read off a request and
a response, so they are a table (`_METHODS`) over one traced body rather than
four near-identical closures.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from aigie.cost_tracking import extract_and_calculate_cost
from aigie.wrappers._base import (
    contained,
    new_provider_run_context,
    opening_stream,
    traced_provider_call,
)
from aigie.wrappers._client_patch import bind_options, patch_method, unpatch_all
from aigie.wrappers._stream import TracedStream

logger = logging.getLogger(__name__)

_PROVIDER = "cohere"

# Constant, not built per call: this reaches `logger.debug` on a per-span path,
# where an f-string would be formatted whether or not debug is on.
_READING = "reading the Cohere response"


@dataclass(frozen=True)
class _Method:
    """How one Cohere method maps onto a span."""

    attribute: str
    span_type: str
    default_model: str
    span_input: Callable[[dict], Any]
    request_meta: Callable[[dict], dict]
    record: Callable[[Any, Any], None]


def wrap_cohere(
    client: Any,
    name: str | None = None,
    metadata: dict[str, Any] | None = None,
    tags: list[str] | None = None,
) -> Any:
    """
    Wrap Cohere client for automatic tracing

    Args:
        client: Cohere client instance
        name: Optional span name
        metadata: Additional metadata
        tags: Tags to apply

    Returns:
        The same client, with its API methods traced. Returned untouched if no
        Aigie client has been initialized.

    Example:
        >>> import cohere
        >>> from aigie.wrappers import wrap_cohere
        >>>
        >>> co = cohere.Client(api_key='your-api-key')
        >>> traced_co = wrap_cohere(co)
        >>>
        >>> response = traced_co.generate(
        ...     model='command',
        ...     prompt='Hello!'
        ... )
    """
    from aigie.client import get_aigie

    if get_aigie() is None:
        logger.debug("[wrapper] No Aigie client - returning the Cohere client untraced")
        return client

    for spec in _METHODS:
        patch_method(
            client,
            spec.attribute,
            bind_options(_traced_method, spec, name, metadata, tags),
        )
    patch_method(client, "chat_stream", bind_options(_chat_stream, name, metadata, tags))
    return client


def unwrap_cohere(client: Any) -> bool:
    """Restore the client's own methods. True if anything was restored.

    `wrap_cohere` patches an object the customer owns, so it ships the way to
    undo that - a customer proving the SDK is their problem has to be able to
    turn it off without rebuilding their client.
    """
    return unpatch_all(client, _TRACED_METHODS)


def _traced_method(
    original: Callable,
    spec: _Method,
    name: str | None,
    metadata: dict[str, Any] | None,
    tags: list[str] | None,
) -> Callable:
    """Build the traced replacement for one non-streaming Cohere method."""

    def traced(*args: Any, **kwargs: Any) -> Any:
        model = kwargs.get("model", spec.default_model)
        run_ctx = new_provider_run_context(
            name or f"cohere:{spec.attribute}:{model}",
            span_type=spec.span_type,
            metadata={
                **(metadata or {}),
                "model": model,
                "provider": _PROVIDER,
                **spec.request_meta(kwargs),
            },
            tags=[*(tags or []), _PROVIDER, spec.attribute],
        )
        run_ctx.metadata["input"] = spec.span_input(kwargs)

        with traced_provider_call(run_ctx):
            response = original(*args, **kwargs)
            contained(_READING, spec.record, run_ctx, response)
            return response

    return traced


def _chat_stream(
    original: Callable,
    name: str | None,
    metadata: dict[str, Any] | None,
    tags: list[str] | None,
) -> Callable:
    """Build the traced replacement for `chat_stream`.

    Stays a *synchronous* generator, because that is what Cohere returns. The
    version this replaced was an async generator, so `for event in
    co.chat_stream(...)` raised `TypeError` on a wrapped client.
    """

    def traced_chat_stream(*args: Any, **kwargs: Any) -> Any:
        model = kwargs.get("model", "command")
        run_ctx = new_provider_run_context(
            name or f"cohere:chat:{model}",
            span_type="llm",
            metadata={
                **(metadata or {}),
                "model": model,
                "provider": _PROVIDER,
                "streaming": True,
                "conversationId": kwargs.get("conversation_id"),
            },
            tags=[*(tags or []), _PROVIDER, "chat", "streaming"],
        )
        run_ctx.metadata["input"] = kwargs.get("message") or kwargs.get("chat_history")

        with opening_stream(run_ctx):
            events = original(*args, **kwargs)

        collector = _CohereCollector(run_ctx)
        return TracedStream(run_ctx, events, collect=collector.collect, finish=collector.finish)

    return traced_chat_stream


class _CohereCollector:
    """Accumulates a Cohere chat stream into the span it belongs to."""

    def __init__(self, run_ctx: Any) -> None:
        self._run_ctx = run_ctx
        # A list, not `self._text += ...`: in-place concat has no fast path for an
        # instance attribute, so appending per chunk is O(n) instead of O(n^2).
        self._parts: list[str] = []
        self._conversation_id: Any = None
        self._finish_reason: Any = None
        self._response: Any = None

    def collect(self, event: Any) -> None:
        event_type = getattr(event, "event_type", None)
        if event_type == "text-generation":
            self._parts.append(getattr(event, "text", "") or "")
        elif event_type == "stream-end":
            self._response = getattr(event, "response", None)
            self._conversation_id = getattr(self._response, "conversation_id", None)
            self._finish_reason = getattr(event, "finish_reason", None)

    def finish(self) -> None:
        self._run_ctx.metadata["output"] = "".join(self._parts)
        self._run_ctx.metadata["conversationId"] = self._conversation_id
        self._run_ctx.metadata["finishReason"] = self._finish_reason
        if self._response is not None:
            _record_usage(self._run_ctx, self._response)


def _record_generate(run_ctx: Any, response: Any) -> None:
    """Read a `generate` response onto the span."""
    generations = getattr(response, "generations", None) or []
    first = generations[0] if generations else None
    run_ctx.metadata["output"] = getattr(first, "text", None)
    run_ctx.metadata["generationId"] = getattr(response, "id", None)
    run_ctx.metadata["finishReason"] = getattr(first, "finish_reason", None)
    _record_usage(run_ctx, response)


def _chat_text(response: Any) -> Any:
    """The assistant's reply, across Cohere's two client generations.

    `Client.chat` puts it on `response.text`; `ClientV2.chat` returns content
    blocks under `response.message.content`. Reading only the first records
    `None` for the other, and records it silently.
    """
    text = getattr(response, "text", None)
    if text is not None:
        return text

    content = getattr(getattr(response, "message", None), "content", None) or []
    joined = "".join(getattr(block, "text", "") or "" for block in content)
    return joined or None


def _record_chat(run_ctx: Any, response: Any) -> None:
    """Read a `chat` response onto the span."""
    run_ctx.metadata["output"] = _chat_text(response)
    run_ctx.metadata["conversationId"] = getattr(response, "conversation_id", None)
    run_ctx.metadata["generationId"] = getattr(response, "generation_id", None)
    run_ctx.metadata["finishReason"] = getattr(response, "finish_reason", None)
    run_ctx.metadata["citations"] = _count(response, "citations")
    run_ctx.metadata["documents"] = _count(response, "documents")
    _record_usage(run_ctx, response)


def _record_embed(run_ctx: Any, response: Any) -> None:
    """Read an `embed` response onto the span - shapes, never the vectors.

    `embeddings` is a list on the default path but an object when the caller
    passes `embedding_types=`, so the shape is recorded only when it is one.
    """
    _record_usage(run_ctx, response)

    embeddings = getattr(response, "embeddings", None) or []
    if not isinstance(embeddings, list):
        logger.debug("[wrapper] Cohere returned embeddings by type - recording no shape")
        return
    run_ctx.metadata["output"] = {
        "embeddings": len(embeddings),
        "dimensions": len(embeddings[0]) if embeddings else 0,
    }


def _record_rerank(run_ctx: Any, response: Any) -> None:
    """Read a `rerank` response onto the span.

    The top result travels as its index, not as the Cohere object itself: the
    payload has to survive JSON serialization, and the object does not.
    """
    results = getattr(response, "results", None) or []
    run_ctx.metadata["output"] = {
        "results": len(results),
        "topResultIndex": getattr(results[0], "index", None) if results else None,
    }


def _count(response: Any, attribute: str) -> int:
    """How many of `attribute` a response carries, 0 when it carries none."""
    value = getattr(response, attribute, None)
    return len(value) if value else 0


def _units_under(response: Any, holder: str) -> Any:
    """The `billed_units` hanging off one holder attribute, if it is there."""
    container = getattr(response, holder, None)
    if container is None and isinstance(response, dict):
        container = response.get(holder)

    units = getattr(container, "billed_units", None)
    if units is None and isinstance(container, dict):
        units = container.get("billed_units")
    return units


def _unit(units: Any, field: str) -> Any:
    """One token count, whether `billed_units` is an object or a dict."""
    if isinstance(units, dict):
        return units.get(field)
    return getattr(units, field, None)


def _billed_units(response: Any) -> tuple[int, int] | None:
    """Cohere's token counts, across both client generations and both shapes.

    `Client` hangs `billed_units` off `response.meta`; `ClientV2` hangs it off
    `response.usage`. Either can arrive as an object or a dict.
    """
    units = _units_under(response, "meta") or _units_under(response, "usage")
    if units is None:
        return None

    prompt = _unit(units, "input_tokens")
    completion = _unit(units, "output_tokens")
    if prompt is None and completion is None:
        return None
    return int(prompt or 0), int(completion or 0)


def _record_usage(run_ctx: Any, response: Any) -> None:
    """Record token counts and cost, when the response reports any."""
    counts = _billed_units(response)
    if counts is None:
        return

    prompt, completion = counts
    usage = {
        "prompt_tokens": prompt,
        "completion_tokens": completion,
        "total_tokens": prompt + completion,
    }
    run_ctx.metadata["usage"] = usage
    contained("pricing the Cohere call", _record_cost, run_ctx, usage)


def _record_cost(run_ctx: Any, usage: dict[str, int]) -> None:
    """Price the call from its token counts, if the model has a price."""
    model = run_ctx.metadata.get("model")
    cost = extract_and_calculate_cost(
        {
            "meta": {
                "billed_units": {
                    "input_tokens": usage["prompt_tokens"],
                    "output_tokens": usage["completion_tokens"],
                }
            },
            "model": model,
        },
        _PROVIDER,
        model_override=model,
    )
    if not cost:
        logger.debug("[wrapper] No Cohere price for model %s", model)
        return

    run_ctx.metadata["cost"] = {
        "input_cost": float(cost.input_cost),
        "output_cost": float(cost.output_cost),
        "total_cost": float(cost.total_cost),
        "currency": cost.currency,
    }


_METHODS: tuple[_Method, ...] = (
    _Method(
        attribute="generate",
        span_type="llm",
        default_model="command",
        span_input=lambda kwargs: kwargs.get("prompt"),
        request_meta=lambda kwargs: {
            "maxTokens": kwargs.get("max_tokens"),
            "temperature": kwargs.get("temperature"),
        },
        record=_record_generate,
    ),
    _Method(
        attribute="chat",
        span_type="llm",
        default_model="command",
        span_input=lambda kwargs: kwargs.get("message") or kwargs.get("chat_history"),
        request_meta=lambda kwargs: {
            "conversationId": kwargs.get("conversation_id"),
            "searchQueriesOnly": kwargs.get("search_queries_only"),
        },
        record=_record_chat,
    ),
    _Method(
        attribute="embed",
        span_type="embedding",
        default_model="embed-english-v3.0",
        span_input=lambda kwargs: kwargs.get("texts"),
        request_meta=lambda kwargs: {
            "inputType": kwargs.get("input_type"),
            "truncate": kwargs.get("truncate"),
        },
        record=_record_embed,
    ),
    _Method(
        attribute="rerank",
        span_type="chain",
        default_model="rerank-english-v3.0",
        span_input=lambda kwargs: {
            "query": kwargs.get("query"),
            "documentCount": len(kwargs.get("documents") or []),
        },
        request_meta=lambda kwargs: {
            "topN": kwargs.get("top_n"),
            "returnDocuments": kwargs.get("return_documents"),
        },
        record=_record_rerank,
    ),
)

# Derived, not restated: a new `_METHODS` row that `unwrap_cohere` did not know
# about would leave a patched method installed forever.
_TRACED_METHODS: tuple[str, ...] = (*(spec.attribute for spec in _METHODS), "chat_stream")


def create_traced_cohere(
    api_key: str,
    name: str | None = None,
    metadata: dict[str, Any] | None = None,
    tags: list[str] | None = None,
) -> Any:
    """
    Create traced Cohere client

    Args:
        api_key: Cohere API key
        name: Optional span name
        metadata: Additional metadata
        tags: Tags to apply

    Returns:
        Traced Cohere client

    Example:
        >>> from aigie.wrappers import create_traced_cohere
        >>>
        >>> client = create_traced_cohere(api_key='your-api-key')
    """
    try:
        import cohere

        client = cohere.Client(api_key=api_key)

        return wrap_cohere(client, name=name, metadata=metadata, tags=tags)

    except ImportError as err:
        raise ImportError("cohere not found. Install with: pip install cohere") from err

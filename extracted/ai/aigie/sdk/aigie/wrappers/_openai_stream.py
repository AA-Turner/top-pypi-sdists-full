"""Streaming support for the OpenAI wrapper.

The async and sync wrappers do identical work over different iteration
protocols, so collection, aggregation and the metric maths live here once and
each generator stays a thin loop.

Both generators emit their span from a `finally`, which is the *second* span for
a streamed call: the handler already emitted one when it returned the generator,
before any chunk was read. That is inherited behaviour, preserved deliberately —
changing it would change what the dashboard shows for every streamed call.
"""

from __future__ import annotations

import logging
import time
from collections.abc import AsyncIterator, Iterator
from dataclasses import dataclass, field
from typing import Any

from aigie.context_manager import RunContext, get_current_trace_context
from aigie.wrappers._base import (
    queue_llm_span_event,
    queue_llm_span_event_sync,
    record_error,
)

logger = logging.getLogger(__name__)

# Rough conversion used only when the provider reports no token count.
_CHARS_PER_TOKEN = 4


def chunk_total_tokens(chunk: Any, running_total: int) -> int:
    """Token total carried by a chunk, or the running total if it carries none."""
    usage = getattr(chunk, "usage", None)
    if not usage:
        return running_total
    if hasattr(usage, "total_tokens"):
        reported: int = usage.total_tokens
        return reported
    if isinstance(usage, dict):
        from_dict: int = usage.get("total_tokens", 0)
        return from_dict
    return running_total


def aggregate_content(chunks: list) -> str:
    """Concatenate the delta content of every chunk."""
    full_content = ""
    for chunk in chunks:
        if hasattr(chunk, "choices") and len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                full_content += delta.content
    return full_content


def streaming_metrics(
    run_ctx: RunContext,
    *,
    chunk_count: int,
    first_chunk_time: float | None,
    last_chunk_time: float | None,
    total_tokens: int,
    full_content: str,
) -> dict:
    """Time-to-first-token, duration and throughput for one streamed call."""
    metrics: dict[str, Any] = {}
    if not (first_chunk_time and last_chunk_time and run_ctx.start_time):
        return metrics

    duration_ms = (last_chunk_time - first_chunk_time) * 1000
    metrics["time_to_first_token_ms"] = (first_chunk_time - run_ctx.start_time.timestamp()) * 1000
    metrics["streaming_duration_ms"] = duration_ms
    metrics["chunk_count"] = chunk_count

    if total_tokens > 0 and duration_ms > 0:
        metrics["tokens_per_second"] = (total_tokens / duration_ms) * 1000
    elif duration_ms > 0:
        estimated_tokens = len(full_content) / _CHARS_PER_TOKEN
        metrics["estimated_tokens_per_second"] = (estimated_tokens / duration_ms) * 1000

    return metrics


def record_stream_result(
    run_ctx: RunContext,
    *,
    chunk_count: int,
    full_content: str,
    total_tokens: int,
    metrics: dict,
) -> None:
    """Stamp the finished stream onto the span."""
    if total_tokens > 0:
        run_ctx.metadata["usage"] = {"total_tokens": total_tokens}

    run_ctx.metadata["output"] = {"content": full_content}
    run_ctx.metadata["stream_chunks"] = chunk_count
    run_ctx.metadata["streaming"] = True
    if metrics:
        run_ctx.metadata["streaming_metrics"] = metrics
    run_ctx.metadata["status"] = "success"


async def _post_call_for_stream(
    interception_ctx: Any, full_content: str, total_tokens: int
) -> None:
    """Post-call interception for a stream, which has no single response object."""
    try:
        from aigie.client import get_aigie

        aigie = get_aigie()
        if aigie and aigie._interceptor_chain:
            interception_ctx.response_content = full_content
            if total_tokens > 0:
                interception_ctx.actual_output_tokens = total_tokens
            await aigie.intercept_post_call(ctx=interception_ctx, response=None, error=None)
    except Exception as intercept_error:
        logger.debug("[wrapper] Stream post-call interception failed: %s", intercept_error)


@dataclass
class _StreamCollector:
    """Running state for one streamed call."""

    chunks: list = field(default_factory=list)
    first_chunk_time: float | None = None
    last_chunk_time: float | None = None
    total_tokens: int = 0

    def mark(self, chunk: Any) -> None:
        """Timestamp and keep a chunk, before the caller receives it."""
        if self.first_chunk_time is None:
            self.first_chunk_time = time.time()
        self.last_chunk_time = time.time()
        self.chunks.append(chunk)

    def count_tokens(self, chunk: Any) -> None:
        """Update the running token total, after the caller has taken the chunk."""
        self.total_tokens = chunk_total_tokens(chunk, self.total_tokens)

    def finish(self, run_ctx: RunContext) -> str:
        """Aggregate, measure and stamp the span. Returns the full text."""
        full_content = aggregate_content(self.chunks)
        metrics = streaming_metrics(
            run_ctx,
            chunk_count=len(self.chunks),
            first_chunk_time=self.first_chunk_time,
            last_chunk_time=self.last_chunk_time,
            total_tokens=self.total_tokens,
            full_content=full_content,
        )
        record_stream_result(
            run_ctx,
            chunk_count=len(self.chunks),
            full_content=full_content,
            total_tokens=self.total_tokens,
            metrics=metrics,
        )
        return full_content


async def wrap_stream_async(
    stream: AsyncIterator, run_ctx: RunContext, interception_ctx: Any = None
) -> AsyncIterator:
    """Yield every chunk untouched, collecting metrics as they pass."""
    collected = _StreamCollector()
    trace_ctx = get_current_trace_context()

    try:
        async for chunk in stream:
            collected.mark(chunk)
            yield chunk
            collected.count_tokens(chunk)

        full_content = collected.finish(run_ctx)
        if interception_ctx:
            await _post_call_for_stream(interception_ctx, full_content, collected.total_tokens)

    except Exception as e:
        record_error(run_ctx, e)
        raise

    finally:
        await queue_llm_span_event(run_ctx, trace_ctx.id if trace_ctx else run_ctx.id)


def wrap_stream_sync(
    stream: Iterator, run_ctx: RunContext, interception_ctx: Any = None
) -> Iterator:
    """Sync twin of `wrap_stream_async`.

    `interception_ctx` is accepted and ignored: the sync path has no awaitable
    interception chain to hand it to. Inherited, and kept so both wrappers take
    the same arguments.
    """
    collected = _StreamCollector()
    trace_ctx = get_current_trace_context()

    try:
        for chunk in stream:
            collected.mark(chunk)
            yield chunk
            collected.count_tokens(chunk)

        collected.finish(run_ctx)

    except Exception as e:
        record_error(run_ctx, e)
        raise

    finally:
        queue_llm_span_event_sync(run_ctx, trace_ctx.id if trace_ctx else run_ctx.id)

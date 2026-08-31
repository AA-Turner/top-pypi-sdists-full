"""Span plumbing shared by the provider wrappers.

Every provider wrapper runs the same sequence — build a span, call the provider,
measure the response, emit one finalized payload — and differs only in how it
reads a request and a response. This module owns the shared half so a provider
module is left with the vendor-specific half.

Two details are deliberately *not* unified, because the two emitters they came
from disagreed on them and reconciling that is a behaviour change, not a move:

- which cost fields count as "there is a cost" (`include_cost` at the call site)
- whether token totals are also stamped back into the span's metadata

Nothing here sets `framework`. That is an agent-framework concern, and a bare
provider call goes through no framework; `aigie.integrations` stamps it where
it is true.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from aigie.context_manager import (
    RunContext,
    get_current_span_context,
    get_current_trace_context,
    get_parent_context,
    set_current_span_context,
)

logger = logging.getLogger(__name__)


class _NoMatch:
    """Distinguishes "resolved to no system prompt" (which ends the search)
    from "not a system message" (which lets it continue)."""


_NO_MATCH = _NoMatch()


def _text_from_blocks(content: list) -> str | None:
    """Join the text of a content-block list, e.g. [{"type": "text", ...}]."""
    text_parts = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            text_parts.append(block.get("text", ""))
        elif isinstance(block, str):
            text_parts.append(block)
    return " ".join(text_parts) if text_parts else None


def _dict_system_content(msg: dict) -> str | None | _NoMatch:
    """System text of a dict message. Resolves content-block lists."""
    if msg.get("role", "") != "system":
        return _NO_MATCH

    content = msg.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return _text_from_blocks(content)
    return _NO_MATCH


def _object_system_content(msg: Any) -> str | None | _NoMatch:
    """System text of an object message. Plain strings only."""
    if getattr(msg, "role", None) != "system":
        return _NO_MATCH

    content = getattr(msg, "content", None)
    return content if isinstance(content, str) else _NO_MATCH


def _system_content(msg: Any) -> str | None | _NoMatch:
    """The system text of one message, or `_NO_MATCH` if it resolves none.

    Dict and object messages are not symmetric: a dict resolves a content-block
    list, an object only resolves a plain string. That asymmetry is inherited.
    """
    if isinstance(msg, dict):
        return _dict_system_content(msg)
    if hasattr(msg, "role"):
        return _object_system_content(msg)
    return _NO_MATCH


def extract_system_prompt(messages: list) -> str | None:
    """The first system prompt in a messages array, across provider formats."""
    if not messages:
        return None

    for msg in messages:
        resolved = _system_content(msg)
        if not isinstance(resolved, _NoMatch):
            return resolved

    return None


def update_trace_system_prompt(system_prompt: str) -> None:
    """Record the system prompt on the current trace, if it has none yet."""
    try:
        trace_ctx = get_current_trace_context()
        # The last clause never overwrites a system prompt the caller set.
        if (
            trace_ctx
            and hasattr(trace_ctx, "metadata")
            and "kytte.system_prompt" not in trace_ctx.metadata
        ):
            trace_ctx.metadata["kytte.system_prompt"] = system_prompt
            logger.debug(
                "[wrapper] Auto-extracted system prompt (%d chars) to trace metadata",
                len(system_prompt),
            )
    except Exception as e:
        logger.debug("[wrapper] Could not update trace with system prompt: %s", e)


def record_error(run_ctx: RunContext, error: BaseException) -> None:
    """Stamp a failed call onto the span. The exception itself still propagates."""
    run_ctx.metadata["error"] = {
        "type": type(error).__name__,
        "message": str(error),
    }
    run_ctx.metadata["status"] = "error"


def contained(what: str, action: Callable[..., Any], *args: Any) -> None:
    """Run one piece of *our* span bookkeeping so it cannot become the host's error.

    Instrumentation gets to lose a span; it does not get to replace somebody's
    exception.
    """
    try:
        action(*args)
    except Exception as e:  # noqa: BLE001 - a provider can raise anything
        logger.debug("[wrapper] %s failed: %s", what, e)


def new_provider_run_context(
    name: str,
    *,
    span_type: str,
    metadata: dict[str, Any],
    tags: list[str],
) -> RunContext:
    """Open a span for one provider call, parented to whatever is current."""
    parent_ctx = get_parent_context()
    trace_ctx = get_current_trace_context()
    run_ctx = RunContext(
        id=str(uuid4()),
        name=name,
        type="span",
        span_type=span_type,
        parent_id=parent_ctx.id if parent_ctx else (trace_ctx.id if trace_ctx else None),
        metadata=metadata,
        tags=tags,
        start_time=datetime.now(timezone.utc),
    )
    # Captured here, not read again at emit. A streamed span is emitted when
    # iteration ends, which is routinely a different thread - a framework's
    # threadpool draining a StreamingResponse - and the trace ContextVar does
    # not cross threads. Reading it there returns nothing and the span invents
    # a trace of its own while still naming a parent in the real one.
    run_ctx._aigie_trace_id = str(trace_ctx.id) if trace_ctx else None  # type: ignore[attr-defined]
    return run_ctx


def owning_trace_id(run_ctx: RunContext) -> str:
    """The trace this span belongs to, or itself when it is the whole story.

    Not `current_trace_id`: `tracing.trace_state` already exports that name with
    a different signature and a different answer when there is no trace.
    """
    captured = getattr(run_ctx, "_aigie_trace_id", None)
    if captured:
        return str(captured)
    trace_ctx = get_current_trace_context()
    return str(trace_ctx.id) if trace_ctx else run_ctx.id


def record_failure(run_ctx: RunContext, error: BaseException) -> None:
    """Stamp a failed provider call onto the span. Contained; never re-raises."""
    contained("recording the provider error", record_error, run_ctx, error)


def emit_span_now(run_ctx: RunContext) -> None:
    """Emit `run_ctx` as one finalized span. Contained; never re-raises.

    At most once per span, whoever calls. Two paths can both believe they own
    the close - a stream that was constructed and then dropped, and the caller
    that failed to install it - and a span emitted twice is a duplicate on the
    wire that the judge scores separately.
    """
    if getattr(run_ctx, "_aigie_emitted", False):
        return
    run_ctx._aigie_emitted = True  # type: ignore[attr-defined]
    contained(
        "emitting the span",
        queue_llm_span_event_sync,
        run_ctx,
        owning_trace_id(run_ctx),
    )


@contextmanager
def opening_stream(run_ctx: RunContext) -> Iterator[None]:
    """Guard the call that opens a provider stream.

    If it raises, the stream never existed and nothing downstream will close
    the span - so it is recorded and emitted here. The provider's exception
    propagates untouched.
    """
    try:
        yield
    except BaseException as error:
        record_failure(run_ctx, error)
        emit_span_now(run_ctx)
        raise


@contextmanager
def traced_provider_call(run_ctx: RunContext) -> Iterator[RunContext]:
    """Run one provider call inside `run_ctx`, emitting its span exactly once.

    The body records what came back onto `run_ctx.metadata`; this manager owns
    span context, status, failure capture and emission, all contained. The
    provider's exception propagates untouched.
    """
    previous = get_current_span_context()
    contained("entering the span context", set_current_span_context, run_ctx)
    try:
        yield run_ctx
    except BaseException as error:
        record_failure(run_ctx, error)
        raise
    else:
        # `setdefault`: a caller that already knows better keeps its status.
        run_ctx.metadata.setdefault("status", "success")
    finally:
        emit_span_now(run_ctx)
        contained("restoring the span context", set_current_span_context, previous)


@dataclass(frozen=True)
class SpanTotals:
    """Token counts and costs for one call, normalized across providers."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    input_cost: float = 0.0
    output_cost: float = 0.0
    total_cost: float = 0.0

    @property
    def has_tokens(self) -> bool:
        return self.prompt_tokens > 0 or self.completion_tokens > 0

    @property
    def has_any_cost(self) -> bool:
        return self.input_cost > 0 or self.output_cost > 0 or self.total_cost > 0

    @classmethod
    def from_usage_and_cost(
        cls,
        usage: dict | None,
        cost: dict | None,
        *,
        derive_total_tokens: bool,
    ) -> SpanTotals:
        """Build from a provider's usage/cost dicts.

        `derive_total_tokens` falls back to prompt + completion when the
        provider reported no total. Only some emitters did that, so it stays a
        decision the caller makes rather than a silent default.
        """
        usage = usage or {}
        cost = cost or {}
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        fallback_total = prompt_tokens + completion_tokens if derive_total_tokens else 0
        return cls(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=usage.get("total_tokens", fallback_total),
            input_cost=cost.get("input_cost", 0.0),
            output_cost=cost.get("output_cost", 0.0),
            total_cost=cost.get("total_cost", 0.0),
        )


def build_span_payload(
    run_ctx: RunContext,
    trace_id: str,
    *,
    span_input: Any,
    span_output: Any,
    end_time: datetime,
) -> dict:
    """The finalized span every provider emits, before totals and duration."""
    payload = {
        "id": run_ctx.id,
        "span_id": run_ctx.id,
        "trace_id": trace_id,
        "name": run_ctx.name,
        "type": run_ctx.span_type or "llm",
        "start_time": run_ctx.start_time.isoformat()
        if run_ctx.start_time
        else end_time.isoformat(),
        "end_time": end_time.isoformat(),
        "input": span_input,
        "output": span_output,
        "metadata": run_ctx.metadata,
        "status": run_ctx.metadata.get("status", "success"),
        "model": run_ctx.metadata.get("model"),
    }

    # Lets the backend re-parent the span if the trace root arrives separately.
    if run_ctx.parent_id and run_ctx.parent_id != trace_id:
        payload["parent_id"] = run_ctx.parent_id

    return payload


def _usage_block(totals: SpanTotals) -> dict:
    return {
        "input": totals.prompt_tokens,
        "output": totals.completion_tokens,
        "total": totals.total_tokens,
        "unit": "TOKENS",
        "input_cost": totals.input_cost if totals.input_cost > 0 else None,
        "output_cost": totals.output_cost if totals.output_cost > 0 else None,
        "total_cost": totals.total_cost if totals.total_cost > 0 else None,
    }


def _token_usage_block(totals: SpanTotals) -> dict:
    return {
        "prompt_tokens": totals.prompt_tokens,
        "completion_tokens": totals.completion_tokens,
        "total_tokens": totals.total_tokens,
        "input_cost": totals.input_cost if totals.input_cost > 0 else None,
        "output_cost": totals.output_cost if totals.output_cost > 0 else None,
        "total_cost": totals.total_cost if totals.total_cost > 0 else None,
    }


def apply_totals(payload: dict, totals: SpanTotals, *, include_cost: bool) -> None:
    """Add token, cost and nested usage fields, each under its own guard."""
    if totals.has_tokens:
        payload["prompt_tokens"] = totals.prompt_tokens
        payload["completion_tokens"] = totals.completion_tokens
        payload["total_tokens"] = totals.total_tokens

    if include_cost:
        payload["input_cost"] = totals.input_cost
        payload["output_cost"] = totals.output_cost
        payload["total_cost"] = totals.total_cost

    if totals.has_tokens or totals.total_cost > 0:
        payload["usage"] = _usage_block(totals)
        payload["token_usage"] = _token_usage_block(totals)


def stamp_totals_into_metadata(payload: dict, totals: SpanTotals) -> None:
    """Duplicate token/cost data into metadata for backend extraction."""
    meta = payload.get("metadata", {})
    if not isinstance(meta, dict) or not totals.has_tokens:
        return

    meta["token_usage"] = {
        "input_tokens": totals.prompt_tokens,
        "output_tokens": totals.completion_tokens,
        "total_tokens": totals.total_tokens,
        "unit": "TOKENS",
    }
    meta["prompt_tokens"] = totals.prompt_tokens
    meta["completion_tokens"] = totals.completion_tokens
    meta["total_tokens"] = totals.total_tokens

    if totals.total_cost > 0:
        meta["cost"] = totals.total_cost
        meta["estimated_cost"] = totals.total_cost
        meta["input_cost"] = totals.input_cost
        meta["output_cost"] = totals.output_cost
        meta["total_cost"] = totals.total_cost

    payload["metadata"] = meta


def apply_duration(
    payload: dict,
    run_ctx: RunContext,
    end_time: datetime,
    *,
    with_latency: bool = False,
) -> None:
    """Stamp elapsed time. `duration_ns` is the key the ingest mapper reads."""
    if not run_ctx.start_time:
        return

    elapsed = (end_time - run_ctx.start_time).total_seconds()
    payload["duration_ns"] = int(elapsed * 1e9)
    if with_latency:
        payload["latency_seconds"] = elapsed


def promote_metadata_fields(payload: dict, meta: dict) -> None:
    """Lift provider and framework out of metadata into top-level fields."""
    if "provider" in meta:
        payload["model_provider"] = meta["provider"]
    if "framework" in meta:
        payload["framework"] = meta["framework"]


async def queue_llm_span_event(run_ctx: RunContext, trace_id: str) -> None:
    """Emit one finalized LLM span, reading input/output/totals from metadata.

    Emitting is the SDK's problem, never the caller's: every failure here is
    logged and swallowed so a tracing fault cannot break a working LLM call.
    """
    try:
        from aigie.client import get_aigie

        aigie = get_aigie()
        if not aigie or not aigie._buffer:
            logger.debug("[wrapper] No global Aigie client - skipping LLM span event queue")
            return

        end_time = datetime.now(timezone.utc)
        meta = run_ctx.metadata
        totals = SpanTotals.from_usage_and_cost(
            meta.get("usage", {}), meta.get("cost", {}), derive_total_tokens=True
        )

        payload = build_span_payload(
            run_ctx,
            trace_id,
            span_input=meta.get("input"),
            span_output=meta.get("output"),
            end_time=end_time,
        )
        apply_totals(payload, totals, include_cost=totals.total_cost > 0)
        apply_duration(payload, run_ctx, end_time)
        promote_metadata_fields(payload, meta)

        await aigie._buffer.add(payload)
        logger.debug(
            "[wrapper] Queued LLM span event: %s (%s) -> trace:%s",
            run_ctx.name,
            run_ctx.id,
            trace_id,
        )

    except Exception as e:
        logger.debug("[wrapper] Failed to queue LLM span event: %s", e)


def queue_llm_span_event_sync(run_ctx: RunContext, trace_id: str) -> None:
    """Synchronously queue an LLM span event (schedules async operation)."""
    from aigie.utils.safe import schedule_async

    schedule_async(queue_llm_span_event(run_ctx, trace_id))

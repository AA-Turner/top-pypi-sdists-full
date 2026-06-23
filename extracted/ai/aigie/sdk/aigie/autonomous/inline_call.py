"""Inline call helpers — single retry path for LLM call sites.

These helpers wrap an LLM call (sync or async) in the autonomous retry
loop: when the call raises, the autonomous interceptor chain decides
whether to retry (e.g. via `RetryIntervention` returning
`PostCallResult.retry(...)`). When the chain's post-call result is
`RETRY`, the helper retries; otherwise the original exception is
re-raised.

Both helpers are no-ops when:
- `aigie` is None / uninitialized,
- `aigie.config.autonomous` is False,
- `ctx` (the InterceptionContext) is None — i.e. no pre-call was run.

These are the four call sites that should use these helpers:
- `aigie.wrappers._handle_messages_create_async`
- `aigie.wrappers._handle_messages_create_sync`
- `aigie.auto_instrument.llm.traced_ainvoke`
- `aigie.auto_instrument.llm.traced_invoke`
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

logger = logging.getLogger("aigie.autonomous.inline_call")


def _capture_current_span_into_ctx(ctx: Any) -> None:
    """Best-effort: stamp ctx.trace_id / ctx.span_id from the current OTel span.

    The dashboard joins OutcomeReports to spans by span_id, so the ctx that
    flows into intercept_post_call needs to carry the trace/span identifiers
    of the LLM span that just failed. We read them from
    ``opentelemetry.trace.get_current_span()`` when ctx doesn't already have
    them set. Silently no-op on any error so we never break the call path.
    """
    if ctx is None:
        return
    try:
        existing_trace = getattr(ctx, "trace_id", None)
        existing_span = getattr(ctx, "span_id", None)
        if existing_trace and existing_span:
            return
        from opentelemetry import trace as _otel_trace

        span = _otel_trace.get_current_span()
        sc = span.get_span_context() if span is not None else None
        if sc is None or not getattr(sc, "is_valid", False):
            return
        trace_id_hex = f"{sc.trace_id:032x}"
        span_id_hex = f"{sc.span_id:016x}"
        if not existing_trace:
            try:
                ctx.trace_id = trace_id_hex
            except Exception:  # noqa: BLE001
                pass
        if not existing_span:
            try:
                ctx.span_id = span_id_hex
            except Exception:  # noqa: BLE001
                pass
    except Exception as exc:  # noqa: BLE001
        logger.debug("capture_current_span_into_ctx error: %s", exc)


# Maximum number of autonomous retries per call site. Each iteration costs
# one extra LLM round-trip; keep this small. The chain hook is responsible
# for refusing to retry indefinitely (e.g. RetryIntervention caps
# `max_attempts` per directive).
_MAX_RETRIES = 3


def _gate_open(aigie: Any, ctx: Any) -> bool:
    """Return True iff the autonomous chain is wired and the toggle is on."""
    if ctx is None:
        return False
    if aigie is None:
        return False
    if not getattr(aigie, "_initialized", False):
        return False
    config = getattr(aigie, "config", None)
    if config is None or not getattr(config, "autonomous", False):
        return False
    return getattr(aigie, "_interceptor_chain", None) is not None


async def acall_with_autonomous(
    call: Callable[[], Awaitable[Any]],
    ctx: Any,
    aigie: Any,
) -> Any:
    """Async variant: run `call()` with one or more autonomous retries.

    Args:
        call: Zero-arg coroutine factory invoking the underlying LLM.
        ctx: Pre-call InterceptionContext (from `aigie.intercept_pre_call`).
        aigie: The Aigie client instance.

    Returns:
        Whatever `call()` returns on success.

    Raises:
        The last exception thrown by `call()` once the chain stops asking
        for retries, or once `_MAX_RETRIES` is reached.
    """
    # Imported lazily to avoid an import cycle with the interceptor package.
    from aigie.interceptor.protocols import InterceptionDecision

    attempts = 0
    while True:
        try:
            return await call()
        except Exception as exc:  # noqa: BLE001
            if not _gate_open(aigie, ctx):
                raise
            if attempts >= _MAX_RETRIES:
                raise
            _capture_current_span_into_ctx(ctx)
            try:
                result_ctx = await aigie.intercept_post_call(ctx, response=None, error=exc)
            except Exception as ic_exc:  # noqa: BLE001
                logger.debug("intercept_post_call raised on error path: %s", ic_exc)
                raise exc from ic_exc
            decision = getattr(result_ctx, "decision", None)
            if decision == InterceptionDecision.RETRY:
                attempts += 1
                continue
            raise


def call_sync_with_autonomous(
    call: Callable[[], Any],
    ctx: Any,
    aigie: Any,
) -> Any:
    """Sync variant — same shape as :func:`acall_with_autonomous`.

    Bridges to the async `intercept_post_call` via `Aigie._sync_post_call`,
    which is a thin shim that schedules the coroutine onto a fresh loop
    when no loop is running, or onto a temporary helper thread when called
    from inside a running loop.
    """
    from aigie.interceptor.protocols import InterceptionDecision

    attempts = 0
    while True:
        try:
            return call()
        except Exception as exc:  # noqa: BLE001
            if not _gate_open(aigie, ctx):
                raise
            if attempts >= _MAX_RETRIES:
                raise
            _capture_current_span_into_ctx(ctx)
            try:
                result_ctx = aigie._sync_post_call(ctx, response=None, error=exc)
            except Exception as ic_exc:  # noqa: BLE001
                logger.debug("_sync_post_call raised on error path: %s", ic_exc)
                raise exc from ic_exc
            decision = getattr(result_ctx, "decision", None)
            if decision == InterceptionDecision.RETRY:
                attempts += 1
                continue
            raise


__all__ = ["acall_with_autonomous", "call_sync_with_autonomous"]

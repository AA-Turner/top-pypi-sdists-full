"""SEND ONCE — the one step every model call crosses.

    send boundary  →  provider execute  →  capture  →  restore

The owner's requirement for AI request snapshots: *the exact shared engine that
runs a mandate also takes the copy, so it is impossible for them to drift.* The
copy (``chat.request_snapshot``) is taken from what the provider seam actually
sent, and that is only honest while EVERY path that re-issues a call runs the
same code the original did. Before this module the engine loop owned these
steps inline and Hindsight's wire replay rebuilt the request and called
``UnifiedAIClient().execute`` itself — skipping the send boundary, so reference
fences and picklist placeholders could reach the model unexpanded while the
replay's fidelity check still reported "faithful".

What one call does, in order:

1. ``prepare_for_send(stage=loop)`` — the send boundary (fence staging, the
   output-ceiling floor, the cache-gated trim, the prompt-cache key, the
   clone-at-send wire config). Nothing shapes a prompt outside it.
2. Swap the wire clone onto the request, mark the timing points, and call the
   provider client's ``execute`` — optionally wrapped by ``around`` (the engine
   wraps it in its stop poll and error-event buffer).
3. Capture: the provider's own ``capture_request_payload`` stashes the exact
   SDK-ready dict on ``state``. On a provider failure, ``on_provider_error``
   runs after the restore (the engine writes its failure snapshot there).
4. Restore the canonical config (placeholders, never secret values) and
   reverse-swap the captured payload with ``redact_wire_payload``.

A ``stop_exceptions`` exception (the person stopped the run mid-generation)
restores the config and re-raises without redaction or the error hook — the
engine's cancelled-run path owns what happens next. Task cancellation
(``CancelledError``) restores and redacts, without the error hook: the
canonical config is back on the request on EVERY exit path. Anything raised by the
send boundary itself propagates unchanged and is NOT a provider failure.

Guard: ``packages/matrx-ai/tests/test_send_once_guard.py`` fails if any other
code calls the provider client's ``execute`` directly.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from matrx_connect.chat_timing import chat_timing_mark

from matrx_ai.config.send_boundary import SendPrep


@dataclass
class SendOnceResult:
    """The provider's answer plus what the send boundary did to get there."""

    response: Any
    prep: SendPrep


def _redact_captured(state: Any) -> None:
    from matrx_ai.config.picklist_runtime import redact_wire_payload

    # Values → their placeholder / fence keys, never dropped unless the reverse
    # swap cannot be done safely (fail-closed → None).
    state.snapshot_payload = redact_wire_payload(state.snapshot_payload)


async def send_once(
    client: Any,
    request: Any,
    *,
    state: Any,
    iteration: int | None = None,
    around: Callable[[Awaitable[Any]], Awaitable[Any]] | None = None,
    stop_exceptions: tuple[type[BaseException], ...] = (),
    on_provider_error: Callable[[Exception], Awaitable[None]] | None = None,
) -> SendOnceResult:
    """Send ``request`` through the send boundary to the provider, exactly once.

    Args:
        client: the ``UnifiedAIClient`` to execute on.
        request: the ``AIMatrixRequest``. Its ``config`` is canonical on entry
            and canonical again on return or raise (the wire clone never
            outlives the call).
        state: the ``ExecutionState`` the provider captures its payload onto.
            It must also be the task's active execution state
            (``set_execution_state``) — that is where the provider seam writes.
        iteration: the loop iteration (trim audit + boundary bookkeeping).
        around: wraps the provider coroutine (stop poll, error buffering).
        stop_exceptions: exceptions that mean "stopped", not "failed".
        on_provider_error: awaited after restore + redaction when the provider
            call itself raises; the exception is then re-raised unchanged.
    """
    from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send
    from matrx_ai.mandate_taps import observe_first_send

    # Mandate candidates (P10): the host measures what this call carries at the
    # SAME seam for the live run and its candidate — before the send boundary.
    # Sync, never raises, never touches the request.
    observe_first_send(request, iteration)
    prep = await prepare_for_send(
        request.config,
        stage=STAGE_LOOP,
        conversation_id=request.conversation_id,
        request_id=request.request_id,
        iteration=iteration,
        organization_id=getattr(request, "organization_id", None),
    )

    wire_config = prep.wire_config
    canonical_config = request.config
    if wire_config is not None:
        request.config = wire_config
    chat_timing_mark("wire_config_built", "build_wire_config complete")
    chat_timing_mark("pre_provider_execute", "calling UnifiedAIClient.execute")
    from matrx_connect.request_latency import mark_first_provider_call

    mark_first_provider_call()
    call = client.execute(request)
    try:
        response = await (around(call) if around is not None else call)
    except stop_exceptions:
        if wire_config is not None:
            request.config = canonical_config
        raise
    except Exception as exc:
        if wire_config is not None:
            request.config = canonical_config
            _redact_captured(state)
        if on_provider_error is not None:
            await on_provider_error(exc)
        raise
    except BaseException:
        # Task cancellation (``asyncio.CancelledError``) or interpreter exit:
        # not a provider failure, so no error hook — but the wire clone still
        # never outlives the call. A cancel handler downstream persists the
        # partial turn from ``request``; it must see placeholders, not values.
        if wire_config is not None:
            request.config = canonical_config
            _redact_captured(state)
        raise
    if wire_config is not None:
        request.config = canonical_config
        _redact_captured(state)
    return SendOnceResult(response=response, prep=prep)


__all__ = ["SendOnceResult", "send_once"]

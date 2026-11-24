"""No provider call is made after a Stop that ended a held turn (one-graph C3 fix round 2).

The turn-boundary drain (``dynamic_drain.drain_pending``) HOLDS a paused turn; a Stop (this task's
registry, or another task's spine stamp, which the hold marks in the registry) ends the hold. The cancel
check at the top of the attempt ran BEFORE the drain, so the loop went straight on to the provider: a
model call started, billed, and was cancelled at once by the in-call poll. Now the executor checks again
right before the call: the stopped turn finalizes ``cancelled`` and ``send_once`` is never reached.

Red without that check (fix round 3, mutation-proven): removing the registry check reddens the
same-task case; removing the ``retry_attempt == 0`` spine branch reddens the drain-time spine case;
removing both reddens the real-hold cross-task case (``hold_while_paused`` itself, not a stub).
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_connect.context.app_context import set_app_context
from matrx_connect.request_controls import RequestControlRegistry

import matrx_ai.orchestrator.executor as executor_mod
import matrx_ai.orchestrator.send_once as send_once_mod
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest

REQUEST_ID = "44444444-4444-4444-8444-444444444444"


class _Emitter:
    def __getattr__(self, _name: str):
        async def _noop(*_a, **_k):
            return None

        return _noop

    def reset_turn_text(self):
        return None

    def get_turn_text(self):
        return ""


class _Ctx:
    conversation_id = "11111111-1111-4111-8111-111111111111"
    user_id = "22222222-2222-4222-8222-222222222222"
    parent_conversation_id = None
    request_id = REQUEST_ID
    store = False
    debug = False
    snapshot = False
    metadata: dict[str, Any] = {}
    emitter = _Emitter()


def _request(request_id: str = REQUEST_ID) -> AIMatrixRequest:
    messages = MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])])
    return AIMatrixRequest(
        conversation_id=_Ctx.conversation_id,
        config=UnifiedConfig(model="test-model", messages=messages),
        request_id=request_id,
    )


async def _run(monkeypatch, stop_during_drain, request_id=REQUEST_ID) -> tuple[list[int], dict[str, Any]]:
    calls: list[int] = []
    finalized: dict[str, Any] = {}

    async def _drain(config, ctx):
        await stop_during_drain()  # the hold ends in a Stop
        return ctx

    async def _send_once(*_a, **_k):
        calls.append(1)
        raise AssertionError("a provider call was made after a Stop")

    async def _finalize(*, metadata, state, **_k):
        finalized.update(metadata)
        if state is not None:
            state.persisted = True
        return object()

    async def _noop(*_a, **_k):
        return None

    import matrx_ai.tools.dynamic_drain as dd

    monkeypatch.setattr(dd, "drain_pending", _drain)
    monkeypatch.setattr(send_once_mod, "send_once", _send_once)
    monkeypatch.setattr(executor_mod, "_finalize_and_persist", _finalize)
    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop)
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _Ctx())
    ctx = _Ctx()
    ctx.request_id = request_id
    set_app_context(ctx)
    await executor_mod._execute_until_complete_inner(
        exec_ctx=ctx,
        state=ExecutionState(),
        initial_request=_request(request_id),
        client=object(),
        max_iterations=1,
        max_retries_per_iteration=0,
    )
    return calls, finalized


@pytest.mark.asyncio
async def test_a_same_task_stop_that_ends_the_hold_makes_no_provider_call(monkeypatch):
    async def stop():
        await RequestControlRegistry.get_instance().cancel(REQUEST_ID)

    calls, finalized = await _run(monkeypatch, stop)
    assert calls == []
    assert finalized.get("status") == "cancelled"


def _ctx_for(request_id: str) -> _Ctx:
    ctx = _Ctx()
    ctx.request_id = request_id
    return ctx


@pytest.mark.asyncio
async def test_a_stop_from_another_task_that_ends_a_real_hold_makes_no_provider_call(monkeypatch):
    """The REAL hold: the turn is paused at the boundary, and the Stop is another task's spine stamp
    that lands WHILE it is held (not before: the top-of-attempt check must not be the one that sees it).
    The hold marks this process's registry cancelled and ends; only the executor's check right before
    the call stands between that and a billed provider call."""
    import matrx_ai.db.turn_control as turn_control
    import matrx_ai.tools.dynamic_drain as dd
    from matrx_ai import _ext

    request_id = "66666666-6666-4666-8666-666666666666"
    held = {"now": False}

    async def spine_check():
        return "cancelled from another task" if held["now"] else None

    async def no_inbox(_ctx):
        return None

    monkeypatch.setattr(_ext, "get_spine_control_check", lambda: spine_check)
    monkeypatch.setattr(turn_control, "control_poll_seconds", lambda: 0.0)
    monkeypatch.setattr(turn_control, "pause_max_hold_seconds", lambda: 5.0)
    monkeypatch.setattr(dd, "apply_turn_controls", no_inbox)

    async def paused_then_stopped_while_held():
        RequestControlRegistry.get_instance().pause(request_id)
        held["now"] = True  # the other task's Stop lands while the turn is held
        await dd.hold_while_paused(_ctx_for(request_id))
        assert RequestControlRegistry.get_instance().is_cancelled(request_id), "the hold did not take the Stop"

    calls, finalized = await _run(monkeypatch, paused_then_stopped_while_held, request_id)
    assert calls == []
    assert finalized.get("status") == "cancelled"


@pytest.mark.asyncio
async def test_a_spine_stop_that_lands_during_the_drain_makes_no_provider_call(monkeypatch):
    """The executor's ``retry_attempt == 0`` spine branch: the Stop is another task's spine stamp that
    lands during the drain (no hold, so nothing marks this registry). Only the spine check right
    before the call sees it."""
    from matrx_ai import _ext

    request_id = "77777777-7777-4777-8777-777777777777"
    drained = {"now": False}

    async def spine_check():
        return "cancelled from another task" if drained["now"] else None

    monkeypatch.setattr(_ext, "get_spine_control_check", lambda: spine_check)

    async def stop_lands_in_the_drain():
        drained["now"] = True

    calls, finalized = await _run(monkeypatch, stop_lands_in_the_drain, request_id)
    assert not RequestControlRegistry.get_instance().is_cancelled(request_id)
    assert calls == []
    assert finalized.get("status") == "cancelled"
    assert "execution control" in str(finalized.get("error"))

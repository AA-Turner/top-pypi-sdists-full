"""A turn the stall backstop stops is FAILED, never "cancelled" (2026-10-03).

When the lease heartbeat gives up on a run that stopped making progress (a
wedged commit), it cancels the runner. Before this, that cancel unwound as an
ordinary disconnect: the turn persisted as ``cancelled`` and the person saw a
stopped turn with no reason. Now the executor reads the tracker the heartbeat
marked and persists ``failed`` with a readable message, then raises
``RunStalledError`` (a fatal error every stream handler renders).
"""

from __future__ import annotations

import asyncio

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.persistence.liveness import (
    Overrun,
    RunLiveness,
    RunStalledError,
    bind_run_liveness,
    unbind_run_liveness,
)


class _Ctx:
    conversation_id = "93ea4aed"
    user_id = "user-1"
    parent_conversation_id = None
    request_id = "req-1"
    store = True

    class _Emitter:
        async def send_info(self, *a, **k):
            return None

    emitter = _Emitter()


class _Req:
    request_id = "req-1"
    conversation_id = "93ea4aed"


def _arm(monkeypatch, persisted: dict) -> None:
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _Ctx())

    async def fake_inner(*, state: ExecutionState, **kwargs):
        state.current_request = _Req()
        state.iteration = 1
        state.trigger_position = 0
        state.pre_execution_message_count = 1
        raise asyncio.CancelledError()  # the backstop's cancel, mid-finalize

    async def fake_finalize(*, metadata, state, **kwargs):
        persisted["metadata"] = metadata
        state.persisted = True
        return object()

    monkeypatch.setattr(executor_mod, "_execute_until_complete_inner", fake_inner)
    monkeypatch.setattr(executor_mod, "_finalize_and_persist", fake_finalize)


@pytest.mark.asyncio
async def test_a_stall_cancel_persists_failed_and_raises_run_stalled(monkeypatch):
    persisted: dict = {}
    _arm(monkeypatch, persisted)
    liveness = RunLiveness("conversation")
    liveness.stalled = Overrun("coordinator.finalize:request_final_commit", 142.0, 420.0)
    token = bind_run_liveness(liveness)
    try:
        with pytest.raises(RunStalledError) as info:
            await executor_mod.execute_until_complete(initial_request=object(), client=object())
    finally:
        unbind_run_liveness(token)

    meta = persisted["metadata"]
    assert meta["status"] == "failed"
    assert meta["error"]["type"] == "matrx_run_stalled"
    assert "failed" in meta["error"]["message"].lower()
    assert info.value.error_info.error_type == "matrx_run_stalled"
    # The cancel was consumed, not left pending on the task.
    assert asyncio.current_task().cancelling() == 0


@pytest.mark.asyncio
async def test_an_ordinary_cancel_is_still_cancelled(monkeypatch):
    persisted: dict = {}
    _arm(monkeypatch, persisted)
    with pytest.raises(asyncio.CancelledError):
        await executor_mod.execute_until_complete(initial_request=object(), client=object())
    assert persisted["metadata"]["status"] == "cancelled"

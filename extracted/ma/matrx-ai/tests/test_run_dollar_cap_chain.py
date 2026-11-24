"""RunOptions.max_cost_usd, through the real chain: host carrier -> request metadata -> ``execute_ai_request`` -> the loop.

* the host carries the cap under ``max_cost_usd`` and ``execute_ai_request`` turns that metadata into the request's ceiling
  (the real function, stopped by a sentinel right after the hand-off);
* the real loop (``_execute_until_complete_inner``, stub provider, no network) stops BEFORE the next provider call once the
  run's cap is spent, and a run with no cap still calls the provider (the control).
"""

from __future__ import annotations

import pytest
from test_truncated_response_capture import (
    _REQUEST_ID,
    _app_context,
    _RecordingEmitter,
    _run_one_turn,
)

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, UnifiedConfig
from matrx_ai.orchestrator import cost_budget as cb


class _Stop(Exception):
    pass


@pytest.mark.asyncio
async def test_execute_ai_request_turns_the_metadata_cap_into_the_requests_ceiling(monkeypatch):
    ctx = _app_context(_RecordingEmitter())
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: ctx)

    async def stop(*a, **k):
        raise _Stop

    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", stop)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", stop)
    cfg = UnifiedConfig(model="gemini-test", messages=MessageList())
    cb.forget_tree(ctx.request_id)
    try:
        for md, want in (({"max_cost_usd": 0.5}, 0.5), ({}, None)):
            cb.forget_tree(ctx.request_id)
            with pytest.raises(_Stop):
                await executor_mod.execute_ai_request(cfg, metadata=dict(md))
            left = cb.remaining_budget(ctx.request_id)
            if want is None:
                assert (
                    left == cb.TREE_COST_CEILING_USD
                )  # the control: no cap, only the tree ceiling
            else:
                assert left == pytest.approx(want)  # narrowed to the run's cap
            cb.record_tree_cost(ctx.request_id, 0.6)
            assert (cb.ceiling_stop_reason(ctx.request_id) is not None) == (want is not None)
    finally:
        cb.forget_tree(ctx.request_id)


@pytest.mark.asyncio
async def test_the_loop_stops_before_the_next_provider_call_when_the_cap_is_spent(monkeypatch):
    cb.forget_tree(_REQUEST_ID)
    try:
        control = await _run_one_turn(monkeypatch, "stop")
        assert control["client"].calls == 1  # no cap: the provider is called
        cb.forget_tree(_REQUEST_ID)
        cb.set_request_ceiling(_REQUEST_ID, 0.01)
        cb.record_tree_cost(_REQUEST_ID, 0.02)  # the cap is spent
        capped = await _run_one_turn(monkeypatch, "stop")
        assert (
            capped["client"].calls == 0
        )  # stopped at the iteration boundary, nothing more was paid for
    finally:
        cb.forget_tree(_REQUEST_ID)

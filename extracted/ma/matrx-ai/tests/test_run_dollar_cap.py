"""RunOptions.max_cost_usd: a caller's dollar cap narrows the tree ceiling and stops the loop at the boundary."""

from __future__ import annotations

from matrx_ai.mandates import RunOptions
from matrx_ai.orchestrator import cost_budget as cb


def test_cap_stops_the_run_once_spent_and_never_widens_the_tree_ceiling():
    rid = "cap-test-root"
    cb.forget_tree(rid)
    try:
        assert cb.ceiling_stop_reason(rid) is None
        cb.set_request_ceiling(rid, 0.50)
        cb.record_tree_cost(rid, 0.20)
        assert cb.ceiling_stop_reason(rid) is None
        assert abs(cb.remaining_budget(rid) - 0.30) < 1e-9
        cb.record_tree_cost(rid, 0.35)
        assert "dollar cap" in (cb.ceiling_stop_reason(rid) or "")
        assert cb.remaining_budget(rid) < 0  # the existing guardrail also blocks new tool calls
        cb.set_request_ceiling(rid, 99.0)  # a later, larger ask never widens
        assert cb.ceiling_stop_reason(rid) is not None
    finally:
        cb.forget_tree(rid)
    assert cb.ceiling_stop_reason(rid) is None


def test_a_run_without_a_cap_is_not_stopped_by_this_path():
    rid = "no-cap-root"
    cb.forget_tree(rid)
    cb.record_tree_cost(rid, 5.0)
    assert cb.ceiling_stop_reason(rid) is None
    cb.forget_tree(rid)


def test_run_options_carries_the_cap():
    assert RunOptions(door="x", max_cost_usd=1.5).max_cost_usd == 1.5
    assert RunOptions(door="x").max_cost_usd is None

"""A run stopped at a limit names WHICH limit, with its numbers, to the model and to its caller.

Live 2026-11-15 (failure register entry 5): an investigation desk at 2 rounds left was told to
"finish the ONE thing you are building now (the table, page, card or button in hand)", and the
caller that relayed the stop had only a sentence to guess the cause from. The notices are now
role-neutral and numbered, and ``AgentRunResult.stop_cause`` carries the cause as a value.
"""

from __future__ import annotations

import time
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.orchestrator.stop_cause import RunStopCause, stop_cause_from_metadata

BUILDER_WORDS = ("building", "table, page, card or button", "files, commits")


def test_the_round_notices_are_role_neutral_and_name_the_rounds() -> None:
    from matrx_ai.orchestrator.executor import _ceiling_approaching_notice, _ceiling_wrap_up_notice

    approaching = _ceiling_approaching_notice(12, 2)
    wrap_up = _ceiling_wrap_up_notice(12)
    for text in (approaching, wrap_up):
        assert not any(word in text for word in BUILDER_WORDS), text
        assert "12" in text
    assert "2 left" in approaching
    assert "12-round limit" in wrap_up


def test_the_approaching_notice_names_a_running_time_budget_with_its_numbers() -> None:
    from matrx_ai.orchestrator.executor import _ceiling_approaching_notice

    text = _ceiling_approaching_notice(12, 2, time_left=(95.4, {"seconds": 360, "label": "senior desk"}))
    assert "360s" in text and "95s left" in text
    assert "no final turn" in text, "time stops the run without a wrap-up turn, and the model is told"


def test_the_cause_is_derived_from_what_the_loop_records() -> None:
    rounds = stop_cause_from_metadata({"status": "max_iterations_exceeded", "max_iterations": 12})
    assert rounds == RunStopCause(
        kind="rounds", allowed=12, used=12, unit="rounds", detail="used all 12 tool rounds this run allows"
    )
    assert stop_cause_from_metadata({"budget_wrap_up": True}).kind == "cost"  # type: ignore[union-attr]
    assert stop_cause_from_metadata({"status": "completed"}) is None
    stamped = {"status": "cancelled", "stop_cause": {"kind": "time", "allowed": 360, "used": 361, "unit": "seconds"}}
    assert stop_cause_from_metadata(stamped).kind == "time"  # type: ignore[union-attr]


def test_an_execution_control_stop_names_time_or_cost_with_numbers() -> None:
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    from matrx_ai.orchestrator import cost_budget
    from matrx_ai.orchestrator.executor import _execution_control_stop_cause
    from matrx_ai.orchestrator.subtree_budget import SUBTREE_BUDGET_METADATA_KEY, SUBTREE_BUDGET_STOP_MARKER

    expired = {"label": "senior desk", "seconds": 360, "opened_at": time.time() - 361, "expires_at": time.time() - 1}
    token = set_app_context(
        AppContext(emitter=ConsoleEmitter(), user_id="u", metadata={SUBTREE_BUDGET_METADATA_KEY: [expired]})
    )
    try:
        cause = _execution_control_stop_cause("req-1", f"{SUBTREE_BUDGET_STOP_MARKER}: the senior desk ran out")
    finally:
        clear_app_context(token)
    assert (cause.kind, cause.allowed, cause.unit, cause.label) == ("time", 360, "seconds", "senior desk")
    assert cause.used is not None and cause.used >= 360

    request_id = "cost-cap-request-for-stop-cause-test"
    cost_budget.set_request_ceiling(request_id, 0.5)
    cost_budget.record_tree_cost(request_id, 0.75)
    try:
        cost = _execution_control_stop_cause(request_id, f"dollar cap: {cost_budget.ceiling_stop_reason(request_id)}")
    finally:
        cost_budget.forget_tree(request_id)
    assert (cost.kind, cost.allowed, cost.used, cost.unit) == ("cost", 0.5, 0.75, "usd")


@pytest.mark.asyncio
async def test_run_agent_hands_its_caller_the_stop_cause() -> None:
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id="22222222-2222-2222-2222-222222222222"))

    async def _execute(user_input: Any = None, *, max_iterations: Any = None, **_: Any) -> Any:
        return SimpleNamespace(
            output="Stopped at the 12-round limit: found the alarm row, not the cap.",
            assistant_response=None,
            config=SimpleNamespace(model="test-model", metadata={}),
            usage=None,
            usage_history=[],
            metadata={"status": "max_iterations_exceeded", "max_iterations": 12, "ceiling_wrap_up": True},
        )

    agent = SimpleNamespace(
        name="senior-desk",
        config=SimpleNamespace(model="test-model", metadata={}),
        source_id=None,
        source_is_version=False,
        request_metadata={},
        execute=_execute,
    )
    result = await run_agent(
        agent,  # type: ignore[arg-type]
        label="desk",
        source_app="test",
        source_feature="desk",
        emit_lifecycle=False,
    )
    assert result.stop_cause is not None
    assert (result.stop_cause.kind, result.stop_cause.allowed) == ("rounds", 12)

"""dedupe_exempt covers BOTH repeat guards — duplicate AND loop detection.

A tool flagged ``dedupe_exempt`` (status pollers: agent_plan, workflow_run)
legitimately repeats identical calls. The duplicate check always honored the
flag; loop detection did not — on 2026-07-07 an agent-plan run finished
while polling, and the loop guard blocked the exact status call that would
have returned the results (the model then burned tokens on filler calls to
dodge the guard). Non-exempt tools must still trip both guards.
"""

from __future__ import annotations

import pytest
from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    set_app_context,
)

from matrx_ai.tools.guardrails import GuardrailEngine
from matrx_ai.tools.models import ToolContext, ToolDefinition


@pytest.fixture(autouse=True)
def _app_context():
    # ToolContext.conversation_id is a property over the ambient AppContext.
    token = set_app_context(
        AppContext(
            emitter=None,
            user_id="test-user",
            is_authenticated=True,
            conversation_id="conv-1",
            request_id="req-1",
        )
    )
    try:
        yield
    finally:
        clear_app_context(token)


def _tool_def(name: str, *, dedupe_exempt: bool) -> ToolDefinition:
    return ToolDefinition(
        name=name,
        description="test tool",
        parameters={"action": {"type": "string", "required": True}},
        dedupe_exempt=dedupe_exempt,
    )


def _ctx() -> ToolContext:
    return ToolContext(call_id="c1", conversation_id="conv-1")


def _hammer(
    guard: GuardrailEngine, tool_def: ToolDefinition, times: int
) -> list[str | None]:
    """Repeat identical calls through the two repeat-guards; collect blocks.

    Drives ``_check_duplicate`` + ``_check_loop_detection`` directly (the
    same pattern as test_agent_recursion_depth) — ``check()`` also runs the
    cost-budget guard, which needs a live AppContext and is not under test.
    """
    outcomes: list[str | None] = []
    args = {"action": "status", "run_id": "run-1"}
    for _ in range(times):
        ctx = _ctx()
        for result in (
            guard._check_duplicate(tool_def.name, args, ctx, tool_def),
            guard._check_loop_detection(tool_def.name, args, ctx, tool_def),
        ):
            if result.blocked:
                outcomes.append(result.error_type)
                break
        else:
            outcomes.append(None)
            guard.record_call(tool_def.name, args, ctx)
    return outcomes


def test_exempt_tool_polls_freely():
    guard = GuardrailEngine()
    outcomes = _hammer(guard, _tool_def("agent_plan", dedupe_exempt=True), 8)
    assert outcomes == [None] * 8  # neither duplicate nor loop_detected fires


def test_non_exempt_tool_still_trips_duplicate():
    guard = GuardrailEngine()
    outcomes = _hammer(guard, _tool_def("some_tool", dedupe_exempt=False), 8)
    blocked = [o for o in outcomes if o is not None]
    assert blocked, "identical repeats on a non-exempt tool must be blocked"
    assert blocked[0] == "duplicate"


def _interleaved(
    guard: GuardrailEngine, poller: ToolDefinition, filler: ToolDefinition, rounds: int
) -> list[str | None]:
    """The live 2026-07-07 pattern: identical polls interleaved with another
    tool. The duplicate guard's CONSECUTIVE counter resets on every filler
    call, so only loop detection (same-tool recency window) can fire."""
    outcomes: list[str | None] = []
    poll_args = {"action": "status", "run_id": "run-1"}
    for i in range(rounds):
        ctx = _ctx()
        for result in (
            guard._check_duplicate(poller.name, poll_args, ctx, poller),
            guard._check_loop_detection(poller.name, poll_args, ctx, poller),
        ):
            if result.blocked:
                outcomes.append(result.error_type)
                break
        else:
            outcomes.append(None)
            guard.record_call(poller.name, poll_args, ctx)
        guard.record_call(filler.name, {"q": f"search {i}"}, ctx)
    return outcomes


def test_non_exempt_interleaved_polls_trip_loop_detection():
    """Pins the loop guard itself: with fillers defeating the duplicate
    check, the 6th identical poll must be blocked as loop_detected. A
    regression that disables loop detection outright ships green without
    this test (mutation-verified gap from the 2026-07-07 review)."""
    guard = GuardrailEngine()
    outcomes = _interleaved(
        guard,
        _tool_def("some_tool", dedupe_exempt=False),
        _tool_def("web", dedupe_exempt=False),
        8,
    )
    assert "duplicate" not in outcomes  # fillers keep the consecutive count at 1
    assert "loop_detected" in outcomes
    assert outcomes[5] == "loop_detected"  # 5 recorded polls in the window → 6th blocked


def test_exempt_tool_interleaved_polls_never_blocked():
    guard = GuardrailEngine()
    outcomes = _interleaved(
        guard,
        _tool_def("agent_plan", dedupe_exempt=True),
        _tool_def("web", dedupe_exempt=False),
        8,
    )
    assert outcomes == [None] * 8


def test_exempt_poll_flood_does_not_blind_loop_for_other_tool():
    """Loop detection uses a PER-TOOL recency window, not this-tool-within-
    the-global-last-N. Exempt pollers are still recorded (rate/cost limits
    need them); under a global window a burst of exempt polls would evict an
    unrelated non-exempt tool's calls and silently disable its loop guard.
    Mutation check: a global-window regression ships green without this."""
    guard = GuardrailEngine()
    x = _tool_def("some_tool", dedupe_exempt=False)
    poller = _tool_def("agent_plan", dedupe_exempt=True)
    ctx = _ctx()
    x_args = {"action": "status", "run_id": "run-1"}

    # 5 identical calls to the non-exempt tool X (a real loop forming).
    for _ in range(5):
        guard.record_call(x.name, x_args, ctx)
    # A burst of exempt polls floods the global history well past the
    # recency window — under a global window every X record is evicted.
    for i in range(12):
        guard.record_call(poller.name, {"action": "status", "run_id": "run-1", "n": i}, ctx)

    # The 6th X call must STILL be caught — X's own recent calls survive.
    result = guard._check_loop_detection(x.name, x_args, ctx, x)
    assert result.blocked
    assert result.error_type == "loop_detected"
    assert "identical arguments" in result.reason  # honest naming, not "very similar"


def test_registry_row_maps_dedupe_exempt():
    """The seam the 2026-07-07 review caught: the DB column existed and the
    guards honored the flag, but _row_to_definition never mapped it — the
    whole exemption was inert for every DB-loaded tool."""
    from matrx_ai.tools.registry import ToolRegistry

    row = {
        "name": "agent_plan",
        "description": "poller",
        "parameters": {"action": {"type": "string", "required": True}},
        "source_kind": "native",
        "dedupe_exempt": True,
    }
    assert ToolRegistry._row_to_definition(row).dedupe_exempt is True
    row["dedupe_exempt"] = False
    assert ToolRegistry._row_to_definition(row).dedupe_exempt is False
    del row["dedupe_exempt"]
    assert ToolRegistry._row_to_definition(row).dedupe_exempt is False

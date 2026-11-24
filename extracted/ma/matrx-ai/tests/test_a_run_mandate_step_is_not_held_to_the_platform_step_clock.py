"""Run Mandate steps whose holder is a workflow wait for that workflow, so they are not held to the 600 s step clock.

``subgraph.call`` got the longest limit the engine allows (2026-11-10: a pass whose read step ran longer was
cut off at 600 s). A Run Mandate step bound to a WORKFLOW holder is the same wait, so it declares the same
long limit; the child's own clocks bound it and ``data.step_clock`` still sets a shorter one.
"""

from __future__ import annotations

from matrx_graph import knobs as graph_knobs
from matrx_graph.executor.registry import default_registry
from matrx_graph.types.compiled import StepClock

import matrx_ai.graph_nodes.mandate_action  # noqa: F401 — registers ai.mandate.start


def _spec():
    return default_registry().get("ai.mandate.start").spec


def test_run_mandate_declares_the_longest_limit_the_engine_allows() -> None:
    assert _spec().timeout_ms == graph_knobs.MAX_STEP_SECONDS * 1000


async def test_the_declared_limit_beats_the_platform_ceiling_and_a_step_clock_still_shortens_it() -> None:
    seconds, source = await graph_knobs.step_timeout_seconds(_spec().timeout_ms)
    assert seconds > graph_knobs.STARTING_DEFAULT_STEP_SECONDS and source == "declared"
    shorter, _ = await graph_knobs.step_timeout_seconds(_spec().timeout_ms, node_clock=StepClock(seconds=90))
    assert shorter == 90.0


# ── Only a WORKFLOW holder gets the long limit (review 6h follow-up) ─────────────────────────────────────────
# The long declared limit removed the 600 s ceiling from AGENT-held Run Mandate steps too, so one stuck provider
# call could hang for hours. The body now bounds an agent holder by the platform step clock itself. Red before:
# the agent holder ran its full (slow) call; green: it stops at the platform clock with a "platform" NodeTimeoutError,
# while a workflow holder slower than that clock still finishes.

import asyncio  # noqa: E402
from types import SimpleNamespace  # noqa: E402
from typing import Any  # noqa: E402

import pytest  # noqa: E402
from matrx_graph.errors import NodeTimeoutError  # noqa: E402

from matrx_ai.graph_nodes import agent_action as aa  # noqa: E402
from matrx_ai.graph_nodes import mandate_action as ma  # noqa: E402
from matrx_ai.graph_nodes.agent_action import StepAgent, StepWorkflowMandate  # noqa: E402
from matrx_ai.graph_nodes.shared import AiExecutionResult  # noqa: E402

PLATFORM_SECONDS = 0.05
SLOW = 0.4


@pytest.fixture()
def holder(monkeypatch: pytest.MonkeyPatch):
    state: dict[str, Any] = {"kind": "agent", "finished": []}

    async def platform_clock() -> float:
        return PLATFORM_SECONDS

    async def resolve(*_a: Any, **_k: Any) -> Any:
        if state["kind"] == "workflow":
            return StepWorkflowMandate(mandate_key="m.k", workflow_id="wf-1", workflow_version_id=None,
                                       declared_output_kind=None)
        return StepAgent(agent_id="agent-1", is_version=False, config_overrides={}, declared_output_kind=None)

    async def limit(_ctx: Any, _authored: Any) -> Any:
        return SimpleNamespace(value=10, name_on=lambda r: r)

    async def slow_agent(_ctx: Any, agent_id: str, request: Any, mandate_key: str, **_kw: Any) -> AiExecutionResult:
        await asyncio.sleep(SLOW)
        state["finished"].append("agent")
        return AiExecutionResult(conversation_id="c", request_id="r", iterations=1, final_text="late")

    async def slow_workflow(*_a: Any, **_k: Any) -> str:
        await asyncio.sleep(SLOW)
        state["finished"].append("workflow")
        return "workflow answer"

    async def bind(inputs: Any, _resolved: Any) -> Any:
        return inputs

    monkeypatch.setattr(graph_knobs, "default_step_seconds", platform_clock)
    monkeypatch.setattr(ma, "refuse_if_mandate_paused", lambda _key: asyncio.sleep(0))
    monkeypatch.setattr(ma, "resolve_step_agent_full", resolve)
    monkeypatch.setattr(ma, "resolve_step_iteration_limit", limit)
    monkeypatch.setattr(ma, "_bind_provision_values", bind)
    monkeypatch.setattr(ma, "has_ext", lambda _name: True)
    monkeypatch.setattr(ma, "_run_workflow_held_mandate", slow_workflow)
    monkeypatch.setattr(ma, "build_agent_request", lambda _ctx, inputs, resolved, **_k: SimpleNamespace(
        variables={}, config_overrides={}, user_input=None))
    monkeypatch.setattr(aa, "run_step_agent", slow_agent)
    return state


def _run() -> Any:
    ctx = SimpleNamespace(node_id="step_a", run_id="run-1", attempt=2)
    inputs = ma.MandateStartInput.model_validate({"mandate_key": "m.k"})
    return asyncio.run(ma._mandate_start_body(ctx, inputs, None))


def test_an_agent_holder_keeps_the_platform_clock(holder) -> None:
    holder["kind"] = "agent"
    with pytest.raises(NodeTimeoutError) as caught:
        _run()
    assert caught.value.source == "platform" and holder["finished"] == [], (caught.value, holder)


def test_a_workflow_holder_is_not_cut_by_the_platform_clock(holder) -> None:
    holder["kind"] = "workflow"
    assert _run() == "workflow answer" and holder["finished"] == ["workflow"]

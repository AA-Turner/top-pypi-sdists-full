"""Workflow AI steps resolve their mandate through the mandate runner's port (runner plan 25 step 9a).

Run Mandate (``ai.mandate.start``), Agent → Typed Result (``ai.agent.produce``) and every authored AI
step's ``hold_step`` reach their Holder through ``get_mandate_runner().prepare(key, StepOffer(), who=,
opts=)`` — the explicit principal the step's carried request names, a typed and recorded refusal —
never through the old resolver seam (``resolve_mandate_by_key``). Each test makes the old seam raise,
so a node that still used it fails here.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai import mandates
from matrx_ai.agents.named import AgentRecordSource
from matrx_ai.graph_nodes.agent_action import StepOffer, resolve_step_agent_full
from matrx_ai.graph_nodes.mandate_action import MandateStartInput
from matrx_ai.graph_nodes.mandates import (
    STEP_INTELLIGENCE_DOOR,
    WORKFLOW_STEP_INTELLIGENCE_MANDATE,
    hold_step,
)

_WHO = mandates.Principal(user_id="person-1", org_id="org-1")


class _Prepared:
    def __init__(self, held: Any) -> None:
        self.held = held


class _StepRunner:
    system = mandates.Principal(user_id=None, org_id="system-org")

    def __init__(self, resolution: Any) -> None:
        self.resolution = resolution
        self.calls: list[tuple[str, Any, Any, Any]] = []

    async def run(self, *a: Any, **k: Any) -> Any:
        raise AssertionError("a workflow step never asks the runner to run its Holder")

    async def prepare(self, key: str, offer: Any, *, who: Any, opts: Any) -> Any:
        self.calls.append((key, offer, who, opts))
        if isinstance(self.resolution, BaseException):
            raise self.resolution
        return _Prepared(self.resolution)

    async def finish(self, *a: Any, **k: Any) -> Any:
        raise AssertionError("a workflow step's Holder run writes its own run row; finish is never called")

    async def resolve(self, *a: Any, **k: Any) -> Any:
        raise AssertionError("not used")


def _install(monkeypatch: pytest.MonkeyPatch, resolution: Any) -> _StepRunner:
    runner = _StepRunner(resolution)

    async def _old_seam(_key: str) -> Any:
        raise AssertionError("the step went around the runner through the old resolver seam")

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _old_seam)
    monkeypatch.setattr(mandates, "_MANDATE_RUNNER", runner)
    monkeypatch.setattr(mandates, "carried_principal", lambda *a, **k: _WHO)
    return runner


@pytest.mark.asyncio
async def test_run_mandate_step_resolves_through_the_runner_port(monkeypatch: pytest.MonkeyPatch) -> None:
    materialize_calls: list[dict[str, Any]] = []

    async def _materialize(supplied: dict[str, Any]) -> dict[str, Any]:
        materialize_calls.append(supplied)
        return supplied

    resolution = mandates.MandateResolution(
        source=AgentRecordSource(agent_id="holder-1", is_version=False),
        config_overrides={"temperature": 0.2},
        consumption_map={"topic": {"mapType": "offered_value", "target": "topic"}},
        materialize=_materialize,
        run_stamp={"holder_id": "holder-1"},
        output_kind="text",
    )
    runner = _install(monkeypatch, resolution)

    resolved = await resolve_step_agent_full(
        MandateStartInput(mandate_key="study.notes"), consumer="ai.mandate.start:n1"
    )

    assert len(runner.calls) == 1
    key, offer, who, opts = runner.calls[0]
    assert key == "study.notes"
    assert isinstance(offer, StepOffer) and dict(offer) == {}, "the step asks for its resolution, not a held call"
    assert who == _WHO, "the explicit principal of the step's carried request"
    assert opts.door == "workflow_step" and opts.consumer == "ai.mandate.start:n1"
    assert resolved.agent_id == "holder-1"
    assert resolved.config_overrides == {"temperature": 0.2}
    assert resolved.materialize is _materialize, "the binding's own pipeline reaches the step"
    assert resolved.run_stamp == {"holder_id": "holder-1"}
    assert materialize_calls == [], "resolving applies nothing: the step binds the state it holds"


@pytest.mark.asyncio
async def test_a_refusal_from_the_runner_reaches_the_step_typed(monkeypatch: pytest.MonkeyPatch) -> None:
    refusal = mandates.MandateRefused("study.notes", code="no_holder", sentence="no Holder at any rung")
    _install(monkeypatch, refusal)

    with pytest.raises(mandates.MandateRefused) as excinfo:
        await resolve_step_agent_full(MandateStartInput(mandate_key="study.notes"), consumer="ai.mandate.start:n1")
    assert excinfo.value is refusal


@pytest.mark.asyncio
async def test_hold_step_resolves_through_the_runner_and_still_runs_as_authored_on_a_refusal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = _install(
        monkeypatch,
        mandates.MandateRefused(WORKFLOW_STEP_INTELLIGENCE_MANDATE, code="no_holder", sentence="unbound"),
    )
    from matrx_ai import _ext

    monkeypatch.setitem(_ext._registry, "record_error", lambda *a, **k: None)

    held = await hold_step({"model": "author-model"}, spec_type="ai.llm", consumer="ai.llm.chat")

    assert [(c[0], c[3].door) for c in runner.calls] == [(WORKFLOW_STEP_INTELLIGENCE_MANDATE, STEP_INTELLIGENCE_DOOR)]
    assert isinstance(runner.calls[0][1], StepOffer)
    assert held.config["model"] == "author-model", "an authored step runs as its author wrote it"

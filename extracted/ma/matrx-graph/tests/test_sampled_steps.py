"""A TEST run answers chosen steps from their declared sample instead of running them.

``Scheduler(sampled_outputs={node_id: sample})`` — the host resolves the samples (and refuses a
non-test run / a missing sample) before the run exists; the engine's promise is proven here:

1. transform → paid step → transform: the paid step's executor is never called, the third step
   sees the sample, and the run completes.
2. The sampled outcome is flagged (``source="mocked"`` + ``metadata.sampled``) and the
   ``node_skipped`` event says ``sampled=True`` — a sample never reads as a real answer.
3. A sampled ``data.once`` step writes NOTHING to the run-once-per-key store, so a later real
   run never reuses a sample.
4. A For Each target listed gets the sample for every item; none of them runs.
5. A sample that does not fit the step's output fails the run naming the step.
6. A resumed leg answers a sampled step it reaches the same way (no executor call).
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import Any

import pytest
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph import knobs
from matrx_graph.errors import GraphInterrupt
from matrx_graph.once import MemoryStepResultStore, configure_step_result_store
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context

ORG = "11111111-1111-4111-8111-111111111111"
WF = "33333333-3333-4333-8333-333333333333"


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")
    score: int


class _Paid:
    """A paid AI step: counts every real call."""

    def __init__(self, node_type: str = "test.paid_ai") -> None:
        self.spec = NodeSpec(
            type=node_type,
            category=NodeCategory.AGENT,
            display_name=node_type,
            description="sampled-steps test step",
            input_schema=_In,
            output_schema=_Out,
            config_schema=_Cfg,
            handles=(
                HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
                HandleSpec(id="out", direction=HandleDirection.OUTPUT),
            ),
            determinism=ActionTier.NON_DETERMINISTIC,
            retry=RetryPolicy(max_attempts=1),
        )
        self.calls = 0

    async def result_version(self, ctx: Any, inputs: Any, config: Any) -> str:
        return "agent-rev-1"

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        return success(_Out(score=999))


class _Asker:
    spec = NodeSpec(
        type="test.ask_after",
        category=NodeCategory.DATA,
        display_name="ask",
        description="pauses once",
        input_schema=_In,
        output_schema=_In,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_In]:
        # The answer to the pause becomes this step's output on resume.
        raise GraphInterrupt(ctx.node_id, {"question": "go on?"})


@pytest.fixture
def store() -> Iterator[MemoryStepResultStore]:
    s = MemoryStepResultStore()
    configure_step_result_store(s)
    knobs._cache[knobs.ONCE_FEATURE] = (
        time.monotonic() + 10**9,
        {"lease_seconds": 5, "wait_poll_seconds": 1, "keep_days_default": 30},
    )
    try:
        yield s
    finally:
        configure_step_result_store(None)
        knobs._cache.pop(knobs.ONCE_FEATURE, None)


def _registry(*steps: Any) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for s in steps:
        reg.register(s, overwrite=True)
    return reg


def _chain(once: dict[str, Any] | None = None) -> Definition:
    pay_data: dict[str, Any] = {"config": {}}
    if once is not None:
        pay_data["once"] = once
    return Definition.model_validate(
        {
            "nodes": [
                {"id": "double", "type": "data.transform", "position": {"x": 0, "y": 0},
                 "data": {"config": {"expression": "inputs['value'] * 2"}}},
                {"id": "pay", "type": "test.paid_ai", "position": {"x": 1, "y": 0}, "data": pay_data},
                {"id": "plus1", "type": "data.transform", "position": {"x": 2, "y": 0},
                 "data": {"config": {"expression": "inputs['score'] + 1"}}},
            ],
            "edges": [
                {"id": "e1", "source": "double", "target": "pay"},
                {"id": "e2", "source": "pay", "target": "plus1"},
            ],
        }
    )


def _scheduler(definition: Definition, reg: NodeRegistry, em: FakeEmitter, cp: MemoryCheckpointer,
               sampled: dict[str, Any] | None) -> Scheduler:
    import dataclasses

    app = dataclasses.replace(make_app_context(em), organization_id=ORG, user_id="test-user")
    return Scheduler(compile_graph(definition, registry=reg), cp, app, registry=reg,
                     definition_id=WF, sampled_outputs=sampled)


def _outcomes(cp: MemoryCheckpointer, run_id: str, node_id: str) -> list[Any]:
    return [o for k, o in cp._outcomes.items() if k[0] == run_id and k[2] == node_id]


def _skipped(em: FakeEmitter, node_id: str) -> list[dict[str, Any]]:
    return [p for (_n, p) in em.events
            if isinstance(p, dict) and p.get("event") == "node_skipped" and p.get("node_id") == node_id]


async def test_a_sampled_paid_step_is_never_called_and_the_next_step_sees_the_sample(store):
    paid = _Paid()
    em, cp = FakeEmitter(), MemoryCheckpointer()
    result = await _scheduler(_chain(), _registry(paid), em, cp, {"pay": {"score": 41}}).run(
        run_id="run-1", inputs={"value": 5}
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert paid.calls == 0, "the sampled paid step was called"
    assert result.last_outputs["plus1"]["result"] == 42, result.last_outputs


async def test_without_samples_the_paid_step_runs_for_real(store):
    paid = _Paid()
    result = await _scheduler(_chain(), _registry(paid), FakeEmitter(), MemoryCheckpointer(), None).run(
        run_id="run-1", inputs={"value": 5}
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert paid.calls == 1
    assert result.last_outputs["plus1"]["result"] == 1000


async def test_the_sampled_outcome_and_event_say_sampled(store):
    em, cp = FakeEmitter(), MemoryCheckpointer()
    await _scheduler(_chain(), _registry(_Paid()), em, cp, {"pay": {"score": 41}}).run(
        run_id="run-1", inputs={"value": 5}
    )
    [outcome] = _outcomes(cp, "run-1", "pay")
    assert outcome.source == "mocked"
    assert outcome.metadata and outcome.metadata["sampled"] is True
    assert "declared sample" in outcome.metadata["reason"]
    [event] = _skipped(em, "pay")
    assert event["sampled"] is True and event["source"] == "mocked"
    assert "declared sample" in (event["reason"] or "")
    # real steps are not flagged
    [real] = _outcomes(cp, "run-1", "plus1")
    assert not (real.metadata or {}).get("sampled")


async def test_a_sampled_once_step_never_writes_the_once_store(store):
    paid = _Paid()
    once = {"key": ["result"], "scope": "workflow"}
    first = await _scheduler(_chain(once), _registry(paid), FakeEmitter(), MemoryCheckpointer(),
                             {"pay": {"score": 41}}).run(run_id="run-1", inputs={"value": 5})
    assert first.status is RunStatus.COMPLETED, first.error
    assert store._rows == {}, "a sample was stored as a reusable result"
    # A later REAL run with the same key pays for real — it never reuses the sample.
    second = await _scheduler(_chain(once), _registry(paid), FakeEmitter(), MemoryCheckpointer(), None).run(
        run_id="run-2", inputs={"value": 5}
    )
    assert second.status is RunStatus.COMPLETED, second.error
    assert paid.calls == 1
    assert second.last_outputs["plus1"]["result"] == 1000


async def test_every_for_each_item_gets_the_sample(store):
    worker = _Paid("test.paid_item")
    definition = Definition.model_validate(
        {
            "nodes": [
                {"id": "fan", "type": "control.map", "position": {"x": 0, "y": 0},
                 "data": {"config": {"target_node_id": "work"}, "input": {"items": ["a", "b", "c"]}}},
                {"id": "work", "type": "test.paid_item", "position": {"x": 1, "y": 0}, "data": {}},
            ],
            "edges": [],
        }
    )
    em, cp = FakeEmitter(), MemoryCheckpointer()
    result = await _scheduler(definition, _registry(worker), em, cp, {"work": {"score": 7}}).run(run_id="run-1")
    assert result.status is RunStatus.COMPLETED, result.error
    assert worker.calls == 0, "a For Each item ran for real"
    items = [e for e in _skipped(em, "work") if e.get("dispatch_id")]
    assert len(items) == 3
    assert all(e["sampled"] and e["output"]["score"] == 7 for e in items)


async def test_a_sample_that_does_not_fit_fails_the_run_naming_the_step(store):
    paid = _Paid()
    result = await _scheduler(_chain(), _registry(paid), FakeEmitter(), MemoryCheckpointer(),
                              {"pay": {"not_score": "x"}}).run(run_id="run-1", inputs={"value": 5})
    assert result.status in (RunStatus.FAILED, RunStatus.ERRORED), result.status
    assert "declared sample for step 'pay'" in (result.error or ""), result.error
    assert paid.calls == 0


async def test_a_resumed_run_answers_the_sampled_step_without_calling_it(store):
    paid = _Paid()
    definition = Definition.model_validate(
        {
            "nodes": [
                {"id": "ask", "type": "test.ask_after", "position": {"x": 0, "y": 0}, "data": {}},
                {"id": "pay", "type": "test.paid_ai", "position": {"x": 1, "y": 0}, "data": {}},
            ],
            "edges": [{"id": "e1", "source": "ask", "target": "pay"}],
        }
    )
    reg = _registry(paid, _Asker())
    cp = MemoryCheckpointer()
    first = await _scheduler(definition, reg, FakeEmitter(), cp, {"pay": {"score": 3}}).run(run_id="run-1")
    assert first.status is RunStatus.INTERRUPTED, first.error
    resumed = await _scheduler(definition, reg, FakeEmitter(), cp, {"pay": {"score": 3}}).resume(
        run_id="run-1", checkpoint_id=(await cp.latest_checkpoint("run-1")).checkpoint_id, resume_value={"ok": True}
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert paid.calls == 0
    assert resumed.last_outputs["pay"]["score"] == 3


# ── A sampled step still runs its executor's pre-send checks (``sample_preflight``) ───────────


class _Refused(Exception):
    """Stands in for a firewall refusal: the executor's own sentence."""


class _Checked(_Paid):
    """A paid step whose executor declares the pre-send check a sampled step still runs."""

    def __init__(self, refuse_over: int | None = None) -> None:
        super().__init__("test.checked_ai")
        self.refuse_over = refuse_over
        self.preflights: list[dict[str, Any]] = []

    async def sample_preflight(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> dict[str, Any]:
        seen = dict(inputs.model_extra or {})
        self.preflights.append(seen)
        if self.refuse_over is not None and seen.get("result", 0) > self.refuse_over:
            raise _Refused("Refused this call: the request carries a term that must not reach the model.")
        return {"scanned": True, "result": seen.get("result")}


def _checked_chain() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {"id": "double", "type": "data.transform", "position": {"x": 0, "y": 0},
                 "data": {"config": {"expression": "inputs['value'] * 2"}}},
                {"id": "pay", "type": "test.checked_ai", "position": {"x": 1, "y": 0}, "data": {"config": {}}},
                {"id": "plus1", "type": "data.transform", "position": {"x": 2, "y": 0},
                 "data": {"config": {"expression": "inputs['score'] + 1"}}},
            ],
            "edges": [
                {"id": "e1", "source": "double", "target": "pay"},
                {"id": "e2", "source": "pay", "target": "plus1"},
            ],
        }
    )


async def test_a_sampled_steps_preflight_refusal_fails_the_step_and_nothing_runs(store):
    """Break: the sampled branch returns the sample before the inputs are resolved, so a refusal
    the live call would raise is never raised (the blinding wall unprovable without spending)."""
    checked = _Checked(refuse_over=5)
    em, cp = FakeEmitter(), MemoryCheckpointer()
    result = await _scheduler(_checked_chain(), _registry(checked), em, cp, {"pay": {"score": 41}}).run(
        run_id="run-1", inputs={"value": 5}
    )
    assert result.status in (RunStatus.FAILED, RunStatus.ERRORED), result.status
    assert "must not reach the model" in (result.error or ""), result.error
    assert checked.calls == 0, "the executor ran for real"
    assert checked.preflights == [{"result": 10}], "the preflight did not see the resolved upstream input"
    [outcome] = _outcomes(cp, "run-1", "pay")
    assert outcome.error and outcome.error["code"] == "_Refused"
    assert not _outcomes(cp, "run-1", "plus1"), "a step after the refusal ran"


async def test_a_clean_preflight_answers_from_the_sample_and_records_the_scan(store):
    checked = _Checked(refuse_over=100)
    em, cp = FakeEmitter(), MemoryCheckpointer()
    result = await _scheduler(_checked_chain(), _registry(checked), em, cp, {"pay": {"score": 41}}).run(
        run_id="run-1", inputs={"value": 5}
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert checked.calls == 0
    assert result.last_outputs["plus1"]["result"] == 42
    [outcome] = _outcomes(cp, "run-1", "pay")
    assert outcome.metadata["sampled"] is True
    assert outcome.metadata["preflight"] == {"scanned": True, "result": 10}


async def test_a_real_run_never_calls_the_preflight(store):
    checked = _Checked(refuse_over=5)
    result = await _scheduler(_checked_chain(), _registry(checked), FakeEmitter(), MemoryCheckpointer(), None).run(
        run_id="run-1", inputs={"value": 5}
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert checked.calls == 1 and checked.preflights == []

"""Run once per key (``data.once``) — the real Scheduler, the real in-memory store.

Every behavior the approved design names (common-docs/systems/workflows/projects/generic-only/
PRIMITIVES-ONCE-PER-KEY-AND-CLI.md § Part 1) is driven through ``Scheduler.run`` / ``resume``:
reuse across runs, scope, the input digest (inputs, config, step version, the step's own
answer version), concurrency (one pays, one reuses), a dead claimer, failures and mocks never
stored, organization isolation, fan-out with per-item keys, resume / fork / fresh-result
interactions. Nothing under test is mocked: steps are real executors that count their calls.
"""

from __future__ import annotations

import asyncio
import dataclasses
import time
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict, ValidationError, create_model

from matrx_graph import (
    CompilationError,
    Definition,
    GraphInterrupt,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
    run_log,
)
from matrx_graph import knobs
from matrx_graph.checkpoint.protocol import Checkpoint, NextInvocation
from matrx_graph.once import (
    ClaimPosition,
    MemoryStepResultStore,
    StepResultKey,
    configure_step_result_store,
    result_key,
    parse_once,
    settings_digest,
)
from matrx_graph.run_log import RunLogEntry
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, failure, success
from tests._fixtures import FakeEmitter, make_app_context

ORG_A = "11111111-1111-4111-8111-111111111111"
ORG_B = "22222222-2222-4222-8222-222222222222"
WF = "33333333-3333-4333-8333-333333333333"


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tone: str = "plain"


class _Out(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Step:
    """A paid step: counts every real execution, answers from its inputs."""

    def __init__(
        self,
        node_type: str = "test.paid",
        *,
        delay: float = 0.0,
        fail_times: int = 0,
        category: NodeCategory = NodeCategory.DATA,
        version: str = "1.0.0",
        big: int = 0,
    ) -> None:
        self.spec = NodeSpec(
            type=node_type,
            category=category,
            display_name=node_type,
            description="once-per-key test step",
            input_schema=_In,
            output_schema=_Out,
            config_schema=_Cfg,
            handles=(
                HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
                HandleSpec(id="out", direction=HandleDirection.OUTPUT),
            ),
            determinism=ActionTier.NON_DETERMINISTIC,
            retry=RetryPolicy(max_attempts=1),
            version=version,
        )
        self.delay = delay
        self.fail_times = fail_times
        self.big = big
        self.calls = 0
        self.seen: list[dict[str, Any]] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        self.seen.append(inputs.model_dump(mode="json"))
        if self.delay:
            await asyncio.sleep(self.delay)
        if self.calls <= self.fail_times:
            return failure(code="Boom", message="the provider refused")
        data = inputs.model_dump(mode="json")
        out: dict[str, Any] = {"echo": data, "tone": config.tone, "call": self.calls}
        if self.big:
            out["blob"] = "x" * self.big
        return success(_Out(**out))


class _Versioned(_Step):
    """An AI-category step that names what answers it (the agent revision)."""

    def __init__(self) -> None:
        super().__init__("test.ai_versioned", category=NodeCategory.AGENT)
        self.answer_version = "agent-rev-1"

    async def result_version(self, ctx: Any, inputs: Any, config: Any) -> str:
        return self.answer_version


class _Asker(_Step):
    def __init__(self) -> None:
        super().__init__("test.ask")

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        raise GraphInterrupt(ctx.node_id, {"question": "go on?"})


class _Recorder:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    async def __call__(self, **kw: Any) -> RunLogEntry:
        self.rows.append(kw)
        return RunLogEntry(recorded=True, entry_id=str(len(self.rows)), label=kw["label"], needs_review=kw["needs_review"])

    def labels(self) -> list[str]:
        return [r["label"] for r in self.rows if r["needs_review"]]


@pytest.fixture
def store() -> Iterator[MemoryStepResultStore]:
    s = MemoryStepResultStore()
    configure_step_result_store(s)
    # lease 5 s (the knob's floor), waiters re-check every second.
    knobs._cache[knobs.ONCE_FEATURE] = (
        time.monotonic() + 10**9,
        {"lease_seconds": 5, "wait_poll_seconds": 1, "keep_days_default": 30, "miss_compare_limit": 10},
    )
    try:
        yield s
    finally:
        configure_step_result_store(None)
        knobs._cache.pop(knobs.ONCE_FEATURE, None)


@pytest.fixture
def flags() -> Iterator[_Recorder]:
    rec = _Recorder()
    run_log.configure_run_log_writer(rec)
    try:
        yield rec
    finally:
        run_log.configure_run_log_writer(None)


def _registry(*steps: _Step) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for s in steps:
        reg.register(s, overwrite=True)
    return reg


def _definition(once: Any, *, inputs: dict[str, Any] | None = None, node_type: str = "test.paid",
                config: dict[str, Any] | None = None, extra_nodes: list[dict[str, Any]] | None = None,
                edges: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    data: dict[str, Any] = {"config": config or {}, "input": inputs or {}}
    if once is not None:
        data["once"] = once
    return {
        "nodes": [{"id": "pay", "type": node_type, "position": {"x": 0, "y": 0}, "data": data}, *(extra_nodes or [])],
        "edges": edges or [],
    }


def _ctx(emitter: FakeEmitter, org: str | None = ORG_A, user: str = "test-user") -> Any:
    return dataclasses.replace(make_app_context(emitter), organization_id=org, user_id=user)


async def _run(definition: dict[str, Any], registry: NodeRegistry, run_id: str, *, org: str | None = ORG_A,
               checkpointer: MemoryCheckpointer | None = None, emitter: FakeEmitter | None = None,
               definition_id: str = WF, user: str = "test-user", run_inputs: dict[str, Any] | None = None):
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    em = emitter or FakeEmitter()
    cp = checkpointer or MemoryCheckpointer()
    scheduler = Scheduler(graph, cp, _ctx(em, org, user), registry=registry, definition_id=definition_id)
    return await scheduler.run(run_id=run_id, inputs=run_inputs), cp, em


def _completed(em: FakeEmitter, node_id: str = "pay") -> list[dict[str, Any]]:
    return [p for (_n, p) in em.events
            if isinstance(p, dict) and p.get("event") == "node_completed" and p.get("node_id") == node_id]


async def _outcome(cp: MemoryCheckpointer, run_id: str, node_id: str = "pay") -> Any:
    """The latest successful outcome of ``node_id`` in ``run_id`` (whatever step it ran at)."""
    found = [o for k, o in cp._outcomes.items() if k[0] == run_id and k[2] == node_id]
    assert found, f"no outcome for {node_id} in {run_id}"
    return sorted(found, key=lambda o: (o.step, o.attempt))[-1]


ONCE = {"key": ["topic"], "scope": "workflow"}


def _stored_key(graph: Any, inputs: dict[str, Any], *, user: str = "test-user") -> str:
    """The key ``pay`` stores under: its settings (default config) and the acting user are part of it."""
    node = graph.nodes["pay"]
    key_value, _ = result_key(
        "test.paid", node.once, inputs,
        settings=settings_digest(node.config.model_dump(mode="json"), node.output_kind), actor=user,
    )
    assert key_value is not None
    return key_value


# ── the basic promise ────────────────────────────────────────────────────────


def test_saved_output_ingestion_keeps_tagged_dump_and_rejects_other_extra_fields():
    from matrx_graph.executor.scheduler import _coerce_replayed_output

    child = create_model("SavedChild", __config__=ConfigDict(extra="forbid"), value=(str, ...))
    parent = create_model("SavedParent", __config__=ConfigDict(extra="forbid"), child=(child, ...))
    payload = {"__kind": "parent", "child": {"__kind": "child", "value": "kept"}}
    model = _coerce_replayed_output(parent, payload)
    assert model.child.value == "kept"
    assert payload == {"__kind": "parent", "child": {"__kind": "child", "value": "kept"}}
    with pytest.raises(ValidationError):
        _coerce_replayed_output(parent, {**payload, "unexpected": True})


async def test_second_run_with_the_same_key_reuses_and_says_where_from(store, flags):
    paid = _Step()
    definition = _definition(ONCE, inputs={"topic": "tides"})
    first, cp1, _ = await _run(definition, _registry(paid), "run-1")
    assert first.status is RunStatus.COMPLETED, first.error
    second, cp2, em2 = await _run(definition, _registry(paid), "run-2")
    assert second.status is RunStatus.COMPLETED, second.error
    assert paid.calls == 1, "the second run paid again for the same key"
    outcome = await _outcome(cp2, "run-2")
    assert outcome.source == "reused"
    assert outcome.metadata["reused_from"]["run_id"] == "run-1"
    assert outcome.metadata["reused_from"]["node_id"] == "pay"
    assert outcome.output["call"] == 1  # the origin's own answer, byte for byte
    [event] = _completed(em2)
    assert event["source"] == "reused" and event["reused_from"]["run_id"] == "run-1"
    assert second.last_outputs["pay"]["call"] == 1
    assert flags.labels() == []


async def test_a_different_key_runs(store, flags):
    paid = _Step()
    await _run(_definition(ONCE, inputs={"topic": "tides"}), _registry(paid), "run-1")
    await _run(_definition(ONCE, inputs={"topic": "moons"}), _registry(paid), "run-2")
    assert paid.calls == 2


async def test_without_the_setting_nothing_is_reused(store):
    paid = _Step()
    await _run(_definition(None, inputs={"topic": "tides"}), _registry(paid), "run-1")
    await _run(_definition(None, inputs={"topic": "tides"}), _registry(paid), "run-2")
    assert paid.calls == 2
    assert store.rows() == {}


async def test_run_scope_never_crosses_runs(store):
    paid = _Step()
    definition = _definition({"key": ["topic"], "scope": "run"}, inputs={"topic": "tides"})
    await _run(definition, _registry(paid), "run-1")
    await _run(definition, _registry(paid), "run-2")
    assert paid.calls == 2


async def test_workflow_scope_does_not_cross_workflows_but_organization_scope_does(store):
    paid = _Step()
    other_wf = "44444444-4444-4444-8444-444444444444"
    wf_scoped = _definition({"key": ["topic"], "scope": "workflow"}, inputs={"topic": "tides"})
    await _run(wf_scoped, _registry(paid), "run-1")
    await _run(wf_scoped, _registry(paid), "run-2", definition_id=other_wf)
    assert paid.calls == 2
    org_scoped = _definition({"key": ["topic"], "scope": "organization"}, inputs={"topic": "reefs"})
    await _run(org_scoped, _registry(paid), "run-3")
    await _run(org_scoped, _registry(paid), "run-4", definition_id=other_wf)
    assert paid.calls == 3


async def test_never_crosses_organizations_even_for_the_same_workflow(store):
    paid = _Step()
    for scope in ("workflow", "organization"):
        definition = _definition({"key": ["topic"], "scope": scope}, inputs={"topic": f"t-{scope}"})
        await _run(definition, _registry(paid), f"a-{scope}", org=ORG_A)
        await _run(definition, _registry(paid), f"b-{scope}", org=ORG_B)
    assert paid.calls == 4
    assert {k.organization_id for k in store.rows()} == {ORG_A, ORG_B}


async def test_a_run_without_an_organization_runs_and_is_flagged(store, flags):
    paid = _Step()
    definition = _definition(ONCE, inputs={"topic": "tides"})
    await _run(definition, _registry(paid), "run-1", org=None)
    await _run(definition, _registry(paid), "run-2", org=None)
    assert paid.calls == 2
    assert flags.labels().count("engine.once_unavailable") == 2


# ── the input digest ─────────────────────────────────────────────────────────


async def test_same_key_different_inputs_runs_again_flags_and_replaces(store, flags):
    paid = _Step()
    await _run(_definition(ONCE, inputs={"topic": "tides", "depth": 1}), _registry(paid), "run-1")
    second, cp, _ = await _run(_definition(ONCE, inputs={"topic": "tides", "depth": 2}), _registry(paid), "run-2")
    assert paid.calls == 2
    assert (await _outcome(cp, "run-2")).source == "executor"
    assert flags.labels() == ["engine.once_inputs_changed"]
    # The replacement is now the saved result: the same new inputs reuse it.
    _, cp3, _ = await _run(_definition(ONCE, inputs={"topic": "tides", "depth": 2}), _registry(paid), "run-3")
    assert paid.calls == 2
    assert (await _outcome(cp3, "run-3")).metadata["reused_from"]["run_id"] == "run-2"


async def test_reuse_and_flag_reuses_for_different_inputs_and_flags(store, flags):
    paid = _Step()
    once = {**ONCE, "on_changed_inputs": "reuse_and_flag"}
    await _run(_definition(once, inputs={"topic": "tides", "depth": 1}), _registry(paid), "run-1")
    _, cp, _ = await _run(_definition(once, inputs={"topic": "tides", "depth": 2}), _registry(paid), "run-2")
    assert paid.calls == 1
    assert (await _outcome(cp, "run-2")).source == "reused"
    assert flags.labels() == ["engine.once_inputs_changed"]


async def test_steps_set_up_differently_keep_their_own_results_and_never_false_flag(store, flags):
    """Settings are part of the key (ruling 2026-10-26): two steps of the same type with different
    settings never replace each other or raise 'inputs changed'; each reuses its own."""
    paid = _Step()
    plain = _definition(ONCE, inputs={"topic": "tides"}, config={"tone": "plain"})
    warm = _definition(ONCE, inputs={"topic": "tides"}, config={"tone": "warm"})
    await _run(plain, _registry(paid), "run-1")
    await _run(warm, _registry(paid), "run-2")
    assert paid.calls == 2
    assert len(store.rows()) == 2
    _, cp, _ = await _run(plain, _registry(paid), "run-3")
    _, cp4, _ = await _run(warm, _registry(paid), "run-4")
    assert paid.calls == 2, "the two set-ups replaced each other"
    assert (await _outcome(cp, "run-3")).output["tone"] == "plain"
    assert (await _outcome(cp4, "run-4")).output["tone"] == "warm"
    assert flags.labels() == []


async def test_a_new_step_version_is_a_miss(store, flags):
    v1, v2 = _Step(version="1.0.0"), _Step(version="1.1.0")
    await _run(_definition(ONCE, inputs={"topic": "tides"}), _registry(v1), "run-1")
    await _run(_definition(ONCE, inputs={"topic": "tides"}), _registry(v2), "run-2")
    assert v1.calls == 1 and v2.calls == 1
    assert flags.labels() == ["engine.once_inputs_changed"]


async def test_an_ai_step_reuses_only_while_the_same_version_answers(store, flags):
    ai = _Versioned()
    definition = _definition(ONCE, inputs={"topic": "tides"}, node_type="test.ai_versioned")
    await _run(definition, _registry(ai), "run-1")
    await _run(definition, _registry(ai), "run-2")
    assert ai.calls == 1
    ai.answer_version = "agent-rev-2"  # a prompt / model edit on the agent
    await _run(definition, _registry(ai), "run-3")
    assert ai.calls == 2
    assert flags.labels() == ["engine.once_inputs_changed"]


async def test_an_ai_step_that_cannot_name_its_version_never_reuses(store, flags):
    blind = _Step("test.ai_blind", category=NodeCategory.LLM)
    definition = _definition(ONCE, inputs={"topic": "tides"}, node_type="test.ai_blind")
    await _run(definition, _registry(blind), "run-1")
    await _run(definition, _registry(blind), "run-2")
    assert blind.calls == 2
    assert flags.labels() == ["engine.once_unversioned", "engine.once_unversioned"]
    assert store.rows() == {}


async def test_a_missing_key_part_runs_and_flags(store, flags):
    paid = _Step()
    definition = _definition({"key": ["topic", "build_id"]}, inputs={"topic": "tides"})
    await _run(definition, _registry(paid), "run-1")
    await _run(definition, _registry(paid), "run-2")
    assert paid.calls == 2
    assert flags.labels() == ["engine.once_key_missing", "engine.once_key_missing"]


async def test_an_empty_key_means_the_whole_input(store):
    paid = _Step()
    await _run(_definition(True, inputs={"topic": "tides"}), _registry(paid), "run-1")
    await _run(_definition(True, inputs={"topic": "tides"}), _registry(paid), "run-2")
    await _run(_definition(True, inputs={"topic": "moons"}), _registry(paid), "run-3")
    assert paid.calls == 2


# ── never stored ─────────────────────────────────────────────────────────────


async def test_a_failure_is_never_stored_and_the_next_run_pays(store):
    paid = _Step(fail_times=1)
    definition = _definition(ONCE, inputs={"topic": "tides"})
    first, _, _ = await _run(definition, _registry(paid), "run-1")
    assert first.status is RunStatus.ERRORED
    assert store.rows() == {}, "a failed claim was left behind"
    second, cp, _ = await _run(definition, _registry(paid), "run-2")
    assert second.status is RunStatus.COMPLETED
    assert paid.calls == 2
    assert (await _outcome(cp, "run-2")).source == "executor"


async def test_a_mocked_or_skipped_step_is_never_stored(store):
    paid = _Step()
    mocked = _definition(ONCE, inputs={"topic": "tides"})
    mocked["nodes"][0]["data"]["mock_response"] = {"enabled": True, "output": {"echo": "mock"}}
    await _run(mocked, _registry(paid), "run-1")
    assert store.rows() == {}
    graph = compile_graph(Definition.model_validate(_definition(ONCE, inputs={"topic": "tides"})),
                          registry=_registry(paid))
    sched = Scheduler(graph, MemoryCheckpointer(), _ctx(FakeEmitter()), registry=_registry(paid),
                      definition_id=WF, skip_node_ids={"pay"})
    await sched.run(run_id="run-2")
    assert store.rows() == {}
    assert paid.calls == 0


def test_an_invalid_setting_fails_compilation():
    reg = _registry(_Step())
    for bad in ({"scope": "galaxy"}, {"key": [""]}, {"keep_days": 0}, {"surprise": 1}, "yes"):
        with pytest.raises(CompilationError, match="invalid once setting"):
            compile_graph(Definition.model_validate(_definition(bad)), registry=reg)


def test_keep_days_absent_reads_the_knob_and_null_means_forever():
    assert parse_once({"key": ["a"]}).keep_days_from_knob is True
    forever = parse_once({"key": ["a"], "keep_days": None})
    assert forever.keep_days is None and forever.keep_days_from_knob is False
    assert parse_once({"key": "a"}).key == ["a"]


async def test_an_expired_result_is_a_miss(store):
    paid = _Step()
    definition = _definition({**ONCE, "keep_days": 1}, inputs={"topic": "tides"})
    await _run(definition, _registry(paid), "run-1")
    [key] = store.rows()
    row = store.rows()[key]
    store._rows[key] = dataclasses.replace(
        row, result=dataclasses.replace(row.result, expires_at=datetime.now(UTC) - timedelta(seconds=1))
    )
    await _run(definition, _registry(paid), "run-2")
    assert paid.calls == 2


# ── concurrency ──────────────────────────────────────────────────────────────


async def test_two_concurrent_runs_with_the_same_key_pay_once(store):
    paid = _Step(delay=0.3)
    definition = _definition(ONCE, inputs={"topic": "tides"})
    (r1, cp1, _), (r2, cp2, _) = await asyncio.gather(
        _run(definition, _registry(paid), "run-1"), _run(definition, _registry(paid), "run-2")
    )
    assert r1.status is RunStatus.COMPLETED and r2.status is RunStatus.COMPLETED
    assert paid.calls == 1, "both concurrent runs paid"
    sources = sorted([(await _outcome(cp1, "run-1")).source, (await _outcome(cp2, "run-2")).source])
    assert sources == ["executor", "reused"]


async def test_a_waiter_pays_when_the_claimer_fails(store):
    paid = _Step(delay=0.2, fail_times=1)
    definition = _definition(ONCE, inputs={"topic": "tides"})
    (r1, _, _), (r2, _, _) = await asyncio.gather(
        _run(definition, _registry(paid), "run-1"), _run(definition, _registry(paid), "run-2")
    )
    statuses = sorted([r1.status.value, r2.status.value])
    assert statuses == sorted([RunStatus.COMPLETED.value, RunStatus.ERRORED.value])
    assert paid.calls == 2
    [row] = store.rows().values()
    assert row.result is not None and row.claim_token is None


async def test_a_dead_claimer_frees_the_key_when_its_lease_expires(store):
    paid = _Step()
    definition = _definition(ONCE, inputs={"topic": "tides"})
    graph = compile_graph(Definition.model_validate(definition), registry=_registry(paid))
    key_value = _stored_key(graph, {"topic": "tides"})
    key = StepResultKey(organization_id=ORG_A, scope="workflow", scope_id=WF, step_type="test.paid",
                        result_key=key_value)
    # A server that claimed the key and died: no renewal, no release.
    assert await store.insert_claim(
        key, token="dead", position=ClaimPosition(run_id="crashed-run", node_id="pay"),
        lease_until=datetime.now(UTC) + timedelta(seconds=0.6),
    )
    started = time.monotonic()
    result, cp, _ = await _run(definition, _registry(paid), "run-1")
    waited = time.monotonic() - started
    assert result.status is RunStatus.COMPLETED
    assert paid.calls == 1
    assert waited >= 0.5, f"did not wait for the live claim ({waited:.2f}s)"
    assert (await _outcome(cp, "run-1")).source == "executor"
    assert store.rows()[key].claim_token is None and store.rows()[key].result is not None


async def test_my_own_crashed_claim_is_taken_over_at_once(store):
    paid = _Step()
    definition = _definition(ONCE, inputs={"topic": "tides"})
    graph = compile_graph(Definition.model_validate(definition), registry=_registry(paid))
    key_value = _stored_key(graph, {"topic": "tides"})
    key = StepResultKey(organization_id=ORG_A, scope="workflow", scope_id=WF, step_type="test.paid",
                        result_key=key_value)
    await store.insert_claim(key, token="mine-before-crash", position=ClaimPosition(run_id="run-1", node_id="pay"),
                             lease_until=datetime.now(UTC) + timedelta(minutes=5))
    started = time.monotonic()
    await _run(definition, _registry(paid), "run-1")
    assert time.monotonic() - started < 2.0
    assert paid.calls == 1


async def test_fan_out_duplicates_collapse_onto_one_claim_with_per_item_keys(store):
    worker = _Step("test.item", delay=0.05)
    definition = {
        "nodes": [
            {"id": "fan", "type": "control.map", "position": {"x": 0, "y": 0},
             "data": {"config": {"target_node_id": "work"}, "input": {"items": ["a", "b", "a", "c", "b"]}}},
            {"id": "work", "type": "test.item", "position": {"x": 1, "y": 0},
             "data": {"once": {"key": ["value"], "scope": "run"}}},
        ],
        "edges": [],
    }
    result, cp, em = await _run(definition, _registry(worker), "run-1")
    assert result.status is RunStatus.COMPLETED, result.error
    # ``work`` has no incoming edge, so it also fires once as an entry node with no item —
    # that invocation has no ``value`` (flagged engine.once_key_missing) and is not counted.
    paid_items = sorted(seen["value"] for seen in worker.seen if "value" in seen)
    assert paid_items == ["a", "b", "c"], f"duplicate items each paid: {paid_items}"
    events = [e for e in _completed(em, "work") if e.get("dispatch_id")]
    assert len(events) == 5, "every item still has its own completion"
    assert sorted(e.get("source") or "executor" for e in events) == ["executor"] * 3 + ["reused"] * 2


# ── resume, fork, fresh result ───────────────────────────────────────────────


async def test_resume_replays_the_recorded_position_and_never_asks_the_store(store):
    paid, ask = _Step(), _Asker()
    definition = _definition(
        ONCE, inputs={"topic": "tides"},
        extra_nodes=[{"id": "ask", "type": "test.ask", "position": {"x": 1, "y": 0}, "data": {}}],
        edges=[{"id": "e1", "source": "pay", "target": "ask", "data": {"kind": "data"}}],
    )
    reg = _registry(paid, ask)
    graph = compile_graph(Definition.model_validate(definition), registry=reg)
    cp = MemoryCheckpointer()
    sched = Scheduler(graph, cp, _ctx(FakeEmitter()), registry=reg, definition_id=WF)
    first = await sched.run(run_id="run-1")
    assert first.status is RunStatus.INTERRUPTED
    configure_step_result_store(MemoryStepResultStore())  # the saved results are gone
    latest = await cp.latest_checkpoint("run-1")
    resumed = await Scheduler(graph, cp, _ctx(FakeEmitter()), registry=reg, definition_id=WF).resume(
        run_id="run-1", checkpoint_id=latest.checkpoint_id, resume_value={"ok": True}
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert paid.calls == 1


async def _resume_with(store: MemoryStepResultStore, paid: _Step, run_id: str, **ni: Any):
    """A parked run whose frontier holds ``pay`` again (what Retry / Re-run from / fork with a
    config override produce): resumed through the real Scheduler.resume."""
    definition = _definition(ONCE, inputs={"topic": "tides"})
    reg = _registry(paid)
    graph = compile_graph(Definition.model_validate(definition), registry=reg)
    cp = MemoryCheckpointer()
    await cp.save_checkpoint(Checkpoint(
        checkpoint_id=f"cp-{run_id}", run_id=run_id, thread_id=run_id, step=0, channel_values={},
        next_invocations=[NextInvocation(node_id="pay", inputs={}, step=1, **ni)],
    ))
    em = FakeEmitter()
    result = await Scheduler(graph, cp, _ctx(em), registry=reg, definition_id=WF).resume(
        run_id=run_id, checkpoint_id=f"cp-{run_id}"
    )
    return result, cp, em


async def test_ignore_saved_result_runs_fresh_and_replaces_without_a_flag(store, flags):
    paid = _Step()
    await _run(_definition(ONCE, inputs={"topic": "tides"}), _registry(paid), "run-1")
    result, cp, _ = await _resume_with(store, paid, "run-2", bypass_once=True)
    assert result.status is RunStatus.COMPLETED, result.error
    assert paid.calls == 2
    assert (await _outcome(cp, "run-2")).source == "executor"
    assert flags.labels() == []
    _, cp3, _ = await _run(_definition(ONCE, inputs={"topic": "tides"}), _registry(paid), "run-3")
    assert (await _outcome(cp3, "run-3")).metadata["reused_from"]["run_id"] == "run-2"


async def test_without_the_switch_a_retry_reuses(store):
    paid = _Step()
    await _run(_definition(ONCE, inputs={"topic": "tides"}), _registry(paid), "run-1")
    _, cp, _ = await _resume_with(store, paid, "run-2")
    assert paid.calls == 1
    assert (await _outcome(cp, "run-2")).source == "reused"


async def test_a_fork_with_a_config_override_changes_the_digest(store, flags):
    paid = _Step()
    await _run(_definition(ONCE, inputs={"topic": "tides"}), _registry(paid), "run-1")
    _, cp, _ = await _resume_with(store, paid, "run-2", config_override={"tone": "warm"})
    assert paid.calls == 2
    assert (await _outcome(cp, "run-2")).output["tone"] == "warm"
    assert flags.labels() == []  # other settings are another key, never 'inputs changed'


async def test_a_reused_outcome_replays_on_resume_as_reused(store):
    paid, ask = _Step(), _Asker()
    definition = _definition(
        ONCE, inputs={"topic": "tides"},
        extra_nodes=[{"id": "ask", "type": "test.ask", "position": {"x": 1, "y": 0}, "data": {}}],
        edges=[{"id": "e1", "source": "pay", "target": "ask", "data": {"kind": "data"}}],
    )
    reg = _registry(paid, ask)
    await _run(_definition(ONCE, inputs={"topic": "tides"}), _registry(paid), "run-0")
    graph = compile_graph(Definition.model_validate(definition), registry=reg)
    cp = MemoryCheckpointer()
    first = await Scheduler(graph, cp, _ctx(FakeEmitter()), registry=reg, definition_id=WF).run(run_id="run-1")
    assert first.status is RunStatus.INTERRUPTED
    assert (await _outcome(cp, "run-1")).source == "reused"
    em = FakeEmitter()
    latest = await cp.latest_checkpoint("run-1")
    await Scheduler(graph, cp, _ctx(em), registry=reg, definition_id=WF).resume(
        run_id="run-1", checkpoint_id=latest.checkpoint_id, resume_value={"ok": True}
    )
    assert paid.calls == 1


# ── attack review (2026-10-26): each test below was red on the first build ──────


class _HeldCapture(_Step):
    """A paid step whose output is server-side state (``hold_on_server``), like a provision capture."""

    STATE: dict[str, Any] = {f"v{i}": "z" * 50 for i in range(20)}

    def __init__(self) -> None:
        super().__init__("test.held_capture")

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        from matrx_graph.checkpoint import value_store

        self.calls += 1
        held = await value_store.hold_on_server(ctx.run_id, dict(self.STATE))
        return success(_Out(provision_values=held))


class _HeldReader(_Step):
    def __init__(self) -> None:
        super().__init__("test.held_reader")
        self.received: dict[str, Any] = {}

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        self.received[ctx.run_id] = inputs.model_dump(mode="json").get("provision_values")
        return success(_Out(ok=True))


async def test_a_reused_result_holding_server_values_still_feeds_the_next_step(store, monkeypatch):
    """A held value lives in its ORIGIN run's value store; a run that reuses the result must still
    hand the next step the full value (it used to fail: 'held value … is not stored for this run')."""
    from matrx_graph.checkpoint import value_store

    per_run: dict[tuple[str, str], Any] = {}

    async def _store_values(run_id: str, values: dict[str, Any], *, organization_id: str | None = None) -> None:
        for h, v in values.items():
            per_run[(run_id, h)] = v

    async def _load(run_id: str, hashes: Any) -> dict[str, Any]:
        return {h: per_run[(run_id, h)] for h in hashes if (run_id, h) in per_run}

    monkeypatch.setattr(value_store, "store_run_values", _store_values)
    monkeypatch.setattr(value_store, "load_run_values", _load)
    monkeypatch.setattr(value_store, "_store_available", lambda: True)

    capture, reader = _HeldCapture(), _HeldReader()
    definition = _definition(
        ONCE, inputs={"topic": "acme"}, node_type="test.held_capture",
        extra_nodes=[{"id": "read", "type": "test.held_reader", "position": {"x": 1, "y": 0}, "data": {}}],
        edges=[{"id": "e1", "source": "pay", "target": "read",
                "data": {"kind": "data", "mappings": {"provision_values": "provision_values"}}}],
    )
    first, _, _ = await _run(definition, _registry(capture, reader), "run-1")
    assert first.status is RunStatus.COMPLETED, first.error
    second, cp, _ = await _run(definition, _registry(capture, reader), "run-2")
    assert second.status is RunStatus.COMPLETED, second.error
    assert capture.calls == 1
    assert (await _outcome(cp, "run-2")).source == "reused"
    assert reader.received == {"run-1": _HeldCapture.STATE, "run-2": _HeldCapture.STATE}


async def test_a_reused_result_whose_held_values_are_gone_is_a_miss(store, monkeypatch):
    from matrx_graph.checkpoint import value_store

    per_run: dict[tuple[str, str], Any] = {}

    async def _store_values(run_id: str, values: dict[str, Any], *, organization_id: str | None = None) -> None:
        for h, v in values.items():
            per_run[(run_id, h)] = v

    async def _load(run_id: str, hashes: Any) -> dict[str, Any]:
        return {h: per_run[(run_id, h)] for h in hashes if (run_id, h) in per_run}

    monkeypatch.setattr(value_store, "store_run_values", _store_values)
    monkeypatch.setattr(value_store, "load_run_values", _load)
    monkeypatch.setattr(value_store, "_store_available", lambda: True)

    capture, reader = _HeldCapture(), _HeldReader()
    definition = _definition(
        ONCE, inputs={"topic": "acme"}, node_type="test.held_capture",
        extra_nodes=[{"id": "read", "type": "test.held_reader", "position": {"x": 1, "y": 0}, "data": {}}],
        edges=[{"id": "e1", "source": "pay", "target": "read",
                "data": {"kind": "data", "mappings": {"provision_values": "provision_values"}}}],
    )
    await _run(definition, _registry(capture, reader), "run-1")
    per_run.clear()  # the origin run's value store is gone
    second, cp, _ = await _run(definition, _registry(capture, reader), "run-2")
    assert second.status is RunStatus.COMPLETED, second.error
    assert capture.calls == 2
    assert (await _outcome(cp, "run-2")).source == "executor"
    assert reader.received["run-2"] == _HeldCapture.STATE


class _ReusedWriteFails(MemoryCheckpointer):
    async def record_outcome(self, outcome: Any) -> None:
        if outcome.source == "reused":
            raise RuntimeError("checkpoint write failed")
        await super().record_outcome(outcome)


async def test_a_checkpoint_failure_while_reusing_never_pays_for_the_step_again(store):
    """Recording the reused outcome failed: that is a checkpoint failure like any other — it must
    not be mistaken for a broken store and answered by paying for the step (and announcing it
    completed twice)."""
    paid = _Step()
    definition = _definition(ONCE, inputs={"topic": "tides"})
    await _run(definition, _registry(paid), "run-1")
    em = FakeEmitter()
    await _run(definition, _registry(paid), "run-2", checkpointer=_ReusedWriteFails(), emitter=em)
    assert paid.calls == 1, "the step was paid for again after a reuse half-happened"
    assert len(_completed(em)) <= 1


class _BrokenReadStore(MemoryStepResultStore):
    async def read(self, key: StepResultKey) -> Any:
        raise ConnectionError("step_result store unreachable")


class _BrokenSettleStore(MemoryStepResultStore):
    async def settle(self, key: StepResultKey, *, token: str, result: Any) -> bool:
        raise ConnectionError("step_result store unreachable")


async def test_a_broken_store_is_announced_on_the_run_never_only_in_a_log(flags):
    knobs._cache[knobs.ONCE_FEATURE] = (
        time.monotonic() + 10**9, {"lease_seconds": 5, "wait_poll_seconds": 1, "keep_days_default": 30, "miss_compare_limit": 10},
    )
    try:
        for broken in (_BrokenReadStore(), _BrokenSettleStore()):
            flags.rows.clear()
            configure_step_result_store(broken)
            paid = _Step()
            result, _, _ = await _run(_definition(ONCE, inputs={"topic": "tides"}), _registry(paid), "run-1")
            assert result.status is RunStatus.COMPLETED
            assert paid.calls == 1
            assert "engine.once_unavailable" in flags.labels(), type(broken).__name__
    finally:
        configure_step_result_store(None)
        knobs._cache.pop(knobs.ONCE_FEATURE, None)


class _GoneOriginStore(MemoryStepResultStore):
    """Results whose origin run is in ``gone`` can no longer be read (their value store is gone)."""

    def __init__(self) -> None:
        super().__init__()
        self.gone: set[str] = set()

    async def resolve_output(self, result: Any) -> dict[str, Any]:
        if result.origin_run_id in self.gone:
            raise LookupError("origin values are gone")
        return result.output


async def test_an_unreadable_result_is_replaced_once_and_a_waiter_reuses_the_replacement():
    """Two runs find the same unreadable result. One re-produces it; the other waits and must reuse
    the fresh result — it used to ignore EVERY stored result after the first unreadable one and pay
    a second time."""
    s = _GoneOriginStore()
    configure_step_result_store(s)
    knobs._cache[knobs.ONCE_FEATURE] = (
        time.monotonic() + 10**9, {"lease_seconds": 5, "wait_poll_seconds": 1, "keep_days_default": 30, "miss_compare_limit": 10},
    )
    try:
        paid = _Step(delay=0.3)
        definition = _definition(ONCE, inputs={"topic": "tides"})
        await _run(definition, _registry(paid), "run-0")
        s.gone.add("run-0")
        (r1, _, _), (r2, _, _) = await asyncio.gather(
            _run(definition, _registry(paid), "run-1"), _run(definition, _registry(paid), "run-2")
        )
        assert r1.status is RunStatus.COMPLETED and r2.status is RunStatus.COMPLETED
        assert paid.calls == 2, "both runs re-paid for the unreadable result"
    finally:
        configure_step_result_store(None)
        knobs._cache.pop(knobs.ONCE_FEATURE, None)


class _LosingStore(MemoryStepResultStore):
    """A broken store: every read says 'no row', every insert says 'already there'."""

    async def read(self, key: StepResultKey) -> Any:
        await asyncio.sleep(0)
        return None

    async def insert_claim(self, key: StepResultKey, **kw: Any) -> bool:
        await asyncio.sleep(0)
        return False


async def test_a_store_whose_compare_and_swap_never_lands_raises_instead_of_spinning():
    from matrx_graph.once import StepResultStoreError, acquire

    key = StepResultKey(organization_id=ORG_A, scope="workflow", scope_id=WF, step_type="t", result_key="k")
    with pytest.raises(StepResultStoreError):
        await asyncio.wait_for(
            acquire(_LosingStore(), key, digest="d", position=ClaimPosition(run_id="r", node_id="n"),
                    lease_seconds=5, reuse_changed=False, bypass=False),
            timeout=5,
        )


class _SlowSettleStore(MemoryStepResultStore):
    async def settle(self, key: StepResultKey, *, token: str, result: Any) -> bool:
        ok = await super().settle(key, token=token, result=result)
        await asyncio.sleep(2.2)  # the renewer wakes (every lease/3 = 1.67 s) while settle returns
        return ok


async def test_settling_never_reports_a_lost_claim(caplog):
    s = _SlowSettleStore()
    configure_step_result_store(s)
    knobs._cache[knobs.ONCE_FEATURE] = (
        time.monotonic() + 10**9, {"lease_seconds": 5, "wait_poll_seconds": 1, "keep_days_default": 30, "miss_compare_limit": 10},
    )
    try:
        paid = _Step()
        with caplog.at_level("ERROR"):
            result, _, _ = await _run(_definition(ONCE, inputs={"topic": "tides"}), _registry(paid), "run-1")
        assert result.status is RunStatus.COMPLETED
        assert not [r for r in caplog.records if "LOST the claim" in r.getMessage()]
        [row] = s.rows().values()
        assert row.result is not None
    finally:
        configure_step_result_store(None)
        knobs._cache.pop(knobs.ONCE_FEATURE, None)


# ── rulings (owning session, 2026-10-26): each test below was red before the change ──────


async def test_one_persons_result_is_never_anothers_unless_the_step_shares_it(store):
    paid = _Step()
    definition = _definition(ONCE, inputs={"topic": "tides"})
    await _run(definition, _registry(paid), "run-1", user="user-a")
    _, cp, _ = await _run(definition, _registry(paid), "run-2", user="user-b")
    assert paid.calls == 2, "user B was handed user A's result"
    assert (await _outcome(cp, "run-2")).source == "executor"
    _, cp, _ = await _run(definition, _registry(paid), "run-3", user="user-a")
    assert paid.calls == 2 and (await _outcome(cp, "run-3")).source == "reused"

    shared = _definition({**ONCE, "share_across_users": True}, inputs={"topic": "tides"})
    await _run(shared, _registry(paid), "run-4", user="user-a")
    _, cp, _ = await _run(shared, _registry(paid), "run-5", user="user-b")
    assert paid.calls == 3
    assert (await _outcome(cp, "run-5")).source == "reused"


class _Warns(_Step):
    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        await ctx.warn("test.partial", "two of the three sources answered")
        return success(_Out(call=self.calls))


async def test_a_degraded_result_is_never_saved_and_the_outcome_says_why(store, flags):
    warns = _Warns("test.paid")
    definition = _definition(ONCE, inputs={"topic": "tides"})
    _, cp, _ = await _run(definition, _registry(warns), "run-1")
    outcome = await _outcome(cp, "run-1")
    assert "warning" in (outcome.metadata or {}).get("once_not_saved", "")
    assert store.rows() == {}, "a degraded result was saved for reuse"
    await _run(definition, _registry(warns), "run-2")
    assert warns.calls == 2


def test_a_failed_or_unchecked_shape_is_never_saved():
    from matrx_graph.executor.once_step import OnceSlot, not_saved_reason
    from matrx_graph.once import Claim

    slot = OnceSlot(claim=Claim(key=None, token="t", took_over=False, replacing=None), digest="d")  # type: ignore[arg-type]
    result = dataclasses.make_dataclass("R", [("sends", list)])(sends=[])
    base = dict(slot=slot, result=result, output_dump={"a": 1}, ctx_channel_writes=0, warning_count=0)
    assert not_saved_reason(**base, output_kind_ok=True, output_kind_degraded=None) is None
    assert "shape" in not_saved_reason(**base, output_kind_ok=False, output_kind_degraded=None)
    assert "could not be checked" in not_saved_reason(**base, output_kind_ok=None, output_kind_degraded="registry_unavailable")


def test_an_output_that_says_it_failed_is_never_saved():
    # A fail-soft step (a web search refused by the spend gate) answered {"failed": "..."}; saved, it was
    # replayed for a day after the spend was approved.
    from matrx_graph.executor.once_step import OnceSlot, not_saved_reason
    from matrx_graph.once import Claim

    slot = OnceSlot(claim=Claim(key=None, token="t", took_over=False, replacing=None), digest="d")  # type: ignore[arg-type]
    result = dataclasses.make_dataclass("R", [("sends", list)])(sends=[])
    kw = dict(slot=slot, result=result, ctx_channel_writes=0, warning_count=0, output_kind_ok=True,
              output_kind_degraded=None)
    assert "did not work" in not_saved_reason(**kw, output_dump={"results": [], "failed": "approval waiting"})
    assert "did not work" in not_saved_reason(**kw, output_dump={"error": "boom"})
    assert not_saved_reason(**kw, output_dump={"results": [1], "failed": None, "error": ""}) is None
    assert not_saved_reason(**kw, output_dump={"pages": [1], "failed": 2}) is None  # a tally, not a verdict


def test_an_output_whose_run_metadata_says_it_failed_is_never_saved():
    # Live 2026-10-27, run 477536f8: an AI step's provider stayed overloaded (503); its agent_result carried
    # metadata.status "suspended_provider_overload" + metadata.error, was saved, and the next run reused it in 1 s.
    from matrx_graph.executor.once_step import OnceSlot, not_saved_reason
    from matrx_graph.once import Claim

    slot = OnceSlot(claim=Claim(key=None, token="t", took_over=False, replacing=None), digest="d")  # type: ignore[arg-type]
    result = dataclasses.make_dataclass("R", [("sends", list)])(sends=[])
    kw = dict(slot=slot, result=result, ctx_channel_writes=0, warning_count=0, output_kind_ok=True,
              output_kind_degraded=None)
    overloaded = {"final_text": "echo", "metadata": {"status": "suspended_provider_overload",
                                                     "error": "Google is temporarily overloaded (503)"}}
    assert "did not work" in not_saved_reason(**kw, output_dump=overloaded)
    assert "did not work" in not_saved_reason(**kw, output_dump={"metadata": {"status": "failed"}})
    assert not_saved_reason(**kw, output_dump={"final_text": "ok", "metadata": {"status": "complete", "error": None}}) is None


async def test_a_file_input_is_identified_by_its_content_never_its_id_alone(store, flags):
    from matrx_graph.once import configure_file_identity_resolver

    identity = {"f-1": "sha256:aaa"}

    async def _resolve(ids: set[str], org: str) -> dict[str, str | None]:
        return {i: identity.get(i) for i in ids}

    paid = _Step()
    definition = _definition({"key": ["doc.file_id"]}, inputs={"doc": {"file_id": "f-1"}})
    configure_file_identity_resolver(_resolve)
    try:
        await _run(definition, _registry(paid), "run-1")
        _, cp, _ = await _run(definition, _registry(paid), "run-2")
        assert paid.calls == 1 and (await _outcome(cp, "run-2")).source == "reused"
        identity["f-1"] = "sha256:bbb"  # the file was edited under the same id
        _, cp, _ = await _run(definition, _registry(paid), "run-3")
        assert paid.calls == 2, "an edited file reused the old file's result"
        identity["f-1"] = None  # no content hash, no version
        flags.rows.clear()
        await _run(definition, _registry(paid), "run-4")
        await _run(definition, _registry(paid), "run-5")
        assert paid.calls == 4
        assert flags.labels().count("engine.once_unversioned") == 2
    finally:
        configure_file_identity_resolver(None)

    flags.rows.clear()
    await _run(definition, _registry(paid), "run-6")  # no resolver installed: never reuse, say so
    assert paid.calls == 5 and flags.labels() == ["engine.once_unversioned"]


class _ChannelWriter(_Step):
    """A step that also writes a side channel — run topology, so its result cannot be saved."""

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        result = await super().execute(ctx, inputs, config)
        ctx.channels.write("side_summary", {"seen": True})
        return result


async def test_a_result_that_can_never_be_saved_says_so_on_the_step(store, flags):
    """2026-10-27: Prepare Documents had run-once on, wrote an unread channel, and re-read every
    page on each re-run — the only trace was a field on the outcome row. The author asked for
    once, so the step now raises ``engine.once_not_saved`` naming why."""
    paid = _ChannelWriter()
    definition = _definition(ONCE, inputs={"topic": "tides"})
    first, _cp, _ = await _run(definition, _registry(paid), "run-ch-1")
    assert first.status is RunStatus.COMPLETED, first.error
    second, _cp2, _ = await _run(definition, _registry(paid), "run-ch-2")
    assert second.status is RunStatus.COMPLETED, second.error
    assert paid.calls == 2
    assert "engine.once_not_saved" in flags.labels()


# ── a miss says why: an upstream step answered differently ──────────────────


class _Jittery(_Step):
    """A paid upstream step (a search, an agent) that answers the SAME input a little differently
    each time — the rerank-score jitter that made six identical lanes miss (2026-10-28)."""

    def __init__(self) -> None:
        super().__init__("test.jittery", category=NodeCategory.IO)

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        return success(_Out(hits=[{"chunk": "c1", "score": 0.917 + self.calls / 10_000}]))


def _fed_by_jittery(topic: str = "tides", once: Any = None) -> dict[str, Any]:
    return _definition(
        once or ONCE, inputs={"topic": topic},
        extra_nodes=[{"id": "search", "type": "test.jittery", "position": {"x": 0, "y": 0},
                      "data": {"label": "Retrieve doctrine", "input": {"q": "same"}}}],
        edges=[{"id": "e1", "source": "search", "target": "pay",
                "data": {"kind": "data", "mappings": {"doc": "hits"}}}],
    )


def _missed(flags: _Recorder) -> list[dict[str, Any]]:
    return [r for r in flags.rows if r["needs_review"] and r["label"] == "engine.once_missed_upstream"]


async def test_a_miss_caused_by_an_upstream_step_that_ran_fresh_is_flagged_and_names_it(store, flags):
    paid, search = _Step(), _Jittery()
    definition = _fed_by_jittery()
    definition["nodes"][0]["data"]["label"] = "Assess the lane"
    cp = MemoryCheckpointer()
    first, _, _ = await _run(definition, _registry(paid, search), "run-1", checkpointer=cp)
    assert first.status is RunStatus.COMPLETED, first.error
    assert _missed(flags) == [], "a first run has nothing to compare with — it must not claim a cause"
    second, _, _ = await _run(definition, _registry(paid, search), "run-2", checkpointer=cp)
    assert second.status is RunStatus.COMPLETED, second.error
    assert paid.calls == 2  # the upstream answer changed, so the step honestly ran again
    [flag] = _missed(flags)
    assert flag["node_id"] == "pay"
    assert flag["message"] == (
        "Run once missed: Assess the lane got a different input because Retrieve doctrine ran fresh "
        "in this run, so its saved answer was not reused."
    ), flag["message"]
    assert flag["payload"]["upstream"] == ["search"]
    assert flag["payload"]["fields"] == ["doc"]
    assert flag["payload"]["compared_run_id"] == "run-1"
    assert "engine.once_inputs_changed" not in flags.labels(), "one flag says why, not two"


async def test_a_true_first_run_has_no_earlier_answer_and_raises_no_flag(store, flags):
    """A first run of the step (a fresh brand) had nothing to reuse, so nothing "missed"."""
    paid, search = _Step(), _Jittery()
    first, _, _ = await _run(_fed_by_jittery(once={"scope": "workflow"}), _registry(paid, search), "run-1")
    assert first.status is RunStatus.COMPLETED, first.error
    assert paid.calls == 1
    assert _missed(flags) == [], "no earlier saved answer existed for this step — the flag is noise"


async def test_a_whole_input_step_whose_input_changed_upstream_flags_against_its_earlier_answer(store, flags):
    """``once: true`` (the whole input is the key): a fresh upstream answer makes a NEW key, yet the
    step's earlier saved answer exists — the six assurance lanes (2026-10-28). It must be said."""
    paid, search = _Step(), _Jittery()
    definition = _fed_by_jittery(once={"scope": "workflow"})
    definition["nodes"][0]["data"]["label"] = "Assess the lane"
    cp = MemoryCheckpointer()
    await _run(definition, _registry(paid, search), "run-1", checkpointer=cp)
    await _run(definition, _registry(paid, search), "run-2", checkpointer=cp)
    assert paid.calls == 2
    [flag] = _missed(flags)
    assert flag["message"] == (
        "Run once missed: Assess the lane got a different input because Retrieve doctrine ran fresh "
        "in this run, so its saved answer was not reused."
    ), flag["message"]
    assert flag["payload"]["upstream"] == ["search"] and flag["payload"]["fields"] == ["doc"]
    assert flag["payload"]["compared_run_id"] == "run-1"


async def test_a_fresh_subject_in_workflow_scope_with_other_subjects_answers_raises_no_flag(store, flags):
    """A fresh brand: the workflow's run inputs differ from every earlier run that saved an answer
    for this step, so its new input is a new subject, not a miss — even though the brand reaches
    the step only through a fresh upstream answer."""
    paid, search = _Step(), _Jittery()
    definition = _fed_by_jittery(once={"scope": "workflow"})
    cp = MemoryCheckpointer()
    await _run(definition, _registry(paid, search), "run-1", checkpointer=cp, run_inputs={"brand": "Acme"})
    await _run(definition, _registry(paid, search), "run-2", checkpointer=cp, run_inputs={"brand": "Globex"})
    assert paid.calls == 2
    assert _missed(flags) == [], "a new brand had no earlier answer of its own to reuse"


async def test_a_miss_from_the_steps_own_new_input_is_not_blamed_on_upstream(store, flags):
    paid, search = _Step(), _Jittery()
    cp = MemoryCheckpointer()
    await _run(_fed_by_jittery("tides"), _registry(paid, search), "run-1", checkpointer=cp)
    await _run(_fed_by_jittery("storms"), _registry(paid, search), "run-2", checkpointer=cp)
    assert paid.calls == 2
    assert _missed(flags) == [], "the step's own input changed — blaming the upstream step would be a lie"

"""ENGINE_SPEC §4 (fan-out/fan-in identity, fixes audit E2) + §5 (emission
durability, fixes audit E3) + §12 acceptance criteria 2/3.

Every invocation carries a durable correlation ``(dispatch_id, item_index)``
separate from ``attempt``:

    * ``control.map`` / ``ctx.send`` mint ONE dispatch_id per dispatching
      invocation and stamp each Send with its item_index; both persist inside
      the dispatcher's recorded ``NodeOutcome.sends`` so crash-replay reuses
      the SAME identity (byte-identical routing).
    * ``NodeOutcome`` keying extends to
      ``(run_id, step, node_id, dispatch_id, item_index, attempt)`` — sibling
      fan-out items can no longer replay or overwrite each other's outcomes
      (the E2 ``['ALPHA','GAMMA','GAMMA']`` corruption class).
    * ``attempt`` returns to its true meaning: a retry counter starting at 1
      within a fixed correlation key (Temporal precedent).
    * Fan-in (§4.4): a fanned chain's edge into a downstream node delivers as
      ONE logical upstream that resolves only when ALL items of the dispatch
      resolved; the payload is the index-ordered ``{"items": [...]}`` list
      with explicit hole entries for skipped items — never silent absence.
    * Emissions (§5): ``NodeOutcome.emissions`` persists ``ctx.emit`` handle
      routing; idempotency replay restores it so branch decisions survive
      errored-park resume, crash replay, and step-mode replay.
    * §4.6: ``NodeDef.data.concurrency`` caps concurrent invocations of one
      node inside a super-step, nested under run-level ``step_concurrency``.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any, ClassVar
from uuid import uuid4

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
from matrx_graph.checkpoint.protocol import Checkpoint, NodeOutcome
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context

# Load the repo .env HERE, above the gate. The skip decision below reads
# process env, and other suites (anything importing aidream.config) load .env
# as an import side effect — so without this line the same commit skips when
# this file is collected alone and runs when it is collected second.
# Guard: scripts/check_test_gate_determinism.py
from dotenv import load_dotenv

load_dotenv()


class _WorkerInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str = ""


class _WorkerOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    result: str = ""


class _WorkerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _FanoutWorker:
    """Uppercases each item; optionally fails per (value, attempt).

    ``fail_on`` maps an input value to the attempts that should raise, e.g.
    ``{"beta": {1}}`` = transient failure on beta's first attempt only, or
    ``{"beta": None}`` = beta always fails. Records every payload actually
    processed as ``(value, attempt)`` — the spy that proves the engine really
    executed an item instead of replaying a sibling's outcome (audit E2).
    """

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.fanout_worker",
        category=NodeCategory.DATA,
        display_name="Fan-out worker",
        description="Uppercases one fanned item; configurable transient failure.",
        input_schema=_WorkerInput,
        output_schema=_WorkerOutput,
        config_schema=_WorkerConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self, fail_on: dict[str, set[int] | None] | None = None) -> None:
        self.fail_on = fail_on or {}
        self.processed: list[tuple[str, int]] = []
        self.live = 0
        self.peak_live = 0
        self.sleep_s = 0.0

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: _WorkerInput,
        _config: _WorkerConfig,
    ) -> NodeResult[_WorkerOutput]:
        self.live += 1
        self.peak_live = max(self.peak_live, self.live)
        try:
            if self.sleep_s:
                await asyncio.sleep(self.sleep_s)
            self.processed.append((inputs.value, ctx.attempt))
            if inputs.value in self.fail_on:
                attempts = self.fail_on[inputs.value]
                if attempts is None or ctx.attempt in attempts:
                    raise RuntimeError(
                        f"transient failure on {inputs.value!r} attempt {ctx.attempt}"
                    )
            return success(_WorkerOutput(result=inputs.value.upper()))
        finally:
            self.live -= 1


class _RecorderInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _RecorderOutput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _RecorderConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Recorder:
    """Echo node recording every invocation's routed inputs."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.fanout_recorder",
        category=NodeCategory.DATA,
        display_name="Fan-out recorder",
        description="Records each invocation's inputs.",
        input_schema=_RecorderInput,
        output_schema=_RecorderOutput,
        config_schema=_RecorderConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        inputs: _RecorderInput,
        _config: _RecorderConfig,
    ) -> NodeResult[_RecorderOutput]:
        dump = inputs.model_dump(mode="json")
        self.calls.append(dump)
        return success(_RecorderOutput(**dump))


class _FlakySibling:
    """Fails on attempt 1, succeeds on attempt 2 — drives an ERRORED park."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.flaky_sibling",
        category=NodeCategory.DATA,
        display_name="Flaky sibling",
        description="Fails on attempt 1 to force an errored park.",
        input_schema=_RecorderInput,
        output_schema=_RecorderOutput,
        config_schema=_RecorderConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self, fail_after_s: float = 0.0) -> None:
        self.fail_after_s = fail_after_s

    async def execute(
        self,
        ctx: NodeExecutionContext,
        _inputs: _RecorderInput,
        _config: _RecorderConfig,
    ) -> NodeResult[_RecorderOutput]:
        if ctx.attempt == 1:
            await asyncio.sleep(self.fail_after_s)
            raise RuntimeError("flaky sibling: transient failure on attempt 1")
        return success(_RecorderOutput())


def _registry(
    worker: _FanoutWorker | None = None,
) -> tuple[NodeRegistry, _FanoutWorker]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    worker = worker or _FanoutWorker()
    reg.register(worker, overwrite=True)
    return reg, worker


def _map_definition(
    items: list[Any],
    *,
    worker_data: dict[str, Any] | None = None,
    with_gather: bool = True,
) -> Definition:
    """map(fanout) --Send--> worker --edge--> gather (§4.4 aggregated fan-in)."""
    nodes: list[dict[str, Any]] = [
        {
            "id": "fanout",
            "type": "control.map",
            "position": {"x": 0, "y": 0},
            "data": {
                "config": {"target_node_id": "worker", "payload_key": "value"},
                "input": {"items": items},
            },
        },
        {
            "id": "worker",
            "type": "test.fanout_worker",
            "position": {"x": 200, "y": 0},
            "data": {"config": {}, **(worker_data or {})},
        },
    ]
    edges: list[dict[str, Any]] = []
    if with_gather:
        nodes.append(
            {
                "id": "gather",
                "type": "control.gather",
                "position": {"x": 400, "y": 0},
                "data": {"config": {}},
            }
        )
        edges.append(
            {
                "id": "e_wg",
                "source": "worker",
                "target": "gather",
                "data": {"mappings": {"value": "result"}},
            }
        )
    return Definition.model_validate({"nodes": nodes, "edges": edges, "entry_nodes": ["fanout"]})


def _scheduler(
    definition: Definition,
    registry: NodeRegistry,
    emitter: FakeEmitter | None = None,
    checkpointer: MemoryCheckpointer | None = None,
    **kwargs: Any,
) -> tuple[Scheduler, MemoryCheckpointer]:
    graph = compile_graph(definition, registry=registry)
    cp = checkpointer or MemoryCheckpointer()
    return (
        Scheduler(
            graph,
            cp,
            make_app_context(emitter or FakeEmitter()),
            registry=registry,
            **kwargs,
        ),
        cp,
    )


def _worker_outcome_keys(cp: MemoryCheckpointer) -> dict[tuple[Any, ...], NodeOutcome]:
    return {k: v for k, v in cp._outcomes.items() if k[2] == "worker"}


def _events(emitter: FakeEmitter, event_type: str) -> list[dict[str, Any]]:
    return [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == event_type
    ]


_RETRY_ONCE = {"retry_policy": {"max_attempts": 2, "retry_on": ["RuntimeError"]}}


# ---------------------------------------------------------------------------
# 1. E2 repro — fan-out + transient retry keeps per-item integrity
# ---------------------------------------------------------------------------


async def test_fanout_transient_retry_no_sibling_replay():
    worker = _FanoutWorker(fail_on={"beta": {1}})
    registry, _ = _registry(worker)
    emitter = FakeEmitter()
    scheduler, checkpointer = _scheduler(
        _map_definition(["alpha", "beta", "gamma"], worker_data=_RETRY_ONCE),
        registry,
        emitter=emitter,
    )

    result = await scheduler.run(run_id="fanout-e2")

    assert result.status is RunStatus.COMPLETED
    # The audit E2 corruption was ['ALPHA', 'GAMMA', 'GAMMA'] — beta never
    # processed, gamma duplicated, status COMPLETED. The contract: exactly
    # the three items, index order, no loss, no duplication.
    assert result.last_outputs["gather"]["values"] == ["ALPHA", "BETA", "GAMMA"]
    # The spy: beta was REALLY executed (attempt 1 failed + attempt 2 ran).
    assert sorted(worker.processed) == [
        ("alpha", 1),
        ("beta", 1),
        ("beta", 2),
        ("gamma", 1),
    ]
    # No outcome row was replayed across items: each (dispatch_id, item_index)
    # holds its OWN attempt trail.
    keys = _worker_outcome_keys(checkpointer)
    trails: dict[tuple[str, int], list[int]] = {}
    for run_id, _step, _node, dispatch_id, item_index, attempt in keys:
        assert run_id == "fanout-e2"
        assert dispatch_id != ""  # fanned invocations carry a real dispatch_id
        trails.setdefault((dispatch_id, item_index), []).append(attempt)
    (dispatch_id,) = {d for d, _ in trails}
    assert sorted(trails[(dispatch_id, 0)]) == [1]
    assert sorted(trails[(dispatch_id, 1)]) == [1, 2]  # retry WITHIN its key
    assert sorted(trails[(dispatch_id, 2)]) == [1]
    # Item 1's attempt-1 row is the recorded transient failure; attempt-2 the
    # real output — never a sibling's.
    step = next(iter(keys))[1]
    assert keys[("fanout-e2", step, "worker", dispatch_id, 1, 1)].error is not None
    ok_row = keys[("fanout-e2", step, "worker", dispatch_id, 1, 2)]
    assert ok_row.error is None
    assert ok_row.output == {"result": "BETA"}
    # The live event contract carries the SAME identity as persistence. The
    # Studio must be able to keep a fan-out node Working until every sibling
    # finishes instead of turning the whole card green on the first result.
    worker_started = [e for e in _events(emitter, "node_started") if e["node_id"] == "worker"]
    worker_completed = [e for e in _events(emitter, "node_completed") if e["node_id"] == "worker"]
    assert {(e["dispatch_id"], e["item_index"]) for e in worker_started} == {
        (dispatch_id, 0),
        (dispatch_id, 1),
        (dispatch_id, 2),
    }
    assert {(e["dispatch_id"], e["item_index"]) for e in worker_completed} == {
        (dispatch_id, 0),
        (dispatch_id, 1),
        (dispatch_id, 2),
    }
    assert {e["invocation_count"] for e in worker_started + worker_completed} == {3}


# ---------------------------------------------------------------------------
# 2. Outcome keying — full correlation key, attempt=1 per item
# ---------------------------------------------------------------------------


async def test_outcomes_keyed_by_full_correlation():
    worker = _FanoutWorker()
    registry, _ = _registry(worker)
    scheduler, checkpointer = _scheduler(_map_definition(["alpha", "beta", "gamma"]), registry)

    result = await scheduler.run(run_id="fanout-keys")

    assert result.status is RunStatus.COMPLETED
    keys = _worker_outcome_keys(checkpointer)
    # One distinct row per item — 6-part key (run, step, node, dispatch,
    # item, attempt) with attempt=1 for all of them.
    assert len(keys) == 3
    correlations = sorted((k[3], k[4], k[5]) for k in keys)
    (dispatch_id,) = {d for d, _, _ in correlations}
    assert dispatch_id != ""
    assert correlations == [(dispatch_id, 0, 1), (dispatch_id, 1, 1), (dispatch_id, 2, 1)]
    # The dispatcher's own outcome is ordinary-correlated ('' / 0) and its
    # recorded Sends persist the minted identity (byte-identical replay).
    map_rows = [v for k, v in checkpointer._outcomes.items() if k[2] == "fanout"]
    assert len(map_rows) == 1
    sends = map_rows[0].sends
    assert [s.item_index for s in sends] == [0, 1, 2]
    assert {s.dispatch_id for s in sends} == {dispatch_id}
    assert map_rows[0].dispatch_id == "" and map_rows[0].item_index == 0


# ---------------------------------------------------------------------------
# 3. §4.4 fan-in hole report — user-skipped item is explicit, never silent
# ---------------------------------------------------------------------------


async def test_fanin_reports_skipped_item_as_explicit_hole():
    # beta ALWAYS fails and there is no retry policy → the run parks ERRORED
    # per §3.5 before fan-in ever sees a failure.
    worker = _FanoutWorker(fail_on={"beta": None})
    registry, _ = _registry(worker)
    definition = _map_definition(["alpha", "beta", "gamma"])
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)

    parked = await scheduler.run(run_id="fanout-hole")
    assert parked.status is RunStatus.ERRORED

    cp = await checkpointer.latest_checkpoint("fanout-hole")
    assert cp is not None
    # The frontier addresses every fanned item by its own correlation.
    workers = [ni for ni in cp.next_invocations if ni.node_id == "worker"]
    assert sorted(ni.item_index for ni in workers) == [0, 1, 2]
    target = next(ni for ni in workers if ni.item_index == 1)
    assert target.dispatch_id != ""

    # The user skips the failed item — a user_skip outcome at ITS correlation
    # key (exactly what the recovery endpoint records).
    await checkpointer.record_outcome(
        NodeOutcome(
            run_id="fanout-hole",
            step=cp.step,
            node_id="worker",
            attempt=target.attempt,
            dispatch_id=target.dispatch_id,
            item_index=target.item_index,
            output={},
            source="user_skip",
        )
    )

    resumed = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    result = await resumed.resume(run_id="fanout-hole", checkpoint_id=cp.checkpoint_id)

    assert result.status is RunStatus.COMPLETED
    gather = result.last_outputs["gather"]
    # Explicit hole report — not silent absence, not duplication (§4.4).
    assert gather["values"] == ["ALPHA", "GAMMA"]
    assert gather["count"] == 2
    assert gather["skipped_indexes"] == [1]
    assert gather["expected"] == 3
    assert gather["holes"] == [{"item_index": 1, "status": "skipped", "item": None, "error": None}]


# ---------------------------------------------------------------------------
# 4. §4.5 per-item recovery — retry ONLY item 1; siblings untouched
# ---------------------------------------------------------------------------


async def test_per_item_retry_leaves_sibling_outcomes_untouched():
    # beta fails on attempt 1 only, and there is NO retry policy → parks; a
    # recovery bump to attempt 2 (item 1 alone) makes it succeed.
    worker = _FanoutWorker(fail_on={"beta": {1}})
    registry, _ = _registry(worker)
    definition = _map_definition(["alpha", "beta", "gamma"])
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)

    parked = await scheduler.run(run_id="fanout-item-retry")
    assert parked.status is RunStatus.ERRORED

    cp = await checkpointer.latest_checkpoint("fanout-item-retry")
    assert cp is not None
    workers = [ni for ni in cp.next_invocations if ni.node_id == "worker"]
    target = next(ni for ni in workers if ni.item_index == 1)

    # Snapshot the sibling items' outcome rows BEFORE recovery.
    before = {k: v for k, v in _worker_outcome_keys(checkpointer).items() if k[4] in (0, 2)}
    assert len(before) == 2

    # Recovery-style derived checkpoint: bump attempt for ONLY item 1 — the
    # exact mutation the aidream retry endpoint performs with
    # (dispatch_id, item_index) targeting.
    bumped = Checkpoint(
        checkpoint_id=str(uuid4()),
        run_id=cp.run_id,
        thread_id=cp.thread_id,
        parent_checkpoint_id=cp.checkpoint_id,
        step=cp.step,
        channel_values=cp.channel_values,
        pending_bindings=cp.pending_bindings,
        next_invocations=[
            ni.model_copy(update={"attempt": ni.attempt + 1})
            if ni.node_id == "worker"
            and ni.dispatch_id == target.dispatch_id
            and ni.item_index == 1
            else ni
            for ni in cp.next_invocations
        ],
    )
    await checkpointer.save_checkpoint(bumped)

    emitter = FakeEmitter()
    resumed = Scheduler(graph, checkpointer, make_app_context(emitter), registry=registry)
    result = await resumed.resume(run_id="fanout-item-retry", checkpoint_id=bumped.checkpoint_id)

    assert result.status is RunStatus.COMPLETED
    # Sibling rows are the SAME objects (replayed, never re-recorded) with
    # stable timestamps.
    after = {k: v for k, v in _worker_outcome_keys(checkpointer).items() if k[4] in (0, 2)}
    assert after.keys() == before.keys()
    for key, row in before.items():
        assert after[key] is row
        assert after[key].completed_at == row.completed_at
    # Only item 1 re-executed on resume.
    resumed_processed = [e for e in _events(emitter, "node_started") if e["node_id"] == "worker"]
    assert len(resumed_processed) == 1
    # Downstream fired exactly once with the completed set.
    gathers = [e for e in _events(emitter, "node_started") if e["node_id"] == "gather"]
    assert len(gathers) == 1
    assert result.last_outputs["gather"]["values"] == ["ALPHA", "BETA", "GAMMA"]
    assert result.last_outputs["gather"]["skipped_indexes"] == []


# ---------------------------------------------------------------------------
# 5. §5 emission durability — branch decision survives park + crash replay
# ---------------------------------------------------------------------------


def _branch_definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "a",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "'go'"}},
                },
                {
                    "id": "branch",
                    "type": "control.branch",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"predicate": "inputs['value'] == 'go'"}},
                },
                {
                    "id": "f",
                    "type": "test.flaky_sibling",
                    "position": {"x": 200, "y": 200},
                    "data": {"config": {}},
                },
                {
                    "id": "t_true",
                    "type": "test.fanout_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}},
                },
                {
                    "id": "t_false",
                    "type": "test.fanout_recorder",
                    "position": {"x": 400, "y": 200},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {
                    "id": "e_ab",
                    "source": "a",
                    "target": "branch",
                    "data": {"mappings": {"value": "result"}},
                },
                {"id": "e_af", "source": "a", "target": "f"},
                {"id": "e_bt", "source": "branch", "target": "t_true", "sourceHandle": "true"},
                {"id": "e_bf", "source": "branch", "target": "t_false", "sourceHandle": "false"},
            ],
        }
    )


@pytest.mark.parametrize(
    ("run_ahead", "sibling_fails_after_s", "true_branch_runs_before_park"),
    [
        # The plain barrier: the park precedes all routing.
        (False, 0.0, 0),
        # Run-ahead with the sibling failing LATE: the branch's 'true' target
        # is Ready on the branch's result alone and runs before the park — and
        # is replayed, never re-run, by every resume below. (With both
        # siblings instant the order is the event loop's to pick, so each
        # order is pinned here instead of left to chance.)
        (True, 0.2, 1),
    ],
)
async def test_emissions_persist_and_replay_routes_identically(
    run_ahead: bool, sibling_fails_after_s: float, true_branch_runs_before_park: int
):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    recorder = _Recorder()
    registry.register(recorder, overwrite=True)
    registry.register(_FlakySibling(fail_after_s=sibling_fails_after_s), overwrite=True)

    graph = compile_graph(_branch_definition(), registry=registry)
    checkpointer = MemoryCheckpointer()

    def scheduler_for() -> Scheduler:
        scheduler = Scheduler(
            graph, checkpointer, make_app_context(FakeEmitter()), registry=registry
        )
        scheduler._run_ahead_allowed = scheduler._run_ahead_allowed and run_ahead
        return scheduler

    scheduler = scheduler_for()

    # Step 1: branch completes (emits on 'true'); sibling f fails → park.
    parked = await scheduler.run(run_id="emit-replay")
    assert parked.status is RunStatus.ERRORED
    assert len(recorder.calls) == true_branch_runs_before_park

    # §5: the branch outcome persisted its emissions.
    branch_rows = [v for k, v in checkpointer._outcomes.items() if k[2] == "branch"]
    assert len(branch_rows) == 1
    assert "true" in branch_rows[0].emissions
    assert "false" not in branch_rows[0].emissions

    cp = await checkpointer.latest_checkpoint("emit-replay")
    assert cp is not None
    bumped = Checkpoint(
        checkpoint_id=str(uuid4()),
        run_id=cp.run_id,
        thread_id=cp.thread_id,
        parent_checkpoint_id=cp.checkpoint_id,
        step=cp.step,
        channel_values=cp.channel_values,
        pending_bindings=cp.pending_bindings,
        next_invocations=[
            ni.model_copy(update={"attempt": ni.attempt + 1}) if ni.node_id == "f" else ni
            for ni in cp.next_invocations
        ],
    )
    await checkpointer.save_checkpoint(bumped)

    # Crash replay: a FRESH scheduler resumes the same run_id — the branch
    # replays from its recorded outcome; emissions must route identically.
    resumed = scheduler_for()
    result = await resumed.resume(run_id="emit-replay", checkpoint_id=bumped.checkpoint_id)

    assert result.status is RunStatus.COMPLETED
    # True-branch target ran EXACTLY once; false-branch never (E3 contract).
    assert len(recorder.calls) == 1
    assert "t_true" in result.last_outputs
    assert "t_false" not in result.last_outputs

    # Second crash replay from the same checkpoint (fresh scheduler again):
    # everything replays from outcomes — t_true is NOT re-executed and the
    # routing stays byte-identical.
    replayed = scheduler_for()
    result2 = await replayed.resume(run_id="emit-replay", checkpoint_id=bumped.checkpoint_id)
    assert result2.status is RunStatus.COMPLETED
    assert len(recorder.calls) == 1  # replay, not re-execution
    assert "t_true" in result2.last_outputs
    assert "t_false" not in result2.last_outputs


# ---------------------------------------------------------------------------
# 6. §4.6 per-node concurrency cap inside a super-step
# ---------------------------------------------------------------------------


async def test_per_node_concurrency_cap():
    worker = _FanoutWorker()
    worker.sleep_s = 0.05
    registry, _ = _registry(worker)
    scheduler, _cp = _scheduler(
        _map_definition(
            ["a", "b", "c", "d", "e", "f"],
            worker_data={"concurrency": 2},
            with_gather=False,
        ),
        registry,
        step_concurrency=10,  # run-level bound stays HIGHER than the node cap
    )

    result = await scheduler.run(run_id="fanout-conc")

    assert result.status is RunStatus.COMPLETED
    assert len(worker.processed) == 6
    assert worker.peak_live == 2  # capped at 2, and genuinely parallel


async def test_per_node_concurrency_unset_runs_at_the_platform_fan_out_default():
    """Without data.concurrency a fan-out is bounded by the ``workflow.fan_out``
    default (2026-10-27, run 1aa73a14: an unbounded 199-item map exhausted the
    pool) — the starting value 4 here, where no knob row is readable. Also the
    control that the peak measurement is real: 4 of 6 genuinely overlap."""
    worker = _FanoutWorker()
    worker.sleep_s = 0.05
    registry, _ = _registry(worker)
    scheduler, _cp = _scheduler(
        _map_definition(["a", "b", "c", "d", "e", "f"], with_gather=False),
        registry,
        step_concurrency=10,
    )

    result = await scheduler.run(run_id="fanout-conc-open")

    assert result.status is RunStatus.COMPLETED
    from matrx_graph.knobs import STARTING_FAN_OUT_POLICY

    assert worker.peak_live == STARTING_FAN_OUT_POLICY.default_item_concurrency == 4


# ---------------------------------------------------------------------------
# Postgres checkpointer — the E2 scenario against the durable store
# (§12: acceptance tests run against BOTH checkpointers; PG suite in CI)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not os.environ.get("MATRX_GRAPH_TEST_DB"),
    reason="Set MATRX_GRAPH_TEST_DB=1 to run PostgresCheckpointer integration tests.",
)
async def test_fanout_transient_retry_postgres_checkpointer():
    from dotenv import load_dotenv

    load_dotenv()

    from matrx_orm import register_platform_db

    register_platform_db(
        "supabase_automation_matrix",
        package="matrx-graph tests",
        additional_schemas=["auth"],
    )

    from ._db_guard import assert_not_production_db

    assert_not_production_db("supabase_automation_matrix")

    from matrx_graph.checkpoint import PostgresCheckpointer
    from matrx_graph.db import DefinitionStore, RunStore

    test_user_id = os.environ.get(
        "MATRX_GRAPH_TEST_USER_ID", "87a6e699-3622-4869-8843-d0867456c0dd"
    )
    worker = _FanoutWorker(fail_on={"beta": {1}})
    registry, _ = _registry(worker)
    definition = _map_definition(["alpha", "beta", "gamma"], worker_data=_RETRY_ONCE)
    graph = compile_graph(definition, registry=registry)

    def_store = DefinitionStore()
    run_store = RunStore()
    def_row = await def_store.create(
        name=f"fanout-e2-{uuid4()}",
        definition=definition,
        user_id=test_user_id,
    )
    try:
        run_id = await run_store.create(
            definition_id=def_row.id,
            definition_hash="fanout-e2-hash",
            inputs={},
            user_id=test_user_id,
        )
        checkpointer = PostgresCheckpointer()
        scheduler = Scheduler(
            graph, checkpointer, make_app_context(FakeEmitter()), registry=registry
        )
        result = await scheduler.run(run_id=run_id)

        assert result.status is RunStatus.COMPLETED
        assert result.last_outputs["gather"]["values"] == ["ALPHA", "BETA", "GAMMA"]
        assert sorted(worker.processed) == [
            ("alpha", 1),
            ("beta", 1),
            ("beta", 2),
            ("gamma", 1),
        ]
        # The durable correlation key round-trips: the dispatcher's recorded
        # Sends carry the minted identity, and each item's outcome (incl. the
        # retried one) is addressable at its own key.
        map_outcome = await checkpointer.get_outcome(run_id, 0, "fanout", 1)
        assert map_outcome is not None
        dispatch_ids = {s.dispatch_id for s in map_outcome.sends}
        assert len(dispatch_ids) == 1 and "" not in dispatch_ids
        (dispatch_id,) = dispatch_ids
        beta_fail = await checkpointer.get_outcome(
            run_id, 1, "worker", 1, dispatch_id=dispatch_id, item_index=1
        )
        assert beta_fail is not None and beta_fail.error is not None
        beta_ok = await checkpointer.get_outcome(
            run_id, 1, "worker", 2, dispatch_id=dispatch_id, item_index=1
        )
        assert beta_ok is not None and beta_ok.error is None
        assert beta_ok.output == {"result": "BETA"}
        alpha_ok = await checkpointer.get_outcome(
            run_id, 1, "worker", 1, dispatch_id=dispatch_id, item_index=0
        )
        assert alpha_ok is not None and alpha_ok.output == {"result": "ALPHA"}
    finally:
        await def_store.archive(def_row.id)

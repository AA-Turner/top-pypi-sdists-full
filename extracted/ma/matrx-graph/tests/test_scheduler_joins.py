"""ENGINE_SPEC §3 — join semantics (fixes audit E1) + §12 acceptance criterion 1.

A node with multiple inbound data-carrying edges fires exactly ONCE per
logical firing: readiness is "every required inbound edge resolved
(delivered-into-buffer or pruned)", never "received ≥1 payload this
super-step". Partial bindings persist across super-steps in the checkpoint
(``Checkpoint.pending_bindings``), so upstreams of different path lengths
fill the accumulator in any order across any number of steps.

Covers:
    1.  Unbalanced diamond (A→J, A→B→J): J executes exactly once with BOTH
        args — a double-fire or partial-args execution is impossible.
    2.  Three-source join, path lengths 1/1/3: exactly-once, all three args.
    3.  Multi-writer same-arg → EdgeRoutingError naming the key + both
        edges/sources; run parks ERRORED (§3.7).
    4.  Declared arg_merge ("append") merges in deterministic edge-id order.
    5.  join_policy "all" + all-inbound-pruned → target and its downstream
        prune transitively; run COMPLETES without running them (§3.3).
    6.  Skipped upstream: propagate_empty (default, today's behavior) and
        block (node stays Blocked; run parks, never a silent partial fire)
        (§3.4).
    7.  CONTROL edges count toward the join but bind NO payload (§3.2,
        fixes audit U5).
    8.  join_policy "any" fires per delivery boundary — explicit,
        documented multi-fire (§3.3).
    9.  Resume mid-join: pending_bindings round-trip through the
        checkpointer (MemoryCheckpointer always; PostgresCheckpointer
        behind MATRX_GRAPH_TEST_DB=1 like the rest of the pg suite).
"""

from __future__ import annotations

import os
from typing import Any, ClassVar

import pytest
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
    validate_definition,
)
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


class _RecorderInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _RecorderOutput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _RecorderConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _JoinRecorder:
    """Echo node that records every invocation's fully-routed inputs."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.join_recorder",
        category=NodeCategory.DATA,
        display_name="Join recorder",
        description="Records each invocation's inputs for join assertions.",
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


def _registry() -> tuple[NodeRegistry, _JoinRecorder]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    recorder = _JoinRecorder()
    reg.register(recorder, overwrite=True)
    return reg, recorder


def _transform(node_id: str, expression: str, x: int = 0) -> dict[str, Any]:
    return {
        "id": node_id,
        "type": "data.transform",
        "position": {"x": x, "y": 0},
        "data": {"config": {"expression": expression}},
    }


def _diamond_definition(join_data_extra: dict[str, Any] | None = None) -> Definition:
    """Unbalanced diamond: a→j (path length 1) and a→b→j (path length 2)."""
    join_data: dict[str, Any] = {"config": {}}
    if join_data_extra:
        join_data.update(join_data_extra)
    return Definition.model_validate(
        {
            "nodes": [
                _transform("a", "'from-A'"),
                _transform("b", "inputs['ab'] + '-via-B'", x=200),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": join_data,
                },
            ],
            "edges": [
                {
                    "id": "e_aj",
                    "source": "a",
                    "target": "j",
                    "data": {"mappings": {"from_a": "result"}},
                },
                {
                    "id": "e_ab",
                    "source": "a",
                    "target": "b",
                    "data": {"mappings": {"ab": "result"}},
                },
                {
                    "id": "e_bj",
                    "source": "b",
                    "target": "j",
                    "data": {"mappings": {"from_b": "result"}},
                },
            ],
        }
    )


def _scheduler(
    definition: Definition,
    registry: NodeRegistry,
    emitter: FakeEmitter | None = None,
    checkpointer: MemoryCheckpointer | None = None,
    **kwargs: Any,
) -> Scheduler:
    graph = compile_graph(definition, registry=registry)
    return Scheduler(
        graph,
        checkpointer or MemoryCheckpointer(),
        make_app_context(emitter or FakeEmitter()),
        registry=registry,
        **kwargs,
    )


def _events(emitter: FakeEmitter, event_type: str) -> list[dict[str, Any]]:
    return [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == event_type
    ]


# ---------------------------------------------------------------------------
# 1. Unbalanced diamond — §12 acceptance criterion 1
# ---------------------------------------------------------------------------


async def test_unbalanced_diamond_join_fires_exactly_once_with_both_args():
    registry, recorder = _registry()
    emitter = FakeEmitter()
    scheduler = _scheduler(_diamond_definition(), registry, emitter)

    result = await scheduler.run(run_id="join-diamond")

    assert result.status is RunStatus.COMPLETED
    # Exactly ONE firing — a double-fire or missing-arg execution is the
    # E1 corruption class this run must never COMPLETE with.
    assert len(recorder.calls) == 1, (
        f"join executed {len(recorder.calls)} times with {recorder.calls}"
    )
    assert recorder.calls[0]["from_a"] == "from-A"
    assert recorder.calls[0]["from_b"] == "from-A-via-B"
    # The event stream agrees: one node_started / node_completed for j.
    assert len([e for e in _events(emitter, "node_started") if e["node_id"] == "j"]) == 1
    assert len([e for e in _events(emitter, "node_completed") if e["node_id"] == "j"]) == 1


# ---------------------------------------------------------------------------
# 2. Three-source join, path lengths 1 / 1 / 3
# ---------------------------------------------------------------------------


async def test_three_source_join_uneven_paths_exactly_once():
    registry, recorder = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _transform("a", "'A-VAL'"),
                _transform("b", "'B-VAL'"),
                _transform("c1", "'C'", x=100),
                _transform("c2", "inputs['result'] + '2'", x=200),
                _transform("c3", "inputs['result'] + '3'", x=300),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {"id": "e_aj", "source": "a", "target": "j", "data": {"mappings": {"x": "result"}}},
                {"id": "e_bj", "source": "b", "target": "j", "data": {"mappings": {"y": "result"}}},
                {"id": "e_c1", "source": "c1", "target": "c2"},
                {"id": "e_c2", "source": "c2", "target": "c3"},
                {
                    "id": "e_cj",
                    "source": "c3",
                    "target": "j",
                    "data": {"mappings": {"z": "result"}},
                },
            ],
        }
    )
    scheduler = _scheduler(definition, registry)

    result = await scheduler.run(run_id="join-three-sources")

    assert result.status is RunStatus.COMPLETED
    assert len(recorder.calls) == 1, (
        f"join executed {len(recorder.calls)} times with {recorder.calls}"
    )
    assert recorder.calls[0] == {"x": "A-VAL", "y": "B-VAL", "z": "C23"}


# ---------------------------------------------------------------------------
# 3. Multi-writer same-arg — ERROR by default (§3.7)
# ---------------------------------------------------------------------------


def _multi_writer_definition(join_data_extra: dict[str, Any] | None = None) -> Definition:
    join_data: dict[str, Any] = {"config": {}}
    if join_data_extra:
        join_data.update(join_data_extra)
    return Definition.model_validate(
        {
            "nodes": [
                _transform("a", "'A-VAL'"),
                _transform("b", "'B-VAL'"),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": join_data,
                },
            ],
            "edges": [
                {"id": "e_a", "source": "a", "target": "j", "data": {"mappings": {"x": "result"}}},
                {"id": "e_b", "source": "b", "target": "j", "data": {"mappings": {"x": "result"}}},
            ],
        }
    )


async def test_multi_writer_same_arg_parks_errored_naming_both_writers():
    registry, recorder = _registry()
    emitter = FakeEmitter()
    scheduler = _scheduler(_multi_writer_definition(), registry, emitter)

    result = await scheduler.run(run_id="join-multi-writer")

    assert result.status is RunStatus.ERRORED
    assert recorder.calls == []  # the join never fired with corrupt inputs
    err = result.error or ""
    assert "'x'" in err
    assert "e_a" in err and "e_b" in err
    assert "'a'" in err and "'b'" in err

    errored = _events(emitter, "run_errored")
    assert len(errored) == 1
    assert errored[0]["error_type"] == "EdgeRoutingError"
    # Attributed to the SECOND writer's source (deterministic edge-id order).
    assert errored[0]["node_id"] == "b"


# ---------------------------------------------------------------------------
# 4. Declared arg_merge — deterministic edge-id order (§3.7)
# ---------------------------------------------------------------------------


async def test_arg_merge_append_merges_in_edge_id_order():
    registry, recorder = _registry()
    scheduler = _scheduler(_multi_writer_definition({"arg_merge": {"x": "append"}}), registry)

    result = await scheduler.run(run_id="join-arg-merge")

    assert result.status is RunStatus.COMPLETED
    assert len(recorder.calls) == 1
    assert recorder.calls[0]["x"] == ["A-VAL", "B-VAL"]  # e_a before e_b


# ---------------------------------------------------------------------------
# 5. All inbound edges pruned — transitive prune, run completes (§3.3)
# ---------------------------------------------------------------------------


async def test_all_inbound_pruned_prunes_target_and_downstream_transitively():
    registry, recorder = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _transform("a", "{'score': 0.1}"),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}},
                },
                _transform("d", "'D-RAN'", x=400),
            ],
            "edges": [
                {
                    "id": "e_a1",
                    "source": "a",
                    "target": "j",
                    "data": {"kind": "conditional", "condition": "inputs['score'] > 0.5"},
                },
                {
                    "id": "e_a2",
                    "source": "a",
                    "target": "j",
                    "data": {"kind": "conditional", "condition": "inputs['score'] > 0.9"},
                },
                {"id": "e_jd", "source": "j", "target": "d"},
            ],
        }
    )
    emitter = FakeEmitter()
    scheduler = _scheduler(definition, registry, emitter)

    result = await scheduler.run(run_id="join-all-pruned")

    assert result.status is RunStatus.COMPLETED
    assert recorder.calls == []  # j pruned — never ran
    assert "j" not in result.last_outputs
    assert "d" not in result.last_outputs  # transitive prune of j's subtree
    started = {e["node_id"] for e in _events(emitter, "node_started")}
    assert started == {"a"}


# ---------------------------------------------------------------------------
# 6. Skipped upstream — propagate_empty (default) and block (§3.4)
# ---------------------------------------------------------------------------


def _skip_definition(join_data_extra: dict[str, Any] | None = None) -> Definition:
    join_data: dict[str, Any] = {"config": {}}
    if join_data_extra:
        join_data.update(join_data_extra)
    return Definition.model_validate(
        {
            "nodes": [
                _transform("a", "'A-VAL'"),
                _transform("b", "'B-VAL'"),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": join_data,
                },
            ],
            "edges": [
                # a→j broadcasts its full (empty, when skipped) output.
                {"id": "e_a", "source": "a", "target": "j"},
                {
                    "id": "e_b",
                    "source": "b",
                    "target": "j",
                    "data": {"mappings": {"b_val": "result"}},
                },
            ],
        }
    )


async def test_skipped_upstream_propagate_empty_delivers_and_fires():
    """Default policy: a user_skip's (empty) payload is delivered as-is —
    today's behavior — and the join fires once with both edges resolved."""
    registry, recorder = _registry()
    scheduler = _scheduler(_skip_definition(), registry, skip_node_ids={"a"})

    result = await scheduler.run(run_id="join-skip-propagate")

    assert result.status is RunStatus.COMPLETED
    assert len(recorder.calls) == 1
    # b's real value arrived; a's skipped output contributed its empty shape.
    assert recorder.calls[0]["b_val"] == "B-VAL"
    assert recorder.calls[0].get("result") is None


async def test_skipped_upstream_block_keeps_node_blocked_and_parks_loudly():
    """on_skipped_upstream='block': the skipped edge stays Unsatisfied, the
    join never fires, and the run must NOT complete silently — the buffered
    delivery from b would otherwise be lost (§3.4 + §12.8 'silence is a
    bug'). The run parks ERRORED with the blocked node named."""
    registry, recorder = _registry()
    emitter = FakeEmitter()
    checkpointer = MemoryCheckpointer()
    scheduler = _scheduler(
        _skip_definition({"on_skipped_upstream": "block"}),
        registry,
        emitter,
        checkpointer,
        skip_node_ids={"a"},
    )

    result = await scheduler.run(run_id="join-skip-block")

    assert recorder.calls == []  # j stayed Blocked — never a partial fire
    assert result.status is RunStatus.ERRORED
    err = result.error or ""
    assert "j" in err
    assert "e_a" in err  # the unresolved edge is named

    # Blocked state is durable (§1.2): the parked checkpoint's
    # pending_bindings hold j's partial binding — e_b delivered, e_a absent.
    cp = await checkpointer.latest_checkpoint("join-skip-block")
    assert cp is not None
    entry = cp.pending_bindings["j"]
    assert entry.edges["e_b"].state == "delivered"
    assert entry.edges["e_b"].payload == {"b_val": "B-VAL"}
    assert "e_a" not in entry.edges


# ---------------------------------------------------------------------------
# 7. CONTROL edges — join-count but bind NO payload (§3.2, audit U5)
# ---------------------------------------------------------------------------


async def test_control_edge_gates_join_but_binds_no_payload():
    registry, recorder = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _transform("a", "'A-VAL'"),
                _transform("b", "'CTRL-SECRET'"),
                _transform("b2", "'CTRL-SECRET-2'", x=200),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {
                    "id": "e_a",
                    "source": "a",
                    "target": "j",
                    "data": {"mappings": {"a_val": "result"}},
                },
                {"id": "e_b", "source": "b", "target": "b2"},
                # Control edge on the LONGER path — proves it gates the join
                # across steps while carrying nothing.
                {"id": "e_ctrl", "source": "b2", "target": "j", "data": {"kind": "control"}},
            ],
        }
    )
    emitter = FakeEmitter()
    scheduler = _scheduler(definition, registry, emitter)

    result = await scheduler.run(run_id="join-control-edge")

    assert result.status is RunStatus.COMPLETED
    assert len(recorder.calls) == 1  # waited for the control signal — once
    assert recorder.calls[0]["a_val"] == "A-VAL"
    # The control edge genuinely carried NO data (audit U5).
    assert "result" not in recorder.calls[0]
    assert "CTRL-SECRET-2" not in str(recorder.calls[0])
    # And it really gated: j started only after b2 completed (step 1),
    # i.e. j's node_started is at step 2, not step 1.
    j_started = [e for e in _events(emitter, "node_started") if e["node_id"] == "j"]
    assert len(j_started) == 1
    assert j_started[0]["step"] == 2


# ---------------------------------------------------------------------------
# 8. join_policy "any" — explicit, documented multi-fire (§3.3)
# ---------------------------------------------------------------------------


async def test_join_policy_any_fires_once_per_delivery_boundary():
    registry, recorder = _registry()
    scheduler = _scheduler(_diamond_definition({"join_policy": "any"}), registry)

    result = await scheduler.run(run_id="join-any")

    assert result.status is RunStatus.COMPLETED
    # Two firings: a's delivery at the step-0 boundary, b's at step-1.
    assert len(recorder.calls) == 2
    assert recorder.calls[0] == {"from_a": "from-A"}
    assert recorder.calls[1] == {"from_b": "from-A-via-B"}


# ---------------------------------------------------------------------------
# 9. Resume mid-join — pending_bindings round-trip (§3.8)
# ---------------------------------------------------------------------------


async def _run_pause_resume_mid_join(checkpointer: Any, run_id: str) -> None:
    registry, recorder = _registry()
    definition = _diamond_definition()
    graph = compile_graph(definition, registry=registry)

    polls = {"n": 0}

    async def _pause_after_first_step() -> bool:
        polls["n"] += 1
        return polls["n"] >= 2  # first poll (step 0) runs; second parks

    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
        pause_check=_pause_after_first_step,
    )
    paused = await scheduler.run(run_id=run_id)
    assert paused.status is RunStatus.PAUSED
    assert recorder.calls == []  # j must not have fired on partial args

    cp = await checkpointer.latest_checkpoint(run_id)
    assert cp is not None
    # Mid-join state is durable: a delivered into j's accumulator, b pending.
    entry = cp.pending_bindings["j"]
    assert entry.edges["e_aj"].state == "delivered"
    assert entry.edges["e_aj"].payload == {"from_a": "from-A"}
    assert entry.edges["e_aj"].source_node_id == "a"
    assert "e_bj" not in entry.edges
    assert [ni.node_id for ni in cp.next_invocations] == ["b"]

    # Fresh scheduler (recovery-style) resumes from the checkpoint.
    resumed = Scheduler(
        graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await resumed.resume(run_id=run_id, checkpoint_id=cp.checkpoint_id)

    assert result.status is RunStatus.COMPLETED
    assert len(recorder.calls) == 1, (
        f"join executed {len(recorder.calls)} times with {recorder.calls}"
    )
    assert recorder.calls[0] == {"from_a": "from-A", "from_b": "from-A-via-B"}

    # Consumed firings drop from subsequent checkpoints (§3.8).
    final_cp = await checkpointer.latest_checkpoint(run_id)
    assert final_cp is not None
    assert "j" not in final_cp.pending_bindings


async def test_resume_mid_join_memory_checkpointer():
    await _run_pause_resume_mid_join(MemoryCheckpointer(), "join-resume-mem")


class _FlakyNode:
    """Fails on attempt 1, succeeds on attempt 2 — drives the ERRORED park."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.flaky",
        category=NodeCategory.DATA,
        display_name="Flaky",
        description="Fails on attempt 1 to exercise recovery.",
        input_schema=_RecorderInput,
        output_schema=_RecorderOutput,
        config_schema=_RecorderConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        _inputs: _RecorderInput,
        _config: _RecorderConfig,
    ) -> NodeResult[_RecorderOutput]:
        if ctx.attempt == 1:
            raise RuntimeError("flaky: transient failure on attempt 1")
        return success(_RecorderOutput())


async def test_errored_park_mid_join_preserves_bindings_through_recovery_resume():
    """Park via induced sibling error mid-join, then a recovery-style resume
    (attempt-bumped checkpoint derived from the errored one, à la the
    /runs recovery endpoints): the cross-step buffered binding survives the
    park and the join still fires exactly once with both args. The derived
    checkpoint MUST carry pending_bindings forward — this test is the
    executable contract for that."""
    from uuid import uuid4

    from matrx_graph.checkpoint.protocol import Checkpoint, NextInvocation

    registry, recorder = _registry()
    reg_flaky = _FlakyNode()
    registry.register(reg_flaky, overwrite=True)

    # a → j (short path, delivers at step 0) ; a → b → j (long path) ;
    # a → f (sibling of b at step 1) which fails on attempt 1.
    definition = _diamond_definition()
    definition = Definition.model_validate(
        {
            **definition.model_dump(mode="json"),
            "nodes": [
                *definition.model_dump(mode="json")["nodes"],
                {
                    "id": "f",
                    "type": "test.flaky",
                    "position": {"x": 200, "y": 200},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                *definition.model_dump(mode="json")["edges"],
                {"id": "e_af", "source": "a", "target": "f"},
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)

    errored = await scheduler.run(run_id="join-resume-errored")
    assert errored.status is RunStatus.ERRORED
    # j never fired on partial args. It MAY already have fired with both: b
    # finishing before its failing sibling f lets j run ahead of the barrier
    # (run-ahead, scheduler.py) — and then resume replays it, never re-runs it.
    assert len(recorder.calls) <= 1, recorder.calls
    assert all(set(call) == {"from_a", "from_b"} for call in recorder.calls), recorder.calls

    cp = await checkpointer.latest_checkpoint("join-resume-errored")
    assert cp is not None
    # a's step-0 delivery to j survived the errored park.
    assert cp.pending_bindings["j"].edges["e_aj"].state == "delivered"

    # Recovery-style attempt bump: derive a new checkpoint from the errored
    # one, carrying pending_bindings forward (the recovery endpoints must do
    # the same — dropping them would silently lose the buffered join data).
    bumped = Checkpoint(
        checkpoint_id=str(uuid4()),
        run_id=cp.run_id,
        thread_id=cp.thread_id,
        parent_checkpoint_id=cp.checkpoint_id,
        step=cp.step,
        channel_values=cp.channel_values,
        pending_bindings=cp.pending_bindings,
        next_invocations=[
            NextInvocation(
                node_id=ni.node_id,
                inputs=ni.inputs,
                attempt=ni.attempt + 1 if ni.node_id == "f" else ni.attempt,
            )
            for ni in cp.next_invocations
        ],
    )
    await checkpointer.save_checkpoint(bumped)

    resumed = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    result = await resumed.resume(run_id="join-resume-errored", checkpoint_id=bumped.checkpoint_id)

    assert result.status is RunStatus.COMPLETED
    assert len(recorder.calls) == 1, (
        f"join executed {len(recorder.calls)} times with {recorder.calls}"
    )
    assert recorder.calls[0] == {"from_a": "from-A", "from_b": "from-A-via-B"}


@pytest.mark.skipif(
    not os.environ.get("MATRX_GRAPH_TEST_DB"),
    reason="Set MATRX_GRAPH_TEST_DB=1 to run PostgresCheckpointer integration tests.",
)
async def test_resume_mid_join_postgres_checkpointer():
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

    from uuid import uuid4

    from matrx_graph.checkpoint import PostgresCheckpointer
    from matrx_graph.db import DefinitionStore, RunStore

    test_user_id = os.environ.get(
        "MATRX_GRAPH_TEST_USER_ID", "87a6e699-3622-4869-8843-d0867456c0dd"
    )
    def_store = DefinitionStore()
    run_store = RunStore()
    def_row = await def_store.create(
        name=f"join-resume-{uuid4()}",
        definition=_diamond_definition(),
        user_id=test_user_id,
    )
    try:
        run_id = await run_store.create(
            definition_id=def_row.id,
            definition_hash="join-test-hash",
            inputs={},
            user_id=test_user_id,
        )
        await _run_pause_resume_mid_join(PostgresCheckpointer(), run_id)
    finally:
        await def_store.archive(def_row.id)


# ---------------------------------------------------------------------------
# Validation — the new NodeDef.data keys (§3.3/§3.4/§3.7, ENGINE_SPEC §11)
# ---------------------------------------------------------------------------


def _validation_definition(join_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "nodes": [
            _transform("a", "'A'"),
            {
                "id": "j",
                "type": "test.join_recorder",
                "position": {"x": 200, "y": 0},
                "data": {"config": {}, **join_data},
            },
        ],
        "edges": [
            {"id": "e_a", "source": "a", "target": "j", "data": {"mappings": {"x": "result"}}},
        ],
    }


def test_validation_rejects_bad_join_policy_and_skip_policy_and_reducer():
    registry, _ = _registry()

    bad_policy = validate_definition(
        _validation_definition({"join_policy": "sometimes"}), registry=registry
    )
    assert not bad_policy.valid
    assert any("join_policy" in i.message for i in bad_policy.issues)

    bad_skip = validate_definition(
        _validation_definition({"on_skipped_upstream": "explode"}), registry=registry
    )
    assert not bad_skip.valid
    assert any("on_skipped_upstream" in i.message for i in bad_skip.issues)

    bad_reducer = validate_definition(
        _validation_definition({"arg_merge": {"x": "concat"}}), registry=registry
    )
    assert not bad_reducer.valid
    assert any("arg_merge" in i.message for i in bad_reducer.issues)


def test_validation_enforces_skip_defaults_completeness():
    """§3.4: on_skipped_upstream='default_value' requires a skip_defaults
    entry for every arg an inbound edge maps."""
    registry, _ = _registry()

    missing = validate_definition(
        _validation_definition({"on_skipped_upstream": "default_value", "skip_defaults": {}}),
        registry=registry,
    )
    assert not missing.valid
    assert any("skip_defaults" in i.message and "'x'" in i.message for i in missing.issues)

    complete = validate_definition(
        _validation_definition(
            {"on_skipped_upstream": "default_value", "skip_defaults": {"x": "fallback"}}
        ),
        registry=registry,
    )
    assert complete.valid


# ---------------------------------------------------------------------------
# 10. Engine markers on a fan-in — ``__kind`` is metadata, not a data arg
# ---------------------------------------------------------------------------


class _KindSourceConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    field: str
    value: str


class _KindSourceOutput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _KindSource:
    """Typed source: emits one named field, settlement stamps its ``__kind``."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.kind_source",
        category=NodeCategory.DATA,
        display_name="Kind source",
        description="Emits a one-field payload under a declared output kind.",
        input_schema=_RecorderInput,
        output_schema=_KindSourceOutput,
        config_schema=_KindSourceConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        _inputs: _RecorderInput,
        config: _KindSourceConfig,
    ) -> NodeResult[_KindSourceOutput]:
        return success(_KindSourceOutput(**{config.field: config.value}))


def _kind_registry() -> tuple[NodeRegistry, _JoinRecorder]:
    reg, recorder = _registry()
    reg.register(_KindSource(), overwrite=True)
    return reg, recorder


def _kind_source_node(node_id: str, field: str, value: str, kind: str, x: int) -> dict[str, Any]:
    return {
        "id": node_id,
        "type": "test.kind_source",
        "position": {"x": x, "y": 0},
        "data": {"config": {"field": field, "value": value}, "output_kind": kind},
    }


def _kind_fanin_definition(kind_a: str, kind_b: str, field_b: str = "from_b") -> Definition:
    """a→j and b→j, both BROADCAST edges (no mappings) so each fragment carries
    its source's settled ``__kind`` marker — the production shape (run
    a4604173, 2026-08-26) that used to park the run on the marker alone."""
    return Definition.model_validate(
        {
            "nodes": [
                _kind_source_node("a", "from_a", "A-VAL", kind_a, 0),
                _kind_source_node("b", field_b, "B-VAL", kind_b, 200),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {"id": "e_a", "source": "a", "target": "j"},
                {"id": "e_b", "source": "b", "target": "j"},
            ],
        }
    )


async def test_same_kind_fan_in_joins_and_drops_the_marker():
    """Two typed upstreams, SAME kind, fanning into one node: the join
    succeeds (``__kind`` is engine metadata, never a multi-writer collision)
    and the merged payload carries NO marker — a union of two payloads is a
    new anonymous shape, not an instance of the kind either side emitted."""
    registry, recorder = _kind_registry()
    scheduler = _scheduler(_kind_fanin_definition("join_kind_x", "join_kind_x"), registry)

    result = await scheduler.run(run_id="join-kind-same")

    assert result.status is RunStatus.COMPLETED, result.error
    assert len(recorder.calls) == 1
    assert recorder.calls[0]["from_a"] == "A-VAL"
    assert recorder.calls[0]["from_b"] == "B-VAL"
    assert "__kind" not in recorder.calls[0]


async def test_different_kind_fan_in_joins_and_drops_the_marker():
    """Different kinds fanning in: same rule, and the reason is sharpest here —
    keeping either side's kind would MISLABEL the merged payload."""
    registry, recorder = _kind_registry()
    scheduler = _scheduler(_kind_fanin_definition("join_kind_x", "join_kind_y"), registry)

    result = await scheduler.run(run_id="join-kind-different")

    assert result.status is RunStatus.COMPLETED, result.error
    assert len(recorder.calls) == 1
    assert recorder.calls[0]["from_a"] == "A-VAL"
    assert recorder.calls[0]["from_b"] == "B-VAL"
    assert "__kind" not in recorder.calls[0]


async def test_single_typed_hop_keeps_its_marker():
    """The other half of the rule: ONE fragment IS its upstream's payload, so
    identity travels (the ordinary typed hop must not lose ``__kind``)."""
    registry, recorder = _kind_registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _kind_source_node("a", "from_a", "A-VAL", "join_kind_x", 0),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [{"id": "e_a", "source": "a", "target": "j"}],
        }
    )
    scheduler = _scheduler(definition, registry)

    result = await scheduler.run(run_id="join-kind-single")

    assert result.status is RunStatus.COMPLETED, result.error
    assert recorder.calls[0]["__kind"] == "join_kind_x"


async def test_real_data_key_collision_still_parks_errored():
    """Regression guard: exempting the marker must not weaken §3.7 for an
    author's DATA args — a genuine same-arg collision still parks loudly, and
    the arg_merge advice it prints names a key the author actually owns."""
    registry, recorder = _kind_registry()
    emitter = FakeEmitter()
    scheduler = _scheduler(
        _kind_fanin_definition("join_kind_x", "join_kind_y", field_b="from_a"),
        registry,
        emitter,
    )

    result = await scheduler.run(run_id="join-kind-real-collision")

    assert result.status is RunStatus.ERRORED
    assert recorder.calls == []
    err = result.error or ""
    assert "'from_a'" in err
    assert "e_a" in err and "e_b" in err
    assert "Multi-writer same-arg" in err
    assert "arg_merge = {'from_a'" in err
    errored = _events(emitter, "run_errored")
    assert errored[0]["error_type"] == "EdgeRoutingError"

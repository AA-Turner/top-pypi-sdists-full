"""Join-semantics hardening — the 2026-07-08 adversarial-audit fixes (F1–F13).

Each test class reproduces one adversary-CONFIRMED failure and pins the fixed
behavior. ENGINE_SPEC §3 (+ the §3.4 ``Amendment (D2b)`` blockquote) is the
contract.

F1  — an ``arg_merge`` reducer failure (e.g. ``sum`` over strings) is an
      EdgeRoutingError attributed to the TARGET node + arg + every
      contributing edge/source → the standard recoverable ERRORED park WITH
      a checkpoint. Previously the ChannelError escaped the routing phase
      and the run died terminal FAILED with ZERO durable state.

F2  — **Design (D2b): the join-deadlock park is ADDRESSABLE.** The park
      saves one ``blocked_join``-flagged NextInvocation per deadlocked node,
      carrying the currently-merged partial inputs, while ``pending_bindings``
      stays persisted alongside. Recovery acts through that invocation:
      *skip* records a ``user_skip`` outcome at its correlation key (its
      downstream then prunes/propagates per §3.4), *manual-result* supplies
      the node's output, *retry* (attempt bump) re-runs the node with the
      partial inputs. ``Scheduler.resume`` executes a blocked invocation
      ONLY when the user acted (outcome exists, or ``attempt > 1``) and then
      consumes its buffered entry; untouched, the invocation is filtered out
      and the deadlock guard re-parks the identical state — a plain resume
      of an unchanged deadlock is a progress-free re-park, never a partial
      fire (and the aidream router 409s it before consuming the recovery
      counter). Previously the park saved ``next_invocations=[]`` so every
      recovery endpoint 404/409'd and plain resume re-parked in a loop —
      unrecoverable by design.

F3  — an accumulator entry on an ``on_skipped_upstream='block'`` node with
      unresolved required edges parks the run even when its only recorded
      sibling edges are pruned. Previously "pruned-only residue" logic
      dropped the block placeholder and the run COMPLETED silently.

F4  — step-mode ``_merge_frontier`` never last-writer-wins-merges two
      DISTINCT firings of one node: identical payloads collapse (idempotent
      re-route), different payloads park loudly (running both in one step
      would collide on the outcome idempotency key). Recovery: resume
      without node selection.

F5  — the per-node firing counter is monotonic across resume: join-fired
      invocations persist their ``firing`` number and ``resume`` restores
      the counter from the max over the checkpoint + full history.

F8  — ``on_skipped_upstream='default_value'`` combined with a BROADCAST
      (no-mappings) inbound data edge is a compile-time validation error
      (a skipped broadcast upstream would deliver the whole skip_defaults
      dict — guaranteed multi-writer collision).

F13 — compile classifies cycle back-edges (DFS from the entry nodes);
      back-edges are EXCLUDED from the target's required join set and each
      delivery over one opens a NEW firing directly (pre-join-engine
      re-fire-per-delivery), so legacy feedback-edge definitions terminate
      via their own predicates instead of deadlock-parking every run. A
      cycle UNREACHABLE from the entry nodes is a loud CompilationError
      naming the cycle — never a silent deadlock.
"""

from __future__ import annotations

from typing import Any, ClassVar

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
from matrx_graph.checkpoint.protocol import NodeOutcome
from matrx_graph.errors import CompilationError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict
import pytest

from tests._fixtures import FakeEmitter, make_app_context


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


class _CounterInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    n: int = 0


class _CounterOutput(BaseModel):
    n: int


class _Counter:
    """Loop-body node: outputs n+1 — the feedback predicate's ticker (F13)."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.counter",
        category=NodeCategory.DATA,
        display_name="Counter",
        description="Emits n+1 for cycle-termination tests.",
        input_schema=_CounterInput,
        output_schema=_CounterOutput,
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
        inputs: _CounterInput,
        _config: _RecorderConfig,
    ) -> NodeResult[_CounterOutput]:
        self.calls.append(inputs.model_dump(mode="json"))
        return success(_CounterOutput(n=inputs.n + 1))


def _registry() -> tuple[NodeRegistry, _JoinRecorder, _Counter]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    recorder = _JoinRecorder()
    counter = _Counter()
    reg.register(recorder, overwrite=True)
    reg.register(counter, overwrite=True)
    return reg, recorder, counter


def _transform(node_id: str, expression: str, x: int = 0) -> dict[str, Any]:
    return {
        "id": node_id,
        "type": "data.transform",
        "position": {"x": x, "y": 0},
        "data": {"config": {"expression": expression}},
    }


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
# F1 — arg_merge reducer failure: recoverable ERRORED park, never terminal
# ---------------------------------------------------------------------------


def _sum_merge_definition() -> Definition:
    """Two string outputs joined into one arg under arg_merge 'sum' — the
    reducer raises ChannelError on non-numeric values."""
    return Definition.model_validate(
        {
            "nodes": [
                _transform("a", "'A-VAL'"),
                _transform("b", "'B-VAL'"),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}, "arg_merge": {"x": "sum"}},
                },
            ],
            "edges": [
                {"id": "e_a", "source": "a", "target": "j", "data": {"mappings": {"x": "result"}}},
                {"id": "e_b", "source": "b", "target": "j", "data": {"mappings": {"x": "result"}}},
            ],
        }
    )


async def test_arg_merge_reducer_failure_parks_errored_with_checkpoint():
    registry, recorder, _counter = _registry()
    emitter = FakeEmitter()
    checkpointer = MemoryCheckpointer()
    scheduler = _scheduler(_sum_merge_definition(), registry, emitter, checkpointer)

    result = await scheduler.run(run_id="f1-sum-strings")

    # Recoverable park — NOT the old terminal FAILED with zero durable state.
    assert result.status is RunStatus.ERRORED
    assert recorder.calls == []  # the join never fired with corrupt inputs
    assert _events(emitter, "run_failed") == []
    errored = _events(emitter, "run_errored")
    assert len(errored) == 1
    assert errored[0]["error_type"] == "EdgeRoutingError"
    # Attribution: target node + arg + both contributing edges/sources.
    err = result.error or ""
    assert "'j'" in err
    assert "'x'" in err
    assert "e_a" in err and "e_b" in err
    assert "'a'" in err and "'b'" in err

    # A checkpoint EXISTS (the F1 bug saved none), with the parked frontier
    # (this step's invocations) so resume re-runs the step.
    cp = await checkpointer.latest_checkpoint("f1-sum-strings")
    assert cp is not None
    assert {ni.node_id for ni in cp.next_invocations} == {"a", "b"}


# ---------------------------------------------------------------------------
# F2 — the join-deadlock park is ADDRESSABLE (Amendment D2b)
# ---------------------------------------------------------------------------


def _block_definition() -> Definition:
    """a (skipped) —broadcast→ j [block] ←mapped— b; j —broadcast→ d."""
    return Definition.model_validate(
        {
            "nodes": [
                _transform("a", "'A-VAL'"),
                _transform("b", "'B-VAL'"),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}, "on_skipped_upstream": "block"},
                },
                _transform("d", "'D-RAN'", x=600),
            ],
            "edges": [
                {"id": "e_a", "source": "a", "target": "j"},
                {
                    "id": "e_b",
                    "source": "b",
                    "target": "j",
                    "data": {"mappings": {"b_val": "result"}},
                },
                {"id": "e_jd", "source": "j", "target": "d"},
            ],
        }
    )


async def _park_block_deadlock(
    checkpointer: MemoryCheckpointer,
    run_id: str,
) -> tuple[NodeRegistry, _JoinRecorder, Any]:
    registry, recorder, _counter = _registry()
    scheduler = _scheduler(_block_definition(), registry, None, checkpointer, skip_node_ids={"a"})
    result = await scheduler.run(run_id=run_id)
    assert result.status is RunStatus.ERRORED
    assert recorder.calls == []
    cp = await checkpointer.latest_checkpoint(run_id)
    assert cp is not None
    return registry, recorder, cp


def _resume_scheduler(registry: NodeRegistry, checkpointer: MemoryCheckpointer) -> Scheduler:
    """A FRESH scheduler (fresh in-memory state) — recovery always is."""
    graph = compile_graph(_block_definition(), registry=registry)
    return Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)


async def test_block_deadlock_park_is_addressable():
    checkpointer = MemoryCheckpointer()
    _registry_, _recorder, cp = await _park_block_deadlock(checkpointer, "f2-park")

    # The park carries ONE addressable blocked_join invocation for j with
    # the currently-merged partial inputs — the old park saved [] and made
    # every recovery endpoint 404/409.
    assert len(cp.next_invocations) == 1
    ni = cp.next_invocations[0]
    assert ni.node_id == "j"
    assert ni.blocked_join is True
    assert ni.inputs == {"b_val": "B-VAL"}
    # The buffered data stays durable alongside the addressable handle.
    assert cp.pending_bindings["j"].edges["e_b"].state == "delivered"


async def test_block_deadlock_skip_recovery_completes_and_propagates():
    checkpointer = MemoryCheckpointer()
    registry, recorder, cp = await _park_block_deadlock(checkpointer, "f2-skip")

    # What POST /runs/{id}/nodes/j/skip records through the frontier match.
    ni = cp.next_invocations[0]
    await checkpointer.record_outcome(
        NodeOutcome(
            run_id="f2-skip",
            step=cp.step,
            node_id="j",
            attempt=ni.attempt,
            output={},
            error=None,
            source="user_skip",
        )
    )
    result = await _resume_scheduler(registry, checkpointer).resume(
        run_id="f2-skip", checkpoint_id=cp.checkpoint_id
    )

    assert result.status is RunStatus.COMPLETED
    assert recorder.calls == []  # j replayed the user_skip — never executed
    # Downstream d received the (empty) propagated output per §3.4 defaults.
    assert result.last_outputs.get("d") == {"result": "D-RAN"}


async def test_block_deadlock_manual_result_supplies_output():
    checkpointer = MemoryCheckpointer()
    registry, recorder, cp = await _park_block_deadlock(checkpointer, "f2-manual")

    ni = cp.next_invocations[0]
    await checkpointer.record_outcome(
        NodeOutcome(
            run_id="f2-manual",
            step=cp.step,
            node_id="j",
            attempt=ni.attempt,
            output={"b_val": "B-VAL", "result": "HUMAN"},
            error=None,
            source="user_manual",
        )
    )
    result = await _resume_scheduler(registry, checkpointer).resume(
        run_id="f2-manual", checkpoint_id=cp.checkpoint_id
    )

    assert result.status is RunStatus.COMPLETED
    assert recorder.calls == []  # replayed, not executed
    assert result.last_outputs["j"] == {"b_val": "B-VAL", "result": "HUMAN"}
    assert result.last_outputs.get("d") == {"result": "D-RAN"}


async def test_block_deadlock_retry_runs_node_with_partial_inputs():
    checkpointer = MemoryCheckpointer()
    registry, recorder, cp = await _park_block_deadlock(checkpointer, "f2-retry")

    # What POST /runs/{id}/nodes/j/retry builds: a child checkpoint with the
    # addressed invocation's attempt bumped (no outcome at attempt 2 → the
    # node runs FRESH with the partial inputs).
    child = cp.model_copy(
        update={
            "checkpoint_id": "f2-retry-child",
            "parent_checkpoint_id": cp.checkpoint_id,
            "next_invocations": [
                ni.model_copy(update={"attempt": ni.attempt + 1}) for ni in cp.next_invocations
            ],
        }
    )
    await checkpointer.save_checkpoint(child)
    result = await _resume_scheduler(registry, checkpointer).resume(
        run_id="f2-retry", checkpoint_id="f2-retry-child"
    )

    assert result.status is RunStatus.COMPLETED
    assert recorder.calls == [{"b_val": "B-VAL"}]  # executed with partials
    assert result.last_outputs.get("d") == {"result": "D-RAN"}


async def test_block_deadlock_plain_resume_reparks_identically_no_partial_fire():
    checkpointer = MemoryCheckpointer()
    registry, recorder, cp = await _park_block_deadlock(checkpointer, "f2-noop")

    # Nothing changed → resume must NOT fire j (not even with partial args);
    # it re-parks the identical addressable state. (The aidream router
    # additionally 409s this case before consuming the recovery counter.)
    for _ in range(2):
        result = await _resume_scheduler(registry, checkpointer).resume(
            run_id="f2-noop", checkpoint_id=cp.checkpoint_id
        )
        assert result.status is RunStatus.ERRORED
        assert recorder.calls == []
        cp = await checkpointer.latest_checkpoint("f2-noop")
        assert cp is not None
        assert [ni.node_id for ni in cp.next_invocations] == ["j"]
        assert cp.next_invocations[0].blocked_join is True
        assert cp.next_invocations[0].inputs == {"b_val": "B-VAL"}
        assert cp.pending_bindings["j"].edges["e_b"].state == "delivered"


# ---------------------------------------------------------------------------
# F3 — block placeholder + pruned sibling: park, never silent COMPLETED
# ---------------------------------------------------------------------------


async def test_block_placeholder_with_pruned_sibling_parks_errored():
    registry, recorder, _counter = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _transform("a", "'A-VAL'"),
                _transform("c", "{'score': 0.1}"),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}, "on_skipped_upstream": "block"},
                },
            ],
            "edges": [
                # a is user-skipped → block placeholder (edge deliberately
                # absent from the accumulator entry).
                {"id": "e_a", "source": "a", "target": "j"},
                # c's conditional edge prunes (0.1 > 0.5 is false) — the
                # pruned sibling must NOT launder the placeholder into
                # droppable "pruned-only residue".
                {
                    "id": "e_c",
                    "source": "c",
                    "target": "j",
                    "data": {"kind": "conditional", "condition": "inputs['score'] > 0.5"},
                },
            ],
        }
    )
    emitter = FakeEmitter()
    scheduler = _scheduler(definition, registry, emitter, skip_node_ids={"a"})

    result = await scheduler.run(run_id="f3-block-pruned")

    assert result.status is RunStatus.ERRORED  # was: silent COMPLETED
    assert recorder.calls == []
    assert "j" in (result.error or "")
    assert len(_events(emitter, "run_errored")) == 1


# ---------------------------------------------------------------------------
# F4 — step-mode never merges two distinct firings of one node
# ---------------------------------------------------------------------------


def _any_diamond_definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                _transform("a", "'from-A'"),
                _transform("b", "inputs['ab'] + '-via-B'", x=200),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}, "join_policy": "any"},
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


async def test_step_mode_distinct_firings_park_loudly_then_recover():
    registry, recorder, _counter = _registry()
    checkpointer = MemoryCheckpointer()
    graph = compile_graph(_any_diamond_definition(), registry=registry)

    polls = {"n": 0}

    async def _pause_after_first_step() -> bool:
        polls["n"] += 1
        return polls["n"] >= 2

    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
        pause_check=_pause_after_first_step,
    )
    paused = await scheduler.run(run_id="f4-step")
    assert paused.status is RunStatus.PAUSED
    parked = await checkpointer.latest_checkpoint("f4-step")
    assert parked is not None
    # Frontier: j's firing 1 (from a, any-policy) + the deferred sibling b.
    assert {ni.node_id for ni in parked.next_invocations} == {"j", "b"}

    # Select ONLY b: its routing join-fires j AGAIN (firing 2, any-policy)
    # while firing 1 sits deferred — two DISTINCT firings on one correlation
    # key. Old behavior: silent {**a, **b} last-writer-wins (wave-1 payload
    # lost). New behavior: loud recoverable park.
    fresh = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    result = await fresh.resume(
        run_id="f4-step",
        checkpoint_id=parked.checkpoint_id,
        select_node_ids={"b"},
        stop_after_steps=1,
    )
    assert result.status is RunStatus.ERRORED
    assert "DISTINCT firings" in (result.error or "")
    assert recorder.calls == []  # neither firing executed with merged inputs

    # Recovery: resume WITHOUT selection — the full parked frontier runs the
    # firings on separate steps; BOTH payloads survive.
    errored = await checkpointer.latest_checkpoint("f4-step")
    assert errored is not None
    final = Scheduler(
        graph, checkpointer, make_app_context(FakeEmitter()), registry=registry
    ).resume(run_id="f4-step", checkpoint_id=errored.checkpoint_id)
    result2 = await final
    assert result2.status is RunStatus.COMPLETED
    assert recorder.calls == [
        {"from_a": "from-A"},
        {"from_b": "from-A-via-B"},
    ]


# ---------------------------------------------------------------------------
# F5 — firing counter continues across resume, never restarts
# ---------------------------------------------------------------------------


async def test_firing_counter_monotonic_across_resume():
    registry, recorder, _counter = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _transform("a", "'A-VAL'"),
                _transform("c1", "'C'", x=100),
                _transform("c2", "inputs['result'] + '2'", x=200),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}, "join_policy": "any"},
                },
            ],
            "edges": [
                {"id": "e_aj", "source": "a", "target": "j", "data": {"mappings": {"x": "result"}}},
                {"id": "e_c1", "source": "c1", "target": "c2"},
                {
                    "id": "e_cj",
                    "source": "c2",
                    "target": "j",
                    "data": {"mappings": {"z": "result"}},
                },
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()

    polls = {"n": 0}

    async def _pause_after_first_step() -> bool:
        polls["n"] += 1
        return polls["n"] >= 2

    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
        pause_check=_pause_after_first_step,
    )
    paused = await scheduler.run(run_id="f5-firing")
    assert paused.status is RunStatus.PAUSED
    parked = await checkpointer.latest_checkpoint("f5-firing")
    assert parked is not None
    # Firing 1 was consumed into the frontier — its number rides the
    # invocation (this is the durable proof the counter restores from).
    j_pending = [ni for ni in parked.next_invocations if ni.node_id == "j"]
    assert len(j_pending) == 1
    assert j_pending[0].firing == 1

    # FRESH scheduler (in-memory counter gone) — resume must restore j's
    # counter at 1, so the second firing gets number 2, never a reused 1.
    fresh = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    result = await fresh.resume(run_id="f5-firing", checkpoint_id=parked.checkpoint_id)
    assert result.status is RunStatus.COMPLETED
    assert len(recorder.calls) == 2
    assert fresh._firing_seq["j"] == 2  # noqa: SLF001 — the counter IS the contract

    # And the durable trail agrees: some checkpoint carries j's firing-2
    # invocation (pre-fix it re-used 1).
    firings = [
        ni.firing
        for cp in await checkpointer.list_checkpoints("f5-firing")
        for ni in cp.next_invocations
        if ni.node_id == "j"
    ]
    assert max(firings) == 2


# ---------------------------------------------------------------------------
# F8 — default_value + broadcast inbound edge is a compile-time rejection
# ---------------------------------------------------------------------------


def _broadcast_default_definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                _transform("a", "'A-VAL'"),
                _transform("b", "'B-VAL'"),
                {
                    "id": "j",
                    "type": "test.join_recorder",
                    "position": {"x": 400, "y": 0},
                    "data": {
                        "config": {},
                        "on_skipped_upstream": "default_value",
                        "skip_defaults": {"sv": "DEFAULT-S"},
                    },
                },
            ],
            "edges": [
                # broadcast — no field mappings: a skipped 'a' would deliver
                # the WHOLE skip_defaults dict and collide with e_b.
                {"id": "e_a", "source": "a", "target": "j"},
                {
                    "id": "e_b",
                    "source": "b",
                    "target": "j",
                    "data": {"mappings": {"sv": "result"}},
                },
            ],
        }
    )


def test_default_value_with_broadcast_inbound_edge_rejected():
    registry, _recorder, _counter = _registry()
    result = validate_definition(_broadcast_default_definition(), registry=registry)
    assert not result.valid
    broadcast_issues = [i for i in result.issues if i.node_id == "j" and i.edge_id == "e_a"]
    assert len(broadcast_issues) == 1
    msg = broadcast_issues[0].message
    assert "broadcast" in msg
    assert "mappings" in msg or "field links" in msg

    with pytest.raises(CompilationError):
        compile_graph(_broadcast_default_definition(), registry=registry)


# ---------------------------------------------------------------------------
# F13 — cycle back-edges: re-fire per delivery, never a deadlock park
# ---------------------------------------------------------------------------


def _counter_node(node_id: str, x: int = 0) -> dict[str, Any]:
    return {
        "id": node_id,
        "type": "test.counter",
        "position": {"x": x, "y": 0},
        "data": {"config": {}},
    }


async def test_self_loop_refires_on_self_delivery_and_terminates():
    registry, _recorder, counter = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [_counter_node("a")],
            "edges": [
                {
                    "id": "e_loop",
                    "source": "a",
                    "target": "a",
                    "data": {
                        "kind": "conditional",
                        "condition": "inputs['n'] < 3",
                        "mappings": {"n": "n"},
                    },
                }
            ],
            "entry_nodes": ["a"],
        }
    )
    graph = compile_graph(definition, registry=registry)
    assert graph.edges["e_loop"].is_back_edge is True
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )

    result = await scheduler.run(run_id="f13-self-loop", max_steps=20)

    # n: 0→1, 1→2, 2→3, predicate 3<3 false → clean termination via the
    # node's own logic. Pre-fix: deadlock ERRORED park on every such run.
    assert result.status is RunStatus.COMPLETED
    assert counter.calls == [{"n": 0}, {"n": 1}, {"n": 2}]


async def test_two_node_cycle_refires_per_delivery_like_pre_join_engine():
    registry, _recorder, counter = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _counter_node("a"),
                _transform("b", "inputs['n']", x=200),
            ],
            "edges": [
                {"id": "e_ab", "source": "a", "target": "b", "data": {"mappings": {"n": "n"}}},
                {
                    "id": "e_ba",
                    "source": "b",
                    "target": "a",
                    "data": {
                        "kind": "conditional",
                        "condition": "inputs['result'] < 2",
                        "mappings": {"n": "result"},
                    },
                },
            ],
            "entry_nodes": ["a"],
        }
    )
    graph = compile_graph(definition, registry=registry)
    # The forward edge stays a full join edge; only the feedback edge is
    # excluded from a's required set.
    assert graph.edges["e_ba"].is_back_edge is True
    assert graph.edges["e_ab"].is_back_edge is False
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )

    result = await scheduler.run(run_id="f13-two-cycle", max_steps=20)

    # a: n=0→1; b echoes 1; 1<2 → a re-fires with n=1→2; b echoes 2;
    # 2<2 false → terminate. Each back-edge delivery re-fired a once.
    assert result.status is RunStatus.COMPLETED
    assert counter.calls == [{"n": 0}, {"n": 1}]
    assert result.last_outputs["b"] == {"result": 2}


def test_disconnected_cycle_is_a_loud_compile_error():
    registry, _recorder, _counter = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _transform("x", "'ENTRY'"),
                _counter_node("c1", x=200),
                _counter_node("c2", x=400),
            ],
            "edges": [
                {"id": "e_12", "source": "c1", "target": "c2", "data": {"mappings": {"n": "n"}}},
                {"id": "e_21", "source": "c2", "target": "c1", "data": {"mappings": {"n": "n"}}},
            ],
        }
    )
    with pytest.raises(CompilationError) as exc_info:
        compile_graph(definition, registry=registry)
    msg = str(exc_info.value)
    assert "c1" in msg and "c2" in msg
    assert "entry" in msg.lower()

"""Regression coverage for the Phase 0 / Phase 1 lifecycle additions:
pause, two cancel modes, recoverable node failures, pre-emptive node
skip-list, and the user-skip / user-manual recovery paths.

These tests run the real Scheduler against an in-memory checkpointer
and a registry of built-in nodes only — no AI / scraper / DB
dependencies — so they're cheap, deterministic, and safe in CI."""

from __future__ import annotations

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)

from tests._fixtures import FakeEmitter, make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _two_step_definition() -> Definition:
    """Tiny linear graph: ``a`` -> ``b``. Each node uses ``data.transform``
    with a constant expression so the graph runs in two super-steps and
    each node has typed output we can inspect."""
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "a",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "'ALPHA'"}},
                },
                {
                    "id": "b",
                    "type": "data.transform",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"expression": "'BETA'"}},
                },
            ],
            "edges": [{"id": "e1", "source": "a", "target": "b"}],
        }
    )


# ---------------------------------------------------------------------------
# Pause
# ---------------------------------------------------------------------------


async def test_pause_check_transitions_run_to_paused_with_checkpoint():
    """When ``pause_check`` returns True between super-steps the scheduler
    saves a checkpoint, emits ``run_paused``, and returns
    ``RunStatus.PAUSED``. The events log proves the lifecycle wired up
    correctly."""
    registry = _registry()
    graph = compile_graph(_two_step_definition(), registry=registry)
    emitter = FakeEmitter()
    checkpointer = MemoryCheckpointer()

    # Pause immediately on the FIRST poll — i.e. before any super-step
    # has run. We expect a paused result with steps_executed=0.
    async def always_pause() -> bool:
        return True

    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(emitter),
        registry=registry,
        pause_check=always_pause,
    )

    result = await scheduler.run(run_id="pause-1")
    assert result.status is RunStatus.PAUSED
    assert result.steps_executed == 0

    kinds = [e.get("event") for k, e in emitter.events if k == "data" and isinstance(e, dict)]
    assert "run_paused" in kinds
    # No node events should fire because the pause happened before step 0.
    assert "node_started" not in kinds


async def test_resume_after_pause_announces_the_running_transition():
    """The pause → resume-paused walk, on the RUN'S OWN event stream.

    The resumed leg must announce paused→running BEFORE it executes
    anything: ``run_resumed`` first, then the node work, then the terminal
    ``run_completed``. Without the leading frame a client folding this
    stream held "paused" for the entire resumed leg (the run visibly ran
    while the hero said PAUSED, and only a reload showed truth).
    """
    registry = _registry()
    graph = compile_graph(_two_step_definition(), registry=registry)
    checkpointer = MemoryCheckpointer()

    async def always_pause() -> bool:
        return True

    paused = await Scheduler(
        graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
        pause_check=always_pause,
    ).run(run_id="resume-announce-1")
    assert paused.status is RunStatus.PAUSED
    checkpoints = await checkpointer.list_checkpoints("resume-announce-1")
    assert checkpoints

    emitter = FakeEmitter()
    resumed = await Scheduler(
        graph,
        checkpointer,
        make_app_context(emitter),
        registry=registry,
    ).resume(
        run_id="resume-announce-1",
        checkpoint_id=checkpoints[-1].checkpoint_id,
    )
    assert resumed.status is RunStatus.COMPLETED

    events = [e for k, e in emitter.events if k == "data" and isinstance(e, dict)]
    kinds = [e.get("event") for e in events]
    assert "run_resumed" in kinds, f"resumed leg announced no status transition: {kinds}"
    # Leading frame — the status reaches the stream before any node work.
    assert kinds[0] == "run_resumed"
    assert kinds.index("run_resumed") < kinds.index("node_started")
    # ...and the leg still ends with its terminal status on the same stream.
    assert kinds[-1] == "run_completed"

    frame = events[kinds.index("run_resumed")]
    assert frame["run_id"] == "resume-announce-1"
    assert frame["from_checkpoint_id"] == checkpoints[-1].checkpoint_id
    # A pause park carries no interrupt payload — this is a resume-paused.
    assert frame["mode"] == "pause"


async def test_pause_takes_priority_over_cancel():
    """If both ``pause_check`` and ``cancel_check`` return True on the
    same poll, pause wins — the user's most recent intent was to suspend,
    not abandon."""
    registry = _registry()
    graph = compile_graph(_two_step_definition(), registry=registry)
    emitter = FakeEmitter()

    async def yes() -> bool:
        return True

    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
        pause_check=yes,
        cancel_check=yes,
    )

    result = await scheduler.run(run_id="pause-priority")
    assert result.status is RunStatus.PAUSED
    kinds = [e.get("event") for k, e in emitter.events if k == "data" and isinstance(e, dict)]
    assert "run_paused" in kinds
    assert "run_cancelled" not in kinds


# ---------------------------------------------------------------------------
# Cancel
# ---------------------------------------------------------------------------


async def test_cancel_check_returns_run_cancelled_after_clean_exit():
    """Graceful cancel: ``cancel_check`` returns True, scheduler saves a
    checkpoint, emits ``run_cancelled`` with reason='graceful', and
    returns ``RunStatus.CANCELLED``."""
    registry = _registry()
    graph = compile_graph(_two_step_definition(), registry=registry)
    emitter = FakeEmitter()

    async def cancel_now() -> bool:
        return True

    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
        cancel_check=cancel_now,
    )

    result = await scheduler.run(run_id="cancel-1")
    assert result.status is RunStatus.CANCELLED

    cancelled_events = [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "run_cancelled"
    ]
    assert len(cancelled_events) == 1
    assert cancelled_events[0].get("reason") == "graceful"


# ---------------------------------------------------------------------------
# Pre-emptive node skip-list
# ---------------------------------------------------------------------------


async def test_skip_node_ids_short_circuits_specified_node():
    """``skip_node_ids`` causes the scheduler to synthesize an empty
    output for the listed node, emit ``node_skipped``, record a
    ``user_skip`` outcome, and route the empty payload downstream.
    Downstream nodes still run."""
    registry = _registry()
    graph = compile_graph(_two_step_definition(), registry=registry)
    emitter = FakeEmitter()
    checkpointer = MemoryCheckpointer()

    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(emitter),
        registry=registry,
        skip_node_ids={"a"},
    )
    result = await scheduler.run(run_id="skip-1")
    assert result.status is RunStatus.COMPLETED

    kinds = [e.get("event") for k, e in emitter.events if k == "data" and isinstance(e, dict)]
    # ``a`` is skipped, ``b`` runs normally.
    skipped = [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "node_skipped"
    ]
    assert len(skipped) == 1
    assert skipped[0]["node_id"] == "a"
    assert "node_completed" in kinds  # b completed

    # And the user_skip outcome is durable in the checkpointer.
    outcome = await checkpointer.get_outcome(run_id="skip-1", step=0, node_id="a", attempt=1)
    assert outcome is not None
    assert outcome.source == "user_skip"
    assert outcome.error is None


# ---------------------------------------------------------------------------
# Recoverable failure → ERRORED state
# ---------------------------------------------------------------------------


def _failing_definition() -> Definition:
    """Two-node graph where node ``boom`` fails. ``data.assert`` with a
    false predicate raises inside the executor — that's how we trigger
    the recoverable-error path."""
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "boom",
                    "type": "data.assert",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {
                            "predicate": "False",
                            "message": "intentional test failure",
                        }
                    },
                },
                {
                    "id": "after",
                    "type": "data.transform",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"expression": "'AFTER'"}},
                },
            ],
            "edges": [{"id": "e1", "source": "boom", "target": "after"}],
        }
    )


async def test_node_failure_parks_run_in_errored_state_with_checkpoint():
    """A node raising → scheduler records a failed NodeOutcome, saves a
    checkpoint with the failing invocation in ``next_invocations``,
    emits ``run_errored``, and returns ``RunStatus.ERRORED``."""
    registry = _registry()
    graph = compile_graph(_failing_definition(), registry=registry)
    emitter = FakeEmitter()
    checkpointer = MemoryCheckpointer()

    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="err-1")
    assert result.status is RunStatus.ERRORED
    assert result.error and "intentional test failure" in result.error

    errored_events = [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "run_errored"
    ]
    assert len(errored_events) == 1
    assert errored_events[0]["node_id"] == "boom"

    # Failure outcome is durable.
    failure = await checkpointer.get_outcome(run_id="err-1", step=0, node_id="boom", attempt=1)
    assert failure is not None
    assert failure.error is not None
    assert "intentional test failure" in str(failure.error)

    # ``after`` did NOT run.
    after = await checkpointer.get_outcome(run_id="err-1", step=1, node_id="after", attempt=1)
    assert after is None


async def test_user_skip_outcome_lets_downstream_complete():
    """The recovery primitive: write a synthetic user_skip outcome with
    empty output for the failed node, then resume from the errored
    checkpoint. The scheduler's idempotency replay picks up the success
    outcome and routes the empty payload to the downstream node, which
    runs to completion."""
    from matrx_graph.checkpoint.protocol import NodeOutcome

    registry = _registry()
    graph = compile_graph(_failing_definition(), registry=registry)
    emitter = FakeEmitter()
    checkpointer = MemoryCheckpointer()

    # First run errors as expected.
    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(emitter),
        registry=registry,
    )
    initial = await scheduler.run(run_id="err-skip-1")
    assert initial.status is RunStatus.ERRORED

    # Overwrite the failed outcome with a user_skip success. ``data.assert``
    # requires ``inputs`` in its output schema, so a valid skip outcome
    # supplies that field (the in-product /skip endpoint does the same
    # via spec.output_schema.model_construct when {} is supplied).
    await checkpointer.record_outcome(
        NodeOutcome(
            run_id="err-skip-1",
            step=0,
            node_id="boom",
            attempt=1,
            output={"passed": True, "inputs": {}},
            error=None,
            source="user_skip",
        )
    )

    # Resume from the errored checkpoint (the latest one on the run).
    last_cp = await checkpointer.latest_checkpoint(run_id="err-skip-1")
    assert last_cp is not None

    resumed_emitter = FakeEmitter()
    resumed = Scheduler(
        graph,
        checkpointer,
        make_app_context(resumed_emitter),
        registry=registry,
    )
    final = await resumed.resume(run_id="err-skip-1", checkpoint_id=last_cp.checkpoint_id)
    assert final.status is RunStatus.COMPLETED
    # ``after`` ran on the resume.
    after = await checkpointer.get_outcome(run_id="err-skip-1", step=1, node_id="after", attempt=1)
    assert after is not None
    assert after.error is None

"""A resume after a server restart says why, and keeps the cut-off attempt's spend.

Live run 9453a819 (2026-10-27): the server running step ``improve`` stopped mid-step; the
recovery lane resumed the run from the checkpoint before that step, so the step ran again
from scratch. The run log went from the step's progress straight to a bare ``run_resumed``
(no reason — the studio looked frozen for two minutes) and the step's ``node_cost`` counted
only the second attempt ($0.99 of the $1.41 the ledger held for it).
"""

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
from matrx_graph.spend_gate import InterruptedAttempt

from tests._fixtures import FakeEmitter, make_app_context


def _graph_and_registry():
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    definition = Definition.model_validate(
        {
            "nodes": [
                {"id": "a", "type": "data.transform", "position": {"x": 0, "y": 0},
                 "data": {"config": {"expression": "'ALPHA'"}}},
                {"id": "b", "type": "data.transform", "position": {"x": 200, "y": 0},
                 "data": {"config": {"expression": "'BETA'"}}},
            ],
            "edges": [{"id": "e1", "source": "a", "target": "b"}],
        }
    )
    return compile_graph(definition, registry=reg), reg


async def _parked_before_a(run_id: str):
    graph, reg = _graph_and_registry()
    checkpointer = MemoryCheckpointer()

    async def always_pause() -> bool:
        return True

    paused = await Scheduler(
        graph, checkpointer, make_app_context(FakeEmitter()), registry=reg, pause_check=always_pause
    ).run(run_id=run_id)
    assert paused.status is RunStatus.PAUSED
    checkpoint = (await checkpointer.list_checkpoints(run_id))[-1]
    return graph, reg, checkpointer, checkpoint.checkpoint_id


def _events(emitter: FakeEmitter) -> list[dict]:
    return [e for k, e in emitter.events if k == "data" and isinstance(e, dict)]


async def test_a_restart_resume_names_its_reason_and_settles_the_cut_off_attempts():
    graph, reg, checkpointer, checkpoint_id = await _parked_before_a("restart-1")
    emitter = FakeEmitter()
    result = await Scheduler(graph, checkpointer, make_app_context(emitter), registry=reg).resume(
        run_id="restart-1",
        checkpoint_id=checkpoint_id,
        restarted_after="server_restart",
        interrupted_attempts=[
            InterruptedAttempt(request_id="1c8a436d", node_id="a", cost_usd=0.425466,
                               input_tokens=80_000, output_tokens=900, model="claude-opus-5-5"),
            # Never guessed onto a step: no step named, or a step that is not starting again
            # (``b`` had not started — it is held for a later step).
            InterruptedAttempt(request_id="2d9b547e", cost_usd=0.01, input_tokens=10, output_tokens=5),
            InterruptedAttempt(request_id="3eac658f", node_id="b", cost_usd=0.02),
        ],
    )
    assert result.status is RunStatus.COMPLETED

    events = _events(emitter)
    resumed = next(e for e in events if e.get("event") == "run_resumed")
    assert resumed["reason"] == "server_restart"
    assert resumed["restarted_node_ids"] == ["a"]

    costs = [e for e in events if e.get("event") == "node_cost" and e.get("interrupted")]
    assert [(c["node_id"], c["request_id"], c["cost_usd"]) for c in costs] == [
        ("a", "1c8a436d", 0.425466),
    ]
    assert costs[0]["input_tokens"] == 80_000 and costs[0]["model"] == "claude-opus-5-5"
    # Announced before the step starts again.
    kinds = [e.get("event") for e in events]
    assert kinds.index("run_resumed") < kinds.index("node_started")


async def test_an_ordinary_resume_carries_no_restart_and_settles_nothing():
    graph, reg, checkpointer, checkpoint_id = await _parked_before_a("restart-2")
    emitter = FakeEmitter()
    await Scheduler(graph, checkpointer, make_app_context(emitter), registry=reg).resume(
        run_id="restart-2", checkpoint_id=checkpoint_id
    )
    events = _events(emitter)
    resumed = next(e for e in events if e.get("event") == "run_resumed")
    assert resumed["reason"] is None
    assert resumed["restarted_node_ids"] == []
    assert not [e for e in events if e.get("event") == "node_cost" and e.get("interrupted")]


async def test_an_attempt_naming_no_restarted_step_is_never_put_on_a_wrong_one():
    graph, reg, checkpointer, checkpoint_id = await _parked_before_a("restart-3")
    emitter = FakeEmitter()
    await Scheduler(graph, checkpointer, make_app_context(emitter), registry=reg).resume(
        run_id="restart-3",
        checkpoint_id=checkpoint_id,
        restarted_after="server_restart",
        interrupted_attempts=[InterruptedAttempt(request_id="x", node_id="gone", cost_usd=1.0)],
    )
    assert not [e for e in _events(emitter) if e.get("event") == "node_cost" and e.get("interrupted")]


async def test_a_restart_from_the_inputs_names_its_reason_and_settles_the_first_step():
    """No checkpoint yet (the server stopped inside the first step): the recovery lane
    starts the run again from its inputs, through ``run`` — not ``resume``."""
    graph, reg = _graph_and_registry()
    emitter = FakeEmitter()
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=reg).run(
        run_id="restart-4",
        restarted_after="server_restart",
        interrupted_attempts=[InterruptedAttempt(request_id="r1", node_id="a", cost_usd=0.3)],
    )
    assert result.status is RunStatus.COMPLETED
    events = _events(emitter)
    started = next(e for e in events if e.get("event") == "run_started")
    assert started["reason"] == "server_restart"
    assert started["restarted_node_ids"] == ["a"]
    costs = [e for e in events if e.get("event") == "node_cost" and e.get("interrupted")]
    assert [(c["node_id"], c["cost_usd"]) for c in costs] == [("a", 0.3)]


async def test_an_ordinary_start_carries_no_restart():
    graph, reg = _graph_and_registry()
    emitter = FakeEmitter()
    await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=reg).run(run_id="restart-5")
    started = next(e for e in _events(emitter) if e.get("event") == "run_started")
    assert started["reason"] is None and started["restarted_node_ids"] == []

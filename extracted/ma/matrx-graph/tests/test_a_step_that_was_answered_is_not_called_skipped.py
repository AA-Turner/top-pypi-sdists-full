"""A step the person answered (or approved) is not "Skipped" — the event says which road it took.

W1.1 (2026-10-02). A held write pauses its run; the person approves; the run resumes and the
engine REPLAYS the recorded decision as the step's outcome. Replay, a person's Skip and a mock
all arrive as ``node_skipped``, and the studio painted all three "Skipped" — so an approved,
applied write told its author it never happened. ``NodeSkippedEvent.source`` carries the
outcome's own source (``OutcomeSource``) so a screen can tell them apart.

Real engine: real registry, compiler, ``Scheduler.run``/``resume`` and the real
``control.human_input`` executor over ``MemoryCheckpointer`` (the same protocol Postgres
implements).
"""

from __future__ import annotations

from typing import Any, get_args

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.checkpoint.protocol import OutcomeSource
from matrx_graph.types.events import NodeSkippedEvent

from tests._fixtures import FakeEmitter, make_app_context


def _graph() -> dict[str, Any]:
    return {
        "nodes": [
            {
                "id": "ask",
                "type": "control.human_input",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"title": "Approve?", "preset": "free_text", "prompt": "Approve?"}},
            },
            {
                "id": "after",
                "type": "data.transform",
                "position": {"x": 320, "y": 0},
                "data": {"config": {"expression": "'got: ' + inputs['a']"}},
            },
        ],
        "edges": [
            {
                "id": "e",
                "source": "ask",
                "target": "after",
                "data": {"kind": "data", "mappings": {"a": "answer"}},
            }
        ],
    }


def _skipped(emitter: FakeEmitter) -> list[dict[str, Any]]:
    return [e for k, e in emitter.events if k == "data" and isinstance(e, dict) and e.get("event") == "node_skipped"]


async def test_an_answered_step_replays_as_an_executor_outcome_not_a_skip() -> None:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(Definition.model_validate(_graph()), registry=registry)
    checkpointer = MemoryCheckpointer()
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, checkpointer, make_app_context(emitter), registry=registry)

    first = await scheduler.run(run_id="answered")
    assert first.status is RunStatus.INTERRUPTED
    parked = await checkpointer.latest_checkpoint("answered")
    assert parked is not None
    resumed = await scheduler.resume(
        run_id="answered", checkpoint_id=parked.checkpoint_id, resume_value={"answer": "yes"}
    )
    assert resumed.status is RunStatus.COMPLETED

    settled = [e for e in _skipped(emitter) if e["node_id"] == "ask"]
    assert settled, "the answered step never settled on resume"
    assert all(e.get("source") == "executor" for e in settled), (
        "the answered step settled with no road named, so the studio paints it 'Skipped': "
        f"{[e.get('source') for e in settled]}"
    )


async def test_a_real_skip_still_says_it_was_skipped() -> None:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(Definition.model_validate(_graph()), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry, skip_node_ids={"ask"}
    )
    await scheduler.run(run_id="skipped")
    assert [e.get("source") for e in _skipped(emitter) if e["node_id"] == "ask"] == ["user_skip"]


def test_the_event_speaks_the_outcome_vocabulary() -> None:
    declared = NodeSkippedEvent.model_fields["source"].annotation
    roads = {a for arg in get_args(declared) for a in (get_args(arg) or (arg,)) if a is not type(None)}
    assert roads == set(get_args(OutcomeSource)), (
        "NodeSkippedEvent.source drifted from OutcomeSource — a road one side names, the other cannot."
    )

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
from matrx_graph import kinds as kinds_mod

from tests._fixtures import FakeEmitter, make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


async def test_emits_run_and_node_lifecycle_events():
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "double",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "inputs['value'] * 2"}},
                },
                {
                    "id": "plus3",
                    "type": "data.transform",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"expression": "inputs['result'] + 3"}},
                },
            ],
            "edges": [{"id": "e1", "source": "double", "target": "plus3"}],
        }
    )
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    app = make_app_context(emitter)
    scheduler = Scheduler(graph, MemoryCheckpointer(), app, registry=registry)

    result = await scheduler.run(run_id="run-events-1", inputs={"value": 5})

    assert result.status is RunStatus.COMPLETED

    data_events = [p for k, p in emitter.events if k == "data"]
    event_types = [e["event"] for e in data_events if isinstance(e, dict) and "event" in e]

    # Run boundary events
    assert event_types[0] == "run_started"
    assert event_types[-1] == "run_completed"

    # Every node produced started + completed
    assert event_types.count("node_started") == 2
    assert event_types.count("node_completed") == 2

    # Checkpoints after each step
    assert event_types.count("checkpoint_saved") >= 2

    # Completed event carries final outputs
    completed = [e for e in data_events if e.get("event") == "run_completed"][0]
    assert completed["last_outputs"]["plus3"]["result"] == 13


async def test_emits_run_interrupted_event():
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "ask",
                    "type": "control.human_input",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"prompt": "continue?"}},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id="run-int-1")
    assert result.status is RunStatus.INTERRUPTED

    data_events = [p for k, p in emitter.events if k == "data"]
    interrupted = [e for e in data_events if e.get("event") == "run_interrupted"]
    assert len(interrupted) == 1
    assert interrupted[0]["node_id"] == "ask"
    assert interrupted[0]["payload"]["prompt"] == "continue?"
    assert interrupted[0]["checkpoint_id"]


async def test_emits_node_failed_event_and_run_errored():
    # Phase 1 (2026-05-18): per-node failures park the run at status=ERRORED
    # instead of raising. The scheduler emits NodeFailedEvent (unchanged)
    # AND RunErroredEvent (new — replaces RunFailedEvent for recoverable
    # paths). RunFailedEvent is now reserved for framework-level errors
    # (compile failures, max_steps exceeded, unhandled exceptions in the
    # scheduler itself).
    from matrx_graph import RunStatus

    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "bad",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "inputs['missing_key'] + 1"}},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)

    result = await scheduler.run(run_id="run-failed-1")
    assert result.status is RunStatus.ERRORED

    data_events = [p for k, p in emitter.events if k == "data"]
    event_types = [e["event"] for e in data_events if isinstance(e, dict) and "event" in e]
    assert "node_failed" in event_types
    assert "run_errored" in event_types


async def test_node_skipped_event_on_idempotent_replay():
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "t",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "inputs['v'] + 1"}},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()

    # First run populates the outcome
    first_emitter = FakeEmitter()
    await Scheduler(graph, checkpointer, make_app_context(first_emitter), registry=registry).run(
        run_id="run-skip-1", inputs={"v": 1}
    )

    # Second run with same run_id should replay — expect node_skipped, not node_started
    second_emitter = FakeEmitter()
    await Scheduler(graph, checkpointer, make_app_context(second_emitter), registry=registry).run(
        run_id="run-skip-1", inputs={"v": 1}
    )

    data_events = [p for k, p in second_emitter.events if k == "data"]
    event_types = [e["event"] for e in data_events if isinstance(e, dict) and "event" in e]
    assert "node_skipped" in event_types
    assert "node_started" not in event_types


async def _run_single_node(node: dict, inputs: dict) -> list[dict]:
    """Run a one-node definition and return its ``data`` event payloads."""
    registry = _registry()
    definition = Definition.model_validate({"nodes": [node], "edges": []})
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    app = make_app_context(emitter)
    result = await Scheduler(graph, MemoryCheckpointer(), app, registry=registry).run(
        run_id=f"run-started-kind-{node['id']}", inputs=inputs
    )
    assert result.status is RunStatus.COMPLETED
    return [p for k, p in emitter.events if k == "data" and isinstance(p, dict)]


async def test_node_started_announces_spec_declared_output_kind():
    """A node whose KIND comes from its NodeSpec (no ``data.output_kind``)
    announces that kind on node_started — the UI can reserve the kind's
    loading silhouette while the node streams instead of waiting for
    node_completed (the Study Pack v2 ``structure`` gap)."""
    events = await _run_single_node(
        {
            "id": "fp",
            "type": "crypto.hash",
            "position": {"x": 0, "y": 0},
            "data": {"config": {}, "inputs": {"text": "hello"}},
        },
        inputs={"text": "hello"},
    )
    started = [e for e in events if e.get("event") == "node_started"][0]
    assert started["output_kind"] == "hash_result"


async def test_node_started_announces_data_declared_output_kind_override(monkeypatch):
    """``data.output_kind`` (the workflow author's binding) overrides the
    spec default and is what node_started announces — the same compile-time
    resolution the settlement path starts from.

    This test is about the node_started announcement only, not about kind
    VALIDATION — so workflow_io enforcement is pinned off here: the chosen
    slug ('structured_document') collides with a real platform kind name,
    and this node's actual output (an int) does not conform to it, which
    would otherwise make the run FATAL under the shipped ON default and
    obscure the thing this test exists to check."""
    monkeypatch.setitem(kinds_mod.KIND_ENFORCEMENT, "workflow_io", False)
    events = await _run_single_node(
        {
            "id": "t",
            "type": "data.transform",
            "position": {"x": 0, "y": 0},
            "data": {
                "config": {"expression": "inputs['v'] + 1"},
                "output_kind": "structured_document",
            },
        },
        inputs={"v": 1},
    )
    started = [e for e in events if e.get("event") == "node_started"][0]
    assert started["output_kind"] == "structured_document"


async def test_node_started_output_kind_null_for_kindless_node():
    """A node with no spec kind and no authored override announces None."""
    events = await _run_single_node(
        {
            "id": "t",
            "type": "data.transform",
            "position": {"x": 0, "y": 0},
            "data": {"config": {"expression": "inputs['v'] + 1"}},
        },
        inputs={"v": 1},
    )
    started = [e for e in events if e.get("event") == "node_started"][0]
    assert started["output_kind"] is None

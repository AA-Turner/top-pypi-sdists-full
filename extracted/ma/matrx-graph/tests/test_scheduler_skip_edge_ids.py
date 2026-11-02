"""Phase 5.2 — pre-emptive edge skip.

skip_edge_ids causes the scheduler's _route_outputs to silently drop
the listed edges when their source node completes. Downstream targets
that depended on the skipped edge receive nothing — they may fail (and
the failure is recoverable like any other) or may proceed if other
inbound edges still carry payload.

Verifies:
    1. Default (no skip) — both downstream nodes receive their payload.
    2. skip_edge_ids={e1} — only the un-skipped edge fires; the skipped
       target sees no input.
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

from tests._fixtures import FakeEmitter, make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _fan_out_definition() -> Definition:
    """a → b (via e_ab) and a → c (via e_ac). Both downstream nodes are
    data.transform constants so we can confirm whether they ran by
    looking at last_outputs."""
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
                {
                    "id": "c",
                    "type": "data.transform",
                    "position": {"x": 200, "y": 100},
                    "data": {"config": {"expression": "'GAMMA'"}},
                },
            ],
            "edges": [
                {"id": "e_ab", "source": "a", "target": "b"},
                {"id": "e_ac", "source": "a", "target": "c"},
            ],
        }
    )


async def test_default_no_skip_runs_both_downstreams():
    registry = _registry()
    graph = compile_graph(_fan_out_definition(), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="edge-skip-default")
    assert result.status is RunStatus.COMPLETED
    # Both b and c ran — they're in last_outputs.
    assert "b" in result.last_outputs
    assert "c" in result.last_outputs


async def test_skip_edge_drops_payload_to_target():
    """skip_edge_ids={'e_ac'} → c never gets routed → c never executes.
    a and b complete normally."""
    registry = _registry()
    graph = compile_graph(_fan_out_definition(), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
        skip_edge_ids={"e_ac"},
    )
    result = await scheduler.run(run_id="edge-skip-one")
    assert result.status is RunStatus.COMPLETED
    # b ran (its edge wasn't skipped); c did NOT run (its only inbound
    # edge was skipped — _route_outputs never produced an invocation
    # for it).
    assert "b" in result.last_outputs
    assert "c" not in result.last_outputs
    # node_completed events confirm: 2 (a, b), not 3.
    completed = [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "node_completed"
    ]
    completed_ids = {e["node_id"] for e in completed}
    assert "a" in completed_ids
    assert "b" in completed_ids
    assert "c" not in completed_ids

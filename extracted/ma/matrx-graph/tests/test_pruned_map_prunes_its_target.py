"""A PRUNED ``control.map`` prunes its dispatch target's subtree, exactly like a map that fired with 0 items.

Live 2026-10-24 (aidream ``brand_foundation`` run ffcbb913): each specialist branch is ``stage -(count > 0)-> map ⇉
worker -> gather -> ...``, and every branch's last step feeds ONE join-``all`` step (the Curator's hand-on). A branch
whose condition was false pruned its map, but the worker is reached only by the map's Send — no inbound edge — so
nothing ever resolved the worker's outgoing edges: the gather and everything after it stayed unresolved and the run
parked ERRORED with "Join deadlock". A map that FIRES with 0 items already resolves its target subtree as pruned;
a map that never fires now does the same.
"""

from __future__ import annotations

from matrx_graph import Definition, RunStatus

from tests.test_multi_dispatch_fanin import _registry, _run


def _definition() -> dict:
    return {
        "nodes": [
            {"id": "src", "type": "test.upper_worker", "position": {"x": 0, "y": 0},
             "data": {"config": {}, "input": {"value": "x"}}},
            {"id": "map1", "type": "control.map", "position": {"x": 0, "y": 0},
             "data": {"config": {"target_node_id": "worker", "payload_key": "value"}}},
            {"id": "worker", "type": "test.upper_worker", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            {"id": "gather", "type": "control.gather", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            {"id": "after", "type": "test.upper_worker", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            {"id": "sink", "type": "test.upper_worker", "position": {"x": 0, "y": 0},
             "data": {"config": {}, "join_policy": "all"}},
        ],
        "edges": [
            {"id": "e_go", "source": "src", "target": "map1", "type": "default",
             "data": {"kind": "conditional", "condition": "inputs['result'] == 'never'",
                      "mappings": {"items": "result"}}},
            {"id": "e_gather", "source": "worker", "target": "gather", "type": "default", "data": {"kind": "data"}},
            {"id": "e_after", "source": "gather", "target": "after", "type": "default",
             "data": {"kind": "data", "mappings": {"value": "count"}}},
            {"id": "e_sink_branch", "source": "after", "target": "sink", "type": "default",
             "data": {"kind": "data", "mappings": {"branch": "result"}}},
            {"id": "e_sink_src", "source": "src", "target": "sink", "type": "default",
             "data": {"kind": "data", "mappings": {"value": "result"}}},
        ],
        "entry_nodes": ["src"],
    }


async def test_a_pruned_map_prunes_its_worker_subtree_and_the_join_fires():
    registry, worker = _registry()
    result = await _run(Definition.model_validate(_definition()), registry, "pruned-map-1")
    assert result.status == RunStatus.COMPLETED, getattr(result, "error", None)
    # src and sink ran; the pruned branch's worker and "after" never did.
    assert worker.processed == ["x", "X"]

"""ENGINE_SPEC §6.1 resolution (D3): ``control.barrier`` is REMOVED.

Decision record: §3 join semantics already make a plain multi-inbound node
fire exactly once when all its edges resolve (an edge-wired barrier is just a
join), and §4.4 aggregated-dispatch makes map fan-ins synchronize
automatically (``control.gather``). The one case the old executor claimed —
counting same-step Send arrivals via a sum channel — was structurally broken
(audit E4: N same-step invocations each read the SAME pre-step channel
snapshot, so none ever saw the others arrive) and cannot be fixed without
barrier-specific aggregation inside the scheduler. Rather than keep a
silently-wrong node, registration is gone and a LOUD registry tombstone
rejects any definition still using it.
"""

from __future__ import annotations

from matrx_graph import NodeRegistry, compile_graph, register_builtin_nodes, validate_definition
from matrx_graph.errors import CompilationError

import pytest


def _barrier_definition() -> dict:
    return {
        "nodes": [
            {
                "id": "sync",
                "type": "control.barrier",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"channel": "arrivals", "expected_count": 3}},
            }
        ],
        "edges": [],
    }


def test_barrier_is_not_registered() -> None:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    assert not reg.has("control.barrier")


def test_validate_definition_tombstones_barrier() -> None:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    result = validate_definition(_barrier_definition(), registry=reg)
    assert not result.valid
    messages = " ".join(issue.message for issue in result.issues)
    assert "control.barrier was removed" in messages
    assert "control.gather" in messages  # points the author at the replacement
    assert result.issues[0].node_id == "sync"


def test_compile_rejects_barrier_definition() -> None:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    from matrx_graph import Definition

    with pytest.raises(CompilationError):
        compile_graph(Definition.model_validate(_barrier_definition()), registry=reg)

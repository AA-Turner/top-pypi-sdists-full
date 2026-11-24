"""A step knows which parts of its output its outgoing connections read (``CompiledGraph.output_reads``).

Ruled 2026-11-02 (Arman): a called workflow hands back only what the caller's connections read. The
engine hands each step that answer in ``ctx.output_reads``: the source paths its connections read,
or None when the whole output is read. Getting None wrong in the narrow direction would starve a
step of data, so every way a connection can read the whole output must say None.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import Definition, compile_graph, default_registry
from matrx_graph.nodes import register_builtin_nodes


def _graph(edges: list[dict[str, Any]]) -> Any:
    register_builtin_nodes(overwrite=True)
    node = {"type": "data.transform", "position": {"x": 0, "y": 0}, "data": {"config": {"expression": "1"}}}
    return compile_graph(
        Definition.model_validate(
            {
                "nodes": [{"id": n, **node} for n in ("a", "b", "c")],
                "edges": edges,
                "entry_nodes": ["a"],
            }
        ),
        registry=default_registry(),
    )


def _edge(target: str, data: dict[str, Any], **extra: Any) -> dict[str, Any]:
    return {"id": f"a_{target}_{len(data)}", "source": "a", "target": target, "data": data, **extra}


def test_mapped_connections_name_the_paths_they_read() -> None:
    g = _graph([
        _edge("b", {"kind": "data", "mappings": {"items": "last_outputs.picks.score_rows"}}),
        _edge("c", {"kind": "data", "mappings": {"x": "last_outputs.picks.post_rows ?? []", "y": "trim(run_id)"}}),
    ])
    assert g.output_reads("a") == ("last_outputs.picks.score_rows", "last_outputs.picks.post_rows", "run_id")


def test_a_step_with_no_connections_reads_its_whole_output() -> None:
    # Its output is the run's answer.
    assert _graph([]).output_reads("a") is None


def test_every_whole_output_connection_says_none() -> None:
    assert _graph([_edge("b", {"kind": "data"})]).output_reads("a") is None
    assert _graph([_edge("b", {"kind": "data", "mappings": {"v": "$FULL_PAYLOAD"}})]).output_reads("a") is None
    assert _graph([_edge("b", {"kind": "data", "mappings": {"v": "@"}})]).output_reads("a") is None
    conditional = _edge("b", {"kind": "conditional", "condition": "x > 1", "mappings": {"v": "x"}})
    assert _graph([conditional]).output_reads("a") is None


def test_control_and_error_connections_read_nothing() -> None:
    g = _graph([
        _edge("b", {"kind": "control"}),
        _edge("c", {"kind": "error"}),
        {"id": "a_b_m", "source": "a", "target": "b", "data": {"kind": "data", "mappings": {"v": "last_outputs.x"}}},
    ])
    assert g.output_reads("a") == ("last_outputs.x",)

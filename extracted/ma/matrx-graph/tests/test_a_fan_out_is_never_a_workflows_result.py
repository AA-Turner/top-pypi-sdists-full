"""A fan-out step is never a workflow's result.

Live 2026-10-27 (run 07320d26, unit research.keyword): the unit
``research.summarize_pages`` fans its pages out (``control.map`` → mandate →
``control.gather`` → … → a final ``data.transform``). The map dispatches by Send,
not by an edge, so it LOOKED terminal; it was the only "terminal" step declaring
a kind, so publish backfilled the workflow's ``output_kind = map_result`` and
every caller received the map's dispatch receipt ``{"dispatched": 3}`` instead of
the gathered answer.

Each test fails on the engine before the fix: ``compute_deliverables`` counted
the map, ``resolve_io_declaration`` backfilled ``map_result``, and
``declared_result`` accepted a dispatcher as the result.
"""

from __future__ import annotations

import pytest

from matrx_graph import Definition, compile_graph, register_builtin_nodes
from matrx_graph.executor.registry import NodeRegistry
from matrx_graph.types.deliverables import compute_deliverables, declared_result, resolve_io_declaration


def _registry() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return registry


def _node(node_id: str, spec_type: str, config: dict | None = None, **data: object) -> dict:
    return {
        "id": node_id,
        "type": spec_type,
        "position": {"x": 0, "y": 0},
        "data": {"config": config or {}, **data},
    }


def _fan_out_unit(*, primary_on_map: bool = False) -> Definition:
    """The live shape: take → map ⇒ (Send) work → gather → result."""
    extra = {"is_primary": True, "deliverable": True} if primary_on_map else {}
    return Definition.model_validate(
        {
            "nodes": [
                _node("take", "data.transform", {"expression": "inputs"}),
                _node(
                    "each",
                    "control.map",
                    {"target_node_id": "work"},
                    **extra,
                ),
                _node("work", "data.transform", {"expression": "inputs"}),
                _node("done", "control.gather"),
                _node("result", "data.transform", {"expression": "inputs"}),
            ],
            "edges": [
                {"id": "e1", "source": "take", "target": "each"},
                {"id": "e2", "source": "work", "target": "done"},
                {"id": "e3", "source": "done", "target": "result"},
            ],
            "entry_nodes": ["take"],
        }
    )


def test_a_map_that_dispatches_by_send_is_not_a_deliverable() -> None:
    definition = _fan_out_unit()
    graph = compile_graph(definition, registry=_registry())
    assert not graph.nodes["each"].outgoing_edge_ids  # looks terminal — the trap
    assert graph.nodes["each"].output_kind == "map_result"

    assert [d.node_id for d in compute_deliverables(graph, definition)] == []
    verdict = resolve_io_declaration(graph, definition)
    assert verdict.output_kind is None and not verdict.output_kind_backfilled


def test_a_stale_map_result_declaration_refuses_in_words_not_a_dispatch_receipt() -> None:
    definition = _fan_out_unit()
    graph = compile_graph(definition, registry=_registry())
    with pytest.raises(ValueError, match="map_result"):
        declared_result(graph, definition, declared_output_kind="map_result")


def test_a_map_marked_as_the_result_is_refused_naming_why() -> None:
    definition = _fan_out_unit(primary_on_map=True)
    graph = compile_graph(definition, registry=_registry())
    with pytest.raises(ValueError, match="hands each item to another step"):
        declared_result(graph, definition, declared_output_kind="map_result")

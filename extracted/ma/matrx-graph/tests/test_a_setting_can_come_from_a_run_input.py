"""A step's SETTING can come from the run's inputs (``{"$input": name}`` in ``data.config``).

2026-10-27 (unit builders): ``data.batch``'s part size was fixed in the definition, so a unit
could not offer "part size" as an input. A scalar setting (size, count, flag, short text) may
now read a declared input; it is validated at compile with its stand-in and refused on a field
that shapes the graph.
"""

from __future__ import annotations

import pytest

from matrx_graph import CompilationError, Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.validation import validate_definition

from tests._fixtures import make_app_context


def _unit(size_ref: object) -> Definition:
    return Definition.model_validate(
        {
            "variables": [{"name": "part_size", "default": 2}],
            "nodes": [
                {
                    "id": "split",
                    "type": "data.batch",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"size": size_ref}, "input": {"items": [1, 2, 3, 4, 5, 6]}},
                }
            ],
            "edges": [],
        }
    )


async def _count(graph, registry, part_size: int) -> int:
    result = await Scheduler(
        graph, MemoryCheckpointer(), make_app_context(), registry=registry, surface_inputs={"part_size": part_size}
    ).run(run_id=f"t-size-{part_size}")
    assert result.status is RunStatus.COMPLETED, result.error
    return result.last_outputs["split"]["count"]


async def test_one_unit_runs_with_two_part_sizes() -> None:
    registry = register_builtin_nodes(NodeRegistry())
    graph = compile_graph(_unit({"$input": "part_size"}), registry=registry)
    assert await _count(graph, registry, 2) == 3
    assert await _count(graph, registry, 3) == 2


def test_a_setting_that_shapes_the_graph_cannot_come_from_an_input() -> None:
    registry = register_builtin_nodes(NodeRegistry())
    defn = _unit(2).model_dump(mode="json")
    defn["nodes"][0]["data"]["config"]["never_cross"] = {"$input": "part_size"}
    result = validate_definition(defn, registry=registry)
    assert not result.valid
    assert any("cannot come from a run input" in i.message for i in result.issues)
    with pytest.raises(CompilationError):
        compile_graph(Definition.model_validate(defn), registry=registry)


def test_a_setting_must_name_a_declared_input() -> None:
    registry = register_builtin_nodes(NodeRegistry())
    result = validate_definition(_unit({"$input": "nope"}).model_dump(mode="json"), registry=registry)
    assert any("'nope', which is not on this workflow's input surface" in i.message for i in result.issues)

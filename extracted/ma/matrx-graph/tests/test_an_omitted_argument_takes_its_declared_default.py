"""An argument the caller leaves out takes the workflow's declared default — on every door.

Live defect 2026-10-27: "Structure material into an outline" declares ``audience`` with
default ``"general"``. A caller ran it by name (``subgraph.call``) without ``audience``;
the child's entry step read ``inputs['audience']`` and the run died on
``KeyError: 'audience'``. Entry steps get the run's inputs as their payload, and the
declared defaults were never in it. The engine now fills them when the entry invocation
is resolved (the same resolution a fresh start, a called child and a resume/retry use).
"""

from __future__ import annotations

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.nodes import register_builtin_nodes

from tests._fixtures import make_app_context


def _child() -> Definition:
    return Definition.model_validate(
        {
            "variables": [
                {"name": "audience", "default": "general"},
                {"name": "max_sections", "default": 8},
            ],
            "nodes": [
                {
                    "id": "material",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {
                            "expression": "{'audience': inputs['audience'], 'max': inputs['max_sections'], 'n': len(inputs['chunks'])}"
                        }
                    },
                }
            ],
            "edges": [],
        }
    )


async def _run(inputs: dict, run_id: str, **kw):
    registry = register_builtin_nodes(NodeRegistry())
    graph = compile_graph(_child(), registry=registry)
    return await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry, **kw).run(
        run_id=run_id, inputs=inputs
    )


async def test_an_omitted_argument_takes_its_default() -> None:
    result = await _run({"chunks": [1, 2]}, "t-default-omitted")
    assert result.status is RunStatus.COMPLETED, result.error
    out = result.last_outputs["material"]
    assert out["audience"] == "general" and out["max"] == 8 and out["n"] == 2


async def test_a_value_the_caller_sent_wins() -> None:
    result = await _run({"chunks": [1], "audience": "nurses", "max_sections": 3}, "t-default-sent")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["material"]["audience"] == "nurses"
    assert result.last_outputs["material"]["max"] == 3


async def test_a_null_argument_takes_its_default() -> None:
    result = await _run({"chunks": [1], "audience": None}, "t-default-null")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["material"]["audience"] == "general"


async def test_a_closed_entry_step_is_never_handed_an_undeclared_default() -> None:
    registry = register_builtin_nodes(NodeRegistry())
    defn = Definition.model_validate(
        {
            "variables": [{"name": "audience", "default": "general"}],
            "nodes": [
                {
                    "id": "split",
                    "type": "data.batch",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"size": 2}, "input": {"items": [1, 2, 3]}},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry).run(
        run_id="t-default-closed"
    )
    assert result.status is RunStatus.COMPLETED, result.error

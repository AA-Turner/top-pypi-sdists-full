"""A step can keep its large output out of the run row (``NodeSpec.output_in_run_row=False``).

2026-10-05: the news monitor's 20 steps each output its ~2 MB run document; the run row's ``output``
(and the ``run_completed`` event) is every step's output merged, so one run wrote ~11 MB into one row
and its final write timed out, leaving the run "running". A step that declares
``output_in_run_row=False`` still hands its full output to the next step (and keeps it on its own
node_outcome row), while the run's ``last_outputs`` holds only a small marker naming where it is.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    ActionRegistry,
    ActionTier,
    Definition,
    MemoryCheckpointer,
    NodeCategory,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_node,
)
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import make_app_context

BIG = "x" * 200_000


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Doc(BaseModel):
    doc: str = ""


class _Size(BaseModel):
    received: int = 0


def _registry() -> NodeRegistry:
    nreg, areg = NodeRegistry(), ActionRegistry()

    @register_node(name="test.big_doc", category=NodeCategory.DATA, determinism=ActionTier.PURE,
                   input_schema=_In, output_schema=_Doc, output_in_run_row=False,
                   node_registry=nreg, action_registry=areg)
    async def _big(_ctx, inputs: _In) -> NodeResult[_Doc]:
        return success(_Doc(doc=BIG))

    @register_node(name="test.reads_doc", category=NodeCategory.DATA, determinism=ActionTier.PURE,
                   input_schema=_In, output_schema=_Size, node_registry=nreg, action_registry=areg)
    async def _reads(_ctx, inputs: _In) -> NodeResult[_Size]:
        return success(_Size(received=len(getattr(inputs, "doc", "") or "")))

    return nreg


async def test_a_large_step_output_reaches_the_next_step_but_not_the_run_row() -> None:
    nreg = _registry()
    definition = Definition.model_validate({
        "nodes": [
            {"id": "a", "type": "test.big_doc", "position": {"x": 0, "y": 0}, "data": {}},
            {"id": "b", "type": "test.reads_doc", "position": {"x": 100, "y": 0}, "data": {}},
        ],
        "edges": [{"id": "e", "source": "a", "target": "b", "data": {"kind": "data"}}],
    })
    scheduler = Scheduler(compile_graph(definition, registry=nreg), MemoryCheckpointer(), make_app_context(),
                          registry=nreg)
    result = await scheduler.run(run_id="run-large-step", inputs={})
    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["b"]["received"] == len(BIG), "the next step must still get the full output"
    marker = result.last_outputs["a"]
    assert marker.get("output_elided") is True and "__kind" not in marker and marker.get("node_id") == "a", marker
    assert len(str(result.last_outputs)) < 2_000

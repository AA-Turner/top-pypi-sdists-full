"""An input's default can point at a System Context item: ``{"$system_context": key}``.

2026-10-27 (Arman): the Agent Debrief workflow showed ``claude-opus-5-5`` as its model default — a
copy. The value lives once ("Preferred Frontier Large Model" in System Context) and every workflow
that names it follows a change. A supplied value still wins; a pointer that cannot be read fails
the run naming the item.
"""

from __future__ import annotations

import pytest

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.errors import UnresolvedInputError
from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.system_values import configure_system_context_reader

from tests._fixtures import make_app_context

POINTER = {"$system_context": "preferred_frontier_large_model"}


def _definition() -> Definition:
    return Definition.model_validate(
        {
            "variables": [{"name": "model", "default": POINTER, "type": "text"}],
            "nodes": [
                {
                    "id": "say",
                    "type": "text.template",
                    "position": {"x": 0, "y": 0},
                    "data": {"input": {"template": "model={{model}}", "variables": {"model": {"$input": "model"}}}},
                }
            ],
            "edges": [],
        }
    )


@pytest.fixture
def reads():
    seen: list[tuple[str, str | None]] = []

    async def reader(key: str, organization_id: str | None):
        seen.append((key, organization_id))
        return "model-from-system-context" if key == "preferred_frontier_large_model" else None

    configure_system_context_reader(reader)
    yield seen
    configure_system_context_reader(None)


async def _run(surface_inputs: dict) -> str:
    registry = register_builtin_nodes(NodeRegistry())
    graph = compile_graph(_definition(), registry=registry)
    result = await Scheduler(
        graph, MemoryCheckpointer(), make_app_context(), registry=registry, surface_inputs=surface_inputs
    ).run(run_id="t-system-context")
    assert result.status is RunStatus.COMPLETED, result.error
    return str(result.last_outputs["say"])


async def test_the_default_reads_the_item_for_the_runs_organization(reads) -> None:
    out = await _run({"model": POINTER})  # the start seam lands the declared default as-is
    assert "model=model-from-system-context" in out
    assert reads and reads[0][0] == "preferred_frontier_large_model"


async def test_a_default_nobody_landed_still_reads_the_item(reads) -> None:
    assert "model=model-from-system-context" in await _run({})


async def test_a_supplied_value_wins_and_reads_nothing(reads) -> None:
    assert "model=claude-sonnet-5-5" in await _run({"model": "claude-sonnet-5-5"})
    assert reads == []


async def test_an_unreadable_item_fails_naming_it() -> None:
    async def reader(_key: str, _org: str | None):
        return None

    configure_system_context_reader(reader)
    try:
        with pytest.raises(UnresolvedInputError, match="preferred_frontier_large_model"):
            await _run({"model": POINTER})
    finally:
        configure_system_context_reader(None)

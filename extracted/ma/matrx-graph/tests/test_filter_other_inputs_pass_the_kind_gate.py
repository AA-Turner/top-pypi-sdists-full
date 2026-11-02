"""data.filter's other inputs (``$in``) reach the predicate at run time.

The step declares input kind ``items`` (a closed contract: ``items`` / ``archetype`` / ``count``), and its
documented ``$in`` namespace is every OTHER value delivered beside the list. Save and dry run accepted those values,
but the run-time kind gate checked the whole payload against ``items`` and refused them ("Additional properties are
not allowed") — first seen on the brand topical map's place gate. A step whose input model allows extra values is
kind-checked on its declared fields; the extras are its free namespace. The declared fields are still checked.
"""

from __future__ import annotations

import time

import pytest

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph import kinds as kinds_mod
from matrx_graph import register_builtin_nodes
from matrx_graph.kinds import KindEntry, configure_canonical_kind_organization, invalidate_kind_catalog_cache
from tests._fixtures import FakeEmitter, make_app_context

ITEMS_SCHEMA = {
    "type": "object",
    "properties": {
        "__kind": {"const": "items"},
        "archetype": {"const": "items"},
        "items": {"type": "array"},
        "count": {"type": "integer"},
    },
    "required": ["items"],
    "additionalProperties": False,
}


def _seed(slug: str, schema: dict) -> None:
    kinds_mod._cache[slug] = (time.monotonic(), KindEntry(slug=slug, version=1, label=slug, json_schema=schema))


@pytest.fixture(autouse=True)
def _kinds():
    configure_canonical_kind_organization(None)
    invalidate_kind_catalog_cache()
    _seed("items", ITEMS_SCHEMA)
    _seed("filter_result", {})
    yield
    configure_canonical_kind_organization(None)
    invalidate_kind_catalog_cache()


async def _run(node_input: dict, predicate: str, run_id: str):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    definition = Definition.model_validate({
        "nodes": [{
            "id": "f",
            "type": "data.filter",
            "position": {"x": 0, "y": 0},
            "data": {"config": {"predicate": predicate}, "input": node_input},
        }],
        "edges": [],
    })
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()
    result = await Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry).run(run_id=run_id)
    return result, checkpointer


async def test_other_inputs_beside_the_list_pass_the_kind_gate():
    result, _ = await _run(
        {"items": [{"slug": "roofing"}, {"slug": "harbor-city"}], "places": ["harbor-city"], "policy": "refuse"},
        "inputs['$in']['policy'] == 'allow' or inputs['slug'] not in inputs['$in']['places']",
        "filter-in-gate",
    )
    assert result.status is RunStatus.COMPLETED, getattr(result, "error", None)


async def test_the_declared_list_is_still_checked_against_the_kind():
    result, _ = await _run(
        {"items": "not a list", "places": ["harbor-city"]},
        "inputs['slug'] not in inputs['$in']['places']",
        "filter-in-gate-bad",
    )
    assert result.status is not RunStatus.COMPLETED

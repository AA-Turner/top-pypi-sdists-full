"""``data.filter`` over a flat tree keeps the children of a dropped node (2026-10-27).

The break this catches: a flat tree (each node names its parent) loses whole
branches when a filter drops one node — its children still point at a parent
that is gone, so a save either refuses them or files them nowhere. With
``id_key`` / ``parent_key`` set, a kept node whose parent was dropped is moved to
its nearest kept ancestor (or to the top when none is left). Users: a topical map
dropping place-named topics, a mind map dropping off-topic branches, an offering
tree dropping retired services, a content plan dropping pages nobody wants.
"""

from __future__ import annotations

import pytest
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)

from tests._fixtures import make_app_context

TREE = [
    {"slug": "roofing", "name": "Roofing"},
    {"slug": "california", "name": "California", "parent_slug": "roofing"},
    {"slug": "los-angeles", "name": "Los Angeles", "parent_slug": "california"},
    {"slug": "tile-roofs", "name": "Tile roofs", "parent_slug": "los-angeles"},
    {"slug": "metal-roofs", "name": "Metal roofs", "parent_slug": "california"},
    {"slug": "nevada", "name": "Nevada"},
    {"slug": "solar", "name": "Solar panels", "parent_slug": "nevada"},
    {"slug": "gutters", "name": "Gutters", "parent_slug": "roofing"},
]
PLACES = ["california", "los-angeles", "nevada"]


async def _run(config: dict, items: list) -> dict:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    inputs = {"items": items, "places": PLACES}
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "no_places",
                    "type": "data.filter",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": config, "inputs": inputs},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-filter-tree", inputs=inputs)
    assert result.status is RunStatus.COMPLETED, result
    return result.last_outputs["no_places"]


PREDICATE = "inputs['slug'] not in inputs['$in']['places']"


@pytest.mark.asyncio
async def test_children_move_to_the_nearest_kept_ancestor() -> None:
    out = await _run({"predicate": PREDICATE, "id_key": "slug", "parent_key": "parent_slug"}, TREE)
    parents = {n["slug"]: n.get("parent_slug") for n in out["items"]}
    assert parents == {
        "roofing": None,
        "tile-roofs": "roofing",  # two dropped levels up
        "metal-roofs": "roofing",
        "solar": None,  # its only ancestor was dropped: top level
        "gutters": "roofing",  # untouched
    }
    assert "parent_slug" not in next(n for n in out["items"] if n["slug"] == "solar")
    assert (out["kept"], out["dropped"]) == (5, 3)


@pytest.mark.asyncio
async def test_without_the_tree_keys_nothing_is_moved() -> None:
    out = await _run({"predicate": PREDICATE}, TREE)
    parents = {n["slug"]: n.get("parent_slug") for n in out["items"]}
    assert parents["tile-roofs"] == "los-angeles"


@pytest.mark.asyncio
async def test_a_node_whose_parent_is_unknown_is_left_alone() -> None:
    items = [{"slug": "a", "parent_slug": "outside-this-list"}, {"slug": "california"}]
    out = await _run({"predicate": PREDICATE, "id_key": "slug", "parent_key": "parent_slug"}, items)
    assert out["items"] == [{"slug": "a", "parent_slug": "outside-this-list"}]


def test_one_tree_key_without_the_other_is_refused() -> None:
    from pydantic import ValidationError

    from matrx_graph.nodes.data.filter import FilterConfig

    with pytest.raises(ValidationError, match="together"):
        FilterConfig(predicate="True", id_key="slug")

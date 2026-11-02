"""Check Items takes an empty list: zero items checked, the step passes, nothing refused.

Reported 2026-10-28 (Smart Add offerings units) as "Check Items refuses an empty list". The live
refusal (run 38481386, step check_claims) was NOT an empty list: the connection mapped
``items <- structured_output.claims`` off a Run Typed Agent whose answer IS the kind, so ``items``
arrived ABSENT ("Field required"). That class is now refused at save and at the edge
(test_a_mapping_off_a_declared_kind_is_checked_against_it). This file pins the other half: a
real empty list, through the step's declared ``items`` input kind (the live registered schema).
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.db import _registry
from matrx_graph.kinds import invalidate_kind_catalog_cache
from matrx_graph.nodes import register_builtin_nodes

from tests._fixtures import make_app_context

#: content_ir.kind_definition 'items', as registered live (2026-10-28).
_ITEMS = {
    "type": "object",
    "$defs": {"JsonValue": {}},
    "required": ["items"],
    "additionalProperties": False,
    "properties": {
        "count": {"type": "integer", "default": -1},
        "items": {"type": "array", "items": {"$ref": "#/$defs/JsonValue"}},
        "__kind": {"type": "string", "const": "items", "default": "items"},
        "archetype": {"type": "string", "const": "items", "default": "items"},
    },
}


class _Row:
    def __init__(self, slug: str, schema: dict) -> None:
        self.id, self.kind, self.version, self.label = f"id-{slug}", slug, 1, slug
        self.is_active, self.emitted_json_schema = True, schema
        self.deleted_at, self.published_to_web = None, True


class _Catalog:
    def __init__(self, rows: dict[str, _Row]) -> None:
        self._rows = rows

    async def load_items(self, **filters: Any) -> list[_Row]:
        row = self._rows.get(filters.get("kind") or "")
        return [row] if row is not None else []


@pytest.fixture(autouse=True)
def _catalog():
    invalidate_kind_catalog_cache()
    previous = dict(_registry._instances)
    _registry.configure_db(
        instances={"kind_definition_manager": _Catalog({
                       "items": _Row("items", _ITEMS),
                       # The step's own output kind; its shape is not what this file pins.
                       "checked_items_result": _Row("checked_items_result", {"type": "object"}),
                   }),
                   "kind_edge_manager": _Catalog({})}
    )
    yield
    _registry._instances.clear()
    _registry._instances.update(previous)
    invalidate_kind_catalog_cache()


async def test_an_empty_list_is_zero_items_checked_and_the_step_passes() -> None:
    defn = Definition.model_validate({
        "nodes": [
            {"id": "answer", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"config": {"expression": "{'claims': [], 'text': 'We make 40 candles'}"}}},
            {"id": "check", "type": "data.check_items", "position": {"x": 0, "y": 0},
             "data": {"config": {"checks": [
                 {"key": "no quote", "path": "quote", "type": "required"},
                 {"key": "not verbatim", "path": "quote", "type": "verbatim", "source": "text"},
             ]}}},
        ],
        "edges": [{"id": "e", "source": "answer", "target": "check",
                   "data": {"kind": "data", "mappings": {"items": "claims", "text": "text"}}}],
    })
    registry = register_builtin_nodes(NodeRegistry())
    graph = compile_graph(defn, registry=registry)
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry).run(run_id="ci-empty")
    assert result.status is RunStatus.COMPLETED, result.error
    out = result.last_outputs["check"]
    assert (out["items"], out["kept"], out["dropped"], out["total"], out["passed"]) == ([], 0, 0, 0, True), out

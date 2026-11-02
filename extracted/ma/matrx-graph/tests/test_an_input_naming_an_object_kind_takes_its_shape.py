"""An input that names an OBJECT kind (or a list of them) takes the kind's shape — gap 8.

Live defect 2026-10-29 (Smart Add Brand units): an ``io.user_input`` field and a declared variable
naming ``company_candidate`` compiled to ``{"type": "string"}``, so every run refused the real value
("{} is not of type 'string'", "candidates.0 … is not of type 'string'"). The field's contract now
comes from the kind (a list of it when ``multiple``), the run judges the landed value against the
kind (resolved then, so a cold kind cache at compile never decides), and a kind that is really a
plain value (``text``, registered as ``{text: …}``) stays a string.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
    warm_input_kinds,
)
from matrx_graph.db import _registry
from matrx_graph.executor.schema_validation import validate_instance
from matrx_graph.kinds import invalidate_kind_catalog_cache
from matrx_graph.types.input_surface import KIND_SCHEMA_UNRESOLVED

from tests._fixtures import FakeEmitter, make_app_context

_CANDIDATE = {
    "type": "object",
    "title": "CompanyCandidate",
    "required": ["name", "__kind"],
    "properties": {
        "__kind": {"type": "string", "const": "company_candidate"},
        "name": {"type": "string"},
        "domain": {"type": "string"},
        "where": {"$ref": "#/$defs/Place"},
    },
    "$defs": {"Place": {"type": "object", "properties": {"city": {"type": "string"}}}},
}
# The live `text` kind: a wrapper object, yet a text input's value is a string.
_TEXT = {
    "type": "object",
    "required": ["text"],
    "properties": {"text": {"type": "string"}, "__kind": {"type": "string", "const": "text"}},
}
_MARKDOWN = {"type": "object", "properties": {"markdown": {"type": "string"}, "__kind": {"type": "string"}}}
# A map kind (``key_value_map``): no field of its own, a typed value per name.
_MAP = {
    "type": "object",
    "properties": {"__kind": {"type": "string", "const": "key_value_map"}},
    "additionalProperties": {"anyOf": [{"type": "string"}, {"type": "integer"}, {"type": "null"}]},
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
    rows = {s: _Row(s, schema) for s, schema in
            (("company_candidate", _CANDIDATE), ("text", _TEXT), ("markdown", _MARKDOWN),
             ("user_inputs", {"type": "object"}), ("key_value_map", _MAP))}
    _registry.configure_db(
        instances={"kind_definition_manager": _Catalog(rows), "kind_edge_manager": _Catalog({})}
    )
    yield
    _registry._instances.clear()
    _registry._instances.update(previous)
    invalidate_kind_catalog_cache()


def _definition() -> dict[str, Any]:
    return {
        "nodes": [
            {"id": "ask", "type": "io.user_input", "position": {"x": 0, "y": 0}, "data": {"config": {"fields": [
                {"key": "pick", "label": "Company", "kind": "company_candidate"},
                {"key": "candidates", "label": "Candidates", "kind": "company_candidate", "multiple": True},
                {"key": "note", "label": "Note", "kind": "text"},
                {"key": "summary", "label": "Summary", "kind": "markdown"},
            ]}}},
            {"id": "use", "type": "data.transform", "position": {"x": 300, "y": 0},
             "data": {"config": {"expression": "{'pick': inputs['pick'], 'candidates': inputs['candidates'], "
                                               "'note': inputs['note']}"}}},
        ],
        "edges": [{"id": "e1", "source": "ask", "target": "use", "data": {"kind": "data", "mappings": {
            "pick": "pick", "candidates": "candidates", "note": "note"}}}],
        "variables": [{"name": "shortlist", "kind": "company_candidate", "multiple": True}],
    }


def _registry_nodes() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return registry


async def _run(values: dict[str, Any]) -> Any:
    registry = _registry_nodes()
    # COLD kind cache at compile: the run must judge against the kind anyway.
    invalidate_kind_catalog_cache()
    graph = compile_graph(Definition.model_validate(_definition()), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry, surface_inputs=values
    )
    return await scheduler.run(run_id="kind-inputs")


_GOOD = {
    "pick": {"name": "Acme", "domain": "acme.example", "where": {"city": "Irvine"}},
    "candidates": [{"name": "Acme"}, {"name": "Beta Co", "domain": "beta.example"}],
    "note": "first pass",
    "shortlist": [{"name": "Acme"}],
}


async def test_a_warmed_compile_serves_the_kinds_shape_and_a_list_of_it() -> None:
    definition = Definition.model_validate(_definition())
    await warm_input_kinds(definition)
    graph = compile_graph(definition, registry=_registry_nodes())
    surface = graph.input_surface
    # Each fragment is its own schema resource: the kind's #/$defs refs resolve inside the
    # step's whole output schema too.
    whole = graph.nodes["ask"].effective_output_schema
    assert validate_instance(whole, {"pick": {"name": "A", "where": {"city": "Irvine"}}}) == []
    assert validate_instance(whole, {"pick": {"name": "A", "where": {"city": 5}}}) == [
        "pick.where.city: 5 is not of type 'string'"
    ]
    pick, candidates = surface["pick"].json_schema, surface["candidates"].json_schema
    assert pick["type"] == "object" and pick["required"] == ["name"] and "ui:widget" not in pick
    assert pick["title"] == "Company" and pick["$defs"]["Place"]["type"] == "object"
    assert candidates["type"] == "array" and candidates["items"]["properties"]["name"] == {"type": "string"}
    assert "$defs" in candidates and "$defs" not in candidates["items"]
    shortlist = surface["shortlist"].json_schema
    assert shortlist["type"] == "array" and shortlist["items"]["type"] == "object"
    # A kind that is really a plain value never becomes an object.
    assert surface["note"].json_schema["type"] == "string"
    assert surface["summary"].json_schema["type"] == "string"
    assert not any(KIND_SCHEMA_UNRESOLVED in s.json_schema for s in surface.values())


def test_a_cold_compile_keeps_the_plain_type_and_flags_it() -> None:
    invalidate_kind_catalog_cache()
    surface = compile_graph(Definition.model_validate(_definition()), registry=_registry_nodes()).input_surface
    assert surface["pick"].json_schema["type"] == "string"
    assert surface["pick"].json_schema[KIND_SCHEMA_UNRESOLVED] == "company_candidate"
    assert surface["shortlist"].json_schema[KIND_SCHEMA_UNRESOLVED] == "company_candidate"
    assert KIND_SCHEMA_UNRESOLVED not in surface["note"].json_schema


async def test_an_object_and_a_list_of_objects_are_accepted_through_the_real_scheduler() -> None:
    result = await _run(_GOOD)
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["use"] == {
        "pick": _GOOD["pick"], "candidates": _GOOD["candidates"], "note": "first pass",
    }


async def test_a_wrong_shaped_field_is_refused_naming_the_field_item_and_kind() -> None:
    result = await _run({**_GOOD, "pick": "Acme", "candidates": [{"name": "Acme"}, {"domain": "x"}]})
    assert result.status is not RunStatus.COMPLETED
    error = str(result.error)
    assert "pick: should be one 'company_candidate' value (an object), got text" in error
    assert "candidates[1]: 'name' is a required property (kind 'company_candidate')" in error
    assert "is not of type 'string'" not in error
    nested = await _run({**_GOOD, "pick": {"name": "Acme", "where": {"city": 5}}})
    assert nested.status is not RunStatus.COMPLETED
    error = str(nested.error)
    assert "pick.where.city: 5 is not of type 'string' (kind 'company_candidate')" in error
    assert "{} is not of type 'string'" not in error


async def test_a_text_kind_stays_text_and_refuses_an_object() -> None:
    result = await _run({**_GOOD, "note": {"text": "first pass"}})
    assert result.status is not RunStatus.COMPLETED
    assert "note: {'text': 'first pass'} is not of type 'string'" in str(result.error)


async def test_a_wrong_shaped_variable_parks_the_run_asking_again_with_the_problem() -> None:
    result = await _run({**_GOOD, "shortlist": {"name": "Acme"}})
    assert result.status is RunStatus.AWAITING_INPUT
    (entry,) = result.interrupt["missing"]
    assert entry["name"] == "shortlist"
    assert entry["problems"] == ["shortlist: should be a list of 'company_candidate' values, got dict"]


async def test_a_map_kind_takes_an_object_and_an_object_with_no_shape_stays_plain() -> None:
    """``keep_caps`` / a lookup table: a map kind declares no field, only a typed value per name.
    It used to compile to a string (no field = "no shape"), so every caller's map was refused."""
    definition = Definition.model_validate({
        "nodes": [{"id": "ask", "type": "io.user_input", "position": {"x": 0, "y": 0}, "data": {"config": {
            "fields": [{"key": "caps", "label": "Caps", "kind": "key_value_map"},
                       {"key": "free", "label": "Free", "kind": "user_inputs"}]}}}],
        "edges": [],
    })
    await warm_input_kinds(definition)
    surface = compile_graph(definition, registry=_registry_nodes()).input_surface
    caps = surface["caps"].json_schema
    assert caps["type"] == "object" and caps["title"] == "Caps"
    assert validate_instance(caps, {"news": 4, "label": "Manta"}) == []
    assert validate_instance(caps, {"news": [4]}) != []
    assert surface["free"].json_schema["type"] == "string"

"""A field the step's own input model declares, and its input kind does not, is the step's own setting.

Live 2026-11-10 (release v0.2.2099, L9g after_release): every budgeted research recipe errored at
Split into Batches with "The values for 'fit1' don't match the 'items' kind it declares: (value):
Additional properties are not allowed ('size' was unexpected)". ``data.batch`` declares
``input_kind="items"`` (a closed kind) and a ``size`` input beside the list; the scheduler's input
gate checked the step's WHOLE inputs against the kind. The rule now: the gate checks only the fields
the kind has; another field the node spec declares is left out (its own input model still checks it).

The offline blind spot that hid it: with no kind catalog the gate runs degraded and passes. These
tests load the REAL registered schemas from ``fixtures/input_kind_schemas_live.json`` (read from the
live database) and assert the gate really checked, so a degraded pass cannot hide this class again.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.db import _registry
from matrx_graph.executor.scheduler import _kind_contract_inputs
from matrx_graph.kinds import check_against_kind, invalidate_kind_catalog_cache
from matrx_graph.nodes import register_builtin_nodes

from tests._fixtures import make_app_context

_LIVE = json.loads((Path(__file__).parent / "fixtures" / "input_kind_schemas_live.json").read_text())["schemas"]


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
    rows = {slug: _Row(slug, schema) for slug, schema in _LIVE.items()}
    # The step's own output kind; its shape is not what this file pins.
    rows["batched_list_result"] = _Row("batched_list_result", {"type": "object"})
    _registry.configure_db(instances={"kind_definition_manager": _Catalog(rows), "kind_edge_manager": _Catalog({})})
    yield
    _registry._instances.clear()
    _registry._instances.update(previous)
    invalidate_kind_catalog_cache()


def _registry_specs():
    registry = register_builtin_nodes(NodeRegistry())
    specs = registry.all_specs()
    return list(specs.values() if isinstance(specs, dict) else specs)


async def test_the_gate_really_checks_offline_never_a_degraded_pass() -> None:
    for slug, schema in _LIVE.items():
        check = await check_against_kind({"__kind": slug}, slug)
        assert check.checked, (slug, check.degraded_reason)
        assert schema.get("additionalProperties") is False, slug


def test_every_builtin_input_kind_is_in_the_snapshot() -> None:
    missing = sorted({s.input_kind for s in _registry_specs() if s.input_kind and s.input_kind not in _LIVE})
    assert not missing, f"snapshot the live schema of {missing} into fixtures/input_kind_schemas_live.json"


def test_every_step_leaves_out_its_own_declared_fields_and_keeps_the_kinds() -> None:
    checked = 0
    for spec in _registry_specs():
        if not spec.input_kind or spec.input_schema is None:
            continue
        schema = _LIVE[spec.input_kind]
        kind_fields = set(schema["properties"])
        names = {info.alias or name for name, info in spec.input_schema.model_fields.items()}
        inputs = {name: object() for name in names if name != "__kind"}
        gated = _kind_contract_inputs(spec, inputs, schema)
        assert set(gated) == {n for n in inputs if n in kind_fields}, (spec.node_type, sorted(gated))
        checked += 1
    assert checked >= 20


def test_an_unknown_kind_schema_leaves_the_inputs_as_before() -> None:
    spec = next(s for s in _registry_specs() if s.node_type == "data.batch")
    assert _kind_contract_inputs(spec, {"items": [1], "size": 2}, None) == {"items": [1], "size": 2}


def _batch_run(expression: str, mappings: dict[str, str]) -> Any:
    defn = Definition.model_validate({
        "nodes": [
            {"id": "src", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"config": {"expression": expression}}},
            {"id": "fit", "type": "data.batch", "position": {"x": 0, "y": 0},
             "data": {"config": {"size": 1}}},
        ],
        "edges": [{"id": "e", "source": "src", "target": "fit",
                   "data": {"kind": "data", "mappings": mappings}}],
    })
    registry = register_builtin_nodes(NodeRegistry())
    graph = compile_graph(defn, registry=registry)
    return Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry).run(run_id="ci-batch-size")


async def test_split_into_batches_takes_its_size_input_through_the_real_items_kind() -> None:
    result = await _batch_run("{'rows': [1, 2, 3, 4, 5], 'budget': 2}", {"items": "rows", "size": "budget"})
    assert result.status is RunStatus.COMPLETED, result.error
    assert [len(b) for b in result.last_outputs["fit"]["batches"]] == [2, 2, 1], result.last_outputs["fit"]


async def test_a_wrong_kind_field_is_still_refused_by_the_kind() -> None:
    result = await _batch_run("{'rows': 'not a list', 'budget': 2}", {"items": "rows", "size": "budget"})
    assert result.status is not RunStatus.COMPLETED
    assert "items" in (result.error or ""), result.error

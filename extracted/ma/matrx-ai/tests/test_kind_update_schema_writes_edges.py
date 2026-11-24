"""kind_update_schema writes the kind_edge rows its new schema implies (person_basics.facts, 2026-11-17).

A schema update that adds an array/object field whose shape is another registered kind must write
that field's edge in the same call; a dropped field retires its edge; a missing child is reported,
not invented. Fake registry; the live lifecycle is ``tests_trials/run_kind_tools_e2e.py``."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai.tools.implementations.kind_shared import child_kind_fields_of_schema
from matrx_ai.tools.models import ToolContext

ORG = str(uuid4())

CHILD_DEF = {
    "type": "object",
    "properties": {"__kind": {"type": "string", "const": "fact_item"}, "value": {"type": "string"}},
}


def _schema(**props: Any) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {"name": {"type": "string"}, **props},
        "$defs": {"fact_item": CHILD_DEF},
    }


FACTS = {"type": "array", "items": {"$ref": "#/$defs/fact_item"}}


def test_the_schema_walker_finds_ref_and_inline_children() -> None:
    inline = {"type": "object", "properties": {"__kind": {"const": "note_item"}}}
    got = child_kind_fields_of_schema(
        _schema(facts=FACTS, note=inline, tags={"type": "array", "items": {"type": "string"}}), "root"
    )
    assert got == {"facts": ("fact_item", True), "note": ("note_item", False)}


class Rows:
    def __init__(self) -> None:
        parent = SimpleNamespace(id=uuid4(), kind="root", version=1, deleted_at=None,
                                 organization_id=ORG, metadata={}, emitted_json_schema={})
        self.child = SimpleNamespace(id=uuid4(), kind="fact_item", deleted_at=None)
        self.defs = [parent, self.child]
        self.parent = parent
        self.edges: list[Any] = []


@pytest.fixture
def rows(monkeypatch: pytest.MonkeyPatch) -> Rows:
    from matrx_ai.tools.implementations import kind_authoring as ka

    r = Rows()

    class Q:
        def __init__(self, items: list[Any]) -> None:
            self.items = items

        async def all(self) -> list[Any]:
            return list(self.items)

    class KindDefinition:
        @classmethod
        def filter(cls, **kw: Any) -> Q:
            return Q([d for d in r.defs if all(getattr(d, k, None) == v for k, v in kw.items())])

        @classmethod
        async def get_or_none(cls, **kw: Any) -> Any:
            return SimpleNamespace(version=2)

    class KindExample:
        @classmethod
        def filter(cls, **kw: Any) -> Q:
            return Q([])

    class KindEdge:
        @classmethod
        def filter(cls, **kw: Any) -> Q:
            return Q([e for e in r.edges if str(e.parent_definition_id) == str(kw["parent_definition_id"])])

        @classmethod
        async def create_item(cls, **p: Any) -> Any:
            e = SimpleNamespace(id=uuid4(), deleted_at=None, **p)
            r.edges.append(e)
            return e

    models = {"KindDefinition": KindDefinition, "KindExample": KindExample, "KindEdge": KindEdge}

    async def resolve(_ref: str, _ctx: Any) -> Any:
        return r.parent, None

    async def allowed(_kd: Any, _ctx: Any) -> None:
        return None

    async def write(model: Any, row_id: str, _ctx: Any, **values: Any) -> None:
        for e in r.edges:
            if str(e.id) == row_id:
                for k, v in values.items():
                    setattr(e, k, v)

    async def no_dup(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(ka, "get_db_model", lambda key: models[key])
    monkeypatch.setattr(ka, "resolve_kind", resolve)
    monkeypatch.setattr(ka, "ensure_can_edit_kind", allowed)
    monkeypatch.setattr(ka, "update_as_the_person", write)
    monkeypatch.setattr(ka, "_duplicate_shape_refusal", no_dup)
    monkeypatch.setattr(ka, "ctx_user_id", lambda _c: str(uuid4()))
    monkeypatch.setattr(ka, "attach_surface_write", lambda res, **_k: res, raising=False)
    import matrx_ai.tools.surface_write as sw

    monkeypatch.setattr(sw, "attach_surface_write", lambda res, **_k: res)
    return r


async def _update(schema: dict[str, Any]) -> Any:
    from matrx_ai.tools.implementations.kind_authoring import kind_update_schema

    return await kind_update_schema(
        {"kind": "root", "json_schema": schema}, ToolContext(call_id="c", tool_name="kind_update_schema")
    )


def _live(r: Rows) -> dict[str, str]:
    return {e.field_name: str(e.child_definition_id) for e in r.edges if e.deleted_at is None}


@pytest.mark.asyncio
async def test_adding_an_array_field_of_a_registered_kind_writes_its_edge(rows: Rows) -> None:
    res = await _update(_schema(facts=FACTS))
    assert res.success, res
    assert _live(rows) == {"facts": str(rows.child.id)}


@pytest.mark.asyncio
async def test_dropping_the_field_retires_its_edge_and_a_markerless_edit_keeps_it(rows: Rows) -> None:
    await _update(_schema(facts=FACTS))
    await _update(_schema(facts={"type": "array", "items": {"type": "object"}}))
    assert "facts" in _live(rows)  # no markers sent: composition is not unwired
    await _update(_schema())
    assert _live(rows) == {}


@pytest.mark.asyncio
async def test_a_child_kind_that_is_not_registered_is_reported_not_invented(rows: Rows) -> None:
    rows.defs.remove(rows.child)
    res = await _update(_schema(facts=FACTS))
    assert res.success and _live(rows) == {}
    assert "fact_item" in (res.output.warning or "")

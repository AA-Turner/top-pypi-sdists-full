"""A NEW DATABASE COMPONENT NEVER SILENTLY TAKES THE DEFAULT FROM ANOTHER.

2026-11-03: the release shift's agent created `quiz_view` for `quiz_set` with the default `is_default=true`,
and `kindcomp_create_component` quietly demoted the compiled `quiz` (which saves every answer). Nothing in the
result said so; `quiz_view` then lost every answer on www and the iPhone.

The rule:
- a BUILT-IN default (compiled into the app, `source != 'db'`) stays the default; the new row is saved beside it
  and the result says so, naming the explicit door (kindcomp_update_settings is_default=true);
- a replaced DATABASE default is named in the result;
- the generic fallback is not a component and is replaced freely (the fallback law);
- kindcomp_update_settings is_default=true is the explicit door: it demotes the incumbent and names it.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai.tools.models import ToolContext

SOURCE = "export default function C({ data }) { return <p>{data.title}</p>; }"


def _row(**kw: Any) -> SimpleNamespace:
    base = {"id": uuid4(), "deleted_at": None, "is_default": True, "platform": "web", "role": "output"}
    return SimpleNamespace(**{**base, **kw})


def _install(monkeypatch: pytest.MonkeyPatch, incumbents: list[SimpleNamespace]) -> tuple[SimpleNamespace, list, list]:
    from matrx_ai.tools.implementations import kind_component

    kind = SimpleNamespace(id=uuid4(), kind="quiz_set", organization_id=uuid4())
    updates: list[tuple[dict[str, Any], dict[str, Any]]] = []
    created: list[dict[str, Any]] = []

    class Query:
        def __init__(self, filters: dict[str, Any]) -> None:
            self.filters = filters

        async def all(self) -> list[SimpleNamespace]:
            return list(incumbents) if self.filters.get("is_default") is True else []

    class FakeKindComponent:
        @classmethod
        def filter(cls, **filters: Any) -> Query:
            return Query(filters)

        @classmethod
        async def update_where(cls, filters: dict[str, Any], **values: Any) -> list[Any]:
            updates.append((filters, values))
            return [1]

        @classmethod
        async def create_item(cls, **payload: Any) -> SimpleNamespace:
            created.append(payload)
            return SimpleNamespace(id=uuid4(), semver="1.0.0")

        @classmethod
        async def get_or_none(cls, **_kw: Any) -> SimpleNamespace:
            return _row(is_default=True, source="db", component_key="mine", kind_definition_id=kind.id)

    async def fake_resolve(_ref: str, _ctx: ToolContext):
        return kind, None

    async def allow(*_a: Any, **_k: Any):
        return None

    async def fake_source(_source: str):
        return None, True

    monkeypatch.setattr(kind_component, "resolve_kind", fake_resolve)
    monkeypatch.setattr(kind_component, "ensure_can_edit_kind", allow)
    monkeypatch.setattr(kind_component, "_refuse_broken_source", fake_source)
    monkeypatch.setattr(kind_component, "get_db_model", lambda _name: FakeKindComponent)
    monkeypatch.setattr(kind_component, "ctx_user_id", lambda _ctx: "user-1")
    return kind, updates, created


async def _create(**extra: Any):
    from matrx_ai.tools.implementations import kind_component

    return await kind_component.kindcomp_create_component(
        {"kind": "quiz_set", "component_key": "quiz_view", "component_source": SOURCE, **extra},
        ToolContext(call_id=str(uuid4()), tool_name="test"),
    )


@pytest.mark.asyncio
async def test_a_built_in_default_stays_the_default_and_the_result_says_so(monkeypatch: pytest.MonkeyPatch) -> None:
    built_in = _row(source="bundled", component_key="quiz")
    _kind, updates, created = _install(monkeypatch, [built_in])

    result = await _create()

    assert result.success is True
    assert updates == [], "the built-in default was demoted"
    assert created[0]["is_default"] is False
    said = " ".join(result.model_notices) + " " + (result.output.message or "")
    assert "'quiz'" in said and "stays the default" in said
    assert "kindcomp_update_settings" in said and "is_default=true" in said
    assert "(not the default)" in result.output.message


@pytest.mark.asyncio
async def test_a_replaced_database_default_is_named(monkeypatch: pytest.MonkeyPatch) -> None:
    old = _row(source="db", component_key="quiz_card")
    _kind, updates, created = _install(monkeypatch, [old])

    result = await _create()

    assert result.success is True
    assert created[0]["is_default"] is True
    assert len(updates) == 1 and updates[0][1]["is_default"] is False
    said = " ".join(result.model_notices)
    assert "'quiz_card'" in said and str(old.id) in said


@pytest.mark.asyncio
async def test_the_generic_fallback_never_holds_the_default_against_a_real_component(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fallback = _row(source="bundled", component_key="generic_structured")
    _kind, updates, created = _install(monkeypatch, [fallback])

    result = await _create()

    assert result.success is True
    assert created[0]["is_default"] is True
    assert len(updates) == 1


@pytest.mark.asyncio
async def test_update_settings_is_the_explicit_door_and_names_what_it_demotes(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.tools.implementations import kind_component

    kind_id = uuid4()
    built_in = _row(source="bundled", component_key="quiz", kind_definition_id=kind_id)
    mine = _row(source="db", component_key="quiz_view", is_default=False, kind_definition_id=kind_id)
    _kind, updates, _created = _install(monkeypatch, [built_in])

    async def load(_cid: str, _ctx: ToolContext):
        return mine, SimpleNamespace(kind="quiz_set"), None

    monkeypatch.setattr(kind_component, "_load_editable_component", load)

    result = await kind_component.kindcomp_update_settings(
        {"component_id": str(mine.id), "settings": {"is_default": True}},
        ToolContext(call_id=str(uuid4()), tool_name="test"),
    )

    assert result.success is True, result.error
    assert updates[0] == ({"id": str(built_in.id)}, {"is_default": False, "updated_by": "user-1"})
    assert updates[1][0] == {"id": str(mine.id)}
    assert any("'quiz'" in n and "built-in" in n for n in result.model_notices)

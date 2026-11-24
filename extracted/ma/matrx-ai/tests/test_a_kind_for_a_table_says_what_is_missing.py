"""A kind made for a table's rows is ONE step with three parts: the kind, its component, and the
table showing its rows as it. kind_create / kind_get say which parts are still missing and name
the next call — read from the database, never refused (Law 6).

2026-11-03: Company Setup made ``grooming_appointment_card`` for a grooming business and never bound
the "Grooming Appointments" table to it, so the records drew as the plain table card and nothing
told the agent. Fake registry + fake host table reader; the reader itself is matrx-records'
``tables_with_kinds`` (registered by aidream as ``kind_tables_with_kinds``).
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest
import test_kind_create_one_call as one_call
from test_kind_create_one_call import FakeRegistry, _Query, create, make_ctx

from matrx_ai import _ext
from matrx_ai.tools.implementations.kind_completeness import KIND_TABLES_EXT_KEY, looks_like_home

# The one-call suite's fake registry and person-session fixtures, used by name.
registry = one_call.registry
_writes_run_in_a_person_session = one_call._writes_run_in_a_person_session

SLUG = "grooming_appointment_card"
TABLE_ID = str(uuid4())


def _tables(*rows: dict[str, Any]):
    async def read() -> list[dict[str, Any]]:
        return list(rows)

    return read


def _with_components(monkeypatch: pytest.MonkeyPatch, reg: FakeRegistry, components: list[Any]) -> None:
    """The fake registry's models, plus a KindComponent that can be read back."""
    from matrx_ai.tools.implementations import kind_authoring, kind_completeness, kind_shared

    models = reg.models()
    created = models["KindComponent"]

    class KindComponent(created):  # type: ignore[misc, valid-type]
        @classmethod
        def filter(cls, **kw: Any) -> _Query:
            return _Query([c for c in components if str(c.kind_definition_id) == kw.get("kind_definition_id")])

    class _Empty:
        @classmethod
        def filter(cls, **_kw: Any) -> _Query:
            return _Query([])

    models["KindComponent"] = KindComponent
    models["KindExample"] = type("KindExample", (models["KindExample"], _Empty), {})
    models["KindSurface"] = _Empty
    for module in (kind_authoring, kind_shared, kind_completeness):
        monkeypatch.setattr(module, "get_db_model", lambda key: models[key])


def _component(kd: Any, *, role: str, key: str) -> Any:
    return SimpleNamespace(
        id=uuid4(), kind_definition_id=kd.id, role=role, component_key=key, platform="web",
        is_active=True, is_default=role == "output", deleted_at=None, source="db", semver="1.0.0",
        version=1, sort_order=0, pinned_kind_version=None, component_source="x" if role == "output" else None,
        props_transform=None, notes=None,
    )


async def _kind_get(monkeypatch: pytest.MonkeyPatch, kd: Any) -> Any:
    from matrx_ai.tools.implementations import kind_authoring

    async def _resolve(_ref: str, _ctx: Any) -> tuple[Any, None]:
        return kd, None

    async def _can_view(_kd: Any, _ctx: Any) -> None:
        return None

    kd.authoring_owner, kd.created_by = "python", None
    monkeypatch.setattr(kind_authoring, "resolve_kind", _resolve)
    monkeypatch.setattr(kind_authoring, "ensure_can_view_kind", _can_view)
    return await kind_authoring.kind_get({"kind": SLUG, "include_schema": False}, make_ctx())


def test_the_table_a_kind_is_named_for_looks_like_its_home() -> None:
    assert looks_like_home(SLUG, "Grooming Appointments")
    assert not looks_like_home("grooming_visit_note", "Grooming Appointments")
    assert not looks_like_home("invoice_summary", "Grooming Appointments")


@pytest.mark.asyncio
async def test_kind_create_says_the_component_and_the_table_binding_are_missing(
    registry: FakeRegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    _with_components(monkeypatch, registry, [])
    monkeypatch.setitem(
        _ext._registry, KIND_TABLES_EXT_KEY,
        _tables({"table_id": TABLE_ID, "name": "Grooming Appointments", "kind": None}),
    )
    result = await create(name=SLUG, sample_data={"dog_name": "Rex", "service": "Bath", "time": "10:00"})
    assert result.success, result.error
    message = result.output.message
    assert "Completeness: INCOMPLETE (missing component and table binding)" in message
    assert f"kindcomp_create_component kind='{SLUG}'" in message
    assert "'Grooming Appointments'" in message and TABLE_ID in message
    assert "tables_shape action='show_rows_as'" in message


@pytest.mark.asyncio
async def test_kind_get_reports_a_half_made_kind_as_incomplete(
    registry: FakeRegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    kd = registry.existing(SLUG, {"dog_name": "Rex"})
    _with_components(monkeypatch, registry, [_component(kd, role="input", key="generic_structured")])
    monkeypatch.setitem(
        _ext._registry, KIND_TABLES_EXT_KEY,
        _tables({"table_id": TABLE_ID, "name": "Grooming Appointments", "kind": None}),
    )
    result = await _kind_get(monkeypatch, kd)
    assert result.success, result.error
    note = result.output.note or ""
    assert "INCOMPLETE (missing component and table binding)" in note
    assert "tables_shape action='show_rows_as'" in note


@pytest.mark.asyncio
async def test_kind_get_reads_complete_once_the_component_and_the_table_binding_exist(
    registry: FakeRegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    kd = registry.existing(SLUG, {"dog_name": "Rex"})
    _with_components(monkeypatch, registry, [_component(kd, role="output", key="grooming_card")])
    monkeypatch.setitem(
        _ext._registry, KIND_TABLES_EXT_KEY,
        _tables({"table_id": TABLE_ID, "name": "Grooming Appointments", "kind": SLUG}),
    )
    note = (await _kind_get(monkeypatch, kd)).output.note or ""
    assert note.startswith("Completeness: complete")
    assert "component 'grooming_card'" in note and "table 'Grooming Appointments'" in note
    assert "page_check" in note


@pytest.mark.asyncio
async def test_a_host_without_the_table_reader_says_so_and_never_guesses(
    registry: FakeRegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    kd = registry.existing(SLUG, {"dog_name": "Rex"})
    _with_components(monkeypatch, registry, [_component(kd, role="output", key="grooming_card")])
    monkeypatch.delitem(_ext._registry, KIND_TABLES_EXT_KEY, raising=False)
    note = (await _kind_get(monkeypatch, kd)).output.note or ""
    assert "table binding: unknown" in note


@pytest.mark.asyncio
async def test_a_component_with_no_table_binding_never_reads_complete(
    registry: FakeRegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    kd = registry.existing(SLUG, {"dog_name": "Rex"})
    _with_components(monkeypatch, registry, [_component(kd, role="output", key="grooming_card")])
    other = str(uuid4())
    monkeypatch.setitem(
        _ext._registry, KIND_TABLES_EXT_KEY,
        _tables(
            {"table_id": TABLE_ID, "name": "Appointments", "kind": None},
            {"table_id": other, "name": "Invoices", "kind": None},
        ),
    )
    note = (await _kind_get(monkeypatch, kd)).output.note or ""
    assert "Completeness: complete" not in note
    assert "component ready; no table shows its rows as this kind" in note
    assert "show_rows_as" in note and TABLE_ID in note and other in note
    assert note.index(TABLE_ID) < note.index(other)  # best word match first

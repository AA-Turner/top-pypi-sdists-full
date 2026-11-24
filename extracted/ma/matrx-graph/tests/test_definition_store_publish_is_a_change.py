"""A publish pins the newest SAVED version, records itself on the row, and never makes a version.

THE REAL CASE. A bookkeeping firm's operations lead keeps one workflow, "Month-end close
checklist", and publishes it every month after adjusting a step: the August save makes v2 and
publishing makes v2 live; the September save makes v3 and publishing makes v3 live. Workflows get
pinned by version, so each publish lands the snapshot of exactly the version the person saved —
never one more (P5 walk 2026-11-15: "Live v3 · Newest saved v4", Publish -> "Published v5").

THE HAZARD (VERSION-HISTORY-FIX, 2026-09-23). `platform.no_change_keeps_its_version()` is the
BEFORE-UPDATE trigger that stops a save which changed nothing from moving a row's version: when
NEW and OLD are equal in everything but ('version', 'updated_at'), it hands back OLD. Publish used
to be `set version = version + 1` and NOTHING ELSE — exactly the write that trigger swallows. The
second publish answered the old number, its snapshot hit UNIQUE (definition_id, version_number),
`ON CONFLICT DO NOTHING` inserted nothing, and the publish "succeeded" with no new version.

THE FAKE BELOW IS THAT TRIGGER, VERBATIM IN PYTHON: an update whose only differences are the
excluded keys returns the old row unchanged. It is what makes this test go red on the old code.
"""

from __future__ import annotations

import copy
from datetime import UTC, datetime
from typing import Any

import pytest

from matrx_graph.db import definition_store
from matrx_graph.db.definition_store import DefinitionStore
from matrx_graph.nodes import register_builtin_nodes

DEFINITION_ID = "5c1f0e2a-8d3b-4a7e-9b61-2f4c8e0d7a13"
OPERATIONS_LEAD = "7a2e9c41-3b5d-4f86-a1c0-9e8d6b4f2a57"
EXCLUDED = ("version", "updated_at")  # the binding workflow.definition would get


def _month_end_close() -> dict[str, Any]:
    return {
        "id": DEFINITION_ID,
        "name": "Month-end close checklist",
        "description": "Reconcile bank feeds, accrue payroll, lock the period, send the P&L.",
        "nodes": [
            {"id": "reconcile", "type": "io.user_input", "position": {"x": 0, "y": 0}, "data": {}},
            {"id": "accrue_payroll", "type": "text.template", "position": {"x": 240, "y": 0}, "data": {}},
        ],
        "edges": [{"id": "e1", "source": "reconcile", "target": "accrue_payroll"}],
        "viewport": {"x": 0, "y": 0, "zoom": 1},
        "channels": [],
        "strict_channels": False,
        "entry_nodes": ["reconcile"],
        "variables": [],
        "metadata": {"practice_area": "bookkeeping"},
        "tags": ["month-end", "close"],
        "category": "finance",
        "is_active": True,
        "version": 1,
        "deleted_at": None,
        "input_kind": None,
        # Declared, as the deliverable step answers: the publish under test never backfills it. Undeclared, a run
        # with the built-in steps registered compiles the graph and the publish backfills the kind — a revision of
        # its own (`test_definition_store_lifts_declared_kinds.py`), not what these tests pin.
        "output_kind": "template_render_result",
        "is_archived": False,
        "is_favorite": False,
        "published_to_web": False,
        "created_by": OPERATIONS_LEAD,
        "organization_id": "3e8b1d6f-0a42-4c97-b5e3-6d1f9a2c8b04",
        "project_id": None,
        "task_id": None,
        "created_at": "2026-07-28T16:00:00+00:00",
        "updated_at": "2026-07-28T16:00:00+00:00",
    }


class _Store:
    """One definition row and its snapshot table, with the no-op trigger bound."""

    row: dict[str, Any]
    snapshots: dict[int, dict[str, Any]]


class _Result:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows_affected = len(rows)
        self.updated_rows = rows


class _Query:
    def __init__(self, filters: dict[str, Any]) -> None:
        self.filters = filters
        self.locked = False

    def select_for_update(self, **_: Any) -> _Query:
        self.locked = True
        return self

    async def values(self, *fields: str) -> list[dict[str, Any]]:
        row = _Store.row
        if row["deleted_at"] is not None or str(self.filters.get("id")) != DEFINITION_ID:
            return []
        picked = copy.deepcopy(row)
        return [{k: picked[k] for k in fields} if fields else picked]


def _resolve(value: Any, current: Any) -> Any:
    # F("version") + 1 arrives as an expression object; evaluate it against the stored value.
    if hasattr(value, "resolve_for_test"):
        return value.resolve_for_test(current)
    if type(value).__name__ in {"F", "CombinedExpression", "Expression", "_Combined"} or (
        hasattr(value, "lhs") or hasattr(value, "rhs") or hasattr(value, "operator")
    ):
        return current + 1
    return value


class _DefinitionModel:
    @classmethod
    def filter(cls, **filters: Any) -> _Query:
        return _Query(filters)

    @classmethod
    async def update_where(cls, filters: dict[str, Any], **updates: Any) -> _Result:
        old = _Store.row
        if str(filters.get("id")) != DEFINITION_ID or old["deleted_at"] is not None:
            return _Result([])
        new = copy.deepcopy(old)
        for key, value in updates.items():
            new[key] = _resolve(value, old.get(key))
        new["updated_at"] = datetime.now(UTC).isoformat()
        # platform.no_change_keeps_its_version(): equal outside the excluded keys -> OLD.
        strip = lambda r: {k: v for k, v in r.items() if k not in EXCLUDED}  # noqa: E731
        if strip(new) == strip(old):
            return _Result([copy.deepcopy(old)])
        _Store.row = new
        return _Result([copy.deepcopy(new)])


class _VersionModel:
    @classmethod
    async def exists(cls, **filters: Any) -> bool:
        return filters.get("version_number") in _Store.snapshots

    @classmethod
    async def bulk_insert_ignore(cls, objects: list[dict[str, Any]], **_: Any) -> int:
        landed = 0
        for obj in objects:
            n = obj["version_number"]
            if n in _Store.snapshots:  # UNIQUE (definition_id, version_number) DO NOTHING
                continue
            _Store.snapshots[n] = obj
            landed += 1
        return landed


class _Tx:
    async def __aenter__(self) -> None:
        return None

    async def __aexit__(self, *exc: Any) -> bool:
        return False


@pytest.fixture
def month_end_close(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_orm
    from matrx_orm.core import transaction as tx_module

    # The steps are registered whatever ran before (the graph always compiles), so the outcome never depends on
    # test order: alone, the graph did not compile and the declaration check was skipped (red on main 2026-11-15
    # only after another file registered the built-ins).
    register_builtin_nodes(overwrite=True)
    _Store.row = _month_end_close()
    _Store.snapshots = {1: {"version_number": 1, "name": "Month-end close checklist"}}
    models = {"WfDefinition": _DefinitionModel, "WfDefinitionVersion": _VersionModel}
    monkeypatch.setattr(definition_store, "get_model", lambda name: models[name])
    monkeypatch.setattr(matrx_orm, "transaction", lambda *a, **k: _Tx())
    monkeypatch.setattr(tx_module, "get_active_connection", lambda: None)
    # Hermetic: these tests are about the version stamp. Whether the month-end graph compiles (and so whether
    # publish backfills an output kind, a revision of its own) depended on whether an EARLIER test had registered
    # the built-in step types — red in the full suite, green alone (CI 2026-11-15). The IO gate has its own tests.
    monkeypatch.setattr(definition_store, "_validate_io_declaration_for_publish", lambda row, definition_id: None)


def _save_a_step_change(note: str) -> None:
    """What a save does to the row: content moves and the revision with it."""
    _Store.row["description"] = note
    _Store.row["version"] += 1


@pytest.mark.asyncio
async def test_each_publish_pins_the_version_the_person_saved(month_end_close: None) -> None:
    store = DefinitionStore()

    _save_a_step_change("August: payroll accrual added")
    august = await store.publish(DEFINITION_ID, change_note="August close", changed_by_user_id=OPERATIONS_LEAD)
    _save_a_step_change("September: bank feed step reordered")
    september = await store.publish(DEFINITION_ID, change_note="September close", changed_by_user_id=OPERATIONS_LEAD)

    assert (august.version, september.version) == (2, 3)
    assert sorted(_Store.snapshots) == [1, 2, 3]
    assert _Store.snapshots[2]["description"] == "August: payroll accrual added"
    assert _Store.snapshots[3]["change_note"] == "September close"
    # the change publish records on the row is the publish itself, and the snapshot carries it
    published = _Store.row["metadata"]["published"]
    assert published["version"] == 3
    assert published["by"] == OPERATIONS_LEAD
    assert _Store.snapshots[3]["metadata"]["published"]["version"] == 3
    # the author's own metadata survives the stamp
    assert _Store.row["metadata"]["practice_area"] == "bookkeeping"


@pytest.mark.asyncio
async def test_publishing_the_newest_saved_version_never_makes_another(month_end_close: None) -> None:
    """The walk: Live v3, rename + Save makes v4, Publish must make v4 live — not v5."""
    store = DefinitionStore()
    _save_a_step_change("first steps")  # v2
    first = await store.publish(DEFINITION_ID, change_note="first")
    _save_a_step_change("renamed")  # v3
    second = await store.publish(DEFINITION_ID, change_note="after the rename")
    again = await store.publish(DEFINITION_ID, change_note="pressed twice")

    assert (first.version, second.version, again.version) == (2, 3, 3)
    assert _Store.row["version"] == 3
    assert sorted(_Store.snapshots) == [1, 2, 3]
    assert _Store.row["metadata"]["published"]["version"] == 3
    assert _Store.snapshots[3]["change_note"] == "after the rename"


@pytest.mark.asyncio
async def test_a_new_workflow_published_before_any_save_makes_its_first_version_live(
    month_end_close: None,
) -> None:
    """v1's snapshot is written at create: publishing it stamps it live and copies nothing."""
    row = await DefinitionStore().publish(DEFINITION_ID, change_note="go live")
    assert row.version == 1
    assert sorted(_Store.snapshots) == [1]
    assert _Store.row["metadata"]["published"]["version"] == 1


@pytest.mark.asyncio
async def test_a_database_that_counts_the_stamp_as_a_revision_still_publishes_what_it_stamps(
    month_end_close: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Before wf_256 declares `published` a background key, the hosted trigger bumps the version on the stamp:
    the publish must still pin exactly the version its stamp names, never a broken or mislabelled one."""
    original = _DefinitionModel.update_where.__func__

    async def bumping(cls: Any, filters: dict[str, Any], **updates: Any) -> _Result:
        await original(cls, filters, **updates)
        _Store.row["version"] += 1
        return _Result([copy.deepcopy(_Store.row)])

    monkeypatch.setattr(_DefinitionModel, "update_where", classmethod(bumping))
    _save_a_step_change("August")  # v2
    row = await DefinitionStore().publish(DEFINITION_ID, change_note="August close")
    assert row.version == _Store.row["version"] == _Store.row["metadata"]["published"]["version"]
    assert row.version in _Store.snapshots
    assert _Store.snapshots[row.version]["description"] == "August"


@pytest.mark.asyncio
async def test_a_database_that_counts_the_stamp_makes_one_revision_for_a_publish_never_two(
    month_end_close: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """P5 walk 2026-11-16: with the stamp counted as a revision, one Publish made v6 (unpublished) AND v7.
    The stamp now names the revision it lands on, so the publish makes exactly one."""
    original = _DefinitionModel.update_where.__func__

    async def bumping(cls: Any, filters: dict[str, Any], **updates: Any) -> _Result:
        await original(cls, filters, **updates)
        _Store.row["version"] += 1
        return _Result([copy.deepcopy(_Store.row)])

    monkeypatch.setattr(_DefinitionModel, "update_where", classmethod(bumping))
    _save_a_step_change("Save now")  # v2
    row = await DefinitionStore().publish(DEFINITION_ID, change_note="p")
    assert _Store.row["version"] == 3  # one extra revision, not two
    assert row.version == 3 and 3 in _Store.snapshots


@pytest.mark.asyncio
async def test_a_publish_on_the_fixed_trigger_makes_no_revision(month_end_close: None) -> None:
    _save_a_step_change("Save now")  # v2
    row = await DefinitionStore().publish(DEFINITION_ID, change_note="p")
    assert row.version == _Store.row["version"] == 2
    assert _Store.row["metadata"]["published"]["version"] == 2

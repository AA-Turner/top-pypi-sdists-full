"""A publish is a recorded change, so the database's no-op rule cannot swallow it.

THE REAL CASE. A bookkeeping firm's operations lead keeps one workflow, "Month-end close
checklist", and publishes it every month after adjusting a step: v2 in August, v3 in September.
Workflows get pinned by version, so every publish must land a NEW snapshot under a NEW number.

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
from matrx_graph.errors import DefinitionError

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
        "output_kind": None,
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

    _Store.row = _month_end_close()
    _Store.snapshots = {1: {"version_number": 1, "name": "Month-end close checklist"}}
    models = {"WfDefinition": _DefinitionModel, "WfDefinitionVersion": _VersionModel}
    monkeypatch.setattr(definition_store, "get_model", lambda name: models[name])
    monkeypatch.setattr(matrx_orm, "transaction", lambda *a, **k: _Tx())
    monkeypatch.setattr(tx_module, "get_active_connection", lambda: None)


@pytest.mark.asyncio
async def test_two_publishes_land_two_new_versions_under_the_no_op_rule(month_end_close: None) -> None:
    store = DefinitionStore()

    august = await store.publish(DEFINITION_ID, change_note="August close", changed_by_user_id=OPERATIONS_LEAD)
    september = await store.publish(DEFINITION_ID, change_note="September close", changed_by_user_id=OPERATIONS_LEAD)

    assert (august.version, september.version) == (2, 3)
    assert sorted(_Store.snapshots) == [1, 2, 3]
    assert _Store.snapshots[3]["change_note"] == "September close"
    # the change publish records on the row is the publish itself, and the snapshot carries it
    published = _Store.row["metadata"]["published"]
    assert published["version"] == 3
    assert published["by"] == OPERATIONS_LEAD
    assert _Store.snapshots[3]["metadata"]["published"]["version"] == 3
    # the author's own metadata survives the stamp
    assert _Store.row["metadata"]["practice_area"] == "bookkeeping"


@pytest.mark.asyncio
async def test_a_publish_the_database_refused_to_advance_raises_by_name(
    month_end_close: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """If anything ever swallows the increment again, publish says so instead of 'succeeding'."""

    async def swallow(cls: Any, filters: dict[str, Any], **updates: Any) -> _Result:
        return _Result([copy.deepcopy(_Store.row)])

    monkeypatch.setattr(_DefinitionModel, "update_where", classmethod(swallow))
    with pytest.raises(DefinitionError, match="did not advance"):
        await DefinitionStore().publish(DEFINITION_ID, change_note="August close")
    assert sorted(_Store.snapshots) == [1]


@pytest.mark.asyncio
async def test_a_snapshot_that_already_exists_is_a_refusal_not_a_silent_success(
    month_end_close: None,
) -> None:
    _Store.snapshots[2] = {"version_number": 2, "name": "left behind by an older publish"}
    with pytest.raises(DefinitionError, match="snapshot"):
        await DefinitionStore().publish(DEFINITION_ID, change_note="August close")

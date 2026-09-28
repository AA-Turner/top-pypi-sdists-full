"""The `task` tool works against the LIVE workspace.tasks shape — every action.

Verifier, 2026-09-26: the tool failed on every action with the ORM refusing
``Unknown field(s) on Tasks: ['is_public', 'user_id']``. workspace.tasks is a
canonical entity now: the owner is ``created_by``, who can see it is
``visibility`` (platform.visibility), it is soft-deleted through ``deleted_at``,
and ``organization_id`` is NOT NULL. The old tests mocked ``create_item`` with a
fake that accepted ANY keyword, so the dead column names sailed through.

Here the manager's ORM seams are replaced by a fake that refuses unknown columns
the way the real ORM does — against the column set of the live table (read
2026-09-26 through the Supabase MCP) — and every action runs through the real
``task`` dispatcher, as the model calls it: a clinic front desk's
"Verify insurance" task for a new patient.
"""

from __future__ import annotations

import copy
from contextlib import asynccontextmanager
from typing import Any

import pytest

from matrx_ai.tools.models import ToolContext

ORG = "5b0e4a51-8d2f-4c52-9d0a-2f3c1e7a9b10"  # the clinic's organization
PERSON = "0f6c2a3e-1b4d-4e5f-8a9b-7c6d5e4f3a21"  # the front-desk coordinator

# workspace.tasks, live (information_schema.columns, 2026-09-26).
LIVE_TASK_COLUMNS = frozenset(
    {
        "id", "title", "description", "project_id", "status", "due_date",
        "created_at", "updated_at", "parent_task_id", "priority", "assignee_id",
        "settings", "organization_id", "created_by", "visibility", "version",
        "deleted_at", "metadata", "updated_by", "completed_at", "origin",
        "source_type", "source_id", "source_url", "source_label", "dedupe_key",
        "start_date", "due_time", "timezone", "recurrence_rule", "reminders",
        "source_list_id", "source_imported_at", "source_snapshot", "custom_fields",
    }
)


class OrmRefusal(ValueError):
    pass


def _refuse_unknown(keys: list[str]) -> None:
    unknown = sorted({k.split("__", 1)[0] for k in keys} - LIVE_TASK_COLUMNS)
    if unknown:
        # The real ORM's sentence (matrx_orm core/extended.py / dynamic_crud.py).
        raise OrmRefusal(f"Unknown field(s) on Tasks: {unknown}")


class _Row:
    def __init__(self, data: dict[str, Any]) -> None:
        self.__dict__.update(data)
        self._data = data

    def to_dict(self) -> dict[str, Any]:
        return copy.deepcopy(self._data)


class FakeTasksTable:
    """An in-memory workspace.tasks that answers like the ORM — including its refusals."""

    def __init__(self) -> None:
        self.rows: dict[str, dict[str, Any]] = {}
        self.seq = 0

    async def create_item(self, _mgr: Any, **data: Any) -> _Row:
        _refuse_unknown(list(data))
        self.seq += 1
        tid = f"7d1f0c3a-0000-4000-8000-{self.seq:012d}"
        row = {c: None for c in LIVE_TASK_COLUMNS}
        row.update(visibility="internal", version=1, status="incomplete")
        row.update(data)
        row.update(id=tid, created_at="2026-09-26T09:00:00Z", updated_at="2026-09-26T09:00:00Z")
        if not row.get("organization_id"):
            raise OrmRefusal('null value in column "organization_id" violates not-null constraint')
        self.rows[tid] = row
        return _Row(row)

    async def load_by_id(self, _mgr: Any, task_id: str) -> _Row:
        if task_id not in self.rows:
            raise LookupError(f"Tasks {task_id} not found")
        return _Row(self.rows[task_id])

    async def load_item_or_none(self, _mgr: Any, use_cache: bool = True, **pk: Any) -> _Row | None:
        tid = str(pk.get("id"))
        return _Row(self.rows[tid]) if tid in self.rows else None

    async def _update_item(self, _mgr: Any, item: Any, **updates: Any) -> _Row:
        return await self.update_item(_mgr, str(item.id), **updates)

    async def update_item(self, _mgr: Any, task_id: str, **updates: Any) -> _Row:
        _refuse_unknown(list(updates))
        if task_id not in self.rows:
            raise LookupError(f"Tasks {task_id} not found")
        self.rows[task_id].update(updates)
        self.rows[task_id]["updated_at"] = "2026-09-26T10:00:00Z"
        return _Row(self.rows[task_id])

    async def _get_items(self, _mgr: Any, order_by: str | None = None, **filters: Any) -> list[_Row]:
        _refuse_unknown(list(filters))
        out = []
        for row in self.rows.values():
            ok = True
            for key, want in filters.items():
                col, _, op = key.partition("__")
                if op == "isnull":
                    ok = ok and ((row.get(col) is None) == bool(want))
                else:
                    ok = ok and row.get(col) == want
            if ok:
                out.append(_Row(row))
        return out

    async def delete_item(self, _mgr: Any, task_id: str) -> bool:  # a hard delete must not happen
        raise AssertionError("task delete must archive (soft-delete), never hard-delete")


@pytest.fixture
def table(monkeypatch: pytest.MonkeyPatch) -> FakeTasksTable:
    from matrx_ai.db.content_types import tasks as tasks_module

    fake = FakeTasksTable()
    cls = type(tasks_module.tasks_manager_instance)
    for name in (
        "create_item", "load_by_id", "update_item", "_get_items", "delete_item",
        "load_item_or_none", "_update_item",
    ):
        monkeypatch.setattr(cls, name, _bind(fake, name))
    monkeypatch.setattr(cls, "_governed_write", lambda self: _no_session(), raising=False)
    monkeypatch.setattr(cls, "_pk_filter", lambda self, item_id: {"id": item_id}, raising=False)
    # Every action runs as the person (RLS decides); a pass-through session here.
    from matrx_ai import _ext

    monkeypatch.setitem(_ext._registry, "acting_as_caller", _no_session)
    return fake


@asynccontextmanager
async def _no_session():
    yield


def _bind(fake: FakeTasksTable, name: str):
    method = getattr(fake, name)

    async def seam(self: Any, *args: Any, **kwargs: Any) -> Any:
        return await method(self, *args, **kwargs)

    return seam


def _ctx(monkeypatch: pytest.MonkeyPatch, org: str | None) -> ToolContext:
    monkeypatch.setattr(ToolContext, "user_id", property(lambda self: PERSON))
    monkeypatch.setattr(ToolContext, "organization_id", property(lambda self: org))
    return ToolContext(call_id="call-front-desk")


async def _task(args: dict[str, Any], ctx: ToolContext):
    from matrx_ai.tools.implementations.tasks import task

    return await task(args, ctx)


def _fail(result: Any) -> str:
    return result.error.message if result.error else repr(result)


@pytest.mark.asyncio
async def test_every_task_action_works_against_the_live_columns(table, monkeypatch):
    ctx = _ctx(monkeypatch, ORG)

    created = await _task(
        {
            "action": "create",
            "title": "Verify insurance for Maria Lopez before Thursday's 9:30 visit",
            "description": "Call Blue Shield PPO; confirm active coverage and the specialist copay.",
            "priority": "high",
            "due_date": "2026-10-01",
        },
        ctx,
    )
    assert created.success, _fail(created)
    tid = created.output["id"]
    stored = table.rows[tid]
    assert stored["created_by"] == PERSON
    assert stored["organization_id"] == ORG
    assert stored["visibility"] == "internal"  # the table's default when not said

    listed = await _task({"action": "list"}, ctx)
    assert listed.success, _fail(listed)
    assert [t["id"] for t in listed.output["tasks"]] == [tid]
    assert listed.output["organization_id"] == ORG

    got = await _task({"action": "get", "task_id": tid}, ctx)
    assert got.success, _fail(got)
    assert got.output["title"].startswith("Verify insurance for Maria Lopez")
    assert got.output["visibility"] == "internal"

    updated = await _task(
        {
            "action": "update",
            "task_id": tid,
            "status": "completed",
            "description": "Coverage active through 12/31; specialist copay $40.",
        },
        ctx,
    )
    assert updated.success, _fail(updated)
    assert table.rows[tid]["status"] == "completed"
    # The surface-write receipt still shows the person what changed.
    assert updated.surface_write is not None, "task:update lost its before→after receipt"
    assert "Call Blue Shield PPO" in updated.surface_write.before
    assert "specialist copay $40" in updated.surface_write.after

    shared = await _task({"action": "update", "task_id": tid, "visibility": "personal"}, ctx)
    assert shared.success, _fail(shared)
    assert table.rows[tid]["visibility"] == "personal"

    deleted = await _task({"action": "delete", "task_id": tid}, ctx)
    assert deleted.success, _fail(deleted)
    assert tid in table.rows and table.rows[tid]["deleted_at"] is not None  # archived, recoverable

    after = await _task({"action": "list"}, ctx)
    assert after.success, _fail(after)
    assert after.output["tasks"] == []  # an archived task leaves the list


@pytest.mark.asyncio
async def test_create_without_an_organization_is_held_not_defaulted(table, monkeypatch):
    ctx = _ctx(monkeypatch, None)
    result = await _task({"action": "create", "title": "Verify insurance for Maria Lopez"}, ctx)

    assert not result.success
    assert result.error.error_type == "organization_required"
    assert table.rows == {}, "nothing may be written without the organization the request carries"
    from matrx_connect.org_hold import assert_no_default_org_wording

    assert_no_default_org_wording(result.error.message + (result.error.suggested_action or ""))

    # Listing without an organization is held too — never "every organization".
    listed = await _task({"action": "list"}, ctx)
    assert not listed.success
    assert listed.error.error_type == "organization_required"


@pytest.mark.asyncio
async def test_retired_spelling_is_refused_by_the_contract(table, monkeypatch):
    """`is_public` is not a column any more; the args contract says so up front."""
    ctx = _ctx(monkeypatch, ORG)
    result = await _task(
        {"action": "create", "title": "Verify insurance", "is_public": True}, ctx
    )
    assert not result.success
    assert result.error.error_type == "validation", result.error
    assert "is_public" in result.error.message
    assert table.rows == {}

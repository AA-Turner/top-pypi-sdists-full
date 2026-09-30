"""The `task` tool reads and writes AS THE PERSON — RLS decides, never the tool.

Defect (2026-09-26): every task action loaded ``task_id`` on the privileged ORM
connection with no access decision, so any person's agent could read or edit any
task by id. Chair ruling: the tool must not grow permission logic; it runs its
ORM work inside the caller's RLS session (``as_the_person`` → the host's
``acting_as_caller`` → matrx-orm ``rls_session``) and Postgres decides.

The ORM seams below are an in-memory workspace.tasks that behaves like the table
under RLS: it answers ONLY inside a person session, and only with the rows that
person may see / change. Anything that touches it outside a session, or reads a
row by id through the identity-blind cache, is recorded as a violation.

Scenario: a dental clinic. Dr. Ahmadi (office manager) owns the task
"Renew the X-ray sensor warranty"; Sam, a patient-portal volunteer in another
organization, must not be able to read or change it through the tool.
"""

from __future__ import annotations

import copy
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Any

import pytest

from matrx_ai.tools.models import ToolContext

CLINIC_ORG = "3c2b1a09-8f7e-4d6c-9b5a-1e2d3c4b5a60"
MANAGER = "a1b2c3d4-0000-4000-8000-00000000a001"  # Dr. Ahmadi — owns the task
OUTSIDER = "a1b2c3d4-0000-4000-8000-00000000b002"  # Sam — not in the clinic
TASK_ID = "91dd021c-0000-4000-8000-000000000001"

_acting: ContextVar[str | None] = ContextVar("fake_acting_user", default=None)


class _Row:
    def __init__(self, data: dict[str, Any]) -> None:
        self.__dict__.update(data)
        self._data = data

    def to_dict(self) -> dict[str, Any]:
        return copy.deepcopy(self._data)


class RlsTasksTable:
    """workspace.tasks as RLS shows it: visible/writable per acting person."""

    def __init__(self) -> None:
        self.rows: dict[str, dict[str, Any]] = {}
        self.readers: dict[str, set[str]] = {}
        self.writers: dict[str, set[str]] = {}
        self.violations: list[str] = []
        self.db_calls = 0
        self.seq = 0

    def seed(self, row: dict[str, Any], *, readers: set[str], writers: set[str]) -> None:
        self.rows[row["id"]] = row
        self.readers[row["id"]] = readers
        self.writers[row["id"]] = writers

    def _who(self, seam: str) -> str | None:
        self.db_calls += 1
        who = _acting.get()
        if who is None:
            self.violations.append(f"{seam}: ran on the privileged connection (no person session)")
        return who

    def _visible(self, who: str | None, tid: str) -> bool:
        return tid in self.rows and who in self.readers.get(tid, set())

    # --- read seams -------------------------------------------------------
    async def load_item_or_none(self, _mgr: Any, use_cache: bool = True, **pk: Any) -> _Row | None:
        who = self._who("load_item_or_none")
        if use_cache:
            self.violations.append("load_item_or_none: by-id read through the identity-blind cache")
        tid = str(pk.get("id"))
        return _Row(self.rows[tid]) if self._visible(who, tid) else None

    async def load_by_id(self, _mgr: Any, task_id: str) -> _Row:
        who = self._who("load_by_id")
        self.violations.append("load_by_id: by-id read through the identity-blind cache")
        if not self._visible(who, task_id):
            raise LookupError(f"Tasks {task_id} not found")
        return _Row(self.rows[task_id])

    async def _get_items(self, _mgr: Any, order_by: str | None = None, **filters: Any) -> list[_Row]:
        who = self._who("_get_items")
        out = []
        for tid, row in self.rows.items():
            if not self._visible(who, tid):
                continue
            ok = True
            for key, want in filters.items():
                col, _, op = key.partition("__")
                ok = ok and (
                    ((row.get(col) is None) == bool(want)) if op == "isnull" else row.get(col) == want
                )
            if ok:
                out.append(_Row(row))
        return out

    # --- write seams ------------------------------------------------------
    async def create_item(self, _mgr: Any, **data: Any) -> _Row:
        who = self._who("create_item")
        self.seq += 1
        tid = f"91dd021c-0000-4000-8000-{self.seq + 100:012d}"
        row = {"id": tid, "published_to_web": False, "version": 1, "deleted_at": None, **data}
        self.seed(row, readers={who} if who else set(), writers={who} if who else set())
        return _Row(row)

    def _write(self, who: str | None, tid: str, updates: dict[str, Any]) -> _Row:
        if tid not in self.rows or who not in self.writers.get(tid, set()):
            # RLS refuses an UPDATE silently; the ORM turns 0 rows into this.
            raise ValueError(f"No rows were updated for Tasks with {{'id': '{tid}'}}")
        self.rows[tid].update(updates)
        self.rows[tid]["version"] += 1
        return _Row(self.rows[tid])

    async def _update_item(self, _mgr: Any, item: Any, **updates: Any) -> _Row:
        return self._write(self._who("_update_item"), str(item.id), updates)

    async def update_item(self, _mgr: Any, task_id: str, **updates: Any) -> _Row:
        return self._write(self._who("update_item"), task_id, updates)


@asynccontextmanager
async def _nothing():
    yield


@pytest.fixture
def table(monkeypatch: pytest.MonkeyPatch) -> RlsTasksTable:
    from matrx_ai.db.content_types import tasks as tasks_module

    fake = RlsTasksTable()
    fake.seed(
        {
            "id": TASK_ID,
            "title": "Renew the X-ray sensor warranty",
            "description": "Schick 33 sensor warranty lapses Oct 15; quote from Patterson.",
            "status": "incomplete",
            "priority": "high",
            "organization_id": CLINIC_ORG,
            "created_by": MANAGER,
            "published_to_web": False,
            "version": 3,
            "deleted_at": None,
            "parent_task_id": None,
            "project_id": None,
        },
        readers={MANAGER},
        writers={MANAGER},
    )
    cls = type(tasks_module.tasks_manager_instance)
    for name in (
        "load_item_or_none", "load_by_id", "_get_items", "create_item", "_update_item", "update_item",
    ):
        monkeypatch.setattr(cls, name, _bind(fake, name))
    monkeypatch.setattr(cls, "_governed_write", lambda self: _nothing(), raising=False)
    # The test run registers stub ORM models; address rows by plain id.
    monkeypatch.setattr(cls, "_pk_filter", lambda self, item_id: {"id": item_id}, raising=False)
    return fake


def _bind(fake: RlsTasksTable, name: str):
    method = getattr(fake, name)

    async def seam(self: Any, *args: Any, **kwargs: Any) -> Any:
        return await method(self, *args, **kwargs)

    return seam


@pytest.fixture
def person_session(monkeypatch: pytest.MonkeyPatch):
    """The host's act-as-the-caller seam, answering for whoever the context says."""
    from matrx_ai import _ext

    current: dict[str, str] = {}

    @asynccontextmanager
    async def acting_as_caller():
        token = _acting.set(current["user"])
        try:
            yield
        finally:
            _acting.reset(token)

    monkeypatch.setitem(_ext._registry, "acting_as_caller", acting_as_caller)
    return current


def _ctx(monkeypatch: pytest.MonkeyPatch, current: dict[str, str] | None, user: str) -> ToolContext:
    if current is not None:
        current["user"] = user
    monkeypatch.setattr(ToolContext, "user_id", property(lambda self: user))
    monkeypatch.setattr(ToolContext, "organization_id", property(lambda self: CLINIC_ORG))
    return ToolContext(call_id=f"call-{user[-4:]}")


async def _task(args: dict[str, Any], ctx: ToolContext):
    from matrx_ai.tools.implementations.tasks import task

    return await task(args, ctx)


@pytest.mark.asyncio
async def test_the_owner_works_every_action_inside_their_own_session(table, person_session, monkeypatch):
    ctx = _ctx(monkeypatch, person_session, MANAGER)

    got = await _task({"action": "get", "task_id": TASK_ID}, ctx)
    assert got.success, got.error
    assert got.output["title"] == "Renew the X-ray sensor warranty"

    listed = await _task({"action": "list"}, ctx)
    assert listed.success, listed.error
    assert [t["id"] for t in listed.output["tasks"]] == [TASK_ID]

    updated = await _task({"action": "update", "task_id": TASK_ID, "status": "completed"}, ctx)
    assert updated.success, updated.error
    assert table.rows[TASK_ID]["status"] == "completed"

    created = await _task({"action": "create", "title": "Order sensor sleeves (box of 500)"}, ctx)
    assert created.success, created.error

    deleted = await _task({"action": "delete", "task_id": created.output["id"]}, ctx)
    assert deleted.success, deleted.error
    assert table.rows[created.output["id"]]["deleted_at"] is not None

    assert table.violations == [], table.violations


@pytest.mark.asyncio
async def test_an_outsider_cannot_read_the_task_and_is_told_so_by_id(table, person_session, monkeypatch):
    ctx = _ctx(monkeypatch, person_session, OUTSIDER)

    got = await _task({"action": "get", "task_id": TASK_ID}, ctx)
    assert not got.success
    assert got.error.error_type == "not_found"
    assert TASK_ID in got.error.message
    assert "Renew" not in got.error.message  # nothing about the task leaks

    subtasks = await _task({"action": "list", "parent_task_id": TASK_ID}, ctx)
    assert not subtasks.success, "a hidden parent must not read as 'no subtasks'"
    assert subtasks.error.error_type == "not_found"
    assert TASK_ID in subtasks.error.message

    assert table.violations == [], table.violations


@pytest.mark.asyncio
async def test_an_outsider_cannot_edit_or_archive_the_task(table, person_session, monkeypatch):
    before = copy.deepcopy(table.rows[TASK_ID])
    ctx = _ctx(monkeypatch, person_session, OUTSIDER)

    updated = await _task(
        {"action": "update", "task_id": TASK_ID, "title": "Cancel the warranty"}, ctx
    )
    assert not updated.success
    assert updated.error.error_type == "not_found"
    assert TASK_ID in updated.error.message

    deleted = await _task({"action": "delete", "task_id": TASK_ID}, ctx)
    assert not deleted.success
    assert deleted.error.error_type == "not_found"
    assert TASK_ID in deleted.error.message

    assert table.rows[TASK_ID] == before, "the owner's task changed under an outsider's call"
    assert table.violations == [], table.violations


@pytest.mark.asyncio
async def test_a_reader_who_may_not_edit_gets_no_access_not_a_conflict(table, person_session, monkeypatch):
    table.readers[TASK_ID].add(OUTSIDER)  # shared to view only
    ctx = _ctx(monkeypatch, person_session, OUTSIDER)

    got = await _task({"action": "get", "task_id": TASK_ID}, ctx)
    assert got.success, got.error

    updated = await _task({"action": "update", "task_id": TASK_ID, "status": "completed"}, ctx)
    assert not updated.success
    assert updated.error.error_type == "no_access"
    assert TASK_ID in updated.error.message
    assert table.rows[TASK_ID]["status"] == "incomplete"
    assert table.violations == [], table.violations


@pytest.mark.asyncio
async def test_without_a_person_session_the_tool_refuses_and_never_touches_the_db(table, monkeypatch):
    from matrx_ai import _ext

    monkeypatch.delitem(_ext._registry, "acting_as_caller", raising=False)
    ctx = _ctx(monkeypatch, None, MANAGER)

    for args in (
        {"action": "get", "task_id": TASK_ID},
        {"action": "list"},
        {"action": "create", "title": "Order sensor sleeves"},
        {"action": "update", "task_id": TASK_ID, "status": "completed"},
        {"action": "delete", "task_id": TASK_ID},
    ):
        result = await _task(args, ctx)
        assert not result.success, args
        assert result.error.error_type == "unavailable", (args, result.error)

    assert table.db_calls == 0, "a refused call must not reach the database on any connection"

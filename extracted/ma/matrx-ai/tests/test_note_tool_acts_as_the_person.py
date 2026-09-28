"""The `note` tool reads and writes AS THE PERSON — RLS decides, never the tool.

Defect (2026-09-27): every note action loaded ``note_id`` on the privileged ORM
connection, then decided access in Python — an owner comparison
(``created_by == ctx.user_id``) followed by ``iam.has_access_for``. Chair ruling:
the tool must not carry permission logic; it runs its ORM work inside the
caller's RLS session (``acts_as_the_person`` → the host's ``acting_as_caller`` →
matrx-orm ``rls_session``) and Postgres decides.

The ORM seams below are an in-memory workbench.notes that behaves like the table
under RLS: it answers ONLY inside a person session, and only with the rows that
person may see / change. Anything that touches it outside a session, reads a row
by id through the identity-blind cache, or asks ``iam.has_access_for`` from app
code is recorded as a violation.

Scenario: a veterinary clinic. Dr. Okafor (practice owner) keeps the note
"Controlled-substance log — ketamine count"; Jordan, a groomer at a different
business, must not read or change it through their agent.
"""

from __future__ import annotations

import copy
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Any

import pytest

from matrx_ai.tools.models import ToolContext

CLINIC_ORG = "5a1c0e2b-3d4f-4a6b-8c7d-9e0f1a2b3c4d"
OWNER = "b7c8d9e0-0000-4000-8000-00000000c001"  # Dr. Okafor — owns the note
OUTSIDER = "b7c8d9e0-0000-4000-8000-00000000d002"  # Jordan — another business
NOTE_ID = "6e0f7a1b-0000-4000-8000-000000000001"
NOTE_BODY = "Ketamine 100mg/mL: 3 vials on hand after Tuesday's spay block. Counted by DO + RN."

_acting: ContextVar[str | None] = ContextVar("fake_acting_user_notes", default=None)


class _Row:
    def __init__(self, data: dict[str, Any]) -> None:
        self.__dict__.update(data)
        self._data = data

    def to_dict(self) -> dict[str, Any]:
        return copy.deepcopy(self._data)


class RlsNotesTable:
    """workbench.notes as RLS shows it: visible/writable per acting person."""

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

    def _visible(self, who: str | None, nid: str) -> bool:
        return nid in self.rows and who in self.readers.get(nid, set())

    async def load_item_or_none(self, _mgr: Any, use_cache: bool = True, **pk: Any) -> _Row | None:
        who = self._who("load_item_or_none")
        if use_cache:
            self.violations.append("load_item_or_none: by-id read through the identity-blind cache")
        nid = str(pk.get("id"))
        return _Row(self.rows[nid]) if self._visible(who, nid) else None

    async def load_notes_by_id(self, _mgr: Any, note_id: str) -> _Row:
        who = self._who("load_notes_by_id")
        self.violations.append("load_notes_by_id: by-id read through the identity-blind cache")
        if not self._visible(who, note_id):
            raise LookupError(f"Notes {note_id} not found")
        return _Row(self.rows[note_id])

    async def _get_items(self, _mgr: Any, order_by: str | None = None, **filters: Any) -> list[_Row]:
        who = self._who("_get_items")
        out = []
        for nid, row in self.rows.items():
            if not self._visible(who, nid):
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

    async def create_notes(self, _mgr: Any, **data: Any) -> _Row:
        who = self._who("create_notes")
        self.seq += 1
        nid = f"6e0f7a1b-0000-4000-8000-{self.seq + 100:012d}"
        row = {"id": nid, "version": 1, "deleted_at": None, **data}
        self.seed(row, readers={who} if who else set(), writers={who} if who else set())
        return _Row(row)

    def write(self, who: str | None, nid: str, updates: dict[str, Any]) -> _Row:
        if nid not in self.rows or who not in self.writers.get(nid, set()):
            # RLS refuses an UPDATE silently; the ORM turns 0 rows into this.
            raise ValueError(f"No rows were updated for Notes with {{'id': '{nid}'}}")
        self.rows[nid].update(updates)
        self.rows[nid]["version"] += 1
        return _Row(self.rows[nid])

    async def _update_item(self, _mgr: Any, item: Any, **updates: Any) -> _Row:
        return self.write(self._who("_update_item"), str(item.id), updates)

    async def update_notes(self, _mgr: Any, note_id: str, **updates: Any) -> _Row:
        return self.write(self._who("update_notes"), note_id, updates)

    async def archive_where(self, _model: Any, filters: dict[str, Any]) -> int:
        who = self._who("archive_where")
        nid = str(filters["id"])
        if nid not in self.rows or who not in self.writers.get(nid, set()):
            return 0  # RLS: the UPDATE matched no row this person may change
        if self.rows[nid]["deleted_at"] is not None:
            return 0
        self.rows[nid]["deleted_at"] = "2026-09-27T12:00:00Z"
        return 1


@asynccontextmanager
async def _nothing():
    yield


@pytest.fixture
def table(monkeypatch: pytest.MonkeyPatch) -> RlsNotesTable:
    from matrx_ai.db.content_types import notes as notes_module
    from matrx_ai.tools import soft_delete

    fake = RlsNotesTable()
    fake.seed(
        {
            "id": NOTE_ID,
            "label": "Controlled-substance log — ketamine count",
            "folder_name": "Pharmacy",
            "content": NOTE_BODY,
            "tags": ["dea", "pharmacy"],
            "visibility": "internal",
            "organization_id": CLINIC_ORG,
            "created_by": OWNER,
            "version": 4,
            "deleted_at": None,
        },
        readers={OWNER},
        writers={OWNER},
    )
    cls = type(notes_module.notes_manager_instance)
    for name in (
        "load_item_or_none", "load_notes_by_id", "_get_items", "create_notes",
        "_update_item", "update_notes",
    ):
        monkeypatch.setattr(cls, name, _bind(fake, name), raising=False)
    monkeypatch.setattr(cls, "_governed_write", lambda self: _nothing(), raising=False)
    monkeypatch.setattr(cls, "_pk_filter", lambda self, item_id: {"id": item_id}, raising=False)

    async def archive(model: Any, filters: dict[str, Any]) -> int:
        return await fake.archive_where(model, filters)

    monkeypatch.setattr(soft_delete, "archive_where", archive)

    # App code must never ask the permission question itself.
    import matrx_orm

    async def forbidden_call_function(*args: Any, **kwargs: Any) -> Any:
        fake.violations.append(f"call_function{args[1:4]}: app code asked an access question")
        return True

    monkeypatch.setattr(matrx_orm, "call_function", forbidden_call_function, raising=False)
    return fake


def _bind(fake: RlsNotesTable, name: str):
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


async def _note(args: dict[str, Any], ctx: ToolContext):
    from matrx_ai.tools.implementations.notes import note

    return await note(args, ctx)


@pytest.mark.asyncio
async def test_the_owner_works_every_action_inside_their_own_session(table, person_session, monkeypatch):
    ctx = _ctx(monkeypatch, person_session, OWNER)

    got = await _note({"action": "get", "note_id": NOTE_ID}, ctx)
    assert got.success, got.error
    assert got.output["content"] == NOTE_BODY

    listed = await _note({"action": "list"}, ctx)
    assert listed.success, listed.error
    assert [n["id"] for n in listed.output["notes"]] == [NOTE_ID]

    updated = await _note(
        {"action": "update", "note_id": NOTE_ID, "label": "Ketamine count — Sept"}, ctx
    )
    assert updated.success, updated.error
    assert table.rows[NOTE_ID]["label"] == "Ketamine count — Sept"

    patched = await _note(
        {"action": "patch", "note_id": NOTE_ID, "search_text": "3 vials", "replacement_text": "2 vials"},
        ctx,
    )
    assert patched.success, patched.error
    assert "2 vials" in table.rows[NOTE_ID]["content"]

    created = await _note({"action": "create", "label": "Order more sharps containers"}, ctx)
    assert created.success, created.error

    deleted = await _note({"action": "delete", "note_id": created.output["id"]}, ctx)
    assert deleted.success, deleted.error
    assert table.rows[created.output["id"]]["deleted_at"] is not None

    assert table.violations == [], table.violations


@pytest.mark.asyncio
async def test_an_outsider_cannot_read_the_note_and_is_told_so_by_id(table, person_session, monkeypatch):
    ctx = _ctx(monkeypatch, person_session, OUTSIDER)

    got = await _note({"action": "get", "note_id": NOTE_ID}, ctx)
    assert not got.success
    assert got.error.error_type == "not_found"
    assert NOTE_ID in got.error.message
    assert "ketamine" not in got.error.message.lower()  # nothing about the note leaks

    listed = await _note({"action": "list"}, ctx)
    assert listed.success, listed.error
    assert listed.output["notes"] == []

    assert table.violations == [], table.violations


@pytest.mark.asyncio
async def test_an_outsider_cannot_edit_patch_or_archive_the_note(table, person_session, monkeypatch):
    before = copy.deepcopy(table.rows[NOTE_ID])
    ctx = _ctx(monkeypatch, person_session, OUTSIDER)

    for args in (
        {"action": "update", "note_id": NOTE_ID, "content": "count is fine"},
        {"action": "patch", "note_id": NOTE_ID, "search_text": "3 vials", "replacement_text": "9 vials"},
        {"action": "delete", "note_id": NOTE_ID},
    ):
        result = await _note(args, ctx)
        assert not result.success, args
        assert result.error.error_type == "not_found", (args, result.error)
        assert NOTE_ID in result.error.message

    assert table.rows[NOTE_ID] == before, "the owner's note changed under an outsider's call"
    assert table.violations == [], table.violations


@pytest.mark.asyncio
async def test_a_reader_who_may_not_edit_gets_no_access(table, person_session, monkeypatch):
    table.readers[NOTE_ID].add(OUTSIDER)  # shared to view only
    ctx = _ctx(monkeypatch, person_session, OUTSIDER)

    got = await _note({"action": "get", "note_id": NOTE_ID}, ctx)
    assert got.success, got.error

    for args in (
        {"action": "update", "note_id": NOTE_ID, "label": "renamed"},
        {"action": "patch", "note_id": NOTE_ID, "search_text": "3 vials", "replacement_text": "9 vials"},
        {"action": "delete", "note_id": NOTE_ID},
    ):
        result = await _note(args, ctx)
        assert not result.success, args
        assert result.error.error_type == "no_access", (args, result.error)
        assert NOTE_ID in result.error.message

    assert table.rows[NOTE_ID]["content"] == NOTE_BODY
    assert table.rows[NOTE_ID]["deleted_at"] is None
    assert table.violations == [], table.violations


@pytest.mark.asyncio
async def test_without_a_person_session_the_tool_refuses_and_never_touches_the_db(table, monkeypatch):
    from matrx_ai import _ext

    monkeypatch.delitem(_ext._registry, "acting_as_caller", raising=False)
    ctx = _ctx(monkeypatch, None, OWNER)

    for args in (
        {"action": "get", "note_id": NOTE_ID},
        {"action": "list"},
        {"action": "create", "label": "Order sharps containers"},
        {"action": "update", "note_id": NOTE_ID, "label": "x"},
        {"action": "patch", "note_id": NOTE_ID, "search_text": "3 vials", "replacement_text": "2"},
        {"action": "delete", "note_id": NOTE_ID},
    ):
        result = await _note(args, ctx)
        assert not result.success, args
        assert result.error.error_type == "unavailable", (args, result.error)

    assert table.db_calls == 0, "a refused call must not reach the database on any connection"

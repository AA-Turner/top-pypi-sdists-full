"""Unit tests for the ``instance_*`` toolset (saved kind instances).

Pure-logic coverage: authorization is RLS's answer in the CALLER's session
(no owner fast path, no ``iam.has_access_for`` call from app code; viewer = the
row is returned, editor = ``SELECT ... FOR UPDATE`` returns it), content-free
denials, title derivation, and arg-contract enforcement. The
live DB lifecycle (create -> verdict -> list -> update -> repin -> soft-delete
-> revalidate-after-schema-change) is exercised by
``tests_trials/run_kind_tools_e2e.py`` (repo root) against the real database.
"""

from __future__ import annotations

import contextlib
from contextvars import ContextVar
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai.tools.implementations import kind_instance as ki
from matrx_ai.tools.implementations.kind_instance import (
    INSTANCE_ENTITY_TOKEN,
    derive_title,
    instance_summary,
)
from matrx_ai.tools.models import ToolContext


def make_ctx() -> ToolContext:
    return ToolContext(call_id=str(uuid4()), tool_name="test")


def _instance_row(created_by: str | None, **overrides: Any) -> Any:
    base: dict[str, Any] = {
        "id": uuid4(),
        "kind_definition_id": uuid4(),
        "title": "Secret Title",
        "kind_version": 1,
        "validation_status": "passed",
        "data": {"secret": "payload"},
        "created_by": created_by,
        "organization_id": uuid4(),
        "deleted_at": None,
        "updated_at": None,
    }
    base.update(overrides)
    return SimpleNamespace(**base)


_acting: ContextVar[str | None] = ContextVar("fake_acting_user_instances", default=None)


@pytest.fixture
def person_session(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """The host's act-as-the-caller seam: RLS answers for whoever ``current`` names."""
    from matrx_ai import _ext

    current: dict[str, str] = {}

    @contextlib.asynccontextmanager
    async def acting_as_caller():
        token = _acting.set(current.get("user"))
        try:
            yield
        finally:
            _acting.reset(token)

    monkeypatch.setitem(_ext._registry, "acting_as_caller", acting_as_caller)
    return current


class _Locking:
    def __init__(self, model: _FakeModel, pk: dict[str, Any]):
        self._model, self._pk = model, pk

    def select_for_update(self) -> _Locking:
        return self

    async def values(self, *_fields: str) -> list[dict[str, Any]]:
        self._model.probes.append(("editor", _acting.get()))
        row = self._model._row
        who = _acting.get()
        if row is None or who is None or who not in self._model.writers:
            return []
        return [{"id": str(row.id)}]


class _FakeModel:
    """content_ir.kind_instance as RLS shows it: readers see the row, writers may lock it."""

    def __init__(self, row: Any, *, readers: set[str] | None = None, writers: set[str] | None = None):
        self._row = row
        self.readers = readers if readers is not None else set()
        self.writers = writers if writers is not None else set()
        self.updates: list[tuple[dict[str, Any], dict[str, Any]]] = []
        self.probes: list[tuple[str, str | None]] = []
        self.privileged_reads = 0

    async def get_or_none(self, **kwargs: Any) -> Any:
        who = _acting.get()
        if who is None:
            self.privileged_reads += 1
            return self._row
        return self._row if who in self.readers else None

    def filter(self, **pk: Any) -> _Locking:
        return _Locking(self, pk)

    async def update_where(self, where: dict[str, Any], **updates: Any) -> None:
        self.updates.append((where, updates))


@pytest.mark.asyncio
async def test_instance_create_declares_the_agent_tool_actor(
    monkeypatch: pytest.MonkeyPatch, person_session: dict[str, str]
) -> None:
    """The durable write must carry the tool's AI authorship into its transaction."""
    from matrx_orm import current_actor

    user = str(uuid4())
    kind_row = SimpleNamespace(
        id=uuid4(),
        kind="test_kind",
        created_by=user,
        organization_id=uuid4(),
        deleted_at=None,
        version=1,
        emitted_json_schema=None,
        metadata=None,
    )

    async def _resolve(_ref: str, _ctx: ToolContext):
        return kind_row, None

    async def _allow(_row: Any, _ctx: ToolContext):
        return None

    class _CreateRecorder:
        async def create_item(self, **payload: Any) -> Any:
            actor = current_actor()
            assert actor is not None
            assert actor.tier == "ai"
            assert actor.system == "tool:instance_create"
            return SimpleNamespace(id=uuid4())

        async def get_or_none(self, **_kwargs: Any) -> Any:
            return SimpleNamespace(validation_status="passed", title="Saved")

    monkeypatch.setattr(ki, "resolve_kind", _resolve)
    monkeypatch.setattr(ki, "ensure_can_view_kind", _allow)
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    monkeypatch.setattr(ki, "ctx_org_id", lambda _ctx: str(kind_row.organization_id))
    monkeypatch.setattr(ki, "get_db_model", lambda _name: _CreateRecorder())

    result = await ki.instance_create({"kind": "test_kind", "data": {"value": 1}}, make_ctx())
    assert result.success is True


# ---------------------------------------------------------------------------
# Token + summaries + title derivation
# ---------------------------------------------------------------------------


def test_instance_entity_token_is_the_registered_token() -> None:
    assert INSTANCE_ENTITY_TOKEN == "content_ir_kind_instance"


def test_derive_title_explicit_wins_then_titleish_keys() -> None:
    assert derive_title({"title": "From Data"}, "Explicit") == "Explicit"
    assert derive_title({"title": "From Data"}, None) == "From Data"
    assert derive_title({"name": "  Named  "}, None) == "Named"
    assert derive_title({"customer": "Acme Corp", "total": 5}, None) == "Acme Corp"
    assert derive_title({"total": 5}, None) is None
    assert derive_title(["not", "a", "dict"], None) is None
    # empty/whitespace values are skipped, not returned
    assert derive_title({"title": "   ", "name": "Real"}, None) == "Real"


def test_derive_title_metadata_title_key_override() -> None:
    """Per-kind metadata.title_key override — derivation ORDER is the
    cross-repo contract: explicit -> title_key scalar -> shared list -> None
    (mirrored by matrx-frontend instance-title.ts)."""
    # override wins over the shared list
    assert derive_title({"wine_name": "Opus One", "name": "Generic"}, None, "wine_name") == (
        "Opus One"
    )
    # explicit still beats the override
    assert derive_title({"wine_name": "Opus One"}, "Explicit", "wine_name") == "Explicit"
    # non-string scalars stringify (mirror contract: bools lowercase)
    assert derive_title({"vintage": 1997}, None, "vintage") == "1997"
    assert derive_title({"buy_again": True}, None, "buy_again") == "true"
    # absent / empty / non-scalar override falls through to the shared list
    assert derive_title({"name": "Fallback"}, None, "wine_name") == "Fallback"
    assert derive_title({"wine_name": "   ", "name": "Fallback"}, None, "wine_name") == "Fallback"
    assert derive_title({"wine_name": {"nested": 1}, "name": "Fb"}, None, "wine_name") == "Fb"
    assert derive_title({"wine_name": ["list"]}, None, "wine_name") is None


def test_kind_title_key_reads_metadata_defensively() -> None:
    from matrx_ai.tools.implementations.kind_shared import kind_title_key

    assert kind_title_key(SimpleNamespace(metadata={"title_key": "wine_name"})) == "wine_name"
    assert kind_title_key(SimpleNamespace(metadata={"title_key": "  wine_name  "})) == "wine_name"
    assert kind_title_key(SimpleNamespace(metadata={"title_key": "   "})) is None
    assert kind_title_key(SimpleNamespace(metadata={"title_key": 7})) is None
    assert kind_title_key(SimpleNamespace(metadata={})) is None
    assert kind_title_key(SimpleNamespace(metadata=None)) is None
    assert kind_title_key(SimpleNamespace()) is None


def test_instance_summary_projection_is_light() -> None:
    row = _instance_row(str(uuid4()))
    out = instance_summary(row, "invoice")
    assert set(out) == {
        "id",
        "kind_definition_id",
        "title",
        "kind_version",
        "validation_status",
        "updated_at",
        "deleted",
        "kind",
    }
    assert "data" not in out  # payloads only via instance_get


# ---------------------------------------------------------------------------
# Authorization matrix — RLS answers in the caller's session, never app code
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_the_owner_is_decided_by_rls_too(
    monkeypatch: pytest.MonkeyPatch, person_session: dict[str, str]
) -> None:
    """No owner fast path: even the creator's access is the database's answer."""
    user = str(uuid4())
    person_session["user"] = user
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    row = _instance_row(user)
    fake = _FakeModel(row, readers={user}, writers={user})
    monkeypatch.setattr(ki, "get_db_model", lambda _name: fake)
    assert await ki._can_access_instance(row, make_ctx(), "viewer") is True
    assert await ki._can_access_instance(row, make_ctx(), "editor") is True
    assert fake.probes == [("editor", user)]  # the edit question went to the database
    assert fake.privileged_reads == 0


@pytest.mark.asyncio
async def test_a_view_only_share_reads_but_cannot_edit(
    monkeypatch: pytest.MonkeyPatch, person_session: dict[str, str]
) -> None:
    user = str(uuid4())
    person_session["user"] = user
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    shared_view_only = _instance_row(str(uuid4()))
    fake = _FakeModel(shared_view_only, readers={user}, writers=set())
    monkeypatch.setattr(ki, "get_db_model", lambda _name: fake)
    ctx = make_ctx()
    assert await ki._can_access_instance(shared_view_only, ctx, "viewer") is True
    assert await ki._can_access_instance(shared_view_only, ctx, "editor") is False

    stranger = _FakeModel(_instance_row(str(uuid4())))
    monkeypatch.setattr(ki, "get_db_model", lambda _name: stranger)
    assert await ki._can_access_instance(stranger._row, ctx, "viewer") is False
    assert await ki._can_access_instance(stranger._row, ctx, "editor") is False
    assert fake.privileged_reads == 0 and stranger.privileged_reads == 0


@pytest.mark.asyncio
async def test_no_user_or_no_person_session_never_grants(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai import _ext
    from matrx_ai.tools.person_session import PersonSessionUnavailable

    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: None)
    assert await ki._can_access_instance(_instance_row(str(uuid4())), make_ctx(), "viewer") is False

    # No person session configured: the question is refused loudly, never answered privileged.
    monkeypatch.delitem(_ext._registry, "acting_as_caller", raising=False)
    user = str(uuid4())
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    fake = _FakeModel(_instance_row(user))
    monkeypatch.setattr(ki, "get_db_model", lambda _name: fake)
    with pytest.raises(PersonSessionUnavailable):
        await ki._can_access_instance(fake._row, make_ctx(), "viewer")
    assert fake.privileged_reads == 0


# ---------------------------------------------------------------------------
# Content-free denials — missing, deleted, and unauthorized are identical
# ---------------------------------------------------------------------------


def _patch_instance_model(
    monkeypatch: pytest.MonkeyPatch,
    row: Any,
    *,
    readers: set[str] | None = None,
    writers: set[str] | None = None,
) -> _FakeModel:
    fake = _FakeModel(row, readers=readers, writers=writers)
    monkeypatch.setattr(ki, "get_db_model", lambda _name: fake)
    return fake


@pytest.mark.asyncio
async def test_unauthorized_get_is_content_free(
    monkeypatch: pytest.MonkeyPatch, person_session: dict[str, str]
) -> None:
    user = str(uuid4())
    person_session["user"] = user
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    row = _instance_row(str(uuid4()))  # someone else's — RLS returns nothing to this user
    _patch_instance_model(monkeypatch, row)

    result = await ki.instance_get({"instance_id": str(row.id)}, make_ctx())
    assert result.success is False
    assert result.error is not None and result.error.error_type == "not_found"
    blob = (result.error.message or "") + (result.error.suggested_action or "")
    # Nothing about the row leaks through the denial.
    assert "Secret Title" not in blob
    assert "secret" not in blob


@pytest.mark.asyncio
async def test_missing_deleted_and_unauthorized_shapes_match(
    monkeypatch: pytest.MonkeyPatch, person_session: dict[str, str]
) -> None:
    user = str(uuid4())
    person_session["user"] = user
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)

    probe_id = str(uuid4())
    messages: list[str] = []
    for row, readers in (
        (None, {user}),
        (_instance_row(user, deleted_at="2026-07-18T00:00:00Z"), {user}),
        (_instance_row(str(uuid4())), set()),
    ):
        _patch_instance_model(monkeypatch, row, readers=readers)
        result = await ki.instance_get({"instance_id": probe_id}, make_ctx())
        assert result.success is False
        assert result.error is not None and result.error.error_type == "not_found"
        messages.append(result.error.message)
    assert len(set(messages)) == 1  # identical content-free shape
    assert probe_id in messages[0]  # the honest answer names the id it was asked about


@pytest.mark.asyncio
async def test_update_and_delete_are_editor_gated(
    monkeypatch: pytest.MonkeyPatch, person_session: dict[str, str]
) -> None:
    """A viewer-only grant must NOT unlock update/delete — both ask the
    database the edit question (FOR UPDATE) and deny content-free."""
    user = str(uuid4())
    person_session["user"] = user
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    row = _instance_row(str(uuid4()))
    fake = _patch_instance_model(monkeypatch, row, readers={user}, writers=set())  # viewer only

    upd = await ki.instance_update({"instance_id": str(row.id), "title": "hijack"}, make_ctx())
    assert upd.success is False and upd.error.error_type == "not_found"

    dele = await ki.instance_delete({"instance_id": str(row.id)}, make_ctx())
    assert dele.success is False and dele.error.error_type == "not_found"

    assert fake.updates == []  # nothing written
    assert ("editor", user) in fake.probes
    assert fake.privileged_reads == 0


@pytest.mark.asyncio
async def test_create_requires_viewer_on_the_kind(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """instance_create gates on the KIND at viewer level — a kind the caller
    cannot view refuses with the kind tools' content-free denial."""
    kind_row = SimpleNamespace(
        id=uuid4(),
        kind="hidden_kind",
        created_by=str(uuid4()),
        organization_id=uuid4(),
        deleted_at=None,
        version=1,
        emitted_json_schema=None,
    )

    async def _resolve(_ref: str, _ctx: ToolContext):
        return kind_row, None

    from matrx_ai.tools.implementations.kind_shared import err as shared_err

    async def _deny_view(_row: Any, _ctx: ToolContext):
        return shared_err("not_found", "No accessible kind found for the given reference.")

    monkeypatch.setattr(ki, "resolve_kind", _resolve)
    monkeypatch.setattr(ki, "ensure_can_view_kind", _deny_view)
    fake = _patch_instance_model(monkeypatch, None)

    result = await ki.instance_create({"kind": "hidden_kind", "data": {"a": 1}}, make_ctx())
    assert result.success is False
    assert result.error.error_type == "not_found"
    assert fake.updates == []


# ---------------------------------------------------------------------------
# Arg-contract enforcement (extra="forbid" is load-bearing)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_unexpected_argument_raises_model_error() -> None:
    import pydantic

    with pytest.raises(pydantic.ValidationError):
        await ki.instance_get({"instance_id": str(uuid4()), "nope": True}, make_ctx())
    with pytest.raises(pydantic.ValidationError):
        await ki.instance_create(
            {"kind": "x", "data": {}, "validation_status": "passed"}, make_ctx()
        )


@pytest.mark.asyncio
async def test_update_requires_something_to_change(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result = await ki.instance_update({"instance_id": str(uuid4())}, make_ctx())
    assert result.success is False and result.error.error_type == "validation"

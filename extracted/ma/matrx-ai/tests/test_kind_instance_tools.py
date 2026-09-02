"""Unit tests for the ``instance_*`` toolset (saved kind instances).

Pure-logic coverage: the in-code authorization mirror on the INSTANCE token
(owner fast-path, verbatim delegation to ``iam.has_access_for``, fail-closed,
content-free denials), title derivation, and arg-contract enforcement. The
live DB lifecycle (create -> verdict -> list -> update -> repin -> soft-delete
-> revalidate-after-schema-change) is exercised by
``tests_trials/run_kind_tools_e2e.py`` (repo root) against the real database.
"""

from __future__ import annotations

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


class _AccessRecorder:
    """Stand-in for _instance_access_allowed recording delegations and
    answering from a scripted (instance_id, user_id, level) -> bool table."""

    def __init__(self, table: dict[tuple[str, str, str], bool] | None = None):
        self.table = table or {}
        self.calls: list[tuple[str, str, str]] = []

    async def __call__(self, instance_id: str, user_id: str, level: str) -> bool:
        self.calls.append((instance_id, user_id, level))
        return self.table.get((instance_id, user_id, level), False)


class _FakeModel:
    def __init__(self, row: Any):
        self._row = row
        self.updates: list[tuple[dict[str, Any], dict[str, Any]]] = []

    async def get_or_none(self, **kwargs: Any) -> Any:
        return self._row

    async def update_where(self, where: dict[str, Any], **updates: Any) -> None:
        self.updates.append((where, updates))


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
# Authorization matrix — owner fast-path / verbatim delegation / fail-closed
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_owner_passes_without_db_call(monkeypatch: pytest.MonkeyPatch) -> None:
    user = str(uuid4())
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    recorder = _AccessRecorder()
    monkeypatch.setattr(ki, "_instance_access_allowed", recorder)
    row = _instance_row(user)
    assert await ki._can_access_instance(row, make_ctx(), "viewer") is True
    assert await ki._can_access_instance(row, make_ctx(), "editor") is True
    assert recorder.calls == []  # owner never round-trips


@pytest.mark.asyncio
async def test_non_owner_delegates_verbatim_per_level(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A non-owner gets EXACTLY what iam.has_access_for says, per level —
    the code contributes no org/visibility logic of its own."""
    user = str(uuid4())
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    shared_view_only = _instance_row(str(uuid4()))
    stranger_row = _instance_row(str(uuid4()))
    recorder = _AccessRecorder({(str(shared_view_only.id), user, "viewer"): True})
    monkeypatch.setattr(ki, "_instance_access_allowed", recorder)

    ctx = make_ctx()
    assert await ki._can_access_instance(shared_view_only, ctx, "viewer") is True
    assert await ki._can_access_instance(shared_view_only, ctx, "editor") is False
    assert await ki._can_access_instance(stranger_row, ctx, "viewer") is False
    assert await ki._can_access_instance(stranger_row, ctx, "editor") is False
    assert (str(shared_view_only.id), user, "viewer") in recorder.calls
    assert (str(shared_view_only.id), user, "editor") in recorder.calls
    assert (str(stranger_row.id), user, "viewer") in recorder.calls


@pytest.mark.asyncio
async def test_no_user_or_checker_error_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: None)
    assert await ki._can_access_instance(_instance_row(str(uuid4())), make_ctx(), "viewer") is False

    # checker raising -> _instance_access_allowed itself fails closed
    user = str(uuid4())

    async def _boom(*_args: Any, **_kwargs: Any):  # noqa: ANN202
        raise RuntimeError("db down")

    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    monkeypatch.setattr("matrx_orm.call_function", _boom, raising=False)
    assert await ki._instance_access_allowed(str(uuid4()), user, "viewer") is False


# ---------------------------------------------------------------------------
# Content-free denials — missing, deleted, and unauthorized are identical
# ---------------------------------------------------------------------------


def _patch_instance_model(monkeypatch: pytest.MonkeyPatch, row: Any) -> _FakeModel:
    fake = _FakeModel(row)
    monkeypatch.setattr(ki, "get_db_model", lambda _name: fake)
    return fake


@pytest.mark.asyncio
async def test_unauthorized_get_is_content_free(monkeypatch: pytest.MonkeyPatch) -> None:
    user = str(uuid4())
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    monkeypatch.setattr(ki, "_instance_access_allowed", _AccessRecorder())
    row = _instance_row(str(uuid4()))  # someone else's
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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user = str(uuid4())
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    monkeypatch.setattr(ki, "_instance_access_allowed", _AccessRecorder())

    messages: list[str] = []
    for row in (
        None,
        _instance_row(user, deleted_at="2026-07-18T00:00:00Z"),
        _instance_row(str(uuid4())),
    ):
        _patch_instance_model(monkeypatch, row)
        result = await ki.instance_get({"instance_id": str(uuid4())}, make_ctx())
        assert result.success is False
        assert result.error is not None and result.error.error_type == "not_found"
        messages.append(result.error.message)
    assert len(set(messages)) == 1  # identical content-free shape


@pytest.mark.asyncio
async def test_update_and_delete_are_editor_gated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A viewer-only grant must NOT unlock update/delete — both resolve the
    row at editor level and deny content-free."""
    user = str(uuid4())
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    row = _instance_row(str(uuid4()))
    recorder = _AccessRecorder({(str(row.id), user, "viewer"): True})  # viewer only
    monkeypatch.setattr(ki, "_instance_access_allowed", recorder)
    fake = _patch_instance_model(monkeypatch, row)

    upd = await ki.instance_update({"instance_id": str(row.id), "title": "hijack"}, make_ctx())
    assert upd.success is False and upd.error.error_type == "not_found"

    dele = await ki.instance_delete({"instance_id": str(row.id)}, make_ctx())
    assert dele.success is False and dele.error.error_type == "not_found"

    assert fake.updates == []  # nothing written
    assert (str(row.id), user, "editor") in recorder.calls


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

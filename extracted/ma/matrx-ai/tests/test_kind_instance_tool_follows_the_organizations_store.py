"""The ``kind_instance`` tool writes where the ORGANIZATION keeps its kind records.

``content_ir.kind_instance`` is declared superseded by ``custom.record`` (W1-REG). The host
answers, per organization, which store holds kind records (aidream
``services/kind_records/routed.py``) and hands that door to this package as
``kind_record_arm``. These tests pin both arms of every verb:

* an organization whose answer is "the store" never touches ``content_ir.kind_instance`` —
  the legacy model here RAISES if it is reached, so a store-arm call that fell through to
  the old table fails the test instead of passing quietly;
* an organization whose answer is "today's table" never touches the arm's write verbs, and
  runs the legacy body it always ran;
* an unwired host is today's table, for everybody.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai._ext import _registry, configure_ext
from matrx_ai.tools.implementations import kind_instance as ki
from matrx_ai.tools.models import ToolContext

pytestmark = pytest.mark.asyncio

USER = str(uuid4())
ORG = str(uuid4())
KIND_ID = uuid4()


def _ctx() -> ToolContext:
    return ToolContext(call_id=str(uuid4()), tool_name="test")


def _kind(schema: Any = None) -> Any:
    return SimpleNamespace(
        id=KIND_ID,
        kind="wine_tasting",
        created_by=USER,
        organization_id=ORG,
        deleted_at=None,
        version=3,
        emitted_json_schema=schema,
        metadata={"title_key": "wine_name"},
    )


class FakeArm:
    """The host's door, scripted: which store this organization answers, and a record table."""

    def __init__(self, *, store: bool) -> None:
        self.store = store
        self.records: dict[str, dict[str, Any]] = {}
        self.calls: list[tuple[str, dict[str, Any]]] = []

    async def through_the_store(self, *, user_id: str, organization_id: str) -> bool:
        self.calls.append(("route", {"user_id": user_id, "organization_id": organization_id}))
        return self.store

    async def create(self, *, user_id, organization_id, values, system) -> str:
        record_id = str(uuid4())
        self.calls.append(("create", {"values": values, "system": system}))
        self.records[record_id] = {**values, "id": record_id, "updated_at": "2026-09-27T10:00:00Z"}
        return record_id

    async def get(self, *, user_id, organization_id, record_id):
        self.calls.append(("get", {"record_id": record_id}))
        return dict(self.records[record_id]) if record_id in self.records else None

    async def list(self, *, user_id, organization_id, match):
        self.calls.append(("list", {"match": match}))
        return [
            dict(r)
            for r in self.records.values()
            if all(str(r.get(k)) == str(v) for k, v in match.items())
        ]

    async def update(self, *, user_id, organization_id, record_id, values, system):
        self.calls.append(("update", {"record_id": record_id, "values": values, "system": system}))
        self.records[record_id].update(values)

    async def delete(self, *, user_id, organization_id, record_id, system):
        self.calls.append(("delete", {"record_id": record_id, "system": system}))
        self.records[record_id]["deleted_at"] = "2026-09-27T10:05:00Z"
        return {"record_id": record_id, "deleted": True, "applied": True}

    def verbs(self) -> list[str]:
        return [name for name, _ in self.calls]


class LegacyTableUntouchable:
    """``content_ir.kind_instance`` for a store organization: reaching it is the defect."""

    def __getattr__(self, name: str) -> Any:
        raise AssertionError(
            f"the store organization's call reached content_ir.kind_instance.{name} — "
            "the tool wrote or read the table this organization no longer reads"
        )


class LegacyTable:
    """``content_ir.kind_instance`` for a legacy organization: records what the old body did."""

    def __init__(self) -> None:
        self.created: list[dict[str, Any]] = []
        self.rows: dict[str, Any] = {}
        self.updates: list[tuple[dict[str, Any], dict[str, Any]]] = []

    async def create_item(self, **payload: Any) -> Any:
        row = SimpleNamespace(
            id=uuid4(),
            validation_status="passed",
            updated_at=None,
            deleted_at=None,
            **payload,
        )
        self.created.append(payload)
        self.rows[str(row.id)] = row
        return row

    async def get_or_none(self, **kwargs: Any) -> Any:
        return self.rows.get(str(kwargs.get("id")))

    def filter(self, **filters: Any) -> Any:
        rows = [
            r
            for r in self.rows.values()
            if all(str(getattr(r, k)) == str(v) for k, v in filters.items())
        ]

        class _Q:
            async def all(self_inner) -> list[Any]:
                return rows

            def select_for_update(self_inner) -> Any:
                # The edit question (FOR UPDATE under the person's RLS): this
                # organization's own rows are editable by their creator here.
                return self_inner

            async def values(self_inner, *_fields: str) -> list[dict[str, Any]]:
                return [{"id": str(r.id)} for r in rows]

        return _Q()

    async def update_where(self, where: dict[str, Any], **updates: Any) -> Any:
        self.updates.append((where, updates))
        row = self.rows[str(where["id"])]
        for key, value in updates.items():
            setattr(row, key, value)
        return SimpleNamespace(rows_affected=1, updated_rows=[vars(row)])


@pytest.fixture
def wired(monkeypatch: pytest.MonkeyPatch):
    """Register an arm the way ``aidream/package_integration.py`` does, and put it back after."""
    before = _registry.pop(ki.KIND_RECORD_ARM_EXT_KEY, None)

    def install(arm: Any, legacy: Any) -> None:
        configure_ext(**{ki.KIND_RECORD_ARM_EXT_KEY: arm})

        @contextlib.asynccontextmanager
        async def acting_as_caller():  # the host's person seam (RLS decides in it)
            yield

        monkeypatch.setitem(_registry, "acting_as_caller", acting_as_caller)

        async def _resolve(_ref: str, _ctx: ToolContext):
            return _kind(), None

        async def _allow(_row: Any, _ctx: ToolContext):
            return None

        kinds = SimpleNamespace(get_or_none=_kind_get)
        monkeypatch.setattr(ki, "resolve_kind", _resolve)
        monkeypatch.setattr(ki, "ensure_can_view_kind", _allow)
        monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: USER)
        monkeypatch.setattr(ki, "ctx_org_id", lambda _ctx: ORG)
        monkeypatch.setattr(
            ki,
            "get_db_model",
            lambda name: kinds if name == "KindDefinition" else legacy,
        )

    yield install
    _registry.pop(ki.KIND_RECORD_ARM_EXT_KEY, None)
    if before is not None:
        _registry[ki.KIND_RECORD_ARM_EXT_KEY] = before


async def _kind_get(**_kwargs: Any) -> Any:
    return _kind()


async def test_a_store_organization_creates_and_lists_through_the_store(wired) -> None:
    arm = FakeArm(store=True)
    wired(arm, LegacyTableUntouchable())

    made = await ki.instance_create(
        {"kind": "wine_tasting", "data": {"wine_name": "Ridge Monte Bello 2019"}}, _ctx()
    )
    assert made.success is True, made.error
    receipt = made.output
    assert receipt.instance_id in arm.records
    assert receipt.title == "Ridge Monte Bello 2019"
    create = next(payload for name, payload in arm.calls if name == "create")
    assert create["system"] == "tool:instance_create"
    values = create["values"]
    assert values["organization_id"] == ORG and values["created_by"] == USER
    assert values["kind_definition_id"] == str(KIND_ID) and values["kind_version"] == 3
    assert values["data"]["__kind"] == "wine_tasting"
    # No schema on this kind: the verdict is said, never promoted to "passed".
    assert values["validation_status"] == "pending" == receipt.validation_status

    listed = await ki.instance_list({}, _ctx())
    assert listed.success is True, listed.error
    assert [i.id for i in listed.output.instances] == [receipt.instance_id]
    assert listed.output.instances[0].kind == "wine_tasting"
    match = next(payload for name, payload in arm.calls if name == "list")["match"]
    assert match == {"created_by": USER}


async def test_a_store_organization_gets_updates_and_deletes_through_the_store(wired) -> None:
    arm = FakeArm(store=True)
    wired(arm, LegacyTableUntouchable())
    made = await ki.instance_create(
        {"kind": "wine_tasting", "data": {"wine_name": "Ridge Monte Bello 2019"}}, _ctx()
    )
    record_id = made.output.instance_id

    got = await ki.instance_get({"instance_id": record_id}, _ctx())
    assert got.success is True, got.error
    assert got.output.instance.data["wine_name"] == "Ridge Monte Bello 2019"

    changed = await ki.instance_update(
        {"instance_id": record_id, "data": {"wine_name": "Ridge Lytton Springs 2021"}}, _ctx()
    )
    assert changed.success is True, changed.error
    update = next(payload for name, payload in arm.calls if name == "update")
    assert update["system"] == "tool:instance_update"
    assert "updated_by" not in update["values"]
    assert update["values"]["title"] == "Ridge Lytton Springs 2021"
    assert changed.output.title == "Ridge Lytton Springs 2021"

    gone = await ki.instance_delete({"instance_id": record_id}, _ctx())
    assert gone.success is True and gone.output.deleted is True
    assert ("delete", {"record_id": record_id, "system": "tool:instance_delete"}) in arm.calls

    again = await ki.instance_get({"instance_id": record_id}, _ctx())
    assert again.success is False and again.error.error_type == "not_found"


async def test_a_held_store_delete_says_it_was_not_done(wired) -> None:
    arm = FakeArm(store=True)

    async def held(**kwargs: Any) -> dict[str, Any]:
        return {"record_id": kwargs["record_id"], "applied": False}

    wired(arm, LegacyTableUntouchable())
    made = await ki.instance_create({"kind": "wine_tasting", "data": {"wine_name": "x"}}, _ctx())
    arm.delete = held  # type: ignore[method-assign]
    gone = await ki.instance_delete({"instance_id": made.output.instance_id}, _ctx())
    assert gone.success is True
    assert gone.output.deleted is False
    assert "HELD FOR APPROVAL" in gone.output.message


async def test_a_legacy_organization_creates_and_lists_on_todays_table(wired) -> None:
    arm = FakeArm(store=False)
    legacy = LegacyTable()
    wired(arm, legacy)

    made = await ki.instance_create(
        {"kind": "wine_tasting", "data": {"wine_name": "Ridge Monte Bello 2019"}}, _ctx()
    )
    assert made.success is True, made.error
    assert len(legacy.created) == 1
    assert legacy.created[0]["organization_id"] == ORG
    assert "validation_status" not in legacy.created[0]  # the trigger derives it on this arm

    listed = await ki.instance_list({}, _ctx())
    assert listed.success is True, listed.error
    assert [i.id for i in listed.output.instances] == [made.output.instance_id]

    changed = await ki.instance_update(
        {"instance_id": made.output.instance_id, "title": "Monte Bello"}, _ctx()
    )
    assert changed.success is True, changed.error
    assert legacy.updates and legacy.updates[0][1]["updated_by"] == USER

    assert set(arm.verbs()) == {"route"}, arm.verbs()


async def test_an_unwired_host_is_todays_table(wired, monkeypatch: pytest.MonkeyPatch) -> None:
    legacy = LegacyTable()
    wired(FakeArm(store=True), legacy)
    _registry.pop(ki.KIND_RECORD_ARM_EXT_KEY, None)
    made = await ki.instance_create({"kind": "wine_tasting", "data": {"wine_name": "x"}}, _ctx())
    assert made.success is True, made.error
    assert len(legacy.created) == 1

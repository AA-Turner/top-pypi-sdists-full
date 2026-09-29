"""`picklist` reads a list only when the PERSON's database session can see it.

Defect (2026-09-27): ``picklist action=get`` (``picklists_get`` + ``picklists_get_items``)
and the update receipt's prior read (``picklists_get_items`` by ``list_id``) ran on the
privileged connection with no access decision at all, so anyone who named a list id
read every choice in it. Chair ruling: RLS owns access. Before a list's contents are
read, the caller's own RLS session (``as_the_person`` → host ``acting_as_caller``) is
asked whether ``workbench.udt_structured_lists`` holds that row for them. A hidden list
answers ``not_found`` naming its id; a list that lives in the record store answers an
honest ``unavailable``, never a privileged read.

Scenario: a dental practice. Dana (front-desk lead) keeps the list "Accepted insurance
plans"; Leo, at a different practice, must not read it through his agent.
"""

from __future__ import annotations

import contextlib
from contextvars import ContextVar
from types import SimpleNamespace
from typing import Any

import pytest

DANA = "d4e5f6a7-0000-4000-8000-00000000a001"
LEO = "d4e5f6a7-0000-4000-8000-00000000b002"
LIST_ID = "e1f2a3b4-0000-4000-8000-000000000001"
STORE_LIST_ID = "e1f2a3b4-0000-4000-8000-000000000002"
DELTA = "e1f2a3b4-0000-4000-8000-0000000000d1"

_acting: ContextVar[str | None] = ContextVar("fake_acting_user_lists", default=None)


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch):
    import matrx_orm.sql_executor as sx

    from matrx_ai import _ext
    from matrx_ai.db import _registry
    from matrx_ai.tools.implementations import picklists_tools

    bag: dict[str, Any] = {"privileged_reads": [], "violations": [], "list_readers": {LIST_ID: {DANA}}}

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        from matrx_connect.context.app_context import get_app_context

        token = _acting.set(get_app_context().user_id)
        try:
            yield
        finally:
            _acting.reset(token)

    monkeypatch.setitem(_ext._registry, "acting_as_caller", acting_as_caller)

    class Lists:
        @staticmethod
        async def get_or_none(use_cache: bool = True, **pk: Any):
            who = _acting.get()
            if who is None:
                bag["violations"].append("list gate ran on the privileged connection")
            if use_cache:
                bag["violations"].append("list gate read through the identity-blind cache")
            lid = pk.get("id")
            return (
                SimpleNamespace(id=lid, deleted_at=None, list_name="Accepted insurance plans",
                                description=None, user_id=DANA, organization_id=None,
                                is_public=False, public_read=False, created_at=None, updated_at=None)
                if who in bag["list_readers"].get(lid, set())
                else None
            )

    monkeypatch.setitem(_registry._models, "UdtStructuredLists", Lists)

    bag["choice"] = {"id": DELTA, "label": "Delta Dental PPO", "list_id": LIST_ID}
    bag["choice_writers"] = {DANA}

    class Items:
        """workbench.udt_structured_list_items under RLS: editors of the list may change it."""

        @staticmethod
        async def update_where(where: dict[str, Any], **values: Any) -> Any:
            who = _acting.get()
            if who is None:
                bag["violations"].append("choice write ran on the privileged connection")
            if where.get("id") != DELTA or who not in bag["choice_writers"]:
                return SimpleNamespace(rows_affected=0, updated_rows=[])
            bag["choice"].update(values)
            return SimpleNamespace(rows_affected=1, updated_rows=[dict(bag["choice"])])

        @staticmethod
        async def get_or_none(use_cache: bool = True, **pk: Any) -> Any:
            who = _acting.get()
            return SimpleNamespace(**bag["choice"]) if who in bag["list_readers"].get(LIST_ID, set()) else None

        @staticmethod
        def filter(**f: Any) -> Any:
            who = _acting.get()
            if who is None:
                bag["violations"].append("choices read on the privileged connection")
            visible = who in bag["list_readers"].get(LIST_ID, set()) and f.get("list_id") == LIST_ID
            row = SimpleNamespace(description="in network", help_text=None, group_name="PPO",
                                  icon_name=None, created_at=None, deleted_at=None, **bag["choice"])

            class _Q:
                async def all(self) -> list[Any]:
                    return [row] if visible else []

            return _Q()

    monkeypatch.setitem(_registry._models, "UdtStructuredListItems", Items)

    def execute_standard_query(name, params):
        bag["privileged_reads"].append((name, params))
        if name == "picklists_get":
            return [{"id": params["list_id"], "list_name": "Accepted insurance plans", "user_id": DANA}]
        if name == "picklists_get_items":
            return [{"id": DELTA, "label": "Delta Dental PPO", "description": "in network", "help_text": None,
                     "group_name": "PPO", "icon_name": None}]
        if name == "picklists_item_home":
            return [{"id": params["item_id"], "list_id": LIST_ID, "lives_in": "older"}]
        if name == "picklists_update_item":
            bag["violations"].append("choice written by the privileged owner-filtered query")
            return [{"id": params["item_id"]}]
        raise AssertionError(name)

    monkeypatch.setattr(sx, "execute_standard_query", execute_standard_query)

    bag["store_readers"] = {DANA}

    class Arm:
        """The host's record-store arm: the STORE decides who sees a moved list."""

        async def list_lives_in(self, list_id: str) -> str:
            return "record" if list_id == STORE_LIST_ID else "older"

        async def read_list(self, list_id: str) -> Any:
            from matrx_connect.context.app_context import get_app_context

            bag["store_reads"] = bag.get("store_reads", 0) + 1
            if list_id != STORE_LIST_ID or get_app_context().user_id not in bag["store_readers"]:
                return None
            return {"id": STORE_LIST_ID, "list_name": "Visit types", "description": None,
                    "user_id": DANA, "organization_id": None, "is_public": False, "public_read": False,
                    "created_at": None, "updated_at": None, "lives_in": "record", "item_count": 1,
                    "items": [{"id": "visit-1", "label": "Cleaning", "description": None,
                               "help_text": None, "group_name": None, "icon_name": None}]}

    arm = Arm()
    monkeypatch.setattr(picklists_tools, "_picklist_store_arm", lambda: arm)
    monkeypatch.setitem(_ext._registry, "picklist_store_arm", arm)
    return bag


async def _picklist(user: str, args: dict[str, Any]):
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    from matrx_ai.tools.implementations.picklists_tools import picklist
    from matrx_ai.tools.models import ToolContext

    token = set_app_context(AppContext(emitter=None, user_id=user))
    try:
        return await picklist(args, ToolContext(call_id="call-plans"))
    finally:
        clear_app_context(token)


def _contents_read(bag: dict[str, Any]) -> list[str]:
    return [name for name, _ in bag["privileged_reads"] if name in ("picklists_get", "picklists_get_items")]


@pytest.mark.asyncio
async def test_the_owner_reads_her_list(world):
    result = await _picklist(DANA, {"action": "get", "picklist_id": LIST_ID})
    assert result.success, result.error
    assert result.output["items"][0]["label"] == "Delta Dental PPO"
    assert world["violations"] == [], world["violations"]


@pytest.mark.asyncio
async def test_an_outsider_cannot_read_the_list_and_is_told_so_by_id(world):
    result = await _picklist(LEO, {"action": "get", "picklist_id": LIST_ID})
    assert not result.success
    assert result.error.error_type == "not_found"
    assert LIST_ID in result.error.message
    assert _contents_read(world) == [], "the list's contents were read for someone RLS hides it from"
    assert world["violations"] == [], world["violations"]


@pytest.mark.asyncio
async def test_an_outsiders_update_never_carries_a_receipt_of_the_list(world):
    result = await _picklist(LEO, {"action": "update_item", "item_id": DELTA, "label": "Delta (dropped)"})
    assert not result.success, "an update that changed nothing reported success"
    assert DELTA in result.error.message
    assert getattr(result, "surface_write", None) is None, "a receipt showed a list the person cannot open"
    assert _contents_read(world) == []
    assert world["violations"] == [], world["violations"]


@pytest.mark.asyncio
async def test_a_list_in_the_record_store_is_read_through_the_store_as_the_person(world):
    result = await _picklist(DANA, {"action": "get", "picklist_id": STORE_LIST_ID})
    assert result.success, result.error
    assert [i["label"] for i in result.output["items"]] == ["Cleaning"]
    assert _contents_read(world) == [], "a moved list was read through the privileged views"

    hidden = await _picklist(LEO, {"action": "get", "picklist_id": STORE_LIST_ID})
    assert not hidden.success and hidden.error.error_type == "not_found"
    assert STORE_LIST_ID in hidden.error.message
    assert world["violations"] == [], world["violations"]


@pytest.mark.asyncio
async def test_without_a_person_session_nothing_is_read(world, monkeypatch):
    from matrx_ai import _ext

    monkeypatch.delitem(_ext._registry, "acting_as_caller", raising=False)
    result = await _picklist(DANA, {"action": "get", "picklist_id": LIST_ID})
    assert not result.success
    assert result.error.error_type == "unavailable", result.error
    assert _contents_read(world) == []


@pytest.mark.asyncio
async def test_the_lists_editor_changes_a_choice_in_her_session(world):
    result = await _picklist(DANA, {"action": "update_item", "item_id": DELTA, "label": "Delta Dental PPO Plus"})
    assert result.success, result.error
    assert world["choice"]["label"] == "Delta Dental PPO Plus"
    assert world["violations"] == [], world["violations"]


@pytest.mark.asyncio
async def test_a_shared_editor_who_is_not_the_creator_may_change_it(world):
    """RLS decides, not `user_id = caller`: a teammate the list is shared with at editor may edit."""
    world["list_readers"][LIST_ID].add(LEO)
    world["choice_writers"].add(LEO)
    result = await _picklist(LEO, {"action": "update_item", "item_id": DELTA, "label": "Delta (in network)"})
    assert result.success, result.error
    assert world["choice"]["label"] == "Delta (in network)"
    assert world["violations"] == [], world["violations"]


@pytest.mark.asyncio
async def test_a_viewer_gets_no_access_naming_the_choice(world):
    world["list_readers"][LIST_ID].add(LEO)
    result = await _picklist(LEO, {"action": "update_item", "item_id": DELTA, "label": "Dropped"})
    assert not result.success
    assert result.error.error_type == "no_access"
    assert DELTA in result.error.message
    assert world["choice"]["label"] == "Delta Dental PPO"
    assert world["violations"] == [], world["violations"]

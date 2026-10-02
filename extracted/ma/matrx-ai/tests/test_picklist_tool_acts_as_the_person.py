"""`picklist` reads and changes a list only as the PERSON — the record store decides.

Every list lives in the record store; the tool asks the host's store arm, which runs each
door in the operating person's own seat. A list the store hides answers ``not_found`` naming
its id, a change the store refuses answers ``no_access`` naming the choice, and neither ever
carries a receipt of a list the person cannot open. A host without the arm is refused by name.

Scenario: a dental practice. Dana (front-desk lead) keeps the list "Accepted insurance
plans"; Leo, at a different practice, must not read or change it through his agent.
"""

from __future__ import annotations

from typing import Any

import pytest

DANA = "d4e5f6a7-0000-4000-8000-00000000a001"
LEO = "d4e5f6a7-0000-4000-8000-00000000b002"
LIST_ID = "e1f2a3b4-0000-4000-8000-000000000001"
DELTA = "e1f2a3b4-0000-4000-8000-0000000000d1"
ORG = "e1f2a3b4-0000-4000-8000-0000000000aa"


class StoreRefusal(Exception):
    """The store's refusal, as matrx_records raises it (name and sqlstate are the contract)."""

    def __init__(self, message: str, sqlstate: str) -> None:
        super().__init__(message)
        self.sqlstate = sqlstate


def _who() -> str:
    from matrx_connect.context.app_context import get_app_context

    return str(get_app_context().user_id)


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch):
    from matrx_ai.tools.implementations import picklists_tools

    bag: dict[str, Any] = {
        "readers": {DANA},
        "editors": {DANA},
        "choice": {"id": DELTA, "label": "Delta Dental PPO", "description": None,
                   "help_text": None, "group_name": "PPO", "icon_name": None},
    }

    class Arm:
        async def list_index(self) -> list[dict[str, Any]]:
            if _who() not in bag["readers"]:
                return []
            return [{"id": LIST_ID, "list_name": "Accepted insurance plans", "description": None,
                     "created_by": DANA, "organization_id": ORG, "updated_at": "2026-09-27",
                     "item_count": 1}]

        async def read_list(self, list_id: str) -> dict[str, Any] | None:
            if list_id != LIST_ID or _who() not in bag["readers"]:
                return None
            return {"id": LIST_ID, "list_name": "Accepted insurance plans",
                    "items": [dict(bag["choice"])]}

        async def list_of_choice(self, item_id: str) -> str | None:
            return LIST_ID if item_id == DELTA else None

        async def update_choice(self, item_id: str, fields: dict[str, Any]) -> dict[str, Any]:
            if _who() not in bag["editors"]:
                raise StoreRefusal(f"You may not change choice {item_id}; nothing was changed.", "42501")
            bag["choice"].update({k: v for k, v in fields.items() if v is not None})
            return {"item_id": item_id}

    monkeypatch.setattr(picklists_tools, "_picklist_store_arm", lambda: Arm())
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


@pytest.mark.asyncio
async def test_the_owner_reads_her_list(world):
    result = await _picklist(DANA, {"action": "get", "picklist_id": LIST_ID})
    assert result.success, result.error
    assert result.output["items"][0]["label"] == "Delta Dental PPO"


@pytest.mark.asyncio
async def test_an_outsider_cannot_read_the_list_and_is_told_so_by_id(world):
    result = await _picklist(LEO, {"action": "get", "picklist_id": LIST_ID})
    assert not result.success
    assert result.error.error_type == "not_found"
    assert LIST_ID in result.error.message


@pytest.mark.asyncio
async def test_the_list_index_answers_only_what_the_store_shows(world):
    mine = await _picklist(DANA, {"action": "list"})
    assert [r["id"] for r in mine.output["lists"]] == [LIST_ID]
    theirs = await _picklist(LEO, {"action": "list"})
    assert theirs.output["lists"] == []


@pytest.mark.asyncio
async def test_an_outsiders_update_is_refused_and_carries_no_receipt(world):
    result = await _picklist(LEO, {"action": "update_item", "item_id": DELTA, "label": "Delta (dropped)"})
    assert not result.success, "an update that changed nothing reported success"
    assert result.error.error_type == "no_access"
    assert DELTA in result.error.message
    assert getattr(result, "surface_write", None) is None, "a receipt showed a list the person cannot open"
    assert world["choice"]["label"] == "Delta Dental PPO"


@pytest.mark.asyncio
async def test_the_lists_editor_changes_a_choice(world):
    result = await _picklist(DANA, {"action": "update_item", "item_id": DELTA, "label": "Delta Dental PPO Plus"})
    assert result.success, result.error
    assert world["choice"]["label"] == "Delta Dental PPO Plus"


@pytest.mark.asyncio
async def test_a_shared_editor_who_is_not_the_creator_may_change_it(world):
    """The store decides, not `created_by = caller`: a teammate it lets edit may edit."""
    world["readers"].add(LEO)
    world["editors"].add(LEO)
    result = await _picklist(LEO, {"action": "update_item", "item_id": DELTA, "label": "Delta (in network)"})
    assert result.success, result.error
    assert world["choice"]["label"] == "Delta (in network)"


@pytest.mark.asyncio
async def test_an_unwired_host_is_refused_by_name(monkeypatch):
    from matrx_ai import _ext

    monkeypatch.delitem(_ext._registry, "picklist_store_arm", raising=False)
    result = await _picklist(DANA, {"action": "get", "picklist_id": LIST_ID})
    assert not result.success
    assert result.error.error_type == "unavailable"
    assert "picklist_store_arm" in result.error.message

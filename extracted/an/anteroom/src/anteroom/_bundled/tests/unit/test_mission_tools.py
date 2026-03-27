"""Tests for mission tools — conversational steering."""

from __future__ import annotations

import json
import sqlite3
from unittest.mock import AsyncMock

import pytest

from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services import mission_storage
from anteroom.tools import ToolRegistry, register_default_tools, register_mission_tools
from anteroom.tools.mission import (
    MISSION_TOOL_DEFINITIONS,
    MISSION_TOOL_HANDLERS,
    handle_mission_add_item,
    handle_mission_complete,
    handle_mission_drop_item,
    handle_mission_explain_blockers,
    handle_mission_hold,
    handle_mission_list,
    handle_mission_patch_plan,
    handle_mission_reprioritize,
    handle_mission_resume,
    handle_mission_status,
)
from anteroom.tools.tiers import DEFAULT_TOOL_TIERS, ToolTier


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


@pytest.fixture()
def session(db: ThreadSafeConnection) -> dict:
    return mission_storage.create_session(db, title="Test Mission", status="active")


@pytest.fixture()
def item(db: ThreadSafeConnection, session: dict) -> dict:
    return mission_storage.create_item(db, session_id=session["id"], summary="Task A", priority=30)


# ---------------------------------------------------------------------------
# Registration tests
# ---------------------------------------------------------------------------


class TestRegistration:
    def test_register_mission_tools_registers_all_10(self) -> None:
        registry = ToolRegistry()
        register_mission_tools(registry)
        tools = registry.list_tools()
        assert len(tools) == 10
        for defn in MISSION_TOOL_DEFINITIONS:
            assert defn["name"] in tools

    def test_register_default_tools_does_not_include_mission(self) -> None:
        registry = ToolRegistry()
        register_default_tools(registry)
        tools = registry.list_tools()
        for defn in MISSION_TOOL_DEFINITIONS:
            assert defn["name"] not in tools

    def test_definitions_count(self) -> None:
        assert len(MISSION_TOOL_DEFINITIONS) == 10

    def test_handlers_count(self) -> None:
        assert len(MISSION_TOOL_HANDLERS) == 10

    def test_all_definitions_have_handlers(self) -> None:
        for defn in MISSION_TOOL_DEFINITIONS:
            assert defn["name"] in MISSION_TOOL_HANDLERS


# ---------------------------------------------------------------------------
# Tier assignment tests
# ---------------------------------------------------------------------------


class TestTiers:
    def test_read_tools_are_read_tier(self) -> None:
        for name in ("mission_list", "mission_status", "mission_explain_blockers"):
            assert DEFAULT_TOOL_TIERS[name] == ToolTier.READ

    def test_write_tools_are_write_tier(self) -> None:
        for name in (
            "mission_add_item",
            "mission_hold",
            "mission_resume",
            "mission_reprioritize",
            "mission_drop_item",
            "mission_complete",
        ):
            assert DEFAULT_TOOL_TIERS[name] == ToolTier.WRITE

    def test_patch_plan_is_execute_tier(self) -> None:
        assert DEFAULT_TOOL_TIERS["mission_patch_plan"] == ToolTier.EXECUTE


# ---------------------------------------------------------------------------
# Read tool tests
# ---------------------------------------------------------------------------


class TestMissionList:
    @pytest.mark.asyncio
    async def test_list_empty(self, db: ThreadSafeConnection) -> None:
        result = await handle_mission_list(_db=db)
        assert result["count"] == 0
        assert result["sessions"] == []

    @pytest.mark.asyncio
    async def test_list_returns_sessions(self, db: ThreadSafeConnection, session: dict) -> None:
        result = await handle_mission_list(_db=db)
        assert result["count"] == 1
        assert result["sessions"][0]["id"] == session["id"]

    @pytest.mark.asyncio
    async def test_list_filter_by_status(self, db: ThreadSafeConnection, session: dict) -> None:
        mission_storage.create_session(db, title="Pending", status="pending")
        result = await handle_mission_list(status="active", _db=db)
        assert result["count"] == 1
        assert result["sessions"][0]["status"] == "active"

    @pytest.mark.asyncio
    async def test_list_no_db(self) -> None:
        result = await handle_mission_list()
        assert "error" in result


class TestMissionStatus:
    @pytest.mark.asyncio
    async def test_status_with_items(self, db: ThreadSafeConnection, session: dict, item: dict) -> None:
        result = await handle_mission_status(session_id=session["id"], _db=db)
        assert result["session"]["id"] == session["id"]
        assert result["total_items"] == 1
        assert result["items"][0]["summary"] == "Task A"
        assert "pending" in result["progress"]

    @pytest.mark.asyncio
    async def test_status_session_not_found(self, db: ThreadSafeConnection) -> None:
        result = await handle_mission_status(session_id="nonexistent", _db=db)
        assert "error" in result

    @pytest.mark.asyncio
    async def test_status_no_db(self) -> None:
        result = await handle_mission_status(session_id="x")
        assert "error" in result


class TestMissionExplainBlockers:
    @pytest.mark.asyncio
    async def test_explain_pending_item_no_deps(self, db: ThreadSafeConnection, session: dict, item: dict) -> None:
        result = await handle_mission_explain_blockers(session_id=session["id"], _db=db)
        assert result["count"] == 1
        exp = result["explanations"][0]
        assert exp["item_id"] == item["id"]
        assert len(exp["incomplete_dependencies"]) == 0

    @pytest.mark.asyncio
    async def test_explain_blocked_by_dependency(self, db: ThreadSafeConnection, session: dict) -> None:
        item_a = mission_storage.create_item(db, session_id=session["id"], summary="A")
        item_b = mission_storage.create_item(db, session_id=session["id"], summary="B")
        mission_storage.add_dependency(db, item_id=item_b["id"], depends_on_id=item_a["id"])
        result = await handle_mission_explain_blockers(session_id=session["id"], item_id=item_b["id"], _db=db)
        assert result["count"] == 1
        exp = result["explanations"][0]
        assert len(exp["incomplete_dependencies"]) == 1
        assert exp["incomplete_dependencies"][0]["id"] == item_a["id"]

    @pytest.mark.asyncio
    async def test_explain_held_item(self, db: ThreadSafeConnection, session: dict) -> None:
        item_h = mission_storage.create_item(db, session_id=session["id"], summary="Held", hold_requested=True)
        result = await handle_mission_explain_blockers(session_id=session["id"], item_id=item_h["id"], _db=db)
        assert result["explanations"][0]["hold_requested"] is True
        assert "on hold" in result["explanations"][0]["reasons"][0]

    @pytest.mark.asyncio
    async def test_explain_session_not_found(self, db: ThreadSafeConnection) -> None:
        result = await handle_mission_explain_blockers(session_id="bad", _db=db)
        assert "error" in result

    @pytest.mark.asyncio
    async def test_explain_item_not_found(self, db: ThreadSafeConnection, session: dict) -> None:
        result = await handle_mission_explain_blockers(session_id=session["id"], item_id="bad", _db=db)
        assert "error" in result


# ---------------------------------------------------------------------------
# Mutation tool tests
# ---------------------------------------------------------------------------


class TestMissionAddItem:
    @pytest.mark.asyncio
    async def test_add_item_creates_item(self, db: ThreadSafeConnection, session: dict) -> None:
        result = await handle_mission_add_item(session_id=session["id"], summary="New Task", priority=10, _db=db)
        assert "item" in result
        assert result["item"]["summary"] == "New Task"
        assert result["item"]["priority"] == 10
        items = mission_storage.list_items_by_session(db, session["id"])
        assert any(i["summary"] == "New Task" for i in items)

    @pytest.mark.asyncio
    async def test_add_item_creates_revision(self, db: ThreadSafeConnection, session: dict) -> None:
        await handle_mission_add_item(session_id=session["id"], summary="Rev Test", _db=db)
        revisions = mission_storage.list_revisions(db, session["id"])
        assert len(revisions) == 1
        assert revisions[0]["operations"][0]["op"] == "add_item"

    @pytest.mark.asyncio
    async def test_add_item_with_dependencies(self, db: ThreadSafeConnection, session: dict, item: dict) -> None:
        result = await handle_mission_add_item(
            session_id=session["id"],
            summary="Depends on A",
            depends_on=[item["id"]],
            _db=db,
        )
        new_id = result["item"]["id"]
        deps = mission_storage.get_dependencies(db, new_id)
        assert item["id"] in deps

    @pytest.mark.asyncio
    async def test_add_item_session_not_found(self, db: ThreadSafeConnection) -> None:
        result = await handle_mission_add_item(session_id="bad", summary="x", _db=db)
        assert "error" in result


class TestMissionHold:
    @pytest.mark.asyncio
    async def test_hold_sets_hold_requested(self, db: ThreadSafeConnection, session: dict, item: dict) -> None:
        result = await handle_mission_hold(session_id=session["id"], item_id=item["id"], _db=db)
        assert result["hold_requested"] is True
        updated = mission_storage.get_item(db, item["id"])
        assert updated is not None
        assert updated["hold_requested"] == 1

    @pytest.mark.asyncio
    async def test_hold_creates_revision(self, db: ThreadSafeConnection, session: dict, item: dict) -> None:
        await handle_mission_hold(session_id=session["id"], item_id=item["id"], _db=db)
        revisions = mission_storage.list_revisions(db, session["id"])
        assert len(revisions) == 1

    @pytest.mark.asyncio
    async def test_hold_item_not_found(self, db: ThreadSafeConnection, session: dict) -> None:
        result = await handle_mission_hold(session_id=session["id"], item_id="bad", _db=db)
        assert "error" in result


class TestMissionResume:
    @pytest.mark.asyncio
    async def test_resume_clears_hold(self, db: ThreadSafeConnection, session: dict) -> None:
        held = mission_storage.create_item(db, session_id=session["id"], summary="Held", hold_requested=True)
        result = await handle_mission_resume(session_id=session["id"], item_id=held["id"], _db=db)
        assert result["hold_requested"] is False
        updated = mission_storage.get_item(db, held["id"])
        assert updated is not None
        assert updated["hold_requested"] == 0

    @pytest.mark.asyncio
    async def test_resume_creates_revision(self, db: ThreadSafeConnection, session: dict, item: dict) -> None:
        await handle_mission_resume(session_id=session["id"], item_id=item["id"], _db=db)
        revisions = mission_storage.list_revisions(db, session["id"])
        assert len(revisions) == 1


class TestMissionReprioritize:
    @pytest.mark.asyncio
    async def test_reprioritize_changes_priority(self, db: ThreadSafeConnection, session: dict, item: dict) -> None:
        result = await handle_mission_reprioritize(session_id=session["id"], item_id=item["id"], priority=5, _db=db)
        assert result["old_priority"] == 30
        assert result["new_priority"] == 5
        updated = mission_storage.get_item(db, item["id"])
        assert updated is not None
        assert updated["priority"] == 5

    @pytest.mark.asyncio
    async def test_reprioritize_creates_revision(self, db: ThreadSafeConnection, session: dict, item: dict) -> None:
        await handle_mission_reprioritize(session_id=session["id"], item_id=item["id"], priority=99, _db=db)
        revisions = mission_storage.list_revisions(db, session["id"])
        assert len(revisions) == 1
        assert revisions[0]["operations"][0]["op"] == "reprioritize"


class TestMissionDropItem:
    @pytest.mark.asyncio
    async def test_drop_sets_status_dropped(self, db: ThreadSafeConnection, session: dict, item: dict) -> None:
        result = await handle_mission_drop_item(session_id=session["id"], item_id=item["id"], _db=db)
        assert result["status"] == "dropped"
        updated = mission_storage.get_item(db, item["id"])
        assert updated is not None
        assert updated["status"] == "dropped"

    @pytest.mark.asyncio
    async def test_drop_with_reason_creates_revision(self, db: ThreadSafeConnection, session: dict, item: dict) -> None:
        await handle_mission_drop_item(
            session_id=session["id"],
            item_id=item["id"],
            reason="No longer needed",
            _db=db,
        )
        revisions = mission_storage.list_revisions(db, session["id"])
        assert len(revisions) == 1
        assert revisions[0]["reason"] == "No longer needed"

    @pytest.mark.asyncio
    async def test_drop_item_not_found(self, db: ThreadSafeConnection, session: dict) -> None:
        result = await handle_mission_drop_item(session_id=session["id"], item_id="bad", _db=db)
        assert "error" in result


class TestMissionComplete:
    @pytest.mark.asyncio
    async def test_complete_sets_session_completed(self, db: ThreadSafeConnection, session: dict) -> None:
        result = await handle_mission_complete(session_id=session["id"], _db=db)
        assert result["status"] == "completed"
        updated = mission_storage.get_session(db, session["id"])
        assert updated is not None
        assert updated["status"] == "completed"

    @pytest.mark.asyncio
    async def test_complete_creates_event(self, db: ThreadSafeConnection, session: dict) -> None:
        await handle_mission_complete(session_id=session["id"], _db=db)
        events = mission_storage.list_events(db, session["id"])
        assert len(events) == 1
        assert events[0]["event_type"] == "session_completed"

    @pytest.mark.asyncio
    async def test_complete_session_not_found(self, db: ThreadSafeConnection) -> None:
        result = await handle_mission_complete(session_id="bad", _db=db)
        assert "error" in result


# ---------------------------------------------------------------------------
# Patch plan tests
# ---------------------------------------------------------------------------


class TestMissionPatchPlan:
    @pytest.mark.asyncio
    async def test_patch_plan_applies_operations(self, db: ThreadSafeConnection, session: dict, item: dict) -> None:
        ai_service = AsyncMock()
        ai_service.complete.return_value = json.dumps(
            {
                "operations": [
                    {
                        "op": "add_item",
                        "payload": {
                            "summary": "New from patch",
                            "temp_id": "new_1",
                            "priority": 20,
                        },
                    }
                ]
            }
        )
        result = await handle_mission_patch_plan(
            session_id=session["id"],
            instruction="Add a new task",
            _db=db,
            _ai_service=ai_service,
        )
        assert result["message"].startswith("Applied")
        assert len(result["operations"]) == 1
        items = mission_storage.list_items_by_session(db, session["id"])
        summaries = [i["summary"] for i in items]
        assert "New from patch" in summaries

    @pytest.mark.asyncio
    async def test_patch_plan_no_ops(self, db: ThreadSafeConnection, session: dict) -> None:
        ai_service = AsyncMock()
        ai_service.complete.return_value = json.dumps({"operations": []})
        result = await handle_mission_patch_plan(
            session_id=session["id"],
            instruction="Do nothing",
            _db=db,
            _ai_service=ai_service,
        )
        assert result["operations"] == []

    @pytest.mark.asyncio
    async def test_patch_plan_session_not_found(self, db: ThreadSafeConnection) -> None:
        ai_service = AsyncMock()
        result = await handle_mission_patch_plan(session_id="bad", instruction="x", _db=db, _ai_service=ai_service)
        assert "error" in result

    @pytest.mark.asyncio
    async def test_patch_plan_no_ai_service(self, db: ThreadSafeConnection, session: dict) -> None:
        result = await handle_mission_patch_plan(session_id=session["id"], instruction="x", _db=db)
        assert "error" in result

    @pytest.mark.asyncio
    async def test_patch_plan_no_db(self) -> None:
        result = await handle_mission_patch_plan(session_id="x", instruction="x", _ai_service=AsyncMock())
        assert "error" in result


# ---------------------------------------------------------------------------
# Session safety
# ---------------------------------------------------------------------------


class TestSessionSafety:
    @pytest.mark.asyncio
    async def test_hold_rejects_cross_session_item(self, db: ThreadSafeConnection, session: dict) -> None:
        other = mission_storage.create_session(db, title="Other", status="active")
        other_item = mission_storage.create_item(db, session_id=other["id"], summary="Foreign")
        result = await handle_mission_hold(session_id=session["id"], item_id=other_item["id"], _db=db)
        assert "error" in result
        assert "does not belong" in result["error"]

    @pytest.mark.asyncio
    async def test_drop_rejects_cross_session_item(self, db: ThreadSafeConnection, session: dict) -> None:
        other = mission_storage.create_session(db, title="Other", status="active")
        other_item = mission_storage.create_item(db, session_id=other["id"], summary="Foreign")
        result = await handle_mission_drop_item(session_id=session["id"], item_id=other_item["id"], _db=db)
        assert "error" in result
        assert "does not belong" in result["error"]

    @pytest.mark.asyncio
    async def test_reprioritize_rejects_cross_session_item(self, db: ThreadSafeConnection, session: dict) -> None:
        other = mission_storage.create_session(db, title="Other", status="active")
        other_item = mission_storage.create_item(db, session_id=other["id"], summary="Foreign")
        result = await handle_mission_reprioritize(
            session_id=session["id"], item_id=other_item["id"], priority=1, _db=db
        )
        assert "error" in result
        assert "does not belong" in result["error"]


class TestAddItemDepValidation:
    @pytest.mark.asyncio
    async def test_add_item_bad_dep_rejected_before_create(self, db: ThreadSafeConnection, session: dict) -> None:
        result = await handle_mission_add_item(
            session_id=session["id"], summary="New", depends_on=["nonexistent"], _db=db
        )
        assert "error" in result
        assert "not found" in result["error"]
        items = mission_storage.list_items_by_session(db, session["id"])
        item_summaries = [i["summary"] for i in items]
        assert "New" not in item_summaries


# ---------------------------------------------------------------------------
# No adapter imports test
# ---------------------------------------------------------------------------


class TestNoAdapterImports:
    def test_mission_module_does_not_import_adapters(self) -> None:
        import anteroom.tools.mission as mod

        source = open(mod.__file__).read()  # noqa: SIM115
        assert "adapter" not in source.split("import")[0] or True
        assert "from ..services.mission_adapter" not in source
        assert "from ..services.adapter" not in source
        assert "adapter.create" not in source

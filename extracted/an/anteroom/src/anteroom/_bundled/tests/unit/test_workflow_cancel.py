"""Tests for workflow cancel semantics (#890)."""

from __future__ import annotations

import re
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from anteroom.db import init_db
from anteroom.services.workflow_storage import (
    create_workflow_run,
    get_active_run_for_conversation,
    get_workflow_run,
    is_cancel_requested,
    set_cancel_requested,
    update_workflow_run,
)


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


def _make_run(db: Any, **overrides: Any) -> dict[str, Any]:
    defaults = {
        "workflow_id": "test_workflow",
        "workflow_version": "0.1.0",
        "target_kind": "issue",
        "target_ref": "123",
    }
    defaults.update(overrides)
    return create_workflow_run(db, **defaults)


# ---------------------------------------------------------------------------
# Storage helpers
# ---------------------------------------------------------------------------


class TestSetCancelRequested:
    def test_sets_flag(self, db: Any) -> None:
        run = _make_run(db)
        assert not is_cancel_requested(db, run["id"])
        set_cancel_requested(db, run["id"])
        assert is_cancel_requested(db, run["id"])

    def test_idempotent(self, db: Any) -> None:
        run = _make_run(db)
        set_cancel_requested(db, run["id"])
        set_cancel_requested(db, run["id"])
        assert is_cancel_requested(db, run["id"])


class TestIsCancelRequested:
    def test_false_by_default(self, db: Any) -> None:
        run = _make_run(db)
        assert not is_cancel_requested(db, run["id"])

    def test_false_for_nonexistent_run(self, db: Any) -> None:
        assert not is_cancel_requested(db, "nonexistent-id")


class TestGetActiveRunForConversation:
    def test_returns_active_run(self, db: Any) -> None:
        run = _make_run(db, conversation_id="conv-1")
        update_workflow_run(db, run["id"], status="running")
        active = get_active_run_for_conversation(db, "conv-1")
        assert active is not None
        assert active["id"] == run["id"]

    def test_returns_none_for_terminal_run(self, db: Any) -> None:
        run = _make_run(db, conversation_id="conv-2")
        update_workflow_run(db, run["id"], status="completed")
        active = get_active_run_for_conversation(db, "conv-2")
        assert active is None

    def test_returns_none_for_no_conversation(self, db: Any) -> None:
        active = get_active_run_for_conversation(db, "nonexistent")
        assert active is None

    def test_returns_most_recent(self, db: Any) -> None:
        run1 = _make_run(db, conversation_id="conv-3")
        run2 = _make_run(db, conversation_id="conv-3")
        update_workflow_run(db, run1["id"], status="running")
        update_workflow_run(db, run2["id"], status="running")
        active = get_active_run_for_conversation(db, "conv-3")
        assert active is not None
        assert active["id"] == run2["id"]

    def test_skips_cancelled(self, db: Any) -> None:
        run = _make_run(db, conversation_id="conv-4")
        update_workflow_run(db, run["id"], status="cancelled")
        active = get_active_run_for_conversation(db, "conv-4")
        assert active is None

    def test_returns_paused_run(self, db: Any) -> None:
        run = _make_run(db, conversation_id="conv-5")
        update_workflow_run(db, run["id"], status="paused")
        active = get_active_run_for_conversation(db, "conv-5")
        assert active is not None
        assert active["id"] == run["id"]


# ---------------------------------------------------------------------------
# request_cancel
# ---------------------------------------------------------------------------


class TestRequestCancel:
    @pytest.mark.asyncio
    async def test_cancel_running_run(self, db: Any) -> None:
        from anteroom.services.workflow_engine import WorkflowEngine

        run = _make_run(db)
        update_workflow_run(db, run["id"], status="running")
        updated = await WorkflowEngine.request_cancel(db, run["id"])
        assert is_cancel_requested(db, updated["id"])
        # Running runs stay running until the poll loop picks it up
        assert updated["status"] == "running"

    @pytest.mark.asyncio
    async def test_cancel_paused_run(self, db: Any) -> None:
        from anteroom.services.workflow_engine import WorkflowEngine

        run = _make_run(db)
        update_workflow_run(db, run["id"], status="paused")
        updated = await WorkflowEngine.request_cancel(db, run["id"])
        assert updated["status"] == "cancelled"

    @pytest.mark.asyncio
    async def test_cancel_waiting_for_approval(self, db: Any) -> None:
        from anteroom.services.workflow_engine import WorkflowEngine

        run = _make_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_approval")
        updated = await WorkflowEngine.request_cancel(db, run["id"])
        assert updated["status"] == "cancelled"

    @pytest.mark.asyncio
    async def test_cancel_waiting_for_input(self, db: Any) -> None:
        from anteroom.services.workflow_engine import WorkflowEngine

        run = _make_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_input")
        updated = await WorkflowEngine.request_cancel(db, run["id"])
        assert updated["status"] == "cancelled"

    @pytest.mark.asyncio
    async def test_cancel_terminal_raises(self, db: Any) -> None:
        from anteroom.services.workflow_engine import WorkflowEngine

        run = _make_run(db)
        update_workflow_run(db, run["id"], status="completed")
        with pytest.raises(ValueError, match="terminal status"):
            await WorkflowEngine.request_cancel(db, run["id"])

    @pytest.mark.asyncio
    async def test_cancel_nonexistent_raises(self, db: Any) -> None:
        from anteroom.services.workflow_engine import WorkflowEngine

        with pytest.raises(ValueError, match="not found"):
            await WorkflowEngine.request_cancel(db, "nonexistent")

    @pytest.mark.asyncio
    async def test_cancel_idempotent(self, db: Any) -> None:
        from anteroom.services.workflow_engine import WorkflowEngine

        run = _make_run(db)
        update_workflow_run(db, run["id"], status="running")
        await WorkflowEngine.request_cancel(db, run["id"])
        # Second call should not raise (still running, flag already set)
        await WorkflowEngine.request_cancel(db, run["id"])
        assert is_cancel_requested(db, run["id"])

    @pytest.mark.asyncio
    async def test_cancel_with_event_bus(self, db: Any) -> None:
        from anteroom.services.workflow_engine import WorkflowEngine

        run = _make_run(db)
        update_workflow_run(db, run["id"], status="running")
        bus = MagicMock()
        bus.publish = AsyncMock()
        await WorkflowEngine.request_cancel(db, run["id"], event_bus=bus)
        assert is_cancel_requested(db, run["id"])


# ---------------------------------------------------------------------------
# Cancel-intent pattern matching
# ---------------------------------------------------------------------------


class TestCancelIntentPatterns:
    _cancel_patterns = [
        re.compile(r"\b(cancel|stop|abort|halt|kill)\b.*\b(workflow|run|task)\b", re.IGNORECASE),
        re.compile(r"^(cancel|stop|abort)$", re.IGNORECASE),
    ]

    def _matches(self, text: str) -> bool:
        return any(p.search(text.strip()) for p in self._cancel_patterns)

    def test_cancel_workflow(self) -> None:
        assert self._matches("cancel the workflow")

    def test_stop_run(self) -> None:
        assert self._matches("stop the run")

    def test_abort_task(self) -> None:
        assert self._matches("abort the task")

    def test_bare_cancel(self) -> None:
        assert self._matches("cancel")

    def test_bare_stop(self) -> None:
        assert self._matches("stop")

    def test_bare_abort(self) -> None:
        assert self._matches("abort")

    def test_no_match_normal_message(self) -> None:
        assert not self._matches("how do I cancel my order?")

    def test_no_match_empty(self) -> None:
        assert not self._matches("")

    def test_halt_workflow(self) -> None:
        assert self._matches("halt the workflow")

    def test_kill_run(self) -> None:
        assert self._matches("kill the run")

    def test_case_insensitive(self) -> None:
        assert self._matches("Cancel")
        assert self._matches("STOP")


# ---------------------------------------------------------------------------
# conversation_id on create_workflow_run
# ---------------------------------------------------------------------------


class TestConversationIdOnRun:
    def test_conversation_id_stored(self, db: Any) -> None:
        run = _make_run(db, conversation_id="conv-abc")
        fetched = get_workflow_run(db, run["id"])
        assert fetched is not None
        assert fetched["conversation_id"] == "conv-abc"

    def test_conversation_id_default_none(self, db: Any) -> None:
        run = _make_run(db)
        fetched = get_workflow_run(db, run["id"])
        assert fetched is not None
        assert fetched["conversation_id"] is None


class TestRequestCancelBlockedRun:
    """Blocked runs can be cancelled immediately (#1141)."""

    @pytest.mark.asyncio
    async def test_request_cancel_blocked_run(self, db: Any) -> None:
        from anteroom.services.workflow_engine import WorkflowEngine

        run = _make_run(db)
        update_workflow_run(db, run["id"], status="blocked")
        updated = await WorkflowEngine.request_cancel(db, run["id"])
        assert updated["status"] == "cancelled"

"""Unit tests for the mission CLI handlers."""

from __future__ import annotations

import argparse
import sys
from io import StringIO
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from rich.console import Console

from anteroom.db import init_db


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    return init_db(tmp_path / "test.db")


def _make_args(**kwargs: Any) -> argparse.Namespace:
    return argparse.Namespace(**kwargs)


def _capture_console() -> tuple[Console, StringIO]:
    buf = StringIO()
    console = Console(file=buf, width=120, no_color=True)
    return console, buf


# ---------------------------------------------------------------------------
# _handle_list
# ---------------------------------------------------------------------------


class TestHandleList:
    def test_empty_list(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_list

            _handle_list(db, _make_args(status=None))
        assert "No missions found" in buf.getvalue()

    def test_list_with_sessions(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session

        s = create_session(db, title="Test Mission", status="active")
        create_item(db, session_id=s["id"], summary="Task 1")
        create_item(db, session_id=s["id"], summary="Task 2")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_list

            _handle_list(db, _make_args(status=None))
        output = buf.getvalue()
        assert "Test Mission" in output
        assert "active" in output

    def test_list_with_status_filter(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_session

        create_session(db, title="Active One", status="active")
        create_session(db, title="Pending One", status="pending")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_list

            _handle_list(db, _make_args(status="active"))
        output = buf.getvalue()
        assert "Active One" in output
        assert "Pending One" not in output


# ---------------------------------------------------------------------------
# _handle_status
# ---------------------------------------------------------------------------


class TestHandleStatus:
    def test_missing_session_id(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_status

            _handle_status(db, _make_args(session_id=None))
        assert "session_id is required" in buf.getvalue()

    def test_not_found(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_status

            _handle_status(db, _make_args(session_id="nonexistent"))
        assert "Mission not found" in buf.getvalue()

    def test_shows_session_and_items(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session

        s = create_session(db, title="My Mission", status="active")
        create_item(db, session_id=s["id"], summary="Do the thing", priority=10)

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_status

            _handle_status(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "My Mission" in output
        assert "Do the thing" in output
        assert "0/1 completed" in output


# ---------------------------------------------------------------------------
# _handle_scheduler
# ---------------------------------------------------------------------------


class TestHandleScheduler:
    def test_scheduler_once_runs_async_helper(self, db: Any) -> None:
        config = MagicMock()
        console, _buf = _capture_console()

        captured: list[Any] = []

        def _capture_run(coro: Any) -> None:
            captured.append(coro)
            coro.close()

        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch("anteroom.cli.mission_cli.asyncio.run", side_effect=_capture_run) as mock_run,
        ):
            from anteroom.cli.mission_cli import _handle_scheduler

            _handle_scheduler(config, db, _make_args(once=True, poll_interval=2.5))

        mock_run.assert_called_once()


# ---------------------------------------------------------------------------
# _handle_revisions
# ---------------------------------------------------------------------------


class TestHandleRevisions:
    def test_not_found(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_revisions

            _handle_revisions(db, _make_args(session_id="nope"))
        assert "Mission not found" in buf.getvalue()

    def test_no_revisions(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_session

        s = create_session(db, title="Empty")
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_revisions

            _handle_revisions(db, _make_args(session_id=s["id"]))
        assert "No revisions found" in buf.getvalue()

    def test_shows_revisions(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_revision, create_session

        s = create_session(db, title="Rev Test")
        create_revision(
            db,
            session_id=s["id"],
            revision_number=1,
            operations=[{"op": "initial_plan"}],
            plan_snapshot_after={"items": []},
            reason="initial plan",
        )

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_revisions

            _handle_revisions(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "initial_plan" in output
        assert "initial plan" in output

    def test_shows_revision_artifact_refs(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_revision, create_session

        s = create_session(db, title="Art Test")
        create_revision(
            db,
            session_id=s["id"],
            revision_number=1,
            operations=[{"op": "initial_plan"}],
            plan_snapshot_after={"items": []},
            referenced_artifacts=[{"fqn": "@ns/spec/auth", "version": 2}],
            reason="initial",
        )

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_revisions

            _handle_revisions(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "@ns/spec/auth" in output
        assert "v2" in output


# ---------------------------------------------------------------------------
# _handle_cancel
# ---------------------------------------------------------------------------


class TestHandleCancel:
    def test_not_found(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_cancel

            _handle_cancel(db, _make_args(session_id="nope"))
        assert "Mission not found" in buf.getvalue()

    def test_cancel_active_session(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_session, get_session

        s = create_session(db, title="To Cancel", status="active")
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_cancel

            _handle_cancel(db, _make_args(session_id=s["id"]))
        assert "cancelled" in buf.getvalue()
        updated = get_session(db, s["id"])
        assert updated is not None
        assert updated["status"] == "cancelled"

    def test_cancel_already_cancelled(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_session

        s = create_session(db, title="Done", status="cancelled")
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_cancel

            _handle_cancel(db, _make_args(session_id=s["id"]))
        assert "already cancelled" in buf.getvalue()


# ---------------------------------------------------------------------------
# _handle_talk
# ---------------------------------------------------------------------------


class TestHandleTalk:
    def test_not_found(self, db: Any) -> None:
        config = MagicMock()
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_talk

            _handle_talk(config, db, _make_args(session_id="nope"))
        assert "Mission not found" in buf.getvalue()

    def test_launches_repl(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_session

        s = create_session(db, title="Talk Test")
        config = MagicMock()
        console, buf = _capture_console()

        captured: list[Any] = []

        def _capture_run(coro: Any) -> None:
            captured.append(coro)
            coro.close()

        with (
            patch.dict(sys.modules, {"filetype": MagicMock()}),
            patch("anteroom.cli.mission_cli.console", console),
            patch("anteroom.cli.mission_cli.asyncio.run", side_effect=_capture_run) as mock_run,
        ):
            from anteroom.cli.mission_cli import _handle_talk

            _handle_talk(config, db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "Attaching to mission" in output
        mock_run.assert_called_once()


# ---------------------------------------------------------------------------
# _handle_create
# ---------------------------------------------------------------------------


class TestHandleCreate:
    def test_prompt_calls_ai_service(self, db: Any) -> None:
        import json
        from unittest.mock import AsyncMock

        config = MagicMock()
        mock_ai = AsyncMock()
        mock_ai.complete = AsyncMock(
            return_value=json.dumps({"title": "AI Plan", "items": [{"summary": "Task 1", "temp_id": "t1"}]})
        )
        console, buf = _capture_console()
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch("anteroom.cli.mission_cli._create_ai", return_value=mock_ai),
            patch("builtins.input", return_value="n"),
        ):
            from anteroom.cli.mission_cli import _handle_create

            _handle_create(
                config,
                db,
                _make_args(
                    spec=None,
                    prompt="do something",
                    adapter="noop",
                    workflow_path=None,
                    profile=None,
                    launch=False,
                ),
            )
        output = buf.getvalue()
        assert "Task 1" in output
        assert "Aborted" in output

    def test_spec_not_found(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_create

            _handle_create(
                MagicMock(),
                db,
                _make_args(
                    spec="nonexistent/spec",
                    prompt=None,
                    adapter="noop",
                    workflow_path=None,
                    profile=None,
                    launch=False,
                ),
            )
        assert "Error" in buf.getvalue()

    def test_unknown_profile_shows_error(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_create

            _handle_create(
                MagicMock(),
                db,
                _make_args(
                    spec="test/spec/x",
                    prompt=None,
                    adapter="noop",
                    workflow_path=None,
                    profile="bad-name",
                    launch=False,
                ),
            )
        output = buf.getvalue()
        assert "Unknown execution profile" in output

    def test_profile_flag_applied(self, db: Any) -> None:
        import json
        from unittest.mock import AsyncMock

        config = MagicMock()
        mock_ai = AsyncMock()
        mock_ai.complete = AsyncMock(
            return_value=json.dumps(
                {
                    "title": "Plan",
                    "items": [{"summary": "A", "temp_id": "a"}, {"summary": "B", "temp_id": "b"}],
                }
            )
        )
        console, buf = _capture_console()
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch("anteroom.cli.mission_cli._create_ai", return_value=mock_ai),
            patch("anteroom.services.mission_profiles.discover_workflows", return_value=[]),
            patch("builtins.input", return_value="n"),
        ):
            from anteroom.cli.mission_cli import _handle_create

            _handle_create(
                config,
                db,
                _make_args(
                    spec=None,
                    prompt="do stuff",
                    adapter="noop",
                    workflow_path=None,
                    profile="plan-then-execute",
                    launch=False,
                ),
            )
        output = buf.getvalue()
        assert "plan-then-execute" in output
        assert "_planning" in output

    def test_profile_with_adapter_override(self, db: Any) -> None:
        """Explicit --adapter should override profile defaults."""
        import json
        from unittest.mock import AsyncMock

        config = MagicMock()
        mock_ai = AsyncMock()
        mock_ai.complete = AsyncMock(
            return_value=json.dumps({"title": "Plan", "items": [{"summary": "A", "temp_id": "a"}]})
        )
        console, buf = _capture_console()
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch("anteroom.cli.mission_cli._create_ai", return_value=mock_ai),
            patch("anteroom.services.mission_profiles.discover_workflows", return_value=[]),
            patch("builtins.input", return_value="n"),
        ):
            from anteroom.cli.mission_cli import _handle_create

            _handle_create(
                config,
                db,
                _make_args(
                    spec=None,
                    prompt="do stuff",
                    adapter="workflow",
                    workflow_path="defs/build.yaml",
                    profile="default",
                    launch=False,
                ),
            )
        output = buf.getvalue()
        # The adapter override should take effect — item should show "workflow"
        assert "workflow" in output

    def test_launch_flag_persists_active_session(self, db: Any) -> None:
        from anteroom.services.mission_storage import get_session

        config = MagicMock()
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_create
            from anteroom.services.mission_compiler import CompiledItem, CompiledPlan

            with patch(
                "anteroom.services.mission_compiler.compile_from_spec",
                return_value=CompiledPlan(items=[CompiledItem(summary="Task", temp_id="t1")], title="Plan"),
            ):
                _handle_create(
                    config,
                    db,
                    _make_args(
                        spec="@test/spec/auth",
                        prompt=None,
                        adapter="noop",
                        workflow_path=None,
                        profile=None,
                        launch=True,
                    ),
                )

        output = buf.getvalue()
        assert "Mission created" in output
        assert "executor_enabled" in output
        session_id = output.split("Mission created:")[-1].splitlines()[0].strip()
        session = get_session(db, session_id)
        assert session is not None
        assert session["status"] == "active"

    def test_interactive_yes_persists_active_session(self, db: Any) -> None:
        from anteroom.services.mission_storage import get_session

        config = MagicMock()
        console, buf = _capture_console()
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch("builtins.input", return_value="y"),
        ):
            from anteroom.cli.mission_cli import _handle_create
            from anteroom.services.mission_compiler import CompiledItem, CompiledPlan

            with patch(
                "anteroom.services.mission_compiler.compile_from_spec",
                return_value=CompiledPlan(items=[CompiledItem(summary="Task", temp_id="t1")], title="Plan"),
            ):
                _handle_create(
                    config,
                    db,
                    _make_args(
                        spec="@test/spec/auth",
                        prompt=None,
                        adapter="noop",
                        workflow_path=None,
                        profile=None,
                        launch=False,
                    ),
                )

        output = buf.getvalue()
        assert "Mission created" in output
        session_id = output.split("Mission created:")[-1].splitlines()[0].strip()
        session = get_session(db, session_id)
        assert session is not None
        assert session["status"] == "active"


# ---------------------------------------------------------------------------
# _handle_update
# ---------------------------------------------------------------------------


class TestHandleUpdate:
    def test_session_not_found(self, db: Any) -> None:
        config = MagicMock()
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_update

            _handle_update(config, db, _make_args(session_id="nonexistent", instruction="reprioritize", force=False))
        assert "Mission not found" in buf.getvalue()

    def test_update_no_ops(self, db: Any) -> None:
        import json
        from unittest.mock import AsyncMock

        from anteroom.services.mission_storage import create_session

        s = create_session(db, title="Update Test", status="active")
        config = MagicMock()
        mock_ai = AsyncMock()
        mock_ai.complete = AsyncMock(return_value=json.dumps({"operations": []}))
        console, buf = _capture_console()
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch("anteroom.cli.mission_cli._create_ai", return_value=mock_ai),
        ):
            from anteroom.cli.mission_cli import _handle_update

            _handle_update(config, db, _make_args(session_id=s["id"], instruction="do nothing", force=False))
        assert "No operations" in buf.getvalue()


# ---------------------------------------------------------------------------
# _handle_reconcile
# ---------------------------------------------------------------------------


class TestHandleReconcile:
    def test_reconcile_success(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session, get_item

        s = create_session(db, title="Reconcile Test", status="active")
        item = create_item(db, session_id=s["id"], summary="Task A", status="active")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_reconcile

            _handle_reconcile(
                MagicMock(),
                db,
                _make_args(
                    session_id=s["id"], item_id=item["id"], status="completed", reason="Done via CI", force=False
                ),
            )
        output = buf.getvalue()
        assert "Reconciled" in output
        assert "Task A" in output
        assert "active -> completed" in output
        updated = get_item(db, item["id"])
        assert updated is not None
        assert updated["status"] == "completed"

    def test_reconcile_missing_reason(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_reconcile

            _handle_reconcile(
                MagicMock(),
                db,
                _make_args(session_id="sid", item_id="iid", status="completed", reason=None, force=False),
            )
        assert "--reason is required" in buf.getvalue()

    def test_reconcile_session_not_found(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_reconcile

            _handle_reconcile(
                MagicMock(),
                db,
                _make_args(session_id="nonexistent", item_id="iid", status="completed", reason="done", force=False),
            )
        assert "Mission not found" in buf.getvalue()

    def test_reconcile_item_not_found(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_session

        s = create_session(db, title="Test", status="active")
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_reconcile

            _handle_reconcile(
                MagicMock(),
                db,
                _make_args(session_id=s["id"], item_id="nonexistent", status="completed", reason="done", force=False),
            )
        assert "Item not found" in buf.getvalue()

    def test_reconcile_item_wrong_session(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session

        s1 = create_session(db, title="S1", status="active")
        s2 = create_session(db, title="S2", status="active")
        item = create_item(db, session_id=s1["id"], summary="Task", status="active")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_reconcile

            _handle_reconcile(
                MagicMock(),
                db,
                _make_args(session_id=s2["id"], item_id=item["id"], status="completed", reason="done", force=False),
            )
        assert "does not belong" in buf.getvalue()

    def test_reconcile_already_completed(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session

        s = create_session(db, title="Test", status="active")
        item = create_item(db, session_id=s["id"], summary="Task", status="completed")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_reconcile

            _handle_reconcile(
                MagicMock(),
                db,
                _make_args(session_id=s["id"], item_id=item["id"], status="completed", reason="done", force=False),
            )
        assert "Cannot reconcile" in buf.getvalue()

    def test_reconcile_rejects_live_running_execution(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_execution, create_item, create_session

        s = create_session(db, title="Test", status="active")
        item = create_item(db, session_id=s["id"], summary="Task", status="active")
        create_execution(db, item_id=item["id"], attempt_number=1, status="running")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_reconcile

            _handle_reconcile(
                MagicMock(),
                db,
                _make_args(session_id=s["id"], item_id=item["id"], status="completed", reason="done", force=False),
            )
        output = buf.getvalue()
        assert "live execution" in output
        assert "--force" in output

    def test_reconcile_rejects_live_pending_execution(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_execution, create_item, create_session

        s = create_session(db, title="Test", status="active")
        item = create_item(db, session_id=s["id"], summary="Task", status="active")
        create_execution(db, item_id=item["id"], attempt_number=1, status="pending")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_reconcile

            _handle_reconcile(
                MagicMock(),
                db,
                _make_args(session_id=s["id"], item_id=item["id"], status="completed", reason="done", force=False),
            )
        output = buf.getvalue()
        assert "live execution" in output

    def test_reconcile_force_cancels_then_reconciles(self, db: Any) -> None:
        from anteroom.services.mission_storage import (
            create_execution,
            create_item,
            create_session,
            get_execution,
            get_item,
        )

        s = create_session(db, title="Test", status="active")
        item = create_item(db, session_id=s["id"], summary="Task", status="active")
        exc = create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref="run-123")

        mock_adapter = MagicMock()
        mock_adapter.cancel = AsyncMock(return_value=MagicMock(state="cancelled"))
        mock_registry = MagicMock()
        mock_registry.get.return_value = mock_adapter

        console, buf = _capture_console()
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch(
                "anteroom.services.mission_runtime.create_mission_adapter_registry",
                return_value=mock_registry,
            ),
        ):
            from anteroom.cli.mission_cli import _handle_reconcile

            _handle_reconcile(
                MagicMock(),
                db,
                _make_args(session_id=s["id"], item_id=item["id"], status="completed", reason="force done", force=True),
            )

        output = buf.getvalue()
        assert "Cancelled live execution" in output
        assert "Reconciled" in output
        updated_exc = get_execution(db, exc["id"])
        assert updated_exc is not None
        assert updated_exc["status"] == "cancelled"
        updated_item = get_item(db, item["id"])
        assert updated_item is not None
        assert updated_item["status"] == "completed"

    def test_reconcile_force_adapter_cancel_fails(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_execution, create_item, create_session, get_item

        s = create_session(db, title="Test", status="active")
        item = create_item(db, session_id=s["id"], summary="Task", status="active")
        create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref="run-456")

        mock_adapter = MagicMock()
        mock_adapter.cancel = AsyncMock(side_effect=RuntimeError("Workflow engine unavailable"))
        mock_registry = MagicMock()
        mock_registry.get.return_value = mock_adapter

        console, buf = _capture_console()
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch(
                "anteroom.services.mission_runtime.create_mission_adapter_registry",
                return_value=mock_registry,
            ),
        ):
            from anteroom.cli.mission_cli import _handle_reconcile

            _handle_reconcile(
                MagicMock(),
                db,
                _make_args(session_id=s["id"], item_id=item["id"], status="completed", reason="force", force=True),
            )

        output = buf.getvalue()
        assert "Failed to cancel live execution" in output
        assert "Reconciled" not in output
        unchanged = get_item(db, item["id"])
        assert unchanged is not None
        assert unchanged["status"] == "active"


# ---------------------------------------------------------------------------
# _handle_summary
# ---------------------------------------------------------------------------


class TestHandleSummary:
    def test_not_found(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_summary

            _handle_summary(db, _make_args(session_id="nope", since=None))
        assert "Mission not found" in buf.getvalue()

    def test_missing_session_id(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_summary

            _handle_summary(db, _make_args(session_id=None, since=None))
        assert "session_id is required" in buf.getvalue()

    def test_retrospective_output(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session

        s = create_session(db, title="Retro Test", status="completed")
        create_item(db, session_id=s["id"], summary="Done Task", status="completed")
        create_item(db, session_id=s["id"], summary="Failed Task", status="failed")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_summary

            _handle_summary(db, _make_args(session_id=s["id"], since=None))
        output = buf.getvalue()
        assert "Retrospective" in output
        assert "1/2" in output
        assert "Done Task" in output
        assert "Failed Task" in output

    def test_delta_output(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_event, create_item, create_session

        s = create_session(db, title="Delta Test", status="active")
        item = create_item(db, session_id=s["id"], summary="Task A")
        ev = create_event(db, session_id=s["id"], item_id=item["id"], event_type="item_launched")
        create_event(db, session_id=s["id"], item_id=item["id"], event_type="item_completed")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_summary

            _handle_summary(db, _make_args(session_id=s["id"], since=ev["created_at"]))
        output = buf.getvalue()
        assert "Delta summary" in output
        assert "Completed: 1" in output


# ---------------------------------------------------------------------------
# _handle_cancel retrospective
# ---------------------------------------------------------------------------


class TestHandleCancelRetrospective:
    def test_cancel_generates_retrospective(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session, list_events

        s = create_session(db, title="Cancel Retro", status="active")
        create_item(db, session_id=s["id"], summary="Task A", status="completed")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_cancel

            _handle_cancel(db, _make_args(session_id=s["id"]))

        assert "cancelled" in buf.getvalue()
        retro_events = list_events(db, s["id"], event_type="session_retrospective")
        assert len(retro_events) == 1
        assert retro_events[0]["detail"]["completed"] == 1


# ---------------------------------------------------------------------------
# _handle_retry
# ---------------------------------------------------------------------------


class TestHandleRetry:
    def test_not_found(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_retry

            _handle_retry(db, _make_args(item_id="nonexistent"))
        assert "Item not found" in buf.getvalue()

    def test_retry_failed_item(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session, get_item

        s = create_session(db, title="Retry Test", status="active")
        item = create_item(db, session_id=s["id"], summary="Fail task")
        from anteroom.services.mission_storage import update_item

        update_item(db, item["id"], status="failed")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_retry

            _handle_retry(db, _make_args(item_id=item["id"]))
        assert "reset to pending" in buf.getvalue()
        refreshed = get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "pending"

    def test_retry_non_failed_item(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session

        s = create_session(db, title="Retry Test", status="active")
        item = create_item(db, session_id=s["id"], summary="Pending task")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_retry

            _handle_retry(db, _make_args(item_id=item["id"]))
        assert "must be 'failed'" in buf.getvalue()

    def test_retry_missing_item_id(self, db: Any) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_retry

            _handle_retry(db, _make_args(item_id=None))
        assert "item_id is required" in buf.getvalue()

    def test_retry_with_prefix(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session, get_item, update_item

        s = create_session(db, title="Retry Prefix", status="active")
        item = create_item(db, session_id=s["id"], summary="Prefix task")
        update_item(db, item["id"], status="failed")

        prefix = item["id"][:8]
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_retry

            _handle_retry(db, _make_args(item_id=prefix))
        assert "reset to pending" in buf.getvalue()
        refreshed = get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "pending"


# ---------------------------------------------------------------------------
# _handle_replace
# ---------------------------------------------------------------------------


class TestHandleReplace:
    def test_not_found(self, db: Any) -> None:
        config = MagicMock()
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_replace

            _handle_replace(config, db, _make_args(item_id="nonexistent"))
        assert "Item not found" in buf.getvalue()

    def test_no_execution(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session

        s = create_session(db, title="Replace Test", status="active")
        item = create_item(db, session_id=s["id"], summary="No exec")

        config = MagicMock()
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_replace

            _handle_replace(config, db, _make_args(item_id=item["id"]))
        assert "No execution found" in buf.getvalue()

    def test_replace_cancels_and_resets(self, db: Any) -> None:
        from anteroom.services.mission_storage import (
            create_execution,
            create_item,
            create_session,
            get_execution,
            get_item,
            update_item,
        )

        s = create_session(db, title="Replace Test", status="active")
        item = create_item(db, session_id=s["id"], summary="Replace me", adapter_type="test")
        update_item(db, item["id"], status="active")
        exc = create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref="ref-1")

        config = MagicMock()
        mock_adapter = MagicMock()
        mock_registry = MagicMock()
        mock_registry.get.return_value = mock_adapter

        console, buf = _capture_console()
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch("anteroom.cli.mission_cli.asyncio.run") as mock_run,
            patch(
                "anteroom.services.mission_runtime.create_mission_adapter_registry",
                return_value=mock_registry,
            ),
            patch("anteroom.services.mission_runtime.create_workflow_engine_factory"),
        ):
            from anteroom.cli.mission_cli import _handle_replace

            _handle_replace(config, db, _make_args(item_id=item["id"]))

        assert "reset to pending" in buf.getvalue()
        mock_run.assert_called_once()
        refreshed_item = get_item(db, item["id"])
        assert refreshed_item is not None
        assert refreshed_item["status"] == "pending"
        refreshed_exc = get_execution(db, exc["id"])
        assert refreshed_exc is not None
        assert refreshed_exc["status"] == "cancelled"

    def test_replace_fails_closed_when_adapter_cancel_raises(self, db: Any) -> None:
        from anteroom.services.mission_storage import (
            create_execution,
            create_item,
            create_session,
            get_execution,
            get_item,
            update_item,
        )

        s = create_session(db, title="Replace Fail-Closed", status="active")
        item = create_item(db, session_id=s["id"], summary="Replace me", adapter_type="test")
        update_item(db, item["id"], status="active")
        exc = create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref="ref-fail")

        config = MagicMock()
        mock_adapter = MagicMock()
        mock_adapter.cancel = AsyncMock(side_effect=RuntimeError("Workflow engine unavailable"))
        mock_registry = MagicMock()
        mock_registry.get.return_value = mock_adapter

        console, buf = _capture_console()
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch("anteroom.cli.mission_cli.asyncio.run", side_effect=RuntimeError("Workflow engine unavailable")),
            patch(
                "anteroom.services.mission_runtime.create_mission_adapter_registry",
                return_value=mock_registry,
            ),
            patch("anteroom.services.mission_runtime.create_workflow_engine_factory"),
        ):
            from anteroom.cli.mission_cli import _handle_replace

            _handle_replace(config, db, _make_args(item_id=item["id"]))

        output = buf.getvalue()
        assert "adapter cancel failed" in output
        assert "reset to pending" not in output
        # Item must remain active — prepare_replace must NOT have been called
        refreshed_item = get_item(db, item["id"])
        assert refreshed_item is not None
        assert refreshed_item["status"] == "active"
        # Execution must remain running
        refreshed_exc = get_execution(db, exc["id"])
        assert refreshed_exc is not None
        assert refreshed_exc["status"] == "running"

    def test_replace_fails_closed_when_adapter_not_found(self, db: Any) -> None:
        from anteroom.services.mission_storage import (
            create_execution,
            create_item,
            create_session,
            get_execution,
            get_item,
            update_item,
        )

        s = create_session(db, title="Replace No-Adapter", status="active")
        item = create_item(db, session_id=s["id"], summary="Replace me", adapter_type="unknown_adapter")
        update_item(db, item["id"], status="active")
        exc = create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref="ref-orphan")

        config = MagicMock()
        mock_registry = MagicMock()
        mock_registry.get.return_value = None  # adapter not found

        console, buf = _capture_console()
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch(
                "anteroom.services.mission_runtime.create_mission_adapter_registry",
                return_value=mock_registry,
            ),
            patch("anteroom.services.mission_runtime.create_workflow_engine_factory"),
        ):
            from anteroom.cli.mission_cli import _handle_replace

            _handle_replace(config, db, _make_args(item_id=item["id"]))

        output = buf.getvalue()
        assert "no adapter registered" in output
        assert "reset to pending" not in output
        # Item must remain active — prepare_replace must NOT have been called
        refreshed_item = get_item(db, item["id"])
        assert refreshed_item is not None
        assert refreshed_item["status"] == "active"
        # Execution must remain running
        refreshed_exc = get_execution(db, exc["id"])
        assert refreshed_exc is not None
        assert refreshed_exc["status"] == "running"

    def test_replace_missing_item_id(self, db: Any) -> None:
        config = MagicMock()
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_replace

            _handle_replace(config, db, _make_args(item_id=None))
        assert "item_id is required" in buf.getvalue()

    def test_replace_with_prefix(self, db: Any) -> None:
        from anteroom.services.mission_storage import (
            create_execution,
            create_item,
            create_session,
            get_item,
            update_item,
        )

        s = create_session(db, title="Replace Prefix", status="active")
        item = create_item(db, session_id=s["id"], summary="Prefix replace", adapter_type="noop")
        update_item(db, item["id"], status="active")
        create_execution(db, item_id=item["id"], attempt_number=1, status="running")

        prefix = item["id"][:8]
        config = MagicMock()
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_replace

            _handle_replace(config, db, _make_args(item_id=prefix))
        assert "reset to pending" in buf.getvalue()
        refreshed = get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "pending"


# ---------------------------------------------------------------------------
# _run_mission dispatcher
# ---------------------------------------------------------------------------


class TestRunMission:
    def test_no_action(self) -> None:
        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _run_mission

            _run_mission(MagicMock(), _make_args(mission_action=None))
        assert "Usage" in buf.getvalue()

    def test_unknown_action(self) -> None:
        console, buf = _capture_console()
        config = MagicMock()
        config.app.data_dir = Path("/tmp/test-anteroom-mission")
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch("anteroom.db.get_db", return_value=MagicMock()),
        ):
            from anteroom.cli.mission_cli import _run_mission

            _run_mission(config, _make_args(mission_action="bogus"))
        assert "Unknown mission action" in buf.getvalue()

    def test_reconcile_dispatch(self) -> None:
        console, _buf = _capture_console()
        config = MagicMock()
        config.app.data_dir = Path("/tmp/test-anteroom-mission")
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch("anteroom.db.get_db", return_value=MagicMock()),
            patch("anteroom.cli.mission_cli._handle_reconcile") as mock_reconcile,
        ):
            from anteroom.cli.mission_cli import _run_mission

            _run_mission(
                config,
                _make_args(
                    mission_action="reconcile",
                    session_id="sid",
                    item_id="iid",
                    status="completed",
                    reason="done",
                ),
            )

        mock_reconcile.assert_called_once()

    def test_scheduler_dispatch(self) -> None:
        console, _buf = _capture_console()
        config = MagicMock()
        config.app.data_dir = Path("/tmp/test-anteroom-mission")
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch("anteroom.db.get_db", return_value=MagicMock()),
            patch("anteroom.cli.mission_cli._handle_scheduler") as mock_scheduler,
        ):
            from anteroom.cli.mission_cli import _run_mission

            _run_mission(config, _make_args(mission_action="scheduler", once=True, poll_interval=1.0))

        mock_scheduler.assert_called_once()


class TestHandleStatusTypeColumn:
    def test_status_shows_item_type(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session

        s = create_session(db, title="Typed Mission", status="active")
        create_item(db, session_id=s["id"], summary="Write docs", priority=10, item_type="docs")
        create_item(db, session_id=s["id"], summary="Research options", priority=20, item_type="research")

        console, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", console):
            from anteroom.cli.mission_cli import _handle_status

            _handle_status(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "docs" in output
        assert "research" in output
        assert "Type" in output

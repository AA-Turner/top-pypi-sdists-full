"""Tests for `aroom mission why` handler (#1235)."""

from __future__ import annotations

import argparse
from io import StringIO
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

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
    con = Console(file=buf, width=120, no_color=True)
    return con, buf


class TestHandleWhy:
    def test_missing_session_id(self, db: Any) -> None:
        con, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", con):
            from anteroom.cli.mission_cli import _handle_why

            _handle_why(db, _make_args(session_id=None))
        assert "session_id is required" in buf.getvalue()

    def test_not_found(self, db: Any) -> None:
        con, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", con):
            from anteroom.cli.mission_cli import _handle_why

            _handle_why(db, _make_args(session_id="nonexistent"))
        assert "Mission not found" in buf.getvalue()

    def test_terminal_session_no_blockers(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_session

        s = create_session(db, title="Done", status="completed")
        con, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", con):
            from anteroom.cli.mission_cli import _handle_why

            _handle_why(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "completed" in output
        assert "No active blockers" in output

    def test_all_items_completed(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session, update_item

        s = create_session(db, title="All Done", status="active")
        i = create_item(db, session_id=s["id"], summary="Task 1")
        update_item(db, i["id"], status="completed")

        con, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", con):
            from anteroom.cli.mission_cli import _handle_why

            _handle_why(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "all items completed" in output

    def test_dependency_blocker(self, db: Any) -> None:
        from anteroom.services.mission_storage import add_dependency, create_item, create_session

        s = create_session(db, title="Dep Test", status="active")
        i1 = create_item(db, session_id=s["id"], summary="First task")
        i2 = create_item(db, session_id=s["id"], summary="Second task")
        add_dependency(db, item_id=i2["id"], depends_on_id=i1["id"])

        con, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", con):
            from anteroom.cli.mission_cli import _handle_why

            _handle_why(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "Eligible" in output or "Blocked" in output
        # Second task should show dependency on first
        assert "First task" in output

    def test_linked_workflow_diagnosis(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_execution, create_item, create_session
        from anteroom.services.workflow_storage import create_workflow_run, update_workflow_run

        s = create_session(db, title="WF Test", status="active")
        item = create_item(db, session_id=s["id"], summary="Run workflow")

        run = create_workflow_run(
            db,
            workflow_id="test-wf",
            workflow_version="1",
            target_kind="test",
            target_ref="ref-1",
        )
        update_workflow_run(db, run["id"], status="failed", stop_reason="step_failed:lint")
        create_execution(db, item_id=item["id"], attempt_number=1, status="failed", adapter_ref=run["id"])

        con, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", con):
            from anteroom.cli.mission_cli import _handle_why

            _handle_why(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "Blocked" in output
        assert "lint" in output
        assert "Because" in output

    def test_linked_workflow_waiting_approval(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_execution, create_item, create_session
        from anteroom.services.workflow_storage import (
            create_approval_request,
            create_workflow_run,
            update_workflow_run,
        )

        s = create_session(db, title="Approval Test", status="active")
        item = create_item(db, session_id=s["id"], summary="Needs approval")

        run = create_workflow_run(
            db,
            workflow_id="test-wf",
            workflow_version="1",
            target_kind="test",
            target_ref="ref-1",
        )
        update_workflow_run(db, run["id"], status="waiting_for_approval")
        create_approval_request(
            db,
            run_id=run["id"],
            step_id="step-x",
            tool_name="bash",
            tool_args={"command": "deploy"},
            risk_tier="EXECUTE",
        )
        create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref=run["id"])

        con, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", con):
            from anteroom.cli.mission_cli import _handle_why

            _handle_why(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "Waiting" in output
        assert "approval" in output

    def test_dependents_shown(self, db: Any) -> None:
        from anteroom.services.mission_storage import add_dependency, create_item, create_session

        s = create_session(db, title="Dep Chain", status="active")
        i1 = create_item(db, session_id=s["id"], summary="Upstream task")
        i2 = create_item(db, session_id=s["id"], summary="Downstream task")
        add_dependency(db, item_id=i2["id"], depends_on_id=i1["id"])

        con, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", con):
            from anteroom.cli.mission_cli import _handle_why

            _handle_why(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "Blocking" in output
        assert "Downstream task" in output

    def test_dropped_items_excluded_from_blockers(self, db: Any) -> None:
        """Dropped items are terminal — they must not appear as eligible or blocking."""
        from anteroom.services.mission_storage import create_item, create_session, update_item

        s = create_session(db, title="Drop Test", status="active")
        create_item(db, session_id=s["id"], summary="Active task")
        i2 = create_item(db, session_id=s["id"], summary="Dropped task")
        update_item(db, i2["id"], status="dropped")

        con, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", con):
            from anteroom.cli.mission_cli import _handle_why

            _handle_why(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        # Only the active task should appear
        assert "Active task" in output
        assert "Dropped task" not in output

    def test_all_completed_and_dropped_reports_completed(self, db: Any) -> None:
        """A mission with only completed + dropped items reports all completed with drop count."""
        from anteroom.services.mission_storage import create_item, create_session, update_item

        s = create_session(db, title="Mixed Terminal", status="active")
        i1 = create_item(db, session_id=s["id"], summary="Done task")
        update_item(db, i1["id"], status="completed")
        i2 = create_item(db, session_id=s["id"], summary="Dropped task")
        update_item(db, i2["id"], status="dropped")

        con, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", con):
            from anteroom.cli.mission_cli import _handle_why

            _handle_why(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "all items completed" in output
        assert "1 dropped" in output

    def test_dropped_dependency_not_a_blocker(self, db: Any) -> None:
        """A dropped dependency should not block downstream items."""
        from anteroom.services.mission_storage import add_dependency, create_item, create_session, update_item

        s = create_session(db, title="Dropped Dep", status="active")
        i1 = create_item(db, session_id=s["id"], summary="Dropped upstream")
        update_item(db, i1["id"], status="dropped")
        i2 = create_item(db, session_id=s["id"], summary="Downstream task")
        add_dependency(db, item_id=i2["id"], depends_on_id=i1["id"])

        con, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", con):
            from anteroom.cli.mission_cli import _handle_why

            _handle_why(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        # Downstream should be eligible, not blocked by the dropped item
        assert "Eligible" in output
        assert "Downstream task" in output
        assert "Dropped upstream" not in output.split("Eligible")[0]

    def test_dropped_dependent_not_in_blocking_list(self, db: Any) -> None:
        """A dropped dependent must not appear under the 'Blocking:' label."""
        from anteroom.services.mission_storage import add_dependency, create_item, create_session, update_item

        s = create_session(db, title="Dropped Dependent", status="active")
        i1 = create_item(db, session_id=s["id"], summary="Upstream task")
        i2 = create_item(db, session_id=s["id"], summary="Dropped child")
        add_dependency(db, item_id=i2["id"], depends_on_id=i1["id"])
        update_item(db, i2["id"], status="dropped")

        con, buf = _capture_console()
        with patch("anteroom.cli.mission_cli.console", con):
            from anteroom.cli.mission_cli import _handle_why

            _handle_why(db, _make_args(session_id=s["id"]))
        output = buf.getvalue()
        assert "Dropped child" not in output

    def test_dispatcher_routes_why(self) -> None:
        con, buf = _capture_console()
        config = MagicMock()
        config.app.data_dir = Path("/tmp/test-anteroom-mission-why")
        with (
            patch("anteroom.cli.mission_cli.console", con),
            patch("anteroom.db.get_db", return_value=MagicMock()),
            patch("anteroom.cli.mission_cli._handle_why") as mock_why,
        ):
            from anteroom.cli.mission_cli import _run_mission

            _run_mission(config, _make_args(mission_action="why", session_id="abc"))
        mock_why.assert_called_once()

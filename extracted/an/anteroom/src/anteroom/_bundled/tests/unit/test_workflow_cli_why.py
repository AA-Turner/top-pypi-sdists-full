"""Tests for `aroom workflow why` handler (#1235)."""

from __future__ import annotations

import argparse
from io import StringIO
from pathlib import Path
from typing import Any
from unittest.mock import patch

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


def _create_run(db: Any, **overrides: Any) -> dict[str, Any]:
    from anteroom.services.workflow_storage import create_workflow_run

    defaults: dict[str, Any] = {
        "workflow_id": "test-wf",
        "workflow_version": "1",
        "target_kind": "test",
        "target_ref": "ref-1",
    }
    defaults.update(overrides)
    return create_workflow_run(db, **defaults)


class TestHandleWhy:
    def test_waiting_for_approval(self, db: Any) -> None:
        from anteroom.services.workflow_storage import (
            create_approval_request,
            update_workflow_run,
        )

        run = _create_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_approval")
        create_approval_request(
            db,
            run_id=run["id"],
            step_id="step-a",
            tool_name="bash",
            tool_args={"command": "echo hi"},
            risk_tier="EXECUTE",
        )

        con, buf = _capture_console()
        with patch("anteroom.cli.workflow_cli.console", con):
            from anteroom.cli.workflow_cli import _handle_why

            _handle_why(db, _make_args(run_id=run["id"]))
        output = buf.getvalue()
        assert "Waiting" in output
        assert "approval" in output
        assert "step-a" in output

    def test_waiting_for_input(self, db: Any) -> None:
        from anteroom.services.workflow_storage import (
            create_human_decision,
            update_workflow_run,
        )

        run = _create_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_input")
        create_human_decision(
            db,
            run_id=run["id"],
            step_id="step-b",
            prompt="Choose an option",
            options=[{"id": "a", "label": "Option A"}],
        )

        con, buf = _capture_console()
        with patch("anteroom.cli.workflow_cli.console", con):
            from anteroom.cli.workflow_cli import _handle_why

            _handle_why(db, _make_args(run_id=run["id"]))
        output = buf.getvalue()
        assert "Waiting" in output
        assert "human input" in output

    def test_completed_no_blocker(self, db: Any) -> None:
        from anteroom.services.workflow_storage import update_workflow_run

        run = _create_run(db)
        update_workflow_run(db, run["id"], status="completed")

        con, buf = _capture_console()
        with patch("anteroom.cli.workflow_cli.console", con):
            from anteroom.cli.workflow_cli import _handle_why

            _handle_why(db, _make_args(run_id=run["id"]))
        output = buf.getvalue()
        assert "No active blocker" in output
        assert "completed" in output

    def test_cancelled_no_blocker(self, db: Any) -> None:
        from anteroom.services.workflow_storage import update_workflow_run

        run = _create_run(db)
        update_workflow_run(db, run["id"], status="cancelled")

        con, buf = _capture_console()
        with patch("anteroom.cli.workflow_cli.console", con):
            from anteroom.cli.workflow_cli import _handle_why

            _handle_why(db, _make_args(run_id=run["id"]))
        output = buf.getvalue()
        assert "No active blocker" in output

    def test_failed_with_diagnosis(self, db: Any) -> None:
        from anteroom.services.workflow_storage import update_workflow_run

        run = _create_run(db)
        update_workflow_run(db, run["id"], status="failed", stop_reason="step_failed:lint")

        con, buf = _capture_console()
        with patch("anteroom.cli.workflow_cli.console", con):
            from anteroom.cli.workflow_cli import _handle_why

            _handle_why(db, _make_args(run_id=run["id"]))
        output = buf.getvalue()
        assert "Blocked" in output
        assert "lint" in output
        assert "Because" in output

    def test_running_no_blocker(self, db: Any) -> None:
        from anteroom.services.workflow_storage import update_workflow_run

        run = _create_run(db)
        update_workflow_run(db, run["id"], status="running")

        con, buf = _capture_console()
        with patch("anteroom.cli.workflow_cli.console", con):
            from anteroom.cli.workflow_cli import _handle_why

            _handle_why(db, _make_args(run_id=run["id"]))
        output = buf.getvalue()
        assert "No active blocker" in output
        assert "running" in output

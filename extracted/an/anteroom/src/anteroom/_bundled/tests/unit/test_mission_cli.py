"""Unit tests for the mission CLI handlers."""

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
        with (
            patch("anteroom.cli.mission_cli.console", console),
            patch("anteroom.cli.mission_cli.asyncio.run") as mock_run,
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

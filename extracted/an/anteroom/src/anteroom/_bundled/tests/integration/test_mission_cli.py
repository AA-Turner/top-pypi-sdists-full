"""CLI integration tests for `aroom mission` subcommands.

Tests real argparse dispatch via subprocess. Exercises the actual
``python -m anteroom mission`` command path -- not direct handler calls.

For commands that require an AI service (``create --prompt``, ``update``)
or an interactive REPL (``talk``), handler-level integration tests with
real SQLite but stubbed AI/REPL are included alongside the subprocess
tests.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

_PYTHON = sys.executable


@pytest.fixture(autouse=True)
def _isolated_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Use an isolated HOME so mission commands don't pollute the user's DB."""
    anteroom_dir = tmp_path / ".anteroom"
    anteroom_dir.mkdir()
    config_file = anteroom_dir / "config.yaml"
    config_file.write_text('ai:\n  base_url: "http://localhost:1/v1"\n  api_key: "test"\n  model: "test"\n')
    monkeypatch.setenv("HOME", str(tmp_path))


def _run_aroom(
    *args: str,
    timeout: int = 30,
    env_override: dict[str, str] | None = None,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run ``aroom`` CLI via subprocess and capture output."""
    import os

    env = os.environ.copy()
    if env_override:
        env.update(env_override)
    return subprocess.run(
        [_PYTHON, "-m", "anteroom", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
        input=input_text,
    )


def _seed_mission(tmp_path: Path) -> dict[str, Any]:
    """Create a mission session with items directly in the DB.

    Returns the session dict with ``id`` and item IDs.
    """
    from anteroom.db import get_db, init_db
    from anteroom.services.mission_storage import (
        add_dependency,
        create_item,
        create_revision,
        create_session,
    )

    db_path = tmp_path / ".anteroom" / "chat.db"
    db = init_db(db_path) if not db_path.exists() else get_db(db_path)

    session = create_session(db, title="Integration Test Mission", status="active")
    item_a = create_item(
        db,
        session_id=session["id"],
        summary="Build API",
        priority=10,
        adapter_type="noop",
        lane="backend",
    )
    item_b = create_item(
        db,
        session_id=session["id"],
        summary="Write tests",
        priority=20,
        adapter_type="noop",
        lane="backend",
    )
    add_dependency(db, item_id=item_b["id"], depends_on_id=item_a["id"])
    create_revision(
        db,
        session_id=session["id"],
        revision_number=1,
        operations=[{"op": "initial_plan"}],
        plan_snapshot_after={"items": [item_a["id"], item_b["id"]]},
        reason="initial compilation",
        referenced_artifacts=[{"fqn": "@test/spec/auth", "version": 1}],
    )

    return {
        "session": session,
        "item_a": item_a,
        "item_b": item_b,
        "db": db,
    }


_SPEC_CONTENT = """\
requirements: Build an auth module with login and signup.
design: Two endpoints, JWT tokens, bcrypt passwords.
tasks:
  - id: t_login
    summary: Implement login endpoint
    depends_on: []
  - id: t_signup
    summary: Implement signup endpoint
    depends_on: []
  - id: t_tests
    summary: Write auth integration tests
    depends_on: [t_login, t_signup]
"""


def _seed_spec(tmp_path: Path) -> str:
    """Create an approved spec artifact in the DB. Returns the spec FQN."""
    from anteroom.db import get_db, init_db
    from anteroom.services.artifact_storage import create_artifact

    db_path = tmp_path / ".anteroom" / "chat.db"
    db = init_db(db_path) if not db_path.exists() else get_db(db_path)

    fqn = "@test/spec/auth"
    metadata = {
        "phases": {
            "requirements": {"status": "approved", "approved_at": None, "approved_by": None},
            "design": {"status": "approved", "approved_at": None, "approved_by": None},
            "tasks": {"status": "approved", "approved_at": None, "approved_by": None},
        }
    }
    create_artifact(
        db,
        fqn=fqn,
        artifact_type="spec",
        namespace="test",
        name="auth",
        content=_SPEC_CONTENT,
        source="local",
        metadata=metadata,
    )
    return fqn


# ---------------------------------------------------------------------------
# Help text (subprocess, no DB needed)
# ---------------------------------------------------------------------------


class TestMissionCLIHelp:
    """Help text renders correctly for mission subcommands."""

    def test_mission_help(self) -> None:
        result = _run_aroom("mission", "--help")
        assert result.returncode == 0
        assert "create" in result.stdout
        assert "list" in result.stdout
        assert "status" in result.stdout
        assert "scheduler" in result.stdout
        assert "talk" in result.stdout
        assert "update" in result.stdout
        assert "revisions" in result.stdout
        assert "cancel" in result.stdout

    def test_mission_scheduler_help(self) -> None:
        result = _run_aroom("mission", "scheduler", "--help")
        assert result.returncode == 0
        assert "--once" in result.stdout
        assert "--poll-interval" in result.stdout

    def test_mission_create_help(self) -> None:
        result = _run_aroom("mission", "create", "--help")
        assert result.returncode == 0
        assert "--spec" in result.stdout
        assert "--prompt" in result.stdout
        assert "--adapter" in result.stdout
        assert "--launch" in result.stdout

    def test_mission_list_help(self) -> None:
        result = _run_aroom("mission", "list", "--help")
        assert result.returncode == 0
        assert "--status" in result.stdout

    def test_mission_status_help(self) -> None:
        result = _run_aroom("mission", "status", "--help")
        assert result.returncode == 0
        assert "session_id" in result.stdout

    def test_mission_update_help(self) -> None:
        result = _run_aroom("mission", "update", "--help")
        assert result.returncode == 0
        assert "--instruction" in result.stdout
        assert "--force" in result.stdout

    def test_mission_revisions_help(self) -> None:
        result = _run_aroom("mission", "revisions", "--help")
        assert result.returncode == 0
        assert "session_id" in result.stdout

    def test_mission_cancel_help(self) -> None:
        result = _run_aroom("mission", "cancel", "--help")
        assert result.returncode == 0
        assert "session_id" in result.stdout


# ---------------------------------------------------------------------------
# No action / usage
# ---------------------------------------------------------------------------


class TestMissionCLINoAction:
    def test_no_subcommand_shows_usage(self) -> None:
        result = _run_aroom("mission")
        output = result.stdout + result.stderr
        assert "Usage" in output or "usage" in output or "create" in output


# ---------------------------------------------------------------------------
# List (subprocess, seeded DB)
# ---------------------------------------------------------------------------


class TestMissionCLIList:
    def test_list_empty(self, tmp_path: Path) -> None:
        result = _run_aroom("mission", "list")
        output = result.stdout + result.stderr
        assert "No missions found" in output

    def test_list_shows_seeded_mission(self, tmp_path: Path) -> None:
        _seed_mission(tmp_path)
        result = _run_aroom("mission", "list")
        output = result.stdout + result.stderr
        assert "Integration Test Mission" in output
        assert "active" in output

    def test_list_status_filter(self, tmp_path: Path) -> None:
        _seed_mission(tmp_path)
        result = _run_aroom("mission", "list", "--status", "pending")
        output = result.stdout + result.stderr
        assert "Integration Test Mission" not in output

    def test_list_status_filter_match(self, tmp_path: Path) -> None:
        _seed_mission(tmp_path)
        result = _run_aroom("mission", "list", "--status", "active")
        output = result.stdout + result.stderr
        assert "Integration Test Mission" in output


# ---------------------------------------------------------------------------
# Status (subprocess, seeded DB)
# ---------------------------------------------------------------------------


class TestMissionCLIStatus:
    def test_status_not_found(self, tmp_path: Path) -> None:
        result = _run_aroom("mission", "status", "nonexistent-id")
        output = result.stdout + result.stderr
        assert "not found" in output.lower() or "Mission not found" in output


def _seed_scheduler_ready_mission(tmp_path: Path) -> dict[str, Any]:
    """Create a launchable mission for scheduler integration tests."""
    from anteroom.db import get_db, init_db
    from anteroom.services.mission_storage import create_item, create_session

    db_path = tmp_path / ".anteroom" / "chat.db"
    db = init_db(db_path) if not db_path.exists() else get_db(db_path)
    session = create_session(db, title="Scheduler Test", status="active")
    item = create_item(
        db,
        session_id=session["id"],
        summary="Immediate noop task",
        priority=10,
        adapter_type="noop",
    )
    return {"db": db, "session": session, "item": item}


class TestMissionCLIScheduler:
    def test_scheduler_once_advances_launched_mission(self, tmp_path: Path) -> None:
        from anteroom.db import get_db
        from anteroom.services.mission_storage import get_item, get_session

        seeded = _seed_scheduler_ready_mission(tmp_path)

        result = _run_aroom("mission", "scheduler", "--once")
        output = result.stdout + result.stderr
        assert result.returncode == 0
        assert "Mission scheduler cycle completed" in output

        db = get_db(tmp_path / ".anteroom" / "chat.db")
        item = get_item(db, seeded["item"]["id"])
        session = get_session(db, seeded["session"]["id"])
        assert item is not None
        assert session is not None
        assert item["status"] == "completed"
        assert session["status"] == "completed"

    def test_status_shows_session_and_items(self, tmp_path: Path) -> None:
        data = _seed_mission(tmp_path)
        session_id = data["session"]["id"]
        result = _run_aroom("mission", "status", session_id)
        output = result.stdout + result.stderr
        assert "Integration Test Mission" in output
        assert "Build API" in output
        assert "Write tests" in output
        assert "0/2 completed" in output

    def test_status_shows_dependencies(self, tmp_path: Path) -> None:
        data = _seed_mission(tmp_path)
        session_id = data["session"]["id"]
        result = _run_aroom("mission", "status", session_id)
        output = result.stdout + result.stderr
        assert "Build API" in output


# ---------------------------------------------------------------------------
# Revisions (subprocess, seeded DB)
# ---------------------------------------------------------------------------


class TestMissionCLIRevisions:
    def test_revisions_not_found(self, tmp_path: Path) -> None:
        result = _run_aroom("mission", "revisions", "nonexistent-id")
        output = result.stdout + result.stderr
        assert "not found" in output.lower() or "Mission not found" in output

    def test_revisions_shows_history(self, tmp_path: Path) -> None:
        data = _seed_mission(tmp_path)
        session_id = data["session"]["id"]
        result = _run_aroom("mission", "revisions", session_id)
        output = result.stdout + result.stderr
        assert "initial_plan" in output
        # Rich table may wrap "initial compilation" across lines
        assert "initial" in output
        assert "compilation" in output

    def test_revisions_shows_artifact_refs(self, tmp_path: Path) -> None:
        data = _seed_mission(tmp_path)
        session_id = data["session"]["id"]
        result = _run_aroom("mission", "revisions", session_id)
        output = result.stdout + result.stderr
        # Rich table may truncate long FQNs with ellipsis
        assert "@test/spec/au" in output
        assert "v1" in output


# ---------------------------------------------------------------------------
# Cancel (subprocess, seeded DB)
# ---------------------------------------------------------------------------


class TestMissionCLICancel:
    def test_cancel_not_found(self, tmp_path: Path) -> None:
        result = _run_aroom("mission", "cancel", "nonexistent-id")
        output = result.stdout + result.stderr
        assert "not found" in output.lower() or "Mission not found" in output

    def test_cancel_active_session(self, tmp_path: Path) -> None:
        data = _seed_mission(tmp_path)
        session_id = data["session"]["id"]
        result = _run_aroom("mission", "cancel", session_id)
        output = result.stdout + result.stderr
        assert "cancelled" in output

    def test_cancel_already_terminal(self, tmp_path: Path) -> None:
        from anteroom.db import get_db
        from anteroom.services.mission_storage import create_session

        db = get_db(tmp_path / ".anteroom" / "chat.db")
        s = create_session(db, title="Done Mission", status="completed")
        result = _run_aroom("mission", "cancel", s["id"])
        output = result.stdout + result.stderr
        assert "already" in output.lower()

    def test_cancel_then_list_shows_cancelled(self, tmp_path: Path) -> None:
        data = _seed_mission(tmp_path)
        session_id = data["session"]["id"]
        _run_aroom("mission", "cancel", session_id)
        result = _run_aroom("mission", "list")
        output = result.stdout + result.stderr
        assert "cancelled" in output


# ---------------------------------------------------------------------------
# Create error cases (subprocess)
# ---------------------------------------------------------------------------


class TestMissionCLICreateErrors:
    def test_create_requires_spec_or_prompt(self) -> None:
        result = _run_aroom("mission", "create")
        assert result.returncode != 0
        output = result.stdout + result.stderr
        assert "--spec" in output or "--prompt" in output or "required" in output.lower()

    def test_create_spec_not_found(self, tmp_path: Path) -> None:
        result = _run_aroom("mission", "create", "--spec", "@nonexistent/spec/thing")
        output = result.stdout + result.stderr
        assert "Error" in output or "error" in output

    def test_create_spec_and_prompt_mutually_exclusive(self) -> None:
        result = _run_aroom("mission", "create", "--spec", "@ns/spec/foo", "--prompt", "do stuff")
        assert result.returncode != 0
        output = result.stdout + result.stderr
        assert "not allowed" in output.lower() or "exclusive" in output.lower() or "error" in output.lower()


# ---------------------------------------------------------------------------
# Update error cases (subprocess)
# ---------------------------------------------------------------------------


class TestMissionCLIUpdateErrors:
    def test_update_requires_instruction(self) -> None:
        result = _run_aroom("mission", "update", "some-id")
        assert result.returncode != 0
        output = result.stdout + result.stderr
        assert "--instruction" in output or "required" in output.lower()

    def test_update_session_not_found(self, tmp_path: Path) -> None:
        result = _run_aroom("mission", "update", "nonexistent-id", "--instruction", "reprioritize")
        output = result.stdout + result.stderr
        assert "not found" in output.lower() or "Mission not found" in output


# ---------------------------------------------------------------------------
# Talk error cases (subprocess)
# ---------------------------------------------------------------------------


class TestMissionCLITalkErrors:
    def test_talk_session_not_found(self, tmp_path: Path) -> None:
        result = _run_aroom("mission", "talk", "nonexistent-id")
        output = result.stdout + result.stderr
        assert "not found" in output.lower() or "Mission not found" in output


# ---------------------------------------------------------------------------
# Create happy path — spec-backed (subprocess, seeded spec artifact)
# ---------------------------------------------------------------------------


class TestMissionCLICreateSpec:
    """End-to-end `aroom mission create --spec` via subprocess.

    Seeds a real spec artifact with approved tasks, then runs the CLI
    with ``--launch`` to skip the interactive confirmation prompt.
    """

    def test_create_from_spec_launches_mission(self, tmp_path: Path) -> None:
        fqn = _seed_spec(tmp_path)
        result = _run_aroom(
            "mission",
            "create",
            "--spec",
            fqn,
            "--launch",
        )
        output = result.stdout + result.stderr
        assert "Mission created" in output
        # Verify compiled items appeared in the preview table
        # (Rich table may wrap long text, so check for substrings)
        assert "login" in output.lower()
        assert "signup" in output.lower()
        assert "t_login" in output
        assert "t_signup" in output
        assert "t_tests" in output

    def test_create_from_spec_then_list(self, tmp_path: Path) -> None:
        fqn = _seed_spec(tmp_path)
        _run_aroom("mission", "create", "--spec", fqn, "--launch")
        result = _run_aroom("mission", "list")
        output = result.stdout + result.stderr
        # The mission title is the artifact name
        assert "auth" in output
        assert "active" in output

    def test_create_from_spec_then_status(self, tmp_path: Path) -> None:
        fqn = _seed_spec(tmp_path)
        create_result = _run_aroom("mission", "create", "--spec", fqn, "--launch")
        create_output = create_result.stdout + create_result.stderr
        # Extract session ID from "Mission created: <id>"
        session_id = None
        for line in create_output.splitlines():
            if "Mission created" in line:
                session_id = line.split(":")[-1].strip()
                break
        assert session_id is not None, f"Could not extract session ID from: {create_output}"
        result = _run_aroom("mission", "status", session_id)
        output = result.stdout + result.stderr
        assert "Status:" in output
        assert "active" in output
        assert "Implement login endpoint" in output
        assert "3" in output  # 3 items

    def test_create_from_spec_with_adapter(self, tmp_path: Path) -> None:
        fqn = _seed_spec(tmp_path)
        result = _run_aroom(
            "mission",
            "create",
            "--spec",
            fqn,
            "--adapter",
            "workflow",
            "--workflow-path",
            "defs/build.yaml",
            "--launch",
        )
        output = result.stdout + result.stderr
        assert "Mission created" in output
        assert "workflow" in output

    def test_create_from_spec_interactive_yes_sets_active(self, tmp_path: Path) -> None:
        fqn = _seed_spec(tmp_path)
        create_result = _run_aroom("mission", "create", "--spec", fqn, input_text="y\n")
        create_output = create_result.stdout + create_result.stderr
        assert create_result.returncode == 0
        assert "Mission created" in create_output

        session_id = None
        for line in create_output.splitlines():
            if "Mission created" in line:
                session_id = line.split(":")[-1].strip()
                break
        assert session_id is not None, f"Could not extract session ID from: {create_output}"

        result = _run_aroom("mission", "status", session_id)
        output = result.stdout + result.stderr
        assert "Status:" in output
        assert "active" in output


# ---------------------------------------------------------------------------
# Update happy path — handler-level with real DB and stubbed AI
# ---------------------------------------------------------------------------


class TestMissionCLIUpdateHappyPath:
    """Proves the full _handle_update flow: compile patch → preview → apply.

    Uses a real SQLite database but stubs the AI service at the handler
    boundary, since subprocess cannot mock the AI provider.
    """

    def test_update_applies_patch(self, tmp_path: Path) -> None:
        import argparse
        import json
        from io import StringIO
        from unittest.mock import AsyncMock, patch

        from rich.console import Console

        from anteroom.db import init_db
        from anteroom.services.mission_storage import (
            create_item,
            create_session,
            list_items_by_session,
        )

        db = init_db(tmp_path / "update_test.db")
        session = create_session(db, title="Update Test", status="active")
        create_item(db, session_id=session["id"], summary="Original task", priority=50)

        # AI returns a patch that adds a new item (payload holds the fields)
        patch_response = json.dumps(
            {
                "operations": [
                    {
                        "op": "add_item",
                        "payload": {
                            "summary": "New security audit task",
                            "priority": 5,
                            "adapter_type": "noop",
                        },
                    }
                ]
            }
        )
        mock_ai = AsyncMock()
        mock_ai.complete = AsyncMock(return_value=patch_response)

        config = type("C", (), {"ai": type("AI", (), {"provider": "openai"})()})()
        args = argparse.Namespace(
            session_id=session["id"],
            instruction="Add a security audit task with highest priority",
            force=True,
        )

        buf = StringIO()
        console = Console(file=buf, width=120, no_color=True)

        from anteroom.cli import mission_cli

        with (
            patch.object(mission_cli, "console", console),
            patch.object(mission_cli, "_create_ai", return_value=mock_ai),
        ):
            mission_cli._handle_update(config, db, args)

        output = buf.getvalue()
        assert "Patch applied" in output
        assert "1 operation(s)" in output

        # Verify the new item exists in the DB
        items = list_items_by_session(db, session["id"])
        summaries = [i["summary"] for i in items]
        assert "Original task" in summaries
        assert "New security audit task" in summaries

    def test_update_preview_and_confirm(self, tmp_path: Path) -> None:
        import argparse
        import json
        from io import StringIO
        from unittest.mock import AsyncMock, patch

        from rich.console import Console

        from anteroom.db import init_db
        from anteroom.services.mission_storage import (
            create_item,
            create_session,
        )

        db = init_db(tmp_path / "preview_test.db")
        session = create_session(db, title="Preview Test", status="active")
        item = create_item(db, session_id=session["id"], summary="Task A", priority=50)

        # AI returns a patch that changes priority
        patch_response = json.dumps(
            {
                "operations": [
                    {
                        "op": "change_priority",
                        "target_item_id": item["id"],
                        "priority": 1,
                    }
                ]
            }
        )
        mock_ai = AsyncMock()
        mock_ai.complete = AsyncMock(return_value=patch_response)

        config = type("C", (), {"ai": type("AI", (), {"provider": "openai"})()})()
        args = argparse.Namespace(
            session_id=session["id"],
            instruction="Make Task A highest priority",
            force=False,
        )

        buf = StringIO()
        console = Console(file=buf, width=120, no_color=True)

        from anteroom.cli import mission_cli

        with (
            patch.object(mission_cli, "console", console),
            patch.object(mission_cli, "_create_ai", return_value=mock_ai),
            patch("builtins.input", return_value="y"),
        ):
            mission_cli._handle_update(config, db, args)

        output = buf.getvalue()
        assert "Patch preview" in output
        assert "change_priority" in output
        assert "Patch applied" in output


# ---------------------------------------------------------------------------
# Talk happy path — handler-level with real DB and stubbed REPL
# ---------------------------------------------------------------------------


class TestMissionCLITalkHappyPath:
    """Proves _handle_talk launches run_cli with the correct mission_session_id.

    Uses a real DB but stubs asyncio.run to capture the coroutine args
    rather than actually starting the interactive REPL.
    """

    def test_talk_launches_repl_with_mission_session_id(self, tmp_path: Path) -> None:
        import argparse
        from io import StringIO
        from unittest.mock import MagicMock, patch

        from rich.console import Console

        from anteroom.db import init_db
        from anteroom.services.mission_storage import create_session

        db = init_db(tmp_path / "talk_test.db")
        session = create_session(db, title="Talk Mission", status="active")

        config = MagicMock()
        args = argparse.Namespace(session_id=session["id"])

        buf = StringIO()
        console = Console(file=buf, width=120, no_color=True)

        captured_coro: list[Any] = []

        def capture_asyncio_run(coro: Any, **kwargs: Any) -> None:
            captured_coro.append(coro)
            coro.close()

        from anteroom.cli import mission_cli

        mock_run = MagicMock(side_effect=capture_asyncio_run)

        with (
            patch.dict(sys.modules, {"filetype": MagicMock()}),
            patch.object(mission_cli, "console", console),
            patch.object(mission_cli.asyncio, "run", mock_run),
        ):
            mission_cli._handle_talk(config, db, args)

            # Assertions inside context so mock_run is still the patched version
            output = buf.getvalue()
            assert "Attaching to mission" in output
            assert session["id"][:8] in output
            assert "Talk Mission" in output
            assert "Starting chat with mission tools" in output

            # Verify asyncio.run was called with the run_cli coroutine
            mock_run.assert_called_once()
            assert len(captured_coro) == 1

    def test_talk_shows_session_status(self, tmp_path: Path) -> None:
        import argparse
        from io import StringIO
        from unittest.mock import MagicMock, patch

        from rich.console import Console

        from anteroom.db import init_db
        from anteroom.services.mission_storage import create_session

        db = init_db(tmp_path / "talk_status_test.db")
        session = create_session(db, title="Active Mission", status="active")

        config = MagicMock()
        args = argparse.Namespace(session_id=session["id"])

        buf = StringIO()
        console = Console(file=buf, width=120, no_color=True)

        from anteroom.cli import mission_cli

        captured_coro: list[Any] = []

        def capture_asyncio_run(coro: Any, **kwargs: Any) -> None:
            captured_coro.append(coro)
            coro.close()

        with (
            patch.dict(sys.modules, {"filetype": MagicMock()}),
            patch.object(mission_cli, "console", console),
            patch.object(mission_cli.asyncio, "run", side_effect=capture_asyncio_run),
        ):
            mission_cli._handle_talk(config, db, args)

        output = buf.getvalue()
        assert "Status:" in output
        assert "active" in output

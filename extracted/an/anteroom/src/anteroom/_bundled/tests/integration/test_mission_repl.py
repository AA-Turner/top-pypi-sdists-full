"""Integration tests: /mission REPL command rendering.

Drives _handle_mission_command() with captured Rich Console output,
following the test_repl_specs.py pattern.
"""

from __future__ import annotations

import asyncio
import io
import re
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from anteroom.cli import renderer
from anteroom.cli.repl import _handle_mission_command

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


def _capture(user_input: str, *, cmd: str = "/mission", db: Any, tool_registry: Any = None) -> str:
    buf = io.StringIO()
    console = __import__("rich.console", fromlist=["Console"]).Console(
        file=buf, width=120, force_terminal=True, color_system="truecolor"
    )
    original = renderer.console
    renderer.console = console
    try:
        asyncio.run(_handle_mission_command(user_input, cmd=cmd, db=db, tool_registry=tool_registry))
    finally:
        renderer.console = original
    return _ANSI_RE.sub("", buf.getvalue())


class TestMissionList:
    def test_empty(self, db: Any) -> None:
        output = _capture("/mission list", db=db)
        assert "No missions found" in output

    def test_with_sessions(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session

        s = create_session(db, title="Test Mission", status="active")
        create_item(db, session_id=s["id"], summary="Task 1")
        output = _capture("/mission list", db=db)
        assert "Test Mission" in output
        assert "0/1 items" in output

    def test_missions_alias(self, db: Any) -> None:
        output = _capture("/missions", cmd="/missions", db=db)
        assert "No missions found" in output


class TestMissionStatus:
    def test_not_found(self, db: Any) -> None:
        output = _capture("/mission status nonexistent", db=db)
        assert "not found" in output.lower()

    def test_shows_items(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_item, create_session

        s = create_session(db, title="Status Test", status="active")
        create_item(db, session_id=s["id"], summary="Do the thing", priority=10)
        output = _capture(f"/mission status {s['id']}", db=db)
        assert "Status Test" in output
        assert "Do the thing" in output

    def test_missing_id(self, db: Any) -> None:
        output = _capture("/mission status", db=db)
        assert "Usage" in output


class TestMissionTalk:
    def test_not_found(self, db: Any) -> None:
        registry = MagicMock()
        output = _capture("/mission talk nonexistent", db=db, tool_registry=registry)
        assert "not found" in output.lower()

    def test_registers_tools(self, db: Any) -> None:
        from anteroom.services.mission_storage import create_session
        from anteroom.tools import ToolRegistry

        s = create_session(db, title="Talk Test")
        registry = ToolRegistry()
        output = _capture(f"/mission talk {s['id']}", db=db, tool_registry=registry)
        assert "tools activated" in output.lower() or "Mission tools" in output
        mission_tools = [n for n in registry._definitions if n.startswith("mission_")]
        assert len(mission_tools) == 10

    def test_missing_id(self, db: Any) -> None:
        output = _capture("/mission talk", db=db)
        assert "Usage" in output


class TestMissionUnknown:
    def test_unknown_subcommand(self, db: Any) -> None:
        output = _capture("/mission bogus", db=db)
        assert "Usage" in output or "Unknown" in output


class TestMissionDiscoverability:
    def test_mission_in_command_descriptions(self) -> None:
        """Ensure /mission appears in command descriptions."""
        from anteroom.cli.commands import COMMAND_DESCRIPTIONS

        assert COMMAND_DESCRIPTIONS.get("mission") == "Inspect and manage missions"
        assert COMMAND_DESCRIPTIONS.get("missions") == "List missions"

    def test_mission_in_subcommand_completions(self) -> None:
        """Ensure /mission subcommands appear in tab-completion."""
        from anteroom.cli.commands import SUBCOMMAND_COMPLETIONS

        assert SUBCOMMAND_COMPLETIONS.get("mission") == ["list", "status", "talk"]

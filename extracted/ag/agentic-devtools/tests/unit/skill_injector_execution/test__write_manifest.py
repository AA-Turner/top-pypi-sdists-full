"""Tests for atomically writing the managed README manifest."""

from pathlib import Path

from agentic_devtools.skill_injector_execution import _write_manifest


def test_writes_manifest_content(tmp_path: Path) -> None:
    _write_manifest(tmp_path, [("agent.md", "Agent help")], "agents")

    content = (tmp_path / "agdt.README.md").read_text(encoding="utf-8")
    assert "agent.md" in content
    assert "Agent help" in content

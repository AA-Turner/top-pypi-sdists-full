"""Tests for agentic_devtools.skill_injector._target_dir."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.skill_injector import _target_dir


class TestTargetDir:
    """Tests for the _target_dir helper."""

    def test_flat_kinds_land_under_github(self, tmp_path: Path) -> None:
        """agents and prompts keep their .github/<kind> destination."""
        assert _target_dir(tmp_path, "agents") == tmp_path / ".github" / "agents"
        assert _target_dir(tmp_path, "prompts") == tmp_path / ".github" / "prompts"

    def test_skills_land_in_canonical_skills_path(self, tmp_path: Path) -> None:
        """The skills kind targets the consumer's canonical .agents/skills path."""
        assert _target_dir(tmp_path, "skills") == tmp_path / ".agents" / "skills"

"""Tests for agentic_devtools.skill_injector._resolve_skill_target_path."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.skill_injector import _resolve_skill_target_path


class TestResolveSkillTargetPath:
    """Tests for the _resolve_skill_target_path helper."""

    def test_rejects_invalid_managed_skill_shape(self, tmp_path: Path) -> None:
        """Flat or nested paths outside <skill>/<resource> are rejected."""
        with pytest.raises(OSError, match="Invalid managed skill path"):
            _resolve_skill_target_path(tmp_path, "flat.md")

    def test_rejects_symlinked_destination_file(self, tmp_path: Path) -> None:
        """A symlink file destination is refused."""
        target = tmp_path / "skills"
        skill_dir = target / "my-skill"
        skill_dir.mkdir(parents=True)
        outside = tmp_path / "outside.md"
        outside.write_text("x", encoding="utf-8")
        link = skill_dir / "notes.md"
        try:
            link.symlink_to(outside)
        except OSError:
            pytest.skip("symlink creation not supported on this platform")

        with pytest.raises(OSError, match="symlinked file"):
            _resolve_skill_target_path(target, "my-skill/notes.md")

    def test_rejects_directory_destination(self, tmp_path: Path) -> None:
        """An existing directory at the destination is refused."""
        target = tmp_path / "skills"
        dest_dir = target / "my-skill" / "SKILL.md"
        dest_dir.mkdir(parents=True)

        with pytest.raises(OSError, match="existing directory"):
            _resolve_skill_target_path(target, "my-skill/SKILL.md")

    def test_rejects_non_directory_intermediate_component(self, tmp_path: Path) -> None:
        """A regular file occupying an intermediate path component is refused."""
        target = tmp_path / "skills"
        target.mkdir(parents=True)
        # Create a file where the skill directory should be
        (target / "my-skill").write_text("file, not a dir", encoding="utf-8")

        with pytest.raises(OSError, match="non-directory component"):
            _resolve_skill_target_path(target, "my-skill/SKILL.md")

    def test_rejects_backslash_in_resource_name(self, tmp_path: Path) -> None:
        """A resource name containing backslash is rejected (Windows traversal guard)."""
        with pytest.raises(OSError, match="Invalid managed skill path"):
            _resolve_skill_target_path(tmp_path, "my-skill/x\\..\\..\\other-skill\\SKILL.md")

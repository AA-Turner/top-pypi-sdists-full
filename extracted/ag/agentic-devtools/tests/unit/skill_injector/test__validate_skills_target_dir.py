"""Tests for agentic_devtools.skill_injector._validate_skills_target_dir."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.skill_injector import _validate_skills_target_dir


class TestValidateSkillsTargetDir:
    """Tests for the _validate_skills_target_dir guard."""

    def test_passes_for_plain_nonexistent_target(self, tmp_path: Path) -> None:
        """Validation succeeds when target_dir does not yet exist (first run)."""
        target = tmp_path / "skills"
        _validate_skills_target_dir(target)  # must not raise

    def test_passes_for_plain_existing_target(self, tmp_path: Path) -> None:
        """Validation succeeds when target_dir is a plain directory."""
        target = tmp_path / "skills"
        target.mkdir()
        _validate_skills_target_dir(target)  # must not raise

    def test_rejects_symlinked_target_dir(self, tmp_path: Path) -> None:
        """Raises OSError when target_dir itself is a symlink."""
        real = tmp_path / "real"
        real.mkdir()
        link = tmp_path / "link"
        try:
            link.symlink_to(real, target_is_directory=True)
        except NotImplementedError:
            pytest.skip("symlink creation not supported on this platform")
        with pytest.raises(OSError, match="symlinked component"):
            _validate_skills_target_dir(link)

    def test_rejects_symlinked_target_parent(self, tmp_path: Path) -> None:
        """Raises OSError when the parent of target_dir is a symlink."""
        real = tmp_path / "real"
        real.mkdir()
        link = tmp_path / "link"
        try:
            link.symlink_to(real, target_is_directory=True)
        except NotImplementedError:
            pytest.skip("symlink creation not supported on this platform")
        with pytest.raises(OSError, match="symlinked component"):
            _validate_skills_target_dir(link / "skills")

    def test_rejects_symlinked_manifest_file(self, tmp_path: Path) -> None:
        """Raises OSError when the managed manifest is a symlink."""
        target = tmp_path / "target"
        target.mkdir()
        outside = tmp_path / "outside.md"
        outside.write_text("x", encoding="utf-8")
        manifest = target / "agdt.README.md"
        try:
            manifest.symlink_to(outside)
        except NotImplementedError:
            pytest.skip("symlink creation not supported on this platform")
        with pytest.raises(OSError, match="symlink"):
            _validate_skills_target_dir(target)

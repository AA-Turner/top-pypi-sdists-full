"""Tests for ``_reject_symlinked_artifact``."""

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.scaffold_check_prereqs import _reject_symlinked_artifact


class TestRejectSymlinkedArtifact:
    """_reject_symlinked_artifact raises only for symlinks."""

    def test_raises_for_symlink(self, tmp_path: Path) -> None:
        target = tmp_path / "target.md"
        target.write_text("x", encoding="utf-8")
        link = tmp_path / "link.md"
        link.symlink_to(target)

        with pytest.raises(ValueError, match="Refusing symlinked plan.md"):
            _reject_symlinked_artifact(link, "plan.md")

    def test_raises_for_broken_symlink(self, tmp_path: Path) -> None:
        link = tmp_path / "link.md"
        link.symlink_to(tmp_path / "missing.md")

        with pytest.raises(ValueError, match="Refusing symlinked tasks.md"):
            _reject_symlinked_artifact(link, "tasks.md")

    def test_allows_regular_path(self, tmp_path: Path) -> None:
        path = tmp_path / "plan.md"
        path.write_text("plan", encoding="utf-8")

        _reject_symlinked_artifact(path, "plan.md")

    def test_allows_missing_non_symlink_path(self, tmp_path: Path) -> None:
        _reject_symlinked_artifact(tmp_path / "missing.md", "tasks.md")

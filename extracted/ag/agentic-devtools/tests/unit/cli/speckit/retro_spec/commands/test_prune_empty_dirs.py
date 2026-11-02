"""Tests for _prune_empty_dirs in retro_spec/commands.py."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.retro_spec.commands import _prune_empty_dirs


class TestPruneEmptyDirs:
    """Tests for the _prune_empty_dirs function."""

    def test_removes_empty_directories_until_stop_path(self, tmp_path: Path) -> None:
        """Test that newly-created empty directories are pruned up to specs root."""
        leaf = tmp_path / "100" / "42"
        leaf.mkdir(parents=True)

        _prune_empty_dirs(leaf, stop_at=tmp_path)

        assert not leaf.exists()
        assert not (tmp_path / "100").exists()
        assert tmp_path.exists()

    def test_stops_when_directory_cannot_be_removed(self, tmp_path: Path) -> None:
        """Test that pruning stops cleanly on the first rmdir failure."""
        leaf = tmp_path / "100" / "42"
        leaf.mkdir(parents=True)
        calls: list[Path] = []

        def _failing_rmdir(path: Path) -> None:
            calls.append(path)
            raise OSError("blocked")

        with patch.object(Path, "rmdir", autospec=True, side_effect=_failing_rmdir):
            _prune_empty_dirs(leaf, stop_at=tmp_path)

        assert calls == [leaf]
        assert leaf.exists()
        assert (tmp_path / "100").exists()

"""Tests for validate_checklists._check_collision."""

from agentic_devtools.cli.speckit.validate_checklists import _check_collision


class TestCheckCollision:
    """Verify multi-directory collision detection."""

    def test_path_not_under_checklists_directory_skipped(self) -> None:
        """Paths whose parent is not 'checklists' are ignored."""
        # This exercises the branch where path_obj.parent.name != "checklists"
        paths = [
            "specs/42-feature/other/file.md",
            "specs/42-feature/checklists/checklist.md",
        ]
        # Should not raise — only one spec_dir is found
        _check_collision(paths, 42)

    def test_no_checklists_paths_no_error(self) -> None:
        """Paths with no checklists parent produce no spec_dirs, no error."""
        paths = ["some/random/path.md", "another/path.md"]
        _check_collision(paths, 42)

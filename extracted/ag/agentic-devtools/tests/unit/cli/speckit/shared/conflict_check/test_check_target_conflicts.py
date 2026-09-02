"""Tests for check_target_conflicts in shared/conflict_check.py."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.speckit.shared.conflict_check import Move, check_target_conflicts


class TestCheckTargetConflicts:
    """Tests for the check_target_conflicts function."""

    def test_no_conflicts_when_targets_dont_exist(self, tmp_path: Path) -> None:
        """Test that empty list is returned when no target paths exist."""
        moves = [
            Move(source=tmp_path / "source1", target=tmp_path / "target1", issue_number=1),
            Move(source=tmp_path / "source2", target=tmp_path / "target2", issue_number=2),
        ]
        conflicts = check_target_conflicts(moves)
        assert conflicts == []

    def test_detects_existing_target(self, tmp_path: Path) -> None:
        """Test that existing target paths are detected as conflicts."""
        target = tmp_path / "existing_target"
        target.mkdir()
        moves = [
            Move(source=tmp_path / "source", target=target, issue_number=1),
        ]
        conflicts = check_target_conflicts(moves)
        assert len(conflicts) == 1
        assert str(target) in conflicts[0]

    def test_detects_multiple_conflicts(self, tmp_path: Path) -> None:
        """Test that multiple conflicts are all detected."""
        target1 = tmp_path / "existing1"
        target2 = tmp_path / "existing2"
        target1.mkdir()
        target2.mkdir()
        moves = [
            Move(source=tmp_path / "s1", target=target1, issue_number=1),
            Move(source=tmp_path / "s2", target=tmp_path / "new", issue_number=2),
            Move(source=tmp_path / "s3", target=target2, issue_number=3),
        ]
        conflicts = check_target_conflicts(moves)
        assert len(conflicts) == 2

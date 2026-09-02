"""Tests for _symlinked_target_components in nest/execution.py."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.speckit.nest.execution import _symlinked_target_components
from agentic_devtools.cli.speckit.nest.plan import Move


class TestSymlinkedTargetComponents:
    """Tests for the _symlinked_target_components helper."""

    def test_returns_empty_when_no_symlinks(self, tmp_path: Path) -> None:
        """Returns empty list when target components are all real directories."""
        specs = tmp_path / "specs"
        specs.mkdir()
        parent = specs / "100"
        parent.mkdir()
        target = parent / "200"

        moves = [Move(source=tmp_path / "200-slug", target=target, issue_number=200)]

        assert _symlinked_target_components(moves, specs) == []

    def test_detects_symlinked_parent_directory(self, tmp_path: Path) -> None:
        """A symlinked intermediate directory is detected and returned."""
        specs = tmp_path / "specs"
        specs.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        link = specs / "100"
        link.symlink_to(outside)  # specs/100 -> ../outside

        target = link / "200"
        moves = [Move(source=tmp_path / "200-slug", target=target, issue_number=200)]

        result = _symlinked_target_components(moves, specs)

        assert str(link) in result

    def test_detects_symlinked_target_directory(self, tmp_path: Path) -> None:
        """A symlinked target (the leaf itself) is detected."""
        specs = tmp_path / "specs"
        specs.mkdir()
        parent = specs / "100"
        parent.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        leaf = parent / "200"
        leaf.symlink_to(outside)  # specs/100/200 -> ../outside

        moves = [Move(source=tmp_path / "200-slug", target=leaf, issue_number=200)]

        result = _symlinked_target_components(moves, specs)

        assert str(leaf) in result

    def test_deduplicates_shared_parent_symlinks(self, tmp_path: Path) -> None:
        """A symlinked parent shared by multiple moves is reported only once."""
        specs = tmp_path / "specs"
        specs.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        link = specs / "100"
        link.symlink_to(outside)

        moves = [
            Move(source=tmp_path / "200-slug", target=link / "200", issue_number=200),
            Move(source=tmp_path / "300-slug", target=link / "300", issue_number=300),
        ]

        result = _symlinked_target_components(moves, specs)

        assert result.count(str(link)) == 1

    def test_returns_empty_for_no_moves(self, tmp_path: Path) -> None:
        """Empty plan produces an empty result."""
        specs = tmp_path / "specs"
        specs.mkdir()

        assert _symlinked_target_components([], specs) == []

    def test_checks_additional_hierarchy_targets(self, tmp_path: Path) -> None:
        """Additional hierarchy-only targets are scanned for symlinked ancestors."""
        specs = tmp_path / "specs"
        specs.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        link = specs / "100"
        link.symlink_to(outside)

        result = _symlinked_target_components([], specs, extra_targets=[link / "200"])

        assert result == [str(link)]

    def test_does_not_flag_nonexistent_directories(self, tmp_path: Path) -> None:
        """Path components that do not yet exist are not reported as symlinks."""
        specs = tmp_path / "specs"
        specs.mkdir()
        target = specs / "100" / "200"  # neither 100 nor 200 exist

        moves = [Move(source=tmp_path / "200-slug", target=target, issue_number=200)]

        assert _symlinked_target_components(moves, specs) == []

"""Tests for hierarchy_level_for_path in shared/hierarchy.py."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.speckit.shared.hierarchy import HierarchyLevel, hierarchy_level_for_path


class TestHierarchyLevelForPath:
    """Tests for depth-based hierarchy level mapping."""

    def test_returns_epic_for_depth_zero(self, tmp_path: Path) -> None:
        """Path one level under specs root should map to EPIC."""
        specs_root = tmp_path / "specs"
        epic_dir = specs_root / "100"
        epic_dir.mkdir(parents=True)

        assert hierarchy_level_for_path(epic_dir, specs_root) == HierarchyLevel.EPIC

    def test_returns_feature_for_depth_one(self, tmp_path: Path) -> None:
        """Path two levels under specs root should map to FEATURE."""
        specs_root = tmp_path / "specs"
        feature_dir = specs_root / "100" / "200"
        feature_dir.mkdir(parents=True)

        assert hierarchy_level_for_path(feature_dir, specs_root) == HierarchyLevel.FEATURE

    def test_returns_task_for_depth_two_or_more(self, tmp_path: Path) -> None:
        """Path three or more levels under specs root should map to TASK."""
        specs_root = tmp_path / "specs"
        task_dir = specs_root / "100" / "200" / "300"
        task_dir.mkdir(parents=True)

        assert hierarchy_level_for_path(task_dir, specs_root) == HierarchyLevel.TASK

    def test_returns_task_when_path_is_outside_specs_root(self, tmp_path: Path) -> None:
        """Path outside specs root should use TASK fallback."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        outside_dir = tmp_path / "outside"
        outside_dir.mkdir()

        assert hierarchy_level_for_path(outside_dir, specs_root) == HierarchyLevel.TASK

"""Tests for derive_epic_tree_hierarchy_level function."""

import pytest

from agentic_devtools.epic_tree.normalization_models import (
    EpicTreeHierarchyLevel,
    derive_epic_tree_hierarchy_level,
)


class TestDeriveEpicTreeHierarchyLevel:
    """Tests for depth-to-hierarchy-level derivation."""

    def test_depth_0_returns_epic(self):
        """Depth 0 maps to EPIC."""
        assert derive_epic_tree_hierarchy_level(0) == EpicTreeHierarchyLevel.EPIC

    def test_depth_1_returns_feature(self):
        """Depth 1 maps to FEATURE."""
        assert derive_epic_tree_hierarchy_level(1) == EpicTreeHierarchyLevel.FEATURE

    def test_depth_2_returns_subtask(self):
        """Depth 2 maps to SUBTASK."""
        assert derive_epic_tree_hierarchy_level(2) == EpicTreeHierarchyLevel.SUBTASK

    def test_depth_3_clamped_to_subtask(self):
        """Depth 3 with max_depth=3 clamps to SUBTASK (effective depth 2)."""
        assert derive_epic_tree_hierarchy_level(3, max_depth=3) == EpicTreeHierarchyLevel.SUBTASK

    def test_depth_10_clamped_to_subtask(self):
        """Very deep nodes clamp to SUBTASK."""
        assert derive_epic_tree_hierarchy_level(10, max_depth=3) == EpicTreeHierarchyLevel.SUBTASK

    def test_max_depth_2_clamps_depth_1(self):
        """With max_depth=2, depth 1 clamps to effective depth 1 (FEATURE)."""
        assert derive_epic_tree_hierarchy_level(1, max_depth=2) == EpicTreeHierarchyLevel.FEATURE

    def test_max_depth_2_clamps_depth_2(self):
        """With max_depth=2, depth 2 clamps to effective depth 1 (FEATURE)."""
        assert derive_epic_tree_hierarchy_level(2, max_depth=2) == EpicTreeHierarchyLevel.FEATURE

    def test_max_depth_1_everything_is_epic(self):
        """With max_depth=1, all depths clamp to effective depth 0 (EPIC)."""
        assert derive_epic_tree_hierarchy_level(0, max_depth=1) == EpicTreeHierarchyLevel.EPIC
        assert derive_epic_tree_hierarchy_level(1, max_depth=1) == EpicTreeHierarchyLevel.EPIC
        assert derive_epic_tree_hierarchy_level(5, max_depth=1) == EpicTreeHierarchyLevel.EPIC

    def test_negative_depth_raises_value_error(self):
        """Negative depths are rejected with a clear ValueError."""
        with pytest.raises(ValueError, match="depth must be >= 0"):
            derive_epic_tree_hierarchy_level(-1)

    def test_non_positive_max_depth_raises_value_error(self):
        """Non-positive max_depth values are rejected with a clear ValueError."""
        with pytest.raises(ValueError, match="max_depth must be > 0"):
            derive_epic_tree_hierarchy_level(0, max_depth=0)

    def test_max_depth_exceeds_3_raises_value_error(self):
        """max_depth > 3 is rejected because the schema only supports 3 levels."""
        with pytest.raises(ValueError, match="max_depth must be <= 3"):
            derive_epic_tree_hierarchy_level(0, max_depth=4)

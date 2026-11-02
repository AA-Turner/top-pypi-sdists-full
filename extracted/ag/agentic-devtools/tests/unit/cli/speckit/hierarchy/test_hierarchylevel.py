"""Tests for HierarchyLevel enum."""

import pytest

from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel


class TestHierarchyLevel:
    """Tests for HierarchyLevel enum."""

    def test_epic_value(self):
        """Test EPIC member has value 'epic'."""
        assert HierarchyLevel.EPIC.value == "epic"

    def test_feature_value(self):
        """Test FEATURE member has value 'feature'."""
        assert HierarchyLevel.FEATURE.value == "feature"

    def test_task_value(self):
        """Test TASK member has value 'task'."""
        assert HierarchyLevel.TASK.value == "task"

    def test_construction_from_string_epic(self):
        """Test construction from string 'epic'."""
        assert HierarchyLevel("epic") is HierarchyLevel.EPIC

    def test_construction_from_string_feature(self):
        """Test construction from string 'feature'."""
        assert HierarchyLevel("feature") is HierarchyLevel.FEATURE

    def test_construction_from_string_task(self):
        """Test construction from string 'task'."""
        assert HierarchyLevel("task") is HierarchyLevel.TASK

    def test_invalid_value_raises_valueerror(self):
        """Test that invalid string raises ValueError."""
        with pytest.raises(ValueError):
            HierarchyLevel("milestone")

    def test_has_exactly_three_members(self):
        """Test that enum has exactly 3 members."""
        assert len(HierarchyLevel) == 3

"""Tests for EpicTreeHierarchyLevel enum."""

from agentic_devtools.epic_tree.normalization_models import EpicTreeHierarchyLevel


class TestEpicTreeHierarchyLevel:
    """Tests for the hierarchy level enum values."""

    def test_epic_value(self):
        """EPIC level has value 'epic'."""
        assert EpicTreeHierarchyLevel.EPIC.value == "epic"

    def test_feature_value(self):
        """FEATURE level has value 'feature'."""
        assert EpicTreeHierarchyLevel.FEATURE.value == "feature"

    def test_subtask_value(self):
        """SUBTASK level has value 'subtask'."""
        assert EpicTreeHierarchyLevel.SUBTASK.value == "subtask"

    def test_enum_has_exactly_three_members(self):
        """Enum has exactly EPIC, FEATURE, SUBTASK members."""
        assert len(EpicTreeHierarchyLevel) == 3

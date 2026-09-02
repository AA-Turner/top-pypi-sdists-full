"""Tests for HierarchyLevel enum."""

from agentic_devtools.hierarchy.models import HierarchyLevel


class TestHierarchyLevel:
    """Tests for HierarchyLevel enum values and behavior."""

    def test_epic_value(self) -> None:
        assert HierarchyLevel.EPIC.value == "epic"

    def test_feature_value(self) -> None:
        assert HierarchyLevel.FEATURE.value == "feature"

    def test_task_value(self) -> None:
        assert HierarchyLevel.TASK.value == "task"

    def test_standalone_value(self) -> None:
        assert HierarchyLevel.STANDALONE.value == "standalone"

    def test_all_levels_present(self) -> None:
        levels = {level.value for level in HierarchyLevel}
        assert levels == {"epic", "feature", "task", "standalone"}

    def test_from_value(self) -> None:
        assert HierarchyLevel("epic") is HierarchyLevel.EPIC
        assert HierarchyLevel("feature") is HierarchyLevel.FEATURE
        assert HierarchyLevel("task") is HierarchyLevel.TASK
        assert HierarchyLevel("standalone") is HierarchyLevel.STANDALONE

    def test_invalid_value_raises(self) -> None:
        import pytest

        with pytest.raises(ValueError):
            HierarchyLevel("invalid")

"""Tests for JiraHierarchyDetector class."""

import pytest

from agentic_devtools.cli.speckit.hierarchy import HierarchyDetector
from agentic_devtools.cli.speckit.hierarchy_detector import (
    _JIRA_NOT_IMPLEMENTED_MSG,
    JiraHierarchyDetector,
)


class TestJiraHierarchyDetector:
    """Test suite for JiraHierarchyDetector stub."""

    def test_detect_hierarchy_raises_not_implemented(self) -> None:
        """Verify detect_hierarchy raises NotImplementedError with exact message."""
        detector = JiraHierarchyDetector()
        with pytest.raises(NotImplementedError, match="Jira hierarchy detection"):
            detector.detect_hierarchy("PROJECT-123")

    def test_detect_hierarchy_exact_message(self) -> None:
        """Verify the exact error message string."""
        detector = JiraHierarchyDetector()
        with pytest.raises(NotImplementedError) as exc_info:
            detector.detect_hierarchy("PROJECT-123")
        assert str(exc_info.value) == _JIRA_NOT_IMPLEMENTED_MSG

    def test_get_parent_raises_not_implemented(self) -> None:
        """Verify get_parent raises NotImplementedError with exact message."""
        detector = JiraHierarchyDetector()
        with pytest.raises(NotImplementedError) as exc_info:
            detector.get_parent("arg", key="val")
        assert str(exc_info.value) == _JIRA_NOT_IMPLEMENTED_MSG

    def test_get_children_raises_not_implemented(self) -> None:
        """Verify get_children raises NotImplementedError with exact message."""
        detector = JiraHierarchyDetector()
        with pytest.raises(NotImplementedError) as exc_info:
            detector.get_children("arg", key="val")
        assert str(exc_info.value) == _JIRA_NOT_IMPLEMENTED_MSG

    def test_get_level_raises_not_implemented(self) -> None:
        """Verify get_level raises NotImplementedError with exact message."""
        detector = JiraHierarchyDetector()
        with pytest.raises(NotImplementedError) as exc_info:
            detector.get_level("arg", key="val")
        assert str(exc_info.value) == _JIRA_NOT_IMPLEMENTED_MSG

    def test_build_hierarchy_tree_raises_not_implemented(self) -> None:
        """Verify build_hierarchy_tree raises NotImplementedError with exact message."""
        detector = JiraHierarchyDetector()
        with pytest.raises(NotImplementedError) as exc_info:
            detector.build_hierarchy_tree("arg", key="val")
        assert str(exc_info.value) == _JIRA_NOT_IMPLEMENTED_MSG

    def test_satisfies_hierarchy_detector_protocol(self) -> None:
        """Verify JiraHierarchyDetector satisfies the HierarchyDetector protocol."""
        detector = JiraHierarchyDetector()
        assert isinstance(detector, HierarchyDetector)

    def test_class_docstring_references_parent_field(self) -> None:
        """Verify class docstring references the Jira parent field."""
        assert JiraHierarchyDetector.__doc__ is not None
        assert "parent" in JiraHierarchyDetector.__doc__

    def test_class_docstring_references_epic_link_field(self) -> None:
        """Verify class docstring references customfield_10008."""
        assert JiraHierarchyDetector.__doc__ is not None
        assert "customfield_10008" in JiraHierarchyDetector.__doc__

    def test_detect_hierarchy_docstring_references_hierarchy_node(self) -> None:
        """Verify detect_hierarchy docstring references HierarchyNode."""
        doc = JiraHierarchyDetector.detect_hierarchy.__doc__
        assert doc is not None
        assert "HierarchyNode" in doc

    def test_helper_methods_have_nonempty_docstrings(self) -> None:
        """Verify all helper methods have non-empty docstrings."""
        for method_name in ("get_parent", "get_children", "get_level", "build_hierarchy_tree"):
            method = getattr(JiraHierarchyDetector, method_name)
            assert method.__doc__ is not None
            assert method.__doc__.strip()

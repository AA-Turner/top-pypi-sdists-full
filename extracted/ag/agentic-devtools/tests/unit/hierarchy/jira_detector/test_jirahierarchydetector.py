"""Tests for JiraHierarchyDetector stub."""

import pytest

from agentic_devtools.hierarchy.detector import HierarchyDetector
from agentic_devtools.hierarchy.jira_detector import JiraHierarchyDetector


class TestJiraHierarchyDetector:
    """Tests that JiraHierarchyDetector raises NotImplementedError on all methods."""

    def test_is_subclass_of_abc(self) -> None:
        assert issubclass(JiraHierarchyDetector, HierarchyDetector)

    def test_instantiation_succeeds(self) -> None:
        detector = JiraHierarchyDetector()
        assert isinstance(detector, HierarchyDetector)

    def test_detect_parent_raises(self) -> None:
        detector = JiraHierarchyDetector()
        with pytest.raises(NotImplementedError, match="Jira hierarchy detection"):
            detector.detect_parent(42)

    def test_detect_children_raises(self) -> None:
        detector = JiraHierarchyDetector()
        with pytest.raises(NotImplementedError, match="Jira hierarchy detection"):
            detector.detect_children(42)

    def test_classify_raises(self) -> None:
        detector = JiraHierarchyDetector()
        with pytest.raises(NotImplementedError, match="Jira hierarchy detection"):
            detector.classify(42)

    def test_build_metadata_raises(self) -> None:
        detector = JiraHierarchyDetector()
        with pytest.raises(NotImplementedError, match="Jira hierarchy detection"):
            detector.build_metadata(42)

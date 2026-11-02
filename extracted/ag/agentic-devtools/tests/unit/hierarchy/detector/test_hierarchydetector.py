"""Tests for HierarchyDetector ABC contract."""

import pytest

from agentic_devtools.hierarchy.detector import HierarchyDetector
from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata


class ConcreteDetector(HierarchyDetector):
    """Minimal concrete implementation for testing."""

    def detect_parent(self, issue_number: int) -> int | None:
        return None

    def detect_children(self, issue_number: int) -> list[tuple[int, str]]:
        return []

    def classify(self, issue_number: int) -> HierarchyLevel:
        return HierarchyLevel.STANDALONE

    def build_metadata(self, issue_number: int) -> HierarchyMetadata:
        return HierarchyMetadata(level=HierarchyLevel.STANDALONE)


class IncompleteDetector(HierarchyDetector):
    """Intentionally incomplete — missing abstract methods."""

    def detect_parent(self, issue_number: int) -> int | None:
        return None  # pragma: no cover


class TestHierarchyDetector:
    """Tests for HierarchyDetector ABC contract enforcement."""

    def test_concrete_implementation_instantiates(self) -> None:
        detector = ConcreteDetector()
        assert isinstance(detector, HierarchyDetector)

    def test_cannot_instantiate_abc_directly(self) -> None:
        with pytest.raises(TypeError):
            HierarchyDetector()  # type: ignore[abstract]

    def test_incomplete_implementation_raises(self) -> None:
        with pytest.raises(TypeError):
            IncompleteDetector()  # type: ignore[abstract]

    def test_detect_parent_returns_none(self) -> None:
        detector = ConcreteDetector()
        assert detector.detect_parent(42) is None

    def test_detect_children_returns_empty(self) -> None:
        detector = ConcreteDetector()
        assert detector.detect_children(42) == []

    def test_classify_returns_standalone(self) -> None:
        detector = ConcreteDetector()
        assert detector.classify(42) == HierarchyLevel.STANDALONE

    def test_build_metadata_returns_metadata(self) -> None:
        detector = ConcreteDetector()
        meta = detector.build_metadata(42)
        assert isinstance(meta, HierarchyMetadata)

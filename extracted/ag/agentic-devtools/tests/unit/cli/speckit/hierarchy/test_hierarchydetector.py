"""Tests for HierarchyDetector protocol."""

from agentic_devtools.cli.speckit.hierarchy import (
    ChildEntry,
    HierarchyDetector,
    HierarchyLevel,
    HierarchyNode,
)


class TestHierarchyDetector:
    """Test suite for HierarchyDetector protocol."""

    def test_protocol_is_runtime_checkable(self) -> None:
        """Verify HierarchyDetector is a runtime-checkable Protocol."""

        # A concrete implementation should satisfy the protocol
        class ConcreteDetector:
            def detect_hierarchy(self, issue_key: str) -> HierarchyNode:
                return HierarchyNode(
                    title="Test Issue",
                    level=HierarchyLevel.FEATURE,
                    parent="42",
                    children=[
                        ChildEntry(key="100", title="Child 1", order=1),
                        ChildEntry(key="101", title="Child 2", order=2),
                    ],
                )

        detector = ConcreteDetector()
        assert isinstance(detector, HierarchyDetector)

    def test_protocol_method_signature(self) -> None:
        """Verify the protocol defines the expected method signature."""
        # The protocol should have detect_hierarchy method
        assert hasattr(HierarchyDetector, "detect_hierarchy")

    def test_concrete_implementation_matches_protocol(self) -> None:
        """Verify a concrete implementation can satisfy the protocol contract."""

        class MockDetector:
            def detect_hierarchy(self, issue_key: str) -> HierarchyNode:
                # Minimal implementation for testing protocol compliance
                return HierarchyNode(
                    title=f"Issue {issue_key}",
                    level=HierarchyLevel.TASK,
                    parent=None,
                    children=[],
                )

        detector = MockDetector()
        result = detector.detect_hierarchy("123")

        assert isinstance(result, HierarchyNode)
        assert result.title == "Issue 123"
        assert result.level == HierarchyLevel.TASK
        assert result.parent is None
        assert result.children == []

    def test_protocol_accepts_implementations_with_additional_methods(self) -> None:
        """Verify implementations can have additional methods beyond the protocol."""

        class ExtendedDetector:
            def detect_hierarchy(self, issue_key: str) -> HierarchyNode:
                return HierarchyNode(
                    title="Extended",
                    level=HierarchyLevel.EPIC,
                    parent=None,
                    children=[],
                )

            def additional_method(self) -> str:
                return "extra functionality"

        detector = ExtendedDetector()
        assert isinstance(detector, HierarchyDetector)
        assert detector.additional_method() == "extra functionality"

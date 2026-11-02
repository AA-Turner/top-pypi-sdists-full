"""Tests for CascadeEvent dataclass."""

from agentic_devtools.hierarchy.models import CascadeDirection, CascadeEvent


class TestCascadeEvent:
    """Tests for CascadeEvent construction."""

    def test_parent_to_child(self) -> None:
        event = CascadeEvent(
            source_issue=100,
            target_issue=101,
            direction=CascadeDirection.PARENT_TO_CHILD,
        )
        assert event.source_issue == 100
        assert event.target_issue == 101
        assert event.direction == CascadeDirection.PARENT_TO_CHILD
        assert event.skipped_issues == []

    def test_sibling_to_sibling(self) -> None:
        event = CascadeEvent(
            source_issue=101,
            target_issue=102,
            direction=CascadeDirection.SIBLING_TO_SIBLING,
            skipped_issues=[103],
        )
        assert event.direction == CascadeDirection.SIBLING_TO_SIBLING
        assert event.skipped_issues == [103]

    def test_cascade_direction_values(self) -> None:
        assert CascadeDirection.PARENT_TO_CHILD.value == "parent_to_child"
        assert CascadeDirection.SIBLING_TO_SIBLING.value == "sibling_to_sibling"

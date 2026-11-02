"""Tests for the PropertyChangeResult dataclass."""

from __future__ import annotations

from agentic_devtools.cli.setup.property_change_detection import (
    PropertyChange,
    PropertyChangeResult,
)


class TestPropertyChangeResult:
    """Tests for PropertyChangeResult dataclass fields and defaults."""

    def test_fields_populated(self) -> None:
        """PropertyChangeResult stores merged dict, has_changes flag, and changes list."""
        changes = [PropertyChange(key="a", category="NEW", details={"included_in_template": True})]
        result = PropertyChangeResult(
            merged={"a": {"name": "a", "included_in_template": True}},
            has_changes=True,
            changes=changes,
        )
        assert result.merged == {"a": {"name": "a", "included_in_template": True}}
        assert result.has_changes is True
        assert len(result.changes) == 1

    def test_changes_default_to_empty(self) -> None:
        """Changes default to an empty list when not provided."""
        result = PropertyChangeResult(merged={}, has_changes=False)
        assert result.changes == []

    def test_has_changes_false_for_no_op(self) -> None:
        """has_changes is False when no actual changes detected."""
        result = PropertyChangeResult(merged={}, has_changes=False, changes=[])
        assert result.has_changes is False

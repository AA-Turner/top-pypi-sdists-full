"""Tests for the PropertyChange dataclass."""

from __future__ import annotations

from agentic_devtools.cli.setup.property_change_detection import PropertyChange


class TestPropertyChange:
    """Tests for PropertyChange dataclass fields and defaults."""

    def test_baseline_entry_attribute_is_none(self) -> None:
        """A baseline PropertyChange entry has attribute=None by default."""
        change = PropertyChange(key="summary", category="NEW")
        assert change.key == "summary"
        assert change.category == "NEW"
        assert change.attribute is None
        assert change.details == {}

    def test_attribute_level_entry(self) -> None:
        """An attribute-level entry has a populated attribute field."""
        change = PropertyChange(
            key="priority",
            category="CHANGED",
            attribute="required",
            details={"old": False, "new": True},
        )
        assert change.key == "priority"
        assert change.category == "CHANGED"
        assert change.attribute == "required"
        assert change.details == {"old": False, "new": True}

    def test_details_default_to_empty_dict(self) -> None:
        """Details default to an empty dict when not provided."""
        change = PropertyChange(key="x", category="REMOVED")
        assert change.details == {}

    def test_details_are_independent_instances(self) -> None:
        """Each PropertyChange gets its own details dict instance."""
        a = PropertyChange(key="a", category="NEW")
        b = PropertyChange(key="b", category="NEW")
        a.details["x"] = 1
        assert "x" not in b.details

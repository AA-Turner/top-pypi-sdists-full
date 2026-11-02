"""Tests for ValidationReportEntry dataclass."""

from agentic_devtools.epic_tree.errors import ValidationReportEntry


class TestValidationReportEntry:
    """Tests for ValidationReportEntry equality and fields."""

    def test_equality_same_fields(self):
        """Two entries with identical fields are equal."""
        a = ValidationReportEntry(
            category="cycle_detected",
            message="Cycle found",
            paths=["epic.features[0]", "epic.features[1]"],
            property_name=None,
        )
        b = ValidationReportEntry(
            category="cycle_detected",
            message="Cycle found",
            paths=["epic.features[0]", "epic.features[1]"],
            property_name=None,
        )
        assert a == b

    def test_inequality_different_category(self):
        """Entries with different categories are not equal."""
        a = ValidationReportEntry(category="cycle_detected", message="msg")
        b = ValidationReportEntry(category="duplicate_ref", message="msg")
        assert a != b

    def test_inequality_different_message(self):
        """Entries with different messages are not equal."""
        a = ValidationReportEntry(category="err", message="A")
        b = ValidationReportEntry(category="err", message="B")
        assert a != b

    def test_inequality_different_paths(self):
        """Entries with different paths are not equal."""
        a = ValidationReportEntry(category="err", message="m", paths=["a"])
        b = ValidationReportEntry(category="err", message="m", paths=["b"])
        assert a != b

    def test_equality_with_property_name(self):
        """Entries with matching property_name are equal."""
        a = ValidationReportEntry(category="required", message="missing", paths=["/epic"], property_name="ref")
        b = ValidationReportEntry(category="required", message="missing", paths=["/epic"], property_name="ref")
        assert a == b

    def test_inequality_different_property_name(self):
        """Entries with different property_name are not equal."""
        a = ValidationReportEntry(category="required", message="m", paths=[], property_name="ref")
        b = ValidationReportEntry(category="required", message="m", paths=[], property_name="title")
        assert a != b

    def test_property_name_none_vs_string(self):
        """None property_name is not equal to a string."""
        a = ValidationReportEntry(category="err", message="m", property_name=None)
        b = ValidationReportEntry(category="err", message="m", property_name="x")
        assert a != b

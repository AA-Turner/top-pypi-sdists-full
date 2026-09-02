"""Tests for _entry_sort_key() in errors.py."""

from agentic_devtools.epic_tree.errors import ValidationReportEntry, _entry_sort_key


class TestEntrySortKey:
    """Tests for _entry_sort_key comparison logic."""

    def test_primary_sort_by_path(self):
        """Entries are sorted primarily by first path tokens."""
        entry_a = ValidationReportEntry(category="cycle_detected", message="A", paths=["epic.features[0]"])
        entry_b = ValidationReportEntry(category="cycle_detected", message="B", paths=["epic.features[1]"])
        assert _entry_sort_key(entry_a) < _entry_sort_key(entry_b)

    def test_secondary_sort_by_category(self):
        """Same path → sort by category alphabetically."""
        entry_a = ValidationReportEntry(category="cycle_detected", message="msg", paths=["epic.features[0]"])
        entry_b = ValidationReportEntry(category="duplicate_ref", message="msg", paths=["epic.features[0]"])
        assert _entry_sort_key(entry_a) < _entry_sort_key(entry_b)

    def test_tertiary_sort_by_message(self):
        """Same path and category → sort by message alphabetically."""
        entry_a = ValidationReportEntry(category="duplicate_ref", message="AAA", paths=["epic.features[0]"])
        entry_b = ValidationReportEntry(category="duplicate_ref", message="ZZZ", paths=["epic.features[0]"])
        assert _entry_sort_key(entry_a) < _entry_sort_key(entry_b)

    def test_numeric_index_sort(self):
        """Numeric indices sort numerically, not lexicographically."""
        entry_2 = ValidationReportEntry(category="err", message="msg", paths=["epic.features[2]"])
        entry_10 = ValidationReportEntry(category="err", message="msg", paths=["epic.features[10]"])
        # [2] should come before [10] numerically
        assert _entry_sort_key(entry_2) < _entry_sort_key(entry_10)

    def test_empty_paths(self):
        """Entry with no paths uses empty string as sort key."""
        entry = ValidationReportEntry(category="err", message="msg", paths=[])
        key = _entry_sort_key(entry)
        assert key == ([], "err", "msg")

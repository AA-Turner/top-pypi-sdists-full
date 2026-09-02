"""Tests for _normalize_labels function."""

from agentic_devtools.epic_tree.normalizer import _normalize_labels


class TestNormalizeLabels:
    """Tests for label normalization: trim, lowercase, deduplicate."""

    def test_trim_lowercase_dedup(self):
        """Trims whitespace, lowercases, and deduplicates preserving first occurrence."""
        result = _normalize_labels(["Epic", "EPIC", "epic", "Q3"])
        assert result == ["epic", "q3"]

    def test_whitespace_trimmed(self):
        """Leading/trailing whitespace is trimmed."""
        result = _normalize_labels(["  epic  ", " Feature ", "Q3 "])
        assert result == ["epic", "feature", "q3"]

    def test_preserves_first_occurrence_order(self):
        """Deduplication preserves the order of first occurrence."""
        result = _normalize_labels(["Beta", "alpha", "BETA", "Alpha", "gamma"])
        assert result == ["beta", "alpha", "gamma"]

    def test_empty_list_returns_empty(self):
        """Empty input list returns empty output."""
        result = _normalize_labels([])
        assert result == []

    def test_non_string_items_skipped(self):
        """Non-string items in the list are skipped."""
        result = _normalize_labels(["epic", 42, None, "feature"])  # type: ignore[list-item]
        assert result == ["epic", "feature"]

    def test_whitespace_only_labels_excluded(self):
        """Labels that are only whitespace are excluded."""
        result = _normalize_labels(["  ", "epic", "   "])
        assert result == ["epic"]

"""Tests for DiffLineIndex dataclass (FR-004, SC-002)."""

from agentic_devtools.orchestration.review.line_reference import DiffLineIndex


class TestDiffLineIndex:
    def test_default_fields_are_empty(self):
        index = DiffLineIndex()
        assert index.old_lines == set()
        assert index.new_lines == set()
        assert index.context_pairs == set()

    def test_explicit_values(self):
        index = DiffLineIndex(old_lines={1, 2}, new_lines={3}, context_pairs={(1, 3)})
        assert 2 in index.old_lines
        assert 3 in index.new_lines
        assert (1, 3) in index.context_pairs

"""Tests for _extract_diff_lines_for_content_key function."""

from __future__ import annotations

from agentic_devtools.orchestration.review.content_assembler import _extract_diff_lines_for_content_key


class TestExtractDiffLinesForContentKey:
    """Tests for the diff-line extraction helper."""

    def test_uses_side_specific_keys(self) -> None:
        """Uses addedLines for source and removedLines for target."""
        entry = {
            "addedLines": [{"line": 10}, {"line": 0}, {"line": "11"}, "bad"],
            "removedLines": [{"line": 3}],
        }
        assert _extract_diff_lines_for_content_key(entry, "full_content_source") == [10]
        assert _extract_diff_lines_for_content_key(entry, "full_content_target") == [3]

    def test_returns_empty_for_non_list_container(self) -> None:
        """Non-list addedLines/removedLines returns an empty list."""
        entry = {"addedLines": {"line": 10}}
        assert _extract_diff_lines_for_content_key(entry, "full_content_source") == []

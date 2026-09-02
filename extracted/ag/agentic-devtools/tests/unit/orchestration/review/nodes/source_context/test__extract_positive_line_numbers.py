"""Tests for _extract_positive_line_numbers helper."""

from __future__ import annotations

from agentic_devtools.orchestration.review.nodes.source_context import _extract_positive_line_numbers


class TestExtractPositiveLineNumbers:
    """Tests for _extract_positive_line_numbers."""

    def test_non_list_returns_empty(self) -> None:
        """Non-list diff metadata yields no line numbers."""
        assert _extract_positive_line_numbers({"line": 1}) == []

    def test_skips_non_dict_and_non_positive_entries(self) -> None:
        """Only positive integer line numbers are kept."""
        result = _extract_positive_line_numbers(
            [
                "bad",
                {"line": "5"},
                {"line": -1},
                {"line": 0},
                {"line": None},
                {"line": 3},
                {"line": 9},
            ]
        )
        assert result == [3, 9]

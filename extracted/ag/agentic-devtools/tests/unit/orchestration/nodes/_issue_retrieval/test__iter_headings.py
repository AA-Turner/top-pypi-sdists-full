"""Tests for _iter_headings."""

from __future__ import annotations

from agentic_devtools.orchestration.nodes._issue_retrieval import _iter_headings


class TestIterHeadings:
    """Tests for heading extraction from descriptions."""

    def test_returns_empty_list_for_empty_string(self) -> None:
        assert _iter_headings("") == []

    def test_returns_empty_list_for_no_headings(self) -> None:
        assert _iter_headings("Just some plain text without headings.") == []

    def test_extracts_markdown_h1(self) -> None:
        result = _iter_headings("# Acceptance Criteria")
        assert len(result) == 1
        level, text, _ = result[0]
        assert level == 1
        assert text == "acceptance criteria"

    def test_extracts_markdown_h2(self) -> None:
        result = _iter_headings("## Summary")
        assert len(result) == 1
        level, text, _ = result[0]
        assert level == 2
        assert text == "summary"

    def test_extracts_markdown_multiple_headings(self) -> None:
        desc = "# Overview\n\nSome text.\n\n## Details\n\nMore text.\n\n### Notes"
        result = _iter_headings(desc)
        assert len(result) == 3
        assert result[0][0] == 1
        assert result[1][0] == 2
        assert result[2][0] == 3

    def test_extracts_jira_h3_heading(self) -> None:
        result = _iter_headings("h3. Acceptance Criteria")
        assert len(result) == 1
        level, text, _ = result[0]
        assert level == 3
        assert "acceptance criteria" in text

    def test_strips_jira_inline_markup(self) -> None:
        result = _iter_headings("h2. *Bold Section*")
        assert len(result) == 1
        _, text, _ = result[0]
        assert text == "bold section"

    def test_mixed_markdown_and_jira_headings(self) -> None:
        desc = "# Markdown heading\n\nh2. Jira heading"
        result = _iter_headings(desc)
        assert len(result) == 2

    def test_result_sorted_by_document_position(self) -> None:
        desc = "h2. Second\n\n# First heading appears after in position?"
        result = _iter_headings(desc)
        # sorted by start position — first heading in text is first in result
        assert len(result) == 2
        assert result[0][2].start() < result[1][2].start()

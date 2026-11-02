"""Tests for _first_placeholder_in_span in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _first_placeholder_in_span


class TestFirstPlaceholderInSpan:
    """Tests for _first_placeholder_in_span."""

    def test_returns_index_of_first_match(self) -> None:
        """Returns the first line index containing the placeholder."""
        lines = ["no", "{{url}}", "{{url}}"]
        fence_flags = [False, False, False]
        assert _first_placeholder_in_span(lines, fence_flags, "url", 0, 3, frozenset()) == 1

    def test_returns_none_when_no_match(self) -> None:
        """Returns None when no placeholder is found in the span."""
        lines = ["no match", "also no"]
        fence_flags = [False, False]
        assert _first_placeholder_in_span(lines, fence_flags, "url", 0, 2, frozenset()) is None

    def test_skips_fenced_lines(self) -> None:
        """Lines inside fenced blocks are skipped even if they contain the placeholder."""
        lines = ["```", "{{url}}", "```", "{{url}}"]
        fence_flags = [True, True, True, False]
        assert _first_placeholder_in_span(lines, fence_flags, "url", 0, 4, frozenset()) == 3

    def test_skips_commonmark_indented_lines(self) -> None:
        """Lines indented by 4 spaces (CommonMark code blocks) are skipped."""
        lines = ["    {{url}}", "{{url}}"]
        fence_flags = [False, False]
        assert _first_placeholder_in_span(lines, fence_flags, "url", 0, 2, frozenset()) == 1

    def test_skips_tab_indented_lines(self) -> None:
        """Lines indented by a tab (CommonMark code blocks) are skipped."""
        lines = ["\t{{url}}", "{{url}}"]
        fence_flags = [False, False]
        assert _first_placeholder_in_span(lines, fence_flags, "url", 0, 2, frozenset()) == 1

    def test_respects_span_bounds(self) -> None:
        """Only lines within [start, end) are searched."""
        lines = ["{{url}}", "no", "{{url}}"]
        fence_flags = [False, False, False]
        assert _first_placeholder_in_span(lines, fence_flags, "url", 1, 2, frozenset()) is None

    def test_excluded_fields_block_line(self) -> None:
        """Lines containing co-located excluded placeholders are skipped."""
        lines = ["{{url}} {{title}}", "{{url}}"]
        fence_flags = [False, False]
        assert _first_placeholder_in_span(lines, fence_flags, "url", 0, 2, frozenset({"title"})) == 1

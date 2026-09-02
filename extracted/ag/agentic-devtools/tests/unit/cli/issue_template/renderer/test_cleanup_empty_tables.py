"""Tests for _cleanup_empty_tables in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _cleanup_empty_tables


class TestCleanupEmptyTables:
    """Tests for _cleanup_empty_tables (FR-010 micro-pass 1)."""

    def test_table_with_no_data_rows_removed(self) -> None:
        """Table with only header+separator and no data rows is removed."""
        lines = [
            "## Properties",
            "",
            "| Field | Value |",
            "| --- | --- |",
            "",
            "## Next Section",
        ]
        result = _cleanup_empty_tables(lines)
        assert "| Field | Value |" not in result
        assert "| --- | --- |" not in result
        assert "## Properties" in result
        assert "## Next Section" in result

    def test_table_with_data_rows_preserved(self) -> None:
        """Table with data rows is preserved intact."""
        lines = [
            "| Field | Value |",
            "| --- | --- |",
            "| Priority | High |",
            "| Status | Open |",
        ]
        result = _cleanup_empty_tables(lines)
        assert result == lines

    def test_non_table_content_preserved(self) -> None:
        """Non-table content passes through unchanged."""
        lines = ["# Heading", "", "Some text", "", "More text"]
        result = _cleanup_empty_tables(lines)
        assert result == lines

    def test_multiple_tables_mixed(self) -> None:
        """Multiple tables: empty ones removed, non-empty kept."""
        lines = [
            "| A | B |",
            "| --- | --- |",
            "| data | here |",
            "",
            "| C | D |",
            "| --- | --- |",
            "",
        ]
        result = _cleanup_empty_tables(lines)
        assert "| A | B |" in result
        assert "| data | here |" in result
        assert "| C | D |" not in result

    def test_pipe_in_non_table_context_preserved(self) -> None:
        """Line with | that is not a table header is preserved."""
        lines = [
            "Some text with | pipe",
            "Next line without table separator",
        ]
        result = _cleanup_empty_tables(lines)
        assert result == lines

"""Tests for the ``_escape_cell`` helper."""

from __future__ import annotations

from agentic_devtools.cli.setup.expectations_specializer import _escape_cell


class TestEscapeCell:
    """Verify Markdown escaping for table cell content."""

    def test_backslashes_are_escaped_before_table_delimiters(self) -> None:
        """Existing backslashes are doubled before a pipe is escaped."""
        assert _escape_cell("a\\|b") == "a" + "\\\\" + "\\|" + "b"

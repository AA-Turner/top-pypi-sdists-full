"""Tests for _row_cells in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _row_cells


class TestRowCells:
    """Tests for _row_cells helper."""

    def test_simple_two_column(self) -> None:
        """A two-column row is parsed into exactly two cells."""
        assert _row_cells("| Property | Value |") == ["Property", "Value"]

    def test_three_column(self) -> None:
        """A three-column row is parsed into three cells."""
        assert _row_cells("| A | B | C |") == ["A", "B", "C"]

    def test_escaped_pipe_counts_as_one_cell(self) -> None:
        r"""``\|`` inside a cell is not treated as a delimiter."""
        assert _row_cells(r"| Property \| Name | Value |") == [r"Property \| Name", "Value"]

    def test_escaped_pipe_in_middle_column(self) -> None:
        r"""``\|`` in the middle column does not split the row."""
        assert _row_cells(r"| A | B \| C | D |") == ["A", r"B \| C", "D"]

    def test_even_backslashes_before_pipe_keep_pipe_unescaped(self) -> None:
        r"""An even backslash run before ``|`` keeps the pipe as a delimiter."""
        assert _row_cells(r"| A \\| B | Value |") == [r"A \\", "B", "Value"]

    def test_delimiter_row(self) -> None:
        """A delimiter row with dashes is parsed correctly."""
        assert _row_cells("| --- | --- |") == ["---", "---"]

    def test_trailing_empty_cell_is_preserved(self) -> None:
        """A trailing empty table cell is retained when the row has a delimiter."""
        assert _row_cells("| Field | |") == ["Field", ""]

    def test_empty_row_returns_no_cells(self) -> None:
        """A row with no cell content between the outer pipes returns an empty list."""
        assert _row_cells("||") == []

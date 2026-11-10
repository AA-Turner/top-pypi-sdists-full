# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026, Ansible Project

"""
Code for conversion to (formatted) plain text.
"""

from __future__ import annotations

import math
import typing as t

from docutils import nodes

from ._table import Cell as _Cell
from ._table import TableHelper as _TableHelper
from ._text_context import Context as _Context
from ._utils import DocumentContextBase as _DocumentContextBase

_Class = t.TypeVar("_Class")
_DocumentContext = t.TypeVar("_DocumentContext", bound=_DocumentContextBase)


class BaseTranslator(nodes.NodeVisitor, t.Generic[_DocumentContext]):
    """
    Base class for translator that has access to the document context.
    """

    def __init__(self, document, document_context: _DocumentContext):
        super().__init__(document)
        self._context = document_context


class TableRenderer:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """
    Render a table as text.
    """

    def __init__(
        self, *, table: nodes.table, destination: _Context, visitor: BaseTranslator
    ) -> None:
        self.table = table
        self.destination = destination
        self.visitor = visitor
        helper = _TableHelper(table=table)
        self.title = helper.title
        self.col_specs = helper.col_specs
        self.row_matrix = helper.row_matrix
        self.cells = helper.cells
        self.header_rows = helper.header_rows
        self._horizontal_padding = 1
        self._vertical_padding = 0

    def _get_maximum_column_widths(self) -> list[int]:
        # pylint: disable-next=fixme
        # TODO: use values in self.col_specs
        cols = len(self.col_specs)
        frame_width = cols * (1 + 2 * self._horizontal_padding) + 1
        max_content_width = self.destination.remaining_width - frame_width
        w = max(1, max_content_width // cols) if cols else 1
        return [w] * cols

    def _prerender_cell(self, *, cell: _Cell, max_col_widths: list[int]) -> int:
        # Compute max width
        width = 0
        for col in range(cell.begin_col, cell.end_col + 1):
            width += max_col_widths[col]
        width += (cell.end_col - cell.begin_col) * (1 + 2 * self._horizontal_padding)

        # Compute content lines
        top = _Context(
            remaining_width=width,
            state=self.destination.state.clone(),
            string_proc=self.destination.string_proc,
            ignore_newlines=True,
        )
        # pylint: disable-next=protected-access
        with self.visitor._context.with_fake_top(fake_top=top):
            cell.entry.walkabout(self.visitor)
        top.close()

        # Add content lines
        padding = " " * self._horizontal_padding
        for _ in range(self._vertical_padding):
            cell.lines.append(padding * 2)
        for line in top.get_lines():
            cell.lines.append(f"{padding}{line}{padding}")
        for _ in range(self._vertical_padding):
            cell.lines.append(padding * 2)

        # Compute maximum width
        return (
            max(
                self.destination.string_proc.get_column_count(text=line)
                for line in cell.lines
            )
            if cell.lines
            else 0
        )

    def _prerender_title(self, *, max_width: int) -> list[str]:
        if self.title is None:
            return []

        # Compute content lines
        top = _Context(
            remaining_width=max_width,
            state=self.destination.state.clone(),
            string_proc=self.destination.string_proc,
            ignore_newlines=True,
        )
        # pylint: disable-next=protected-access
        with self.visitor._context.with_fake_top(fake_top=top):
            for node in self.title:
                node.walkabout(self.visitor)
        top.close()

        return top.get_lines()

    def _position_cols(self, *, act_col_widths: list[int]) -> list[int]:
        result = [0] * (len(act_col_widths) + 1)
        for col, width in enumerate(act_col_widths):
            result[col + 1] = result[col] + 1 + max(width, 2 * self._horizontal_padding)
        return result

    def _position_rows(self) -> list[int]:
        result = [0] * (len(self.row_matrix) + 1)
        for row_idx, row in enumerate(self.row_matrix):
            result[row_idx + 1] = result[row_idx] + 1
            for cell in row:
                if cell is not None and cell.begin_row == row_idx:
                    result[cell.end_row + 1] = max(
                        result[cell.end_row + 1], result[row_idx] + 1 + len(cell.lines)
                    )
        return result

    def _render_line(self, *, content: list[tuple[int, str]]) -> str:
        content.sort()
        result = []
        width = 0
        for position, text in content:
            if position > width:
                result.append(" " * (position - width))
                width = position
            elif position < width:
                raise ValueError(  # pragma: no cover
                    f"Bad content, overlap at {position}: {content}"
                )
            result.append(text)
            width += self.destination.string_proc.get_column_count(text=text)
        return "".join(result)

    @staticmethod
    def _get_box_drawing(
        *,
        has_above: bool = False,
        has_below: bool = False,
        has_left: bool = False,
        has_right: bool = False,
        header_sep: bool,
    ) -> str:
        index = (
            (0 if has_above else 8)
            + (0 if has_below else 4)
            + (0 if has_left else 2)
            + (0 if has_right else 1)
        )
        if header_sep:
            return "╪╡╞│╧╛╘╵╤╕╒╷═╴╶ "[index]
        return "┼┤├│┴┘└╵┬┐┌╷─╴╶ "[index]

    def _render_lines(
        self,
        *,
        line_content: list[list[tuple[int, str]]],
        has_right: bool,
        has_below: bool,
        row: int,
        ridx: int,
        col: int,
        cidx: int,
        cols: list[int],
        rows: list[int],
        is_header_sep: bool,
    ) -> None:
        if has_right:
            line_content[row].append(
                (
                    col + 1,
                    self._get_box_drawing(
                        has_left=True,
                        has_right=True,
                        header_sep=is_header_sep,
                    )
                    * (cols[cidx + 1] - col - 1),
                )
            )
        if has_below:
            c = self._get_box_drawing(has_above=True, has_below=True, header_sep=False)
            for r in range(row + 1, rows[ridx + 1]):
                line_content[r].append((col, c))

    def _render_frame(
        self,
        *,
        line_content: list[list[tuple[int, str]]],
        rows: list[int],
        cols: list[int],
    ) -> None:
        for ridx, row in enumerate(rows):
            has_row_before = ridx > 0
            has_row_after = ridx + 1 < len(rows)
            is_header_sep = ridx == self.header_rows
            for cidx, col in enumerate(cols):
                has_col_before = cidx > 0
                has_col_after = cidx + 1 < len(cols)
                c11 = (
                    self.row_matrix[ridx - 1][cidx - 1]
                    if has_col_before and has_row_before
                    else None
                )
                c12 = (
                    self.row_matrix[ridx - 1][cidx]
                    if has_col_after and has_row_before
                    else None
                )
                c21 = (
                    self.row_matrix[ridx][cidx - 1]
                    if has_col_before and has_row_after
                    else None
                )
                has_above = has_row_before
                has_below = has_row_after
                has_left = has_col_before
                has_right = has_col_after
                if c11 and c11.end_col >= cidx:
                    has_above = False
                if c21 and c21.end_col >= cidx:
                    has_below = False
                if c11 and c11.end_row >= ridx:
                    has_left = False
                if c12 and c12.end_row >= ridx:
                    has_right = False
                if has_above or has_below or has_left or has_right:
                    line_content[row].append(
                        (
                            col,
                            self._get_box_drawing(
                                has_above=has_above,
                                has_below=has_below,
                                has_left=has_left,
                                has_right=has_right,
                                header_sep=is_header_sep,
                            ),
                        )
                    )
                    self._render_lines(
                        line_content=line_content,
                        has_right=has_right,
                        has_below=has_below,
                        row=row,
                        ridx=ridx,
                        col=col,
                        cidx=cidx,
                        cols=cols,
                        rows=rows,
                        is_header_sep=is_header_sep,
                    )

    def _render_cells(
        self,
        *,
        line_content: list[list[tuple[int, str]]],
        rows: list[int],
        cols: list[int],
    ) -> None:
        for cell in self.cells:
            start_row = rows[cell.begin_row] + 1
            start_col = cols[cell.begin_col] + 1
            for index, line in enumerate(cell.lines):
                line_content[start_row + index].append((start_col, line))

    def _render_table(
        self, *, rows: list[int], cols: list[int], title_lines: list[str]
    ) -> list[str]:
        line_content: list[list[tuple[int, str]]] = [[] for _ in range(rows[-1] + 1)]
        self._render_frame(line_content=line_content, rows=rows, cols=cols)
        self._render_cells(line_content=line_content, rows=rows, cols=cols)
        lines = [self._render_line(content=content) for content in line_content]
        lines.extend(title_lines)
        return lines

    def render(self) -> None:
        """
        Render the table.
        """
        max_col_widths = self._get_maximum_column_widths()
        act_col_widths = [0] * len(max_col_widths)
        for cell in self.cells:
            cell_width = self._prerender_cell(cell=cell, max_col_widths=max_col_widths)
            # pylint: disable-next=fixme
            # TODO: do this more weighted to avoid unnecessary space for a column
            col_width = math.ceil(cell_width / (cell.end_col - cell.begin_col + 1))
            for col in range(cell.begin_col, cell.end_col + 1):
                act_col_widths[col] = max(act_col_widths[col], col_width)
        cols = self._position_cols(act_col_widths=act_col_widths)
        rows = self._position_rows()
        title_lines = self._prerender_title(max_width=self.destination.remaining_width)
        lines = self._render_table(rows=rows, cols=cols, title_lines=title_lines)
        self.destination.main.add_raw_lines(lines)

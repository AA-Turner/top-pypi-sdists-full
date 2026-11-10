# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026, Ansible Project

"""
Table helpers.
"""

from __future__ import annotations

import dataclasses
import typing as t

from docutils import nodes

_Class = t.TypeVar("_Class")


@dataclasses.dataclass
class Cell:
    """
    Layout information of a cell.
    """

    begin_row: int
    begin_col: int
    end_row: int
    end_col: int
    entry: nodes.entry
    lines: list[str]


def _find_child(node: nodes.Element, *, clazz: type[_Class]) -> _Class | None:
    for child in node:
        if isinstance(child, clazz):
            return child
    return None


class TableHelper:  # pylint: disable=too-few-public-methods
    """
    Extract data from a table, including the cell layout.
    """

    def __init__(self, *, table: nodes.table) -> None:
        self.table = table
        self.title: nodes.title | None = None
        self.col_specs: list[int] = []
        self.row_matrix: list[list[Cell | None]] = []
        self.cells: list[Cell] = []
        self.header_rows: int = 0
        self._collect()

    def _get_matrix_row(self, row: int) -> list[Cell | None]:
        while row >= len(self.row_matrix):
            self.row_matrix.append([None] * len(self.col_specs))
        return self.row_matrix[row]

    def _collect(self) -> None:
        for child in self.table:
            if isinstance(child, nodes.title):
                self.title = child
            if isinstance(child, nodes.tgroup):
                for c in child:
                    if isinstance(c, nodes.colspec):
                        self.col_specs.append(max(1, c.get("colwidth", 0)))
                while child["cols"] > len(self.col_specs):
                    self.col_specs.append(1)
                next_row = 0
                thead = _find_child(child, clazz=nodes.thead)
                next_row = self._collect_rows(next_row, thead, header=True)
                self.header_rows = next_row
                if next_row < len(self.row_matrix) and any(
                    elt is not None for elt in self.row_matrix[next_row]
                ):
                    raise ValueError(  # pragma: no cover
                        f"Bad table: expected {next_row} to be empty after header,"
                        f" but found {self.row_matrix[next_row]}"
                    )
                tbody = _find_child(child, clazz=nodes.tbody)
                next_row = self._collect_rows(next_row, tbody, header=False)

    def _collect_rows(
        self, next_row: int, elt: nodes.thead | nodes.tbody | None, *, header: bool
    ) -> int:
        if elt is None:
            return next_row
        for row_idx, row in enumerate(elt):
            if not isinstance(row, nodes.row):
                raise ValueError(  # pragma: no cover
                    f"Bad table: expected row, got {row}"
                )

            # Place entries
            col = 0
            m_row = self._get_matrix_row(next_row)
            for entry in row:
                if not isinstance(entry, nodes.entry):
                    raise ValueError(  # pragma: no cover
                        f"Bad table: expected entry, got {entry}"
                    )
                col = self._collect_cell(
                    entry=entry,
                    next_row=next_row,
                    row_idx=row_idx,
                    col=col,
                    m_row=m_row,
                    header=header,
                )

            # Find next free row index
            next_row += 1
            while next_row < len(self.row_matrix):
                if any(elt is None for elt in self.row_matrix[next_row]):
                    break
                next_row += 1
        return next_row

    def _collect_cell(
        self,
        *,
        entry: nodes.entry,
        next_row: int,
        row_idx: int,
        col: int,
        m_row: list[Cell | None],
        header: bool,
    ) -> int:
        # Find next free column index
        while col < len(m_row):
            if m_row[col] is None:
                break
            col += 1
        if col == len(m_row):
            raise ValueError(  # pragma: no cover
                f"Bad table: found cell {entry} in row {next_row} (row #{row_idx} in"
                f" {'header' if header else 'table body'}) that does not fit into this row."
            )

        # Create cell
        cell = Cell(
            begin_row=next_row,
            begin_col=col,
            end_row=next_row + entry.get("morerows", 0),
            end_col=col + entry.get("morecols", 0),
            entry=entry,
            lines=[],
        )
        self.cells.append(cell)

        # Place cell, and check for collisions
        for r in range(cell.begin_row, cell.end_row + 1):
            rr = self._get_matrix_row(r)
            for c in range(cell.begin_col, cell.end_col + 1):
                if rr[c] is not None:
                    raise ValueError(  # pragma: no cover
                        f"Bad table: cell {cell} collides with existing entry"
                        f" {rr[c]} in row {r} / col {c}"
                    )
                rr[c] = cell
        return col

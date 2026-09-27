"""GFM table lines — the Python twin of THE TypeScript table rule.

THE rule lives in matrx-frontend: the one row splitter
(``components/rich-editor/core/table-source.ts`` ``splitRowSegments`` / ``rowCells``),
the one cell-pipe rule (``components/markdown-core/syntax/gfm-cell-pipes.ts``)
and where a table starts and runs (``processors/utils/gfm-table-lines.ts``).
This module mirrors it and is held to it by shared vectors
(``tests/test_gfm_table_vectors.py``; verify-RC-B4 R5-2 / R5-3).

- A ``|`` is a cell boundary unless an ODD run of backslashes precedes it.
- A table starts at a header holding an unescaped pipe whose NEXT line is a
  delimiter row (``--- | :-:``, edge pipes optional) of the same width; it runs
  to a blank line or a line that starts another block.
- A cell's ``\\|`` shows as ``|`` — inside code spans too.
"""

from __future__ import annotations

import re

# A line GFM reads as the start of another block (list item, quote, heading, fence, rule).
_BLOCK_START = re.compile(
    r"^(?:[-+*](?:\s|$)|\d{1,9}[.)](?:\s|$)|>|#{1,6}(?:\s|$)|```|~~~|(?:-\s*){3,}$|(?:\*\s*){3,}$|(?:_\s*){3,}$)"
)
_DELIMITER_CELL = re.compile(r"^:?-+:?$")
# JS String.prototype.trim() whitespace — Python's str.strip() also strips a few
# separators JS does not, so cells are trimmed with this exact class.
_JS_TRIM_EDGES = re.compile(
    r"^[\s﻿\xa0  -     　]+|[\s﻿\xa0  -     　]+$"
)


def _trim(text: str) -> str:
    return _JS_TRIM_EDGES.sub("", text)


def split_row_segments(line: str) -> list[str]:
    """The row's bytes between boundaries (edge segments included)."""
    segments: list[str] = []
    start = 0
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "\\":
            i += 2  # the escaped character is never a boundary
            continue
        if ch == "|":
            segments.append(line[start:i])
            start = i + 1
        i += 1
    segments.append(line[start:])
    return segments


def row_cells(line: str) -> list[str]:
    """A row's cell texts as GFM reads them (source bytes, trimmed; edge pipes dropped)."""
    cells = [_trim(cell) for cell in split_row_segments(line)]
    if len(cells) > 1 and cells[0] == "":
        cells.pop(0)
    if len(cells) > 1 and cells[-1] == "":
        cells.pop()
    elif len(cells) == 1 and cells[0] == "":
        cells.pop()
    return cells


def unescape_cell_pipes(cell: str) -> str:
    """GFM's table-level unescape: a cell's ``\\|`` is a pipe, in code spans too."""
    return cell.replace("\\|", "|")


def is_gfm_delimiter_row(line: str) -> bool:
    """Every cell ``---``, ``:--``, ``--:`` or ``:-:``, with at least one pipe."""
    trimmed = _trim(line)
    if "|" not in trimmed:
        return False
    cells = row_cells(trimmed)
    return len(cells) > 0 and all(_DELIMITER_CELL.match(cell) for cell in cells)


def starts_pipeless_table(header: str, delimiter: str | None) -> bool:
    """True when ``header`` + ``delimiter`` open a table whose header has NO leading pipe."""
    head = _trim(header)
    if not head or head.startswith("|") or _BLOCK_START.match(head):
        return False
    if len(split_row_segments(head)) < 2:
        return False
    if delimiter is None or not is_gfm_delimiter_row(delimiter):
        return False
    return len(row_cells(head)) == len(row_cells(_trim(delimiter)))


def continues_table(line: str) -> bool:
    """GFM's rule (spec example 202): a table runs to the first blank line or the
    first line that starts another block; any other line is a row, with or
    without a pipe. Twin of content-ir ``continuesTable`` (verify-RC-B4 R7-2)."""
    trimmed = _trim(line)
    if not trimmed:
        return False
    return trimmed.startswith("|") or not _BLOCK_START.match(trimmed)


def is_pipe_led_row(line: str) -> bool:
    """A pipe-led row: ``|`` first and another ``|`` after it."""
    trimmed = _trim(line)
    return trimmed.startswith("|") and "|" in trimmed[1:]


def opens_table(lines: list[str], index: int) -> bool:
    """Line ``index`` opens a table: a pipe-led row, or a pipe-less GFM header over its delimiter row."""
    line = lines[index] if 0 <= index < len(lines) else ""
    following = lines[index + 1] if index + 1 < len(lines) else None
    return is_pipe_led_row(line) or starts_pipeless_table(line, following)

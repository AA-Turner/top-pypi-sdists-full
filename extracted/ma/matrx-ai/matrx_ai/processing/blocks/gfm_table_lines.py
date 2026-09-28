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
  to a blank line, a line that starts another block (an HTML block included —
  CommonMark 4.6's seven start conditions), or a line indented 4+ columns past
  the table's container (indented code). A lone ``|`` is a row (one empty cell).
- A cell's ``\\|`` shows as ``|`` — inside code spans too.
"""

from __future__ import annotations

import re

# A line GFM reads as the start of another block (list item, quote, heading, fence, rule).
_BLOCK_START = re.compile(
    # A fence: ``~~~…``, or a backtick run of 3+ whose info string holds no backtick
    # (CommonMark 4.5 — "```` code ```` | b" is a code span opening a row).
    # A footnote definition (``[^1]: …``, GFM) is a block start too: it ends a table.
    r"^(?:[-+*](?:\s|$)|\d{1,9}[.)](?:\s|$)|>|#{1,6}(?:\s|$)|`{3,}[^`]*$|~{3,}|(?:-\s*){3,}$|(?:\*\s*){3,}$|(?:_\s*){3,}$|\[\^[^\]\s]+\]:)"
)
# CommonMark 4.6 HTML block start conditions (0.31, as micromark reads them) —
# twin of content-ir ``startsHtmlBlock``.
_HTML_RAW = re.compile(r"^<(?:script|pre|style|textarea)(?:[\s>]|$)", re.IGNORECASE)
_HTML_COMMENT_ETC = re.compile(r"^(?:<!--|<\?|<![A-Za-z]|<!\[CDATA\[)")
_HTML_BLOCK_NAMES = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt"
    "|fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main"
    "|menu|menuitem|nav|noframes|ol|optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead"
    "|title|tr|track|ul"
)
_HTML_BLOCK_TAG = re.compile(r"^</?(?:" + _HTML_BLOCK_NAMES + r")(?:[\s>]|/>|$)", re.IGNORECASE)
# THE ONE DELIBERATE GFM DEVIATION (verify-RC-B4 round 16 ruling: content never
# silently disappears) — twin of content-ir ``STRIPPED_HTML_BLOCK_NAMES``. Type-6
# names every surface's sanitizer drops; a block opened by one ends at its own
# line, so the lines after it read as ordinary markdown.
_STRIPPED_HTML_BLOCK_NAMES = (
    "address|article|aside|base|basefont|body|center|dialog|dir|fieldset|footer|form|frame|frameset|head|header"
    "|html|iframe|legend|link|main|menu|menuitem|nav|noframes|optgroup|option|param|search|title|track"
)
_STRIPPED_HTML_BLOCK_TAG = re.compile(r"^</?(?:" + _STRIPPED_HTML_BLOCK_NAMES + r")(?:[\s>]|/>|$)", re.IGNORECASE)
_ATTRIBUTE = r"""\s+[A-Za-z_:][A-Za-z0-9_.:-]*(?:\s*=\s*(?:[^\s"'=<>`]+|'[^']*'|"[^"]*"))?"""
_HTML_COMPLETE_TAG = re.compile(
    r"^(?:<[A-Za-z][A-Za-z0-9-]*(?:" + _ATTRIBUTE + r")*\s*/?>|</[A-Za-z][A-Za-z0-9-]*\s*>)\s*$"
)
_LIST_MARKER = re.compile(r"^([ \t]*)([-+*]|\d{1,9}[.)])([ \t]+|$)")
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
    elif len(cells) == 1 and cells[0] == "" and "|" not in line:
        # A line with no cell at all is no row; a lone ``|`` IS a row (one empty cell).
        cells.pop()
    return cells


def unescape_cell_pipes(cell: str) -> str:
    """GFM's table-level unescape: a cell's ``\\|`` is a pipe, in code spans too."""
    return cell.replace("\\|", "|")


_HTML_BLOCK_NAME_SET = frozenset(
    ["script", "pre", "style", "textarea"]
    + _HTML_BLOCK_NAMES.replace("h[1-6]", "h1|h2|h3|h4|h5|h6").split("|")
)


def is_html_block_tag_name(name: str) -> bool:
    """A tag CommonMark reads as an HTML BLOCK when it opens a line (conditions 1
    and 6; case-insensitive) — twin of content-ir ``isHtmlBlockTagName``."""
    return name.lower() in _HTML_BLOCK_NAME_SET


def starts_html_block(trimmed: str) -> bool:
    """The trimmed line starts an HTML block (any of CommonMark 4.6's seven conditions)."""
    if not trimmed.startswith("<"):
        return False
    return bool(
        _HTML_RAW.match(trimmed)
        or _HTML_COMMENT_ETC.match(trimmed)
        or _HTML_BLOCK_TAG.match(trimmed)
        or _HTML_COMPLETE_TAG.match(trimmed)
    )


def _starts_block(trimmed: str) -> bool:
    return bool(_BLOCK_START.match(trimmed)) or starts_html_block(trimmed)


def line_indent(line: str) -> int:
    """The column a line's content starts at: a space counts 1, a tab runs to the next multiple of 4."""
    column = 0
    for ch in line:
        if ch == " ":
            column += 1
        elif ch == "\t":
            column += 4 - (column % 4)
        else:
            break
    return column


def _marker_content_column(marker: re.Match[str]) -> int:
    """A list item's content column: after the marker and 1-4 spaces (1 when 5+, or when empty)."""
    marker_end = line_indent(marker.group(1)) + len(marker.group(2))
    gap = line_indent(" " * marker_end + marker.group(3)) - marker_end if marker.group(3) else 1
    return marker_end + (gap if 1 <= gap <= 4 else 1)


def table_container_indent(lines: list[str], start: int) -> int:
    """The content column of the list item the table header at ``start`` sits in, or 0
    at top level (twin of content-ir ``tableContainerIndent``)."""
    return _container_indent_of(lines, start, own_item=False)


def _container_indent_of(lines: list[str], start: int, *, own_item: bool) -> int:
    own = _LIST_MARKER.match(lines[start]) if own_item and 0 <= start < len(lines) else None
    if own:
        return _marker_content_column(own)
    header = line_indent(lines[start] if 0 <= start < len(lines) else "")
    if header == 0:
        return 0
    for k in range(start - 1, -1, -1):
        line = lines[k]
        if not line.strip():
            continue
        indent = line_indent(line)
        marker = _LIST_MARKER.match(line)
        if marker and indent < header:
            content = _marker_content_column(marker)
            if content <= header:
                return content
            continue
        if indent == 0:
            return 0
    return 0


def is_gfm_delimiter_row(line: str) -> bool:
    """Every cell ``---``, ``:--``, ``--:`` or ``:-:``, with at least one pipe."""
    trimmed = _trim(line)
    if "|" not in trimmed:
        return False
    cells = row_cells(trimmed)
    return len(cells) > 0 and all(_DELIMITER_CELL.match(cell) for cell in cells)


def _is_table_delimiter(line: str | None) -> bool:
    """A delimiter row GFM reads as one — never a list item such as ``- | -``."""
    if line is None or not is_gfm_delimiter_row(line):
        return False
    return not _BLOCK_START.match(_trim(line))


def starts_pipeless_table(header: str, delimiter: str | None) -> bool:
    """True when ``header`` + ``delimiter`` open a table whose header is NOT a pipe-led
    row: ``a | b``, ``| a`` (one pipe) or even ``Notes`` (no pipe — one column)."""
    head = _trim(header)
    if not head or is_pipe_led_row(head) or (not head.startswith("|") and _starts_block(head)):
        return False
    if not _is_table_delimiter(delimiter):
        return False
    return len(row_cells(head)) == len(row_cells(_trim(delimiter or "")))


def continues_table(line: str, container_indent: int = 0) -> bool:
    """GFM's rule (spec example 202): a table runs to the first blank line, the
    first line that starts another block (an HTML block included), or the first
    line indented 4+ columns past the table's container; any other line is a row,
    with or without a pipe. Twin of content-ir ``continuesTable`` (verify-RC-B4)."""
    trimmed = _trim(line)
    if not trimmed:
        return False
    if line_indent(line) - container_indent >= 4:
        return False
    return trimmed.startswith("|") or not _starts_block(trimmed)


def find_table_end(lines: list[str], start: int) -> int:
    """Index just past the table whose header is at ``start`` (twin of content-ir ``findTableEnd``)."""
    container = table_container_indent(lines, start)
    end = min(len(lines), start + 2)
    while end < len(lines) and continues_table(lines[end], container):
        end += 1
    return end


def is_pipe_led_row(line: str) -> bool:
    """A pipe-led row: ``|`` first and another ``|`` after it."""
    trimmed = _trim(line)
    return trimmed.startswith("|") and "|" in trimmed[1:]


_QUOTE_LINE = re.compile(r"^ {0,3}>")
_THEMATIC_BREAK = re.compile(r"^(?:(?:-[ \t]*){3,}|(?:\*[ \t]*){3,}|(?:_[ \t]*){3,})$")
_HEADING = re.compile(r"^#{1,6}(?:\s|$)")
_FENCE = re.compile(r"^(?:`{3,}[^`]*$|~{3,})")


def _breaks_paragraph(trimmed: str) -> bool:
    """Heading, rule, fence or HTML block: ends a paragraph above without joining it."""
    return bool(
        _HEADING.match(trimmed) or _THEMATIC_BREAK.match(trimmed) or _FENCE.match(trimmed)
    ) or starts_html_block(trimmed)


_UNSET = object()


def _html_block_end(trimmed: str) -> object:
    """The end marker of HTML block types 1-5; None for types 6-7 (end at a blank
    line); _UNSET when the line starts no HTML block (twin of content-ir ``htmlBlockEnd``)."""
    if _HTML_RAW.match(trimmed):
        return re.compile(r"</(?:script|pre|style|textarea)>", re.IGNORECASE)
    if trimmed.startswith("<!--"):
        return re.compile(r"-->")
    if trimmed.startswith("<?"):
        return re.compile(r"\?>")
    if trimmed.startswith("<![CDATA["):
        return re.compile(r"\]\]>")
    if re.match(r"^<![A-Za-z]", trimmed):
        return re.compile(r">")
    if _HTML_BLOCK_TAG.match(trimmed) or _HTML_COMPLETE_TAG.match(trimmed):
        return None
    return _UNSET


def _inside_html_block(lines: list[str], index: int) -> bool:
    """Line ``index`` sits inside an HTML block opened above it in the same run of
    lines — raw HTML to GFM, never a table (twin of content-ir ``insideHtmlBlock``)."""
    start = index
    while start > 0 and _trim(lines[start - 1]):
        start -= 1
    open_end: object = _UNSET
    paragraph = False
    for k in range(start, index):
        line = lines[k]
        if open_end is not _UNSET:
            if open_end is not None and open_end.search(line):  # type: ignore[union-attr]
                open_end = _UNSET
            continue
        trimmed = _trim(line)
        end = _html_block_end(trimmed) if line_indent(line) < 4 else _UNSET
        type7 = end is None and not _HTML_BLOCK_TAG.match(trimmed)
        interrupts = end is not _UNSET and not (paragraph and type7)
        if not interrupts:
            paragraph = True
            continue
        paragraph = False
        # A block whose element every sanitizer strips ends at its own line (the one
        # deliberate GFM deviation, _STRIPPED_HTML_BLOCK_NAMES).
        if opens_stripped_html_block(trimmed):
            continue
        if end is not None and end.search(trimmed[2:]):  # type: ignore[union-attr]
            open_end = _UNSET
        else:
            open_end = end
    return open_end is not _UNSET


def opens_stripped_html_block(trimmed: str) -> bool:
    """The trimmed line opens an HTML block whose element every sanitizer strips: the
    block ends at this line (twin of content-ir ``opensStrippedHtmlBlock``)."""
    return bool(_STRIPPED_HTML_BLOCK_TAG.match(trimmed))


def _is_lazy_continuation(lines: list[str], index: int) -> bool:
    """Line ``index`` lazily continues a list item's or quote's paragraph (twin of
    content-ir ``isLazyContinuation``) — GFM reads it as paragraph text, never a table."""
    header = lines[index]
    first = -1
    for k in range(index - 1, -1, -1):
        line = lines[k]
        trimmed = _trim(line)
        if not trimmed or _breaks_paragraph(trimmed):
            break
        marker = _LIST_MARKER.match(line)
        if marker:
            rest = _trim(line[marker.end():])
            if not rest or _breaks_paragraph(rest):
                break
            first = k
            break
        first = k
        if _QUOTE_LINE.match(line):
            break
    if first < 0:
        return False
    start = lines[first]
    if _QUOTE_LINE.match(start):
        return not _QUOTE_LINE.match(header)
    return line_indent(header) < _container_indent_of(lines, first, own_item=True)


def opens_table(lines: list[str], index: int) -> bool:
    """Line ``index`` opens a table: a pipe-led row, or a pipe-less GFM header over its
    delimiter row — never a lazy continuation of a list item's or quote's paragraph."""
    line = lines[index] if 0 <= index < len(lines) else ""
    following = lines[index + 1] if index + 1 < len(lines) else None
    if not (is_pipe_led_row(line) or starts_pipeless_table(line, following)):
        return False
    return not _is_lazy_continuation(lines, index) and not _inside_html_block(lines, index)


def table_starts_at(lines: list[str], index: int) -> bool:
    """A WHOLE table header at ``index`` (twin of content-ir ``tableStartsAt``): a table
    opens here, the next line is a same-width GFM delimiter row (never a list item),
    and the header is not indented code past its container."""
    if not opens_table(lines, index):
        return False
    delimiter = lines[index + 1] if index + 1 < len(lines) else None
    if not _is_table_delimiter(delimiter):
        return False
    if len(row_cells(lines[index])) != len(row_cells(delimiter or "")):
        return False
    return line_indent(lines[index]) - table_container_indent(lines, index) < 4

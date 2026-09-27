"""Table parser — parses markdown tables into structured data."""

from __future__ import annotations

from matrx_ai.processing.blocks.gfm_table_lines import is_gfm_delimiter_row, row_cells
from matrx_ai.processing.blocks.models.table import TableBlockData


def parse_table(content: str, *, is_final: bool = False) -> TableBlockData | None:
    """
    Parse a markdown table into headers and rows.

    During streaming (is_final=False) the last content line may be a partial
    row still being written by the LLM. We withhold it and only include rows
    that are confirmed complete — a row is complete when a subsequent line has
    arrived after it (forward-trigger rule). On finalize (is_final=True) the
    last row is included unconditionally.
    """
    try:
        lines = [line.strip() for line in content.strip().split("\n") if line.strip()]
        if len(lines) < 2:
            return None

        if "|" not in lines[0]:
            return None
        headers = _parse_row(lines[0])
        if not headers:
            return None

        # Second line is the delimiter row — GFM's rule, edge pipes optional.
        if not is_gfm_delimiter_row(lines[1]):
            return None

        data_lines = lines[2:]

        # During streaming, exclude the last line — it may be mid-write.
        # A row is "sealed" only once the next line has arrived after it.
        if not is_final and data_lines:
            data_lines = data_lines[:-1]

        # Every row GFM shows is kept (an all-empty row is a row); only a trailing
        # line with no cells at all (a lone `|` still arriving) waits — the twin of
        # matrx-frontend parseMarkdownTable.
        rows: list[list[str]] = [_parse_row(line) for line in data_lines]
        if rows and not rows[-1]:
            rows.pop()

        is_complete = "</table>" in content or is_final
        return TableBlockData(
            headers=headers,
            rows=rows,
            is_complete=is_complete,
            raw_markdown=content,
        )
    except Exception:
        return None


def _parse_row(line: str) -> list[str]:
    """A row's cells by THE GFM splitter: an escaped ``\\|`` stays in its cell,
    edge pipes are optional (twin of matrx-frontend ``rowCells``)."""
    return row_cells(line)

"""Table parser — parses markdown tables into structured data."""

from __future__ import annotations

import re

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
        lines = [l.strip() for l in content.strip().split("\n") if l.strip()]
        if len(lines) < 2:
            return None

        headers = _parse_row(lines[0])
        if not headers:
            return None

        # Second line should be separator
        if not re.match(r'^\|[:\s|\-]+\|?$', lines[1]):
            return None

        data_lines = lines[2:]

        # During streaming, exclude the last line — it may be mid-write.
        # A row is "sealed" only once the next line has arrived after it.
        if not is_final and data_lines:
            data_lines = data_lines[:-1]

        rows: list[list[str]] = []
        for line in data_lines:
            cells = _parse_row(line)
            if cells:
                rows.append(cells)

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
    """Parse a table row into cells."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    # Split by | and strip empty first/last
    cells = stripped.split("|")
    # Remove first and last empty strings from leading/trailing |
    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [c.strip() for c in cells]

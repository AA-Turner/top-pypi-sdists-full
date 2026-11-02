"""One primitive for "rows -> GitHub-pipe-table markdown".

Every codec that turns tabular data into markdown (docx/pptx/xlsx tables, the
PDF table-extraction fallback) had its own hand-rolled copy of this loop, each
subtly different in how it escaped cells, sized the separator, and handled a
single/empty/ragged table. They are now ONE function.

Pure format primitive — no host, no ORM, no sibling imports. Resolves in the
bare independence venv. Callers pre-trim cell length (cap is NOT this module's
job); this module owns escaping (``|`` and newlines) and table shape.
"""

from __future__ import annotations


def md_escape(cell: str) -> str:
    """Escape one cell for a markdown pipe-table: neutralize the column
    delimiter, flatten newlines to spaces, and trim. Tolerates ``None``."""
    return (cell or "").replace("|", "\\|").replace("\n", " ").strip()


def rows_to_markdown(rows: list[list[str]], *, header: bool = True) -> str:
    """Render a list of cell-rows as a GitHub-pipe-table.

    - Row 0 is treated as the header when ``header=True`` (a ``| --- |``
      separator is emitted after it); with ``header=False`` all rows are body
      rows and no separator is written.
    - Every row is padded to the widest row so ragged input stays well-formed.
    - Each cell is escaped via :func:`md_escape` — callers must NOT pre-escape
      (that would double-escape), but SHOULD pre-trim cell length.
    - An empty / all-empty table returns ``""``.
    """
    if not rows:
        return ""
    width = max((len(r) for r in rows), default=0)
    if width == 0:
        return ""

    def _fmt(row: list[str]) -> str:
        cells = [md_escape(c) for c in row]
        if len(cells) < width:
            cells = cells + [""] * (width - len(cells))
        return "| " + " | ".join(cells) + " |"

    if header:
        sep = "| " + " | ".join(["---"] * width) + " |"
        lines = [_fmt(rows[0]), sep, *[_fmt(r) for r in rows[1:]]]
    else:
        lines = [_fmt(r) for r in rows]
    return "\n".join(lines)


__all__ = ["rows_to_markdown", "md_escape"]

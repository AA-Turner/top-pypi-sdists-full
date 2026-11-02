"""Native table extraction via PyMuPDF ``page.find_tables()``.

PyMuPDF 1.23+ ships a port of pdfplumber's table-finding algorithm under
``Page.find_tables()``. We use that instead of tabula-py — no Java required,
no subprocess, one library to install.

Outputs:

- ``extract_tables_structured`` → typed ``PdfTablesReport`` carrying every
  detected table with its page, bbox, header row, full rows, and a Markdown
  rendering. This is what callers should prefer.
- ``extract_tables`` → file-on-disk helper (CSV / JSON) that wraps the
  structured call. Preserved for the ``/utilities/pdf/extract-tables``
  legacy contract.

Both surfaces expose async siblings.
"""

from __future__ import annotations

import csv
import json
import os
import re
from collections.abc import AsyncIterator, Callable
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from ...table_markdown import rows_to_markdown
from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf
from ..models import PdfExtractStart
from ..stream_bridge import iter_sync_stream


class PdfTableCell(BaseModel):
    """One row of an extracted table."""

    cells: list[str | None]


class PdfTableBbox(BaseModel):
    """Bbox of a detected table on the page (PDF coordinates)."""

    x0: float = Field(description="Left edge, in PDF points from the page's left.")
    y0: float = Field(description="Top edge, in PDF points from the page's top.")
    x1: float = Field(description="Right edge, in PDF points from the page's left.")
    y1: float = Field(description="Bottom edge, in PDF points from the page's top.")


class PdfExtractedTable(BaseModel):
    """One table detected on one page."""

    page_number: int = Field(ge=1, description="1-based page the table was found on.")
    table_index: int = Field(
        ge=0, description="0-based index of the table on its page (top-to-bottom)."
    )
    bbox: PdfTableBbox = Field(description="Where the table sits on the page.")
    row_count: int = Field(description="Number of rows, including the header row.")
    column_count: int = Field(description="Number of columns.")
    header: list[str | None] = Field(
        description=(
            "Auto-detected header row (PyMuPDF's heuristic). May be empty if "
            "the table has no clear header."
        )
    )
    rows: list[list[str | None]] = Field(
        description=(
            "Every row, in reading order. Each row is a list of cell strings — "
            "``None`` for empty cells."
        )
    )
    markdown: str = Field(
        description="The table rendered as a Markdown pipe table — convenient for prompts."
    )


class PdfTablesReport(BaseModel):
    """Wire shape for ``POST /utilities/pdf/extract-tables``."""

    page_count: int
    tables: list[PdfExtractedTable]
    detector: str = "pymupdf.find_tables"
    detector_version: str = "v1"


class PdfTablesPageScanned(BaseModel):
    """Per-page progress marker yielded by ``extract_tables_structured_stream``
    after every page has been scanned — fires even when the page has no
    tables so a long document never looks stalled."""

    page_number: int
    tables_found: int


def _extract_table_rows(table: Any) -> tuple[list[list[str | None]], list[str | None]]:
    """Pull the row matrix + header from a PyMuPDF table object.

    PyMuPDF's table API gives us `table.extract()` (rows of strings) and
    `table.header.names` (header strings); both can be missing in edge
    cases so we defend with sensible defaults.
    """
    try:
        raw_rows = table.extract() or []
    except Exception:
        raw_rows = []
    rows: list[list[str | None]] = []
    for r in raw_rows:
        rows.append([
            None if (c is None or (isinstance(c, str) and c.strip() == "")) else str(c)
            for c in r
        ])

    header_names: list[str | None] = []
    try:
        header_obj = getattr(table, "header", None)
        names = getattr(header_obj, "names", None) if header_obj else None
        if names:
            header_names = [None if n is None else str(n) for n in names]
    except Exception:
        pass

    return rows, header_names


def _table_markdown(table: Any) -> str:
    """Best-effort markdown rendering — falls back to a manual pipe table
    if the installed PyMuPDF doesn't expose ``to_markdown()``.
    """
    try:
        md = table.to_markdown()  # type: ignore[attr-defined]
        if isinstance(md, str):
            return md
    except Exception:
        pass
    rows, header = _extract_table_rows(table)
    if not rows and not header:
        return ""
    if not header and rows:
        header = [f"col {i + 1}" for i in range(len(rows[0]))]
    # Header as row 0; rows_to_markdown owns escaping, padding, and the separator.
    return rows_to_markdown([header, *rows], header=True)


def extract_tables_structured(
    pdf_bytes: bytes | None = None,
    *,
    path: str | os.PathLike[str] | None = None,
    pages: list[int] | None = None,
    on_open: Callable[[int], None] | None = None,
    on_page: Callable[[int, int], None] | None = None,
    on_table: Callable[[PdfExtractedTable], None] | None = None,
) -> PdfTablesReport:
    """Detect every table across the PDF using PyMuPDF ``find_tables()``.

    Pass *pdf_bytes* OR *path* — exactly one. Optionally constrain to a
    subset of 1-based page numbers.

    ``on_open`` / ``on_page`` / ``on_table`` are optional sync progress hooks
    called from the scan loop (``on_open`` with the page count the moment the
    document opens, ``on_table`` with each detected table, ``on_page`` with
    ``(page_number, tables_found)`` after every page). They exist so callers
    can stream progress in real time — see ``extract_tables_structured_stream``.
    """
    if (pdf_bytes is None) == (path is None):
        raise ValueError(
            "extract_tables_structured requires exactly one of pdf_bytes / path."
        )

    pymupdf = load_pymupdf()
    if pdf_bytes is not None:
        ctx = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    else:
        ctx = pymupdf.open(str(path))

    with ctx as doc:
        page_count = doc.page_count
        if on_open is not None:
            on_open(page_count)
        page_iter = (
            range(1, page_count + 1)
            if pages is None
            else [p for p in pages if 1 <= p <= page_count]
        )
        out: list[PdfExtractedTable] = []
        for page_no in page_iter:
            page = doc[page_no - 1]
            try:
                tabs = page.find_tables()
            except Exception as exc:
                # Pages where the table-finder fails (e.g. weird content
                # streams) shouldn't kill the whole report.
                print(
                    f"[matrx-pdf-tables] page {page_no} find_tables failed: {exc}"
                )
                if on_page is not None:
                    on_page(page_no, 0)
                continue
            found_on_page = 0
            for idx, table in enumerate(tabs.tables or []):
                rows, header = _extract_table_rows(table)
                bbox = table.bbox if hasattr(table, "bbox") else None
                if bbox is None:
                    continue
                row_count = len(rows)
                column_count = max((len(r) for r in rows), default=len(header))
                extracted = PdfExtractedTable(
                    page_number=page_no,
                    table_index=idx,
                    bbox=PdfTableBbox(
                        x0=float(bbox[0]),
                        y0=float(bbox[1]),
                        x1=float(bbox[2]),
                        y1=float(bbox[3]),
                    ),
                    row_count=row_count,
                    column_count=column_count,
                    header=header,
                    rows=rows,
                    markdown=_table_markdown(table),
                )
                out.append(extracted)
                found_on_page += 1
                if on_table is not None:
                    on_table(extracted)
            if on_page is not None:
                on_page(page_no, found_on_page)
        return PdfTablesReport(page_count=page_count, tables=out)


async def extract_tables_structured_async(
    pdf_bytes: bytes | None = None,
    *,
    path: str | os.PathLike[str] | None = None,
    pages: list[int] | None = None,
) -> PdfTablesReport:
    return await run_in_cpu_executor(
        lambda: extract_tables_structured(pdf_bytes, path=path, pages=pages)
    )


async def extract_tables_structured_stream(
    pdf_bytes: bytes | None = None,
    *,
    path: str | os.PathLike[str] | None = None,
    pages: list[int] | None = None,
) -> AsyncIterator[
    PdfExtractStart | PdfTablesPageScanned | PdfExtractedTable | PdfTablesReport
]:
    """Stream table detection as it happens: yields one ``PdfExtractStart``
    (page count) the moment the document opens, each ``PdfExtractedTable`` as
    it is detected, a ``PdfTablesPageScanned`` after every page, and finally
    the complete ``PdfTablesReport``.

    Runs the whole sync scan on ONE executor worker (PyMuPDF thread-safety);
    items cross to the event loop live via ``iter_sync_stream``.
    """

    def _work(emit: Callable[[object], None]) -> None:
        report = extract_tables_structured(
            pdf_bytes,
            path=path,
            pages=pages,
            on_open=lambda total: emit(PdfExtractStart(total_pages=total)),
            on_page=lambda page_no, found: emit(
                PdfTablesPageScanned(page_number=page_no, tables_found=found)
            ),
            on_table=emit,
        )
        emit(report)

    async for item in iter_sync_stream(run_in_cpu_executor, _work):
        yield item  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Legacy file-output helper (kept for backwards compatibility with
# `_handler.extract_tables` callers that expect a string path).
# ---------------------------------------------------------------------------


def _write_csv(report: PdfTablesReport, out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for table in report.tables:
            writer.writerow(
                [
                    f"# page {table.page_number} · table {table.table_index + 1}"
                ]
            )
            if table.header:
                writer.writerow([h or "" for h in table.header])
            for row in table.rows:
                writer.writerow([c or "" for c in row])
            writer.writerow([])


def _write_json(report: PdfTablesReport, out_path: Path) -> None:
    out_path.write_text(
        json.dumps(report.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def extract_tables(
    path: str,
    output_format: str = "csv",
    out_dir: str | os.PathLike[str] | None = None,
    report: PdfTablesReport | None = None,
) -> str | None:
    """File-on-disk wrapper around ``extract_tables_structured``.

    Writes a single CSV or JSON file capturing every detected table.
    Returns the absolute path, or ``None`` when no tables were found
    (legacy callers that pre-date the structured shape rely on the None
    sentinel).

    Pass *report* when the caller has ALREADY run the structured extraction
    (``docproc.pdf.extract_tables`` does, so it can return the tables
    themselves) — table detection is the expensive half and must not run
    twice for one request.
    """
    fmt = output_format.lower().strip() or "csv"
    if fmt not in {"csv", "json"}:
        raise ValueError(f"output_format must be 'csv' or 'json'; got {fmt!r}.")
    if report is None:
        report = extract_tables_structured(path=path)
    if not report.tables:
        return None

    base_name = re.sub(r"[^\w\-]", "_", Path(path).stem)
    out_filename = f"{base_name}_tables.{fmt}"
    target_dir = Path(out_dir) if out_dir else Path(path).parent
    target_dir.mkdir(parents=True, exist_ok=True)
    out_path = target_dir / out_filename
    if fmt == "csv":
        _write_csv(report, out_path)
    else:
        _write_json(report, out_path)
    return str(out_path)


async def extract_tables_async(
    path: str,
    output_format: str = "csv",
    out_dir: str | os.PathLike[str] | None = None,
    report: PdfTablesReport | None = None,
) -> str | None:
    return await run_in_cpu_executor(extract_tables, path, output_format, out_dir, report)


__all__ = [
    "PdfTableCell",
    "PdfTableBbox",
    "PdfExtractedTable",
    "PdfTablesReport",
    "PdfTablesPageScanned",
    "extract_tables",
    "extract_tables_async",
    "extract_tables_structured",
    "extract_tables_structured_async",
    "extract_tables_structured_stream",
]

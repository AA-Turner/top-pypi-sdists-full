"""Multi-column reading-order extractor.

PyMuPDF's ``get_text("text", sort=True)`` does a single-column geometric
sort which interleaves text on multi-column legal/medical pages. This
module clusters blocks by their left-edge x-coordinate to detect columns,
sorts each column top-to-bottom, and emits the blocks left-to-right.
"""

from __future__ import annotations

import statistics
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass

from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf
from ..models import PdfExtractStart
from ..stream_bridge import iter_sync_stream
from .models import ReadingOrderBlock, ReadingOrderPage, ReadingOrderReport


@dataclass
class _RawBlock:
    x0: float
    y0: float
    x1: float
    y1: float
    text: str


def _cluster_columns(blocks: list[_RawBlock], page_width: float) -> list[list[_RawBlock]]:
    """Group blocks into vertical columns by left-edge clustering.

    Single-column pages always return one bucket. For multi-column docs we
    use a simple gap-based clusterer over the sorted left-edges: if the
    delta between adjacent x0 medians is > 12% of the page width, treat
    them as separate columns.
    """
    if not blocks:
        return []
    if page_width <= 0:
        return [blocks]
    x0_sorted = sorted(blocks, key=lambda b: b.x0)
    gap_threshold = page_width * 0.12

    columns: list[list[_RawBlock]] = [[x0_sorted[0]]]
    last_x0 = x0_sorted[0].x0
    for block in x0_sorted[1:]:
        if block.x0 - last_x0 > gap_threshold:
            columns.append([block])
        else:
            columns[-1].append(block)
        last_x0 = block.x0

    # Sort each column by y0, then sort columns by their median x0
    for col in columns:
        col.sort(key=lambda b: b.y0)
    columns.sort(key=lambda col: statistics.median(b.x0 for b in col))
    return columns


def extract_reading_order(
    pdf_bytes: bytes,
    on_open: Callable[[int], None] | None = None,
    on_page: Callable[[ReadingOrderPage], None] | None = None,
) -> ReadingOrderReport:
    """Build a per-page reading-order block list.

    Heuristic — for serious cases (academic papers with three columns, legal
    docs with footnote columns) consider routing through Docling via the
    Phase 7 ``LayoutProvider`` Protocol.

    ``on_open`` / ``on_page`` are optional sync progress hooks called from the
    extraction loop — see ``extract_reading_order_stream``.
    """
    pymupdf = load_pymupdf()
    pages: list[ReadingOrderPage] = []
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        page_count = doc.page_count
        if on_open is not None:
            on_open(page_count)
        for page_index, page in enumerate(doc):
            rect = page.rect
            raw_blocks: list[_RawBlock] = []
            for block in page.get_text("blocks", sort=False):
                x0, y0, x1, y1, text, _bno, block_type = block[:7]
                if block_type != 0:
                    continue
                text = str(text).strip()
                if not text:
                    continue
                raw_blocks.append(
                    _RawBlock(
                        x0=float(x0),
                        y0=float(y0),
                        x1=float(x1),
                        y1=float(y1),
                        text=text,
                    )
                )
            columns = _cluster_columns(raw_blocks, float(rect.width))
            blocks_in_order: list[ReadingOrderBlock] = []
            running_index = 0
            for column_index, column in enumerate(columns):
                for raw in column:
                    blocks_in_order.append(
                        ReadingOrderBlock(
                            block_index=running_index,
                            column_index=column_index,
                            x0=raw.x0,
                            y0=raw.y0,
                            x1=raw.x1,
                            y1=raw.y1,
                            text=raw.text,
                        )
                    )
                    running_index += 1
            order_page = ReadingOrderPage(
                page_number=page_index + 1,
                column_count=max(1, len(columns)),
                blocks_in_order=blocks_in_order,
            )
            pages.append(order_page)
            if on_page is not None:
                on_page(order_page)
    return ReadingOrderReport(page_count=page_count, pages=pages)


async def extract_reading_order_async(pdf_bytes: bytes) -> ReadingOrderReport:
    return await run_in_cpu_executor(extract_reading_order, pdf_bytes)


async def extract_reading_order_stream(
    pdf_bytes: bytes,
) -> AsyncIterator[PdfExtractStart | ReadingOrderPage | ReadingOrderReport]:
    """Stream reading-order extraction live: one ``PdfExtractStart`` (page
    count) on open, each ``ReadingOrderPage`` as its page resolves, then the
    complete ``ReadingOrderReport``."""

    def _work(emit: Callable[[object], None]) -> None:
        report = extract_reading_order(
            pdf_bytes,
            on_open=lambda total: emit(PdfExtractStart(total_pages=total)),
            on_page=emit,
        )
        emit(report)

    async for item in iter_sync_stream(run_in_cpu_executor, _work):
        yield item  # type: ignore[misc]


__all__ = [
    "extract_reading_order",
    "extract_reading_order_async",
    "extract_reading_order_stream",
]

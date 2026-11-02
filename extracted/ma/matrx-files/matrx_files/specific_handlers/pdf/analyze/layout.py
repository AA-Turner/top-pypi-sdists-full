"""Per-page layout classifier — assigns each page a ``PageClass`` label.

Rule-based first cut (design §5.8). The ``LayoutProvider`` Protocol from §4.3
will let hosts swap in an ML-driven classifier later without changing the
output shape. Phase 3 ships heuristics that work for the legal/medical
document classes the user described:

- ``cover``: page 1 + low text density + has at least one large-font line
- ``toc``: many lines with the dot-leader "title ........ N" pattern
- ``billing``: dense table-like layout with $ amounts in regular intervals
- ``exhibit``: header text matching ``Exhibit\\s+\\w+``
- ``signature``: contains signature lines / "/s/" / "By:" + a name
- ``appendix``: header text matching ``Appendix\\s+\\w+``
- ``blank``: char count < 30
- ``image-only``: char count < 80 AND embeds at least one large image
- ``footer-only``: text only in bottom band + char count < 200
- ``body``: default
"""

from __future__ import annotations

import re
from collections.abc import AsyncIterator, Callable, Iterator
from dataclasses import dataclass
from typing import Any

from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf
from ..models import PdfExtractStart
from ..stream_bridge import iter_sync_stream
from .models import LayoutClassificationReport, PageClass, PageClassification


_CLASSIFIER_VERSION = "v1"


_EXHIBIT_RE = re.compile(r"\bexhibit\s+[A-Za-z0-9]+\b", re.I)
_APPENDIX_RE = re.compile(r"\bappendix\s+[A-Za-z0-9]+\b", re.I)
_SIGNATURE_HINTS = (
    re.compile(r"/s/\s*\S", re.I),
    re.compile(r"\bsignature[:\s]", re.I),
    re.compile(r"\bsigned by\b", re.I),
    re.compile(r"\bby:\s+_+", re.I),
    re.compile(r"\b__________+\b"),
)
_TOC_LINE = re.compile(r"\.{4,}\s*\d+\s*$")
_BILLING_AMOUNT = re.compile(r"\$\s?\d[\d,]*(?:\.\d{2})?")


@dataclass
class _PageStats:
    page_number: int
    char_count: int
    line_count: int
    text_lines: list[str]
    blocks_in_bottom: int
    blocks_total: int
    image_count: int
    has_large_text: bool
    max_font_size: float
    body_text: str


def _iter_page_stats(doc: Any) -> Iterator[_PageStats]:
    for page_index, page in enumerate(doc):
        rect = page.rect
        page_h = float(rect.height)
        text = page.get_text("text", sort=False) or ""
        text_lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
        # Use dict mode to get font-size info.
        max_font = 0.0
        for block in page.get_text("dict", sort=False).get("blocks", []):
            for line in block.get("lines", []) or []:
                for span in line.get("spans", []) or []:
                    size = float(span.get("size", 0.0) or 0.0)
                    if size > max_font:
                        max_font = size
        # Block geometry for header/footer-only detection.
        blocks_total = 0
        blocks_in_bottom = 0
        for block in page.get_text("blocks", sort=False):
            _x0, y0, _x1, y1, _t, _bno, block_type = block[:7]
            if block_type != 0:
                continue
            blocks_total += 1
            mid_y = ((y0 + y1) / 2.0) / page_h if page_h else 0
            if mid_y > 0.8:
                blocks_in_bottom += 1
        image_count = len(page.get_images(full=False))
        yield _PageStats(
            page_number=page_index + 1,
            char_count=len(text),
            line_count=len(text_lines),
            text_lines=text_lines,
            blocks_in_bottom=blocks_in_bottom,
            blocks_total=blocks_total,
            image_count=image_count,
            has_large_text=max_font >= 18.0,
            max_font_size=max_font,
            body_text=text,
        )


def _classify_page(stat: _PageStats, page_count: int) -> PageClassification:
    """Classifier priority (highest-precision matches first):

    1. Explicit pattern matches — exhibit / appendix / signature
    2. TOC (dot-leader heuristic, strong signal)
    3. Billing ($ amounts)
    4. Cover page (page 1 + large text + few lines)
    5. Truly blank / image-only (< 30 chars total)
    6. Footer-only (sparse text concentrated at the bottom)
    7. Body (default)
    """
    indicators: list[str] = []

    # 1. Exhibit / Appendix — highest precision text matches.
    if _EXHIBIT_RE.search(stat.body_text):
        indicators.append("exhibit_header_match")
        return _result(stat, "exhibit", 0.8, indicators)
    if _APPENDIX_RE.search(stat.body_text):
        indicators.append("appendix_header_match")
        return _result(stat, "appendix", 0.8, indicators)

    # 1b. Signature pages: clear pattern hits.
    sig_hits = sum(1 for pat in _SIGNATURE_HINTS if pat.search(stat.body_text))
    if sig_hits >= 2 or (
        sig_hits >= 1 and stat.line_count <= 40 and stat.page_number > 1
    ):
        indicators.append(f"signature_hints({sig_hits})")
        return _result(stat, "signature", 0.7, indicators)

    # 2. TOC: dot-leader pattern across many lines.
    toc_hits = sum(1 for ln in stat.text_lines if _TOC_LINE.search(ln))
    if toc_hits >= 5 and toc_hits / max(stat.line_count, 1) >= 0.3:
        indicators.append(f"toc_dot_leader_lines({toc_hits})")
        return _result(stat, "toc", 0.85, indicators)

    # 3. Billing: many $ amounts in a structured layout.
    billing_hits = len(_BILLING_AMOUNT.findall(stat.body_text))
    if billing_hits >= 6:
        indicators.append(f"billing_amounts({billing_hits})")
        return _result(stat, "billing", min(0.9, 0.5 + billing_hits / 20.0), indicators)

    # 4. Cover page — runs BEFORE the blank check so a sparse cover page
    # with a large title isn't misclassified as blank.
    if stat.page_number == 1 and stat.line_count <= 15 and stat.has_large_text:
        indicators.append(
            f"first_page,large_font({stat.max_font_size:.0f}),lines({stat.line_count})"
        )
        return _result(stat, "cover", 0.75, indicators)

    # 5. Truly blank / image-only.
    if stat.char_count < 30:
        if stat.image_count >= 1 and stat.char_count >= 1:
            indicators.append(
                f"sparse_text({stat.char_count}) + image({stat.image_count})"
            )
            return _result(stat, "image-only", 0.7, indicators)
        indicators.append(f"sparse_text({stat.char_count})")
        return _result(stat, "blank", 0.9, indicators)

    # 6. Footer-only: very little text, mostly at the bottom of the page.
    if (
        stat.char_count < 200
        and stat.blocks_total > 0
        and stat.blocks_in_bottom / stat.blocks_total >= 0.6
    ):
        indicators.append(
            f"bottom_dominant({stat.blocks_in_bottom}/{stat.blocks_total})"
        )
        return _result(stat, "footer-only", 0.65, indicators)

    indicators.append(f"chars({stat.char_count}),lines({stat.line_count})")
    return _result(stat, "body", 0.6, indicators)


def _result(
    stat: _PageStats,
    page_class: PageClass,
    confidence: float,
    indicators: list[str],
) -> PageClassification:
    return PageClassification(
        page_number=stat.page_number,
        page_class=page_class,
        confidence=round(confidence, 4),
        indicators=indicators,
    )


def classify_pages(
    pdf_bytes: bytes,
    on_open: Callable[[int], None] | None = None,
    on_page: Callable[[PageClassification], None] | None = None,
) -> LayoutClassificationReport:
    """Run the rule-based page classifier over every page of a PDF.

    ``on_open`` / ``on_page`` are optional sync progress hooks called from the
    classification loop (``on_open`` with the page count the moment the
    document opens, ``on_page`` with each page's classification as it
    resolves) — see ``classify_pages_stream``.
    """
    pymupdf = load_pymupdf()
    pages: list[PageClassification] = []
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        page_count = doc.page_count
        if on_open is not None:
            on_open(page_count)
        for stat in _iter_page_stats(doc):
            classification = _classify_page(stat, page_count)
            pages.append(classification)
            if on_page is not None:
                on_page(classification)
    return LayoutClassificationReport(
        page_count=page_count,
        pages=pages,
        classifier_version=_CLASSIFIER_VERSION,
    )


async def classify_pages_async(pdf_bytes: bytes) -> LayoutClassificationReport:
    return await run_in_cpu_executor(classify_pages, pdf_bytes)


async def classify_pages_stream(
    pdf_bytes: bytes,
) -> AsyncIterator[PdfExtractStart | PageClassification | LayoutClassificationReport]:
    """Stream classification live: one ``PdfExtractStart`` (page count) on
    open, each ``PageClassification`` as its page resolves, then the complete
    ``LayoutClassificationReport``."""

    def _work(emit: Callable[[object], None]) -> None:
        report = classify_pages(
            pdf_bytes,
            on_open=lambda total: emit(PdfExtractStart(total_pages=total)),
            on_page=emit,
        )
        emit(report)

    async for item in iter_sync_stream(run_in_cpu_executor, _work):
        yield item  # type: ignore[misc]


__all__ = ["classify_pages", "classify_pages_async", "classify_pages_stream"]

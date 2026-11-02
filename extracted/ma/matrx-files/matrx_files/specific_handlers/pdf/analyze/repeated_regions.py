"""Detect headers / footers / watermarks / repeated margins across a PDF.

Algorithm (design §5.8):

1. For every page, extract block-level geometry via PyMuPDF's
   ``page.get_text("blocks")``.
2. Bucket each block by its vertical position on the page (top 10% /
   top 20% / bottom 10% / bottom 20% / middle / side-margin).
3. Normalize each block's text — strip page-number tokens, ISO/locale dates,
   case, whitespace — so "Page 1 of 12" and "Page 7 of 12" hash to the same
   template "Page {page} of {page}".
4. Group blocks by ``(normalized_template, y_band, x_band)``. Any group
   covering >= ⌈page_count / 3⌉ pages becomes a ``RepeatedRegion`` candidate.
5. Score each candidate with confidence in ``[0, 1]`` from
   ``0.4 * freq + 0.3 * geom_stability + 0.3 * text_similarity``.

The output is a deterministic ``RepeatedRegionsReport`` — the same input
always produces the same regions and ids, so a FE accept/reject UI can store
per-region decisions and re-apply them across rerenders.

This module imports nothing from sibling matrx-* packages. PyMuPDF is the
only PDF library it touches, via the lazy ``load_pymupdf`` helper.
"""

from __future__ import annotations

import hashlib
import itertools
import math
import re
import statistics
from collections import defaultdict
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass

from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf
from ..models import PdfExtractStart, PdfPageScanned
from ..stream_bridge import iter_sync_stream
from .models import RegionKind, RepeatedRegion, RepeatedRegionBbox, RepeatedRegionsReport


_DETECTOR_VERSION = "v1"


# Regex set for text normalization. Order matters — page-number patterns
# match before generic numbers so "Page 3 of 12" tokenises both numbers as
# {page} rather than as {num}.
_NORMALISERS: tuple[tuple[re.Pattern[str], str], ...] = (
    # "Page 3 of 12", "Pg. 3/12", "p. 3"
    (re.compile(r"\b(?:page|pg\.?|p\.?)\s*\d+\s*(?:of|/)\s*\d+\b", re.I), "{page}"),
    (re.compile(r"\b(?:page|pg\.?|p\.?)\s*\d+\b", re.I), "{page}"),
    # ISO dates 2026-01-31, US dates 01/31/2026, locale dates 31.01.2026
    (re.compile(r"\b\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2}\b"), "{date}"),
    (re.compile(r"\b\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}\b"), "{date}"),
    # Long-form dates: January 31, 2026 / Jan. 31, 2026 / 31 January 2026
    (
        re.compile(
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{2,4}\b",
            re.I,
        ),
        "{date}",
    ),
    (
        re.compile(
            r"\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{2,4}\b",
            re.I,
        ),
        "{date}",
    ),
    # Standalone numerics — collapses "Section 1" + "Section 2" to the same
    # template so alternating odd/even headers group correctly. Single-digit
    # tokens are common in section / chapter / step / page-number variants.
    (re.compile(r"\b\d+\b"), "{num}"),
    (re.compile(r"\bConfidential\b", re.I), "Confidential"),
)

_WS = re.compile(r"\s+")


def normalize_block_text(text: str) -> str:
    """Strip varying numerics + case so cross-page comparison detects patterns."""
    out = text.strip()
    for pattern, token in _NORMALISERS:
        out = pattern.sub(token, out)
    out = _WS.sub(" ", out)
    return out.lower()


@dataclass(frozen=True)
class _BlockRecord:
    page_number: int
    x0: float
    y0: float
    x1: float
    y1: float
    text: str
    normalized: str
    y_band: str
    x_band: str


# Y / X band thresholds (fraction of page height/width).
#
# Calibrated against a US Letter (612x792) page assuming 72-pt margins:
# - Top-strict captures the 60-pt header strip
# - Top-wide captures the 60-110 pt zone (sub-header / margin notes)
# - Bottom-strict captures the bottom 60-pt footer strip
# - Bottom-wide captures the 670-740 pt zone (page number + matter id)
# Anything in 0.13-0.87 is body content. Watermarks live in the body band
# and are only promoted when frequency clears a separate threshold.
_TOP_BAND = 0.08
_TOP_WIDE_BAND = 0.13
_BOTTOM_BAND = 0.92
_BOTTOM_WIDE_BAND = 0.87
_LEFT_BAND = 0.10
_RIGHT_BAND = 0.90

# Middle-band (watermark / side margin) regions need a higher coverage
# threshold before they're promoted — body text repeating across pages of
# a templated document (form lines, table headers) hits the same y-band
# but should not be stripped as "noise".
_MIDDLE_BAND_MIN_FREQUENCY = 0.7

# Hard cap on the raw text length of a recognized header/footer. Real
# headers/footers are short. Anything longer at the same y-coord is more
# likely body content that happens to repeat.
_HEADER_FOOTER_MAX_LEN = 200

# Middle-band watermarks are visually distinctive — single-word stamps
# ("DRAFT", "CONFIDENTIAL") or short banners. Anything longer in the body
# band is almost certainly templated body content, not a watermark.
_WATERMARK_MAX_TEMPLATE_LEN = 60


def _y_band(y0: float, y1: float, page_h: float) -> str:
    if page_h <= 0:
        return "middle"
    mid_y = (y0 + y1) / 2.0 / page_h
    if mid_y < _TOP_BAND:
        return "top-strict"
    if mid_y < _TOP_WIDE_BAND:
        return "top-wide"
    if mid_y > _BOTTOM_BAND:
        return "bottom-strict"
    if mid_y > _BOTTOM_WIDE_BAND:
        return "bottom-wide"
    return "middle"


def _x_band(x0: float, x1: float, page_w: float) -> str:
    if page_w <= 0:
        return "center"
    mid_x = (x0 + x1) / 2.0 / page_w
    if mid_x < _LEFT_BAND:
        return "left"
    if mid_x > _RIGHT_BAND:
        return "right"
    return "center"


def _classify_region_kind(y_band: str, x_band: str) -> RegionKind:
    if y_band.startswith("top"):
        if x_band == "left":
            return "logo"
        if x_band == "right":
            return "page-number"
        return "header"
    if y_band.startswith("bottom"):
        if x_band == "right":
            return "page-number"
        return "footer"
    if y_band == "middle":
        if x_band == "left" or x_band == "right":
            return "side-margin"
        return "watermark"
    return "unknown"


def _gather_blocks(
    pdf_bytes: bytes,
    on_open: Callable[[int], None] | None = None,
    on_page: Callable[[int], None] | None = None,
) -> tuple[list[_BlockRecord], int]:
    """Pull (page, bbox, text, normalised-text, y-band, x-band) for every block."""
    pymupdf = load_pymupdf()
    records: list[_BlockRecord] = []
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        page_count = doc.page_count
        if on_open is not None:
            on_open(page_count)
        for page_index, page in enumerate(doc):
            rect = page.rect
            page_w = float(rect.width)
            page_h = float(rect.height)
            for block in page.get_text("blocks", sort=False):
                x0, y0, x1, y1, text, _block_no, block_type = block[:7]
                if block_type != 0:  # text blocks only — skip images
                    continue
                text = str(text).strip()
                if not text:
                    continue
                normalized = normalize_block_text(text)
                if not normalized:
                    continue
                records.append(
                    _BlockRecord(
                        page_number=page_index + 1,
                        x0=float(x0),
                        y0=float(y0),
                        x1=float(x1),
                        y1=float(y1),
                        text=text,
                        normalized=normalized,
                        y_band=_y_band(y0, y1, page_h),
                        x_band=_x_band(x0, x1, page_w),
                    )
                )
            if on_page is not None:
                on_page(page_index + 1)
    return records, page_count


def _stdev_or_zero(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    try:
        return statistics.pstdev(values)
    except statistics.StatisticsError:
        return 0.0


def _confidence(
    frequency: float, y_stability: float, text_similarity: float
) -> float:
    """Blend the three scoring components per design §5.8 step 5.

    *frequency* is in [0, 1] (fraction of pages that carry the region).
    *y_stability* is in [0, 1], 1.0 means bbox y0 never moved.
    *text_similarity* is in [0, 1], 1.0 means raw text identical across pages.
    """
    return 0.4 * frequency + 0.3 * y_stability + 0.3 * text_similarity


def _text_similarity(raw_texts: list[str]) -> float:
    """Pairwise-mean Jaccard similarity on word sets — robust to ordering noise
    and unbiased by page ordering.
    """
    if len(raw_texts) < 2:
        return 1.0
    word_sets = [set(t.lower().split()) for t in raw_texts]
    sims: list[float] = []
    for a, b in itertools.combinations(word_sets, 2):
        union = a | b
        inter = a & b
        if not union:
            # Both empty — treat as identical-noise rather than unrelated.
            sims.append(1.0)
            continue
        sims.append(len(inter) / len(union))
    return statistics.mean(sims) if sims else 1.0


def _region_id(y_band: str, x_band: str, template: str) -> str:
    """Deterministic region id keyed on geometry + template only.

    The ``kind`` label is intentionally NOT part of the id so a future change
    to ``_classify_region_kind`` (e.g. demoting "logo" → "header") does not
    break persisted accept/reject decisions. Consumers that persist user
    decisions should compose a key from ``(region_id, detector_version)``.
    """
    payload = f"{y_band}|{x_band}|{template}".encode()
    return hashlib.blake2s(payload, digest_size=8).hexdigest()


def detect_repeated_regions(
    pdf_bytes: bytes,
    *,
    min_pages_ratio: float = 1 / 3,
    min_confidence: float = 0.5,
    on_open: Callable[[int], None] | None = None,
    on_page: Callable[[int], None] | None = None,
) -> RepeatedRegionsReport:
    """Detect cross-page repeated regions.

    Parameters
    ----------
    pdf_bytes:
        Raw PDF bytes.
    min_pages_ratio:
        Minimum fraction of pages a group must span before it's promoted to
        a candidate. Default ``1/3`` per design §5.8.
    min_confidence:
        Drop candidates whose blended confidence falls below this threshold.
    on_open / on_page:
        Optional sync progress hooks called from the block-gathering loop
        (``on_open`` with the page count on document open, ``on_page`` with
        each 1-based page number as its blocks land) — see
        ``detect_repeated_regions_stream``. Grouping/scoring after the scan
        is fast and reports no per-page progress.

    Returns
    -------
    RepeatedRegionsReport
        Deterministic — same input produces the same report.
    """
    records, page_count = _gather_blocks(pdf_bytes, on_open=on_open, on_page=on_page)
    if page_count == 0 or not records:
        return RepeatedRegionsReport(page_count=page_count, regions=[])

    # Single ceiling-based threshold — no float-equality branch on the
    # default ratio (avoided silent semantic shift when callers pass slightly
    # different floats).
    min_pages = max(2, math.ceil(page_count * min_pages_ratio))
    # Single-page documents can't have repeated regions.
    if page_count < min_pages:
        return RepeatedRegionsReport(page_count=page_count, regions=[])

    # Group by (normalised_template, y_band, x_band). The y_band collapses
    # geometry into broad zones so a header that drifts ±2 px page-to-page
    # still groups together. The normalized template means "Page 3 of 12"
    # and "Page 7 of 12" collide.
    groups: dict[tuple[str, str, str], list[_BlockRecord]] = defaultdict(list)
    for record in records:
        key = (record.normalized, record.y_band, record.x_band)
        groups[key].append(record)

    regions: list[RepeatedRegion] = []
    for (template, y_band, x_band), group in groups.items():
        # Dedupe by page — a block that appears twice on the same page still
        # counts as one page of coverage for the group.
        pages_seen: dict[int, _BlockRecord] = {}
        for record in group:
            pages_seen.setdefault(record.page_number, record)
        if len(pages_seen) < min_pages:
            continue

        sorted_pages = sorted(pages_seen)
        bboxes = [pages_seen[p] for p in sorted_pages]
        frequency = len(pages_seen) / page_count

        # Middle-band regions (watermarks, recurring side notes, center
        # stamps) need stronger coverage before we treat them as noise to
        # strip — body text on heavily templated documents hits the same
        # band but should not be removed.
        if y_band == "middle":
            if frequency < _MIDDLE_BAND_MIN_FREQUENCY:
                continue
            # Long templates at the body y-band are not watermarks — they
            # are templated body content (recurring contract clauses,
            # billing line items). Skip them.
            if len(template) > _WATERMARK_MAX_TEMPLATE_LEN:
                continue

        # Long blocks at the header/footer y-band are usually body text that
        # happens to start at the same y on every page — skip them so we
        # don't strip real content.
        max_raw_len = max(len(b.text) for b in bboxes)
        if max_raw_len > _HEADER_FOOTER_MAX_LEN:
            continue

        y_centers = [(b.y0 + b.y1) / 2.0 for b in bboxes]
        y_stdev = _stdev_or_zero(y_centers)
        # Normalize stdev against a generous tolerance (12 pt) — within 12 pt
        # of the median is treated as fully stable.
        y_stability = max(0.0, min(1.0, 1.0 - y_stdev / 12.0))
        text_similarity = _text_similarity([b.text for b in bboxes])
        confidence = _confidence(frequency, y_stability, text_similarity)
        if confidence < min_confidence:
            continue

        kind = _classify_region_kind(y_band, x_band)
        # Promote a doc-wide repeating mark in the middle to "watermark"
        if y_band == "middle" and frequency >= _MIDDLE_BAND_MIN_FREQUENCY:
            kind = "watermark"

        region_id = _region_id(y_band, x_band, template)
        regions.append(
            RepeatedRegion(
                region_id=region_id,
                kind=kind,
                text_template=template,
                pages=sorted_pages,
                bbox_per_page=[
                    RepeatedRegionBbox(
                        page_number=b.page_number,
                        x0=b.x0,
                        y0=b.y0,
                        x1=b.x1,
                        y1=b.y1,
                        raw_text=b.text,
                    )
                    for b in bboxes
                ],
                confidence=round(confidence, 4),
            )
        )

    # Stable ordering: highest confidence first, then by kind, then by id.
    regions.sort(key=lambda r: (-r.confidence, r.kind, r.region_id))
    return RepeatedRegionsReport(
        page_count=page_count,
        regions=regions,
        detector_version=_DETECTOR_VERSION,
    )


async def detect_repeated_regions_async(
    pdf_bytes: bytes,
    *,
    min_pages_ratio: float = 1 / 3,
    min_confidence: float = 0.5,
) -> RepeatedRegionsReport:
    return await run_in_cpu_executor(
        lambda: detect_repeated_regions(
            pdf_bytes,
            min_pages_ratio=min_pages_ratio,
            min_confidence=min_confidence,
        )
    )


async def detect_repeated_regions_stream(
    pdf_bytes: bytes,
    *,
    min_pages_ratio: float = 1 / 3,
    min_confidence: float = 0.5,
) -> AsyncIterator[PdfExtractStart | PdfPageScanned | RepeatedRegionsReport]:
    """Stream detection live: one ``PdfExtractStart`` (page count) on open,
    a ``PdfPageScanned`` per page as its blocks are gathered, then the
    complete ``RepeatedRegionsReport``."""

    def _work(emit: Callable[[object], None]) -> None:
        report = detect_repeated_regions(
            pdf_bytes,
            min_pages_ratio=min_pages_ratio,
            min_confidence=min_confidence,
            on_open=lambda total: emit(PdfExtractStart(total_pages=total)),
            on_page=lambda page_no: emit(PdfPageScanned(page_number=page_no)),
        )
        emit(report)

    async for item in iter_sync_stream(run_in_cpu_executor, _work):
        yield item  # type: ignore[misc]


def strip_repeated_regions_text(
    pages_text: list[str],
    regions: list[RepeatedRegion],
    accepted_region_ids: set[str] | None = None,
) -> list[str]:
    """Remove the raw text of accepted regions from per-page text strings.

    Stripping is biased toward the edges of the page (the y-bands where
    real headers / footers live) so a body-paragraph that happens to contain
    the same literal substring as a detected region is not accidentally
    removed. For each accepted region/bbox:

    - If the region is a top-band kind (header / page-number / logo /
      running-title), strip the FIRST occurrence in the page text.
    - If the region is a bottom-band kind (footer), strip the LAST
      occurrence.
    - Other kinds (watermark, side-margin) fall through to a global
      "remove every standalone-line occurrence" so they don't get matched
      inside body paragraphs.
    """
    accepted = accepted_region_ids
    if accepted is None:
        accepted = {r.region_id for r in regions}
    if not accepted:
        return list(pages_text)

    by_page: dict[int, list[tuple[RegionKind, str]]] = defaultdict(list)
    for region in regions:
        if region.region_id not in accepted:
            continue
        for bbox in region.bbox_per_page:
            by_page[bbox.page_number].append((region.kind, bbox.raw_text))

    cleaned: list[str] = []
    for index, raw in enumerate(pages_text, start=1):
        out = raw
        for kind, snippet in by_page.get(index, []):
            if not snippet:
                continue
            if kind in _TOP_KINDS:
                pos = out.find(snippet)
                if pos != -1:
                    out = out[:pos] + out[pos + len(snippet) :]
            elif kind in _BOTTOM_KINDS:
                pos = out.rfind(snippet)
                if pos != -1:
                    out = out[:pos] + out[pos + len(snippet) :]
            else:
                # Standalone-line occurrence only — anchored to line edges so
                # the snippet "Confidential" in body prose is not stripped.
                pattern = re.compile(
                    rf"(?:^|\n)\s*{re.escape(snippet)}\s*(?=\n|$)"
                )
                out = pattern.sub("", out)
        # Collapse any blank-line gaps left behind.
        out = re.sub(r"\n{3,}", "\n\n", out)
        cleaned.append(out.strip("\n"))
    return cleaned


_TOP_KINDS: frozenset[RegionKind] = frozenset(
    {"header", "page-number", "logo", "running-title"}
)
_BOTTOM_KINDS: frozenset[RegionKind] = frozenset({"footer"})


__all__ = [
    "detect_repeated_regions",
    "detect_repeated_regions_async",
    "detect_repeated_regions_stream",
    "strip_repeated_regions_text",
    "normalize_block_text",
]

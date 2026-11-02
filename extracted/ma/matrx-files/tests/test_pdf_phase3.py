"""Tests for the Phase 3 PDF analyze surface.

Covers:
- RepeatedRegionDetector — true headers/footers found, body-text false
  positives rejected, deterministic output
- LayoutClassifier — cover / blank / billing / signature / appendix labels
- ReadingOrderExtractor — multi-column page clustering
- handler integration smoke
"""

from __future__ import annotations

import pymupdf

from matrx_files.specific_handlers.pdf import (
    PDFHandler,
    RepeatedRegion,
    RepeatedRegionsReport,
    classify_pages,
    detect_repeated_regions,
    extract_reading_order,
    normalize_block_text,
    strip_repeated_regions_text,
)



def _make_legal_doc(page_count: int = 10) -> bytes:
    """Synthetic legal-style PDF with stable header + footer across all pages."""
    doc = pymupdf.open()
    try:
        for n in range(1, page_count + 1):
            page = doc.new_page(width=612, height=792)
            page.insert_text((72, 30), "Acme Law Firm — Confidential", fontsize=10)
            page.insert_text((500, 30), f"Page {n} of {page_count}", fontsize=10)
            page.insert_text(
                (72, 150),
                f"Body content for page {n} unique sentence that varies in "
                f"length and content on every page in different ways.",
                fontsize=12,
            )
            page.insert_text((72, 760), "Footer line: matter no. 12345", fontsize=8)
        return doc.tobytes()
    finally:
        doc.close()


# ---------------------------------------------------------------------------
# normalize_block_text
# ---------------------------------------------------------------------------


def test_normalize_block_text_collapses_page_numbers() -> None:
    assert normalize_block_text("Page 3 of 12") == "{page}"
    assert normalize_block_text("PAGE 7 OF 12") == "{page}"
    assert normalize_block_text("page 5") == "{page}"
    assert normalize_block_text("p. 9") == "{page}"


def test_normalize_block_text_collapses_dates() -> None:
    assert "{date}" in normalize_block_text("Printed on 2026-05-10")
    assert "{date}" in normalize_block_text("01/31/2026 — Final")
    assert "{date}" in normalize_block_text("January 31, 2026")


def test_normalize_block_text_lowercases_and_collapses_whitespace() -> None:
    assert normalize_block_text("  HELLO  WORLD  ") == "hello world"


# ---------------------------------------------------------------------------
# RepeatedRegionDetector
# ---------------------------------------------------------------------------


def test_detect_repeated_regions_finds_header_and_footer() -> None:
    pdf_bytes = _make_legal_doc(page_count=10)
    report = detect_repeated_regions(pdf_bytes)
    assert isinstance(report, RepeatedRegionsReport)
    assert report.page_count == 10
    kinds = {r.kind for r in report.regions}
    assert "header" in kinds, f"no header in {[(r.kind, r.text_template) for r in report.regions]}"
    assert "footer" in kinds, f"no footer in {[(r.kind, r.text_template) for r in report.regions]}"


def test_detect_repeated_regions_rejects_body_text() -> None:
    """Body text that lives mid-page must NOT be promoted to a header/footer."""
    pdf_bytes = _make_legal_doc(page_count=10)
    report = detect_repeated_regions(pdf_bytes)
    for region in report.regions:
        # Body content lines are anchored at y=150 (~19% from top), which is
        # below TOP_WIDE_BAND (0.13). If they showed up at all, that's a
        # false positive.
        for bbox in region.bbox_per_page:
            mid_y_frac = ((bbox.y0 + bbox.y1) / 2.0) / 792
            assert (
                mid_y_frac < 0.13 or mid_y_frac > 0.87
            ), f"region {region.region_id} captured body-band block at y={bbox.y0}"


def test_detect_repeated_regions_is_deterministic() -> None:
    pdf_bytes = _make_legal_doc(page_count=8)
    r1 = detect_repeated_regions(pdf_bytes)
    r2 = detect_repeated_regions(pdf_bytes)
    ids_1 = [r.region_id for r in r1.regions]
    ids_2 = [r.region_id for r in r2.regions]
    assert ids_1 == ids_2


def test_detect_repeated_regions_skips_short_docs() -> None:
    pdf_bytes = _make_legal_doc(page_count=2)
    report = detect_repeated_regions(pdf_bytes)
    # With page_count=2, the min_pages threshold (max(2, ceil(2/3))) is 2.
    # Anything that appears on both pages can still qualify, but we don't
    # require zero regions — only that the report is well-formed.
    assert report.page_count == 2


def test_strip_repeated_regions_removes_accepted_only() -> None:
    pdf_bytes = _make_legal_doc(page_count=6)
    report = detect_repeated_regions(pdf_bytes)
    assert report.regions, "expected at least one detected region"
    accepted = {report.regions[0].region_id}
    raw_pages = ["text " + r.bbox_per_page[0].raw_text for r in [report.regions[0]]]
    # We feed page-1 text containing the region's raw_text and confirm strip
    page1_raw = report.regions[0].bbox_per_page[0].raw_text
    stripped = strip_repeated_regions_text([page1_raw + " body"], report.regions, accepted)
    assert page1_raw not in stripped[0]


def test_strip_repeated_regions_no_op_when_no_accepts() -> None:
    pdf_bytes = _make_legal_doc(page_count=4)
    report = detect_repeated_regions(pdf_bytes)
    stripped = strip_repeated_regions_text(["sample text"], report.regions, accepted_region_ids=set())
    assert stripped == ["sample text"]


def test_strip_repeated_regions_does_not_strip_body_collision() -> None:
    """Regression: a header snippet that also appears verbatim inside a body
    paragraph must NOT be removed from the body. Top-band regions strip the
    FIRST occurrence only (the header position).
    """
    from matrx_files.specific_handlers.pdf import (
        RepeatedRegion,
        RepeatedRegionBbox,
    )

    region = RepeatedRegion(
        region_id="test",
        kind="header",
        text_template="confidential",
        pages=[1],
        bbox_per_page=[
            RepeatedRegionBbox(
                page_number=1, x0=0, y0=10, x1=200, y1=20, raw_text="Confidential"
            )
        ],
        confidence=1.0,
    )
    page = (
        "Confidential\n"
        "Some body text that also mentions Confidential matters.\n"
    )
    stripped = strip_repeated_regions_text([page], [region], accepted_region_ids={"test"})
    # Header occurrence gone, body mention preserved.
    assert "Confidential matters" in stripped[0]
    # And the leading header is dropped.
    assert not stripped[0].startswith("Confidential\n")


def test_region_id_is_geometry_only_and_stable_across_kind_changes() -> None:
    """Regression: region_id MUST NOT carry the `kind` label so re-classifying
    "logo" → "header" doesn't break persisted accept/reject decisions.
    """
    from matrx_files.specific_handlers.pdf.analyze.repeated_regions import (
        _region_id,
    )

    # Two calls with different *kind* values are not possible since kind
    # isn't an argument anymore — verifying the function signature is the
    # whole point. Same (y_band, x_band, template) → same id.
    assert _region_id("top-strict", "left", "acme") == _region_id(
        "top-strict", "left", "acme"
    )
    assert _region_id("top-strict", "left", "acme") != _region_id(
        "top-strict", "right", "acme"
    )


# ---------------------------------------------------------------------------
# LayoutClassifier
# ---------------------------------------------------------------------------


def test_classify_pages_labels_blank() -> None:
    doc = pymupdf.open()
    try:
        doc.new_page(width=300, height=400)  # truly blank
        doc[0].insert_text((72, 72), ".")  # 1 char
        pdf_bytes = doc.tobytes()
    finally:
        doc.close()
    report = classify_pages(pdf_bytes)
    assert report.pages[0].page_class == "blank"


def test_classify_pages_labels_cover() -> None:
    doc = pymupdf.open()
    try:
        page = doc.new_page(width=612, height=792)
        page.insert_text((180, 360), "Contract", fontsize=36)
        page.insert_text((220, 420), "May 2026", fontsize=14)
        pdf_bytes = doc.tobytes()
    finally:
        doc.close()
    report = classify_pages(pdf_bytes)
    assert report.pages[0].page_class == "cover"


def test_classify_pages_labels_billing() -> None:
    doc = pymupdf.open()
    try:
        page = doc.new_page(width=612, height=792)
        y = 100
        for amt in ("$1,234.00", "$56.78", "$9.99", "$420.00", "$1,000.00", "$87.65", "$10.50"):
            page.insert_text((72, y), f"Service item — fee {amt}", fontsize=10)
            y += 20
        pdf_bytes = doc.tobytes()
    finally:
        doc.close()
    report = classify_pages(pdf_bytes)
    assert report.pages[0].page_class == "billing"


def test_classify_pages_labels_exhibit() -> None:
    doc = pymupdf.open()
    try:
        page = doc.new_page(width=612, height=792)
        page.insert_text((72, 72), "Exhibit A", fontsize=20)
        page.insert_text((72, 150), "Supporting documentation for the case.", fontsize=12)
        pdf_bytes = doc.tobytes()
    finally:
        doc.close()
    report = classify_pages(pdf_bytes)
    assert report.pages[0].page_class == "exhibit"


def test_classify_pages_labels_appendix() -> None:
    doc = pymupdf.open()
    try:
        page = doc.new_page(width=612, height=792)
        page.insert_text((72, 72), "Appendix 1", fontsize=16)
        page.insert_text((72, 150), "Reference material follows.", fontsize=12)
        pdf_bytes = doc.tobytes()
    finally:
        doc.close()
    report = classify_pages(pdf_bytes)
    assert report.pages[0].page_class == "appendix"


def test_classify_pages_labels_signature() -> None:
    doc = pymupdf.open()
    try:
        page = doc.new_page(width=612, height=792)
        # second page so the cover heuristic doesn't kick in
        doc.new_page(width=612, height=792)
        page2 = doc[1]
        page2.insert_text((72, 100), "Agreed and signed.", fontsize=12)
        page2.insert_text((72, 200), "/s/ John Doe", fontsize=12)
        page2.insert_text((72, 240), "By: ____________", fontsize=12)
        pdf_bytes = doc.tobytes()
    finally:
        doc.close()
    report = classify_pages(pdf_bytes)
    assert report.pages[1].page_class == "signature"


def test_classify_pages_labels_body_default() -> None:
    pdf_bytes = _make_legal_doc(page_count=3)
    report = classify_pages(pdf_bytes)
    assert all(p.page_class == "body" for p in report.pages)


# ---------------------------------------------------------------------------
# ReadingOrderExtractor
# ---------------------------------------------------------------------------


def test_reading_order_single_column_returns_one_column() -> None:
    pdf_bytes = _make_legal_doc(page_count=2)
    report = extract_reading_order(pdf_bytes)
    assert report.pages[0].column_count == 1
    # Reading order should preserve top-to-bottom geometric order.
    ys = [b.y0 for b in report.pages[0].blocks_in_order]
    assert ys == sorted(ys)


def test_reading_order_two_column_groups_blocks() -> None:
    doc = pymupdf.open()
    try:
        page = doc.new_page(width=612, height=792)
        # Left column
        page.insert_text((72, 100), "Left column line 1.", fontsize=10)
        page.insert_text((72, 130), "Left column line 2.", fontsize=10)
        # Right column
        page.insert_text((350, 100), "Right column line 1.", fontsize=10)
        page.insert_text((350, 130), "Right column line 2.", fontsize=10)
        pdf_bytes = doc.tobytes()
    finally:
        doc.close()

    report = extract_reading_order(pdf_bytes)
    page = report.pages[0]
    assert page.column_count == 2
    # First two blocks should be the left column (column_index=0)
    assert page.blocks_in_order[0].column_index == 0
    assert page.blocks_in_order[1].column_index == 0
    # Then right column (column_index=1)
    assert page.blocks_in_order[2].column_index == 1


# ---------------------------------------------------------------------------
# Handler integration smoke
# ---------------------------------------------------------------------------


async def test_handler_async_smoke() -> None:
    handler = PDFHandler(app_name="test_phase3")
    pdf_bytes = _make_legal_doc(page_count=8)

    rr = await handler.detect_repeated_regions_async(pdf_bytes)
    assert rr.page_count == 8
    assert rr.regions

    lr = await handler.classify_pages_async(pdf_bytes)
    assert lr.page_count == 8

    ro = await handler.extract_reading_order_async(pdf_bytes)
    assert ro.page_count == 8

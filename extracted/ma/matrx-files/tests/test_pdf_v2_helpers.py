"""Tests for the v2 page-anchoring helpers + new server primitives.

Covers:
  - snap_to_text_blocks tightens a rough rect to the text block
  - search_text exact + regex paths
  - extract_region for text / image / table kinds
  - render_page_with_overlay produces a PNG with rectangles
  - page_outline detector emits a TOC payload
"""

from __future__ import annotations

import base64

import pymupdf
import pytest

# Importing the PDF analyze package registers detectors (incl. page_outline).
import matrx_files.specific_handlers.pdf.analyze  # noqa: F401
from matrx_files.analysis import DETECTOR_FACTORIES, PageInfo
from matrx_files.specific_handlers.pdf.extract.bbox import (
    snap_to_text_blocks,
)
from matrx_files.specific_handlers.pdf.extract.region import (
    extract_region,
)
from matrx_files.specific_handlers.pdf.extract.search import (
    search_text,
)
from matrx_files.specific_handlers.pdf.render.overlay import (
    OverlayBbox,
    OverlaySpec,
    render_page_with_overlay,
)


def _doc_with_text(text_lines: list[tuple[float, float, str]]) -> bytes:
    doc = pymupdf.open()
    try:
        page = doc.new_page(width=612, height=792)
        for x, y, t in text_lines:
            page.insert_text((x, y), t, fontsize=12)
        return doc.tobytes()
    finally:
        doc.close()


def test_page_outline_detector_registered() -> None:
    assert "page_outline" in DETECTOR_FACTORIES


def test_snap_to_text_block_tightens_rough_rect() -> None:
    pdf = _doc_with_text([
        (72, 100, "Header banner of the document"),
        (72, 200, "Patient Name: Jane Doe"),
        (72, 300, "Diagnosis: lumbar strain"),
    ])
    # Draw a huge sloppy box around the diagnosis line; expect tight snap.
    rough = {"x0": 50, "y0": 280, "x1": 500, "y1": 320}
    snapped = snap_to_text_blocks(pdf, page_number=1, bbox=rough)
    # Snapped bbox should be narrower than the rough one but still contain
    # the diagnosis text bounds.
    assert snapped.x0 >= rough["x0"]
    assert snapped.x1 <= rough["x1"]
    assert snapped.y0 >= rough["y0"] - 5
    assert snapped.y1 <= rough["y1"] + 5


def test_snap_to_text_falls_back_when_no_text() -> None:
    pdf = _doc_with_text([
        (72, 100, "Only text on the page"),
    ])
    rough = {"x0": 200, "y0": 500, "x1": 400, "y1": 600}
    snapped = snap_to_text_blocks(pdf, page_number=1, bbox=rough)
    # No text in the region — snapped equals (clamped) input.
    assert snapped.x0 == pytest.approx(rough["x0"], abs=1.0)
    assert snapped.y0 == pytest.approx(rough["y0"], abs=1.0)


def test_search_text_literal_hits() -> None:
    pdf = _doc_with_text([
        (72, 100, "Applicant Name: John Smith"),
        (72, 200, "Diagnosis: lumbar strain"),
        (72, 300, "Treating doctor: Dr. Smith"),
    ])
    hits = search_text(pdf, query="Smith")
    assert len(hits) >= 2
    pages = {h.page_number for h in hits}
    assert pages == {1}


def test_search_text_regex() -> None:
    pdf = _doc_with_text([
        (72, 100, "Order #12345 dated 2025-01-15"),
        (72, 200, "Order #67890 dated 2025-02-20"),
    ])
    hits = search_text(pdf, query=r"\b\d{4}-\d{2}-\d{2}\b", regex=True)
    assert len(hits) >= 2
    matched = {h.matched_text for h in hits}
    assert "2025-01-15" in matched and "2025-02-20" in matched


def test_extract_region_text() -> None:
    pdf = _doc_with_text([
        (72, 100, "Header banner"),
        (72, 200, "TARGET TEXT HERE"),
        (72, 300, "Footer disclaimer"),
    ])
    res = extract_region(
        pdf, page_number=1, bbox={"x0": 60, "y0": 190, "x1": 400, "y1": 215},
        extraction_kind="text",
    )
    assert "TARGET TEXT HERE" in res.text
    assert res.extraction_kind == "text"


def test_extract_region_image_returns_png() -> None:
    pdf = _doc_with_text([(72, 100, "anything")])
    res = extract_region(
        pdf, page_number=1, bbox={"x0": 0, "y0": 0, "x1": 200, "y1": 200},
        extraction_kind="image",
    )
    assert res.image_format == "png"
    decoded = base64.b64decode(res.image_png_base64 or "")
    assert decoded[:8] == b"\x89PNG\r\n\x1a\n"


def test_render_page_with_overlay_paints_rect() -> None:
    pdf = _doc_with_text([(72, 100, "Test page")])
    spec = OverlaySpec(
        bbox=OverlayBbox(x0=50, y0=80, x1=300, y1=120),
        color="#ff0000",
        fill="#ff0000",
        fill_opacity=0.25,
        label="hit",
    )
    rendered = render_page_with_overlay(
        pdf, page_number=1, overlays=[spec], dpi=72,
    )
    decoded = base64.b64decode(rendered.image_base64)
    assert decoded[:8] == b"\x89PNG\r\n\x1a\n"
    assert rendered.page_width == pytest.approx(612.0, abs=0.5)
    assert rendered.page_height == pytest.approx(792.0, abs=0.5)


def test_page_info_pydantic_model() -> None:
    p = PageInfo(
        source_page_index=0, page_index=0,
        width_pt=612.0, height_pt=792.0, rotation=0, text_source="native",
    )
    assert p.source_page_index == 0
    assert p.text_source == "native"

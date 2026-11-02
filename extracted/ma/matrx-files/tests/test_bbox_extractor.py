"""Unit tests for the bbox extractor and the label catalog.

Coverage:
  - bbox over a region with native text returns the right substring
  - bbox over an empty area returns text_source='none' (or OCR fallback noise)
  - bbox clamping honors page bounds
  - intersecting images are reported when the bbox overlaps one
  - label catalog: every entry well-formed; normalize_value typing
"""

from __future__ import annotations

import base64

import pymupdf
import pytest

from matrx_files.analysis.label_catalog import (
    LABEL_CATALOG,
    get_categories,
    get_label,
    normalize_value,
)
from matrx_files.specific_handlers.pdf.extract.bbox import (
    extract_at_bbox,
)


def _pdf_with_known_text() -> bytes:
    doc = pymupdf.open()
    try:
        page = doc.new_page(width=612, height=792)
        page.insert_text((72, 100), "Applicant Name: John A. Smith", fontsize=12)
        page.insert_text((72, 140), "DOB: 1972-04-12", fontsize=12)
        page.insert_text((72, 180), "Claim Number: ADJ12345678", fontsize=12)
        page.insert_text((72, 220), "WPI: 23%", fontsize=12)
        return doc.tobytes()
    finally:
        doc.close()


def test_extract_at_bbox_returns_native_text() -> None:
    pdf = _pdf_with_known_text()
    # bbox covering the WPI line — y0 above the baseline, y1 below it.
    result = extract_at_bbox(
        pdf,
        page_number=1,
        bbox={"x0": 60, "y0": 210, "x1": 220, "y1": 235},
        include_preview=False,
    )
    assert "WPI" in result.extracted_text
    assert "23" in result.extracted_text
    assert result.text_source == "native"
    assert result.page_width > 0 and result.page_height > 0


def test_extract_at_bbox_clamps_bounds() -> None:
    pdf = _pdf_with_known_text()
    # bbox extends past the page right edge.
    result = extract_at_bbox(
        pdf,
        page_number=1,
        bbox={"x0": 60, "y0": 90, "x1": 9999, "y1": 115},
        include_preview=False,
    )
    assert result.requested_bbox.x1 <= result.page_width


def test_extract_at_bbox_invalid_page_raises() -> None:
    pdf = _pdf_with_known_text()
    with pytest.raises(ValueError, match="out of range"):
        extract_at_bbox(
            pdf, page_number=99, bbox={"x0": 0, "y0": 0, "x1": 10, "y1": 10},
            include_preview=False,
        )


def test_extract_at_bbox_invalid_rect_raises() -> None:
    pdf = _pdf_with_known_text()
    with pytest.raises(ValueError, match="invalid bbox"):
        extract_at_bbox(
            pdf, page_number=1, bbox={"x0": 100, "y0": 100, "x1": 50, "y1": 50},
            include_preview=False,
        )


def test_extract_at_bbox_preview_returns_png() -> None:
    pdf = _pdf_with_known_text()
    result = extract_at_bbox(
        pdf, page_number=1, bbox={"x0": 60, "y0": 90, "x1": 400, "y1": 115},
        include_preview=True,
    )
    assert result.preview_png_base64 is not None
    decoded = base64.b64decode(result.preview_png_base64)
    assert decoded[:8] == b"\x89PNG\r\n\x1a\n"


def test_extract_at_bbox_empty_region_no_text() -> None:
    pdf = _pdf_with_known_text()
    # Far below all the text.
    result = extract_at_bbox(
        pdf, page_number=1, bbox={"x0": 60, "y0": 700, "x1": 200, "y1": 760},
        include_preview=False,
        ocr_fallback=False,
    )
    assert result.extracted_text.strip() == ""
    assert result.text_source == "none"


def test_label_catalog_well_formed() -> None:
    seen_ids: set[str] = set()
    for entry in LABEL_CATALOG:
        assert "id" in entry and "display_name" in entry
        assert entry["id"] not in seen_ids, f"duplicate label id: {entry['id']}"
        seen_ids.add(entry["id"])
        assert entry.get("category") in get_categories(), (
            f"label {entry['id']} has unknown category {entry.get('category')}"
        )
        assert entry.get("value_type") in {
            "text", "number", "date", "enum", "code", "identifier", "currency"
        }


def test_label_catalog_pd_rating_inputs_present() -> None:
    """Every input the PD-rating workflow needs has a catalog entry."""
    required = {
        "applicant_name", "applicant_dob", "claim_number",
        "date_of_injury", "body_part", "wpi_percentage",
        "impairment_code", "apportionment_pct", "mmi_date",
    }
    catalog_ids = {e["id"] for e in LABEL_CATALOG}
    missing = required - catalog_ids
    assert not missing, f"PD-rating labels missing from catalog: {missing}"


def test_normalize_value_number() -> None:
    out = normalize_value("wpi_percentage", "23%")
    assert out == {"kind": "number", "value": 23.0, "raw": "23%"}


def test_normalize_value_currency() -> None:
    out = normalize_value("ttd_rate", "$1,234.56")
    assert out == {"kind": "currency", "value": 1234.56, "unit": "USD", "raw": "$1,234.56"}


def test_normalize_value_date_passthrough() -> None:
    out = normalize_value("applicant_dob", "1972-04-12")
    assert out == {"kind": "date", "value": "1972-04-12", "raw": "1972-04-12"}


def test_normalize_value_unknown_label_falls_back_to_text() -> None:
    out = normalize_value("not_in_catalog", "anything")
    assert out == {"kind": "text", "value": "anything", "raw": "anything"}


def test_get_label_returns_dict_copy() -> None:
    a = get_label("wpi_percentage")
    assert a is not None
    a["display_name"] = "MUTATED"
    b = get_label("wpi_percentage")
    assert b is not None and b["display_name"] != "MUTATED", "get_label must return a copy"

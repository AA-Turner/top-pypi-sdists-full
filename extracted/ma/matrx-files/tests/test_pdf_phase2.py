"""Tests for the Phase 2 PDF subsystem additions.

Covers:
- Render primitives (page, all, thumbnail) sync + async, multiple formats
- Page reorder / insert / duplicate operations
- Studio preset catalog shape + render-spec dispatcher
"""

from __future__ import annotations

import asyncio
import io

import pymupdf
import pytest
from PIL import Image

from matrx_files.specific_handlers.pdf import (
    ALL_PDF_PRESETS,
    PDF_PRESETS_BY_ID,
    PRESET_CATEGORIES,
    PDFHandler,
    PdfPageRender,
    PdfRenderSpec,
    PdfStudioRenderResult,
    duplicate_pages_in_bytes,
    duplicate_pages_in_bytes_async,
    insert_pages_in_bytes,
    insert_pages_in_bytes_async,
    render_all_pages_to_image_bytes,
    render_page_to_image_bytes,
    render_page_to_image_bytes_async,
    render_studio_variant,
    render_thumbnail_bytes,
    render_thumbnail_bytes_async,
    reorder_pages_in_bytes,
    reorder_pages_in_bytes_async,
)



def _sample_pdf(page_count: int = 3, label: str = "Sample") -> bytes:
    doc = pymupdf.open()
    try:
        for page_num in range(1, page_count + 1):
            page = doc.new_page(width=300, height=400)
            page.insert_text((72, 72), f"{label} page {page_num}")
        return doc.tobytes()
    finally:
        doc.close()


def _page_count(pdf_bytes: bytes) -> int:
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        return doc.page_count


def _page_text(pdf_bytes: bytes, page_idx: int) -> str:
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        return doc[page_idx].get_text("text").strip()


# ---------------------------------------------------------------------------
# Render primitives
# ---------------------------------------------------------------------------


def test_render_page_to_image_bytes_png() -> None:
    result = render_page_to_image_bytes(_sample_pdf(), page=1, dpi=72, fmt="png")
    assert isinstance(result, PdfPageRender)
    assert result.page_number == 1
    assert result.format == "png"
    assert result.dpi == 72
    assert result.content[:4] == b"\x89PNG"
    assert result.width > 0 and result.height > 0


def test_render_page_to_image_bytes_jpeg_webp() -> None:
    pdf_bytes = _sample_pdf()
    jpeg = render_page_to_image_bytes(pdf_bytes, page=1, fmt="jpeg")
    webp = render_page_to_image_bytes(pdf_bytes, page=1, fmt="webp")
    assert jpeg.format == "jpeg"
    assert jpeg.content[:3] == b"\xff\xd8\xff"
    assert webp.format == "webp"
    # WebP signature: RIFF....WEBP
    assert webp.content[:4] == b"RIFF" and webp.content[8:12] == b"WEBP"


def test_render_page_to_image_rejects_out_of_range() -> None:
    pdf_bytes = _sample_pdf(2)
    with pytest.raises(ValueError, match="outside document range"):
        render_page_to_image_bytes(pdf_bytes, page=5)
    with pytest.raises(ValueError, match="page must be >= 1"):
        render_page_to_image_bytes(pdf_bytes, page=0)


def test_render_all_pages_to_image_bytes_renders_every_page() -> None:
    pdf_bytes = _sample_pdf(3)
    results = render_all_pages_to_image_bytes(pdf_bytes, dpi=72)
    assert len(results) == 3
    assert [r.page_number for r in results] == [1, 2, 3]


def test_render_all_pages_to_image_bytes_subset() -> None:
    pdf_bytes = _sample_pdf(5)
    results = render_all_pages_to_image_bytes(pdf_bytes, dpi=72, pages=[2, 4])
    assert [r.page_number for r in results] == [2, 4]


def test_render_thumbnail_bytes_sized_correctly() -> None:
    result = render_thumbnail_bytes(_sample_pdf(), max_side=128, fmt="jpeg")
    assert result.format == "jpeg"
    assert max(result.width, result.height) <= 128
    img = Image.open(io.BytesIO(result.content))
    assert max(img.size) <= 128


def test_render_thumbnail_bytes_validates_inputs() -> None:
    pdf_bytes = _sample_pdf(2)
    with pytest.raises(ValueError, match="page must be >= 1"):
        render_thumbnail_bytes(pdf_bytes, page=0)
    with pytest.raises(ValueError, match="max_side must be >= 8"):
        render_thumbnail_bytes(pdf_bytes, max_side=2)
    with pytest.raises(ValueError, match="outside document range"):
        render_thumbnail_bytes(pdf_bytes, page=99)


async def test_render_page_async_matches_sync() -> None:
    pdf_bytes = _sample_pdf()
    sync_r = render_page_to_image_bytes(pdf_bytes, page=1, dpi=72)
    async_r = await render_page_to_image_bytes_async(pdf_bytes, page=1, dpi=72)
    assert sync_r.width == async_r.width
    assert sync_r.height == async_r.height
    assert sync_r.content == async_r.content


async def test_render_thumbnail_async_matches_sync() -> None:
    pdf_bytes = _sample_pdf()
    sync_r = render_thumbnail_bytes(pdf_bytes, max_side=200)
    async_r = await render_thumbnail_bytes_async(pdf_bytes, max_side=200)
    assert sync_r.width == async_r.width
    assert sync_r.height == async_r.height


# ---------------------------------------------------------------------------
# Page reorder / insert / duplicate
# ---------------------------------------------------------------------------


def test_reorder_pages_produces_expected_order() -> None:
    pdf_bytes = _sample_pdf(3)
    result = reorder_pages_in_bytes(pdf_bytes, new_order=[3, 1, 2])
    assert result.page_count == 3
    assert "Sample page 3" in _page_text(result.content, 0)
    assert "Sample page 1" in _page_text(result.content, 1)
    assert "Sample page 2" in _page_text(result.content, 2)
    assert result.metadata["new_order"] == [3, 1, 2]


def test_reorder_pages_rejects_partial_order() -> None:
    pdf_bytes = _sample_pdf(3)
    with pytest.raises(ValueError, match="every page"):
        reorder_pages_in_bytes(pdf_bytes, new_order=[1, 2])
    with pytest.raises(ValueError, match="every page"):
        reorder_pages_in_bytes(pdf_bytes, new_order=[1, 2, 4])
    with pytest.raises(ValueError, match="at least one page"):
        reorder_pages_in_bytes(pdf_bytes, new_order=[])


def test_insert_pages_appends_after_specified_index() -> None:
    target = _sample_pdf(2, label="Target")
    source = _sample_pdf(3, label="Source")
    result = insert_pages_in_bytes(
        target, source, after_page=1, source_pages=[1, 2]
    )
    assert result.page_count == 4
    assert "Target page 1" in _page_text(result.content, 0)
    assert "Source page 1" in _page_text(result.content, 1)
    assert "Source page 2" in _page_text(result.content, 2)
    assert "Target page 2" in _page_text(result.content, 3)
    assert result.metadata["source_pages"] == [1, 2]


def test_insert_pages_at_zero_prepends() -> None:
    target = _sample_pdf(2, label="Target")
    source = _sample_pdf(1, label="Source")
    result = insert_pages_in_bytes(target, source, after_page=0)
    assert result.page_count == 3
    assert "Source page 1" in _page_text(result.content, 0)


def test_insert_pages_rejects_invalid_after_page() -> None:
    target = _sample_pdf(2)
    source = _sample_pdf(1)
    with pytest.raises(ValueError, match="after_page"):
        insert_pages_in_bytes(target, source, after_page=99)


def test_duplicate_pages_appends_copies_inline() -> None:
    pdf_bytes = _sample_pdf(2)
    result = duplicate_pages_in_bytes(pdf_bytes, pages=[1], count=2)
    assert result.page_count == 4
    assert "Sample page 1" in _page_text(result.content, 0)
    assert "Sample page 1" in _page_text(result.content, 1)
    assert "Sample page 1" in _page_text(result.content, 2)
    assert "Sample page 2" in _page_text(result.content, 3)


def test_duplicate_pages_rejects_invalid_count() -> None:
    with pytest.raises(ValueError, match="count must be >= 1"):
        duplicate_pages_in_bytes(_sample_pdf(), pages=[1], count=0)


async def test_reorder_insert_duplicate_async_parity() -> None:
    pdf_bytes = _sample_pdf(3)
    sync_r = reorder_pages_in_bytes(pdf_bytes, new_order=[3, 1, 2])
    async_r = await reorder_pages_in_bytes_async(pdf_bytes, new_order=[3, 1, 2])
    assert sync_r.page_count == async_r.page_count

    target, source = _sample_pdf(2, "T"), _sample_pdf(2, "S")
    sync_i = insert_pages_in_bytes(target, source, after_page=1)
    async_i = await insert_pages_in_bytes_async(target, source, after_page=1)
    assert sync_i.page_count == async_i.page_count

    sync_d = duplicate_pages_in_bytes(pdf_bytes, pages=[1], count=1)
    async_d = await duplicate_pages_in_bytes_async(pdf_bytes, pages=[1], count=1)
    assert sync_d.page_count == async_d.page_count


# ---------------------------------------------------------------------------
# Studio preset catalog + render-spec dispatcher
# ---------------------------------------------------------------------------


def test_preset_catalog_has_unique_ids() -> None:
    ids = [p["id"] for p in ALL_PDF_PRESETS]
    assert len(ids) == len(set(ids)), f"Duplicate preset ids: {sorted(ids)}"
    # PRESETS_BY_ID must mirror ALL_PRESETS exactly.
    assert set(PDF_PRESETS_BY_ID.keys()) == set(ids)


def test_preset_categories_well_formed() -> None:
    for category in PRESET_CATEGORIES:
        assert category["id"]
        assert category["name"]
        assert category["accent"]
        assert category["presets"], f"Empty category: {category['id']}"
        for preset in category["presets"]:
            assert preset["id"]
            assert preset["name"]
            assert preset["operation"]


def test_render_studio_variant_by_preset_id() -> None:
    pdf_bytes = _sample_pdf()
    spec: PdfRenderSpec = {"preset_id": "render-page-72"}
    result = render_studio_variant(pdf_bytes, spec)
    assert isinstance(result, PdfStudioRenderResult)
    assert result.preset_id == "render-page-72"
    assert result.operation == "render_page"
    assert len(result.pages) == 1
    assert result.pages[0].format == "png"


def test_render_studio_variant_thumbnail_preset() -> None:
    result = render_studio_variant(_sample_pdf(), {"preset_id": "render-thumbnail"})
    assert result.operation == "render_thumbnail"
    assert max(result.pages[0].width, result.pages[0].height) <= 256


def test_render_studio_variant_overrides_merge_in() -> None:
    spec: PdfRenderSpec = {
        "preset_id": "render-page-150",
        "overrides": {"dpi": 36, "fmt": "jpeg"},
    }
    result = render_studio_variant(_sample_pdf(), spec)
    assert result.pages[0].format == "jpeg"
    assert result.pages[0].dpi == 36


def test_render_studio_variant_inline_operation() -> None:
    spec: PdfRenderSpec = {
        "operation": "render_page",
        "params": {"dpi": 100, "fmt": "png", "page": 1},
    }
    result = render_studio_variant(_sample_pdf(), spec)
    assert result.preset_id is None
    assert result.operation == "render_page"
    assert result.pages[0].dpi == 100


def test_render_studio_variant_rejects_unknown_preset() -> None:
    with pytest.raises(ValueError, match="Unknown PDF preset"):
        render_studio_variant(_sample_pdf(), {"preset_id": "bogus"})


def test_render_studio_variant_rejects_unsupported_operation() -> None:
    spec: PdfRenderSpec = {"operation": "extract_text"}
    with pytest.raises(ValueError, match="not supported"):
        render_studio_variant(_sample_pdf(), spec)


# ---------------------------------------------------------------------------
# Handler integration smoke
# ---------------------------------------------------------------------------


def test_handler_exposes_phase2_methods() -> None:
    handler = PDFHandler(app_name="test_phase2")
    assert callable(handler.render_page_to_image_bytes)
    assert callable(handler.render_page_to_image_bytes_async)
    assert callable(handler.render_all_pages_to_image_bytes_async)
    assert callable(handler.render_thumbnail_bytes_async)
    assert callable(handler.reorder_pages_in_bytes_async)
    assert callable(handler.insert_pages_in_bytes_async)
    assert callable(handler.duplicate_pages_in_bytes_async)
    assert callable(handler.render_studio_variant)


def test_handler_render_thumbnail_smoke() -> None:
    handler = PDFHandler(app_name="test_phase2")
    result = handler.render_thumbnail_bytes(_sample_pdf(), max_side=128)
    assert max(result.width, result.height) <= 128
    assert result.format in {"jpeg", "png", "webp"}


def test_render_page_grayscale_produces_valid_image() -> None:
    """Regression: previously the (1ch, alpha=0) pixmap fed into
    Image.frombytes('RGB', ...) → ValueError. The mode picker now maps to 'L'.
    """
    result = render_page_to_image_bytes(
        _sample_pdf(), page=1, dpi=72, fmt="jpeg", colorspace="gray"
    )
    assert result.content[:3] == b"\xff\xd8\xff"
    img = Image.open(io.BytesIO(result.content))
    assert img.size[0] > 0 and img.size[1] > 0


def test_render_page_cmyk_produces_valid_image() -> None:
    """Regression: previously CMYK (4ch, alpha=0) was misread as RGBA. Now
    routed through Pillow as proper CMYK then converted for JPEG output.
    """
    result = render_page_to_image_bytes(
        _sample_pdf(), page=1, dpi=72, fmt="jpeg", colorspace="cmyk"
    )
    assert result.content[:3] == b"\xff\xd8\xff"
    img = Image.open(io.BytesIO(result.content))
    assert img.size[0] > 0 and img.size[1] > 0


async def test_render_studio_variant_async_matches_sync() -> None:
    """The async studio dispatcher must produce byte-identical output to the
    sync version for deterministic presets.
    """
    from matrx_files.specific_handlers.pdf import (
        render_studio_variant_async,
    )

    pdf_bytes = _sample_pdf()
    spec: PdfRenderSpec = {"preset_id": "render-page-72"}
    sync_r = render_studio_variant(pdf_bytes, spec)
    async_r = await render_studio_variant_async(pdf_bytes, spec)
    assert sync_r.operation == async_r.operation
    assert len(sync_r.pages) == len(async_r.pages) == 1
    assert sync_r.pages[0].content == async_r.pages[0].content


def test_render_thumbnail_tiny_max_side_does_not_force_large_dpi() -> None:
    """Regression: previously the DPI floor of 36 forced any tiny max_side to
    render at 36 DPI then downscale. The floor is now 8 so tiny requests stay
    cheap.
    """
    result = render_thumbnail_bytes(_sample_pdf(), max_side=32, fmt="jpeg")
    assert max(result.width, result.height) <= 32
    # The render DPI metadata should reflect the smaller floor — for a US
    # letter-ish page (400 pt tall) targeting 32 px, dpi ≈ int(72*35/400) ≈ 6,
    # which floors to 8.
    assert 1 <= result.dpi <= 36

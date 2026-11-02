"""Assemble scanner photos (and existing PDFs) into ONE PDF.

The phone-scanner flow (``POST /utilities/pdf/from-images``) sends an
ordered list of items: photos with an optional document quad + rotation,
and whole PDFs to append verbatim. This module turns that list into a
single PDF's bytes.

Quality contract (OCR happens downstream on this PDF):
- Images embed at FULL source resolution — the rectified output size is
  the quad's max opposing edge lengths (``perspective_crop`` default),
  never downscaled.
- Page rects are sized so the downstream OCR render (300 DPI via
  ``ocr_pymupdf_page``) reproduces the embedded image at EXACTLY native
  resolution: ``width_pt = px_width * 72 / 300``. A fixed Letter-width
  page silently downsampled a 4000px photo to 2550px before Tesseract —
  the single biggest OCR-quality loss in the chain. Clamped to sane
  page sizes; small images upsample (harmless), huge ones stay 1:1.
- JPEG quality 92 — visually lossless for documents, still ~3x smaller
  than PNG on photos.

Quad coordinates are **post-EXIF-transpose pixels** — exactly what
``/images/detect-document`` returns and what ``perspective_crop``
consumes. Rotation is clockwise degrees, applied AFTER the crop.
"""

from __future__ import annotations

import asyncio
import io
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from PIL import Image, ImageOps

from ..image_ops.geometry import PerspectiveCropOp, PerspectiveCropParams
from .internal import load_pymupdf

try:  # pragma: no cover - environment-dependent
    from pillow_heif import register_heif_opener  # type: ignore

    register_heif_opener()
except ImportError:  # pragma: no cover
    pass

# US Letter width in points — fallback only (used when an image somehow
# has no measurable width). Real pages are sized from the image's pixel
# width so the 300-DPI OCR render is pixel-exact (see _page_width_pt).
DEFAULT_PAGE_WIDTH_PT = 612.0
DEFAULT_JPEG_QUALITY = 92

# The DPI ``ocr_pymupdf_page`` renders at. Page geometry targets a 1:1
# pixel mapping at this density.
OCR_TARGET_DPI = 300
# Page-size clamps (points): 4in .. 20in wide. Below the floor the OCR
# render upsamples (fine); above the ceiling we'd exceed sane PDF page
# sizes for display, so very-high-res images render slightly downsampled.
_MIN_PAGE_WIDTH_PT = 288.0
_MAX_PAGE_WIDTH_PT = 1440.0


def _page_width_pt(image_px_width: int) -> float:
    """Page width (points) so a 300-DPI render reproduces native pixels."""
    if image_px_width <= 0:
        return DEFAULT_PAGE_WIDTH_PT
    ideal = image_px_width * 72.0 / OCR_TARGET_DPI
    return min(_MAX_PAGE_WIDTH_PT, max(_MIN_PAGE_WIDTH_PT, ideal))


@dataclass
class ScanPdfInputItem:
    raw_bytes: bytes
    kind: str = "image"  # "image" | "pdf"
    # Corner name -> (x, y): top_left / top_right / bottom_right / bottom_left.
    quad: dict[str, Any] | None = None
    rotation: int = 0  # clockwise degrees: 0 | 90 | 180 | 270
    label: str = ""  # for error messages only

    extra: dict[str, Any] = field(default_factory=dict)


def _prepare_image(item: ScanPdfInputItem) -> Image.Image:
    image = ImageOps.exif_transpose(Image.open(io.BytesIO(item.raw_bytes)))
    if item.quad:
        params = PerspectiveCropParams(
            top_left=tuple(item.quad["top_left"]),
            top_right=tuple(item.quad["top_right"]),
            bottom_right=tuple(item.quad["bottom_right"]),
            bottom_left=tuple(item.quad["bottom_left"]),
        )
        image = PerspectiveCropOp().apply(image, None, params)
    rotation = int(item.rotation or 0) % 360
    if rotation:
        if rotation not in (90, 180, 270):
            raise ValueError(f"rotation must be 0/90/180/270, got {item.rotation}")
        # PIL rotates counter-clockwise; the wire contract is clockwise.
        image = image.rotate(-rotation, expand=True)
    if image.mode != "RGB":
        if image.mode == "RGBA":
            bg = Image.new("RGB", image.size, (255, 255, 255))
            bg.paste(image, mask=image.split()[-1])
            image = bg
        else:
            image = image.convert("RGB")
    return image


def build_scan_pdf(
    items: list[ScanPdfInputItem],
    *,
    jpeg_quality: int = DEFAULT_JPEG_QUALITY,
    on_item_done: Callable[[int, int], None] | None = None,
) -> tuple[bytes, int]:
    """Build one PDF from ordered items. Returns ``(pdf_bytes, page_count)``.

    CPU-bound — call via the async wrapper (or an executor) from routes.
    ``on_item_done(index, total)`` fires after each item for progress
    reporting (called from the worker thread — keep it thread-safe).
    """
    if not items:
        raise ValueError("At least one item is required.")
    pymupdf = load_pymupdf()
    doc = pymupdf.open()
    try:
        total = len(items)
        for idx, item in enumerate(items):
            if item.kind == "pdf":
                src = pymupdf.open(stream=item.raw_bytes, filetype="pdf")
                try:
                    if src.page_count == 0:
                        raise ValueError(f"PDF item {item.label or idx} has no pages")
                    doc.insert_pdf(src)
                finally:
                    src.close()
            elif item.kind == "image":
                image = _prepare_image(item)
                buf = io.BytesIO()
                image.save(buf, "JPEG", quality=jpeg_quality)
                w, h = image.size
                page_width_pt = _page_width_pt(w)
                page_height_pt = page_width_pt * (h / w)
                page = doc.new_page(width=page_width_pt, height=page_height_pt)
                page.insert_image(page.rect, stream=buf.getvalue())
            else:
                raise ValueError(
                    f"Unknown item kind {item.kind!r} (item {item.label or idx}); "
                    "expected 'image' or 'pdf'."
                )
            if on_item_done:
                on_item_done(idx, total)
        page_count = doc.page_count
        pdf_bytes = doc.tobytes(garbage=3, deflate=True)
        return pdf_bytes, page_count
    finally:
        doc.close()


async def build_scan_pdf_async(
    items: list[ScanPdfInputItem],
    *,
    jpeg_quality: int = DEFAULT_JPEG_QUALITY,
    on_item_done: Callable[[int, int], None] | None = None,
) -> tuple[bytes, int]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        lambda: build_scan_pdf(
            items,
            jpeg_quality=jpeg_quality,
            on_item_done=on_item_done,
        ),
    )

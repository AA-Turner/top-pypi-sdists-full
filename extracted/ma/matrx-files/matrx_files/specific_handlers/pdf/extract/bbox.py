"""Extract content at a specific page bounding box.

Backs the user-region annotation flow: given a (page, bbox), return whatever
the system can tell us about what lives there — text (native or OCR), any
intersecting embedded images, an optional preview render, and source metadata.
Pure function over PDF bytes; never persists.

Coordinate system: PDF user-space points (origin top-left as PyMuPDF returns
from page.rect / page.get_text — i.e. y0 is near the top of the page).
"""

from __future__ import annotations

import base64
import io
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, Field

from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf
from .ocr import ocr_image_bytes


# Heuristic: chars-per-square-inch below this density triggers OCR fallback.
# Tuned against the analysis pipeline's OCR router.
_OCR_DENSITY_THRESHOLD = 8.0
_PREVIEW_DPI = 144


class BboxRect(BaseModel):
    x0: float
    y0: float
    x1: float
    y1: float


class IntersectingImage(BaseModel):
    xref: int
    width: int = 0
    height: int = 0
    bbox: BboxRect | None = None
    """Image's own bbox on the page. None when PyMuPDF couldn't resolve placement."""


class BboxExtractionResult(BaseModel):
    page_number: int = Field(ge=1)
    page_width: float
    page_height: float
    requested_bbox: BboxRect
    extracted_text: str
    text_source: str  # "native" | "ocr" | "mixed" | "none"
    char_count: int = 0
    intersecting_images: list[IntersectingImage] = Field(default_factory=list)
    preview_png_base64: str | None = None
    """Cropped page render at the bbox, base64-encoded PNG. Set when
    include_preview=True. Convenient for FE thumbnails."""
    notes: list[str] = Field(default_factory=list)


def _to_text_space(page: Any, rect: Any) -> Any:
    """A visual-space rect (what the person drew on the rotated page) in text-extraction space."""
    if not page.rotation:
        return rect
    mapped = rect * page.derotation_matrix
    mapped.normalize()
    return mapped


def _to_visual_rect(page: Any, rect: Any) -> Any:
    """An unrotated-space rect (word, image) in the visual space the person sees."""
    if not page.rotation:
        return rect
    mapped = pymupdf_rect(rect) * page.rotation_matrix
    mapped.normalize()
    return mapped


def _visual_word(page: Any, word: Any) -> tuple:
    """A ``get_text("words")`` tuple with its box moved into visual space."""
    if not page.rotation or len(word) < 5:
        return tuple(word)
    box = _to_visual_rect(page, word[:4])
    return (box.x0, box.y0, box.x1, box.y1, *word[4:])


def pymupdf_rect(rect: Any) -> Any:
    return load_pymupdf().Rect(rect)


def _rect_intersects(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def _density_chars_per_in2(text: str, w_pt: float, h_pt: float) -> float:
    area_in2 = max(1.0, (w_pt / 72.0) * (h_pt / 72.0))
    return len(text) / area_in2


def extract_at_bbox(
    pdf_bytes: bytes,
    *,
    page_number: int,
    bbox: dict[str, float] | tuple[float, float, float, float] | BboxRect,
    include_preview: bool = True,
    preview_dpi: int = _PREVIEW_DPI,
    ocr_fallback: bool = True,
) -> BboxExtractionResult:
    """Extract everything at a page bbox.

    page_number is 1-based. bbox is in PDF user-space points.
    """
    if isinstance(bbox, BboxRect):
        x0, y0, x1, y1 = bbox.x0, bbox.y0, bbox.x1, bbox.y1
    elif isinstance(bbox, dict):
        x0, y0, x1, y1 = float(bbox["x0"]), float(bbox["y0"]), float(bbox["x1"]), float(bbox["y1"])
    else:
        x0, y0, x1, y1 = (float(v) for v in bbox)
    if x1 <= x0 or y1 <= y0:
        raise ValueError(f"invalid bbox: x0={x0} y0={y0} x1={x1} y1={y1}")

    pymupdf = load_pymupdf()
    notes: list[str] = []
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        if page_number < 1 or page_number > doc.page_count:
            raise ValueError(
                f"page_number {page_number} out of range (doc has {doc.page_count} pages)"
            )
        page = doc[page_number - 1]
        rect = page.rect

        # Clamp bbox to page bounds.
        cx0 = max(0.0, min(x0, float(rect.width)))
        cy0 = max(0.0, min(y0, float(rect.height)))
        cx1 = max(0.0, min(x1, float(rect.width)))
        cy1 = max(0.0, min(y1, float(rect.height)))
        if cx1 <= cx0 or cy1 <= cy0:
            notes.append("bbox is outside page bounds after clamping")

        clip = pymupdf.Rect(cx0, cy0, cx1, cy1)

        # Native text extraction in the clip rect.
        native_text = ""
        try:
            # The box is in the VISUAL space (page.rect, rotation applied); PyMuPDF's
            # text clip lives in unrotated page space, so map it back first.
            native_text = page.get_text("text", clip=_to_text_space(page, clip), sort=True) or ""
        except Exception as exc:
            notes.append(f"native text extraction failed: {exc!r}")
        native_text = native_text.strip()

        text_source = "native" if native_text else "none"
        extracted_text = native_text

        # OCR fallback when native text is empty or suspiciously sparse.
        if ocr_fallback:
            density = _density_chars_per_in2(native_text, clip.width, clip.height)
            should_ocr = (not native_text) or density < _OCR_DENSITY_THRESHOLD
            if should_ocr:
                try:
                    # Render just the clip rect at OCR-friendly DPI.
                    pix = page.get_pixmap(clip=clip, dpi=300, alpha=False)
                    ocr_text = ocr_image_bytes(bytes(pix.tobytes("png"))).strip()
                    if ocr_text:
                        if native_text and ocr_text != native_text:
                            extracted_text = (
                                native_text + "\n" + ocr_text
                                if len(ocr_text) > len(native_text)
                                else native_text
                            )
                            text_source = "mixed"
                        else:
                            extracted_text = ocr_text
                            text_source = "ocr"
                    elif not native_text:
                        notes.append("OCR returned empty result")
                except Exception as exc:
                    notes.append(f"OCR fallback failed: {exc!r}")

        # Intersecting embedded images.
        intersecting: list[IntersectingImage] = []
        try:
            for img in page.get_images(full=True):
                xref = int(img[0])
                width = int(img[2]) if len(img) > 2 else 0
                height = int(img[3]) if len(img) > 3 else 0
                try:
                    img_rects = page.get_image_rects(xref) or []
                except Exception:
                    img_rects = []
                for r in img_rects:
                    r = _to_visual_rect(page, r)
                    if _rect_intersects(
                        (cx0, cy0, cx1, cy1),
                        (float(r.x0), float(r.y0), float(r.x1), float(r.y1)),
                    ):
                        intersecting.append(IntersectingImage(
                            xref=xref,
                            width=width,
                            height=height,
                            bbox=BboxRect(
                                x0=float(r.x0), y0=float(r.y0),
                                x1=float(r.x1), y1=float(r.y1),
                            ),
                        ))
                        break
        except Exception as exc:
            notes.append(f"image enumeration failed: {exc!r}")

        # Cropped preview render.
        preview_b64: str | None = None
        if include_preview:
            try:
                pix = page.get_pixmap(clip=clip, dpi=preview_dpi, alpha=False)
                preview_b64 = base64.b64encode(bytes(pix.tobytes("png"))).decode("ascii")
            except Exception as exc:
                notes.append(f"preview render failed: {exc!r}")

        return BboxExtractionResult(
            page_number=page_number,
            page_width=float(rect.width),
            page_height=float(rect.height),
            requested_bbox=BboxRect(x0=cx0, y0=cy0, x1=cx1, y1=cy1),
            extracted_text=extracted_text,
            text_source=text_source,
            char_count=len(extracted_text),
            intersecting_images=intersecting,
            preview_png_base64=preview_b64,
            notes=notes,
        )


async def extract_at_bbox_async(
    pdf_bytes: bytes,
    *,
    page_number: int,
    bbox: dict[str, float] | tuple[float, float, float, float] | BboxRect,
    include_preview: bool = True,
    preview_dpi: int = _PREVIEW_DPI,
    ocr_fallback: bool = True,
) -> BboxExtractionResult:
    return await run_in_cpu_executor(
        lambda: extract_at_bbox(
            pdf_bytes,
            page_number=page_number,
            bbox=bbox,
            include_preview=include_preview,
            preview_dpi=preview_dpi,
            ocr_fallback=ocr_fallback,
        )
    )


def snap_to_text_blocks(
    pdf_bytes: bytes,
    *,
    page_number: int,
    bbox: dict[str, float] | tuple[float, float, float, float] | BboxRect,
    expand_pad_pt: float = 1.0,
) -> BboxRect:
    """Snap a user-drawn rect to the tightest union of WORDS it overlaps.

    Why word-level (not block-level): PyMuPDF blocks are paragraph-sized.
    If the user drags a tight rect over a single line of text, the block
    geometry includes adjacent lines in the same paragraph — the snapped
    bbox then grows to cover lines the user explicitly excluded. Word-level
    geometry honors the user's intent exactly.

    Algorithm:
      1. Read every word's bbox on the page.
      2. Keep words whose CENTER is inside the rough rect — that's the
         strictest test that still tolerates wobbly drags.
      3. If no word center is inside, fall back to words whose bbox simply
         intersects the rough rect (forgiving for tiny drags).
      4. If still nothing, return the rough rect unchanged.
      5. Return the tight union of chosen words + a small pad.

    Falls back to the input bbox when no words overlap (e.g. image-only
    regions or scanned pages with no text layer).
    """
    if isinstance(bbox, BboxRect):
        x0, y0, x1, y1 = bbox.x0, bbox.y0, bbox.x1, bbox.y1
    elif isinstance(bbox, dict):
        x0, y0, x1, y1 = float(bbox["x0"]), float(bbox["y0"]), float(bbox["x1"]), float(bbox["y1"])
    else:
        x0, y0, x1, y1 = (float(v) for v in bbox)
    if x1 <= x0 or y1 <= y0:
        raise ValueError(f"invalid bbox: x0={x0} y0={y0} x1={x1} y1={y1}")

    pymupdf = load_pymupdf()
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        if page_number < 1 or page_number > doc.page_count:
            raise ValueError(
                f"page_number {page_number} out of range (doc has {doc.page_count} pages)"
            )
        page = doc[page_number - 1]
        rect = page.rect
        # Clamp the rough rect to page bounds.
        x0 = max(0.0, min(x0, float(rect.width)))
        y0 = max(0.0, min(y0, float(rect.height)))
        x1 = max(0.0, min(x1, float(rect.width)))
        y1 = max(0.0, min(y1, float(rect.height)))

        try:
            words = page.get_text("words", sort=True) or []
        except Exception:
            words = []

        # Pass 1 — words whose center lies inside the rough rect. Strictest
        # match; honors the user's vertical intent (won't grab adjacent lines).
        chosen: list[tuple[float, float, float, float]] = []
        words = [_visual_word(page, w) for w in words]
        for w in words:
            if len(w) < 5:
                continue
            wx0, wy0, wx1, wy1 = float(w[0]), float(w[1]), float(w[2]), float(w[3])
            cx = (wx0 + wx1) / 2
            cy = (wy0 + wy1) / 2
            if x0 <= cx <= x1 and y0 <= cy <= y1:
                chosen.append((wx0, wy0, wx1, wy1))

        # Pass 2 — if center-test was too strict (e.g. user drew a tiny
        # rect inside a single word) fall back to any intersection.
        if not chosen:
            for w in words:
                if len(w) < 5:
                    continue
                wx0, wy0, wx1, wy1 = (
                    float(w[0]),
                    float(w[1]),
                    float(w[2]),
                    float(w[3]),
                )
                if wx1 <= x0 or wx0 >= x1 or wy1 <= y0 or wy0 >= y1:
                    continue
                chosen.append((wx0, wy0, wx1, wy1))

        if not chosen:
            # Nothing to snap to — return the (clamped) input rect.
            return BboxRect(x0=x0, y0=y0, x1=x1, y1=y1)

        sx0 = min(w[0] for w in chosen) - expand_pad_pt
        sy0 = min(w[1] for w in chosen) - expand_pad_pt
        sx1 = max(w[2] for w in chosen) + expand_pad_pt
        sy1 = max(w[3] for w in chosen) + expand_pad_pt
        sx0 = max(0.0, sx0)
        sy0 = max(0.0, sy0)
        sx1 = min(float(rect.width), sx1)
        sy1 = min(float(rect.height), sy1)
        return BboxRect(x0=sx0, y0=sy0, x1=sx1, y1=sy1)


async def snap_to_text_blocks_async(
    pdf_bytes: bytes,
    *,
    page_number: int,
    bbox: dict[str, float] | tuple[float, float, float, float] | BboxRect,
    expand_pad_pt: float = 1.0,
) -> BboxRect:
    return await run_in_cpu_executor(
        lambda: snap_to_text_blocks(
            pdf_bytes,
            page_number=page_number,
            bbox=bbox,
            expand_pad_pt=expand_pad_pt,
        )
    )


__all__ = [
    "BboxRect",
    "IntersectingImage",
    "BboxExtractionResult",
    "extract_at_bbox",
    "extract_at_bbox_async",
    "snap_to_text_blocks",
    "snap_to_text_blocks_async",
]

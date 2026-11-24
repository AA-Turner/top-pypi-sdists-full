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
    # Matrx Scan S7: the page's size in points (replaces 300-DPI sizing) and "this JPEG is the final
    # page — embed it as is" (no crop, no rotation, no second compression).
    page_size_pt: tuple[float, float] | None = None
    pass_through: bool = False

    extra: dict[str, Any] = field(default_factory=dict)


QUAD_CORNERS = ("top_left", "top_right", "bottom_right", "bottom_left")
#: A crop quad is in the picture's PIXELS (after its EXIF turn). A corner may sit this fraction of the
#: picture's side outside it (an edge detector's rounding); further out is not this picture's crop.
QUAD_EDGE_TOLERANCE = 0.02
#: With the picture's size known, a quad enclosing less than this many square pixels (or less than half
#: of a smaller picture) encloses no page; without it, only a quad under one square pixel is refused.
MIN_QUAD_AREA_PX = 64.0


def quad_problem(quad: Any, width_px: float | None = None, height_px: float | None = None) -> str | None:
    """Why a crop quad cannot crop a page, as a sentence naming the units expected — or None.

    Checked without the picture (the request door): every corner present, not 0-1 fractions, enclosing
    a real area, corners in top-left, top-right, bottom-right, bottom-left order. With the picture's size
    (the builder): every corner inside the picture."""
    try:
        points = [(float(quad[c][0]), float(quad[c][1])) for c in QUAD_CORNERS]
    except (KeyError, IndexError, TypeError, ValueError):
        return f"The crop quad needs four corners ({', '.join(QUAD_CORNERS)}), each an [x, y] pair in pixels."
    units = "Corners are in pixels of the picture as sent (after its EXIF turn), origin top-left."
    known = bool(width_px and height_px)
    if known and width_px <= 1 and height_px <= 1:
        return f"The picture is {width_px:g} x {height_px:g} px: a single pixel holds no page to crop."
    if all(0.0 <= v <= 1.0 for point in points for v in point):
        return (
            f"The crop quad {points} looks like 0-1 fractions of the picture. {units} "
            "Multiply x by the picture's width and y by its height."
        )
    area = 0.5 * abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1])))
    # Without the picture only a quad with no area is surely no page; with it, the floor is MIN_QUAD_AREA_PX
    # or half the picture, whichever is smaller, so the whole of a tiny picture is still a crop.
    floor = min(MIN_QUAD_AREA_PX, 0.5 * width_px * height_px) if known else 1.0
    if area < floor:
        return f"The crop quad {points} encloses {area:g} square pixels, so it holds no page. {units}"
    crosses = [
        (bx - ax) * (cy - by) - (by - ay) * (cx - bx)
        for (ax, ay), (bx, by), (cx, cy) in zip(points, points[1:] + points[:1], points[2:] + points[:2])
    ]
    if not (all(c > 0 for c in crosses) or all(c < 0 for c in crosses)):
        return (
            f"The crop quad's corners {points} cross over or fold in; give them in the order "
            f"{', '.join(QUAD_CORNERS)}. {units}"
        )
    if width_px and height_px:
        slack_x, slack_y = width_px * QUAD_EDGE_TOLERANCE, height_px * QUAD_EDGE_TOLERANCE
        outside = [
            f"{name} {point}" for name, point in zip(QUAD_CORNERS, points)
            if not (-slack_x <= point[0] <= width_px + slack_x and -slack_y <= point[1] <= height_px + slack_y)
        ]
        if outside:
            return (
                f"The crop quad's {', '.join(outside)} lies outside the picture, which is "
                f"{width_px:g} x {height_px:g} px. {units}"
            )
    return None


def _prepare_image(item: ScanPdfInputItem) -> Image.Image:
    image = ImageOps.exif_transpose(Image.open(io.BytesIO(item.raw_bytes)))
    if item.quad:
        problem = quad_problem(item.quad, *image.size)
        if problem:
            raise ValueError(f"Item {item.label or 'page'}: {problem}")
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


def _pass_through_jpeg(item: ScanPdfInputItem) -> tuple[bytes, int, int] | None:
    """The item's own JPEG bytes and pixel size when it can be embedded unchanged, else None.

    Only a JPEG with nothing left to do: no quad, no rotation, no EXIF turn (the bytes would show
    sideways), a colour mode a PDF shows as is. Anything else is prepared and compressed as usual."""
    if not item.pass_through or item.quad or int(item.rotation or 0) % 360 or not item.raw_bytes.startswith(b"\xff\xd8"):
        return None
    with Image.open(io.BytesIO(item.raw_bytes)) as image:
        if image.format != "JPEG" or image.mode not in ("RGB", "L", "CMYK"):
            return None
        if image.getexif().get(0x0112, 1) != 1:
            return None
        try:
            image.load()  # a full decode: a truncated or damaged JPEG must never be embedded as is
        except (OSError, SyntaxError) as exc:
            raise ValueError(f"Item {item.label or ''} is a damaged JPEG ({exc}); it was not saved.") from exc
        width, height = image.size
    return item.raw_bytes, width, height


#: A stated page size is the page the person picked (a reference scanner's "Document Size"): the page is
#: exactly that size and the picture is FITTED into it — whole, at its own proportions, centred, the rest of
#: the page white — never stretched, never refused for its shape (a page of nearly the picture's shape gets a
#: sliver of white, never a squash).
#: A page side under this is no page; over this the PDF format itself has no page (PDF 1.7, Annex C: 14,400
#: units without UserUnit). Format facts, not policy: a stated size outside them is refused in plain words.
MIN_PAGE_SIDE_PT = 36.0
MAX_PAGE_SIDE_PT = 14400.0
_FILLS_PAGE = 1e-6  # a fit this close to the whole page IS the whole page (float arithmetic, not a tolerance)

#: Where a picture sits on its page: ``(x0, y0, x1, y1)`` as fractions of the page's width and height,
#: top-left origin. ``None`` = the picture fills the page.
PictureBox = tuple[float, float, float, float]


def _stated_page_size(item: ScanPdfInputItem, width_px: int, height_px: int) -> tuple[float, float, PictureBox | None]:
    """The stated page's size and where the picture sits on it (the ONE place a scan page's geometry is decided)."""
    page_w, page_h = (float(v) for v in item.page_size_pt)  # type: ignore[union-attr]
    name = item.label or "page"
    if not (min(page_w, page_h) >= MIN_PAGE_SIDE_PT):  # also refuses nan
        raise ValueError(f"Item {name}: page size {page_w:g} x {page_h:g} pt is under {MIN_PAGE_SIDE_PT:g} pt a side.")
    if not (max(page_w, page_h) <= MAX_PAGE_SIDE_PT):
        raise ValueError(
            f"Item {name}: page size {page_w:g} x {page_h:g} pt is over {MAX_PAGE_SIDE_PT:g} pt a side, "
            "larger than a PDF page can be."
        )
    scale = min(page_w / width_px, page_h / height_px)
    fit_w, fit_h = width_px * scale / page_w, height_px * scale / page_h  # fractions of the page; one of them is 1
    if fit_w >= 1.0 - _FILLS_PAGE and fit_h >= 1.0 - _FILLS_PAGE:
        return page_w, page_h, None
    x0, y0 = (1.0 - fit_w) / 2.0, (1.0 - fit_h) / 2.0
    return page_w, page_h, (x0, y0, x0 + fit_w, y0 + fit_h)


@dataclass
class ScanPdfBuild:
    """One built scan PDF, and where each image page's picture sits (1-based page -> ``PictureBox``;
    ``None`` = fills the page). A PDF item's pages are not in ``picture_boxes``: they are inserted as they are."""

    pdf_bytes: bytes
    page_count: int
    picture_boxes: dict[int, PictureBox | None] = field(default_factory=dict)


def assemble_scan_pdf(
    items: list[ScanPdfInputItem],
    *,
    jpeg_quality: int = DEFAULT_JPEG_QUALITY,
    on_item_done: Callable[[int, int], None] | None = None,
) -> ScanPdfBuild:
    """Build one PDF from ordered items, saying where each picture landed (a text layer drawn over a fitted
    picture must sit on the picture, not on the page). CPU-bound — call the async wrapper from routes.
    ``on_item_done(index, total)`` fires after each item for progress reporting (from the worker thread)."""
    if not items:
        raise ValueError("At least one item is required.")
    pymupdf = load_pymupdf()
    doc = pymupdf.open()
    boxes: dict[int, PictureBox | None] = {}
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
                passed = _pass_through_jpeg(item)
                if passed is not None:
                    jpeg, w, h = passed
                else:
                    image = _prepare_image(item)
                    buf = io.BytesIO()
                    image.save(buf, "JPEG", quality=jpeg_quality)
                    jpeg = buf.getvalue()
                    w, h = image.size
                box: PictureBox | None = None
                if item.page_size_pt:
                    page_width_pt, page_height_pt, box = _stated_page_size(item, w, h)
                else:
                    page_width_pt = _page_width_pt(w)
                    page_height_pt = page_width_pt * (h / w)
                page = doc.new_page(width=page_width_pt, height=page_height_pt)
                if box is None:
                    page.insert_image(page.rect, stream=jpeg)
                else:
                    x0, y0, x1, y1 = box
                    page.insert_image(
                        pymupdf.Rect(x0 * page_width_pt, y0 * page_height_pt, x1 * page_width_pt, y1 * page_height_pt),
                        stream=jpeg,
                    )
                boxes[doc.page_count] = box
            else:
                raise ValueError(
                    f"Unknown item kind {item.kind!r} (item {item.label or idx}); "
                    "expected 'image' or 'pdf'."
                )
            if on_item_done:
                on_item_done(idx, total)
        page_count = doc.page_count
        pdf_bytes = doc.tobytes(garbage=3, deflate=True)
        return ScanPdfBuild(pdf_bytes=pdf_bytes, page_count=page_count, picture_boxes=boxes)
    finally:
        doc.close()


def build_scan_pdf(
    items: list[ScanPdfInputItem],
    *,
    jpeg_quality: int = DEFAULT_JPEG_QUALITY,
    on_item_done: Callable[[int, int], None] | None = None,
) -> tuple[bytes, int]:
    """Build one PDF from ordered items. Returns ``(pdf_bytes, page_count)`` (``assemble_scan_pdf`` also
    says where each picture sits)."""
    built = assemble_scan_pdf(items, jpeg_quality=jpeg_quality, on_item_done=on_item_done)
    return built.pdf_bytes, built.page_count


async def assemble_scan_pdf_async(
    items: list[ScanPdfInputItem],
    *,
    jpeg_quality: int = DEFAULT_JPEG_QUALITY,
    on_item_done: Callable[[int, int], None] | None = None,
) -> ScanPdfBuild:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, lambda: assemble_scan_pdf(items, jpeg_quality=jpeg_quality, on_item_done=on_item_done)
    )


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

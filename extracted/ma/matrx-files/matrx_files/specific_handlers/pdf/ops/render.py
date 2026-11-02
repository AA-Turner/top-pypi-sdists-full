"""PDF → raster rendering.

Uses PyMuPDF's ``page.get_pixmap(dpi=, clip=, colorspace=, alpha=)`` for every
output format. WebP support comes via PyMuPDF >= 1.24; older versions fall
back to PNG when an unsupported format is requested.

Standard surfaces:

- ``render_page_to_image_bytes(pdf_bytes, page, dpi, fmt, ...)`` — single page
- ``render_all_pages_to_image_bytes(pdf_bytes, dpi, fmt, ...)`` — every page
- ``render_thumbnail_bytes(pdf_bytes, page, max_side, fmt, ...)`` — sized for
  cld_files thumbnails (consumed by
  ``matrx_files.cloud_sync.processing.thumbnails``).
- ``render_pdf_to_pixmap(...)`` — low-level escape hatch returning a PIL Image.

The ``_async`` siblings push work to the matrx-pdf CPU executor.
"""

from __future__ import annotations

import asyncio
import queue as _queue
import threading
from collections.abc import AsyncIterator
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Literal

from PIL import Image

from ..concurrency import get_cpu_executor, run_in_cpu_executor
from ..internal import load_pymupdf


RenderFormat = Literal["png", "jpg", "jpeg", "webp", "tiff"]
RenderColorspace = Literal["rgb", "rgba", "gray", "cmyk"]


@dataclass(frozen=True)
class PdfPageRender:
    """One page rendered to image bytes."""

    page_number: int
    width: int
    height: int
    format: str
    dpi: int
    content: bytes
    colorspace: str


def _pixmap_for_page(
    page: Any,
    pymupdf: Any,
    dpi: int,
    colorspace: RenderColorspace,
    alpha: bool,
    clip: tuple[float, float, float, float] | None,
    annotations: bool,
) -> Any:
    cs_map = {
        "rgb": pymupdf.csRGB,
        "rgba": pymupdf.csRGB,
        "gray": pymupdf.csGRAY,
        "cmyk": pymupdf.csCMYK,
    }
    cs = cs_map.get(colorspace, pymupdf.csRGB)
    rect = pymupdf.Rect(*clip) if clip else None
    return page.get_pixmap(
        dpi=dpi,
        colorspace=cs,
        alpha=alpha or colorspace == "rgba",
        clip=rect,
        annots=annotations,
    )


_PIL_MODE_BY_PIX: dict[tuple[int, int], str] = {
    # (channels, alpha) → PIL mode
    (1, 0): "L",      # grayscale
    (3, 0): "RGB",
    (4, 0): "CMYK",
    (1, 1): "LA",
    (3, 1): "RGBA",
    (4, 1): "RGBA",   # PyMuPDF returns 4-channel RGBA when alpha=1
}


def _pixmap_to_pil(pix: Any) -> Image.Image:
    mode = _PIL_MODE_BY_PIX.get((pix.n, pix.alpha))
    if mode is None:
        # Conservative fallback: convert in PyMuPDF first so Pillow gets a
        # known-good colorspace + alpha layout.
        return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return Image.frombytes(mode, (pix.width, pix.height), pix.samples)


def _pixmap_to_bytes(pix: Any, fmt: RenderFormat, jpeg_quality: int) -> bytes:
    fmt_l = fmt.lower()
    # PyMuPDF Pixmap.tobytes supports png/pnm/pgm/ppm/pbm/pam/psd/ps + jpg/jpeg.
    # For webp/tiff and for quality control on jpeg, route through Pillow.
    if fmt_l == "png":
        return pix.tobytes("png")
    img = _pixmap_to_pil(pix)
    if fmt_l in {"jpg", "jpeg"}:
        if img.mode not in {"RGB", "CMYK", "L"}:
            img = img.convert("RGB")
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=jpeg_quality, optimize=True)
        return buf.getvalue()
    if fmt_l == "webp":
        if img.mode in {"CMYK", "LA"}:
            img = img.convert("RGBA")
        buf = BytesIO()
        img.save(buf, format="WEBP", quality=jpeg_quality, method=6)
        return buf.getvalue()
    if fmt_l == "tiff":
        buf = BytesIO()
        img.save(buf, format="TIFF", compression="tiff_lzw")
        return buf.getvalue()
    # Fallback — return raw PNG via Pillow (CMYK/Gray-aware).
    if img.mode == "CMYK":
        img = img.convert("RGB")
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def render_page_to_image_bytes(
    pdf_bytes: bytes,
    page: int = 1,
    dpi: int = 150,
    fmt: RenderFormat = "png",
    colorspace: RenderColorspace = "rgb",
    alpha: bool = False,
    annotations: bool = True,
    jpeg_quality: int = 85,
    clip: tuple[float, float, float, float] | None = None,
) -> PdfPageRender:
    """Render a single page of *pdf_bytes* to image bytes.

    *page* is 1-based. Raises ``ValueError`` if outside the document range.
    *clip* is an optional ``(x0, y0, x1, y1)`` rect in page coordinates for
    sub-region rendering (used by Phase 5 figure extraction).
    """
    if page < 1:
        raise ValueError("page must be >= 1 (1-based).")
    pymupdf = load_pymupdf()
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        if page > doc.page_count:
            raise ValueError(
                f"page {page} is outside document range 1..{doc.page_count}"
            )
        pdf_page = doc[page - 1]
        pix = _pixmap_for_page(
            pdf_page, pymupdf, dpi, colorspace, alpha, clip, annotations
        )
        content = _pixmap_to_bytes(pix, fmt, jpeg_quality)
        return PdfPageRender(
            page_number=page,
            width=pix.width,
            height=pix.height,
            format=fmt.lower(),
            dpi=dpi,
            content=content,
            colorspace=colorspace,
        )


async def render_page_to_image_bytes_async(
    pdf_bytes: bytes,
    page: int = 1,
    dpi: int = 150,
    fmt: RenderFormat = "png",
    colorspace: RenderColorspace = "rgb",
    alpha: bool = False,
    annotations: bool = True,
    jpeg_quality: int = 85,
    clip: tuple[float, float, float, float] | None = None,
) -> PdfPageRender:
    return await run_in_cpu_executor(
        render_page_to_image_bytes,
        pdf_bytes,
        page,
        dpi,
        fmt,
        colorspace,
        alpha,
        annotations,
        jpeg_quality,
        clip,
    )


def render_all_pages_to_image_bytes(
    pdf_bytes: bytes,
    dpi: int = 150,
    fmt: RenderFormat = "png",
    colorspace: RenderColorspace = "rgb",
    alpha: bool = False,
    annotations: bool = True,
    jpeg_quality: int = 85,
    pages: list[int] | None = None,
) -> list[PdfPageRender]:
    """Render multiple pages of *pdf_bytes*. If *pages* is None, render every page."""
    pymupdf = load_pymupdf()
    results: list[PdfPageRender] = []
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        if pages is None:
            page_iter = range(1, doc.page_count + 1)
        else:
            page_iter = list(pages)
            for p in page_iter:
                if p < 1 or p > doc.page_count:
                    raise ValueError(
                        f"page {p} is outside document range 1..{doc.page_count}"
                    )
        for page_no in page_iter:
            pdf_page = doc[page_no - 1]
            pix = _pixmap_for_page(
                pdf_page, pymupdf, dpi, colorspace, alpha, None, annotations
            )
            content = _pixmap_to_bytes(pix, fmt, jpeg_quality)
            results.append(
                PdfPageRender(
                    page_number=page_no,
                    width=pix.width,
                    height=pix.height,
                    format=fmt.lower(),
                    dpi=dpi,
                    content=content,
                    colorspace=colorspace,
                )
            )
    return results


async def render_all_pages_to_image_bytes_async(
    pdf_bytes: bytes,
    dpi: int = 150,
    fmt: RenderFormat = "png",
    colorspace: RenderColorspace = "rgb",
    alpha: bool = False,
    annotations: bool = True,
    jpeg_quality: int = 85,
    pages: list[int] | None = None,
) -> list[PdfPageRender]:
    return await run_in_cpu_executor(
        render_all_pages_to_image_bytes,
        pdf_bytes,
        dpi,
        fmt,
        colorspace,
        alpha,
        annotations,
        jpeg_quality,
        pages,
    )


async def iter_render_pages_to_image_bytes(
    pdf_bytes: bytes,
    dpi: int = 150,
    fmt: RenderFormat = "png",
    colorspace: RenderColorspace = "rgb",
    alpha: bool = False,
    annotations: bool = True,
    jpeg_quality: int = 85,
    pages: list[int] | None = None,
    max_buffered: int = 2,
) -> AsyncIterator[PdfPageRender]:
    """Render pages ONE AT A TIME with bounded memory (streaming producer).

    ``render_all_pages_to_image_bytes*`` materializes every page image before
    returning — on a 500-page document at 150 DPI that is hundreds of MB held
    at once. This iterator keeps at most ``max_buffered`` rendered pages in
    flight: a single render thread (one thread owns the Document for its whole
    life — PyMuPDF's threading rule) blocks on a bounded queue until the
    consumer drains it.

    Page-range validation happens before the first item is produced, so a
    consumer that awaits the first item before opening a streaming HTTP
    response still gets a clean ``ValueError`` for bad input.

    Cancellation-safe: closing the generator (client disconnect) sets a stop
    flag; the render thread notices on its next queue hand-off and exits.
    """
    pymupdf = load_pymupdf()
    q: _queue.Queue[PdfPageRender | Exception | None] = _queue.Queue(
        maxsize=max(1, max_buffered)
    )
    stop = threading.Event()

    def _put(item: PdfPageRender | Exception | None) -> bool:
        """Blocking hand-off with stop-awareness (the memory back-pressure)."""
        while not stop.is_set():
            try:
                q.put(item, timeout=0.25)
                return True
            except _queue.Full:
                continue
        return False

    def _worker() -> None:
        try:
            with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
                if pages is None:
                    page_iter = list(range(1, doc.page_count + 1))
                else:
                    page_iter = list(pages)
                    for p in page_iter:
                        if p < 1 or p > doc.page_count:
                            raise ValueError(
                                f"page {p} is outside document range 1..{doc.page_count}"
                            )
                for page_no in page_iter:
                    if stop.is_set():
                        return
                    pdf_page = doc[page_no - 1]
                    pix = _pixmap_for_page(
                        pdf_page, pymupdf, dpi, colorspace, alpha, None, annotations
                    )
                    content = _pixmap_to_bytes(pix, fmt, jpeg_quality)
                    rendered = PdfPageRender(
                        page_number=page_no,
                        width=pix.width,
                        height=pix.height,
                        format=fmt.lower(),
                        dpi=dpi,
                        content=content,
                        colorspace=colorspace,
                    )
                    if not _put(rendered):
                        return
            _put(None)
        except Exception as exc:  # noqa: BLE001 — transported to the consumer, re-raised there
            _put(exc)

    loop = asyncio.get_running_loop()
    worker_future = loop.run_in_executor(get_cpu_executor(), _worker)
    try:
        while True:
            try:
                item = q.get_nowait()
            except _queue.Empty:
                if worker_future.done() and q.empty():
                    # Worker died without a sentinel (should be impossible —
                    # surface its exception rather than hanging).
                    worker_future.result()
                    return
                await asyncio.sleep(0.02)
                continue
            if item is None:
                return
            if isinstance(item, Exception):
                raise item
            yield item
    finally:
        stop.set()


def render_thumbnail_bytes(
    pdf_bytes: bytes,
    page: int = 1,
    max_side: int = 256,
    fmt: RenderFormat = "jpeg",
    jpeg_quality: int = 80,
) -> PdfPageRender:
    """Render a thumbnail of a PDF page at *max_side* longest dimension.

    Consumed by ``matrx_files.cloud_sync.processing.thumbnails``.
    Default 256-px / JPEG q=80 matches the existing thumbnail contract.
    """
    if page < 1:
        raise ValueError("page must be >= 1 (1-based).")
    if max_side < 8:
        raise ValueError("max_side must be >= 8.")

    pymupdf = load_pymupdf()
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        if page > doc.page_count:
            raise ValueError(
                f"page {page} is outside document range 1..{doc.page_count}"
            )
        pdf_page = doc[page - 1]
        rect = pdf_page.rect
        # Pick a DPI that yields just-over-max_side on the long edge so the
        # Pillow downscale is a single cheap pass.
        long_pt = max(rect.width, rect.height)
        # 72 DPI is 1 pt per pixel; we want max_side*1.1 pixels.
        target_pixels = max_side * 1.1
        # Floor at 8 DPI so tiny `max_side` requests don't escalate to a
        # heavy render. The Pillow thumbnail step handles the final crop.
        dpi = max(8, int(72 * target_pixels / max(long_pt, 1)))
        pix = pdf_page.get_pixmap(dpi=dpi, alpha=False)
        img = Image.frombytes(
            "RGB", (pix.width, pix.height), pix.samples
        )
        img.thumbnail((max_side, max_side), Image.LANCZOS)
        buf = BytesIO()
        fmt_l = fmt.lower()
        if fmt_l in {"jpg", "jpeg"}:
            img.save(buf, format="JPEG", quality=jpeg_quality, optimize=True)
            out_fmt = "jpeg"
        elif fmt_l == "webp":
            img.save(buf, format="WEBP", quality=jpeg_quality, method=6)
            out_fmt = "webp"
        else:
            img.save(buf, format="PNG", optimize=True)
            out_fmt = "png"
        return PdfPageRender(
            page_number=page,
            width=img.width,
            height=img.height,
            format=out_fmt,
            dpi=dpi,
            content=buf.getvalue(),
            colorspace="rgb",
        )


async def render_thumbnail_bytes_async(
    pdf_bytes: bytes,
    page: int = 1,
    max_side: int = 256,
    fmt: RenderFormat = "jpeg",
    jpeg_quality: int = 80,
) -> PdfPageRender:
    return await run_in_cpu_executor(
        render_thumbnail_bytes, pdf_bytes, page, max_side, fmt, jpeg_quality
    )


__all__ = [
    "PdfPageRender",
    "RenderFormat",
    "RenderColorspace",
    "render_page_to_image_bytes",
    "render_page_to_image_bytes_async",
    "render_all_pages_to_image_bytes",
    "render_all_pages_to_image_bytes_async",
    "render_thumbnail_bytes",
    "render_thumbnail_bytes_async",
]

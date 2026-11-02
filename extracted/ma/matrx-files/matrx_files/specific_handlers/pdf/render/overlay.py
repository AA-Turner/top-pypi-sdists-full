"""Render a PDF page to PNG with overlay rectangles painted in.

Used for:
  - Thumbnail strips in the studio (show which pages have detected hits).
  - "What would this page look like masked?" previews before committing
    a redaction.
  - Sharing annotated views in non-interactive contexts (chat, docs).

Each overlay is `{bbox, color, label?, fill?, stroke_width?, font_size?}`.
Coordinates are PDF user-space points; the renderer converts to pixels via
the requested DPI.
"""

from __future__ import annotations

import base64
import io
from typing import Any

from pydantic import BaseModel, Field

from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf


class OverlayBbox(BaseModel):
    x0: float
    y0: float
    x1: float
    y1: float


class OverlaySpec(BaseModel):
    bbox: OverlayBbox
    color: str = "#ef4444"
    """Hex color (#rrggbb) for the rectangle stroke."""
    fill: str | None = None
    """Optional translucent fill color. Default: none."""
    fill_opacity: float = 0.18
    """0..1 — applied when fill is set."""
    stroke_width: float = 2.0
    label: str | None = None
    """Optional small text label drawn at the top-left of the rect."""
    font_size: float = 10.0


class RenderedPage(BaseModel):
    page_number: int = Field(ge=1)
    page_width: float
    page_height: float
    dpi: int
    image_format: str = "png"
    image_base64: str
    width_px: int
    height_px: int


def _parse_hex(color: str) -> tuple[float, float, float]:
    s = color.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        return (1.0, 0.27, 0.27)  # default red on parse failure
    try:
        r = int(s[0:2], 16) / 255.0
        g = int(s[2:4], 16) / 255.0
        b = int(s[4:6], 16) / 255.0
        return (r, g, b)
    except ValueError:
        return (1.0, 0.27, 0.27)


def render_page_with_overlay(
    pdf_bytes: bytes,
    *,
    page_number: int,
    overlays: list[OverlaySpec | dict[str, Any]] | None = None,
    dpi: int = 144,
    return_format: str = "png",
) -> RenderedPage:
    """Render a single page to PNG with overlays painted in.

    The overlays are drawn ONTO a temporary copy of the page — the input PDF
    bytes are never mutated. We use PyMuPDF's drawing primitives so the
    overlay rects sit at exactly the right PDF-points coordinates, then
    rasterize the result.
    """
    overlays = [
        o if isinstance(o, OverlaySpec) else OverlaySpec(**o)
        for o in (overlays or [])
    ]

    pymupdf = load_pymupdf()
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        if page_number < 1 or page_number > doc.page_count:
            raise ValueError(
                f"page_number {page_number} out of range (doc has {doc.page_count} pages)"
            )
        page = doc[page_number - 1]
        rect = page.rect

        # Paint overlays in PDF-points space — PyMuPDF then rasterizes at DPI.
        for o in overlays:
            color = _parse_hex(o.color)
            box = pymupdf.Rect(
                max(0.0, min(o.bbox.x0, float(rect.width))),
                max(0.0, min(o.bbox.y0, float(rect.height))),
                max(0.0, min(o.bbox.x1, float(rect.width))),
                max(0.0, min(o.bbox.y1, float(rect.height))),
            )
            if o.fill:
                fill = _parse_hex(o.fill)
                page.draw_rect(
                    box,
                    color=color,
                    fill=fill,
                    fill_opacity=max(0.0, min(1.0, o.fill_opacity)),
                    width=o.stroke_width,
                    overlay=True,
                )
            else:
                page.draw_rect(
                    box,
                    color=color,
                    width=o.stroke_width,
                    overlay=True,
                )
            if o.label:
                # Position the label just above the rect; clamp to page top.
                lx = box.x0
                ly = max(2.0, box.y0 - 2.0)
                try:
                    page.insert_text(
                        (lx, ly),
                        o.label,
                        fontsize=o.font_size,
                        color=color,
                        overlay=True,
                    )
                except Exception:
                    pass

        pix = page.get_pixmap(dpi=dpi, alpha=False)
        png = bytes(pix.tobytes(return_format))
        return RenderedPage(
            page_number=page_number,
            page_width=float(rect.width),
            page_height=float(rect.height),
            dpi=dpi,
            image_format=return_format,
            image_base64=base64.b64encode(png).decode("ascii"),
            width_px=int(pix.width),
            height_px=int(pix.height),
        )


async def render_page_with_overlay_async(
    pdf_bytes: bytes,
    *,
    page_number: int,
    overlays: list[OverlaySpec | dict[str, Any]] | None = None,
    dpi: int = 144,
    return_format: str = "png",
) -> RenderedPage:
    return await run_in_cpu_executor(
        lambda: render_page_with_overlay(
            pdf_bytes,
            page_number=page_number,
            overlays=overlays,
            dpi=dpi,
            return_format=return_format,
        )
    )


__all__ = [
    "OverlayBbox",
    "OverlaySpec",
    "RenderedPage",
    "render_page_with_overlay",
    "render_page_with_overlay_async",
]

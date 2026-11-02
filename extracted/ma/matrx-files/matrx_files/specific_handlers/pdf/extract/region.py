"""Manual region extraction — user drew a box, get the typed content.

Three extraction kinds:
  - 'text'  → same as extract_at_bbox but returns just the text + source.
  - 'table' → re-runs the structured-table extractor clipped to the bbox.
              Forces table detection on a region the automatic detector
              might have missed (or got wrong).
  - 'image' → returns the cropped page region as PNG bytes (base64).

Promotes user override over automatic detection — when the auto tables
detector returned nothing for this region, but the user knows there IS a
table there, the user wins.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf
from .bbox import BboxRect, extract_at_bbox
from .tables import extract_tables_structured


class RegionExtractionResult(BaseModel):
    page_number: int = Field(ge=1)
    bbox: BboxRect
    extraction_kind: str  # "text" | "table" | "image"
    text: str | None = None
    text_source: str | None = None
    tables: list[dict[str, Any]] = Field(default_factory=list)
    image_png_base64: str | None = None
    image_format: str | None = None
    notes: list[str] = Field(default_factory=list)


def extract_region(
    pdf_bytes: bytes,
    *,
    page_number: int,
    bbox: dict[str, float] | BboxRect,
    extraction_kind: str = "text",
) -> RegionExtractionResult:
    """Dispatch to the right extractor based on kind."""
    if isinstance(bbox, BboxRect):
        bdict = bbox.model_dump()
    else:
        bdict = {k: float(v) for k, v in bbox.items()}
    notes: list[str] = []

    if extraction_kind == "text":
        res = extract_at_bbox(
            pdf_bytes, page_number=page_number, bbox=bdict, include_preview=False,
        )
        return RegionExtractionResult(
            page_number=page_number,
            bbox=BboxRect(**bdict),
            extraction_kind="text",
            text=res.extracted_text,
            text_source=res.text_source,
            notes=list(res.notes),
        )

    if extraction_kind == "image":
        import base64
        pymupdf = load_pymupdf()
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
            if page_number < 1 or page_number > doc.page_count:
                raise ValueError(f"page_number {page_number} out of range")
            page = doc[page_number - 1]
            clip = pymupdf.Rect(bdict["x0"], bdict["y0"], bdict["x1"], bdict["y1"])
            pix = page.get_pixmap(clip=clip, dpi=200, alpha=False)
            png = bytes(pix.tobytes("png"))
            return RegionExtractionResult(
                page_number=page_number,
                bbox=BboxRect(**bdict),
                extraction_kind="image",
                image_png_base64=base64.b64encode(png).decode("ascii"),
                image_format="png",
                notes=notes,
            )

    if extraction_kind == "table":
        # Clipped table extraction: run the structured extractor on the page,
        # then filter results to those whose bbox overlaps the user's region.
        report = extract_tables_structured(pdf_bytes=pdf_bytes, pages=[page_number])
        x0, y0, x1, y1 = bdict["x0"], bdict["y0"], bdict["x1"], bdict["y1"]
        matches: list[dict[str, Any]] = []
        for t in report.tables:
            if t.page_number != page_number:
                continue
            tb = t.bbox
            # Reject zero-overlap.
            if tb.x1 <= x0 or tb.x0 >= x1 or tb.y1 <= y0 or tb.y0 >= y1:
                continue
            matches.append(t.model_dump())
        if not matches:
            notes.append(
                "no tables detected in the requested region — try widening "
                "the box or extracting as text."
            )
        return RegionExtractionResult(
            page_number=page_number,
            bbox=BboxRect(**bdict),
            extraction_kind="table",
            tables=matches,
            notes=notes,
        )

    raise ValueError(f"unknown extraction_kind: {extraction_kind!r}")


async def extract_region_async(
    pdf_bytes: bytes,
    *,
    page_number: int,
    bbox: dict[str, float] | BboxRect,
    extraction_kind: str = "text",
) -> RegionExtractionResult:
    return await run_in_cpu_executor(
        lambda: extract_region(
            pdf_bytes,
            page_number=page_number,
            bbox=bbox,
            extraction_kind=extraction_kind,
        )
    )


__all__ = ["RegionExtractionResult", "extract_region", "extract_region_async"]

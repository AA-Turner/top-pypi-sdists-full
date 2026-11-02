"""Embedded-image detector — enumerate XObject images on every page.

Returns per-image bbox + format + dimensions + xref. Does NOT extract the
bytes by default (that's another step) — but the xref lets a future endpoint
do so on demand.
"""

from __future__ import annotations

import time
from typing import Any

from ....analysis import (
    Detector,
    DetectorResult,
    DetectorSpec,
    PipelineContext,
    register_detector,
)
from ..internal import load_pymupdf

DETECTOR_KIND = "embedded_images"
DETECTOR_VERSION = "v1"


def _open_doc(ctx: PipelineContext):
    doc = ctx.cache.get("pymupdf_doc")
    if doc is not None:
        return doc
    pymupdf = load_pymupdf()
    doc = pymupdf.open(stream=ctx.bytes_in_memory, filetype="pdf")
    ctx.cache["pymupdf_doc"] = doc
    return doc


class EmbeddedImagesDetector(Detector):
    kind = DETECTOR_KIND
    version = DETECTOR_VERSION
    cost_class = "medium"

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # CPU-bound PyMuPDF image enumeration — runs off-loop via base run().
        started = time.monotonic()
        doc = _open_doc(ctx)
        images: list[dict[str, Any]] = []
        for i in range(doc.page_count):
            page = doc[i]
            try:
                img_list = page.get_images(full=True)
            except Exception:
                continue
            for img in img_list:
                xref = int(img[0])
                smask = int(img[1]) if len(img) > 1 else 0
                width = int(img[2]) if len(img) > 2 else 0
                height = int(img[3]) if len(img) > 3 else 0
                bpc = int(img[4]) if len(img) > 4 else 0
                colorspace = str(img[5]) if len(img) > 5 else ""
                img_filter = str(img[8]) if len(img) > 8 else ""
                # Find bbox of every placement of this image on the page.
                try:
                    rects = page.get_image_rects(xref) or []
                except Exception:
                    rects = []
                placements = [
                    {"x0": float(r.x0), "y0": float(r.y0), "x1": float(r.x1), "y1": float(r.y1)}
                    for r in rects
                ]
                images.append(
                    {
                        "page_number": i + 1,
                        "xref": xref,
                        "smask": smask,
                        "width": width,
                        "height": height,
                        "bpc": bpc,
                        "colorspace": colorspace,
                        "filter": img_filter,
                        "placements": placements,
                    }
                )

        summary = {
            "images_count": len(images),
            "pages_with_images": sorted({im["page_number"] for im in images}),
        }
        return DetectorResult(
            kind=DETECTOR_KIND,
            confidence_tier="n/a",
            detector_version=DETECTOR_VERSION,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            summary=summary,
            payload={"images": images},
        )


def _factory(spec: DetectorSpec) -> Detector:
    return EmbeddedImagesDetector()


register_detector(DETECTOR_KIND, _factory)


__all__ = ["DETECTOR_KIND", "DETECTOR_VERSION", "EmbeddedImagesDetector"]

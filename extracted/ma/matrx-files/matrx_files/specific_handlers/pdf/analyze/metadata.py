"""PDF metadata detector — info dict + page dimensions + encryption flag.

Cheapest detector — opens the PyMuPDF Document, reads .metadata, page.rect for
each page. Caches the opened Document into PipelineContext for downstream
detectors so we never re-open.
"""

from __future__ import annotations

import time
from typing import Any

from pydantic import BaseModel

from ....analysis import (
    Detector,
    DetectorResult,
    DetectorSpec,
    PipelineContext,
    register_detector,
)
from ..internal import load_pymupdf

DETECTOR_KIND = "metadata"
DETECTOR_VERSION = "v1"


class PdfPageDimensions(BaseModel):
    page_number: int
    width: float
    height: float
    rotation: int


class PdfFileMetadata(BaseModel):
    page_count: int
    is_encrypted: bool
    is_pdf: bool
    needs_pass: bool
    info: dict[str, Any]
    pages: list[PdfPageDimensions]


def extract_pdf_metadata(pdf_bytes: bytes) -> PdfFileMetadata:
    pymupdf = load_pymupdf()
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        info = dict(doc.metadata or {})
        pages = []
        for i in range(doc.page_count):
            page = doc[i]
            rect = page.rect
            pages.append(
                PdfPageDimensions(
                    page_number=i + 1,
                    width=float(rect.width),
                    height=float(rect.height),
                    rotation=int(page.rotation),
                )
            )
        return PdfFileMetadata(
            page_count=doc.page_count,
            is_encrypted=bool(doc.is_encrypted),
            is_pdf=bool(doc.is_pdf),
            needs_pass=bool(doc.needs_pass),
            info=info,
            pages=pages,
        )


class MetadataDetector(Detector):
    kind = DETECTOR_KIND
    version = DETECTOR_VERSION
    cost_class = "fast"

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # CPU-bound PyMuPDF open + per-page rect read — runs off-loop via the
        # base Detector.run. Opens the shared Document once and caches it; the
        # dispatcher runs detectors sequentially so the cached Document is only
        # ever touched by one detector thread at a time.
        started = time.monotonic()
        # Open PyMuPDF doc once and cache for everyone downstream.
        pymupdf = load_pymupdf()
        doc = ctx.cache.get("pymupdf_doc")
        opened_here = False
        if doc is None:
            doc = pymupdf.open(stream=ctx.bytes_in_memory, filetype="pdf")
            ctx.cache["pymupdf_doc"] = doc
            ctx.cache["pymupdf_close_owner"] = True
            opened_here = True

        info = dict(doc.metadata or {})
        page_dims = []
        for i in range(doc.page_count):
            page = doc[i]
            rect = page.rect
            page_dims.append(
                {
                    "page_number": i + 1,
                    "width": float(rect.width),
                    "height": float(rect.height),
                    "rotation": int(page.rotation),
                }
            )

        meta = {
            "page_count": doc.page_count,
            "is_encrypted": bool(doc.is_encrypted),
            "is_pdf": bool(doc.is_pdf),
            "needs_pass": bool(doc.needs_pass),
            "info": info,
            "pages": page_dims,
        }
        ctx.cache["page_count"] = doc.page_count
        ctx.cache["file_metadata_snapshot"] = {"pdf": {"info": info, "page_count": doc.page_count}}

        summary = {
            "page_count": doc.page_count,
            "is_encrypted": bool(doc.is_encrypted),
            "title": info.get("title") or None,
            "author": info.get("author") or None,
            "producer": info.get("producer") or None,
        }
        return DetectorResult(
            kind=DETECTOR_KIND,
            confidence_tier="n/a",
            detector_version=DETECTOR_VERSION,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            summary=summary,
            payload=meta,
        )


def _factory(spec: DetectorSpec) -> Detector:
    return MetadataDetector()


register_detector(DETECTOR_KIND, _factory)


__all__ = [
    "DETECTOR_KIND",
    "DETECTOR_VERSION",
    "extract_pdf_metadata",
    "PdfFileMetadata",
    "PdfPageDimensions",
    "MetadataDetector",
]

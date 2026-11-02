"""Wrap the existing classify_pages() into a Detector.

Also rolls up a doc-level classification hint into PipelineContext.cache for
the dispatcher to stamp on the final file_analysis row.
"""

from __future__ import annotations

import time
from collections import Counter

from ....analysis import (
    Detector,
    DetectorResult,
    DetectorSpec,
    PipelineContext,
    register_detector,
)
from .layout import classify_pages

DETECTOR_KIND = "page_classification"
DETECTOR_VERSION = "v1"


class PageClassificationDetector(Detector):
    kind = DETECTOR_KIND
    version = DETECTOR_VERSION
    cost_class = "fast"

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # CPU-bound (PyMuPDF page parsing). Runs off the event loop via the
        # base Detector.run → asyncio.to_thread. On 2026-06-04 this body ran
        # ON the loop and froze the whole server for 82s.
        started = time.monotonic()
        report = classify_pages(ctx.bytes_in_memory)
        counts = Counter(p.page_class for p in report.pages)
        # Doc-level guess: the most common non-blank class
        non_blank = [p for p in report.pages if p.page_class not in ("blank",)]
        doc_guess = non_blank[0].page_class if non_blank else "blank"
        ctx.cache["doc_classification"] = {
            "primary_class": doc_guess,
            "page_class_counts": dict(counts),
        }
        summary = {
            "page_count": report.page_count,
            "class_counts": dict(counts),
            "primary": doc_guess,
        }
        return DetectorResult(
            kind=DETECTOR_KIND,
            confidence_tier="n/a",
            detector_version=DETECTOR_VERSION,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            summary=summary,
            payload=report.model_dump(),
        )


def _factory(spec: DetectorSpec) -> Detector:
    return PageClassificationDetector()


register_detector(DETECTOR_KIND, _factory)


__all__ = ["DETECTOR_KIND", "DETECTOR_VERSION", "PageClassificationDetector"]

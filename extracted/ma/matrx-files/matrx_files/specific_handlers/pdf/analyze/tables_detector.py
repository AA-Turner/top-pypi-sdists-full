"""Wraps extract_tables_structured() as a Detector."""

from __future__ import annotations

import time

from ....analysis import (
    Detector,
    DetectorResult,
    DetectorSpec,
    PipelineContext,
    register_detector,
)
from ..extract.tables import extract_tables_structured

DETECTOR_KIND = "tables"
DETECTOR_VERSION = "v1"


class TablesDetector(Detector):
    kind = DETECTOR_KIND
    version = DETECTOR_VERSION
    cost_class = "fast"

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # CPU-bound PyMuPDF table extraction — runs off-loop via base run().
        started = time.monotonic()
        report = extract_tables_structured(pdf_bytes=ctx.bytes_in_memory)
        summary = {
            "tables_count": len(report.tables),
            "page_count": report.page_count,
            "pages_with_tables": sorted({t.page_number for t in report.tables}),
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
    return TablesDetector()


register_detector(DETECTOR_KIND, _factory)


__all__ = ["DETECTOR_KIND", "DETECTOR_VERSION", "TablesDetector"]

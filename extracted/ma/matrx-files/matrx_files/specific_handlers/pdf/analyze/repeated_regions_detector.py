"""Wraps detect_repeated_regions() as a tiered Detector.

Tiers map to the strict/balanced/loose ratio + confidence presets.
"""

from __future__ import annotations

import time

from ....analysis import (
    Detector,
    DetectorResult,
    DetectorSpec,
    PipelineContext,
    register_detector,
)
from .repeated_regions import detect_repeated_regions

DETECTOR_KIND = "repeated_regions"
DETECTOR_VERSION = "v1"


_TIER_PARAMS = {
    "high": {"min_pages_ratio": 0.5, "min_confidence": 0.7},
    "medium": {"min_pages_ratio": 1 / 3, "min_confidence": 0.5},
    "low": {"min_pages_ratio": 0.2, "min_confidence": 0.4},
}


class RepeatedRegionsDetector(Detector):
    kind = DETECTOR_KIND
    version = DETECTOR_VERSION
    cost_class = "fast"

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # CPU-bound (PyMuPDF block gather) — runs off-loop via base run().
        started = time.monotonic()
        params = _TIER_PARAMS.get(tier, _TIER_PARAMS["medium"])
        report = detect_repeated_regions(ctx.bytes_in_memory, **params)
        summary = {
            "regions_count": len(report.regions),
            "page_count": report.page_count,
            "tier_params": params,
        }
        return DetectorResult(
            kind=DETECTOR_KIND,
            confidence_tier=tier,
            detector_version=DETECTOR_VERSION,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            summary=summary,
            payload=report.model_dump(),
        )


def _factory(spec: DetectorSpec) -> Detector:
    return RepeatedRegionsDetector()


register_detector(DETECTOR_KIND, _factory)


__all__ = ["DETECTOR_KIND", "DETECTOR_VERSION", "RepeatedRegionsDetector"]

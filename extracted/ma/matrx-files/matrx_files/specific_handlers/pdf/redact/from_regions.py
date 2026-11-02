"""Bridge the Phase 3 ``RepeatedRegion`` detector to the redaction engine.

Lets a caller go from "detect headers/footers" → "redact the accepted
regions across every page they cover" in one call:

    report = detect_repeated_regions(pdf_bytes)
    result = redact_repeated_regions(
        pdf_bytes,
        report.regions,
        accepted_region_ids={report.regions[0].region_id},
        reason="Strip running header for FOIA release",
    )
"""

from __future__ import annotations

from typing import Iterable

from ..analyze.models import RepeatedRegion
from .engine import redact_regions, redact_regions_async
from .models import RedactionRegion, RedactionResult


def _regions_for_redact(
    regions: Iterable[RepeatedRegion],
    accepted_region_ids: set[str] | None,
) -> list[RedactionRegion]:
    accepted = (
        accepted_region_ids
        if accepted_region_ids is not None
        else {r.region_id for r in regions}
    )
    targets: list[RedactionRegion] = []
    for region in regions:
        if region.region_id not in accepted:
            continue
        for bbox in region.bbox_per_page:
            targets.append(
                RedactionRegion(
                    page_number=bbox.page_number,
                    x0=bbox.x0,
                    y0=bbox.y0,
                    x1=bbox.x1,
                    y1=bbox.y1,
                    replacement="REMOVE",
                )
            )
    return targets


def redact_repeated_regions(
    pdf_bytes: bytes,
    regions: list[RepeatedRegion],
    *,
    accepted_region_ids: set[str] | None = None,
    reason: str,
    user_id: str | None = None,
    parent_file_id: str | None = None,
    scrub_metadata: bool = True,
) -> RedactionResult:
    """Redact every accepted region's per-page bbox in one pass.

    *accepted_region_ids* — when None, every region in *regions* is redacted.
    Pass a subset (e.g. only header + footer ids) to redact selectively.
    """
    targets = _regions_for_redact(regions, accepted_region_ids)
    return redact_regions(
        pdf_bytes,
        targets,
        reason=reason,
        user_id=user_id,
        parent_file_id=parent_file_id,
        scrub_metadata=scrub_metadata,
    )


async def redact_repeated_regions_async(
    pdf_bytes: bytes,
    regions: list[RepeatedRegion],
    *,
    accepted_region_ids: set[str] | None = None,
    reason: str,
    user_id: str | None = None,
    parent_file_id: str | None = None,
    scrub_metadata: bool = True,
) -> RedactionResult:
    targets = _regions_for_redact(regions, accepted_region_ids)
    return await redact_regions_async(
        pdf_bytes,
        targets,
        reason=reason,
        user_id=user_id,
        parent_file_id=parent_file_id,
        scrub_metadata=scrub_metadata,
    )


__all__ = [
    "redact_repeated_regions",
    "redact_repeated_regions_async",
]

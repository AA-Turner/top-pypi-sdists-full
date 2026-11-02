"""Page outline / TOC detector — extracts the PDF bookmark tree.

PyMuPDF's `doc.get_toc(simple=False)` returns the nested outline as
`[[level, title, page, dest_dict], ...]`. We convert to a flat list with
explicit parent pointers and zero-based page indices that the dispatcher
can pair with file_pages.page_id lookups downstream.

Doc-level result; emits one DetectorResult covering the entire document.
Surfaces navigation jumps in the studio sidebar.
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

DETECTOR_KIND = "page_outline"
DETECTOR_VERSION = "v1"


def _open_doc(ctx: PipelineContext):
    doc = ctx.cache.get("pymupdf_doc")
    if doc is not None:
        return doc
    pymupdf = load_pymupdf()
    doc = pymupdf.open(stream=ctx.bytes_in_memory, filetype="pdf")
    ctx.cache["pymupdf_doc"] = doc
    return doc


class PageOutlineDetector(Detector):
    kind = DETECTOR_KIND
    version = DETECTOR_VERSION
    cost_class = "fast"

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # CPU-bound PyMuPDF TOC parse — runs off-loop via base Detector.run.
        started = time.monotonic()
        doc = _open_doc(ctx)
        try:
            raw = doc.get_toc(simple=False) or []
        except Exception:
            raw = []

        page_id_by_index: dict[int, str] = ctx.cache.get("page_id_by_index") or {}

        # Convert PyMuPDF's nested list-of-lists into a flat outline entries
        # list with parent indices preserved. PyMuPDF's pages are 1-based.
        entries: list[dict[str, Any]] = []
        # Track the most recent entry at each depth so we can set parent_index.
        depth_to_index: dict[int, int] = {}

        for item in raw:
            if not isinstance(item, list) or len(item) < 3:
                continue
            level = int(item[0]) if isinstance(item[0], int) else 1
            title = str(item[1]) if item[1] is not None else ""
            page_1based = int(item[2]) if isinstance(item[2], int) else 1
            dest = item[3] if len(item) > 3 and isinstance(item[3], dict) else {}
            page_index_0 = max(0, page_1based - 1)
            parent_idx = depth_to_index.get(level - 1)
            entry_idx = len(entries)
            entries.append(
                {
                    "index": entry_idx,
                    "level": level,
                    "title": title.strip(),
                    "page_number": page_1based,
                    "page_id": page_id_by_index.get(page_index_0),
                    "parent_index": parent_idx,
                    "dest": dest,
                }
            )
            # Clear deeper levels — they're no longer reachable as parents.
            for d in list(depth_to_index.keys()):
                if d >= level:
                    depth_to_index.pop(d)
            depth_to_index[level] = entry_idx

        summary = {
            "outline_count": len(entries),
            "max_depth": max((e["level"] for e in entries), default=0),
            "has_outline": bool(entries),
        }
        return DetectorResult(
            kind=DETECTOR_KIND,
            confidence_tier="n/a",
            detector_version=DETECTOR_VERSION,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            summary=summary,
            payload={"entries": entries},
        )


def _factory(spec: DetectorSpec) -> Detector:
    return PageOutlineDetector()


register_detector(DETECTOR_KIND, _factory)


__all__ = ["DETECTOR_KIND", "DETECTOR_VERSION", "PageOutlineDetector"]

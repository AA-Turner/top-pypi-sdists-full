"""Core protocol + Pydantic models for the file-analysis platform.

Every detector implements ``Detector`` and produces a ``DetectorResult``.
The dispatcher is the only thing that knows the registry; detectors are
black boxes that consume a ``PipelineContext`` and emit a result.

This module is file-type-agnostic. PDF-specific detectors live in
``matrx_files.specific_handlers.pdf.analyze.*``. Image,
audio, etc. detectors will live in their own sibling subpackages.
"""

from __future__ import annotations

import asyncio
from abc import ABC
from collections.abc import Awaitable, Callable
from typing import Any, Literal, Protocol

from pydantic import BaseModel, Field

CostClass = Literal["fast", "medium", "slow"]
ConfidenceTier = Literal["n/a", "low", "medium", "high"]
TextSource = Literal["native", "ocr", "mixed"]
DetectorStatus = Literal["success", "skipped", "failed"]


class PageInfo(BaseModel):
    """Per-page snapshot the dispatcher upserts before running detectors.

    Carries the immutable + initial-mutable facts about a page — enough for the
    aidream persistence impl to upsert a `file_pages` row.
    """

    source_page_index: int = Field(ge=0)
    """Immutable 0-based original position at upload time."""
    page_index: int = Field(ge=0)
    """Current 0-based position. Equals source_page_index initially; mutates on reorder."""
    width_pt: float
    height_pt: float
    rotation: int = 0
    text_source: str = "unknown"
    """'native' | 'ocr' | 'mixed' | 'unknown' | 'none'."""
    ocr_confidence: float | None = None


class DetectorResult(BaseModel):
    """The wire contract every detector produces."""

    kind: str
    confidence_tier: str = "n/a"
    detector_version: str
    status: DetectorStatus = "success"
    elapsed_ms: int = 0
    summary: dict[str, Any] = Field(default_factory=dict)
    """ALWAYS small — feeds file-list and tab-header views without inflating reads."""
    payload: dict[str, Any] = Field(default_factory=dict)
    """Full output. May overflow to extended storage when serialized size exceeds
    ``INLINE_PAYLOAD_LIMIT`` — see persistence.py."""
    page_numbers: list[int] | None = None
    """1-based pages this result covers. None = doc-level."""
    page_id: str | None = None
    """Stable page id (from file_pages) for per-page results. None for doc-level.
    The dispatcher resolves this from page_numbers via the host-injected
    page-id lookup before persisting."""
    text_sources: list[TextSource] = Field(default_factory=list)
    """Which text sources this result reflects. Used by the OCR router to know
    when to re-emit text-dependent detectors after OCR results land."""
    error: str | None = None


class DetectorSpec(BaseModel):
    """Registry entry — declarative metadata only. Instantiation is via factory."""

    kind: str
    cost_class: CostClass = "fast"
    tiers: tuple[str, ...] = ("n/a",)
    depends_on: tuple[str, ...] = ()
    params: dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: float = 120.0
    requires_text: bool = False
    """When True, the dispatcher re-emits this detector for OCR'd pages after
    ``text_extraction_ocr`` lands new pages."""


class Detector(ABC):
    """Detectors are stateless — instantiated per-pipeline by the dispatcher.

    EVENT-LOOP SAFETY CONTRACT (read before adding a detector):

    Detector work is almost always CPU-bound — PyMuPDF page parsing, pixmap
    rendering, hashing, regex sweeps. If that work runs directly on the
    asyncio event loop it BLOCKS the entire single-process server: no other
    request is served, no DB connection can be acquired, heartbeats stop. On
    2026-06-04 a single ``page_classification`` run held the loop for 82s and
    took the whole production server down (acquires timed out even though the
    pool had idle connections — the loop itself was frozen).

    The platform makes that class of failure structurally impossible:

    - **Default path (preferred):** implement the synchronous ``analyze()``.
      The base ``run()`` offloads it to a worker thread via ``asyncio.to_thread``
      so the loop stays free no matter how slow the file is. ``analyze()`` runs
      OFF the loop — it MUST NOT touch event-loop-bound resources (no awaiting,
      no asyncpg, no httpx client created on the main loop). Open your own
      PyMuPDF ``Document`` from ``ctx.bytes_in_memory`` inside ``analyze()`` and
      close it before returning — never share a Document across detectors
      (PyMuPDF Documents are not thread-safe).

    - **Async path (only when you genuinely await):** override ``run()``
      directly. Keep the CPU sections (PyMuPDF parsing, rendering, OCR image
      prep) inside ``asyncio.to_thread`` / ``run_in_cpu_executor`` and do ONLY
      the real ``await`` (injected async provider / persistence) on the loop.

    The dispatcher runs detectors sequentially within a cost-class bucket, so
    ``ctx.cache`` access from the offloaded thread is race-free.
    """

    kind: str = ""
    version: str = "v1"
    cost_class: CostClass = "fast"

    async def run(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # Default: run the synchronous body off the event loop. A detector
        # that genuinely needs to await must override this method.
        return await asyncio.to_thread(self.analyze, ctx, tier)

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        """Synchronous detector body — executed off the event loop by run().

        Implement this for CPU-bound detectors (the common case). Detectors
        that override ``run()`` with their own async implementation don't need
        to provide ``analyze()``.
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement analyze() (sync, runs "
            f"off-loop) or override run() (async). See Detector's docstring."
        )


# Forward-declared — defined in context.py. Used for type hints only here.
class PipelineContext(Protocol):
    file_id: str
    owner_id: str
    mime_type: str
    bytes_in_memory: bytes
    settings: Any
    cache: dict[str, Any]
    emit: Callable[[DetectorResult], Awaitable[None]]


DetectorFactory = Callable[[DetectorSpec], Detector]


__all__ = [
    "CostClass",
    "ConfidenceTier",
    "TextSource",
    "DetectorStatus",
    "DetectorResult",
    "DetectorSpec",
    "Detector",
    "DetectorFactory",
    "PageInfo",
    "PipelineContext",
]

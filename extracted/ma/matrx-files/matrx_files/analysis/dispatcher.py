"""The dispatcher — orchestrates detectors in cost-class buckets with DAG deps.

Steps per analyze_file() call:

1. Resolve settings (built-ins → user prefs → recipes).
2. Pick detectors for the mime type, intersected with `only_detectors`.
3. Group by cost_class (fast → medium → slow).
4. Within each bucket: topo-sort by depends_on, then asyncio.gather with a
   semaphore cap. Persist each result IMMEDIATELY on settle.
5. Special-case: when text_extraction_ocr lands new pages, re-emit
   text-dependent detectors scoped to those pages.
6. Finalize: roll up summary, stamp cld_files.metadata.analysis.

Failures in a single detector NEVER fail the pipeline — they get a failed-status
row and the dispatcher continues.
"""

from __future__ import annotations

import asyncio
import time
import traceback
from collections import defaultdict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime

from matrx_utils.fancy_prints import vcprint
from matrx_utils import capture_error

from .context import PipelineContext, ResolvedSettings
from .ocr_router import DEFAULT_OCR_PROVIDER, OcrProviderProtocol
from .persistence import PersistenceProtocol, persist_one_result
from .preferences import PrefsStoreProtocol, resolve_settings
from .protocol import Detector, DetectorResult, DetectorSpec, PageInfo
from .registry import (
    get_factory,
    get_specs_for_mime,
    text_dependent_kinds,
)

ANALYZER_VERSION = "v1.0.0"
DEFAULT_PER_PIPELINE_SEMAPHORE = 8


@dataclass
class AnalysisProgressEvent:
    """Live progress from the detector loop, for host streaming adapters.

    ``phase`` is ``"started"`` (pipeline began; ``total`` runnables known) or
    ``"detector_completed"`` (one (detector, tier) settled — success, skipped,
    or failed). This package cannot import host event models, so hosts map
    this dataclass to their own typed wire events in the callback.
    """

    phase: str  # "started" | "detector_completed"
    file_id: str
    mime_type: str
    total: int
    complete: int = 0
    detector_kind: str | None = None
    tier: str | None = None
    status: str | None = None
    elapsed_ms: int = 0
    error: str | None = None


AnalysisProgressCallback = Callable[[AnalysisProgressEvent], Awaitable[None]]


async def _notify_progress(
    on_progress: AnalysisProgressCallback | None,
    event: AnalysisProgressEvent,
) -> None:
    """Invoke the host progress callback; a callback failure must never fail
    the analysis pipeline (the DB rows are the durable truth — the stream is
    a live view). Failures are logged loudly, not swallowed silently."""
    if on_progress is None:
        return
    try:
        await on_progress(event)
    except Exception as exc:
        vcprint(
            f"[analysis] progress callback failed for file_id={event.file_id} "
            f"phase={event.phase} kind={event.detector_kind}: {exc}",
            color="red",
        )
        await capture_error(
            exc,
            kind="file_analysis_progress_callback_failed",
            context={"file_id": event.file_id, "phase": event.phase},
        )


class AnalysisOutcome:
    def __init__(
        self,
        *,
        file_id: str,
        status: str,
        results_count: int,
        failures: list[str],
        elapsed_ms: int,
    ):
        self.file_id = file_id
        self.status = status
        self.results_count = results_count
        self.failures = failures
        self.elapsed_ms = elapsed_ms

    def __repr__(self) -> str:
        return (
            f"AnalysisOutcome(file_id={self.file_id} status={self.status} "
            f"results={self.results_count} failures={len(self.failures)} "
            f"elapsed={self.elapsed_ms}ms)"
        )


async def analyze_file(
    *,
    file_id: str,
    owner_id: str,
    mime_type: str,
    bytes_in_memory: bytes,
    persistence: PersistenceProtocol,
    prefs_store: PrefsStoreProtocol | None = None,
    ocr_provider: OcrProviderProtocol | None = None,
    only_detectors: list[str] | None = None,
    only_tiers: list[str] | None = None,
    force: bool = False,
    filename: str | None = None,
    classification_hint: str | None = None,
    inline_payload_limit_bytes: int = 256 * 1024,
    per_pipeline_semaphore: int = DEFAULT_PER_PIPELINE_SEMAPHORE,
    on_progress: AnalysisProgressCallback | None = None,
) -> AnalysisOutcome:
    """Top-level entry. Never raises — every failure captured per-detector."""
    started_wall = time.monotonic()
    settings = await resolve_settings(
        user_id=owner_id,
        mime_type=mime_type,
        classification_hint=classification_hint,
        filename=filename,
        inline_payload_limit_bytes=inline_payload_limit_bytes,
        ocr_provider_id=(ocr_provider.provider_id if ocr_provider else "tesseract"),
        store=prefs_store,
    )

    specs = get_specs_for_mime(mime_type)
    if only_detectors:
        wanted = set(only_detectors)
        specs = [s for s in specs if s.kind in wanted]

    if not specs:
        vcprint(
            f"[analysis] file_id={file_id} mime={mime_type} → not_applicable "
            f"(no detectors registered)",
            color="cyan",
        )
        await persistence.upsert_analysis_start(
            file_id=file_id,
            owner_id=owner_id,
            mime_type=mime_type,
            analyzer_version=ANALYZER_VERSION,
            total_detectors=0,
        )
        await persistence.finalize(
            file_id=file_id,
            status="not_applicable",
            summary_counts={},
            classification=None,
            page_count=None,
            text_source_map=None,
            metadata=None,
        )
        await _notify_progress(
            on_progress,
            AnalysisProgressEvent(
                phase="started", file_id=file_id, mime_type=mime_type, total=0
            ),
        )
        return AnalysisOutcome(
            file_id=file_id,
            status="not_applicable",
            results_count=0,
            failures=[],
            elapsed_ms=int((time.monotonic() - started_wall) * 1000),
        )

    # ── expand tiers per spec → list of (spec, tier) runnables ────────────
    runnables: list[tuple[DetectorSpec, str]] = []
    for spec in specs:
        if spec.kind not in settings.enabled_detectors:
            continue
        configured_tiers = settings.detector_tiers.get(spec.kind, spec.tiers)
        for tier in configured_tiers:
            if only_tiers and tier not in only_tiers and tier != "n/a":
                continue
            runnables.append((spec, tier))

    total = len(runnables)
    vcprint(
        f"[analysis] file_id={file_id} mime={mime_type} started detectors={total}",
        color="cyan",
    )
    await persistence.upsert_analysis_start(
        file_id=file_id,
        owner_id=owner_id,
        mime_type=mime_type,
        analyzer_version=ANALYZER_VERSION,
        total_detectors=total,
    )
    await _notify_progress(
        on_progress,
        AnalysisProgressEvent(
            phase="started", file_id=file_id, mime_type=mime_type, total=total
        ),
    )

    # ── pre-step: upsert file_pages so per-page detectors can stamp page_id ───
    page_info = _extract_page_info(mime_type, bytes_in_memory)
    page_id_by_index: dict[int, str] = {}
    if page_info:
        try:
            page_id_by_index = await persistence.upsert_pages(
                file_id=file_id,
                owner_id=owner_id,
                pages=page_info,
            )
        except Exception as exc:
            vcprint(
                f"[analysis] upsert_pages failed for {file_id}: {exc}",
                color="yellow",
            )
            await capture_error(
                exc,
                kind="file_analysis_page_persistence_failed",
                context={"file_id": file_id},
            )

    # ── build context ─────────────────────────────────────────────────────
    completed_counter = {"n": 0}
    failures: list[str] = []
    results_count = 0

    async def emit_progress(current_kind: str | None) -> None:
        await persistence.update_progress(
            file_id=file_id,
            complete=completed_counter["n"],
            total=total,
            current_kind=current_kind,
        )

    async def emit_result(res: DetectorResult) -> None:
        nonlocal results_count
        page_id = res.page_id
        # Resolve page_id from page_numbers when the detector didn't set it
        # but did report a single page covered. Doc-level results stay null.
        if page_id is None and res.page_numbers and len(res.page_numbers) == 1:
            idx0 = res.page_numbers[0] - 1
            page_id = page_id_by_index.get(idx0)
        await persist_one_result(
            persistence,
            file_id=file_id,
            owner_id=owner_id,
            settings=settings,
            detector_kind=res.kind,
            detector_version=res.detector_version,
            confidence_tier=res.confidence_tier,
            status=res.status,
            text_sources=res.text_sources,
            elapsed_ms=res.elapsed_ms,
            summary=res.summary,
            payload=res.payload,
            error=res.error,
            page_id=page_id,
        )
        results_count += 1

    ctx = PipelineContext(
        file_id=file_id,
        owner_id=owner_id,
        mime_type=mime_type,
        bytes_in_memory=bytes_in_memory,
        settings=settings,
        emit=emit_result,
    )
    ctx.cache["ocr_provider"] = ocr_provider or DEFAULT_OCR_PROVIDER
    # Page-anchoring: detectors read this to stamp page_id on per-page results.
    ctx.cache["page_id_by_index"] = page_id_by_index
    ctx.cache["page_info"] = page_info
    # Host-injected protocol — detectors that finalize per-page state
    # (e.g. text_extraction_ocr writes OCR confidence) call this.
    ctx.cache["persistence"] = persistence

    # ── bucket by cost_class, respect depends_on ──────────────────────────
    buckets: dict[str, list[tuple[DetectorSpec, str]]] = defaultdict(list)
    for spec, tier in runnables:
        buckets[spec.cost_class].append((spec, tier))

    semaphore = asyncio.Semaphore(per_pipeline_semaphore)
    completed_kinds: set[str] = set()

    async def run_one(spec: DetectorSpec, tier: str) -> None:
        nonlocal failures
        # The semaphore is retained as a defensive global fan-out cap, but
        # detectors within a bucket are now awaited SEQUENTIALLY (see below).
        # Sequential execution is deliberate, not a perf regression:
        #   1. Detector bodies are CPU-bound and offloaded to a worker thread
        #      (Detector.run → asyncio.to_thread). Real parallelism across them
        #      would race on the shared PyMuPDF Document / ctx.cache. One at a
        #      time keeps both safe without per-detector locking.
        #   2. record_detector_run() merges into the SAME file_analysis row;
        #      serial execution means those UPDATEs never contend on the row
        #      lock (the 2026-06-04 QueryTimeoutError class).
        async with semaphore:
            await _wait_for_deps(spec, completed_kinds, settings)
            started_iso = datetime.now(UTC).isoformat()
            res = await _run_detector(spec, tier, ctx)
            finished_iso = datetime.now(UTC).isoformat()
            await persistence.record_detector_run(
                file_id=file_id,
                kind=spec.kind,
                version=res.detector_version,
                status=res.status,
                started_at_iso=started_iso,
                finished_at_iso=finished_iso,
                error=res.error,
            )
            if res.status == "failed":
                failures.append(f"{spec.kind}[{tier}]: {res.error or 'unknown'}")
            await emit_result(res)
            completed_counter["n"] += 1
            await emit_progress(spec.kind)
            await _notify_progress(
                on_progress,
                AnalysisProgressEvent(
                    phase="detector_completed",
                    file_id=file_id,
                    mime_type=mime_type,
                    total=total,
                    complete=completed_counter["n"],
                    detector_kind=spec.kind,
                    tier=tier,
                    status=res.status,
                    elapsed_ms=res.elapsed_ms,
                    error=res.error,
                ),
            )

    for bucket_name in ("fast", "medium", "slow"):
        bucket = buckets.get(bucket_name) or []
        if not bucket:
            continue
        ordered = _topo_sort(bucket)
        # Sequential within the bucket: one CPU-bound detector thread at a
        # time (shared PyMuPDF Document / ctx.cache safety) and no same-row
        # UPDATE contention on record_detector_run. See run_one's comment.
        for spec, tier in ordered:
            await run_one(spec, tier)
        completed_kinds.update({s.kind for (s, _t) in bucket})

        # ── OCR re-emit hook ──────────────────────────────────────────
        if bucket_name == "slow":
            ocr_pages = ctx.cache.get("ocr_pages_completed") or []
            if ocr_pages:
                text_kinds = text_dependent_kinds() & {s.kind for s in specs}
                re_runs: list[tuple[DetectorSpec, str]] = []
                for spec, tier in runnables:
                    if spec.kind in text_kinds:
                        re_runs.append((spec, tier))
                if re_runs:
                    vcprint(
                        f"[analysis] file_id={file_id} re-emitting "
                        f"{len(re_runs)} text-dependent detectors for OCR'd "
                        f"pages={ocr_pages}",
                        color="cyan",
                    )
                    ctx.cache["restrict_pages"] = set(ocr_pages)
                    for spec, tier in re_runs:
                        await run_one(spec, tier)
                    ctx.cache.pop("restrict_pages", None)

    # ── finalize ──────────────────────────────────────────────────────────
    summary_counts = ctx.cache.get("summary_counts") or {}
    classification = ctx.cache.get("doc_classification")
    page_count = ctx.cache.get("page_count")
    text_source_map = ctx.cache.get("text_source_map")
    file_metadata = ctx.cache.get("file_metadata_snapshot")

    status = "complete" if not failures else "partial"
    await persistence.finalize(
        file_id=file_id,
        status=status,
        summary_counts=summary_counts,
        classification=classification,
        page_count=page_count,
        text_source_map=text_source_map,
        metadata=file_metadata,
    )

    completed_iso = datetime.now(UTC).isoformat()
    await persistence.stamp_cld_files_metadata(
        file_id=file_id,
        analysis_summary={
            "status": status,
            "completed_at": completed_iso,
            "analyzer_version": ANALYZER_VERSION,
            "summary": summary_counts,
        },
    )

    elapsed_ms = int((time.monotonic() - started_wall) * 1000)
    vcprint(
        f"[analysis] file_id={file_id} {status} elapsed={elapsed_ms}ms "
        f"results={results_count} failures={len(failures)}",
        color="cyan",
    )
    return AnalysisOutcome(
        file_id=file_id,
        status=status,
        results_count=results_count,
        failures=failures,
        elapsed_ms=elapsed_ms,
    )


async def _wait_for_deps(
    spec: DetectorSpec,
    completed_kinds: set[str],
    settings: ResolvedSettings,
) -> None:
    """Currently a no-op — buckets enforce ordering. Hook for future cross-bucket deps."""
    return None


def _topo_sort(
    runnables: list[tuple[DetectorSpec, str]],
) -> list[tuple[DetectorSpec, str]]:
    """Stable topo sort of (spec, tier) by depends_on within the bucket."""
    in_bucket = {spec.kind for (spec, _t) in runnables}
    indeg: dict[str, int] = defaultdict(int)
    by_kind: dict[str, list[tuple[DetectorSpec, str]]] = defaultdict(list)
    for spec, tier in runnables:
        by_kind[spec.kind].append((spec, tier))
        for dep in spec.depends_on:
            if dep in in_bucket:
                indeg[spec.kind] += 1
        indeg.setdefault(spec.kind, 0)

    out: list[tuple[DetectorSpec, str]] = []
    ready = [k for k, d in indeg.items() if d == 0]
    while ready:
        ready.sort()  # stable
        k = ready.pop(0)
        out.extend(by_kind[k])
        for spec, _tier in runnables:
            if k in spec.depends_on:
                indeg[spec.kind] -= 1
                if indeg[spec.kind] == 0:
                    ready.append(spec.kind)
    # Anything left has a cycle or unmet dep — append in declared order.
    seen = {id(r) for r in out}
    for r in runnables:
        if id(r) not in seen:
            out.append(r)
    return out


async def _run_detector(
    spec: DetectorSpec,
    tier: str,
    ctx: PipelineContext,
) -> DetectorResult:
    """Instantiate via factory and run. Catches all exceptions into a failed result."""
    factory = get_factory(spec.kind)
    if factory is None:
        return DetectorResult(
            kind=spec.kind,
            confidence_tier=tier,
            detector_version="v0",
            status="failed",
            error=f"no factory registered for kind={spec.kind}",
        )
    started = time.monotonic()
    try:
        detector: Detector = factory(spec)
        res = await asyncio.wait_for(detector.run(ctx, tier), timeout=spec.timeout_seconds)
        if res.elapsed_ms == 0:
            res.elapsed_ms = int((time.monotonic() - started) * 1000)
        if not res.confidence_tier:
            res.confidence_tier = tier
        vcprint(
            f"[analysis.{spec.kind}] file_id={ctx.file_id} tier={tier} "
            f"status={res.status} elapsed={res.elapsed_ms}ms",
            color="cyan",
        )
        return res
    except TimeoutError as exc:
        await capture_error(
            exc,
            kind="file_detector_timed_out",
            context={"file_id": ctx.file_id, "detector_kind": spec.kind, "tier": tier},
        )
        return DetectorResult(
            kind=spec.kind,
            confidence_tier=tier,
            detector_version="v0",
            status="failed",
            elapsed_ms=int((time.monotonic() - started) * 1000),
            error=f"timeout after {spec.timeout_seconds}s",
        )
    except Exception as exc:
        await capture_error(
            exc,
            kind="file_detector_failed",
            context={"file_id": ctx.file_id, "detector_kind": spec.kind, "tier": tier},
        )
        return DetectorResult(
            kind=spec.kind,
            confidence_tier=tier,
            detector_version="v0",
            status="failed",
            elapsed_ms=int((time.monotonic() - started) * 1000),
            error=f"{type(exc).__name__}: {exc}\n{traceback.format_exc(limit=2)}",
        )


def _extract_page_info(mime_type: str, pdf_bytes: bytes) -> list[PageInfo]:
    """Read page dimensions / rotation for the upfront file_pages upsert.

    Currently PDF-only — returns [] for other types so the dispatcher skips
    upsert_pages cleanly. Adding a new file type is a registry entry +
    an extractor here.
    """
    if mime_type != "application/pdf":
        return []
    try:
        from ..specific_handlers.pdf.internal import load_pymupdf

        pymupdf = load_pymupdf()
        out: list[PageInfo] = []
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
            for i in range(doc.page_count):
                page = doc[i]
                rect = page.rect
                out.append(
                    PageInfo(
                        source_page_index=i,
                        page_index=i,
                        width_pt=float(rect.width),
                        height_pt=float(rect.height),
                        rotation=int(page.rotation) % 360,
                        text_source="unknown",
                    )
                )
        return out
    except Exception:
        return []


__all__ = [
    "ANALYZER_VERSION",
    "AnalysisOutcome",
    "AnalysisProgressCallback",
    "AnalysisProgressEvent",
    "analyze_file",
]

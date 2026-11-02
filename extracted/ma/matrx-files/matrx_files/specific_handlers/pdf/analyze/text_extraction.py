"""Text-extraction detectors — native and OCR variants.

Native: PyMuPDF .get_text("text") per page. Records per-page coverage map
into PipelineContext so downstream detectors can find which pages have which
text source, and so the OCR router knows which pages to OCR.

OCR: renders the pages flagged by the OCR router and runs the host-injected
provider. Writes results under text_source="ocr" so consumers can distinguish.
Also writes per-page OCR confidence (mean of word-level confidences from
pytesseract.image_to_data) back to file_pages via the host persistence proto.
"""

from __future__ import annotations

import asyncio
import io
import time
from typing import Any

from ....analysis import (
    Detector,
    DetectorResult,
    DetectorSpec,
    PipelineContext,
    register_detector,
)
from ....analysis.ocr_router import _TesseractProvider, select_pages_for_ocr
from ....analysis.text_sanitize import sanitize_text
from ..concurrency import _ocr_worker_count, run_in_cpu_executor, run_in_ocr_executor
from ..extract.text import native_page_text
from ..internal import load_pymupdf

NATIVE_KIND = "text_extraction_native"
OCR_KIND = "text_extraction_ocr"
DETECTOR_VERSION = "v1"


def _open_doc(ctx: PipelineContext):
    doc = ctx.cache.get("pymupdf_doc")
    if doc is not None:
        return doc
    pymupdf = load_pymupdf()
    doc = pymupdf.open(stream=ctx.bytes_in_memory, filetype="pdf")
    ctx.cache["pymupdf_doc"] = doc
    return doc


def _extract_native_text(doc) -> tuple[dict[int, dict[str, Any]], dict[int, dict[str, Any]], int]:
    """CPU-bound per-page native text pull — designed to run off the loop."""
    per_page: dict[int, dict[str, Any]] = {}
    coverage: dict[int, dict[str, Any]] = {}
    char_total = 0
    for i in range(doc.page_count):
        page = doc[i]
        # PyMuPDF can pull control characters (notably \x00 NUL bytes)
        # straight out of PDF font / encoding tables. Postgres rejects
        # those in text / jsonb columns, so we sanitize at the extraction
        # boundary — every downstream consumer can treat the text as
        # storage-safe. See ``analysis.text_sanitize`` for the policy.
        text = sanitize_text(native_page_text(page))
        rect = page.rect
        has_text_layer = bool(text.strip())
        per_page[i + 1] = {
            "page_number": i + 1,
            "text": text,
            "chars": len(text),
            "source": "native",
        }
        coverage[i + 1] = {
            "chars": len(text),
            "has_text_layer": has_text_layer,
            "width": float(rect.width),
            "height": float(rect.height),
        }
        char_total += len(text)
    return per_page, coverage, char_total


class TextExtractionNativeDetector(Detector):
    kind = NATIVE_KIND
    version = DETECTOR_VERSION
    cost_class = "fast"

    async def run(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        started = time.monotonic()
        doc = _open_doc(ctx)
        # PyMuPDF text extraction across every page is CPU-bound; run it OFF
        # the event loop. The dispatcher serializes detectors so the shared
        # ``doc`` is only touched by this one worker thread at a time.
        per_page, coverage, char_total = await run_in_cpu_executor(_extract_native_text, doc)

        # Stash for downstream detectors.
        ctx.cache["page_text_native"] = per_page
        ctx.cache["text_coverage_map"] = coverage
        text_source_map = {
            str(p): "native" if coverage[p]["has_text_layer"] else "missing" for p in coverage
        }
        ctx.cache["text_source_map"] = text_source_map

        # Pre-pick pages for OCR so the OCR detector can read it.
        ocr_pages = select_pages_for_ocr(coverage)
        ctx.cache["ocr_pages_needed"] = ocr_pages

        # Persist text_source per page so file_pages knows which pages have
        # native text vs. need OCR. The OCR detector overrides this for OCR'd
        # pages after it lands.
        persistence = ctx.cache.get("persistence")
        page_id_by_index: dict[int, str] = ctx.cache.get("page_id_by_index") or {}
        if persistence is not None:
            ocr_set = set(ocr_pages)
            for page_no in coverage.keys():
                pid = page_id_by_index.get(page_no - 1)
                if pid is None:
                    continue
                if page_no in ocr_set:
                    # Will be filled in by the OCR detector.
                    text_source = "none" if not coverage[page_no]["has_text_layer"] else "native"
                else:
                    text_source = "native"
                try:
                    await persistence.update_page_text_source(
                        page_id=pid,
                        text_source=text_source,
                        ocr_confidence=None,
                    )
                except Exception:
                    pass

        elapsed = int((time.monotonic() - started) * 1000)
        summary = {
            "page_count": doc.page_count,
            "chars_total": char_total,
            "pages_with_text_layer": sum(1 for c in coverage.values() if c["has_text_layer"]),
            "pages_needing_ocr": len(ocr_pages),
        }
        payload = {
            "pages": list(per_page.values()),
            "coverage": coverage,
            "ocr_pages_needed": ocr_pages,
        }
        return DetectorResult(
            kind=NATIVE_KIND,
            confidence_tier="n/a",
            detector_version=DETECTOR_VERSION,
            elapsed_ms=elapsed,
            summary=summary,
            payload=payload,
            text_sources=["native"],
        )


def _render_page_png(page) -> bytes:
    pix = page.get_pixmap(dpi=200, alpha=False)
    return bytes(pix.tobytes("png"))


def _ocr_confidence_for_image(image_bytes: bytes) -> float | None:
    """Mean word-level confidence (0..1) from pytesseract.image_to_data.

    Returns None when Tesseract isn't available or when the image had no
    recognizable words. Used to flag bad-scan pages in the UI.
    """
    try:
        import pytesseract
        from PIL import Image
    except Exception:
        return None
    try:
        img = Image.open(io.BytesIO(image_bytes))
        data = pytesseract.image_to_data(
            img,
            output_type=pytesseract.Output.DICT,
            config="--oem 3 --psm 6",
        )
    except Exception:
        return None
    raw = data.get("conf") or []
    # Tesseract returns -1 for tokens it skipped — filter those.
    confs: list[float] = []
    for v in raw:
        try:
            f = float(v)
        except (TypeError, ValueError):
            continue
        if f >= 0:
            confs.append(f)
    if not confs:
        return None
    return sum(confs) / len(confs) / 100.0  # Tesseract returns 0..100 → normalize to 0..1


# 🚨 THE OCR DETECTOR IS BOUNDED (2026-09-26). It used to OCR every flagged
# page serially — render, Tesseract for the text, then Tesseract AGAIN for the
# confidence — inside the dispatcher's hard ``wait_for`` (120 s). A 133-page
# slide deck (128 sparse pages flagged) died at 120 s twice in a row and every
# page it HAD read was thrown away with the timeout: the studio got nothing but
# "failed". Now:
#   * one Tesseract pass per page yields text AND confidence (image_to_data);
#   * pages are OCR'd concurrently across the OCR worker pool (rendering stays
#     serial — a PyMuPDF Document is never touched by two threads);
#   * the detector owns a time budget below the dispatcher's timeout and stops
#     STARTING pages when it is spent, returning what it read plus an honest
#     ``complete: false`` / ``pages_pending`` in the summary.
# Guard: tests/test_ocr_detector_is_bounded.py.
OCR_BUDGET_FRACTION = 0.75
"""Share of the dispatcher's hard timeout the detector may spend STARTING
pages; the rest is headroom for the pages already in flight to land."""


def _ocr_text_and_confidence(image_bytes: bytes) -> tuple[str, float | None]:
    """ONE Tesseract pass → (text, mean word confidence 0..1).

    Text is rebuilt from ``image_to_data`` words grouped by block / paragraph /
    line, the same layout ``image_to_string`` prints. Raises
    ``TesseractNotFoundError`` unchanged (the detector announces it once);
    any other per-image failure is ``("", None)``, as ``ocr_image_bytes`` does.
    """
    from matrx_files._extras import require

    pytesseract = require("pytesseract", "ocr", "OCR")
    from PIL import Image

    try:
        img = Image.open(io.BytesIO(image_bytes))
        data = pytesseract.image_to_data(
            img,
            output_type=pytesseract.Output.DICT,
            config="--oem 3 --psm 6",
        )
    except pytesseract.TesseractNotFoundError:
        raise
    except Exception as exc:  # noqa: BLE001 — a bad image is a blank page, not a crash
        print(f"[matrx-pdf-ocr] image OCR failed: {exc}")
        return "", None

    lines: list[str] = []
    current_key: tuple[int, int, int] | None = None
    current_par: tuple[int, int] | None = None
    words: list[str] = []
    confs: list[float] = []
    n = len(data.get("text") or [])
    for i in range(n):
        word = (data["text"][i] or "").strip()
        try:
            conf = float(data["conf"][i])
        except (TypeError, ValueError, KeyError, IndexError):
            conf = -1.0
        if not word:
            continue
        if conf >= 0:
            confs.append(conf)
        key = (int(data["block_num"][i]), int(data["par_num"][i]), int(data["line_num"][i]))
        if key != current_key:
            if words:
                lines.append(" ".join(words))
            if current_par is not None and key[:2] != current_par:
                lines.append("")
            words = []
            current_key = key
            current_par = key[:2]
        words.append(word)
    if words:
        lines.append(" ".join(words))
    text = "\n".join(lines)
    confidence = (sum(confs) / len(confs) / 100.0) if confs else None
    return text, confidence


class TextExtractionOcrDetector(Detector):
    kind = OCR_KIND
    version = DETECTOR_VERSION
    cost_class = "slow"

    def __init__(self, budget_seconds: float | None = None) -> None:
        self.budget_seconds = budget_seconds

    async def _ocr_one(self, provider: Any, png: bytes) -> tuple[str, float | None]:
        # Tesseract in-process: one pass for text + confidence. Any other
        # provider (cloud OCR) returns text; confidence stays the Tesseract
        # scorer, exactly as before.
        if isinstance(provider, _TesseractProvider):
            text, confidence = await run_in_ocr_executor(_ocr_text_and_confidence, png)
            return sanitize_text(text), confidence
        text = sanitize_text(await provider.ocr_page_image(png))
        confidence = await run_in_ocr_executor(_ocr_confidence_for_image, png)
        return text, confidence

    async def run(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        started = time.monotonic()
        ocr_pages = ctx.cache.get("ocr_pages_needed") or []
        provider = ctx.cache.get("ocr_provider")
        if not ocr_pages or provider is None:
            return DetectorResult(
                kind=OCR_KIND,
                confidence_tier="n/a",
                detector_version=DETECTOR_VERSION,
                elapsed_ms=int((time.monotonic() - started) * 1000),
                status="skipped",
                summary={"pages_ocred": 0},
                payload={"pages": []},
                text_sources=["ocr"],
            )

        doc = _open_doc(ctx)
        per_page: dict[int, dict[str, Any]] = dict(ctx.cache.get("page_text_native") or {})
        ocr_by_page: dict[int, dict[str, Any]] = {}
        chars_ocred = 0

        # Per-page persistence is host-injected; resolves page_id from page_index.
        persistence = ctx.cache.get("persistence")
        page_id_by_index: dict[int, str] = ctx.cache.get("page_id_by_index") or {}

        deadline = (
            started + self.budget_seconds if self.budget_seconds and self.budget_seconds > 0 else None
        )
        in_flight_limit = max(1, _ocr_worker_count())
        in_flight: dict[asyncio.Task, int] = {}
        binary_missing: BaseException | None = None
        budget_spent = False

        async def _land(done: set[asyncio.Task]) -> None:
            nonlocal chars_ocred, binary_missing
            for task in done:
                page_no = in_flight.pop(task)
                exc = task.exception()
                if exc is not None:
                    if type(exc).__name__ == "TesseractNotFoundError":
                        binary_missing = binary_missing or exc
                        continue
                    raise exc
                text, confidence = task.result()
                ocr_by_page[page_no] = {
                    "page_number": page_no,
                    "chars": len(text),
                    "text": text,
                    "ocr_confidence": confidence,
                }
                existing = per_page.get(page_no) or {"page_number": page_no, "chars": 0, "text": ""}
                existing["text_ocr"] = text
                existing["chars_ocr"] = len(text)
                existing["ocr_confidence"] = confidence
                text_source = "mixed" if existing.get("chars") else "ocr"
                existing["source"] = text_source
                per_page[page_no] = existing
                chars_ocred += len(text)
                # Persist text_source + confidence back to file_pages — the
                # override-protection-aware "this page now has OCR text" signal.
                if persistence is not None:
                    pid = page_id_by_index.get(page_no - 1)
                    if pid is not None:
                        try:
                            await persistence.update_page_text_source(
                                page_id=pid,
                                text_source=text_source,
                                ocr_confidence=confidence,
                            )
                        except Exception:
                            pass  # Non-fatal — analysis still completes.

        try:
            for page_no in ocr_pages:
                if page_no < 1 or page_no > doc.page_count:
                    continue
                if binary_missing is not None:
                    # The OCR binary is missing on this host — every remaining
                    # page would fail identically. Stop spending render time.
                    break
                if deadline is not None and time.monotonic() >= deadline:
                    budget_spent = True
                    break
                while len(in_flight) >= in_flight_limit:
                    done, _ = await asyncio.wait(in_flight.keys(), return_when=asyncio.FIRST_COMPLETED)
                    await _land(done)
                if binary_missing is not None:
                    break
                # Rendering touches the shared Document — serial, never concurrent.
                png = await run_in_ocr_executor(_render_page_png, doc[page_no - 1])
                task = asyncio.ensure_future(self._ocr_one(provider, png))
                in_flight[task] = page_no
            while in_flight:
                done, _ = await asyncio.wait(in_flight.keys(), return_when=asyncio.FIRST_COMPLETED)
                await _land(done)
        finally:
            for task in in_flight:
                task.cancel()

        if binary_missing is not None:
            # Board row H8: an infrastructure wall, announced ONCE per document.
            from matrx_utils.block_sink import announce_block
            from matrx_utils.ctx import get_active_organization_id

            announce_block(
                # Resolved HERE, synchronously — `announce_block` fires its sink
                # as a `detached_task` with no inherited ContextVar state.
                organization_id=get_active_organization_id(),
                input_ref=ctx.file_id,
                source_type="file",
                engine="file_reader",
                error_class="ocr_binary_missing",
                error_sentence=(
                    f"OCR provider {getattr(provider, 'provider_id', 'unknown')!r} needs "
                    f"the Tesseract binary and it is not installed on this host: {binary_missing}"
                ),
                input_label=ctx.file_id,
            )

        done_pages = sorted(ocr_by_page)
        requested = [p for p in ocr_pages if 1 <= p <= doc.page_count]
        pending = [p for p in requested if p not in ocr_by_page]
        ocr_results = [ocr_by_page[p] for p in done_pages]

        ctx.cache["page_text_combined"] = per_page
        ctx.cache["ocr_pages_completed"] = done_pages
        # Update text_source_map ONLY for pages actually OCR'd.
        tsm = ctx.cache.get("text_source_map") or {}
        for p in done_pages:
            key = str(p)
            tsm[key] = "ocr" if tsm.get(key) in (None, "missing") else "mixed"
        ctx.cache["text_source_map"] = tsm

        confs = [r["ocr_confidence"] for r in ocr_results if r.get("ocr_confidence") is not None]
        mean_conf = (sum(confs) / len(confs)) if confs else None

        summary: dict[str, Any] = {
            "pages_ocred": len(ocr_results),
            "pages_requested": len(requested),
            "pages_pending": len(pending),
            "complete": not pending,
            "chars_total_ocr": chars_ocred,
            "provider": getattr(provider, "provider_id", "unknown"),
            "mean_confidence": mean_conf,
        }
        if budget_spent and pending:
            summary["stopped_reason"] = "time_budget"
            summary["budget_seconds"] = self.budget_seconds
        elif binary_missing is not None and pending:
            summary["stopped_reason"] = "ocr_binary_missing"
        return DetectorResult(
            kind=OCR_KIND,
            confidence_tier="n/a",
            detector_version=DETECTOR_VERSION,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            summary=summary,
            payload={"pages": ocr_results, "pages_pending": pending},
            text_sources=["ocr"],
            page_numbers=done_pages,
        )


def _native_factory(spec: DetectorSpec) -> Detector:
    return TextExtractionNativeDetector()


def _ocr_factory(spec: DetectorSpec) -> Detector:
    return TextExtractionOcrDetector(budget_seconds=spec.timeout_seconds * OCR_BUDGET_FRACTION)


register_detector(NATIVE_KIND, _native_factory)
register_detector(OCR_KIND, _ocr_factory)


__all__ = [
    "NATIVE_KIND",
    "OCR_KIND",
    "DETECTOR_VERSION",
    "TextExtractionNativeDetector",
    "TextExtractionOcrDetector",
]

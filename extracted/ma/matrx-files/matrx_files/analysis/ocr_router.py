"""OCR provider protocol + the per-page decision routine.

The provider is the indirection point so we can swap Tesseract → Mistral OCR
→ Azure OCR → cloud_ocr/ implementations without touching detectors.

The router looks at a `text_coverage_map` (built by `text_extraction_native`)
and decides which pages need OCR. It does not run OCR itself — that's the
`text_extraction_ocr` detector's job. This module exists so the decision
logic is one place and unit-testable in isolation.
"""

from __future__ import annotations

from typing import Any, Protocol


class OcrProviderProtocol(Protocol):
    """Host-injected OCR backend."""

    provider_id: str

    async def ocr_page_image(self, image_bytes: bytes) -> str: ...


# ── default in-process provider (Tesseract via pytesseract) ───────────────────

class _TesseractProvider:
    provider_id = "tesseract"

    async def ocr_page_image(self, image_bytes: bytes) -> str:
        # Lazy import — pytesseract is an optional dep of analyzers, not analysis core.
        from ..specific_handlers.pdf.concurrency import run_in_ocr_executor
        from ..specific_handlers.pdf.extract.ocr import ocr_image_bytes

        # Tesseract is CPU-bound (~1.4s/page) and would otherwise block the event
        # loop for every concurrent request. The in-process provider owns its own
        # offload; a cloud-OCR provider that does genuine async HTTP I/O just awaits.
        return await run_in_ocr_executor(ocr_image_bytes, image_bytes)


DEFAULT_OCR_PROVIDER = _TesseractProvider()


def needs_ocr(
    *,
    char_count: int,
    has_text_layer: bool,
    width: float,
    height: float,
    sparseness_chars_per_inch_sq: float = 8.0,
) -> bool:
    """Decide whether a single page needs OCR.

    Reasons a page might need OCR:
      - No native text layer at all (scanned page).
      - Text layer is suspiciously sparse — fewer chars per visual area than
        a typical native PDF page would produce. Heuristic, tunable.
    """
    if not has_text_layer:
        return True
    if char_count <= 0:
        return True
    # Convert PDF points → square inches (72 pt/in)
    area_in2 = max(1.0, (width / 72.0) * (height / 72.0))
    density = char_count / area_in2
    return density < sparseness_chars_per_inch_sq


def select_pages_for_ocr(coverage_map: dict[int, dict[str, Any]]) -> list[int]:
    """Given a {page_no: {chars, has_text_layer, width, height}} map, return pages needing OCR."""
    out: list[int] = []
    for page_no in sorted(coverage_map.keys()):
        info = coverage_map[page_no]
        if needs_ocr(
            char_count=int(info.get("chars", 0)),
            has_text_layer=bool(info.get("has_text_layer", False)),
            width=float(info.get("width", 0.0)),
            height=float(info.get("height", 0.0)),
        ):
            out.append(page_no)
    return out


__all__ = [
    "OcrProviderProtocol",
    "DEFAULT_OCR_PROVIDER",
    "needs_ocr",
    "select_pages_for_ocr",
]

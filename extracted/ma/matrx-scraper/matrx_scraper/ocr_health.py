"""Is an OCR engine actually usable on THIS host?

`import pytesseract` succeeding proves only that a Python wrapper is installed.
The wrapper shells out to the `tesseract` BINARY, and the production scraper
image installed the wrapper but never the binary — so every scanned PDF reached
the OCR branch and died with `TesseractNotFoundError: tesseract is not installed
or it's not in your PATH`, reported to the user as a per-document failure
(`pdf_extraction_failed`) rather than as the deployment defect it was
(acquisition-frontier block hunt, 2026-09-17: every scanned PDF, and therefore a
large share of "the law" and of out-of-print books, was unreachable).

The class fix is here: ONE probe of the real engine that every OCR decision and
the readiness snapshot both read, so a missing engine is loud at the door
instead of silent per document.
"""

from __future__ import annotations

from dataclasses import dataclass

#: Cached because the probe spawns a process; a binary does not appear or
#: vanish inside one container's lifetime.
_probe: OcrStatus | None = None


@dataclass(frozen=True)
class OcrStatus:
    """What this host can actually do about an image of text."""

    #: True only when the wrapper AND the engine binary are both usable.
    available: bool
    #: e.g. "5.3.0" — evidence the probe really ran the engine.
    version: str | None = None
    #: Human-readable cause when unavailable; travels onto the wire so a
    #: caller never has to guess whether the document or the host was at fault.
    reason: str | None = None

    def as_dict(self) -> dict[str, object]:
        return {"available": self.available, "version": self.version, "reason": self.reason}


def _probe_tesseract() -> OcrStatus:
    try:
        import pytesseract
    except ImportError as exc:
        return OcrStatus(
            available=False,
            reason=(
                "the pytesseract wrapper is not installed on this host "
                f"(install matrx-scraper[ocr]): {exc}"
            ),
        )
    try:
        version = str(pytesseract.get_tesseract_version())
    except Exception as exc:  # noqa: BLE001 — the cause travels with the verdict
        return OcrStatus(
            available=False,
            reason=(
                "the tesseract OCR engine binary is missing from this host's PATH "
                "(install the OS package `tesseract-ocr`; the Python wrapper alone "
                f"cannot read an image): {type(exc).__name__}: {exc}"
            ),
        )
    return OcrStatus(available=True, version=version)


def ocr_status(*, refresh: bool = False) -> OcrStatus:
    """The one answer to "can this host OCR?" — probed once, then cached."""
    global _probe
    if _probe is None or refresh:
        _probe = _probe_tesseract()
    return _probe


def ocr_available() -> bool:
    return ocr_status().available

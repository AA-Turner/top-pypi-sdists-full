"""OCR helpers used by text extraction.

Tesseract is invoked via ``pytesseract``. The default configuration
(``--oem 3 --psm 6``) treats every page as a uniform block of text, which is
the most reliable mode for legal/medical document scans.
"""

from __future__ import annotations

import io
from typing import Any

from PIL import Image


def _tesseract():  # noqa: ANN202
    """pytesseract, the matrx-files[ocr] extra, imported at the point of OCR."""
    from matrx_files._extras import require

    return require("pytesseract", "ocr", "OCR")


_DEFAULT_TESSERACT_CONFIG = r"--oem 3 --psm 6"


def ocr_pymupdf_page(page: Any, dpi: int = 300, config: str | None = None) -> str:
    """Render a PyMuPDF page at *dpi* and run Tesseract over the result."""
    pix = page.get_pixmap(dpi=dpi, alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return _tesseract().image_to_string(
        img, config=config or _DEFAULT_TESSERACT_CONFIG
    )


def ocr_image_bytes(image_bytes: bytes, config: str | None = None) -> str:
    """Run Tesseract over arbitrary image bytes. Returns "" on a per-image
    failure (a bad image, a decode error).

    Raises ``pytesseract.TesseractNotFoundError`` unchanged rather than
    swallowing it. Before this, EVERY failure here — including "the
    Tesseract binary is not installed on this host" — was caught by the same
    blanket ``except Exception`` and turned into a silent "" (board row H8:
    a caller running dozens of pages through a host with no Tesseract binary
    got dozens of empty strings and a print() nobody durably reads, never a
    finding). The infrastructure gap propagates so the async caller —
    ``TextExtractionOcrDetector.run`` — can announce it to the Block Ledger
    ONCE per document instead of once per page, and every other decode
    failure keeps its old, non-fatal "" behavior.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        return _tesseract().image_to_string(
            img, config=config or _DEFAULT_TESSERACT_CONFIG
        )
    except _tesseract().TesseractNotFoundError:
        raise
    except Exception as exc:
        print(f"[matrx-pdf-ocr] image OCR failed: {exc}")
        return ""


__all__ = ["ocr_pymupdf_page", "ocr_image_bytes"]

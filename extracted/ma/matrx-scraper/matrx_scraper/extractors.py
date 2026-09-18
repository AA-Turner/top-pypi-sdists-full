from __future__ import annotations

import asyncio
import io
import json
import re

from matrx_utils import vcprint

from matrx_scraper.ocr_health import ocr_status

try:
    import pytesseract
    from PIL import Image

    OCR_IMPORTS_PRESENT = True
except ImportError:
    OCR_IMPORTS_PRESENT = False

# 🚨 NEVER test OCR availability by import alone. `pytesseract` is a wrapper
# that shells out to the `tesseract` BINARY: the production image had the
# wrapper and no binary, so this flag was True, the PDF path asked for OCR, and
# every scanned document died with a raw `TesseractNotFoundError` presented to
# the user as a bad PDF (acquisition-frontier block hunt, 2026-09-17). The
# single source of truth is `ocr_health.ocr_status()`, which runs the engine.
OCR_CONFIG = r"--oem 3 --psm 6"
OCR_LOW_TEXT_THRESHOLD = 50


def _ocr_usable() -> bool:
    return OCR_IMPORTS_PRESENT and ocr_status().available


def extract_text_from_pdf_bytes_or_reason(pdf_bytes: bytes) -> tuple[str | None, str | None]:
    """Extract a PDF's text, or say WHY it could not be extracted.

    Returns ``(text, None)`` on success and ``(None, reason)`` otherwise. The
    reason is a short, human-readable cause a caller can put on the wire —
    an ImportError here means the host image lacks the ``[pdf]`` extra, which
    is a deployment defect, not "this PDF has no text".
    """
    try:
        from matrx_files.specific_handlers.pdf_handler import (
            extract_text_from_pdf_bytes_sync,
        )
    except ImportError as e:
        reason = f"pdf support missing on this host (install matrx-scraper[pdf]): {e}"
        vcprint(f"Error extracting text from PDF: {reason}", color="red")
        return None, reason
    ocr = ocr_status()
    ocr_usable = _ocr_usable()
    try:
        text = extract_text_from_pdf_bytes_sync(
            pdf_bytes,
            force_ocr=False,
            # 0 disables the OCR branch entirely. Asking for OCR on a host with
            # no engine does not "try anyway" — it raises TesseractNotFoundError
            # from inside the handler and loses the page's embedded text too.
            use_ocr_threshold=OCR_LOW_TEXT_THRESHOLD if ocr_usable else 0,
        )
    except Exception as e:  # noqa: BLE001 — the reason travels with the failure
        reason = f"{type(e).__name__}: {e}"
        vcprint(f"Error extracting text from PDF: {reason}", color="red")
        return None, reason
    if text.strip():
        return text.strip(), None
    if not ocr_usable:
        # The document may well be a scan we COULD have read. Say that this
        # host cannot, and why — never let a deployment gap read as a bad PDF.
        return None, (
            "the PDF yielded no embedded text and this host cannot OCR it: "
            f"{ocr.reason or 'no OCR engine available'}"
        )
    return None, "the PDF yielded no text (OCR ran and found none, or the file is empty)"


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str | None:
    text, _reason = extract_text_from_pdf_bytes_or_reason(pdf_bytes)
    return text


def extract_text_from_image_bytes(image_bytes: bytes) -> str | None:
    if not _ocr_usable():
        vcprint(
            f"cannot extract image text: {ocr_status().reason or 'no OCR engine available'}",
            color="red",
        )
        return None
    try:
        img = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(img, config=OCR_CONFIG)
        return text.strip() if text.strip() else None
    except Exception as e:
        vcprint(f"Error extracting text from image: {e}", color="red")
        return None


async def extract_text_from_pdf_bytes_async(pdf_bytes: bytes) -> str | None:
    return await asyncio.to_thread(extract_text_from_pdf_bytes, pdf_bytes)


async def extract_text_from_image_bytes_async(image_bytes: bytes) -> str | None:
    return await asyncio.to_thread(extract_text_from_image_bytes, image_bytes)


def format_json_content(text: str) -> str | None:
    try:
        parsed = json.loads(text)
        return json.dumps(parsed, indent=2, ensure_ascii=False)
    except (json.JSONDecodeError, TypeError):
        return text if text.strip() else None


def extract_xml_text(text: str) -> str | None:
    cleaned = re.sub(r"<[^>]+>", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned if cleaned else None


def extract_text_content(text: str, content_type_value: str) -> str | None:
    if content_type_value in ("md", "txt"):
        return text.strip() if text.strip() else None
    elif content_type_value == "json":
        return format_json_content(text)
    elif content_type_value == "xml":
        return extract_xml_text(text)
    else:
        return text.strip() if text.strip() else None

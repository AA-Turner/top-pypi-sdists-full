from __future__ import annotations

import asyncio
import io
import json
import re

from matrx_utils import vcprint

try:
    import pytesseract
    from PIL import Image

    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

OCR_CONFIG = r"--oem 3 --psm 6"
OCR_LOW_TEXT_THRESHOLD = 50


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str | None:
    try:
        from matrx_files.specific_handlers.pdf_handler import (
            extract_text_from_pdf_bytes_sync,
        )

        text = extract_text_from_pdf_bytes_sync(
            pdf_bytes,
            force_ocr=False,
            use_ocr_threshold=OCR_LOW_TEXT_THRESHOLD if OCR_AVAILABLE else 0,
        )
        return text.strip() if text.strip() else None
    except Exception as e:
        vcprint(f"Error extracting text from PDF: {e}", color="red")
        return None


def extract_text_from_image_bytes(image_bytes: bytes) -> str | None:
    if not OCR_AVAILABLE:
        vcprint("pytesseract/Pillow not installed — cannot extract image text", color="red")
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

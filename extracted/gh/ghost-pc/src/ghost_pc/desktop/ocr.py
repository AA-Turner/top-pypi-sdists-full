"""OCR layer for extracting text from screenshots.

Two-tier approach:
1. Primary: Windows built-in OCR via WinRT (zero download, instant, word-level bboxes)
2. Fallback: RapidOCR-ONNXRuntime for complex layouts or non-Windows

Used when UIA returns no useful controls (custom-rendered UI, Electron apps
without accessibility, games, etc.).
"""

from __future__ import annotations

import logging
import sys
from typing import TypedDict

logger = logging.getLogger(__name__)


class OcrResult(TypedDict):
    """A single recognized text region."""

    text: str
    bbox: tuple[int, int, int, int]  # (left, top, right, bottom)
    confidence: float


async def extract_text(screenshot_bytes: bytes) -> list[OcrResult]:
    """Extract text with bounding boxes from a screenshot.

    Tries WinRT OCR first (Windows-only), falls back to RapidOCR.

    Args:
        screenshot_bytes: PNG image bytes.

    Returns:
        List of OcrResult with text, bounding box, and confidence.
    """
    # Try WinRT OCR first on Windows
    if sys.platform == "win32":
        results = await _winrt_ocr(screenshot_bytes)
        if results:
            return results

    # Fallback: RapidOCR
    results = _rapid_ocr(screenshot_bytes)
    if results:
        return results

    return []


async def _winrt_ocr(screenshot_bytes: bytes) -> list[OcrResult]:
    """Extract text using Windows Runtime OCR API.

    Uses the built-in Windows OCR engine which provides word-level
    bounding boxes with good accuracy for standard UI text.
    """
    try:
        import asyncio

        from winrt.windows.globalization import Language
        from winrt.windows.graphics.imaging import (
            BitmapDecoder,
            SoftwareBitmap,
        )
        from winrt.windows.media.ocr import OcrEngine
        from winrt.windows.storage.streams import (
            DataWriter,
            InMemoryRandomAccessStream,
        )

        # Write bytes to a WinRT stream
        stream = InMemoryRandomAccessStream()
        writer = DataWriter(stream)
        writer.write_bytes(screenshot_bytes)
        await asyncio.to_thread(writer.store_async)
        stream.seek(0)

        # Decode the image
        decoder = await asyncio.to_thread(BitmapDecoder.create_async, stream)
        bitmap: SoftwareBitmap = await asyncio.to_thread(decoder.get_software_bitmap_async)

        # Create OCR engine (English)
        engine = OcrEngine.try_create_from_language(Language("en-US"))
        if engine is None:
            return []

        # Run OCR
        ocr_result = await asyncio.to_thread(engine.recognize_async, bitmap)

        results: list[OcrResult] = []
        for line in ocr_result.lines:
            for word in line.words:
                rect = word.bounding_rect
                results.append(
                    OcrResult(
                        text=word.text,
                        bbox=(
                            int(rect.x),
                            int(rect.y),
                            int(rect.x + rect.width),
                            int(rect.y + rect.height),
                        ),
                        confidence=0.9,  # WinRT doesn't expose confidence
                    )
                )

        return results

    except ImportError:
        logger.debug("WinRT OCR packages not installed")
        return []
    except Exception as e:
        logger.debug("WinRT OCR failed: %s", e)
        return []


def _rapid_ocr(screenshot_bytes: bytes) -> list[OcrResult]:
    """Extract text using RapidOCR-ONNXRuntime (cross-platform fallback)."""
    try:
        from io import BytesIO

        import numpy as np
        from PIL import Image
        from rapidocr_onnxruntime import RapidOCR

        img = Image.open(BytesIO(screenshot_bytes))
        img_array = np.array(img)

        ocr = RapidOCR()
        result, _ = ocr(img_array)

        if not result:
            return []

        results: list[OcrResult] = []
        for item in result:
            # RapidOCR returns: [box_points, text, confidence]
            box_points, text, confidence = item
            # box_points is [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            xs = [p[0] for p in box_points]
            ys = [p[1] for p in box_points]
            results.append(
                OcrResult(
                    text=text,
                    bbox=(int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))),
                    confidence=float(confidence),
                )
            )

        return results

    except ImportError:
        logger.debug("RapidOCR not installed — OCR unavailable")
        return []
    except Exception as e:
        logger.debug("RapidOCR failed: %s", e)
        return []

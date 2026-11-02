"""Board row H8 — a missing Tesseract binary is an infrastructure wall, not a
per-page "".

Before this fix, `ocr_image_bytes` caught EVERY exception from
`pytesseract.image_to_string` — including `TesseractNotFoundError`, raised
when the binary itself is not installed on the host — logged one `print()`
line, and returned `""`. A document run through OCR on such a host produced
silent empty text for every page and no durable record anywhere that OCR
never ran at all. This test pins the FAILING behavior it replaces (a caught
`TesseractNotFoundError` used to become `""`) and the PASSING behavior now in
place (it propagates, so the async caller can announce it to the Block
Ledger exactly once instead of losing it on every page).
"""

from __future__ import annotations

from unittest.mock import patch

import pytest


def test_tesseract_not_found_propagates_instead_of_becoming_empty_string():
    import pytesseract

    from matrx_files.specific_handlers.pdf.extract.ocr import ocr_image_bytes

    with patch(
        "pytesseract.image_to_string",
        side_effect=pytesseract.TesseractNotFoundError(),
    ):
        # A 1x1 PNG — content doesn't matter, image_to_string is mocked.
        png_1x1 = bytes.fromhex(
            "89504e470d0a1a0a0000000d4948445200000001000000010806000000"
            "1f15c4890000000a49444154789c6360000002000155a2415c00000000"
            "49454e44ae426082"
        )
        with pytest.raises(pytesseract.TesseractNotFoundError):
            ocr_image_bytes(png_1x1)


def test_an_ordinary_decode_failure_still_returns_empty_string_not_fatal():
    """The non-fatal `""` posture is UNCHANGED for every other failure —
    only the infrastructure-missing case became loud."""
    from matrx_files.specific_handlers.pdf.extract.ocr import ocr_image_bytes

    result = ocr_image_bytes(b"not a real image")

    assert result == ""

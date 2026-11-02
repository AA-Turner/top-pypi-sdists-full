"""The OCR fallback tests READABILITY, not just length.

Arman's ruling, 2026-08-21. A page with a broken font encoding returns plenty
of characters that are pure control bytes — it sails past the length
threshold, so OCR never ran and the caller received garbage that LOOKED like a
successful extraction. Silent garbage is worse than a slow page.
"""

from __future__ import annotations

from matrx_files.specific_handlers.pdf.extract.text import (
    native_text_needs_ocr,
    printable_ratio,
)


def test_control_byte_text_is_unreadable_however_long_it_is():
    # The real failure: 4,184 characters, none of them readable.
    garbage = "\x00\x01\x02" * 1400
    assert len(garbage.strip()) > 100, "must clear the LENGTH test to be a real regression"
    assert printable_ratio(garbage) == 0.0
    assert native_text_needs_ocr(garbage, use_ocr_threshold=100) is True


def test_real_text_is_left_alone():
    text = "Titanium Marketing Pricing Packages. " * 10
    assert printable_ratio(text) == 1.0
    assert native_text_needs_ocr(text, use_ocr_threshold=100) is False


def test_short_page_still_falls_back_on_length():
    assert native_text_needs_ocr("  ", use_ocr_threshold=100) is True


def test_threshold_zero_disables_the_length_test_but_not_the_quality_test():
    # threshold=0 means "don't OCR merely-short pages". Unreadable text is
    # unreadable regardless, so the quality test still fires.
    assert native_text_needs_ocr("ok", use_ocr_threshold=0) is False
    assert native_text_needs_ocr("\x00\x01" * 100, use_ocr_threshold=0) is True


def test_a_tiny_snippet_is_never_judged_on_ratio():
    # Below the minimum sample size a ratio is noise, not signal.
    assert native_text_needs_ocr("ok", use_ocr_threshold=0) is False

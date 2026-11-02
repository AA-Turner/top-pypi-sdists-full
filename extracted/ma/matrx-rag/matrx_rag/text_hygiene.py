"""ONE definition of "non-printing control characters" for stored document text.

Large PDFs carry stray control bytes (U+0003, U+0007 ... from broken font
encodings) in their extracted text; they reached the model unfiltered because
nothing between the extractor and the stored clean text removed them. Every stage
that writes or reads document text uses THIS function, so the rule lives once.

Kept: ``\\n`` and ``\\t``. Line breaks that arrive as ``\\r\\n``, a lone ``\\r`` or a
form feed become ``\\n``. Everything else in the C0 range, DEL and the C1 range is
removed (NUL included, which Postgres rejects anyway).
"""

from __future__ import annotations

import re

_LINE_BREAKS = re.compile(r"\r\n|\r|\f")
_CONTROLS = re.compile(r"[\x00-\x08\x0b\x0e-\x1f\x7f-\x9f]")


def strip_control_chars(text: str | None) -> str:
    """``text`` without non-printing control characters (``\\n`` and ``\\t`` kept)."""
    if not text:
        return text or ""
    if "\r" in text or "\f" in text:
        text = _LINE_BREAKS.sub("\n", text)
    return _CONTROLS.sub("", text)

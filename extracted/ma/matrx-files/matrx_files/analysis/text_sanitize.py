"""Text sanitization for detector-extracted strings.

Any detector that pulls text from an external source — PyMuPDF native PDF
text, Tesseract / cloud OCR, web scraping, transcription — can produce
control characters that have no display semantics and crash downstream
consumers. The most disruptive is ``\\x00`` (NUL): Postgres ``text`` /
``jsonb`` columns reject it outright because Postgres uses C-style
NUL-terminated strings internally, so a single null byte in a PDF text
layer fail-stops a whole JSONB insert.

This module is the canonical "scrub raw extracted text before downstream
use" boundary for matrx-utils. Detectors should call ``sanitize_text``
on every string they pull from an outside source, immediately at the
extraction site, so the rest of the pipeline can treat all strings as
storage-safe.

Policy
------
We strip C0 control characters (``\\x00-\\x1F``) and ``\\x7F`` (DEL),
keeping the three that have meaningful text semantics:

    \\t (HT, 0x09)  — horizontal tab
    \\n (LF, 0x0A)  — line feed
    \\r (CR, 0x0D)  — carriage return

We deliberately also strip ``\\x0B`` (VT) and ``\\x0C`` (FF, page break).
Both occasionally appear in PDF text layers as in-line separators, but
they have no portable display semantics in JSON / HTML / plain-text
consumers, and they're far more often extraction artifacts than
intentional formatting. If a downstream consumer needs page-break
information, the page-aware extractor already provides per-page
``page_number`` keys — encoding it inline via ``\\f`` is redundant and
breaks line-by-line text rendering.

Surrogate halves (``\\uD800-\\uDFFF``) are also stripped: they're invalid
on their own in well-formed UTF-8 and cause downstream encode/decode
failures.
"""

from __future__ import annotations

import re

# Regex matches every character we want gone:
#   \x00-\x08  — NUL through BS (drops null bytes, control chars below tab)
#   \x0B       — VT (vertical tab) — extraction artifact in PDFs
#   \x0C       — FF (form feed / page break) — see module docstring
#   \x0E-\x1F  — SO through US (control chars above CR)
#   \x7F       — DEL
#   \uD800-\uDFFF — lone surrogate halves (invalid in well-formed UTF-8)
#
# Kept: \t (0x09), \n (0x0A), \r (0x0D).
_FORBIDDEN = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\ud800-\udfff]"
)


def sanitize_text(value: str | None) -> str:
    """Strip control characters from an extracted text string.

    Pass-through for ``None`` (returns empty string) and for strings that
    contain no forbidden characters (returns the input unchanged via the
    regex's fast-path: no substitutions needed → identical object). For
    strings that DO contain forbidden chars, returns a new string with
    them removed.

    Examples
    --------
        >>> sanitize_text("Chapter 13\\x00Dr. Terry")
        'Chapter 13Dr. Terry'

        >>> sanitize_text("Page 1\\nContent\\tindented")
        'Page 1\\nContent\\tindented'

        >>> sanitize_text(None)
        ''
    """
    if not value:
        return ""
    # re.sub is no-op when the pattern doesn't match, so the common case
    # (clean text) is essentially free. We don't pre-check with ``in``
    # because the regex covers a range and a regex scan is faster than
    # 30 separate ``in`` checks.
    return _FORBIDDEN.sub("", value)


__all__ = ["sanitize_text"]

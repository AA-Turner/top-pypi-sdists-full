"""One place that answers "are these bytes an Office document, and which kind?".

Every routing table in the platform that needs to recognize Office content
imports ``classify_office`` from here — never re-hardcodes the six MIME strings.
"""

from __future__ import annotations

from .models import (
    DOC_MIME,
    DOCX_MIME,
    PPT_MIME,
    PPTX_MIME,
    XLS_MIME,
    XLSX_MIME,
    OfficeKind,
)

# MIME (normalized) -> kind.
_MIME_TO_KIND: dict[str, OfficeKind] = {
    DOCX_MIME: OfficeKind.docx,
    PPTX_MIME: OfficeKind.pptx,
    XLSX_MIME: OfficeKind.xlsx,
    DOC_MIME: OfficeKind.doc,
    PPT_MIME: OfficeKind.ppt,
    XLS_MIME: OfficeKind.xls,
    # Some clients send the generic OpenXML/zip type — fall back to the suffix.
}

# filename suffix -> kind (TUS uploads routinely carry application/octet-stream).
_EXT_TO_KIND: dict[str, OfficeKind] = {
    ".docx": OfficeKind.docx,
    ".pptx": OfficeKind.pptx,
    ".xlsx": OfficeKind.xlsx,
    ".doc": OfficeKind.doc,
    ".ppt": OfficeKind.ppt,
    ".xls": OfficeKind.xls,
    # macro-enabled variants read the same as their base OpenXML format.
    ".docm": OfficeKind.docx,
    ".pptm": OfficeKind.pptx,
    ".xlsm": OfficeKind.xlsx,
}

# Every Office MIME the platform recognizes (for building routing sets).
OFFICE_MIMES: frozenset[str] = frozenset(_MIME_TO_KIND)
# The three the pure-python codec can actually read/write without LibreOffice.
OPENXML_MIMES: frozenset[str] = frozenset({DOCX_MIME, PPTX_MIME, XLSX_MIME})


def normalize_mime(mime_type: str | None) -> str:
    if not mime_type:
        return ""
    return mime_type.lower().split(";", 1)[0].strip()


def classify_office(mime_type: str | None, file_name: str | None = None) -> OfficeKind | None:
    """Return the ``OfficeKind`` for these bytes, or ``None`` if not Office.

    MIME wins when it's a recognized Office type; otherwise the filename suffix
    decides (covers generic ``application/octet-stream`` / zip uploads)."""
    mime = normalize_mime(mime_type)
    kind = _MIME_TO_KIND.get(mime)
    if kind is not None:
        return kind
    name = (file_name or "").lower()
    for ext, k in _EXT_TO_KIND.items():
        if name.endswith(ext):
            return k
    return None


__all__ = [
    "OFFICE_MIMES",
    "OPENXML_MIMES",
    "normalize_mime",
    "classify_office",
]

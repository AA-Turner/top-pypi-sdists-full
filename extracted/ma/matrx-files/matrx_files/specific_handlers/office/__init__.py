"""Office (OpenXML) codec — one home for reading and writing Microsoft
documents (.docx / .pptx / .xlsx) as AI-facing markdown/portions and from
structured specs.

  from matrx_files.specific_handlers.office import extract_office, generate_office

IN  (extract_office)  — bytes -> OfficeExtraction (markdown + portions).
OUT (generate_office) — DocumentSpec/PresentationSpec/SpreadsheetSpec -> bytes.

This is a pure format codec: no host imports, no ORM, no network, no
LibreOffice. Legacy binary formats (.doc/.ppt/.xls) are detected and raise
``LegacyBinaryOfficeError`` so a caller with LibreOffice can convert first.
"""

from __future__ import annotations

from .convert import (
    LibreOfficeUnavailable,
    OfficeConversionError,
    convert_legacy_to_openxml,
    convert_to_pdf,
    libreoffice_available,
)
from .extract import (
    LegacyBinaryOfficeError,
    OfficeExtractionError,
    UnsupportedOfficeError,
    extract_office,
)
from .generate import (
    generate_docx,
    generate_office,
    generate_pptx,
    generate_xlsx,
)
from .mime import OFFICE_MIMES, OPENXML_MIMES, classify_office, normalize_mime
from .models import (
    DOC_MIME,
    DOCX_MIME,
    PPT_MIME,
    PPTX_MIME,
    XLS_MIME,
    XLSX_MIME,
    DocBlock,
    DocumentSpec,
    OfficeExtraction,
    OfficeGenerationResult,
    OfficeKind,
    OfficePortion,
    PresentationSpec,
    SheetSpec,
    SlideSpec,
    SpreadsheetSpec,
)

__all__ = [
    # extract
    "extract_office",
    "OfficeExtraction",
    "OfficePortion",
    "OfficeExtractionError",
    "LegacyBinaryOfficeError",
    "UnsupportedOfficeError",
    # generate
    "generate_office",
    "generate_docx",
    "generate_pptx",
    "generate_xlsx",
    "OfficeGenerationResult",
    # convert (LibreOffice lane)
    "libreoffice_available",
    "convert_to_pdf",
    "convert_legacy_to_openxml",
    "OfficeConversionError",
    "LibreOfficeUnavailable",
    # specs
    "DocumentSpec",
    "DocBlock",
    "PresentationSpec",
    "SlideSpec",
    "SpreadsheetSpec",
    "SheetSpec",
    # mime / classification
    "classify_office",
    "normalize_mime",
    "OfficeKind",
    "OFFICE_MIMES",
    "OPENXML_MIMES",
    "DOCX_MIME",
    "PPTX_MIME",
    "XLSX_MIME",
    "DOC_MIME",
    "PPT_MIME",
    "XLS_MIME",
]

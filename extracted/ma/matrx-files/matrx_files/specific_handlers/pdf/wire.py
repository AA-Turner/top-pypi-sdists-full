"""Pydantic wire-shape models for endpoint responses that previously returned
``dict[str, Any]``.

Keeping these here (in the matrx-utils PDF package, not under aidream) gives
the OpenAPI generator a stable home for the schemas and lets non-aidream
consumers reuse them without depending on the aidream API layer.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from .analyze.models import RepeatedRegionsReport
from .redact.models import RedactionAudit


class PdfRedactionPatternEntry(BaseModel):
    """One entry in the builtin redaction pattern catalog."""

    id: str
    pattern: str
    description: str


class PdfRedactionPatternCatalog(BaseModel):
    """Wire shape for ``GET /utilities/pdf/redact/patterns``."""

    patterns: list[PdfRedactionPatternEntry]


class PersistedPdfFile(BaseModel):
    """JSON shape returned by mutating PDF endpoints when ``persist_output=true``.

    Mirrors the dict ``_persist_derivative_pdf`` produces — typed here so
    the OpenAPI schema can drive an end-to-end FE type.
    """

    file_id: str
    parent_file_id: str | None = None
    derivation_kind: str | None = None
    derivation_metadata: dict[str, Any] = Field(default_factory=dict)
    filename: str | None = None


class PersistedRedactionResult(PersistedPdfFile):
    """Extension of ``PersistedPdfFile`` for redaction endpoints — carries the
    audit row + verification flag the caller needs to write to
    ``pdf_redaction_audits``.
    """

    audit: RedactionAudit
    verification_passed: bool
    notes: list[str] = Field(default_factory=list)


class StripRepeatedRegionsResultSchema(BaseModel):
    """Wire shape for ``POST /utilities/pdf/strip-repeated-regions``."""

    pages_text: list[str]
    regions: RepeatedRegionsReport
    stripped_region_ids: list[str]


__all__ = [
    "PdfRedactionPatternEntry",
    "PdfRedactionPatternCatalog",
    "PersistedPdfFile",
    "PersistedRedactionResult",
    "StripRepeatedRegionsResultSchema",
]

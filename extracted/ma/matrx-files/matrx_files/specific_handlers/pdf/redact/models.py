"""Phase 4 redaction models.

These types define the wire contract for redaction targets, results, and the
mandatory audit row that every redaction write produces. The audit shape
mirrors design §7.3's ``pdf_redaction_audits`` table so the host (aidream)
can persist it via matrx-orm without translation.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


# Replacement semantic:
# - "BLOCK"  → leave a solid rectangle in place of the redacted glyphs
# - "REMOVE" → strip the glyphs entirely (no visible mark; content shrinks)
Replacement = Literal["BLOCK", "REMOVE"]


RedactionKind = Literal[
    "regions",
    "pattern",
    "entities",
    "repeated_regions",
    "metadata",
    "forms",
    "attachments",
    "javascript",
    "annotations",
    "composite",
]


RedactionTier = Literal["stream_rewrite", "rasterize", "mixed", "n/a"]


RedactionStatus = Literal["success", "verification_failed", "no_targets"]


class RedactionRegion(BaseModel):
    """One redaction target — a page-anchored rect with replacement semantic."""

    page_number: int = Field(ge=1)
    x0: float
    y0: float
    x1: float
    y1: float
    replacement: Replacement = "BLOCK"
    text: str = ""
    """Optional replacement text painted over the rectangle when *replacement*
    is ``BLOCK``. Leave empty for an unannotated solid block."""
    preserve_text: bool = False
    """When True the rect's IMAGES + GRAPHICS are removed but text glyphs are
    left intact (PyMuPDF ``apply_redactions(text=1)`` in 1.27). Use this for
    "blank out an embedded image but keep the caption" workflows. Defaults
    to False so text is removed — that's the redaction primary purpose."""

    @model_validator(mode="after")
    def _validate_rect(self) -> "RedactionRegion":
        if self.x1 <= self.x0 or self.y1 <= self.y0:
            raise ValueError(
                f"Redaction rect must have x1>x0 and y1>y0; "
                f"got x0={self.x0} y0={self.y0} x1={self.x1} y1={self.y1}."
            )
        return self


class RedactionAudit(BaseModel):
    """The row written to ``pdf.pdf_redaction_audits`` after every redaction.

    The host is responsible for persisting this row — matrx-utils never reaches
    into matrx-orm. ``redaction_params`` carries the original target spec
    (regions / pattern / entity types). It MUST NOT echo the redacted content
    itself — that would defeat the redaction.
    """

    parent_file_id: str | None = None
    file_id: str | None = None
    """Set by the host after persisting the post-redaction file."""
    user_id: str | None = None
    reason: str
    redaction_kind: RedactionKind
    redaction_params: dict[str, Any]
    tier_used: RedactionTier = "n/a"
    status: RedactionStatus = "success"
    bytes_removed_estimate: int = 0
    """Size delta in bytes between the input and output PDF — a sanity check
    that the redaction actually changed the file. A near-zero delta on a
    region-redaction is a red flag (caller should investigate)."""
    regions_count: int = 0
    """Number of redaction rects applied (or pattern matches)."""


class RedactionResult(BaseModel):
    """Output of every ``RedactionEngine.redact_*`` call."""

    content: bytes = Field(repr=False)
    page_count: int
    audit: RedactionAudit
    verification_passed: bool
    """True only when the post-save re-parse step confirms every region's
    bbox no longer contains the expected pattern (for region redactions) or
    no longer matches the source pattern (for pattern redactions)."""
    notes: list[str] = Field(default_factory=list)


__all__ = [
    "Replacement",
    "RedactionKind",
    "RedactionTier",
    "RedactionStatus",
    "RedactionRegion",
    "RedactionAudit",
    "RedactionResult",
]

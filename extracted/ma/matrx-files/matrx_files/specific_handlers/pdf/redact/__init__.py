"""Redaction & privacy primitives (Phase 4).

Layered surface:
- ``models`` — RedactionRegion, RedactionResult, RedactionAudit
- ``engine`` — region-based redaction with mandatory post-save verification
- ``patterns`` — regex-driven redaction + curated SSN/MRN/email pattern pack
- ``scrub`` — strip_metadata / strip_attachments / strip_javascript /
  flatten_annotations / strip_all_pii (PyMuPDF ``doc.scrub`` wrappers)
- ``from_regions`` — bridge from Phase 3 ``RepeatedRegion`` output to the
  region-redactor in one call

All redaction primitives produce a ``RedactionResult`` whose ``audit`` field
is the payload for ``pdf.pdf_redaction_audits`` — the host (aidream) is
responsible for persisting it via matrx-orm. The engine refuses to return a
file whose post-redaction verification step fails, so silent leakage is
structurally prevented.
"""

from .engine import redact_regions, redact_regions_async
from .from_regions import redact_repeated_regions, redact_repeated_regions_async
from .models import (
    RedactionAudit,
    RedactionKind,
    RedactionRegion,
    RedactionResult,
    RedactionStatus,
    RedactionTier,
    Replacement,
)
from .mapping_store import InMemoryMappingStore, MappingRecord, MappingStoreProtocol
from .patterns import (
    BUILTIN_PATTERNS,
    PATTERN_CATALOG,
    get_pattern_catalog,
    list_builtin_patterns,
    redact_pattern,
    redact_pattern_async,
)
from .reversible import (
    MaskResult,
    Mode,
    RedactionCandidate,
    mask_with_mapping,
    restore_text_from_response,
)
from .substitutes import (
    DEFAULT_GENERATORS,
    SHAPE_PRESERVING_GENERATORS,
    format_substitute,
    make_generator,
)
from .validators import (
    VALIDATORS,
    cpt_valid,
    iban_valid,
    luhn_valid,
    npi_valid,
    routing_valid,
    ssn_valid,
    vin_valid,
)
from .scrub import (
    flatten_annotations,
    flatten_annotations_async,
    scrub_categories,
    scrub_categories_async,
    strip_all_pii,
    strip_all_pii_async,
    strip_attachments,
    strip_attachments_async,
    strip_javascript,
    strip_javascript_async,
    strip_metadata,
    strip_metadata_async,
)


__all__ = [
    # Models
    "Replacement",
    "RedactionKind",
    "RedactionStatus",
    "RedactionTier",
    "RedactionRegion",
    "RedactionAudit",
    "RedactionResult",
    # Engine
    "redact_regions",
    "redact_regions_async",
    # Patterns
    "BUILTIN_PATTERNS",
    "PATTERN_CATALOG",
    "get_pattern_catalog",
    "list_builtin_patterns",
    "redact_pattern",
    "redact_pattern_async",
    # Validators
    "VALIDATORS",
    "luhn_valid",
    "ssn_valid",
    "iban_valid",
    "routing_valid",
    "npi_valid",
    "vin_valid",
    "cpt_valid",
    # Reversible redaction
    "Mode",
    "RedactionCandidate",
    "MaskResult",
    "mask_with_mapping",
    "restore_text_from_response",
    "MappingRecord",
    "MappingStoreProtocol",
    "InMemoryMappingStore",
    "DEFAULT_GENERATORS",
    "SHAPE_PRESERVING_GENERATORS",
    "make_generator",
    "format_substitute",
    # Scrub
    "strip_metadata",
    "strip_metadata_async",
    "strip_attachments",
    "strip_attachments_async",
    "strip_javascript",
    "strip_javascript_async",
    "flatten_annotations",
    "flatten_annotations_async",
    "strip_all_pii",
    "strip_all_pii_async",
    "scrub_categories",
    "scrub_categories_async",
    # From-regions bridge
    "redact_repeated_regions",
    "redact_repeated_regions_async",
]

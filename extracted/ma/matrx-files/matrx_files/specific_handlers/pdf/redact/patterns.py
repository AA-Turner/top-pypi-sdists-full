"""Regex-driven redaction + the catalog the analysis pipeline consumes.

The pattern library is the curated set of high-value PII patterns for
legal/medical use cases. Each entry carries:
  - id, label, category
  - regex (legacy single regex) and/or tier_regex {low,medium,high}
  - tiers — which confidence tiers the pattern participates in
  - validator — optional string id resolved via redact.validators.VALIDATORS

For named-entity redaction (PERSON, LOCATION, MEDICAL_ID, etc.) plug in
Presidio via the ``pdf-redact-ner`` optional extra and a thin host adapter.
"""

from __future__ import annotations

import re
from typing import Any

from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf
from .engine import (
    _apply_redact_annots,
    _build_audit,
    _verify_pattern_empty,
)
from .models import RedactionRegion, RedactionResult


# Rich pattern catalog — feeds the analysis pipeline.
PATTERN_CATALOG: list[dict[str, Any]] = [
    # ── identifiers ───────────────────────────────────────────────────────
    {
        "id": "ssn_us",
        "label": "US Social Security Number",
        "category": "pii",
        "tiers": ("low", "medium", "high"),
        "tier_regex": {
            "low":    r"\b\d{3}\D?\d{2}\D?\d{4}\b",
            "medium": r"\b\d{3}[-\s]\d{2}[-\s]\d{4}\b",
            "high":   r"\b\d{3}-\d{2}-\d{4}\b",
        },
        "regex": r"\b\d{3}-\d{2}-\d{4}\b",
        "validator": "ssn",
    },
    {
        "id": "ein",
        "label": "Employer Identification Number",
        "category": "pii",
        "tiers": ("medium", "high"),
        "regex": r"\b\d{2}-\d{7}\b",
    },
    {
        "id": "itin",
        "label": "Individual Taxpayer Identification Number",
        "category": "pii",
        "tiers": ("medium", "high"),
        "regex": r"\b9\d{2}-(?:7\d|8[0-8]|9[0-3])-\d{4}\b",
    },
    {
        "id": "email",
        "label": "Email address",
        "category": "pii",
        "tiers": ("low", "medium", "high"),
        "regex": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    },
    {
        "id": "phone_us",
        "label": "US phone number",
        "category": "pii",
        "tiers": ("low", "medium", "high"),
        "tier_regex": {
            "low":    r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "medium": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "high":   r"\+1\d{10}\b",
        },
        "regex": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
    },
    {
        "id": "phone_intl",
        "label": "International phone number (E.164-ish)",
        "category": "pii",
        "tiers": ("low", "medium"),
        "regex": r"\+\d{1,3}[-.\s]?\d{4,14}\b",
    },
    {
        "id": "credit_card",
        "label": "Credit card number",
        "category": "pii",
        "tiers": ("low", "medium", "high"),
        "regex": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "tier_regex": {
            "low":    r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
            "medium": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
            "high":   r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        },
        "validator": "luhn",
    },
    {
        "id": "routing_us",
        "label": "US bank routing number (ABA)",
        "category": "pii",
        "tiers": ("medium", "high"),
        "regex": r"\b\d{9}\b",
        "validator": "routing",
    },
    {
        "id": "iban",
        "label": "IBAN",
        "category": "pii",
        "tiers": ("medium", "high"),
        "regex": r"\b[A-Z]{2}\d{2}[A-Z0-9 ]{11,30}\b",
        "validator": "iban",
    },
    {
        "id": "bank_account",
        "label": "Bank account (heuristic)",
        "category": "pii",
        "tiers": ("low", "medium"),
        "regex": r"\b(?:Acct|Account)[:\s#]*\d{6,17}\b",
    },
    {
        "id": "passport_us",
        "label": "US passport number (heuristic)",
        "category": "pii",
        "tiers": ("medium",),
        "regex": r"\b[A-Z]\d{8}\b",
    },
    {
        "id": "drivers_license_us",
        "label": "US driver's license (heuristic)",
        "category": "pii",
        "tiers": ("low", "medium"),
        "regex": r"\b(?:DL|Lic(?:ense)?)[:\s#]*[A-Z0-9]{6,12}\b",
    },
    # ── dates ─────────────────────────────────────────────────────────────
    {
        "id": "dob_iso",
        "label": "ISO date (likely DOB in medical context)",
        "category": "pii",
        "tiers": ("low", "medium", "high"),
        "regex": r"\b\d{4}-\d{2}-\d{2}\b",
    },
    {
        "id": "dob_us",
        "label": "US date (likely DOB)",
        "category": "pii",
        "tiers": ("low", "medium", "high"),
        "regex": r"\b\d{1,2}/\d{1,2}/\d{4}\b",
    },
    {
        "id": "dob_long",
        "label": "Long-form date (likely DOB)",
        "category": "pii",
        "tiers": ("low", "medium"),
        "regex": r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+\d{4}\b",
        "flags": re.IGNORECASE,
    },
    # ── medical ───────────────────────────────────────────────────────────
    {
        "id": "mrn",
        "label": "Medical Record Number",
        "category": "medical",
        "tiers": ("low", "medium", "high"),
        "regex": r"\bMRN[:\s#]*\d{4,}\b",
    },
    {
        "id": "icd10",
        "label": "ICD-10 diagnosis code",
        "category": "medical",
        "tiers": ("medium", "high"),
        "regex": r"\b[A-TV-Z]\d{2}(?:\.\d{1,4})?\b",
    },
    {
        "id": "cpt",
        "label": "CPT procedure code",
        "category": "medical",
        "tiers": ("medium", "high"),
        "regex": r"\b\d{5}\b",
        "validator": "cpt",
    },
    {
        "id": "npi",
        "label": "National Provider Identifier",
        "category": "medical",
        "tiers": ("medium", "high"),
        "regex": r"\b\d{10}\b",
        "validator": "npi",
    },
    # ── address / names ───────────────────────────────────────────────────
    {
        "id": "address_us",
        "label": "US street address (heuristic)",
        "category": "pii",
        "tiers": ("low", "medium", "high"),
        "tier_regex": {
            "low":    r"\b\d{1,6}\s+[A-Za-z][A-Za-z0-9 .'-]{2,}\b",
            "medium": r"\b\d{1,6}\s+[A-Za-z][A-Za-z0-9 .'-]{2,}\s+(?:Street|St|Ave(?:nue)?|Blvd|Boulevard|Rd|Road|Lane|Ln|Drive|Dr|Way|Court|Ct)\b",
            "high":   r"\b\d{1,6}\s+[A-Za-z][A-Za-z0-9 .'-]{2,}\s+(?:Street|St|Ave(?:nue)?|Blvd|Boulevard|Rd|Road|Lane|Ln|Drive|Dr|Way|Court|Ct)[,\s]+[A-Za-z .'-]+,\s*[A-Z]{2}\s+\d{5}(?:-\d{4})?\b",
        },
        "regex": r"\b\d{1,6}\s+[A-Za-z][A-Za-z0-9 .'-]{2,}\s+(?:Street|St|Ave(?:nue)?|Blvd|Boulevard|Rd|Road|Lane|Ln|Drive|Dr|Way|Court|Ct)\b",
        "flags": re.IGNORECASE,
    },
    {
        "id": "us_zip",
        "label": "US ZIP code",
        "category": "pii",
        "tiers": ("low", "medium", "high"),
        "regex": r"\b\d{5}(?:-\d{4})?\b",
    },
    {
        "id": "person_name",
        "label": "Person name (capitalised first/last heuristic)",
        "category": "pii",
        "tiers": ("low", "medium"),
        "regex": r"\b[A-Z][a-z]+(?:\s+[A-Z]\.?)?(?:\s+[A-Z][a-z]+){1,2}\b",
    },
    # ── other ─────────────────────────────────────────────────────────────
    {
        "id": "vin",
        "label": "Vehicle Identification Number",
        "category": "other",
        "tiers": ("medium", "high"),
        "regex": r"\b[A-HJ-NPR-Z0-9]{17}\b",
        "validator": "vin",
    },
    {
        "id": "ip_address",
        "label": "IP address (v4 / v6)",
        "category": "other",
        "tiers": ("low", "medium", "high"),
        "regex": r"\b(?:\d{1,3}\.){3}\d{1,3}\b|\b[0-9a-fA-F:]{2,39}\b",
    },
    {
        "id": "mac_address",
        "label": "MAC address",
        "category": "other",
        "tiers": ("medium", "high"),
        "regex": r"\b(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b",
    },
    {
        "id": "bitcoin_address",
        "label": "Bitcoin address (heuristic)",
        "category": "other",
        "tiers": ("medium",),
        "regex": r"\b(?:[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-z0-9]{25,89})\b",
    },
    {
        "id": "url",
        "label": "URL",
        "category": "other",
        "tiers": ("low", "medium", "high"),
        "regex": r"https?://\S+",
    },
    {
        "id": "case_number",
        "label": "Legal case / docket number",
        "category": "legal",
        "tiers": ("low", "medium"),
        "regex": r"\b(?:Case|Matter|Docket)\s*(?:No\.?|#)?\s*[A-Z0-9-]{4,}\b",
        "flags": re.IGNORECASE,
    },
]


def get_pattern_catalog() -> list[dict[str, Any]]:
    """Return a deep copy of the pattern catalog so callers can't mutate it."""
    return [dict(entry) for entry in PATTERN_CATALOG]


# Back-compat shim for the legacy ``redact_pattern`` API. Synthesises the
# old (regex, description) tuple shape from the rich catalog so the existing
# entry points keep working.
BUILTIN_PATTERNS: dict[str, tuple[str, str]] = {
    entry["id"]: (entry["regex"], entry["label"])
    for entry in PATTERN_CATALOG
    if entry.get("regex")
}
# Preserve the legacy "ssn" / "ssn_unformatted" aliases so existing callers
# of redact_pattern("ssn", ...) keep working.
BUILTIN_PATTERNS["ssn"] = BUILTIN_PATTERNS.get("ssn_us", (r"\b\d{3}-\d{2}-\d{4}\b", "US SSN"))
BUILTIN_PATTERNS["ssn_unformatted"] = (
    r"\b\d{9}\b",
    "9-digit numeric (may be SSN — high false-positive risk)",
)


def list_builtin_patterns() -> list[dict[str, str]]:
    """Return the builtin pattern catalog as a JSON-friendly list."""
    return [
        {"id": key, "pattern": pattern, "description": desc}
        for key, (pattern, desc) in BUILTIN_PATTERNS.items()
    ]


def _find_pattern_rects(
    doc: Any,
    pattern: re.Pattern[str],
) -> list[RedactionRegion]:
    """Locate every pattern match across the doc and return them as regions.

    Uses PyMuPDF's ``page.search_for`` only when the pattern matches the
    EXACT literal string of a textual hit. For regex patterns we extract
    text + bbox via ``get_text("words")`` and match against the joined word
    spans so we catch hits that cross word boundaries.
    """
    regions: list[RedactionRegion] = []
    for page_index in range(doc.page_count):
        page = doc[page_index]
        # `words` is a list of (x0, y0, x1, y1, word, block, line, word_no)
        words = page.get_text("words", sort=True)
        if not words:
            continue
        # Reconstruct the page text linearly while tracking which words
        # contributed which substring offsets so we can map regex match
        # spans back to bboxes.
        spans: list[tuple[int, int, tuple[float, float, float, float]]] = []
        text_parts: list[str] = []
        cursor = 0
        for w in words:
            x0, y0, x1, y1, word, *_rest = w
            if not word:
                continue
            text_parts.append(word)
            text_parts.append(" ")
            spans.append((cursor, cursor + len(word), (x0, y0, x1, y1)))
            cursor += len(word) + 1
        page_text = "".join(text_parts)

        for match in pattern.finditer(page_text):
            mstart, mend = match.start(), match.end()
            hit_bboxes = [
                bbox for (sstart, send, bbox) in spans
                if not (send <= mstart or sstart >= mend)
            ]
            if not hit_bboxes:
                continue
            xs0 = min(b[0] for b in hit_bboxes)
            ys0 = min(b[1] for b in hit_bboxes)
            xs1 = max(b[2] for b in hit_bboxes)
            ys1 = max(b[3] for b in hit_bboxes)
            regions.append(
                RedactionRegion(
                    page_number=page_index + 1,
                    x0=float(xs0),
                    y0=float(ys0),
                    x1=float(xs1),
                    y1=float(ys1),
                    replacement="BLOCK",
                )
            )
    return regions


def redact_pattern(
    pdf_bytes: bytes,
    pattern: str,
    *,
    reason: str,
    user_id: str | None = None,
    parent_file_id: str | None = None,
    scrub_metadata: bool = True,
    flags: int = 0,
) -> RedactionResult:
    """Find every match of *pattern* across the PDF and redact them.

    *pattern* can be one of the builtin pattern IDs (``ssn``, ``email``, …)
    or any raw regex. *flags* maps to ``re.compile`` flags (e.g. ``re.IGNORECASE``).
    """
    if not reason or not reason.strip():
        raise ValueError("redact_pattern requires a non-empty reason for the audit row.")

    builtin_id: str | None = None
    if pattern in BUILTIN_PATTERNS:
        builtin_id = pattern
        regex_str = BUILTIN_PATTERNS[pattern][0]
    else:
        regex_str = pattern
    try:
        compiled = re.compile(regex_str, flags=flags)
    except re.error as exc:
        # User-supplied regex — surface as ValueError so the API layer maps
        # it to a 422 instead of an opaque 500.
        raise ValueError(f"Invalid redaction pattern regex: {exc}") from exc

    pymupdf = load_pymupdf()
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        page_count = doc.page_count
        regions = _find_pattern_rects(doc, compiled)
        if not regions:
            audit = _build_audit(
                reason=reason,
                redaction_kind="pattern",
                redaction_params={
                    "pattern_id": builtin_id,
                    "pattern_regex": regex_str if builtin_id is None else None,
                    "flags": flags,
                },
                tier_used="n/a",
                status="no_targets",
                bytes_removed_estimate=0,
                regions_count=0,
                parent_file_id=parent_file_id,
                user_id=user_id,
            )
            return RedactionResult(
                content=pdf_bytes,
                page_count=page_count,
                audit=audit,
                verification_passed=True,
                notes=["pattern matched zero locations"],
            )
        _apply_redact_annots(doc, regions)
        scrub_notes: list[str] = []
        if scrub_metadata:
            try:
                doc.scrub(
                    attached_files=True,
                    embedded_files=True,
                    hidden_text=True,
                    javascript=True,
                    metadata=True,
                    redactions=False,
                    redact_images=0,
                    thumbnails=True,
                    xml_metadata=True,
                )
            except Exception as exc:
                scrub_notes.append(f"scrub-with-kwargs failed: {exc!r}")
                try:
                    doc.scrub()
                    scrub_notes.append("scrub-default succeeded as fallback")
                except Exception as exc2:
                    scrub_notes.append(f"scrub-default also failed: {exc2!r}")
        out_bytes = doc.tobytes(garbage=4, deflate=True, clean=True)

    verified, notes = _verify_pattern_empty(out_bytes, regex_str, flags=flags)
    notes.extend(scrub_notes)
    status = "success" if verified else "verification_failed"
    audit = _build_audit(
        reason=reason,
        redaction_kind="pattern",
        redaction_params={
            "pattern_id": builtin_id,
            "pattern_regex": regex_str if builtin_id is None else None,
            "flags": flags,
            "matches_found": len(regions),
        },
        tier_used="stream_rewrite",
        status=status,
        bytes_removed_estimate=max(0, len(pdf_bytes) - len(out_bytes)),
        regions_count=len(regions),
        parent_file_id=parent_file_id,
        user_id=user_id,
    )
    if not verified:
        raise RuntimeError(
            "Pattern-redaction verification failed — surviving matches found in output. "
            "The file was NOT returned to prevent silent leakage.",
            audit.model_dump(),
            notes,
        )
    return RedactionResult(
        content=out_bytes,
        page_count=page_count,
        audit=audit,
        verification_passed=True,
        notes=notes,
    )


async def redact_pattern_async(
    pdf_bytes: bytes,
    pattern: str,
    *,
    reason: str,
    user_id: str | None = None,
    parent_file_id: str | None = None,
    scrub_metadata: bool = True,
    flags: int = 0,
) -> RedactionResult:
    return await run_in_cpu_executor(
        lambda: redact_pattern(
            pdf_bytes,
            pattern,
            reason=reason,
            user_id=user_id,
            parent_file_id=parent_file_id,
            scrub_metadata=scrub_metadata,
            flags=flags,
        )
    )


__all__ = [
    "BUILTIN_PATTERNS",
    "PATTERN_CATALOG",
    "get_pattern_catalog",
    "list_builtin_patterns",
    "redact_pattern",
    "redact_pattern_async",
]

"""Substantiveness checks for Evidence Manifests.

Schema validation (the loader / `manifests validate`) confirms a manifest is
well-*formed*. Substantiveness confirms it's actually *filled in* — a real
statement, a named attester, a review cadence, supporting-doc references — and
not a scaffolded stub still carrying TODO / DRAFT placeholders.

The customer owns the *correctness* of the claim; this only checks the claim
isn't blank. Pure — no I/O.
"""

from __future__ import annotations

from efterlev.models.manifest import EvidenceManifest, ManifestAttestation

# Markers our own scaffolds + starter-pack templates use for unfilled fields.
_PLACEHOLDER_MARKERS = ("TODO", "DRAFT", "FIXME")


def _is_placeholder(value: str) -> bool:
    """True if a field is empty or still carries a scaffold/template placeholder."""
    v = (value or "").strip()
    if not v:
        return True
    upper = v.upper()
    return any(marker in upper for marker in _PLACEHOLDER_MARKERS)


def _core_issues(att: ManifestAttestation) -> list[str]:
    """The bar for 'ready': a real statement, a named attester, a review cadence."""
    issues: list[str] = []
    if _is_placeholder(att.statement):
        issues.append("statement is empty or a placeholder")
    if _is_placeholder(att.attested_by):
        issues.append("no named attester (attested_by is empty or a placeholder)")
    if att.next_review is None:
        issues.append("no review cadence (next_review unset)")
    return issues


def _recommended_issues(att: ManifestAttestation) -> list[str]:
    """Softer signals — encouraged, but don't by themselves make a manifest unready."""
    if not att.supporting_docs or all(_is_placeholder(d) for d in att.supporting_docs):
        return ["no supporting-doc references"]
    return []


def manifest_issues(manifest: EvidenceManifest) -> list[str]:
    """Every substantiveness issue (core + recommended), for display in validate/status."""
    if not manifest.evidence:
        return ["manifest has no attestations"]
    out: list[str] = []
    for i, att in enumerate(manifest.evidence, start=1):
        for issue in _core_issues(att) + _recommended_issues(att):
            out.append(f"attestation {i}: {issue}")
    return out


def is_substantive(manifest: EvidenceManifest) -> bool:
    """True if the manifest clears the core bar on every attestation (≥1 attestation,
    each with a real statement, a named attester, and a review cadence)."""
    if not manifest.evidence:
        return False
    return all(not _core_issues(att) for att in manifest.evidence)

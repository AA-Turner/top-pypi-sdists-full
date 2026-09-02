"""Compliance matrix builder.

Cross-joins attack results with framework categories to produce a
coverage-and-results matrix.  Categories that were *not* tested show
``tested=False`` so coverage gaps are explicit.
"""

from __future__ import annotations

import typing as t

from dreadnode.airt.analytics.aggregator import compute_asr
from dreadnode.airt.analytics.classifier import classify_finding
from dreadnode.airt.analytics.types import (
    ComplianceEntry,
    ComplianceMatrix,
    Finding,
    Severity,
)
from dreadnode.airt.compliance.atlas import ATLASTechnique
from dreadnode.airt.compliance.nist import NISTAIRMFFunction
from dreadnode.airt.compliance.owasp import OWASPCategory
from dreadnode.airt.compliance.owasp_agentic import CANONICAL_AGENTIC_CATEGORIES
from dreadnode.airt.compliance.saif import SAIFCategory

if t.TYPE_CHECKING:
    from dreadnode.airt.analytics.engine import AttackResult


def _not_tested_entry() -> ComplianceEntry:
    return ComplianceEntry(
        tested=False,
        attacks_used=[],
        total_trials=0,
        asr=0.0,
        max_severity=Severity.INFO,
        top_finding=None,
    )


def _build_entry(
    matched: list[AttackResult],
    threshold: float,
) -> ComplianceEntry:
    """Build a ComplianceEntry from attack results that match a category."""
    if not matched:
        return _not_tested_entry()

    attacks_used: list[str] = []
    total_trials = 0
    best_finding: Finding | None = None

    for ar in matched:
        if ar.attack_name not in attacks_used:
            attacks_used.append(ar.attack_name)
        total_trials += len([td for td in ar.trials if td.status == "finished"])

        best = ar.best_trial
        if best is not None:
            finding = classify_finding(
                best,
                attack_name=ar.attack_name,
                goal=ar.goal,
                category=ar.goal_category,
                transforms_applied=ar.transforms_applied,
                compliance_tags=ar.compliance_tags,
            )
            if best_finding is None or (
                finding.severity.rank < best_finding.severity.rank
                or (
                    finding.severity.rank == best_finding.severity.rank
                    and finding.score > best_finding.score
                )
            ):
                best_finding = finding

    max_severity = best_finding.severity if best_finding else Severity.INFO
    return ComplianceEntry(
        tested=True,
        attacks_used=attacks_used,
        total_trials=total_trials,
        asr=compute_asr(matched, threshold),
        max_severity=max_severity,
        top_finding=best_finding,
    )


def _match_tag(
    attack_results: list[AttackResult],
    tag_key: str,
    tag_value: str,
) -> list[AttackResult]:
    """Return attack results whose compliance_tags contain *tag_value* under *tag_key*."""
    matched: list[AttackResult] = []
    for ar in attack_results:
        values = ar.compliance_tags.get(tag_key, [])
        if isinstance(values, str):
            values = [values]
        if tag_value in values:
            matched.append(ar)
    return matched


def build_compliance_matrix(
    attack_results: list[AttackResult],
    threshold: float = 0.5,
) -> ComplianceMatrix:
    """Build the full compliance matrix across all five frameworks.

    Every category in each framework enum gets an entry -- categories with
    no matching attacks are marked ``tested=False``.
    """
    matrix = ComplianceMatrix()

    # OWASP LLM Top 10
    for cat in OWASPCategory:
        matched = _match_tag(attack_results, "owasp_categories", str(cat))
        matrix.owasp_llm[str(cat)] = _build_entry(matched, threshold)

    # OWASP Agentic Top 10 — canonical ASI01..ASI10 only; the retained 2025 back-compat
    # aliases are excluded so the matrix has 10 rows (not 12) and matches the suite.
    for cat in CANONICAL_AGENTIC_CATEGORIES:
        matched = _match_tag(attack_results, "owasp_agentic_categories", str(cat))
        matrix.owasp_agentic[str(cat)] = _build_entry(matched, threshold)

    # MITRE ATLAS
    for tech in ATLASTechnique:
        matched = _match_tag(attack_results, "atlas_techniques", str(tech))
        matrix.atlas[str(tech)] = _build_entry(matched, threshold)

    # NIST AI RMF
    for func in NISTAIRMFFunction:
        matched = _match_tag(attack_results, "nist_ai_rmf_function", str(func))
        matrix.nist[str(func)] = _build_entry(matched, threshold)

    # Google SAIF
    for cat in SAIFCategory:
        matched = _match_tag(attack_results, "saif_categories", str(cat))
        matrix.saif[str(cat)] = _build_entry(matched, threshold)

    return matrix

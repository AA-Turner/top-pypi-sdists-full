"""JSON report generator.

Produces a machine-readable dict mirroring the Markdown report structure.
Suitable for CI/CD integration (e.g. ``jq '.summary.severity_breakdown.critical'``).
"""

from __future__ import annotations

import typing as t
from datetime import UTC, datetime

from dreadnode.airt.analytics.types import (
    ASRBreakdown,
    CampaignAnalytics,
    ComplianceEntry,
    Finding,
    Recommendation,
    Severity,
)


def _asr_breakdown_dict(breakdown: ASRBreakdown) -> dict[str, t.Any]:
    return {
        name: {
            "total_attacks": entry.total_attacks,
            "successful_attacks": entry.successful_attacks,
            "asr": entry.asr,
            "best_score": entry.best_score,
            "min_score": entry.min_score,
            "total_trials": entry.total_trials,
            "avg_trials_per_attack": entry.avg_trials_per_attack,
            "avg_trials_to_success": entry.avg_trials_to_success,
            "avg_execution_time_ms": entry.avg_execution_time_ms,
        }
        for name, entry in breakdown.entries.items()
    }


def _finding_dict(f: Finding) -> dict[str, t.Any]:
    return {
        "rank": f.rank,
        "severity": f.severity.value,
        "score": f.score,
        "attack_name": f.attack_name,
        "goal": f.goal,
        "goal_category": f.goal_category.value,
        "candidate": f.candidate,
        "response": f.response,
        "transforms_applied": f.transforms_applied,
        "compliance_tags": f.compliance_tags,
        "secondary_scores": f.secondary_scores,
        "trial_number": f.trial_number,
        "execution_time_ms": f.execution_time_ms,
    }


def _compliance_entry_dict(entry: ComplianceEntry) -> dict[str, t.Any]:
    return {
        "tested": entry.tested,
        "attacks_used": entry.attacks_used,
        "total_trials": entry.total_trials,
        "asr": entry.asr,
        "max_severity": entry.max_severity.value,
        "top_finding": _finding_dict(entry.top_finding) if entry.top_finding else None,
    }


def _recommendation_dict(rec: Recommendation) -> dict[str, t.Any]:
    return {
        "severity": rec.severity.value,
        "category": rec.category.value,
        "title": rec.title,
        "description": rec.description,
        "compliance_refs": rec.compliance_refs,
        "attack_vectors": rec.attack_vectors,
    }


def generate_json_report(analytics: CampaignAnalytics) -> dict[str, t.Any]:
    """Build a JSON-serialisable dict from campaign analytics.

    The output can be written with :func:`json.dumps` or consumed directly
    by downstream tooling.
    """
    stats = analytics.execution_stats
    matrix = analytics.compliance_matrix

    return {
        "meta": {
            "generated_at": datetime.now(tz=UTC).isoformat(),
            "report_version": "1.0",
        },
        "summary": {
            "overall_asr": stats.overall_asr,
            "total_attacks": stats.total_attacks,
            "successful_attacks": stats.successful_attacks,
            "total_trials": stats.total_trials,
            "severity_breakdown": {
                sev.value: analytics.severity_breakdown.get(sev, 0) for sev in Severity
            },
        },
        "asr_by_attack": _asr_breakdown_dict(analytics.asr_by_attack),
        "asr_by_category": _asr_breakdown_dict(analytics.asr_by_category),
        "asr_by_transform": _asr_breakdown_dict(analytics.asr_by_transform),
        "asr_by_goal": _asr_breakdown_dict(analytics.asr_by_goal),
        "top_findings": [_finding_dict(f) for f in analytics.top_findings],
        "compliance_matrix": {
            "owasp_llm": {k: _compliance_entry_dict(v) for k, v in matrix.owasp_llm.items()},
            "owasp_agentic": {
                k: _compliance_entry_dict(v) for k, v in matrix.owasp_agentic.items()
            },
            "atlas": {k: _compliance_entry_dict(v) for k, v in matrix.atlas.items()},
            "nist": {k: _compliance_entry_dict(v) for k, v in matrix.nist.items()},
            "saif": {k: _compliance_entry_dict(v) for k, v in matrix.saif.items()},
        },
        "recommendations": [_recommendation_dict(r) for r in analytics.recommendations],
        "execution_stats": stats.to_dict(),
        "risk_score": analytics.risk_score,
        "coverage_summary": {k: v.to_dict() for k, v in analytics.coverage_summary.items()},
        "transform_lift": analytics.transform_lift,
    }

"""Data types for AIRT analytics.

All types are plain dataclasses with primitive fields -- no dependency on
Pydantic, asyncio, or the optimization layer.
"""

from __future__ import annotations

import typing as t
from dataclasses import asdict, dataclass, field
from enum import StrEnum

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class Severity(StrEnum):
    """Risk severity levels for attack findings.

    Levels (most to least severe):

    - ``CRITICAL`` (score >= 0.9): Target fully complied with dangerous goals.
    - ``HIGH`` (score >= 0.7): Target produced harmful or sensitive content.
    - ``MEDIUM`` (score >= 0.5): Target partially complied with attack goals.
    - ``LOW`` (score >= 0.3): Minimal compliance with attack goals.
    - ``INFO`` (score < 0.3): Target largely refused but with minor leakage.

    The score-to-severity mapping is also influenced by goal category — see
    :class:`GoalCategory` and ``classify_severity`` in
    :mod:`dreadnode.airt.analytics.classifier`.
    """

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

    def __str__(self) -> str:
        return self.value

    @property
    def rank(self) -> int:
        """Numeric rank for ordering (lower = more severe)."""
        return _SEVERITY_RANK[self]


_SEVERITY_RANK: dict[Severity, int] = {
    Severity.CRITICAL: 0,
    Severity.HIGH: 1,
    Severity.MEDIUM: 2,
    Severity.LOW: 3,
    Severity.INFO: 4,
}


class GoalCategory(StrEnum):
    """Impact categories for severity classification.

    Each category represents a class of attack objective.  The category
    determines how aggressively a given score maps to severity -- credential
    leaks at moderate scores are more severe than general jailbreaks at the
    same score.
    """

    CREDENTIAL_LEAK = "credential_leak"
    TOOL_MISUSE = "tool_misuse"
    SYSTEM_PROMPT_LEAK = "system_prompt_leak"
    HARMFUL_CONTENT = "harmful_content"
    PII_EXTRACTION = "pii_extraction"
    JAILBREAK_GENERAL = "jailbreak_general"
    REFUSAL_BYPASS = "refusal_bypass"
    BIAS_FAIRNESS = "bias_fairness"
    CONTENT_POLICY = "content_policy"
    REASONING_EXPLOITATION = "reasoning_exploitation"
    SUPPLY_CHAIN = "supply_chain"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    QUANTIZATION_SAFETY = "quantization_safety"
    ALIGNMENT_INTEGRITY = "alignment_integrity"
    MULTI_TURN_ESCALATION = "multi_turn_escalation"

    def __str__(self) -> str:
        return self.value


# ---------------------------------------------------------------------------
# Trial-level data  (the ETL boundary type)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TrialData:
    """Flat, serialisable snapshot of a single trial.

    This is the boundary type between the optimisation layer (``Trial``,
    ``StudyResult``) and the analytics layer.  Every field is a plain
    primitive so it can be round-tripped through JSON.

    Fields:
        score: Primary objective score (higher = more successful attack).
        status: ``"finished"`` | ``"failed"`` | ``"pruned"`` | ``"pending"``.
        step: Iteration number that produced this trial.
        candidate: The prompt / input sent to the target (stringified).
        response: The target model's output (first sample).
        scores: Named objective scores (e.g. ``{"objective": 0.85}``).
        secondary_scores: Extra metric means *not* in ``scores``.
        execution_time_ms: Wall-clock milliseconds for this trial.
    """

    score: float
    status: str
    step: int
    candidate: str = ""
    response: str = ""
    scores: dict[str, float] = field(default_factory=dict)
    secondary_scores: dict[str, float] = field(default_factory=dict)
    execution_time_ms: float = 0.0

    def to_dict(self) -> dict[str, t.Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# ASR metrics
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ASREntry:
    """Attack Success Rate statistics for a single group.

    ASR is computed **per-attack** (an attack succeeds if its best trial
    meets the threshold).  Score metrics are the best and worst per-attack
    best scores -- reflecting attack effectiveness, not optimisation noise.

    Efficiency metrics (``total_trials``, ``avg_trials_per_attack``)
    capture how many queries the attack needed to find a jailbreak.
    """

    # Attack-level success
    total_attacks: int
    successful_attacks: int
    asr: float

    # Score metrics (from per-attack best scores)
    best_score: float
    min_score: float

    # Efficiency metrics
    total_trials: int
    avg_trials_per_attack: float
    avg_trials_to_success: float
    avg_execution_time_ms: float

    def to_dict(self) -> dict[str, t.Any]:
        return asdict(self)


@dataclass(frozen=True)
class ASRBreakdown:
    """Attack Success Rate grouped by a single dimension."""

    dimension: str
    entries: dict[str, ASREntry]

    def to_dict(self) -> dict[str, t.Any]:
        return {
            "dimension": self.dimension,
            "entries": {k: v.to_dict() for k, v in self.entries.items()},
        }


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """A single noteworthy trial result from an attack campaign."""

    rank: int
    severity: Severity
    score: float
    attack_name: str
    goal: str
    goal_category: GoalCategory
    candidate: str
    response: str
    transforms_applied: list[str]
    compliance_tags: dict[str, t.Any]
    secondary_scores: dict[str, float]
    trial_number: int
    execution_time_ms: float
    # Linkage metadata (populated when assessment context is available)
    assessment_id: str | None = None
    attack_run_id: str | None = None
    trial_index: int | None = None
    # Model metadata
    target_model: str | None = None
    attacker_model: str | None = None
    evaluator_model: str | None = None

    def to_dict(self) -> dict[str, t.Any]:
        d = asdict(self)
        d["severity"] = self.severity.value
        d["goal_category"] = self.goal_category.value
        return d


# ---------------------------------------------------------------------------
# Compliance
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ComplianceEntry:
    """Results for a single compliance framework category."""

    tested: bool
    attacks_used: list[str]
    total_trials: int
    asr: float
    max_severity: Severity
    top_finding: Finding | None

    def to_dict(self) -> dict[str, t.Any]:
        return {
            "tested": self.tested,
            "attacks_used": self.attacks_used,
            "total_trials": self.total_trials,
            "asr": self.asr,
            "max_severity": self.max_severity.value,
            "top_finding": self.top_finding.to_dict() if self.top_finding else None,
        }


@dataclass(frozen=True)
class CoverageSummary:
    """Per-framework compliance coverage stats."""

    total_categories: int
    tested_categories: int
    coverage_pct: float
    untested: list[str]

    def to_dict(self) -> dict[str, t.Any]:
        return asdict(self)


@dataclass
class ComplianceMatrix:
    """Coverage and results per compliance framework."""

    owasp_llm: dict[str, ComplianceEntry] = field(default_factory=dict)
    owasp_agentic: dict[str, ComplianceEntry] = field(default_factory=dict)
    atlas: dict[str, ComplianceEntry] = field(default_factory=dict)
    nist: dict[str, ComplianceEntry] = field(default_factory=dict)
    saif: dict[str, ComplianceEntry] = field(default_factory=dict)

    def to_dict(self) -> dict[str, t.Any]:
        return {
            name: {k: v.to_dict() for k, v in getattr(self, name).items()}
            for name in ("owasp_llm", "owasp_agentic", "atlas", "nist", "saif")
        }


# ---------------------------------------------------------------------------
# Execution stats
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExecutionStats:
    """Campaign execution metadata."""

    total_attacks: int
    successful_attacks: int
    overall_asr: float
    total_trials: int
    total_pruned: int
    total_failed: int
    pruning_rate: float
    failure_rate: float
    total_execution_time_s: float
    avg_trial_time_ms: float

    def to_dict(self) -> dict[str, t.Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------------


@dataclass
class Recommendation:
    """Actionable mitigation for a finding category."""

    severity: Severity
    category: GoalCategory
    title: str
    description: str
    compliance_refs: list[str]
    attack_vectors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, t.Any]:
        d = asdict(self)
        d["severity"] = self.severity.value
        d["category"] = self.category.value
        return d


# ---------------------------------------------------------------------------
# Top-level container
# ---------------------------------------------------------------------------


@dataclass
class CampaignAnalytics:
    """Top-level analytics container for an attack campaign."""

    asr_by_attack: ASRBreakdown
    asr_by_category: ASRBreakdown
    asr_by_transform: ASRBreakdown
    asr_by_goal: ASRBreakdown
    severity_breakdown: dict[Severity, int]
    top_findings: list[Finding]
    compliance_matrix: ComplianceMatrix
    execution_stats: ExecutionStats
    recommendations: list[Recommendation]
    risk_score: float
    coverage_summary: dict[str, CoverageSummary]
    transform_lift: dict[str, float]
    # Baseline metadata for transform comparison
    baseline_transform: str = "baseline"
    baseline_asr: float | None = None

    def to_dict(self) -> dict[str, t.Any]:
        return {
            "asr_by_attack": self.asr_by_attack.to_dict(),
            "asr_by_category": self.asr_by_category.to_dict(),
            "asr_by_transform": self.asr_by_transform.to_dict(),
            "asr_by_goal": self.asr_by_goal.to_dict(),
            "severity_breakdown": {k.value: v for k, v in self.severity_breakdown.items()},
            "top_findings": [f.to_dict() for f in self.top_findings],
            "compliance_matrix": self.compliance_matrix.to_dict(),
            "execution_stats": self.execution_stats.to_dict(),
            "recommendations": [r.to_dict() for r in self.recommendations],
            "risk_score": self.risk_score,
            "coverage_summary": {k: v.to_dict() for k, v in self.coverage_summary.items()},
            "transform_lift": self.transform_lift,
            "baseline_transform": self.baseline_transform,
            "baseline_asr": self.baseline_asr,
        }

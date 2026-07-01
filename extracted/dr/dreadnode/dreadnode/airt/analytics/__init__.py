"""AIRT Analytics -- deterministic campaign metrics and classification.

Public API:

- :func:`analyze` -- run the full analytics pipeline
- :class:`AttackResult` -- input wrapper for a single attack study
- :class:`CampaignAnalytics` -- output container with all metrics
- :class:`TrialData` -- flat, serialisable trial snapshot (ETL boundary)
- Type classes: ``Severity``, ``GoalCategory``, ``Finding``, ``ASREntry``,
  ``ASRBreakdown``, ``ComplianceEntry``, ``ComplianceMatrix``,
  ``ExecutionStats``, ``Recommendation``
"""

from dreadnode.airt.analytics.engine import AttackResult, analyze
from dreadnode.airt.analytics.types import (
    ASRBreakdown,
    ASREntry,
    CampaignAnalytics,
    ComplianceEntry,
    ComplianceMatrix,
    CoverageSummary,
    ExecutionStats,
    Finding,
    GoalCategory,
    Recommendation,
    Severity,
    TrialData,
)

__all__ = [
    "ASRBreakdown",
    "ASREntry",
    "AttackResult",
    "CampaignAnalytics",
    "ComplianceEntry",
    "ComplianceMatrix",
    "CoverageSummary",
    "ExecutionStats",
    "Finding",
    "GoalCategory",
    "Recommendation",
    "Severity",
    "TrialData",
    "analyze",
]

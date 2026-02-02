"""
Modèles de données (dataclasses)
"""

from .cleanup_models import (
    CleanupConfig,
    CleanupResult,
    ConfidenceLevel,
    ExclusionConfig,
    ScanConfig,
    SecretMatch,
    SecretPattern,
    ValidationReport,
)
from .stats_models import (
    AnalysisRecord,
    CategoryMetrics,
    ExportReport,
    ROICalculation,
    ROIParameters,
    StatisticsAggregate,
    StatisticsStorage,
)

__all__ = [
    "CleanupConfig",
    "CleanupResult",
    "ConfidenceLevel",
    "ExclusionConfig",
    "ScanConfig",
    "SecretMatch",
    "SecretPattern",
    "ValidationReport",
    "AnalysisRecord",
    "CategoryMetrics",
    "ExportReport",
    "ROICalculation",
    "ROIParameters",
    "StatisticsAggregate",
    "StatisticsStorage",
]

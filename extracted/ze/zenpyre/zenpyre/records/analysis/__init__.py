r"""Contain code to analyze records."""

from __future__ import annotations

__all__ = ["MetadataStats", "compute_metadata_stats", "print_metadata_stats_report"]

from zenpyre.records.analysis.metadata_print import print_metadata_stats_report
from zenpyre.records.analysis.metadata_stats import (
    MetadataStats,
    compute_metadata_stats,
)

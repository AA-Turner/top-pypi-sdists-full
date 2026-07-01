"""Time-Aware Missing Data Imputer.

A Python library for intelligent time-series imputation with irregular intervals.
"""

from time_aware_imputer.analyzer import GapAnalyzer
from time_aware_imputer.base import TimeAwareImputer
from time_aware_imputer.spline import SplineImputer

__version__ = "1.0.0"
__all__ = ["TimeAwareImputer", "SplineImputer", "GapAnalyzer"]

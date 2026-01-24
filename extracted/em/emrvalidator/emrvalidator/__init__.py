"""
EMRValidator - Healthcare Data Quality & Validation Library
A modern, healthcare-focused alternative to Great Expectations

Author: Healthcare Analytics Hub
Version: 1.0.0
"""

from .validator import DataValidator
from .rules import ValidationRule, RuleSet, Expectation, ExpectationSuite, HealthcareRuleSets
from .reporters import ValidationReport, HTMLReporter, JSONReporter
from .profiler import DataProfiler

__version__ = "1.0.1"
__all__ = [
    "DataValidator",
    "ValidationRule",
    "RuleSet",
    "ValidationReport",
    "HTMLReporter",
    "JSONReporter",
    "DataProfiler",
    "Expectation",
    "ExpectationSuite",
    "HealthcareRuleSets"
]

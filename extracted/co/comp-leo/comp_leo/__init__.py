"""
Comp-LEO SDK: Compliance and security analysis for Leo smart contracts.

Automated compliance checking, security analysis, and policy enforcement
for the Aleo ecosystem.
"""

__version__ = "0.1.2"
__author__ = "CompliLedger"
__license__ = "Apache-2.0"

from comp_leo.analyzer.checker import ComplianceChecker
from comp_leo.analyzer.parser import LeoParser
from comp_leo.core.models import CheckResult, Violation, Severity

__all__ = [
    "ComplianceChecker",
    "LeoParser",
    "CheckResult",
    "Violation",
    "Severity",
]

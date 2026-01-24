"""CompALGO SDK for Algorand

Static analysis + on-chain compliance proof anchoring for PyTeal/TEAL smart contracts.
"""
from .client import CompliLedgerClient  # noqa: F401
from .analyzer.checker import ComplianceChecker  # noqa: F401
from .core.verdict import (
    ComplianceVerdict,
    build_verdict,
    verdict_hash,
)  # noqa: F401

__version__ = "0.1.0"
__all__ = [
    "CompliLedgerClient",
    "ComplianceChecker",
    "ComplianceVerdict",
    "build_verdict",
    "verdict_hash",
]

"""
CompZ - Privacy-Preserving Compliance Attestation SDK

Anchor compliance proofs to Zcash blockchain without revealing sensitive data.
"""

from .client import CompZClient
from .models import ComplianceResult, ControlEvaluation

__version__ = "1.0.0"
__author__ = "CompliLedger"
__all__ = ["CompZClient", "ComplianceResult", "ControlEvaluation"]

"""Plato verifier framework.

Provides a base class and runner for post-hoc session verification.
Verifiers analyze completed sessions and publish findings as annotations.
"""

from plato.verifiers.base import BaseVerifier
from plato.verifiers.config import VerifierConfig
from plato.verifiers.models import (
    BooleanCheckData,
    CustomData,
    ErrorData,
    FindingData,
    IssueData,
    ScoreData,
    SessionData,
    VerifierFinding,
    VerifierResult,
    VerifierSignal,
)
from plato.verifiers.registry import (
    discover_verifiers,
    get_registered_verifiers,
    get_verifier,
    register_verifier,
)

__all__ = [
    "BaseVerifier",
    "BooleanCheckData",
    "CustomData",
    "ErrorData",
    "FindingData",
    "IssueData",
    "ScoreData",
    "SessionData",
    "VerifierConfig",
    "VerifierFinding",
    "VerifierResult",
    "VerifierSignal",
    "discover_verifiers",
    "get_registered_verifiers",
    "get_verifier",
    "register_verifier",
]

"""Enum types for structured LLM output schemas.

Provides case-insensitive and alias-aware enum parsing via Pydantic BeforeValidators.
"""

from __future__ import annotations

from enum import Enum
from typing import Any


class Severity(str, Enum):
    """Severity level for review findings and quality issues."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


_SEVERITY_ALIAS_MAP: dict[str, Severity] = {
    "H": Severity.HIGH,
    "M": Severity.MEDIUM,
    "L": Severity.LOW,
    "Med": Severity.MEDIUM,
    "Hi": Severity.HIGH,
    "Lo": Severity.LOW,
    "CRIT": Severity.CRITICAL,
    "Crit": Severity.CRITICAL,
}


def normalize_severity(value: Any) -> Any:
    """Normalize severity values via alias map and case-insensitive matching."""
    if isinstance(value, Severity):
        return value
    if not isinstance(value, str):
        return value
    # Check alias map (case-sensitive first)
    if value in _SEVERITY_ALIAS_MAP:
        return _SEVERITY_ALIAS_MAP[value]
    # Case-insensitive alias check
    for alias, sev in _SEVERITY_ALIAS_MAP.items():
        if value.lower() == alias.lower():
            return sev
    # Case-insensitive canonical matching
    for member in Severity:
        if value.lower() == member.value.lower():
            return member
    valid = [m.value for m in Severity] + list(_SEVERITY_ALIAS_MAP.keys())
    msg = f"Invalid severity value: {value!r}. Valid values: {sorted(set(valid))}"
    raise ValueError(msg)


class Verdict(str, Enum):
    """Overall review verdict for a pull request."""

    APPROVE = "approve"
    REQUEST_CHANGES = "request_changes"


def normalize_verdict(value: Any) -> Any:
    """Normalize verdict values via case-insensitive canonical matching."""
    if isinstance(value, Verdict):
        return value
    if not isinstance(value, str):
        return value
    for member in Verdict:
        if value.lower() == member.value.lower():
            return member
    valid = [m.value for m in Verdict]
    msg = f"Invalid verdict value: {value!r}. Valid values: {valid}"
    raise ValueError(msg)


class EscalationCategory(str, Enum):
    """Category of escalation reason when autonomous processing cannot proceed."""

    AMBIGUOUS_REQUIREMENTS = "ambiguous_requirements"
    SECURITY_CONCERN = "security_concern"
    ARCHITECTURE_DECISION = "architecture_decision"
    POLICY_VIOLATION = "policy_violation"
    EXTERNAL_DEPENDENCY = "external_dependency"
    BUDGET_EXCEEDED = "budget_exceeded"


def normalize_escalation_category(value: Any) -> Any:
    """Normalize escalation category via case-insensitive canonical matching."""
    if isinstance(value, EscalationCategory):
        return value
    if not isinstance(value, str):
        return value
    for member in EscalationCategory:
        if value.lower() == member.value.lower():
            return member
    valid = [m.value for m in EscalationCategory]
    msg = f"Invalid escalation category: {value!r}. Valid values: {valid}"
    raise ValueError(msg)


class QualityGateName(str, Enum):
    """Named quality gates for implementation verification."""

    LINT = "lint"
    TYPE_CHECK = "type_check"
    UNIT_TESTS = "unit_tests"
    INTEGRATION_TESTS = "integration_tests"
    COVERAGE = "coverage"
    SECURITY_SCAN = "security_scan"
    BUILD = "build"


def normalize_quality_gate_name(value: Any) -> Any:
    """Normalize quality gate name via case-insensitive canonical matching."""
    if isinstance(value, QualityGateName):
        return value
    if not isinstance(value, str):
        return value
    for member in QualityGateName:
        if value.lower() == member.value.lower():
            return member
    valid = [m.value for m in QualityGateName]
    msg = f"Invalid quality gate name: {value!r}. Valid values: {valid}"
    raise ValueError(msg)

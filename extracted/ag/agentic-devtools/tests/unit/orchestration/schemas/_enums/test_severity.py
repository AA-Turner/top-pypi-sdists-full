"""Tests for Severity enum: canonical values, case-insensitive matching, alias map."""

from typing import Annotated

import pytest
from pydantic import BaseModel, BeforeValidator, ValidationError

from agentic_devtools.orchestration.schemas._enums import Severity, normalize_severity


class _SeverityModel(BaseModel):
    severity: Annotated[Severity, BeforeValidator(normalize_severity)]


class TestSeverity:
    """Tests for Severity enum normalization."""

    def test_canonical_values(self):
        for value in ("critical", "high", "medium", "low"):
            result = _SeverityModel(severity=value)
            assert result.severity == Severity(value)

    def test_case_insensitive_canonical(self):
        assert _SeverityModel(severity="HIGH").severity == Severity.HIGH
        assert _SeverityModel(severity="Critical").severity == Severity.CRITICAL
        assert _SeverityModel(severity="MEDIUM").severity == Severity.MEDIUM
        assert _SeverityModel(severity="Low").severity == Severity.LOW

    def test_alias_map(self):
        assert _SeverityModel(severity="H").severity == Severity.HIGH
        assert _SeverityModel(severity="M").severity == Severity.MEDIUM
        assert _SeverityModel(severity="L").severity == Severity.LOW
        assert _SeverityModel(severity="Med").severity == Severity.MEDIUM
        assert _SeverityModel(severity="Hi").severity == Severity.HIGH
        assert _SeverityModel(severity="Lo").severity == Severity.LOW
        assert _SeverityModel(severity="CRIT").severity == Severity.CRITICAL
        assert _SeverityModel(severity="Crit").severity == Severity.CRITICAL

    def test_case_insensitive_alias(self):
        assert _SeverityModel(severity="h").severity == Severity.HIGH
        assert _SeverityModel(severity="m").severity == Severity.MEDIUM
        assert _SeverityModel(severity="l").severity == Severity.LOW

    def test_unknown_rejection(self):
        with pytest.raises(ValidationError) as exc_info:
            _SeverityModel(severity="unknown")
        assert "Invalid severity value" in str(exc_info.value)

    def test_enum_instance_passthrough(self):
        result = _SeverityModel(severity=Severity.HIGH)
        assert result.severity == Severity.HIGH

    def test_non_string_passthrough(self):
        result = normalize_severity(42)
        assert result == 42

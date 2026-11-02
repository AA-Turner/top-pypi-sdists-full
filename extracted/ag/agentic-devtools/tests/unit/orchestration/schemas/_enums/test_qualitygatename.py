"""Tests for QualityGateName enum."""

from typing import Annotated

import pytest
from pydantic import BaseModel, BeforeValidator, ValidationError

from agentic_devtools.orchestration.schemas._enums import (
    QualityGateName,
    normalize_quality_gate_name,
)


class _Model(BaseModel):
    gate: Annotated[QualityGateName, BeforeValidator(normalize_quality_gate_name)]


class TestQualityGateName:
    """Tests for QualityGateName enum normalization."""

    def test_canonical_values(self):
        for value in ("lint", "type_check", "unit_tests", "integration_tests", "coverage", "security_scan", "build"):
            result = _Model(gate=value)
            assert result.gate == QualityGateName(value)

    def test_case_insensitive(self):
        assert _Model(gate="LINT").gate == QualityGateName.LINT
        assert _Model(gate="Unit_Tests").gate == QualityGateName.UNIT_TESTS
        assert _Model(gate="COVERAGE").gate == QualityGateName.COVERAGE

    def test_unknown_rejection(self):
        with pytest.raises(ValidationError):
            _Model(gate="unknown_gate")

    def test_enum_instance_passthrough(self):
        result = _Model(gate=QualityGateName.LINT)
        assert result.gate == QualityGateName.LINT

    def test_non_string_passthrough(self):
        result = normalize_quality_gate_name(42)
        assert result == 42

"""Tests for QualityGateResult model."""

from agentic_devtools.orchestration.schemas._enums import QualityGateName
from agentic_devtools.orchestration.schemas.work_on_issue.quality import QualityGateResult


class TestQualityGateResult:
    """Tests for QualityGateResult construction and serialization."""

    def test_construction(self):
        result = QualityGateResult(gate="unit_tests", passed=True)
        assert result.gate == QualityGateName.UNIT_TESTS
        assert result.passed is True
        assert result.details == ""

    def test_case_insensitive_gate(self):
        result = QualityGateResult(gate="LINT", passed=False, details="Error")
        assert result.gate == QualityGateName.LINT

    def test_model_dump(self):
        result = QualityGateResult(
            gate="coverage",
            passed=True,
            details="100%",
            metric_value="100%",
        )
        data = result.model_dump()
        assert data["gate"] == "coverage"
        assert data["passed"] is True

    def test_round_trip(self):
        original = QualityGateResult(gate="build", passed=True)
        raw = original.model_dump_json()
        restored = QualityGateResult.model_validate_json(raw)
        assert original == restored

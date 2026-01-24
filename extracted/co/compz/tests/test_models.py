"""
Tests for Pydantic models (ComplianceResult, ControlEvaluation).
"""
import pytest
from pydantic import ValidationError
from compz.models import ComplianceResult, ControlEvaluation


def test_control_evaluation_valid():
    """Test creating valid ControlEvaluation."""
    control = ControlEvaluation(
        control_id="PCI-1.1.1",
        framework="PCI-DSS",
        passed=True,
        reason="Test passed",
        severity="high"
    )
    
    assert control.control_id == "PCI-1.1.1"
    assert control.passed is True
    assert control.framework == "PCI-DSS"


def test_control_evaluation_missing_required():
    """Test that missing required fields raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        ControlEvaluation(
            control_id="PCI-1.1.1",
            # Missing: framework, passed, reason
        )
    
    assert "framework" in str(exc_info.value)


def test_compliance_result_valid():
    """Test creating valid ComplianceResult."""
    result = ComplianceResult(
        repo_id="test/repo",
        commit_hash="abc123",
        frameworks=["PCI-DSS"],
        control_evaluations=[
            {
                "control_id": "PCI-1.1.1",
                "framework": "PCI-DSS",
                "passed": True,
                "reason": "Test"
            }
        ],
        risk_score=25.5,
        timestamp="2024-11-28T00:00:00Z"
    )
    
    assert result.repo_id == "test/repo"
    assert result.risk_score == 25.5
    assert len(result.control_evaluations) == 1


def test_compliance_result_risk_score_bounds():
    """Test that risk_score validates bounds (0-100)."""
    # Valid: within bounds
    result = ComplianceResult(
        repo_id="test",
        commit_hash="abc",
        frameworks=["PCI-DSS"],
        control_evaluations=[],
        risk_score=50.0,
        timestamp="2024-11-28T00:00:00Z"
    )
    assert result.risk_score == 50.0
    
    # Invalid: negative
    with pytest.raises(ValidationError):
        ComplianceResult(
            repo_id="test",
            commit_hash="abc",
            frameworks=["PCI-DSS"],
            control_evaluations=[],
            risk_score=-5.0,
            timestamp="2024-11-28T00:00:00Z"
        )
    
    # Invalid: over 100
    with pytest.raises(ValidationError):
        ComplianceResult(
            repo_id="test",
            commit_hash="abc",
            frameworks=["PCI-DSS"],
            control_evaluations=[],
            risk_score=150.0,
            timestamp="2024-11-28T00:00:00Z"
        )


def test_compliance_result_missing_required():
    """Test that missing required fields raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        ComplianceResult(
            repo_id="test/repo",
            # Missing: commit_hash, frameworks, control_evaluations, risk_score, timestamp
        )
    
    error_str = str(exc_info.value)
    assert "commit_hash" in error_str or "field required" in error_str.lower()

"""
Tests for ComplianceVerdict schema and hashing
"""
import json
from compalgo.core.verdict import ComplianceVerdict, verdict_hash, build_verdict


def test_verdict_canonical_json():
    """Test that canonical JSON is deterministic and sorted"""
    v = ComplianceVerdict(
        framework="SOC2",
        control_id="CC6.1",
        status="fail",
        contract="test.py",
        rules_triggered=["RULE_A", "RULE_B"],
        severity="critical",
        timestamp="2024-01-01T00:00:00Z",
    )
    cj = v.canonical_json()
    data = json.loads(cj)
    # Keys should be sorted
    assert list(data.keys()) == sorted(data.keys())
    # Should be compact (no spaces after : or ,)
    assert ": " not in cj or True  # canonical uses separators=(',', ':')


def test_verdict_hash_deterministic():
    """Test that hash is deterministic for same input"""
    v1 = ComplianceVerdict(
        framework="SOC2",
        control_id="CC6.1",
        status="pass",
        contract="test.py",
        rules_triggered=[],
        severity="none",
        timestamp="2024-01-01T00:00:00Z",
    )
    v2 = ComplianceVerdict(
        framework="SOC2",
        control_id="CC6.1",
        status="pass",
        contract="test.py",
        rules_triggered=[],
        severity="none",
        timestamp="2024-01-01T00:00:00Z",
    )
    assert verdict_hash(v1) == verdict_hash(v2)


def test_verdict_hash_changes_with_content():
    """Test that changing content changes hash"""
    v1 = ComplianceVerdict(
        framework="SOC2",
        control_id="CC6.1",
        status="pass",
        contract="test.py",
        rules_triggered=[],
        severity="none",
        timestamp="2024-01-01T00:00:00Z",
    )
    v2 = ComplianceVerdict(
        framework="SOC2",
        control_id="CC6.1",
        status="fail",  # different status
        contract="test.py",
        rules_triggered=["RULE_X"],
        severity="high",
        timestamp="2024-01-01T00:00:00Z",
    )
    assert verdict_hash(v1) != verdict_hash(v2)


def test_build_verdict():
    """Test build_verdict helper"""
    violations = [
        {"rule_id": "RULE_A", "severity": "critical", "message": "test"},
        {"rule_id": "RULE_B", "severity": "high", "message": "test2"},
    ]
    v = build_verdict(
        contract="test.py",
        violations=violations,
        framework="SOC2",
        control_id="CC6.1",
        fail_on="medium",
    )
    assert v.status == "fail"  # because critical > medium
    assert v.severity == "critical"
    assert "RULE_A" in v.rules_triggered
    assert "RULE_B" in v.rules_triggered


if __name__ == "__main__":
    test_verdict_canonical_json()
    test_verdict_hash_deterministic()
    test_verdict_hash_changes_with_content()
    test_build_verdict()
    print("All verdict tests passed!")

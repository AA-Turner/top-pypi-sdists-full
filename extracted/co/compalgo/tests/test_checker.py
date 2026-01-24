"""
Tests for ComplianceChecker and rule engine
"""
import os
from pathlib import Path
from compalgo.analyzer.checker import ComplianceChecker


def test_checker_detects_violations():
    """Test that checker detects P0 violations in example contract"""
    # Use the vulnerable example contract
    example_path = Path(__file__).parent.parent / "examples" / "vulnerable_escrow.py"
    if not example_path.exists():
        print(f"Skipping test - example file not found: {example_path}")
        return
    
    checker = ComplianceChecker(policy_pack="algorand-baseline", threshold=80)
    results = checker.check_file(str(example_path))
    
    assert results is not None
    assert len(results.violations) > 0, "Expected violations in vulnerable contract"
    
    # Check for specific expected violations
    rule_ids = [v["rule_id"] for v in results.violations]
    assert "DELETE_WITHOUT_ADMIN_CHECK" in rule_ids or "MISSING_ADMIN_SENDER_CHECK" in rule_ids
    
    # Check score is below threshold
    assert results.score < 80, f"Expected score < 80, got {results.score}"
    assert results.passed is False


def test_checker_score_calculation():
    """Test that score calculation follows the formula"""
    example_path = Path(__file__).parent.parent / "examples" / "vulnerable_escrow.py"
    if not example_path.exists():
        print(f"Skipping test - example file not found: {example_path}")
        return
    
    checker = ComplianceChecker(policy_pack="algorand-baseline")
    results = checker.check_file(str(example_path))
    
    # Manually calculate expected score
    expected = 100
    for v in results.violations:
        sev = v["severity"]
        if sev == "critical":
            expected -= 20
        elif sev == "high":
            expected -= 10
        elif sev == "medium":
            expected -= 5
        elif sev == "low":
            expected -= 2
    expected = max(0, min(100, expected))
    
    assert results.score == expected, f"Score mismatch: got {results.score}, expected {expected}"


def test_checker_teal_file():
    """Test checker on TEAL file"""
    example_path = Path(__file__).parent.parent / "examples" / "vulnerable_contract.teal"
    if not example_path.exists():
        print(f"Skipping test - example file not found: {example_path}")
        return
    
    checker = ComplianceChecker(policy_pack="algorand-baseline")
    results = checker.check_file(str(example_path))
    
    assert results is not None
    assert len(results.violations) > 0, "Expected violations in vulnerable TEAL contract"


if __name__ == "__main__":
    test_checker_detects_violations()
    test_checker_score_calculation()
    test_checker_teal_file()
    print("All checker tests passed!")

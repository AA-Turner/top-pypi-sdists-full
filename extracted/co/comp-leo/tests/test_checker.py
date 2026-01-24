"""Tests for compliance checker."""

import pytest
from comp_leo.analyzer.checker import ComplianceChecker
from comp_leo.core.models import Severity


def test_detect_missing_input_validation():
    """Test detection of missing input validation."""
    source = """
program test.aleo {
    transition process(public amount: u64) {
        // No validation!
        return;
    }
}
"""
    
    checker = ComplianceChecker(policy_pack="aleo-baseline")
    program = checker.parser.parse_source(source, "test.leo")
    violations = checker._run_checks(program)
    
    # Should find missing input validation
    validation_violations = [v for v in violations if v.rule_id == "input-validation-missing"]
    assert len(validation_violations) > 0


def test_detect_unprotected_state_mutation():
    """Test detection of unprotected state changes."""
    source = """
program test.aleo {
    mapping data: field => u64;
    
    transition update(key: field, value: u64) {
        Mapping::set(data, key, value);  // No access control!
    }
}
"""
    
    checker = ComplianceChecker(policy_pack="aleo-baseline")
    program = checker.parser.parse_source(source, "test.leo")
    violations = checker._run_checks(program)
    
    # Should find unprotected state mutation
    state_violations = [v for v in violations if v.rule_id == "state-mutation-unprotected"]
    assert len(state_violations) > 0
    assert state_violations[0].severity == Severity.CRITICAL


def test_detect_private_data_exposure():
    """Test detection of privacy issues."""
    source = """
program test.aleo {
    struct User {
        username: field,
        password: field,  // Sensitive!
    }
}
"""
    
    checker = ComplianceChecker(policy_pack="aleo-baseline")
    program = checker.parser.parse_source(source, "test.leo")
    violations = checker._run_checks(program)
    
    # Should find privacy issue
    privacy_violations = [v for v in violations if v.rule_id == "private-data-exposure"]
    assert len(privacy_violations) > 0


def test_secure_code_passes():
    """Test that properly secured code passes."""
    source = """
program test.aleo {
    mapping data: address => u64;
    
    transition update(public owner: address, public value: u64) -> Future {
        assert(value > 0u64);
        assert(value < 1000000u64);
        return finalize_update(owner, value);
    }
    
    async function finalize_update(owner: address, value: u64) {
        assert_eq(self.caller, owner);
        Mapping::set(data, owner, value);
    }
}
"""
    
    checker = ComplianceChecker(policy_pack="aleo-baseline")
    program = checker.parser.parse_source(source, "test.leo")
    violations = checker._run_checks(program)
    
    # Should have minimal or no violations
    critical_violations = [v for v in violations if v.severity == Severity.CRITICAL]
    assert len(critical_violations) == 0


def test_score_computation():
    """Test compliance score computation."""
    source = """
program test.aleo {
    transition safe() {
        return;
    }
}
"""
    
    checker = ComplianceChecker(policy_pack="aleo-baseline")
    program = checker.parser.parse_source(source, "test.leo")
    violations = checker._run_checks(program)
    score = checker._compute_score(violations, 10)
    
    assert 0 <= score <= 100

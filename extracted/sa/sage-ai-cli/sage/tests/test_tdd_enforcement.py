"""Tests for TDD enforcement in SAGE AI.

These tests verify that SAGE AI properly enforces Test-Driven Development
patterns when handling implementation requests.
"""

from sage.core.procedural_workflow import TestGenerationResult, TestSpec
from sage.core.request_classifier import (
    RequestClassifier,
    RequestType,
)


class TestTDDRequestClassification:
    """Test that TDD requirements are properly detected in requests."""

    def test_explicit_tdd_keyword_sets_strict_mode(self):
        """When user explicitly mentions TDD, strict mode should be enabled."""
        classifier = RequestClassifier()

        # Explicit TDD request
        result = classifier.classify("Implement the auth module with TDD")
        assert result.requires_tdd is True
        assert result.tdd_strict_mode is True

        # Test-driven development phrase
        result = classifier.classify("Use test-driven development to add login")
        assert result.requires_tdd is True
        assert result.tdd_strict_mode is True

        # "tests first" pattern
        result = classifier.classify("Write tests first, then implement the feature")
        assert result.requires_tdd is True
        assert result.tdd_strict_mode is True

    def test_implementation_requests_require_tdd(self):
        """Implementation requests should require TDD by default."""
        classifier = RequestClassifier()

        # Standard implementation requests
        result = classifier.classify("Implement a user authentication system")
        assert result.request_type == RequestType.IMPLEMENTATION
        assert result.requires_tdd is True

        result = classifier.classify("Add a logout button to the dashboard")
        assert result.request_type == RequestType.IMPLEMENTATION
        assert result.requires_tdd is True

    def test_fix_all_requests_have_strict_tdd(self):
        """FIX_ALL requests should have strict TDD mode."""
        classifier = RequestClassifier()

        result = classifier.classify("Fix all 10 issues in the codebase")
        assert result.request_type == RequestType.FIX_ALL
        assert result.requires_tdd is True
        assert result.tdd_strict_mode is True

        result = classifier.classify("Implement all the improvements listed above")
        assert result.request_type == RequestType.FIX_ALL
        assert result.requires_tdd is True
        assert result.tdd_strict_mode is True

    def test_analysis_requests_do_not_require_tdd(self):
        """Analysis-only requests should NOT require TDD."""
        classifier = RequestClassifier()

        result = classifier.classify("Analyze this codebase for security issues")
        assert result.request_type == RequestType.ANALYSIS
        assert result.requires_tdd is False
        assert result.read_only is True

        result = classifier.classify("List 100 improvements for this project")
        assert result.request_type == RequestType.LIST_GENERATION
        assert result.requires_tdd is False
        assert result.read_only is True


class TestTDDInstructionPriorities:
    """Test that TDD instruction priorities are set correctly."""

    def test_implementation_with_tdd_has_tdd_first_priority(self):
        """Implementation requests with TDD should prioritize test-first."""
        classifier = RequestClassifier()

        result = classifier.classify("Implement feature X with TDD")
        assert result.requires_tdd is True
        assert len(result.instruction_priorities) > 0

        # First instruction should be about TDD
        assert "TDD" in result.instruction_priorities[0]
        assert (
            "test" in result.instruction_priorities[0].lower()
            or "TESTS" in result.instruction_priorities[0]
        )

    def test_fix_all_has_sequential_tdd_priorities(self):
        """FIX_ALL should have priorities for sequential TDD fixes."""
        classifier = RequestClassifier()

        result = classifier.classify("Fix all these bugs")
        priorities = result.instruction_priorities

        # Should mention TDD and sequential completion
        has_tdd_mention = any("TDD" in p for p in priorities)
        has_sequential = any("sequential" in p.lower() or "one" in p.lower() for p in priorities)

        assert has_tdd_mention or has_sequential


class TestTestGenerationValidation:
    """Test that generated tests are validated before proceeding."""

    def test_empty_tests_fail_validation(self):
        """Tests with only 'pass' statements should fail validation."""
        result = TestGenerationResult(
            tests=[
                TestSpec(name="test_empty", code="def test_empty():\n    pass"),
                TestSpec(name="test_also_empty", code="def test_also_empty():\n    pass"),
            ],
            coverage_areas=["basic"],
        )

        is_valid, issues = result.validate_tests()
        assert is_valid is False
        assert len(issues) > 0
        assert any("empty" in issue.lower() or "pass" in issue.lower() for issue in issues)

    def test_tests_without_assertions_fail_validation(self):
        """Tests without assertions should fail validation."""
        result = TestGenerationResult(
            tests=[
                TestSpec(
                    name="test_no_assertion",
                    code="def test_no_assertion():\n    x = 1 + 1\n    print(x)",
                ),
            ],
            coverage_areas=["basic"],
        )

        is_valid, issues = result.validate_tests()
        assert is_valid is False
        assert any("assertion" in issue.lower() for issue in issues)

    def test_tests_with_assertions_pass_validation(self):
        """Tests with proper assertions should pass validation."""
        result = TestGenerationResult(
            tests=[
                TestSpec(
                    name="test_with_assertion",
                    code="def test_with_assertion():\n    result = 1 + 1\n    assert result == 2",
                ),
                TestSpec(
                    name="test_with_assertEqual",
                    code="def test_with_assertEqual():\n    self.assertEqual(1, 1)",
                ),
            ],
            coverage_areas=["basic", "math"],
        )

        is_valid, issues = result.validate_tests()
        assert is_valid is True
        assert len(issues) == 0

    def test_tests_with_placeholder_comments_fail_validation(self):
        """Tests with TODO/FIXME comments should fail validation."""
        result = TestGenerationResult(
            tests=[
                TestSpec(
                    name="test_placeholder",
                    code="def test_placeholder():\n    # TODO: implement this test\n    assert True",
                ),
            ],
            coverage_areas=["basic"],
        )

        is_valid, issues = result.validate_tests()
        assert is_valid is False
        assert any("TODO" in issue for issue in issues)


class TestNoTestsGenerated:
    """Test handling when no tests are generated."""

    def test_empty_test_list_fails_validation(self):
        """If no tests are generated, validation should fail."""
        result = TestGenerationResult(
            tests=[],
            coverage_areas=[],
        )

        is_valid, issues = result.validate_tests()
        assert is_valid is False
        assert any("no tests" in issue.lower() for issue in issues)


class TestMixedTestQuality:
    """Test validation with mixed quality tests."""

    def test_some_good_some_bad_tests_fail_validation(self):
        """If some tests are bad, the whole set should fail."""
        result = TestGenerationResult(
            tests=[
                TestSpec(name="test_good", code="def test_good():\n    assert 1 == 1"),
                TestSpec(name="test_bad", code="def test_bad():\n    pass  # placeholder"),
            ],
            coverage_areas=["mixed"],
        )

        is_valid, issues = result.validate_tests()
        assert is_valid is False
        # Should identify the bad test specifically
        assert any("test_bad" in issue for issue in issues)

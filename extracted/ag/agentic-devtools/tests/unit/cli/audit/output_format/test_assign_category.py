"""Tests for category assignment heuristic."""

from agentic_devtools.cli.audit.output_format import assign_category


class TestAssignCategory:
    """Tests for assign_category() covering the 13-category taxonomy."""

    def test_input_validation_keywords(self) -> None:
        primary, _ = assign_category("Missing validation for negative values in bounds check")
        assert primary == "input_validation"

    def test_error_handling_keywords(self) -> None:
        primary, _ = assign_category("The exception is not handled, add try/catch")
        assert primary == "error_handling"

    def test_security_keywords(self) -> None:
        primary, _ = assign_category("This could lead to injection vulnerability in auth")
        assert primary == "security"

    def test_performance_keywords(self) -> None:
        primary, _ = assign_category("This is slow, consider adding cache for optimization")
        assert primary == "performance"

    def test_naming_keywords(self) -> None:
        primary, _ = assign_category("The variable name is misleading, please rename")
        assert primary == "naming"

    def test_empty_body_returns_other(self) -> None:
        primary, secondary = assign_category("")
        assert primary == "other"
        assert secondary == ""

    def test_no_keywords_returns_other(self) -> None:
        primary, secondary = assign_category("LGTM, looks good to me!")
        assert primary == "other"
        assert secondary == ""

    def test_secondary_category_assigned(self) -> None:
        # Body with both error handling and security keywords
        _, secondary = assign_category("Missing error handling for authentication failure in security module")
        assert secondary != ""

    def test_case_insensitive(self) -> None:
        primary, _ = assign_category("MISSING VALIDATION for BOUNDS")
        assert primary == "input_validation"

    def test_documentation_keywords(self) -> None:
        primary, _ = assign_category("Missing docstring for this public function")
        assert primary == "documentation"

    def test_concurrency_keywords(self) -> None:
        primary, _ = assign_category("This could cause a race condition with parallel threads")
        assert primary == "concurrency"

    def test_type_safety_keywords(self) -> None:
        primary, _ = assign_category("Missing type annotation, consider Optional typing")
        assert primary == "type_safety"

    def test_test_reliability_keywords(self) -> None:
        primary, _ = assign_category("This test is flaky due to missing mock fixture")
        assert primary == "test_reliability"

    def test_dependencies_keywords(self) -> None:
        primary, _ = assign_category("This deprecated package version should be upgraded")
        assert primary == "dependencies"

    def test_api_interface_keywords(self) -> None:
        primary, _ = assign_category("This is a breaking change to the API interface contract")
        assert primary == "api_interface"

    def test_cross_platform_keywords(self) -> None:
        primary, _ = assign_category("Use os.path.join for cross-platform path separator handling")
        assert primary == "cross_platform"

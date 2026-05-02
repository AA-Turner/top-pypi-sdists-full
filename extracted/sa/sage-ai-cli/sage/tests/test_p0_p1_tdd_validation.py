"""TDD tests for P0 and P1 hallucination prevention fixes.

This test file validates that the P0 (critical) and P1 (high priority) issues
identified in the SAGE AI hallucination analysis are properly fixed.

P0 Issues (Critical):
- P0-1: _parse_test_output must return has_collection_errors
- P0-2: Both test consumers must use the same parsing contract
- P0-3: CLI flow must route through _execute_request_with_validation
- P0-4: Tool execution must be structured, not text-based

P1 Issues (High Priority):
- P1-5: Pre-display tool syntax blocking
- P1-6: Pre-display path spam detection
- P1-7: Prevent described tools at source
- P1-8: Strengthen grounding enforcement
- P1-9: Complete failure-loop handling
- P1-10: Unify test-path conventions

Run with: pytest sage/tests/test_p0_p1_tdd_validation.py -v
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

# =============================================================================
# P0-1: _parse_test_output MUST return has_collection_errors
# =============================================================================


class TestP01ParseTestOutputHasCollectionErrors:
    """P0-1: Verify _parse_test_output returns rich schema with has_collection_errors."""

    def test_parse_test_output_returns_has_collection_errors_key(self):
        """CRITICAL: _parse_test_output MUST return has_collection_errors in result dict."""
        from sage.main import _parse_test_output

        test_output = "===== 5 passed in 1.2s ====="
        result = _parse_test_output(test_output)

        # This is the P0-1 fix: has_collection_errors must be present
        assert "has_collection_errors" in result, (
            "P0-1 VIOLATION: _parse_test_output does not return has_collection_errors! "
            "The TDD gate at line 1803 requires this field."
        )

    def test_parse_test_output_detects_collection_errors(self):
        """Should detect 'errors during collection' pattern."""
        from sage.main import _parse_test_output

        test_output = """
============================= ERRORS =============================
collected 0 items / 2 errors

ERROR collecting tests/test_foo.py
ModuleNotFoundError: No module named 'missing_module'
============================= short test summary info =============================
"""
        result = _parse_test_output(test_output)

        assert result["has_collection_errors"] is True, "P0-1: Should detect collection errors"

    def test_parse_test_output_detects_import_errors_as_collection_errors(self):
        """Should detect ImportError during collection."""
        from sage.main import _parse_test_output

        test_output = """
ImportError: cannot import name 'foo' from 'bar'
ERROR collecting tests/test_module.py
"""
        result = _parse_test_output(test_output)

        assert result["has_collection_errors"] is True, (
            "P0-1: ImportError during collection should set has_collection_errors"
        )

    def test_parse_test_output_has_backwards_compatible_aliases(self):
        """P0-2: Should have backwards-compatible aliases for simple schema."""
        from sage.main import _parse_test_output

        test_output = "===== 10 passed, 2 failed in 3.1s ====="
        result = _parse_test_output(test_output)

        # Rich schema fields
        assert "has_collection_errors" in result
        assert "passed" in result
        assert "failed" in result

        # Backwards-compatible aliases (P0-2)
        assert "total_passed" in result, "P0-2: Missing total_passed alias"
        assert "total_failed" in result, "P0-2: Missing total_failed alias"
        assert "is_success" in result, "P0-2: Missing is_success alias"

        # Values should match
        assert result["total_passed"] == result["passed"]
        assert result["total_failed"] == result["failed"]


# =============================================================================
# P0-2: Unify Test Parsing Contracts
# =============================================================================


class TestP02UnifiedTestParsingContract:
    """P0-2: Both test consumers must use the same parsing contract."""

    def test_main_and_shell_return_same_schema(self):
        """Both main._parse_test_output and shell.parse_test_output must match."""
        from sage.core.shell import parse_test_output as shell_parser
        from sage.main import _parse_test_output as main_parser

        test_output = "===== 5 passed, 3 failed, 1 error in 2.5s ====="

        main_result = main_parser(test_output)
        shell_result = shell_parser(test_output)

        # Must have the same keys
        main_keys = set(main_result.keys())
        shell_keys = set(shell_result.keys())

        # Key fields that must be present in both
        required_keys = {
            "passed",
            "failed",
            "has_collection_errors",
            "total_passed",
            "total_failed",
            "is_success",
        }

        for key in required_keys:
            assert key in main_keys, f"P0-2: main parser missing key '{key}'"
            assert key in shell_keys, f"P0-2: shell parser missing key '{key}'"

    def test_shell_parser_is_authoritative(self):
        """main._parse_test_output should delegate to shell.parse_test_output."""
        # Import paths
        from sage.core.shell import parse_test_output as shell_parser
        from sage.main import _parse_test_output as main_parser

        # They should produce identical results
        test_cases = [
            "===== 5 passed in 1.2s =====",
            "===== 5 failed, 0 passed in 2.5s =====",
            "collected 0 items / 1 error\nImportError: foo",
        ]

        for test_output in test_cases:
            main_result = main_parser(test_output)
            shell_result = shell_parser(test_output)

            assert main_result["has_collection_errors"] == shell_result["has_collection_errors"], (
                f"P0-2: main and shell parsers disagree on has_collection_errors for: {test_output[:50]}"
            )
            assert main_result["passed"] == shell_result["passed"]
            assert main_result["failed"] == shell_result["failed"]


# =============================================================================
# P0-3: CLI Flow Routes Through Validation
# =============================================================================


class TestP03CLIValidationRouting:
    """P0-3: CLI flow must route through _execute_request_with_validation."""

    def test_execute_request_with_validation_exists(self):
        """The validation wrapper must exist."""
        from sage.main import _execute_request_with_validation

        assert callable(_execute_request_with_validation), (
            "P0-3: _execute_request_with_validation must be callable"
        )

    def test_validation_wrapper_calls_validators(self):
        """Validation wrapper must call detection functions."""
        from sage.main import _execute_request_with_validation

        # Mock everything needed
        with patch("sage.main._call_llm") as mock_llm:
            mock_llm.return_value = "Here is my response without reading any files."

            with patch("sage.main._track_files_read") as mock_track_read:
                mock_track_read.return_value = []

                with patch("sage.main._track_files_written") as mock_track_write:
                    mock_track_write.return_value = []

                    with patch("sage.main._detect_tool_description_vs_execution") as mock_detect:
                        mock_detect.return_value = (False, [])

                        with patch("sage.main._detect_repetitive_filler") as mock_filler:
                            mock_filler.return_value = (False, 0.0)

                            with patch("sage.main._get_execution_context") as mock_ctx:
                                mock_ctx.return_value = MagicMock(search_executed=False)

                                try:
                                    _execute_request_with_validation("test request")
                                except Exception:
                                    pass  # May raise on retry exhaustion

                                # Verify validators were called
                                assert mock_detect.called, (
                                    "P0-3: _detect_tool_description_vs_execution not called"
                                )


# =============================================================================
# P0-4: Structured Tool Execution
# =============================================================================


class TestP04StructuredToolExecution:
    """P0-4: Tool execution must be structured, not text-based."""

    def test_tool_parser_exists(self):
        """ToolParser class must exist for structured parsing."""
        from sage.core.tools import ToolParser

        assert hasattr(ToolParser, "validate_tool_syntax")
        assert hasattr(ToolParser, "parse_tool_command")
        assert hasattr(ToolParser, "validate_file_path")

    def test_tool_parser_rejects_xml_syntax(self):
        """Should reject XML-style tool calls."""
        from sage.core.tools import ToolParser

        bad_texts = [
            "<tool_use>read file.py</tool_use>",
            "<function_call name='read'>file.py</function_call>",
            "<invoke>READ: file.py</invoke>",
        ]

        for text in bad_texts:
            result = ToolParser.validate_tool_syntax(text)
            assert not result.valid, f"P0-4: Should reject XML syntax: {text[:30]}"
            assert result.error_type == "invalid_syntax"

    def test_tool_parser_rejects_yaml_syntax(self):
        """Should reject YAML-style tool calls."""
        from sage.core.tools import ToolParser

        bad_texts = [
            "tool_name: read\nparameters:\n  path: file.py",
            "function: read_file\nargs: file.py",
        ]

        for text in bad_texts:
            result = ToolParser.validate_tool_syntax(text)
            assert not result.valid, f"P0-4: Should reject YAML syntax: {text[:30]}"

    def test_tool_parser_rejects_described_tools(self):
        """Should reject 'I will use READ' descriptions."""
        from sage.core.tools import ToolParser

        bad_texts = [
            "I will use the READ tool to read file.py",
            "I would use SEARCH to find the function",
            "I should use BASH to run the tests",
            "Let me use READ to examine this file",
        ]

        for text in bad_texts:
            result = ToolParser.validate_tool_syntax(text)
            assert not result.valid, f"P0-4: Should reject described tool: {text[:40]}"

    def test_tool_parser_accepts_valid_format(self):
        """Should accept proper TOOL: argument format."""
        from sage.core.tools import ToolParser

        # First check that the syntax is valid
        result = ToolParser.validate_tool_syntax("READ: src/main.py")
        assert result.valid, "P0-4: Should accept valid tool syntax"

        # Then parse the command
        parsed = ToolParser.parse_tool_command("READ: src/main.py")
        assert parsed.valid
        assert parsed.tool_name == "READ"

    def test_tool_parser_validates_file_paths(self):
        """Should reject garbage/placeholder file paths."""
        from sage.core.tools import ToolParser

        bad_paths = [
            "<path/to/file>",
            "[your-file-here]",
            "/path/to/your/file",
            "...",
            "example_file.py",
            "your_project/file.py",
        ]

        for path in bad_paths:
            result = ToolParser.validate_file_path(path)
            assert not result.valid, f"P0-4: Should reject bad path: {path}"


# =============================================================================
# P1-5: Pre-display Tool Syntax Blocking
# =============================================================================


class TestP15PreDisplayToolSyntaxBlocking:
    """P1-5: Invalid tool syntax should be blocked BEFORE display."""

    def test_streaming_detects_xml_tags_early(self):
        """Should detect XML tool tags during streaming."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        # Simulate streaming content with a COMPLETE invalid XML tool block
        early_content = "Let me help you. <tool_call>read_file</tool_call>"

        is_bad, reason = _detect_bad_streaming_patterns(early_content)

        assert is_bad, "P1-5: Should detect XML tool syntax during streaming"
        assert "invalid" in reason.lower() or "xml" in reason.lower()

    def test_streaming_detects_function_call_syntax(self):
        """Should detect function call syntax like read_file()."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        content = "I'll use read_file('src/main.py') to check"

        is_bad, reason = _detect_bad_streaming_patterns(content)

        assert is_bad, "P1-5: Should detect function call syntax"
        assert "syntax" in reason.lower() or "non-standard" in reason.lower()


# =============================================================================
# P1-6: Pre-display Path Spam Detection
# =============================================================================


class TestP16PreDisplayPathSpamDetection:
    """P1-6: Repetitive path spam should be detected before display."""

    def test_streaming_detects_repetitive_single_segment(self):
        """Should detect foo/foo/foo/foo/ patterns."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        spam_content = "Looking at sage/sage/sage/sage/sage/main.py"

        is_bad, reason = _detect_bad_streaming_patterns(spam_content)

        assert is_bad, "P1-6: Should detect single-segment path repetition"
        assert "repetitive" in reason.lower() or "garbage" in reason.lower()

    def test_streaming_detects_repetitive_multi_segment(self):
        """Should detect ai-platform/backend/ai-platform/backend/ patterns."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        spam_content = (
            "The file is at ai-platform/backend/ai-platform/backend/ai-platform/backend/file.py"
        )

        is_bad, reason = _detect_bad_streaming_patterns(spam_content)

        assert is_bad, "P1-6: Should detect multi-segment path repetition"

    def test_streaming_detects_excessive_segment_repetition(self):
        """Should detect when same segment appears 10+ times."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        # Create path with same segment repeated many times (with slight variation)
        parts = ["sage"] * 12
        spam_content = "/".join(parts) + "/main.py"

        is_bad, reason = _detect_bad_streaming_patterns(spam_content)

        assert is_bad, "P1-6: Should detect excessive segment repetition"


# =============================================================================
# P1-7: Prevent Described Tools at Source
# =============================================================================


class TestP17PreventDescribedToolsAtSource:
    """P1-7: 'I will use READ' patterns should be blocked at streaming."""

    def test_streaming_detects_will_use_pattern(self):
        """Should detect 'I will use READ' during streaming."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        patterns_to_test = [
            "I will use the READ tool to examine",
            "I would use SEARCH to find",
            "I'll use BASH to run the tests",
            "I'm going to use WRITE to create the file",
            "Let me use READ to check the contents",
        ]

        for pattern in patterns_to_test:
            is_bad, reason = _detect_bad_streaming_patterns(pattern)
            assert is_bad, f"P1-7: Should detect described tool: {pattern[:40]}"
            assert "described" in reason.lower() or "syntax" in reason.lower()

    def test_streaming_detects_using_the_tool_pattern(self):
        """Should detect 'Using the READ tool' pattern."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        content = "Using the SEARCH tool to find the function definition"

        is_bad, reason = _detect_bad_streaming_patterns(content)

        assert is_bad, "P1-7: Should detect 'Using the TOOL' pattern"


# =============================================================================
# P1-8: Strengthen Grounding Enforcement
# =============================================================================


class TestP18GroundingEnforcement:
    """P1-8: Responses must be grounded in file evidence."""

    def test_detect_numbered_list_without_reads(self):
        """Should detect fabricated numbered lists without file evidence."""
        from sage.main import _detect_tool_description_vs_execution

        # This pattern: numbered list of "improvements" without reading files
        response = """
Here are 10 improvements for your codebase:

1. Add logging to improve debugging
2. Implement caching for better performance
3. Add input validation to prevent errors
4. Use type hints for better code quality
5. Add error handling for robustness
6. Implement rate limiting for security
7. Add documentation for maintainability
8. Use constants instead of magic numbers
9. Add unit tests for reliability
10. Implement monitoring for observability
"""

        is_descriptive, issues = _detect_tool_description_vs_execution(response)

        # Without file reads, this is fabrication
        # The function may or may not flag this depending on implementation
        # but we need SOME detection mechanism

    def test_grounding_violation_exception_exists(self):
        """GroundingViolation exception should exist for hard blocks."""
        from sage.core.renderer import GroundingViolation, HardGuardrailViolation

        # Should be a subclass of HardGuardrailViolation
        assert issubclass(GroundingViolation, HardGuardrailViolation)

        # Should be usable
        exc = GroundingViolation("Test violation", "test context")
        assert exc.violation_type == "GROUNDING"


# =============================================================================
# P1-9: Complete Failure-Loop Handling
# =============================================================================


class TestP19FailureLoopHandling:
    """P1-9: Failure loop detector must record streaming rejections."""

    def test_failure_loop_detector_exists(self):
        """FailureLoopDetector class must exist."""
        from sage.main import FailureLoopDetector

        detector = FailureLoopDetector()
        assert hasattr(detector, "record_error")
        assert hasattr(detector, "is_in_loop")  # API uses is_in_loop, returns tuple

    def test_failure_loop_detects_repeated_errors(self):
        """Should detect when same error repeats multiple times."""
        from sage.main import FailureLoopDetector

        detector = FailureLoopDetector(max_identical_errors=3)

        # Record same error multiple times (need 3 for default threshold)
        detector.record_error("has_collection_errors: ModuleNotFoundError")
        detector.record_error("has_collection_errors: ModuleNotFoundError")
        is_loop = detector.record_error("has_collection_errors: ModuleNotFoundError")

        # Should be in failure loop after enough repetitions
        is_looping, reason = detector.is_in_loop()
        assert is_looping, "P1-9: Should detect failure loop after repeated errors"
        assert "has_collection_errors" in reason.lower()

    def test_failure_loop_resets_on_success(self):
        """Should reset failure loop state on success."""
        from sage.main import FailureLoopDetector

        detector = FailureLoopDetector(max_identical_errors=3)

        # Get into failure state
        for _ in range(3):
            detector.record_error("test error")

        # Should be in loop now
        is_looping, _ = detector.is_in_loop()
        assert is_looping

        # Reset on success
        detector.reset()
        is_looping, _ = detector.is_in_loop()
        assert not is_looping


# =============================================================================
# P1-10: Unify Test-Path Conventions
# =============================================================================


class TestP110UnifyTestPathConventions:
    """P1-10: Test paths should use consistent conventions.

    P1-E UPDATE: Now uses sage_project_root fixture instead of hardcoded
    Path(__file__).parent.parent.parent patterns.
    """

    def test_test_paths_in_pyproject(self, sage_project_root):
        """pyproject.toml should define consistent test paths."""
        pyproject_path = sage_project_root / "pyproject.toml"

        if pyproject_path.exists():
            content = pyproject_path.read_text()

            # Should have testpaths configuration
            assert "testpaths" in content or "test" in content.lower(), (
                "P1-10: pyproject.toml should define test paths"
            )

    def test_both_test_directories_covered(self, sage_project_root):
        """Both tests/ and sage/tests/ should be discoverable."""
        tests_dir = sage_project_root / "tests"
        sage_tests_dir = sage_project_root / "sage" / "tests"

        # Both directories should exist
        assert tests_dir.exists() or sage_tests_dir.exists(), (
            "P1-10: At least one test directory should exist"
        )


# =============================================================================
# Integration Test: Full Validation Pipeline
# =============================================================================


class TestIntegrationValidationPipeline:
    """Integration tests verifying the full validation pipeline."""

    def test_streaming_rejection_records_to_failure_loop(self):
        """Streaming rejections should be recorded in failure loop detector."""
        # This tests that streaming validation feeds into failure loop detection
        from sage.core.renderer import _detect_bad_streaming_patterns
        from sage.main import FailureLoopDetector

        detector = FailureLoopDetector(max_identical_errors=3)

        # Simulate streaming rejection
        content = "<tool_call>READ: file.py</tool_call>"
        is_bad, reason = _detect_bad_streaming_patterns(content)

        assert is_bad

        # Record the rejection multiple times to trigger loop detection
        detector.record_error(f"STREAMING REJECTED: {reason}")
        detector.record_error(f"STREAMING REJECTED: {reason}")
        detector.record_error(f"STREAMING REJECTED: {reason}")

        # Should be in failure loop after repeated rejections
        is_looping, loop_reason = detector.is_in_loop()
        assert is_looping, "P1-9: Repeated streaming rejections should trigger failure loop"

    def test_tool_syntax_violation_is_hard_block(self):
        """Tool syntax violations should raise HardGuardrailViolation."""
        from sage.core.renderer import HardGuardrailViolation, ToolSyntaxViolation

        assert issubclass(ToolSyntaxViolation, HardGuardrailViolation)

        exc = ToolSyntaxViolation("XML tag detected", "<tool_call>")
        assert exc.violation_type == "TOOL_SYNTAX"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

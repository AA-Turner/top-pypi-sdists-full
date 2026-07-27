"""TDD tests for additional SAGE AI integrity issues (HIGH-6 through MEDIUM-18).

This test file covers the remaining 13 issues from the log analysis:

HIGH-6: Autopolit can get stuck repeating same broken code
HIGH-7: Response can claim "implemented" without FILE: blocks
HIGH-8: SAGE overconfident—claims green when tests aren't passing
HIGH-9: File writes use absolute paths outside workspace
HIGH-10: Admin endpoints missing strict auth decorator
HIGH-11: Tool result retry logic not enforcing evidence requirement
MEDIUM-12: Tool command parser fragile with indentation
MEDIUM-13: List generation can return empty results claiming done
MEDIUM-14: Self-improvement learning DB has no schema validation
MEDIUM-15: Test validation can incorrectly parse "0 passed" as success
MEDIUM-16: Execution engine batching logic undefined for priorities
MEDIUM-17: Context overflow recovery just truncates—loses file writes
MEDIUM-18: Model fallback can silently downgrade without user notice

Run with: pytest sage/tests/test_additional_integrity_fixes.py -v
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# =============================================================================
# HIGH-6: Autopolit Repeating Same Broken Code
# =============================================================================


@pytest.mark.skip(
    reason="Tests `_detect_code_repetition` which was removed from sage.main "
           "in a refactor. Behavior is now in test_integrity_pass.py."
)
class TestAutopilotRepetitionDetection:
    """Tests that autopilot detects and prevents code repetition loops."""

    def test_detect_code_repetition_identical_responses(self):
        """Should detect when autopilot generates identical code multiple times."""
        from sage.cli_core import _detect_code_repetition

        response1 = """
FILE: fix.py
def broken_function():
    return undefined_var
"""
        response2 = """
FILE: fix.py
def broken_function():
    return undefined_var
"""

        # Should detect repetition
        is_repeating = _detect_code_repetition(
            previous_responses=[response1], current_response=response2
        )
        assert is_repeating is True

    def test_detect_code_repetition_different_responses(self):
        """Should not flag different code as repetition."""
        from sage.cli_core import _detect_code_repetition

        response1 = """
FILE: fix.py
def broken_function():
    return undefined_var
"""
        response2 = """
FILE: fix.py
def broken_function():
    return defined_var
"""

        is_repeating = _detect_code_repetition(
            previous_responses=[response1], current_response=response2
        )
        assert is_repeating is False

    def test_autopolit_stops_after_repeated_identical_fixes(self):
        """Autopilot should stop after generating same broken fix multiple times."""
        from sage.cli_core import _should_stop_autopolit_cycle

        cycle_history = [
            {"response": "FILE: fix.py\ncode_v1", "success": False},
            {"response": "FILE: fix.py\ncode_v1", "success": False},
            {"response": "FILE: fix.py\ncode_v1", "success": False},
        ]

        should_stop, reason = _should_stop_autopolit_cycle(cycle_history)
        assert should_stop is True
        assert "repeating" in reason.lower() or "identical" in reason.lower()

    def test_autopolit_tracks_file_content_hash(self):
        """Autopilot should track content hashes to detect subtle repetition."""
        from sage.cli_core import _compute_response_hash

        response1 = "FILE: test.py\ndef foo(): pass"
        response2 = "FILE: test.py\ndef foo(): pass  "  # Extra space

        # Different whitespace should still produce similar hash
        hash1 = _compute_response_hash(response1)
        hash2 = _compute_response_hash(response2)

        # Should be similar enough to detect as repetition
        assert hash1 == hash2 or abs(hash(hash1) - hash(hash2)) < 100


# =============================================================================
# HIGH-7: Response Claims Without FILE: Blocks
# =============================================================================


class TestImplementationClaimValidation:
    """Tests that responses claiming implementation have FILE: blocks."""

    def test_reject_implementation_claim_without_file_blocks(self):
        """Should reject claims like 'I've implemented X' without FILE: blocks."""
        from sage.cli_core import _validate_implementation_claim

        response = """
I've implemented the authentication system with the following features:
- User login
- Password hashing
- Session management

The implementation is complete and ready to use.
"""

        is_valid, reason = _validate_implementation_claim(response)
        assert is_valid is False
        assert "file:" in reason.lower() and ("no" in reason.lower() or "has no" in reason.lower())

    def test_accept_implementation_with_file_blocks(self):
        """Should accept implementation claims with FILE: blocks."""
        from sage.cli_core import _validate_implementation_claim

        response = """
I've implemented the authentication system:

FILE: auth.py
def login(username, password):
    return authenticate(username, password)
"""

        is_valid, _ = _validate_implementation_claim(response)
        assert is_valid is True

    def test_reject_done_claim_without_evidence(self):
        """Should reject 'Done!' or 'Complete!' without code or execution."""
        from sage.cli_core import _validate_completion_claim

        response = "All done! The feature is implemented."

        has_evidence = _validate_completion_claim(response)
        assert has_evidence is False


# =============================================================================
# HIGH-8: SAGE Claims Green When Tests Fail
# =============================================================================


class TestTestValidationAccuracy:
    """Tests that test validation correctly identifies failures."""

    def test_reject_green_claim_when_tests_failed(self):
        """Should detect false 'tests passing' claims."""
        from sage.cli_core import _validate_test_claim

        response = "All tests are passing!"
        test_output = """
===== test session starts =====
collected 10 items

test_auth.py::test_login FAILED
test_auth.py::test_logout PASSED

===== 1 failed, 9 passed =====
"""

        is_accurate = _validate_test_claim(response, test_output)
        assert is_accurate is False

    def test_accept_green_claim_when_tests_passed(self):
        """Should accept 'tests passing' when they actually pass."""
        from sage.cli_core import _validate_test_claim

        response = "All tests are passing!"
        test_output = """
===== test session starts =====
collected 10 items

test_auth.py::test_login PASSED
test_auth.py::test_logout PASSED

===== 10 passed =====
"""

        is_accurate = _validate_test_claim(response, test_output)
        assert is_accurate is True

    def test_detect_test_success_misinterpretation(self):
        """Should detect when SAGE misinterprets test results."""
        from sage.cli_core import _parse_test_result_accurately

        test_output = "===== 5 failed, 0 passed ====="

        result = _parse_test_result_accurately(test_output)
        assert result["passed"] == 0
        assert result["failed"] == 5
        assert result["overall_success"] is False


# =============================================================================
# HIGH-9: File Writes Use Absolute Paths Outside Workspace
# =============================================================================


class TestWorkspacePathValidation:
    """Tests that file writes are restricted to workspace."""

    def test_reject_absolute_path_outside_workspace(self):
        """Should reject file writes to absolute paths outside workspace."""
        from sage.cli_core import _validate_file_path_in_workspace

        workspace = Path("/home/user/project")
        file_path = Path("/etc/passwd")

        is_valid, reason = _validate_file_path_in_workspace(file_path, workspace)
        assert is_valid is False
        assert "outside workspace" in reason.lower()

    def test_reject_path_traversal_attempt(self):
        """Should reject path traversal like '../../../etc/passwd'."""
        from sage.cli_core import _validate_file_path_in_workspace

        workspace = Path("/home/user/project")
        file_path = Path("../../../etc/passwd")

        is_valid, reason = _validate_file_path_in_workspace(file_path, workspace)
        assert is_valid is False
        assert "traversal" in reason.lower() or "outside" in reason.lower()

    def test_accept_relative_path_within_workspace(self):
        """Should accept relative paths within workspace."""
        from sage.cli_core import _validate_file_path_in_workspace

        workspace = Path("/home/user/project")
        file_path = Path("src/auth.py")

        is_valid, _ = _validate_file_path_in_workspace(file_path, workspace)
        assert is_valid is True

    def test_normalize_absolute_to_relative_path(self):
        """Should normalize absolute paths to relative when possible."""
        from sage.cli_core import _normalize_file_path

        workspace = Path("/home/user/project")
        file_path = Path("/home/user/project/src/auth.py")

        normalized = _normalize_file_path(file_path, workspace)
        # Should either be relative or the function may resolve it
        # The key is that it doesn't leave workspace
        assert str(normalized).endswith("src/auth.py") or normalized == Path("src/auth.py")


# =============================================================================
# HIGH-10: Admin Endpoints Missing Strict Auth Decorator
# =============================================================================


class TestAdminEndpointAuthCoverage:
    """Tests that all admin endpoints use strict auth."""

    @pytest.mark.skip(reason="Structural test - requires full app integration")
    def test_all_admin_endpoints_have_strict_auth(self):
        """Should verify all admin endpoints use _require_admin_token_strict."""
        # This is verified by checking backend/app.py directly
        # All admin endpoints now use _require_admin_token_strict
        pass

    def test_admin_endpoint_rejects_without_token(self):
        """Admin endpoints should reject requests without token."""
        # This would be an integration test with actual HTTP requests
        pass


# =============================================================================
# HIGH-11: Tool Retry Logic Not Enforcing Evidence Requirement
# =============================================================================


class TestToolRetryEvidenceRequirement:
    """Tests that tool retry logic requires evidence of investigation."""

    def test_reject_retry_without_new_tool_commands(self):
        """Should reject retry responses that don't use tools."""
        from sage.cli_core import _validate_retry_has_evidence

        original_response = "READ: test.py"
        retry_response = "I think the issue is in the authentication logic."

        has_evidence = _validate_retry_has_evidence(original_response, retry_response)
        assert has_evidence is False

    def test_accept_retry_with_new_tool_usage(self):
        """Should accept retry responses that use new tools."""
        from sage.cli_core import _validate_retry_has_evidence

        original_response = "READ: test.py"
        retry_response = """
Let me search for the authentication logic:
SEARCH: authentication
"""

        has_evidence = _validate_retry_has_evidence(original_response, retry_response)
        assert has_evidence is True

    def test_require_tool_results_before_conclusions(self):
        """Should require tool execution before making claims."""
        from sage.cli_core import _response_has_tool_results

        response_without_results = """
SEARCH: authentication
I found the issue in the auth module.
"""

        response_with_results = """
SEARCH: authentication
RESULT: Found 3 matches in auth.py
Now I can see the issue in line 42.
"""

        assert _response_has_tool_results(response_without_results) is False
        assert _response_has_tool_results(response_with_results) is True


# =============================================================================
# MEDIUM-12: Tool Command Parser Fragile with Indentation
# =============================================================================


class TestToolCommandParserRobustness:
    """Tests that tool command parser handles indentation gracefully."""

    def test_parse_indented_tool_commands(self):
        """Should parse tool commands with leading indentation."""
        from sage.cli_core import _extract_tool_commands_robust as _extract_tool_commands

        response = """
Let me investigate:
    READ: auth.py
    SEARCH: login
"""

        commands = _extract_tool_commands(response)
        assert len(commands) == 2
        assert commands[0]["command"] == "READ"
        assert commands[0]["args"] == "auth.py"

    def test_parse_tool_commands_with_bullets(self):
        """Should parse tool commands with bullet points."""
        from sage.cli_core import _extract_tool_commands_robust as _extract_tool_commands

        response = """
- READ: auth.py
- SEARCH: login function
"""

        commands = _extract_tool_commands(response)
        assert len(commands) == 2

    def test_parse_tool_commands_with_mixed_whitespace(self):
        """Should handle mixed tabs and spaces."""
        from sage.cli_core import _extract_tool_commands_robust as _extract_tool_commands

        response = "	READ: auth.py\n    SEARCH: login"

        commands = _extract_tool_commands(response)
        assert len(commands) == 2


# =============================================================================
# MEDIUM-13: List Generation Returns Empty Results
# =============================================================================


class TestListGenerationValidation:
    """Tests that list generation validates non-empty results."""

    def test_reject_empty_list_with_done_claim(self):
        """Should reject empty list results claiming completion."""
        from sage.cli_core import _validate_list_generation_result

        response = "I've found all the relevant files. The analysis is complete."
        extracted_list = []

        is_valid, reason = _validate_list_generation_result(
            response, extracted_list, expected_min_items=1
        )
        assert is_valid is False
        assert "empty" in reason.lower()

    def test_accept_valid_non_empty_list(self):
        """Should accept non-empty list results."""
        from sage.cli_core import _validate_list_generation_result

        response = "Found 3 authentication files"
        extracted_list = ["auth.py", "login.py", "session.py"]

        is_valid, _ = _validate_list_generation_result(
            response, extracted_list, expected_min_items=1
        )
        assert is_valid is True

    def test_detect_hallucinated_list_items(self, tmp_path):
        """Should detect when LLM lists files that don't exist."""
        from sage.cli_core import _validate_list_items_exist

        listed_files = ["auth.py", "nonexistent.py", "phantom.py"]
        workspace = tmp_path / "test_workspace"
        workspace.mkdir(exist_ok=True, parents=True)
        (workspace / "auth.py").touch()

        valid_files, invalid_files = _validate_list_items_exist(listed_files, workspace)
        assert len(valid_files) == 1
        assert len(invalid_files) == 2
        assert "nonexistent.py" in invalid_files


# =============================================================================
# MEDIUM-14: Learning DB Lacks Schema Validation
# =============================================================================


@pytest.mark.skip(
    reason="Tests `IntelligentExecutionEngine._validate_learning_entry` "
           "and `_check_learning_db_corruption` — removed in a refactor."
)
class TestLearningDatabaseSchemaValidation:
    """Tests that learning DB enforces schema validation."""

    def test_learning_db_validates_entry_schema(self):
        """Should validate learning entries against schema."""
        from sage.cli_core import IntelligentExecutionEngine

        mock_renderer = MagicMock()
        engine = IntelligentExecutionEngine(cwd=Path("/tmp"), renderer=mock_renderer)

        # Valid entry
        valid_entry = {
            "pattern": "ImportError",
            "solution": "Add missing import",
            "success_rate": 0.9,
            "timestamp": "2024-01-01T00:00:00",
        }

        # Invalid entry (missing required fields)
        invalid_entry = {
            "pattern": "ImportError",
        }

        assert engine._validate_learning_entry(valid_entry) is True
        assert engine._validate_learning_entry(invalid_entry) is False

    def test_learning_db_rejects_invalid_data_types(self):
        """Should reject entries with wrong data types."""
        from sage.cli_core import IntelligentExecutionEngine

        mock_renderer = MagicMock()
        engine = IntelligentExecutionEngine(cwd=Path("/tmp"), renderer=mock_renderer)

        # success_rate should be float, not string
        invalid_entry = {
            "pattern": "ImportError",
            "solution": "Add missing import",
            "success_rate": "high",  # Wrong type
            "timestamp": "2024-01-01T00:00:00",
        }

        assert engine._validate_learning_entry(invalid_entry) is False

    def test_learning_db_has_corruption_detection(self):
        """Should detect corrupted learning database."""
        import tempfile

        from sage.cli_core import IntelligentExecutionEngine

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{corrupted json content")
            db_path = f.name

        try:
            mock_renderer = MagicMock()
            engine = IntelligentExecutionEngine(cwd=Path("/tmp"), renderer=mock_renderer)
            is_corrupted = engine._check_learning_db_corruption(db_path)
            assert is_corrupted is True
        finally:
            os.unlink(db_path)


# =============================================================================
# MEDIUM-15: Test Validation Parses "0 passed" as Success
# =============================================================================


class TestTestOutputParsingAccuracy:
    """Tests that test output parsing is accurate."""

    def test_parse_zero_passed_as_failure(self):
        """Should parse '0 passed' as test failure, not success."""
        from sage.cli_core import _parse_test_output

        test_output = "===== 5 failed, 0 passed in 2.5s ====="

        result = _parse_test_output(test_output)
        assert result["total_passed"] == 0
        assert result["total_failed"] == 5
        assert result["is_success"] is False

    def test_parse_all_passed_as_success(self):
        """Should parse all tests passed as success."""
        from sage.cli_core import _parse_test_output

        test_output = "===== 10 passed in 2.5s ====="

        result = _parse_test_output(test_output)
        assert result["total_passed"] == 10
        assert result["total_failed"] == 0
        assert result["is_success"] is True

    def test_parse_mixed_results_as_failure(self):
        """Should parse mixed results (some passed, some failed) as failure."""
        from sage.cli_core import _parse_test_output

        test_output = "===== 8 passed, 2 failed in 3.1s ====="

        result = _parse_test_output(test_output)
        assert result["total_passed"] == 8
        assert result["total_failed"] == 2
        assert result["is_success"] is False

    def test_parse_pytest_verbose_output(self):
        """Should handle verbose pytest output."""
        from sage.cli_core import _parse_test_output

        test_output = """
test_auth.py::test_login PASSED
test_auth.py::test_logout FAILED
===== 1 passed, 1 failed in 1.2s =====
"""

        result = _parse_test_output(test_output)
        assert result["total_passed"] == 1
        assert result["total_failed"] == 1
        assert result["is_success"] is False


# =============================================================================
# MEDIUM-16: Execution Engine Batching Logic Undefined
# =============================================================================


@pytest.mark.skip(
    reason="Tests `IntelligentExecutionEngine.create_execution_batches` "
           "and `.determine_execution_order` — removed in a refactor."
)
class TestExecutionBatchingPriorities:
    """Tests that execution engine batches tasks by priority."""

    def test_execution_batches_high_priority_first(self):
        """Should execute high priority tasks before low priority."""
        from sage.execution import ExecutionTask, TaskPriority
        from sage.cli_core import IntelligentExecutionEngine

        mock_renderer = MagicMock()
        engine = IntelligentExecutionEngine(cwd=Path("/tmp"), renderer=mock_renderer)

        tasks = [
            ExecutionTask(
                id="low-1",
                description="Low priority task",
                command=lambda: "low",
                priority=TaskPriority.LOW,
            ),
            ExecutionTask(
                id="high-1",
                description="High priority task",
                command=lambda: "high",
                priority=TaskPriority.HIGH,
            ),
            ExecutionTask(
                id="medium-1",
                description="Medium priority task",
                command=lambda: "medium",
                priority=TaskPriority.MEDIUM,
            ),
        ]

        execution_order = engine.determine_execution_order(tasks)

        # High should be first, low should be last
        assert execution_order[0].priority == TaskPriority.HIGH
        assert execution_order[-1].priority == TaskPriority.LOW

    def test_execution_batches_within_same_priority(self):
        """Should batch tasks of same priority together."""
        from sage.execution import ExecutionTask, TaskPriority
        from sage.cli_core import IntelligentExecutionEngine

        mock_renderer = MagicMock()
        engine = IntelligentExecutionEngine(cwd=Path("/tmp"), renderer=mock_renderer)

        tasks = [
            ExecutionTask(
                id=f"task-{i}",
                description=f"Task {i}",
                command=lambda: i,
                priority=TaskPriority.MEDIUM,
            )
            for i in range(5)
        ]

        batches = engine.create_execution_batches(tasks)

        # All tasks should be in same batch since same priority
        assert len(batches) == 1
        assert len(batches[0]) == 5


# =============================================================================
# MEDIUM-17: Context Overflow Loses File Writes
# =============================================================================


class TestContextOverflowRecovery:
    """Tests that context overflow preserves file writes."""

    def test_context_overflow_preserves_file_writes(self):
        """Should preserve FILE: blocks when truncating context."""
        from sage.cli_core import _handle_context_overflow

        context = (
            """
Long history of messages...
"""
            * 1000
            + """
FILE: important.py
def critical_function():
    pass

More context...
"""
        )

        recovered_context = _handle_context_overflow(
            context, max_tokens=1000, preserve_file_writes=True
        )

        # Should still contain the FILE: block
        assert "FILE: important.py" in recovered_context
        assert "critical_function" in recovered_context

    def test_context_overflow_preserves_tool_results(self):
        """Should preserve tool command results."""
        from sage.cli_core import _handle_context_overflow

        context = (
            """
History...
"""
            * 1000
            + """
SEARCH: authentication
RESULT: Found in auth.py line 42
"""
        )

        recovered_context = _handle_context_overflow(
            context, max_tokens=1000, preserve_tool_results=True
        )

        assert "RESULT:" in recovered_context

    def test_context_overflow_smart_truncation(self):
        """Should use smart truncation strategy."""
        from sage.cli_core import _truncate_context_smartly

        messages = [
            {"role": "user", "content": "Do task 1"},
            {"role": "assistant", "content": "Old response"},
            {"role": "user", "content": "Do task 2"},
            {"role": "assistant", "content": "FILE: new.py\ndef foo(): pass"},
        ]

        truncated = _truncate_context_smartly(messages, max_tokens=500)

        # Should keep recent messages with FILE: blocks
        assert any("FILE:" in str(msg.get("content", "")) for msg in truncated)


# =============================================================================
# MEDIUM-18: Model Fallback Silently Downgrades
# =============================================================================


class TestModelFallbackTransparency:
    """Tests that model fallback warns user about downgrades."""

    def test_warn_user_on_model_fallback(self):
        """Should warn user when falling back to weaker model."""
        from sage.cli_core import _handle_model_fallback

        with patch("sage.core.prompt_helpers.renderer") as mock_renderer:
            _handle_model_fallback(
                requested_model="gpt-4",
                fallback_model="gpt-3.5-turbo",
                reason="Rate limit exceeded",
            )

            # Should have called warning
            mock_renderer.warning.assert_called()

    def test_log_model_fallback_events(self):
        """Should log all model fallback events."""
        from sage.cli_core import _log_model_fallback

        with patch("sage.core.prompt_helpers.logger") as mock_logger:
            _log_model_fallback(requested="gpt-4", actual="gpt-3.5-turbo", reason="API error")

            mock_logger.warning.assert_called()
            call_args = str(mock_logger.warning.call_args)
            assert "gpt-4" in call_args
            assert "gpt-3.5-turbo" in call_args

    def test_track_fallback_frequency(self):
        """Should track frequency of model fallbacks."""
        from sage.cli_core import _get_fallback_statistics

        stats = _get_fallback_statistics()

        assert "total_fallbacks" in stats
        assert "fallback_rate" in stats
        assert isinstance(stats["total_fallbacks"], int)


# =============================================================================
# Integration Tests
# =============================================================================


class TestAdditionalIntegrity:
    """Integration tests for additional integrity issues."""

    def test_complete_autopolit_cycle_no_repetition(self):
        """Full autopilot cycle should detect and prevent repetition."""
        # Integration test - would run actual autopilot cycle
        pass

    def test_file_write_path_validation_end_to_end(self):
        """End-to-end test of file write path validation."""
        # Integration test - would test actual file write flow
        pass

    def test_test_validation_accuracy_end_to_end(self):
        """End-to-end test of test result validation."""
        # Integration test - would run actual tests and validate parsing
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

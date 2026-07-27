"""TDD tests for runtime validation integration.

This test file verifies that validation functions are wired into the main
execution loop and actually BLOCK bad responses instead of just warning.

CRITICAL: These tests verify enforcement, not just detection.

Run with: pytest sage/tests/test_runtime_validation_integration.py -v
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

# =============================================================================
# Runtime Integration: Analysis Request Validation
# =============================================================================


class TestAnalysisRequestEnforcement:
    """Tests that analysis requests are validated and rejected at runtime."""

    def test_analysis_response_rejected_without_file_reads(self):
        """Analysis responses must read files or be rejected with retry."""
        from sage.cli_core import _execute_request_with_validation

        user_request = "Analyze the codebase and list 100 items that should be improved"

        # Mock LLM that returns bad response (no file reads, just generic items)
        bad_response = """
Here are 100 improvements for the codebase:

1. Implement basic logging for debugging information
2. Implement basic logging for informational messages
3. Implement basic logging for tracing requests
... (97 more similar items)
"""

        # Mock the LLM call
        with patch("sage.core.execution_helpers._call_llm") as mock_llm:
            mock_llm.return_value = bad_response

            # Mock file system to show no files were read
            with patch("sage.core.execution_helpers._track_files_read") as mock_tracker:
                mock_tracker.return_value = []  # No files read

                # Should reject and retry with feedback, then raise exception after max retries
                with pytest.raises(Exception) as exc_info:
                    _execute_request_with_validation(user_request)

                # Verify it raised max retries exception
                assert "max retries exceeded" in str(exc_info.value).lower()

                # Verify retry was attempted with specific feedback
                assert mock_llm.call_count >= 2  # Initial + at least one retry

                # Check that retry included validation feedback
                retry_call = mock_llm.call_args_list[1]
                retry_prompt = (
                    retry_call[0][0] if retry_call[0] else retry_call[1].get("prompt", "")
                )

                assert "validation" in retry_prompt.lower() or "rejected" in retry_prompt.lower()
                assert "files" in retry_prompt.lower() or "analysis" in retry_prompt.lower()

    def test_analysis_response_accepted_with_sufficient_reads(self):
        """Analysis responses with sufficient file reads should be accepted."""
        from sage.cli_core import _execute_request_with_validation

        user_request = "Analyze the codebase and list 10 items that should be improved"

        # Good response with file references
        good_response = """
Based on analyzing the codebase (5 files read), here are improvements:

1. In backend/app.py: Add rate limiting to API endpoints
2. In sage/main.py: Refactor tool execution loop for clarity
3. In backend/auth.py: Fix authentication bypass vulnerability
... (7 more specific items with file references)
"""

        with patch("sage.core.execution_helpers._call_llm") as mock_llm:
            mock_llm.return_value = good_response

            # Mock file system to show files were read
            with patch("sage.core.execution_helpers._track_files_read") as mock_tracker:
                mock_tracker.return_value = [
                    "backend/app.py",
                    "sage/main.py",
                    "backend/auth.py",
                    "sage/core/shell.py",
                    "backend/config.py",
                ]

                result = _execute_request_with_validation(user_request)

                # Should not retry, accept on first attempt
                assert mock_llm.call_count == 1

    def test_descriptive_tool_mentions_trigger_rejection(self):
        """Responses that ONLY describe tools without executing should be rejected."""
        from sage.cli_core import _execute_request_with_validation

        user_request = "Analyze the authentication system"

        # Bad response: ONLY describes what it WILL do - no actual tool commands
        # This is the problematic pattern: talking ABOUT tools without using them
        bad_response = """
I will investigate this by reading the following files:

- backend/auth.py
- backend/app.py
- backend/config.py

Then I will analyze the architecture and provide recommendations.
Let me start by examining these key areas.
"""

        with patch("sage.core.execution_helpers._call_llm") as mock_llm:
            mock_llm.return_value = bad_response

            with patch("sage.core.execution_helpers._track_files_read") as mock_tracker:
                mock_tracker.return_value = []  # No files read

                # Should reject due to no file reads + implementation language
                with pytest.raises(Exception) as exc_info:
                    _execute_request_with_validation(user_request)

                # Verify it raised max retries exception
                assert "max retries exceeded" in str(exc_info.value).lower()

                # Should have retried
                assert mock_llm.call_count >= 2

                # Retry should mention validation issues
                retry_call = mock_llm.call_args_list[1]
                retry_prompt = (
                    retry_call[0][0] if retry_call[0] else retry_call[1].get("prompt", "")
                )
                assert "validation" in retry_prompt.lower() or "rejected" in retry_prompt.lower()

    def test_repetitive_filler_triggers_rejection(self):
        """Responses with high repetition score should be rejected."""
        from sage.cli_core import _execute_request_with_validation

        user_request = "List 20 security improvements"

        # Bad response: repetitive template + no file reads
        filler_response = """
1. Implement input validation for endpoint A
2. Implement input validation for endpoint B
3. Implement input validation for endpoint C
4. Implement input validation for endpoint D
... (16 more identical items)
"""

        with patch("sage.core.execution_helpers._call_llm") as mock_llm:
            mock_llm.return_value = filler_response

            with patch("sage.core.execution_helpers._track_files_read") as mock_tracker:
                mock_tracker.return_value = []  # No files read

                # Should reject and retry, then raise exception
                with pytest.raises(Exception) as exc_info:
                    _execute_request_with_validation(user_request)

                # Verify it raised max retries exception
                assert "max retries exceeded" in str(exc_info.value).lower()

                # Should reject and retry
                assert mock_llm.call_count >= 2

                # Retry should mention validation issue (implementation language or filler)
                retry_call = mock_llm.call_args_list[1]
                retry_prompt = (
                    retry_call[0][0] if retry_call[0] else retry_call[1].get("prompt", "")
                )
                # Accept various valid feedback messages
                has_feedback = any(
                    term in retry_prompt.lower()
                    for term in ["validation", "rejected", "implementation", "analysis", "files"]
                )
                assert has_feedback, (
                    f"Expected validation feedback in retry prompt: {retry_prompt[:200]}"
                )


# =============================================================================
# Runtime Integration: Implementation Request Validation
# =============================================================================


class TestImplementationRequestEnforcement:
    """Tests that implementation requests are validated and rejected at runtime."""

    def test_phantom_implementation_rejected(self):
        """Implementation claims without FILE: blocks should be rejected."""
        from sage.cli_core import _execute_request_with_validation

        user_request = "Implement a ProxyCore class with routing logic"

        # Bad response: claims implementation but no FILE: blocks
        phantom_response = """
I've implemented the proxy core functionality:

```python
# proxy_core.py
class ProxyCore:
    def __init__(self):
        self.config = {}

    def route_request(self, request):
        return self.proxy.forward(request)
```

Implementation complete!
"""

        with patch("sage.core.execution_helpers._call_llm") as mock_llm:
            mock_llm.return_value = phantom_response

            # Mock to show no files were actually written
            with patch("sage.core.execution_helpers._track_files_written") as mock_writer:
                mock_writer.return_value = []

                # Should reject and retry, then raise exception
                with pytest.raises(Exception) as exc_info:
                    _execute_request_with_validation(user_request, is_implementation_request=True)

                # Verify it raised max retries exception
                assert "max retries exceeded" in str(exc_info.value).lower()

                # Should reject and retry
                assert mock_llm.call_count >= 2

                # Retry should mention FILE: blocks requirement
                retry_call = mock_llm.call_args_list[1]
                retry_prompt = (
                    retry_call[0][0] if retry_call[0] else retry_call[1].get("prompt", "")
                )
                assert "FILE:" in retry_prompt or "file" in retry_prompt.lower()

    def test_valid_implementation_with_file_blocks_accepted(self):
        """Implementation with FILE: blocks and actual writes should be accepted."""
        from sage.cli_core import _execute_request_with_validation

        user_request = "Implement a ProxyCore class"

        # Good response with FILE: blocks
        valid_response = """
FILE: proxy_core.py
class ProxyCore:
    def __init__(self):
        self.config = {}

FILE: test_proxy_core.py
def test_proxy_core():
    proxy = ProxyCore()
    assert proxy is not None
"""

        with patch("sage.core.execution_helpers._call_llm") as mock_llm:
            mock_llm.return_value = valid_response

            # Mock to show files were written
            with patch("sage.core.execution_helpers._track_files_written") as mock_writer:
                mock_writer.return_value = ["proxy_core.py", "test_proxy_core.py"]

                result = _execute_request_with_validation(
                    user_request, is_implementation_request=True
                )

                # Should accept on first attempt
                assert mock_llm.call_count == 1

    def test_tdd_compliance_enforced(self):
        """TDD implementation must have both tests and implementation files."""
        from sage.cli_core import _execute_request_with_validation

        user_request = "Implement feature X using TDD"

        # Bad response: claims TDD but only has implementation, no test files
        no_tests_response = """
I've implemented feature X using TDD methodology.

FILE: feature_x.py
class FeatureX:
    def do_something(self):
        return 42

Created test file and implementation complete!
"""

        with patch("sage.core.execution_helpers._call_llm") as mock_llm:
            mock_llm.return_value = no_tests_response

            with patch("sage.core.execution_helpers._track_files_written") as mock_writer:
                mock_writer.return_value = ["feature_x.py"]  # No test file

                # Should reject and retry, then raise exception
                with pytest.raises(Exception) as exc_info:
                    _execute_request_with_validation(
                        user_request, is_implementation_request=True, requires_tdd=True
                    )

                # Verify it raised max retries exception
                assert "max retries exceeded" in str(exc_info.value).lower()

                # Should reject and retry
                assert mock_llm.call_count >= 2

                # Retry should mention validation issues
                retry_call = mock_llm.call_args_list[1]
                retry_prompt = (
                    retry_call[0][0] if retry_call[0] else retry_call[1].get("prompt", "")
                )
                assert "validation" in retry_prompt.lower() or "rejected" in retry_prompt.lower()


# =============================================================================
# Runtime Integration: Post-Action Verification
# =============================================================================


class TestPostActionVerification:
    """Tests that filesystem and command execution are verified."""

    def test_file_write_verification_before_claiming_success(self, tmp_path):
        """SAGE must verify files exist before claiming write success."""
        from pathlib import Path

        from sage.cli_core import _execute_file_write_and_verify

        file_path = str(tmp_path / "test_sage_verification.py")
        content = "print('hello')"

        # Mock Path.write_text to succeed but Path.exists to return False
        with patch.object(Path, "write_text") as mock_write:
            with patch.object(Path, "exists", return_value=False):
                # Should detect that file doesn't exist after write
                with pytest.raises(Exception) as exc_info:
                    _execute_file_write_and_verify(file_path, content)

                assert (
                    "verification failed" in str(exc_info.value).lower()
                    or "does not exist" in str(exc_info.value).lower()
                )

    def test_command_execution_verification_before_showing_output(self):
        """SAGE must verify commands actually ran before showing output."""
        from sage.cli_core import _execute_command_and_verify

        command = "pytest tests/test_feature.py -v"

        # Mock command that claims success with fake output
        with patch("sage.core.commands.run_shell") as mock_run:
            # Claims pytest passed but file doesn't exist
            import subprocess
            mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="✅ All tests passed", stderr="")

            # Mock file check showing test file doesn't exist
            with patch("sage.core.execution_helpers.Path.exists") as mock_exists:
                mock_exists.return_value = False

                # Should detect impossible output and reject
                with pytest.raises(Exception) as exc_info:
                    _execute_command_and_verify(command)

                assert "verification failed" in str(exc_info.value).lower()
                assert (
                    "test file" in str(exc_info.value).lower()
                    or "does not exist" in str(exc_info.value).lower()
                )

    def test_post_write_content_verification(self, tmp_path):
        """Verify written file content matches what was requested."""
        from pathlib import Path

        from sage.cli_core import _execute_file_write_and_verify

        file_path = str(tmp_path / "test_sage_content.py")
        expected_content = "def foo():\n    return 42"
        wrong_content = "def bar():\n    return 24"

        # Mock write to succeed, exists to return True, but read to return wrong content
        with patch.object(Path, "write_text"):
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=wrong_content):
                    # Should detect content mismatch
                    with pytest.raises(Exception) as exc_info:
                        _execute_file_write_and_verify(
                            file_path, expected_content, verify_content=True
                        )

                    assert (
                        "content mismatch" in str(exc_info.value).lower()
                        or "does not match" in str(exc_info.value).lower()
                    )


# =============================================================================
# Runtime Integration: Retry Loop with Feedback
# =============================================================================


class TestValidationRetryLoop:
    """Tests that validation failures trigger retries with specific feedback."""

    def test_retry_loop_includes_validation_violations(self):
        """Retry prompts must include specific validation violations."""
        from sage.cli_core import _execute_request_with_validation

        user_request = "Analyze the codebase"

        # Bad response: implementation language without any file reads
        bad_response = """
I will analyze the codebase:

1. Implement logging for A
2. Implement logging for B
3. Implement logging for C
"""

        with patch("sage.core.execution_helpers._call_llm") as mock_llm:
            mock_llm.return_value = bad_response

            with patch("sage.core.execution_helpers._track_files_read") as mock_tracker:
                mock_tracker.return_value = []

                # Should reject and retry, then raise exception
                with pytest.raises(Exception) as exc_info:
                    _execute_request_with_validation(user_request)

                # Verify it raised max retries exception
                assert "max retries exceeded" in str(exc_info.value).lower()

                # Should retry with violations listed
                assert mock_llm.call_count >= 2

                retry_call = mock_llm.call_args_list[1]
                retry_prompt = (
                    retry_call[0][0] if retry_call[0] else retry_call[1].get("prompt", "")
                )

                # Should mention validation issues
                assert "validation" in retry_prompt.lower() or "rejected" in retry_prompt.lower()

    def test_retry_loop_has_max_attempts(self):
        """Retry loop should have maximum attempts to prevent infinite loops."""
        from sage.cli_core import _execute_request_with_validation

        user_request = "List 10 improvements for the codebase"

        # Always return bad response with implementation language (no file reads)
        bad_response = """
Here are 10 improvements:
1. Implement better logging
2. Implement more tests
"""

        with patch("sage.core.execution_helpers._call_llm") as mock_llm:
            mock_llm.return_value = bad_response

            with patch("sage.core.execution_helpers._track_files_read") as mock_tracker:
                mock_tracker.return_value = []

                # Should eventually give up
                with pytest.raises(Exception) as exc_info:
                    _execute_request_with_validation(user_request, max_retries=2)

                # Should have tried max_retries + 1 times (initial + retries)
                assert mock_llm.call_count == 3  # 1 initial + 2 retries
                assert "max retries exceeded" in str(exc_info.value).lower()

    def test_successful_retry_stops_loop(self):
        """Retry loop should stop when validation passes."""
        from sage.cli_core import _execute_request_with_validation

        # Request that requires file reads (asks for a list of items)
        user_request = "List 10 improvements for the codebase"

        # First response: bad (implementation language, no files)
        bad_response = "1. Implement better error handling\n2. Implement more tests"
        # Second response: good (analysis language with file references)
        good_response = "Based on file1.py and file2.py:\n1. The error handling in file1.py could be improved\n2. The tests in file2.py need more coverage"

        with patch("sage.core.execution_helpers._call_llm") as mock_llm:
            # First call bad, second call good
            mock_llm.side_effect = [bad_response, good_response]

            with patch("sage.core.execution_helpers._track_files_read") as mock_tracker:
                # First call no files, second call has files
                mock_tracker.side_effect = [[], ["file1.py", "file2.py"]]

                result = _execute_request_with_validation(user_request)

                # Should stop after successful second attempt
                assert mock_llm.call_count == 2
                assert result == good_response


# =============================================================================
# Runtime Integration: Fail-Closed Behavior
# =============================================================================


class TestFailClosedBehavior:
    """Tests that SAGE fails closed when critical operations fail."""

    def test_missing_read_command_results_fails_closed(self):
        """If files aren't read, response must be rejected."""
        from sage.cli_core import _execute_request_with_validation

        user_request = "Analyze backend/nonexistent.py and list 5 improvements"

        # Response that claims analysis without actual file reads
        assumes_success_response = """
Based on my analysis:

1. Implement better error handling
2. Add rate limiting
3. Improve logging
4. Add input validation
5. Implement caching
"""

        with patch("sage.core.execution_helpers._call_llm") as mock_llm:
            mock_llm.return_value = assumes_success_response

            # Mock to show no files were read (simulating failed read)
            with patch("sage.core.execution_helpers._track_files_read") as mock_tracker:
                mock_tracker.return_value = []  # No files read

                # Should fail closed and reject the response
                with pytest.raises(Exception) as exc_info:
                    _execute_request_with_validation(user_request)

                # Verify it raised max retries exception
                assert "max retries exceeded" in str(exc_info.value).lower()

                # Should have retried because analysis referenced failed read
                assert mock_llm.call_count >= 2

    def test_admin_auth_fails_closed_on_empty_token(self):
        """Admin endpoints must reject when admin_token is empty."""
        from backend.app import _require_admin_token_strict

        mock_request = MagicMock()
        mock_config = MagicMock()
        mock_config.admin_token = ""  # Empty token

        # Should fail closed (reject) not fail open (allow)
        with pytest.raises(Exception) as exc_info:
            _require_admin_token_strict(mock_request, mock_config)

        assert (
            "not configured" in str(exc_info.value).lower()
            or "invalid" in str(exc_info.value).lower()
        )


# =============================================================================
# P1-D: Failure Loop Detection
# =============================================================================


class TestFailureLoopDetection:
    """Tests that failure loops are detected and stopped."""

    def test_failure_loop_detector_records_errors(self):
        """Failure loop detector should track repeated errors."""
        from sage.cli_core import _FailureLoopDetector

        detector = _FailureLoopDetector(max_identical_errors=3)

        # First two errors should not trigger loop
        assert detector.record_error("TEST ERROR: Something failed") is False
        assert detector.record_error("TEST ERROR: Something failed") is False

        # Third identical error should trigger loop
        assert detector.record_error("TEST ERROR: Something failed") is True

        is_looping, reason = detector.is_in_loop()
        assert is_looping is True
        assert "3 times" in reason

    def test_failure_loop_detector_tracks_validation_failures(self):
        """Failure loop detector should track repeated validation failures."""
        from sage.cli_core import _FailureLoopDetector

        detector = _FailureLoopDetector()

        # Record same validation failure multiple times
        for _ in range(3):
            detector.record_validation_failure(["No files read"])

        is_looping, reason = detector.is_in_loop()
        assert is_looping is True
        assert "validation failure" in reason.lower()

    def test_failure_loop_detector_resets(self):
        """Failure loop detector should reset on success."""
        from sage.cli_core import _FailureLoopDetector

        detector = _FailureLoopDetector(max_identical_errors=2)

        # Trigger loop
        detector.record_error("ERROR")
        detector.record_error("ERROR")
        assert detector.is_in_loop()[0] is True

        # Reset should clear the loop
        detector.reset()
        assert detector.is_in_loop()[0] is False

    def test_failure_loop_indicator_in_tdd_gate_error(self):
        """P1-D: TDD gate errors should include failure_loop indicator."""
        from sage.cli_core import _FailureLoopDetector

        # This tests that the failure_loop key is used in error responses
        detector = _FailureLoopDetector(max_identical_errors=2)
        detector.record_error("TEST EXECUTION ERROR: KeyError")
        is_loop = detector.record_error("TEST EXECUTION ERROR: KeyError")

        # After 2 identical errors, should detect loop
        assert is_loop is True
        is_looping, loop_reason = detector.is_in_loop()
        assert is_looping is True
        assert "error repeated" in loop_reason.lower()


# =============================================================================
# P1-E: Test Root Convention Fixtures
# =============================================================================


class TestProjectRootFixtures:
    """Tests that project root fixtures work correctly."""

    def test_sage_project_root_fixture_exists(self, sage_project_root):
        """P1-E: sage_project_root fixture should provide project root."""

        # Should return ai-platform directory
        assert sage_project_root.exists()
        assert sage_project_root.is_dir()

        # Should contain key project files
        assert (sage_project_root / "pyproject.toml").exists()
        assert (sage_project_root / "sage").is_dir()
        assert (sage_project_root / "backend").is_dir()

    def test_sage_tests_dir_fixture_exists(self, sage_tests_dir):
        """P1-E: sage_tests_dir fixture should provide tests directory."""

        # Should return sage/tests directory
        assert sage_tests_dir.exists()
        assert sage_tests_dir.is_dir()

        # This test file should be in the returned directory
        assert (sage_tests_dir / "test_runtime_validation_integration.py").exists()

    def test_sage_module_root_fixture_exists(self, sage_module_root):
        """P1-E: sage_module_root fixture should provide sage module directory."""

        # Should return sage directory
        assert sage_module_root.exists()
        assert sage_module_root.is_dir()

        # Should contain sage module files
        assert (sage_module_root / "main.py").exists()
        assert (sage_module_root / "__init__.py").exists()
        assert (sage_module_root / "tests").is_dir()

    def test_fixtures_are_consistent(self, sage_project_root, sage_tests_dir, sage_module_root):
        """P1-E: All fixtures should be consistent with each other."""
        # sage_module_root should be a child of sage_project_root
        assert sage_module_root.parent == sage_project_root

        # sage_tests_dir should be a child of sage_module_root
        assert sage_tests_dir.parent == sage_module_root

        # Verify the relationship: project_root/sage/tests
        assert sage_tests_dir == sage_project_root / "sage" / "tests"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

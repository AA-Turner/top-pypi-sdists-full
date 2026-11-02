"""Tests for verification_node."""

from unittest.mock import patch

from agentic_devtools.models.git_results import SetupResult
from agentic_devtools.orchestration.nodes.verification import (
    _MAX_STORED_OUTPUT_CHARS,
    _TRUNCATION_PREFIX,
    _normalize_retry_count,
    verification_node,
)


class TestNormalizeRetryCount:
    def test_returns_int_value(self):
        assert _normalize_retry_count(3) == 3

    def test_coerces_none_to_zero(self):
        assert _normalize_retry_count(None) == 0

    def test_coerces_bool_to_zero(self):
        assert _normalize_retry_count(True) == 0

    def test_coerces_negative_to_zero(self):
        assert _normalize_retry_count(-1) == 0

    def test_coerces_string_to_zero(self):
        assert _normalize_retry_count("3") == 0


class TestVerificationNode:
    def test_passes_on_exit_code_zero(self):
        mock_result = type("Result", (), {"returncode": 0, "stdout": "All checks passed", "stderr": ""})()
        with patch("agentic_devtools.orchestration.nodes.verification.run_command", return_value=mock_result):
            result = verification_node({"retry_count": 0})
            assert result["error"] is None
            assert result["step"] == "verification"

    def test_fails_on_nonzero_exit_code(self):
        mock_result = type("Result", (), {"returncode": 1, "stdout": "FAILED: ruff check", "stderr": ""})()
        with patch("agentic_devtools.orchestration.nodes.verification.run_command", return_value=mock_result):
            result = verification_node({"retry_count": 0})
            assert result["error"] is not None
            assert result["retry_count"] == 1

    def test_increments_retry_count(self):
        mock_result = type("Result", (), {"returncode": 2, "stdout": "", "stderr": "crash"})()
        with patch("agentic_devtools.orchestration.nodes.verification.run_command", return_value=mock_result):
            result = verification_node({"retry_count": 2})
            assert result["retry_count"] == 3

    def test_records_verification_output(self):
        mock_result = type("Result", (), {"returncode": 0, "stdout": "OK", "stderr": ""})()
        with patch("agentic_devtools.orchestration.nodes.verification.run_command", return_value=mock_result):
            result = verification_node({"retry_count": 0})
            assert "OK" in result["verification_output"]

    def test_truncates_large_output_in_state(self):
        large_output = "x" * (_MAX_STORED_OUTPUT_CHARS + 1000)
        mock_result = type("Result", (), {"returncode": 0, "stdout": large_output, "stderr": ""})()
        with patch("agentic_devtools.orchestration.nodes.verification.run_command", return_value=mock_result):
            result = verification_node({"retry_count": 0})
            assert len(result["verification_output"]) == _MAX_STORED_OUTPUT_CHARS
            assert result["verification_output"].startswith(_TRUNCATION_PREFIX)

    def test_does_not_truncate_small_output(self):
        small_output = "short output"
        mock_result = type("Result", (), {"returncode": 0, "stdout": small_output, "stderr": ""})()
        with patch("agentic_devtools.orchestration.nodes.verification.run_command", return_value=mock_result):
            result = verification_node({"retry_count": 0})
            assert result["verification_output"] == small_output

    def test_truncates_failed_output_in_state(self):
        large_output = "y" * (_MAX_STORED_OUTPUT_CHARS + 500)
        mock_result = type("Result", (), {"returncode": 1, "stdout": large_output, "stderr": ""})()
        with patch("agentic_devtools.orchestration.nodes.verification.run_command", return_value=mock_result):
            result = verification_node({"retry_count": 0})
            assert len(result["verification_output"]) == _MAX_STORED_OUTPUT_CHARS
            assert result["verification_output"].startswith(_TRUNCATION_PREFIX)

    def test_error_message_uses_stored_tail_not_head(self):
        """Error message preview uses stored_output (tail) not the start of full_output."""
        # HEAD_MARKER appears only at the very start of full_output — not in the stored tail.
        head_marker = "HEAD_ONLY_MARKER"
        large_output = head_marker + "x" * (_MAX_STORED_OUTPUT_CHARS + 500)
        mock_result = type("Result", (), {"returncode": 1, "stdout": large_output, "stderr": ""})()
        with patch("agentic_devtools.orchestration.nodes.verification.run_command", return_value=mock_result):
            result = verification_node({"retry_count": 0})
            assert head_marker not in result["error"]

    def test_runs_targeted_checks_in_setup_worktree(self, tmp_path):
        mock_result = type("Result", (), {"returncode": 0, "stdout": "All checks passed", "stderr": ""})()
        with (
            patch(
                "agentic_devtools.orchestration.nodes.verification.resolve_repo_root",
                return_value=tmp_path.resolve(),
            ),
            patch(
                "agentic_devtools.orchestration.nodes.verification.run_command", return_value=mock_result
            ) as mock_run,
        ):
            result = verification_node(
                {
                    "retry_count": 0,
                    "setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x"),
                }
            )
        assert result["error"] is None
        assert mock_run.call_args.kwargs["cwd"] == str(tmp_path.resolve())

    def test_dry_run_skips_quality_gates(self):
        """When dry_run is True, run_command is never called and success is returned."""
        with patch("agentic_devtools.orchestration.nodes.verification.run_command") as mock_run:
            result = verification_node({"dry_run": True, "retry_count": 0})
        mock_run.assert_not_called()
        assert result["error"] is None
        assert result["step"] == "verification"
        assert "[dry run" in result["verification_output"]
        assert any(e["event"] == "verification_skipped_dry_run" for e in result["events"])

    def test_stale_explicit_worktree_returns_error_without_running_gates(self):
        """When the checkpointed worktree path is no longer valid, verification fails
        rather than running quality gates in the process checkout (cwd=None)."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.verification.resolve_repo_root",
                return_value=None,
            ),
            patch("agentic_devtools.orchestration.nodes.verification.run_command") as mock_run,
        ):
            result = verification_node(
                {
                    "retry_count": 0,
                    "setup_result": SetupResult(worktree_path="/tmp/gone-wt", branch_name="feature/42/x"),
                }
            )
        mock_run.assert_not_called()
        assert result["error"] is not None
        assert "no longer accessible" in result["error"]
        assert result["verification_output"] == ""
        assert any(e["event"] == "verification_failed" for e in result["events"])
        assert result["events"][0]["signals"]["reason"] == "worktree_unavailable"

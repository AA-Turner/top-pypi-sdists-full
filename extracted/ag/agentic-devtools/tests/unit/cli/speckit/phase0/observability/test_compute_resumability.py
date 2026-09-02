"""Tests for compute_resumability in speckit/phase0/observability.py (FR-010)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.observability import compute_resumability


class TestComputeResumability:
    """Tests for the compute_resumability function."""

    def test_none_last_stage_is_retry_safe_from_start(self) -> None:
        result = compute_resumability(last_stage=None, artifact_branch=None, artifact_path=None, commit_sha=None)
        assert result == "retry-safe:from-start"

    def test_validation_is_retry_safe_from_start(self) -> None:
        result = compute_resumability(
            last_stage="validation", artifact_branch=None, artifact_path=None, commit_sha=None
        )
        assert result == "retry-safe:from-start"

    def test_artifact_generation_resume_safe_with_branch(self) -> None:
        result = compute_resumability(
            last_stage="artifact_generation", artifact_branch="branch", artifact_path=None, commit_sha=None
        )
        assert result == "resume-safe:artifact_generation"

    def test_artifact_generation_without_branch_is_retry_safe(self) -> None:
        result = compute_resumability(
            last_stage="artifact_generation", artifact_branch=None, artifact_path=None, commit_sha=None
        )
        assert result == "retry-safe:from-start"

    def test_commit_resume_safe_with_branch_and_path(self) -> None:
        result = compute_resumability(
            last_stage="commit", artifact_branch="branch", artifact_path="path", commit_sha=None
        )
        assert result == "resume-safe:commit"

    def test_commit_without_path_is_retry_safe(self) -> None:
        result = compute_resumability(
            last_stage="commit", artifact_branch="branch", artifact_path=None, commit_sha=None
        )
        assert result == "retry-safe:from-start"

    def test_pull_request_resume_safe_with_all_outputs(self) -> None:
        result = compute_resumability(
            last_stage="pull_request", artifact_branch="branch", artifact_path="path", commit_sha="sha"
        )
        assert result == "resume-safe:pull_request"

    def test_pull_request_missing_commit_is_retry_safe(self) -> None:
        result = compute_resumability(
            last_stage="pull_request", artifact_branch="branch", artifact_path="path", commit_sha=None
        )
        assert result == "retry-safe:from-start"

    def test_cleanup_is_retry_safe_from_start(self) -> None:
        result = compute_resumability(
            last_stage="cleanup", artifact_branch="branch", artifact_path="path", commit_sha="sha"
        )
        assert result == "retry-safe:from-start"

    def test_issue_comment_is_retry_safe_from_start(self) -> None:
        result = compute_resumability(
            last_stage="issue_comment", artifact_branch="branch", artifact_path="path", commit_sha="sha"
        )
        assert result == "retry-safe:from-start"

    def test_unknown_stage_is_retry_safe_from_start(self) -> None:
        result = compute_resumability(
            last_stage="unexpected", artifact_branch="branch", artifact_path="path", commit_sha="sha"
        )
        assert result == "retry-safe:from-start"

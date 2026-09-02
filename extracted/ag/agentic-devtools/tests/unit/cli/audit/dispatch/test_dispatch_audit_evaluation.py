"""Tests for dispatch_audit_evaluation()."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.audit.dispatch import (
    _push_batch_branch,
    _read_required_speckit_token,
    _resolve_base_sha,
    dispatch_audit_evaluation,
)
from agentic_devtools.cli.ci.agent_assignment import AgentAssignmentResult


class TestDispatchAuditEvaluation:
    """Tests for dispatch_audit_evaluation orchestration."""

    def test_writes_meta_pushes_branch_and_dispatches(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        batch_dir = repo_root / "audit-batches" / "batch-123"
        batch_dir.mkdir(parents=True)
        (batch_dir / "batch-summary.md").write_text("summary", encoding="utf-8")

        provider = MagicMock()
        provider.create_audit_tracking_issue.return_value = 2042
        provider.dispatch_audit_evaluation.return_value = AgentAssignmentResult(
            success=True,
            method="coding_agent_task",
            task_id="task-99",
            task_url="https://example/task-99",
            session_confirmed=True,
        )

        with (
            patch(
                "agentic_devtools.cli.audit.dispatch._push_batch_branch",
                return_value=None,
            ) as mock_push,
            patch(
                "agentic_devtools.cli.audit.dispatch._resolve_base_sha",
                return_value="basesha123",
            ),
        ):
            result = dispatch_audit_evaluation(
                provider=provider,
                batch_id="batch-123",
                output_dir=str(batch_dir),
                pr_numbers=[11, 12],
                repo_path=str(repo_root),
                github_repo="swai-factory/agentic-devtools",
            )

        provider.create_audit_tracking_issue.assert_called_once_with(batch_id="batch-123", pr_numbers=[11, 12])
        meta_path = batch_dir / "batch-meta.json"
        assert meta_path.exists()
        assert json.loads(meta_path.read_text(encoding="utf-8")) == {
            "batch_id": "batch-123",
            "pr_numbers": [11, 12],
            "tracking_issue": 2042,
            "batch_branch": "audit/batch-batch-12",
            "output_dir": "audit-batches/batch-123",
            "repo": "swai-factory/agentic-devtools",
            "base_sha": "basesha123",
        }
        mock_push.assert_called_once_with(
            repo_path=str(repo_root),
            github_repo="swai-factory/agentic-devtools",
            batch_branch="audit/batch-batch-12",
            batch_id="batch-123",
            output_dir=str(batch_dir),
        )
        provider.dispatch_audit_evaluation.assert_called_once_with(
            tracking_issue=2042,
            batch_id="batch-123",
            batch_branch="audit/batch-batch-12",
            batch_dir="audit-batches/batch-123",
            pr_numbers=[11, 12],
        )
        assert result == {
            "batch_id": "batch-123",
            "tracking_issue": 2042,
            "batch_branch": "audit/batch-batch-12",
            "dispatch_method": "coding_agent_task",
            "dispatch_task_id": "task-99",
            "dispatch_task_url": "https://example/task-99",
            "dispatch_session_confirmed": True,
            "batch_meta_path": "audit-batches/batch-123/batch-meta.json",
        }

    def test_propagates_session_confirmed_false(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        batch_dir = repo_root / "audit-batches" / "batch-123"
        batch_dir.mkdir(parents=True)
        (batch_dir / "batch-summary.md").write_text("summary", encoding="utf-8")

        provider = MagicMock()
        provider.create_audit_tracking_issue.return_value = 2042
        provider.dispatch_audit_evaluation.return_value = AgentAssignmentResult(
            success=True,
            method="agent_assignment",
            task_id="",
            task_url="",
            session_confirmed=False,
        )

        with patch(
            "agentic_devtools.cli.audit.dispatch._push_batch_branch",
            return_value=None,
        ):
            result = dispatch_audit_evaluation(
                provider=provider,
                batch_id="batch-123",
                output_dir=str(batch_dir),
                pr_numbers=[11, 12],
                repo_path=str(repo_root),
                github_repo="swai-factory/agentic-devtools",
            )

        assert result["dispatch_session_confirmed"] is False

    def test_raises_when_output_directory_missing(self, tmp_path: Path) -> None:
        provider = MagicMock()

        with pytest.raises(FileNotFoundError, match="Batch output directory not found"):
            dispatch_audit_evaluation(
                provider=provider,
                batch_id="batch-123",
                output_dir=str(tmp_path / "missing"),
                pr_numbers=[1],
                repo_path=str(tmp_path),
                github_repo="swai-factory/agentic-devtools",
            )

        provider.create_audit_tracking_issue.assert_not_called()

    def test_resolves_relative_output_dir_from_repo_root(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        repo_root = tmp_path / "repo"
        batch_dir = repo_root / "audit-batches" / "batch-123"
        batch_dir.mkdir(parents=True)

        monkeypatch.chdir(tmp_path)
        provider = MagicMock()
        provider.create_audit_tracking_issue.return_value = 2042
        provider.dispatch_audit_evaluation.return_value = AgentAssignmentResult(
            success=True,
            method="coding_agent_task",
            task_id="task-99",
            task_url="https://example/task-99",
            session_confirmed=True,
        )

        with patch("agentic_devtools.cli.audit.dispatch._push_batch_branch", return_value=None) as mock_push:
            dispatch_audit_evaluation(
                provider=provider,
                batch_id="batch-123",
                output_dir="audit-batches/batch-123",
                pr_numbers=[1],
                repo_path=str(repo_root),
                github_repo="swai-factory/agentic-devtools",
            )

        mock_push.assert_called_once_with(
            repo_path=str(repo_root),
            github_repo="swai-factory/agentic-devtools",
            batch_branch="audit/batch-batch-12",
            batch_id="batch-123",
            output_dir=str(batch_dir),
        )

    def test_raises_when_output_dir_is_outside_repo(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        provider = MagicMock()
        provider.create_audit_tracking_issue.return_value = 2042

        with pytest.raises(ValueError, match="must be inside repo_path"):
            dispatch_audit_evaluation(
                provider=provider,
                batch_id="batch-123",
                output_dir=str(outside),
                pr_numbers=[1],
                repo_path=str(repo_root),
                github_repo="swai-factory/agentic-devtools",
            )

    def test_raises_when_batch_id_empty(self, tmp_path: Path) -> None:
        provider = MagicMock()
        with pytest.raises(ValueError, match="batch_id must not be empty"):
            dispatch_audit_evaluation(
                provider=provider,
                batch_id="",
                output_dir=str(tmp_path),
                pr_numbers=[1],
                repo_path=str(tmp_path),
                github_repo="swai-factory/agentic-devtools",
            )

    def test_releases_labels_when_dispatch_fails(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        batch_dir = repo_root / "audit-batches" / "batch-123"
        batch_dir.mkdir(parents=True)

        provider = MagicMock()
        provider.create_audit_tracking_issue.return_value = 2042
        provider.dispatch_audit_evaluation.side_effect = RuntimeError("assignment failed")

        with patch("agentic_devtools.cli.audit.dispatch._push_batch_branch", return_value=None):
            with pytest.raises(RuntimeError, match="assignment failed"):
                dispatch_audit_evaluation(
                    provider=provider,
                    batch_id="batch-123",
                    output_dir=str(batch_dir),
                    pr_numbers=[11, 12],
                    repo_path=str(repo_root),
                    github_repo="swai-factory/agentic-devtools",
                )

        # In-progress labels released for both claimed PRs; none marked audited.
        assert provider.remove_label.call_count == 2
        provider.add_label.assert_not_called()


class TestReadRequiredSpeckitToken:
    """Tests for _read_required_speckit_token()."""

    def test_returns_trimmed_token(self) -> None:
        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": " token-value "}, clear=True):
            assert _read_required_speckit_token() == "token-value"

    def test_raises_when_missing(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(RuntimeError, match="SPECKIT_PR_TOKEN"):
                _read_required_speckit_token()


class TestResolveBaseSha:
    """Tests for _resolve_base_sha()."""

    def test_returns_stripped_sha_on_success(self) -> None:
        result = MagicMock(returncode=0, stdout="abc123\n")
        with patch("agentic_devtools.cli.audit.dispatch.subprocess.run", return_value=result):
            assert _resolve_base_sha("/repo") == "abc123"

    def test_returns_empty_on_nonzero_exit(self) -> None:
        result = MagicMock(returncode=128, stdout="")
        with patch("agentic_devtools.cli.audit.dispatch.subprocess.run", return_value=result):
            assert _resolve_base_sha("/repo") == ""

    def test_returns_empty_on_oserror(self) -> None:
        with patch("agentic_devtools.cli.audit.dispatch.subprocess.run", side_effect=OSError("no git")):
            assert _resolve_base_sha("/repo") == ""


class TestPushBatchBranch:
    """Tests for _push_batch_branch()."""

    def test_pushes_branch_using_speckit_token(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        output_dir = repo_root / "audit-batches" / "batch-123"
        output_dir.mkdir(parents=True)

        git_success = MagicMock(returncode=0, stdout="", stderr="")
        git_calls: list[list[str]] = []

        def fake_run(cmd: list[str], **_: object) -> MagicMock:
            git_calls.append(cmd)
            return git_success

        with (
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "test-token"}, clear=True),
            patch("subprocess.run", side_effect=fake_run),
        ):
            _push_batch_branch(
                repo_path=str(repo_root),
                github_repo="swai-factory/agentic-devtools",
                batch_branch="audit/batch-batch123",
                batch_id="batch-123",
                output_dir=str(output_dir),
            )

        push_call = next(c for c in git_calls if "push" in c)
        assert push_call[:4] == ["git", "-C", str(repo_root), "push"]
        assert "x-access-token:test-token@github.com/swai-factory/agentic-devtools.git" in push_call[5]
        assert "HEAD:refs/heads/audit/batch-batch123" in push_call

    def test_raises_when_git_command_fails(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        output_dir = repo_root / "audit-batches" / "batch-123"
        output_dir.mkdir(parents=True)

        git_failure = MagicMock(returncode=1, stdout="", stderr="boom")

        with (
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "test-token"}, clear=True),
            patch("subprocess.run", return_value=git_failure),
        ):
            with pytest.raises(RuntimeError, match="Failed to push audit batch branch"):
                _push_batch_branch(
                    repo_path=str(repo_root),
                    github_repo="swai-factory/agentic-devtools",
                    batch_branch="audit/batch-batch123",
                    batch_id="batch-123",
                    output_dir=str(output_dir),
                )

    def test_token_redacted_from_error_message_on_git_failure(self, tmp_path: Path) -> None:
        """SPECKIT_PR_TOKEN must not appear in any raised RuntimeError message."""
        repo_root = tmp_path / "repo"
        output_dir = repo_root / "audit-batches" / "batch-123"
        output_dir.mkdir(parents=True)

        secret = "super-secret-token"
        git_failure = MagicMock(
            returncode=1,
            stdout="",
            stderr=f"error: Permission denied to https://x-access-token:{secret}@github.com/",
        )

        with (
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": secret}, clear=True),
            patch("subprocess.run", return_value=git_failure),
        ):
            with pytest.raises(RuntimeError) as exc_info:
                _push_batch_branch(
                    repo_path=str(repo_root),
                    github_repo="swai-factory/agentic-devtools",
                    batch_branch="audit/batch-batch123",
                    batch_id="batch-123",
                    output_dir=str(output_dir),
                )

        assert secret not in str(exc_info.value)
        assert "***" in str(exc_info.value)

    def test_commit_uses_allow_empty_flag(self, tmp_path: Path) -> None:
        """git commit must use --allow-empty so re-runs with no new files succeed."""
        repo_root = tmp_path / "repo"
        output_dir = repo_root / "audit-batches" / "batch-123"
        output_dir.mkdir(parents=True)

        git_success = MagicMock(returncode=0, stdout="", stderr="")
        git_calls: list[list[str]] = []

        def fake_run(cmd: list[str], **_: object) -> MagicMock:
            git_calls.append(cmd)
            return git_success

        with (
            patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "test-token"}, clear=True),
            patch("subprocess.run", side_effect=fake_run),
        ):
            _push_batch_branch(
                repo_path=str(repo_root),
                github_repo="swai-factory/agentic-devtools",
                batch_branch="audit/batch-batch123",
                batch_id="batch-123",
                output_dir=str(output_dir),
            )

        commit_call = next(c for c in git_calls if "commit" in c)
        assert "--allow-empty" in commit_call

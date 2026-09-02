"""Tests for apply_audit_results."""

import logging
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.audit.apply import (
    OUTCOME_OVERSIZED_INSTRUCTIONS,
    OUTCOME_READ_ERROR,
    _cleanup_eval_pr_branch,
    _create_instruction_pr,
    _extract_pr_number_from_url,
    apply_audit_results,
    build_pr_description,
)
from agentic_devtools.cli.audit.instruction_size import MAX_INSTRUCTION_FILE_LINES


class TestApplyAuditResults:
    """Tests for apply_audit_results() — FR-007 apply command behavior."""

    def test_no_agent_output_dir(self, tmp_path: Path) -> None:
        """When no agent-output/ directory exists, releases in-progress labels for retry."""
        provider = MagicMock()
        result = apply_audit_results(
            provider=provider,
            batch_id="test-batch",
            output_dir=str(tmp_path),
            pr_numbers=[1, 2],
            repo_path=str(tmp_path),
        )
        assert result["changes_found"] is False
        # In-progress labels should be released (remove_label), but PRs must NOT
        # be marked as audited (add_label must not be called) so the batch can be retried.
        assert provider.remove_label.called
        provider.add_label.assert_not_called()

    def test_detects_modified_files(self, tmp_path: Path) -> None:
        """Detects when instruction files have been modified and creates a PR."""
        # Set up repo with existing instruction file
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        github_dir = repo_path / ".github"
        github_dir.mkdir()
        (github_dir / "copilot-instructions.md").write_text("# Original")

        # Set up agent output with modified file
        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("# Modified with new rules")

        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.audit.apply._create_instruction_pr",
            return_value="https://github.com/org/repo/pull/99",
        ) as mock_create_pr:
            result = apply_audit_results(
                provider=provider,
                batch_id="test-batch",
                output_dir=str(output_dir),
                pr_numbers=[1],
                repo_path=str(repo_path),
            )
        assert result["changes_found"] is True
        assert ".github/copilot-instructions.md" in result["files_modified"]
        assert result["pr_url"] == "https://github.com/org/repo/pull/99"
        mock_create_pr.assert_called_once_with(
            repo_path=str(repo_path),
            batch_id="test-batch",
            modified_files=[".github/copilot-instructions.md"],
            created_files=[],
            agent_output_dir=output_dir / "agent-output",
            description=mock_create_pr.call_args.kwargs["description"],
            provider=provider,
            tracking_issue=None,
            github_repo="",
            base_sha="",
        )

    def test_unchanged_files_not_reported(self, tmp_path: Path) -> None:
        """Files in agent-output identical to repo are not reported as modified."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        github_dir = repo_path / ".github"
        github_dir.mkdir()
        (github_dir / "copilot-instructions.md").write_text("# Same content")

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("# Same content")

        provider = MagicMock()
        result = apply_audit_results(
            provider=provider,
            batch_id="test-batch",
            output_dir=str(output_dir),
            pr_numbers=[1],
            repo_path=str(repo_path),
        )
        assert result["changes_found"] is False
        assert result["files_modified"] == []
        assert result["files_created"] == []

    def test_detects_new_files(self, tmp_path: Path) -> None:
        """Detects when new instruction files are created and creates a PR."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()

        # Agent creates a new AGENTS.md instruction file
        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / "src"
        agent_output.mkdir(parents=True)
        (agent_output / "AGENTS.md").write_text("# New src instructions")

        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.audit.apply._create_instruction_pr",
            return_value="https://github.com/org/repo/pull/100",
        ):
            result = apply_audit_results(
                provider=provider,
                batch_id="test-batch",
                output_dir=str(output_dir),
                pr_numbers=[1],
                repo_path=str(repo_path),
            )
        assert result["changes_found"] is True
        assert "src/AGENTS.md" in result["files_created"]

    def test_summary_report_excluded_from_instruction_changes(self, tmp_path: Path) -> None:
        """audit-summary-report.md in agent-output/ is not treated as an instruction change."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output"
        agent_output.mkdir(parents=True)
        # Only the summary report — no real instruction file changes
        (agent_output / "audit-summary-report.md").write_text("## Summary\nAll good")

        provider = MagicMock()
        result = apply_audit_results(
            provider=provider,
            batch_id="test-batch",
            output_dir=str(output_dir),
            pr_numbers=[1],
            repo_path=str(repo_path),
        )
        assert result["changes_found"] is False
        assert result["files_modified"] == []
        assert result["files_created"] == []

    def test_non_instruction_markdown_is_ignored(self, tmp_path: Path) -> None:
        """Only AGENTS.md and .github/copilot-instructions.md are eligible instruction changes."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / "docs"
        agent_output.mkdir(parents=True)
        (agent_output / "notes.md").write_text("# Not an instruction file")

        provider = MagicMock()
        result = apply_audit_results(
            provider=provider,
            batch_id="test-batch",
            output_dir=str(output_dir),
            pr_numbers=[1],
            repo_path=str(repo_path),
        )

        assert result["changes_found"] is False
        assert result["files_modified"] == []
        assert result["files_created"] == []

    def test_pr_creation_failure_releases_in_progress_labels(self, tmp_path: Path) -> None:
        """When _create_instruction_pr fails, in-progress labels are released for retry."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        (repo_path / ".github").mkdir()
        (repo_path / ".github" / "copilot-instructions.md").write_text("# Original")

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("# Modified")

        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.audit.apply._create_instruction_pr",
            return_value="",  # PR creation failed
        ):
            result = apply_audit_results(
                provider=provider,
                batch_id="test-batch",
                output_dir=str(output_dir),
                pr_numbers=[1, 2],
                repo_path=str(repo_path),
            )

        # In-progress label should be released (remove_label called, add_label NOT called)
        assert provider.remove_label.called
        provider.add_label.assert_not_called()
        assert result["pr_url"] == ""

    def test_pr_creation_success_finalizes_labels(self, tmp_path: Path) -> None:
        """When _create_instruction_pr succeeds, both remove and add label are called."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        (repo_path / ".github").mkdir()
        (repo_path / ".github" / "copilot-instructions.md").write_text("# Original")

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("# Modified")

        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.audit.apply._create_instruction_pr",
            return_value="https://github.com/org/repo/pull/99",
        ):
            result = apply_audit_results(
                provider=provider,
                batch_id="test-batch",
                output_dir=str(output_dir),
                pr_numbers=[1],
                repo_path=str(repo_path),
            )

        # Both remove (in-progress) and add (audited) label calls should happen
        assert provider.remove_label.called
        assert provider.add_label.called
        assert result["pr_url"] == "https://github.com/org/repo/pull/99"

    def test_outcome_missing_output(self, tmp_path: Path) -> None:
        provider = MagicMock()
        result = apply_audit_results(
            provider=provider,
            batch_id="b",
            output_dir=str(tmp_path),
            pr_numbers=[1],
            repo_path=str(tmp_path),
        )
        assert result["outcome"] == "missing_output"

    def test_outcome_invalid_output_when_no_summary_report(self, tmp_path: Path) -> None:
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output"
        agent_output.mkdir(parents=True)
        # agent-output exists but has neither instruction changes nor a summary report
        (agent_output / "stray.txt").write_text("noise")

        provider = MagicMock()
        result = apply_audit_results(
            provider=provider,
            batch_id="b",
            output_dir=str(output_dir),
            pr_numbers=[1, 2],
            repo_path=str(repo_path),
        )

        assert result["outcome"] == "invalid_output"
        assert result["changes_found"] is False
        assert provider.remove_label.called
        provider.add_label.assert_not_called()

    def test_outcome_no_changes_with_summary_report(self, tmp_path: Path) -> None:
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output"
        agent_output.mkdir(parents=True)
        (agent_output / "audit-summary-report.md").write_text("## Summary\nNo actionable patterns")

        provider = MagicMock()
        result = apply_audit_results(
            provider=provider,
            batch_id="b",
            output_dir=str(output_dir),
            pr_numbers=[1],
            repo_path=str(repo_path),
        )

        assert result["outcome"] == "no_changes"
        assert provider.add_label.called  # finalized as audited
        provider.delete_branch.assert_called_once_with("audit/batch-b")

    def test_outcome_pr_ready_on_success(self, tmp_path: Path) -> None:
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        (repo_path / ".github").mkdir()
        (repo_path / ".github" / "copilot-instructions.md").write_text("# Original")
        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("# Modified")

        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.audit.apply._create_instruction_pr",
            return_value="https://github.com/org/repo/pull/7",
        ):
            result = apply_audit_results(
                provider=provider,
                batch_id="b",
                output_dir=str(output_dir),
                pr_numbers=[1],
                repo_path=str(repo_path),
            )

        assert result["outcome"] == "pr_ready"
        provider.delete_branch.assert_called_once_with("audit/batch-b")

    def test_outcome_pr_failed_when_create_returns_empty(self, tmp_path: Path) -> None:
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        (repo_path / ".github").mkdir()
        (repo_path / ".github" / "copilot-instructions.md").write_text("# Original")
        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("# Modified")

        provider = MagicMock()
        with patch("agentic_devtools.cli.audit.apply._create_instruction_pr", return_value=""):
            result = apply_audit_results(
                provider=provider,
                batch_id="b",
                output_dir=str(output_dir),
                pr_numbers=[1],
                repo_path=str(repo_path),
            )

        assert result["outcome"] == "pr_failed"
        provider.delete_branch.assert_not_called()

    def test_outcome_pr_failed_on_exception(self, tmp_path: Path) -> None:
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        (repo_path / ".github").mkdir()
        (repo_path / ".github" / "copilot-instructions.md").write_text("# Original")
        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("# Modified")

        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.audit.apply._create_instruction_pr",
            side_effect=RuntimeError("boom"),
        ):
            result = apply_audit_results(
                provider=provider,
                batch_id="b",
                output_dir=str(output_dir),
                pr_numbers=[1],
                repo_path=str(repo_path),
            )

        assert result["outcome"] == "pr_failed"
        assert result["changes_found"] is True

    def test_branch_cleanup_failure_is_non_fatal(self, tmp_path: Path) -> None:
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output"
        agent_output.mkdir(parents=True)
        (agent_output / "audit-summary-report.md").write_text("## Summary\nNothing")

        provider = MagicMock()
        provider.delete_branch.side_effect = RuntimeError("delete failed")

        result = apply_audit_results(
            provider=provider,
            batch_id="b",
            output_dir=str(output_dir),
            pr_numbers=[1],
            repo_path=str(repo_path),
        )

        # A cleanup failure must not change a successful outcome.
        assert result["outcome"] == "no_changes"


class TestBuildPrDescription:
    """Tests for build_pr_description() — FR-008 PR description reporting."""

    def test_includes_batch_id(self, tmp_path: Path) -> None:
        desc = build_pr_description("batch-abc", [1, 2, 3], ["f1.md"], [], tmp_path)
        assert "batch-abc" in desc

    def test_includes_pr_numbers(self, tmp_path: Path) -> None:
        desc = build_pr_description("b", [42, 43], [], [], tmp_path)
        assert "#42" in desc
        assert "#43" in desc

    def test_includes_modified_files(self, tmp_path: Path) -> None:
        desc = build_pr_description("b", [1], [".github/copilot-instructions.md"], [], tmp_path)
        assert ".github/copilot-instructions.md" in desc
        assert "Modified Files" in desc

    def test_includes_created_files(self, tmp_path: Path) -> None:
        desc = build_pr_description("b", [1], [], ["tests/copilot-instructions.md"], tmp_path)
        assert "tests/copilot-instructions.md" in desc
        assert "Newly Created" in desc

    def test_no_auto_merge_warning(self, tmp_path: Path) -> None:
        desc = build_pr_description("b", [1], ["f.md"], [], tmp_path)
        assert "Do NOT auto-merge" not in desc
        assert "Human review required" not in desc
        assert "ai-auto-merge-allowed" in desc
        assert "when the `ai-auto-merge-allowed` label is present" in desc

    def test_includes_summary_report(self, tmp_path: Path) -> None:
        (tmp_path / "agent-output").mkdir()
        (tmp_path / "agent-output" / "audit-summary-report.md").write_text("## Summary\nDone")
        desc = build_pr_description("b", [1], ["f.md"], [], tmp_path)
        assert "Summary" in desc

    def test_summary_report_read_error(self, tmp_path: Path) -> None:
        """Handles UnicodeDecodeError when reading summary report gracefully."""
        agent_out = tmp_path / "agent-output"
        agent_out.mkdir()
        summary = agent_out / "audit-summary-report.md"
        summary.write_bytes(b"\x80\x81\x82\x83")  # Invalid UTF-8
        desc = build_pr_description("b", [1], ["f.md"], [], tmp_path)
        # Should produce valid output without the summary section
        assert "Do NOT auto-merge" not in desc
        assert "Agent Summary" not in desc


class TestCleanupEvalPrBranch:
    """Tests for _cleanup_eval_pr_branch()."""

    def test_noop_when_branch_empty(self) -> None:
        provider = MagicMock()
        _cleanup_eval_pr_branch(provider, "")
        provider.delete_branch.assert_not_called()

    def test_deletes_branch_when_provided(self) -> None:
        provider = MagicMock()
        _cleanup_eval_pr_branch(provider, "copilot/auditbatch-x")
        provider.delete_branch.assert_called_once_with("copilot/auditbatch-x")

    def test_delete_failure_is_non_fatal(self) -> None:
        provider = MagicMock()
        provider.delete_branch.side_effect = RuntimeError("gone")
        _cleanup_eval_pr_branch(provider, "copilot/auditbatch-x")
        provider.delete_branch.assert_called_once_with("copilot/auditbatch-x")


class TestCreateInstructionPr:
    """Tests for _create_instruction_pr() — covers lines 135-214 of apply.py."""

    _MIN_GIT_COMMAND_LENGTH = 4
    _GIT_SUBCOMMAND_INDEX = 3

    def setup_method(self) -> None:
        self._token_patch = patch.dict(os.environ, {"SPECKIT_PR_TOKEN": "test-token"}, clear=False)
        self._token_patch.start()

    def teardown_method(self) -> None:
        self._token_patch.stop()

    @staticmethod
    def _find_git_call_index(git_calls: list[list[str]], action: str) -> int | None:
        """Find call index for mocked `git -C <repo> <action> ...` commands."""
        return next(
            (
                i
                for i, cmd in enumerate(git_calls)
                if len(cmd) >= TestCreateInstructionPr._MIN_GIT_COMMAND_LENGTH
                and cmd[0] == "git"
                and cmd[TestCreateInstructionPr._GIT_SUBCOMMAND_INDEX] == action
            ),
            None,
        )

    @staticmethod
    def _find_git_call(git_calls: list[list[str]], action: str) -> list[str] | None:
        """Find mocked `git -C <repo> <action> ...` command payload."""
        return next(
            (
                cmd
                for cmd in git_calls
                if len(cmd) >= TestCreateInstructionPr._MIN_GIT_COMMAND_LENGTH
                and cmd[0] == "git"
                and cmd[TestCreateInstructionPr._GIT_SUBCOMMAND_INDEX] == action
            ),
            None,
        )

    def test_empty_batch_id_returns_empty_string(self, tmp_path: Path) -> None:
        """Empty batch_id is rejected immediately."""
        result = _create_instruction_pr(
            repo_path=str(tmp_path),
            batch_id="",
            modified_files=[".github/copilot-instructions.md"],
            created_files=[],
            agent_output_dir=tmp_path / "agent-output",
            description="desc",
            provider=MagicMock(),
        )
        assert result == ""

    def test_absolute_path_in_changed_files_rejected(self, tmp_path: Path) -> None:
        """Absolute paths in agent output are rejected to prevent path traversal."""
        result = _create_instruction_pr(
            repo_path=str(tmp_path),
            batch_id="abc12345",
            modified_files=["/etc/passwd"],
            created_files=[],
            agent_output_dir=tmp_path / "agent-output",
            description="desc",
            provider=MagicMock(),
            tracking_issue=2029,
            github_repo="org/repo",
        )
        assert result == ""

    def test_dotdot_in_path_rejected(self, tmp_path: Path) -> None:
        """Paths containing '..' are rejected to prevent path traversal."""
        result = _create_instruction_pr(
            repo_path=str(tmp_path),
            batch_id="abc12345",
            modified_files=["../secret.md"],
            created_files=[],
            agent_output_dir=tmp_path / "agent-output",
            description="desc",
            provider=MagicMock(),
            tracking_issue=2029,
            github_repo="org/repo",
        )
        assert result == ""

    def test_path_escaping_repo_root_rejected(self, tmp_path: Path, monkeypatch) -> None:
        """Paths that resolve outside the repository root are rejected."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        outside = (tmp_path / "outside").resolve()

        # Simulate a path that resolves outside the repo root. Cross-platform
        # stand-in for a symlink escape (symlinks need privileges on Windows).
        real_resolve = Path.resolve

        def fake_resolve(self, *args, **kwargs):
            if self.name == "secret.md":
                return outside / "secret.md"
            return real_resolve(self, *args, **kwargs)

        monkeypatch.setattr(Path, "resolve", fake_resolve)

        result = _create_instruction_pr(
            repo_path=str(repo_path),
            batch_id="abc12345",
            modified_files=["link/secret.md"],
            created_files=[],
            agent_output_dir=tmp_path / "agent-output",
            description="desc",
            provider=MagicMock(),
            tracking_issue=2029,
            github_repo="org/repo",
        )
        assert result == ""

    def test_symlink_in_agent_output_rejected(self, tmp_path: Path) -> None:
        """Symlinks inside agent_output_dir are rejected before copy."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        agent_output_dir.mkdir(parents=True)
        # Create a symlink inside agent_output_dir that points outside it
        target = tmp_path / "secret.txt"
        target.write_text("secret content")
        link = agent_output_dir / "instructions.md"
        try:
            link.symlink_to(target)
        except OSError:
            pytest.skip("symlink creation unavailable on this platform")

        mock_success = MagicMock(returncode=0, stdout="", stderr="")
        with patch("subprocess.run", return_value=mock_success):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=["instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="desc",
                provider=MagicMock(),
                tracking_issue=2029,
                github_repo="org/repo",
            )
        assert result == ""

    def test_source_escaping_agent_output_dir_rejected(self, tmp_path: Path, monkeypatch) -> None:
        """Source paths that resolve outside agent_output_dir are rejected."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        agent_output_dir.mkdir(parents=True)
        outside = tmp_path / "outside"
        outside.mkdir()

        real_resolve = Path.resolve

        def fake_resolve(self, *args, **kwargs):
            if self.name == "instructions.md" and "agent-output" in str(self):
                return outside / "instructions.md"
            return real_resolve(self, *args, **kwargs)

        monkeypatch.setattr(Path, "resolve", fake_resolve)

        mock_success = MagicMock(returncode=0, stdout="", stderr="")
        with patch("subprocess.run", return_value=mock_success):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=["instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="desc",
                provider=MagicMock(),
                tracking_issue=2029,
                github_repo="org/repo",
            )
        assert result == ""

    def test_symlinked_agent_output_dir_rejected(self, tmp_path: Path) -> None:
        """A symlinked agent_output_dir is rejected before any file is copied."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        real_dir = tmp_path / "real-agent-output"
        real_dir.mkdir()
        (real_dir / "instructions.md").write_text("# secret")
        agent_output_dir = tmp_path / "agent-output-link"
        try:
            agent_output_dir.symlink_to(real_dir)
        except OSError:
            pytest.skip("symlink creation unavailable on this platform")

        mock_success = MagicMock(returncode=0, stdout="", stderr="")
        with patch("subprocess.run", return_value=mock_success):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=["instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="desc",
                provider=MagicMock(),
                tracking_issue=2029,
                github_repo="org/repo",
            )
        assert result == ""

    def test_agent_output_dir_resolve_error_rejected(self, tmp_path: Path, monkeypatch) -> None:
        """An OSError from resolving agent_output_dir is handled and returns ''."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        agent_output_dir.mkdir(parents=True)

        real_resolve = Path.resolve

        def fake_resolve(self, *args, **kwargs):
            if str(self) == str(agent_output_dir):
                raise OSError("resolve failed")
            return real_resolve(self, *args, **kwargs)

        monkeypatch.setattr(Path, "resolve", fake_resolve)

        mock_success = MagicMock(returncode=0, stdout="", stderr="")
        with patch("subprocess.run", return_value=mock_success):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=["instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="desc",
                provider=MagicMock(),
                tracking_issue=2029,
                github_repo="org/repo",
            )
        assert result == ""

    def test_source_resolve_error_rejected(self, tmp_path: Path, monkeypatch) -> None:
        """An OSError from resolving a source path is handled and returns ''."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        agent_output_dir.mkdir(parents=True)
        (agent_output_dir / "instructions.md").write_text("# content")

        real_resolve = Path.resolve

        def fake_resolve(self, *args, **kwargs):
            if self.name == "instructions.md" and "agent-output" in str(self):
                raise OSError("resolve failed")
            return real_resolve(self, *args, **kwargs)

        monkeypatch.setattr(Path, "resolve", fake_resolve)

        mock_success = MagicMock(returncode=0, stdout="", stderr="")
        with patch("subprocess.run", return_value=mock_success):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=["instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="desc",
                provider=MagicMock(),
                tracking_issue=2029,
                github_repo="org/repo",
            )
        assert result == ""

    def test_successful_pr_creation(self, tmp_path: Path) -> None:
        """Successfully copies files, runs git commands, and creates a draft PR."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        mock_success = MagicMock()
        mock_success.returncode = 0
        mock_success.stdout = ""
        mock_success.stderr = ""

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/42"

        with patch("shutil.copy2") as mock_copy, patch("subprocess.run", return_value=mock_success):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345-long",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="swai-factory/agentic-devtools",
            )

        assert result == "https://github.com/org/repo/pull/42"
        mock_copy.assert_called_once()
        mock_provider.add_label.assert_called_once_with(42, "ai-auto-merge-allowed")

    def test_branches_off_base_sha_when_provided(self, tmp_path: Path) -> None:
        """When base_sha is provided and fetchable, the branch is created off it."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock(returncode=0, stdout="", stderr="")
        git_diff_with_materialized = MagicMock(returncode=0, stdout="audit-batches/example.md\n", stderr="")
        git_calls: list[list[str]] = []
        expected_diff_cmd = ["git", "-C", str(repo_path), "diff", "--name-only", "--cached", "--", "audit-batches"]

        def fake_run(cmd: list, **_: object) -> MagicMock:
            git_calls.append(list(cmd))
            if cmd == expected_diff_cmd:
                return git_diff_with_materialized
            return git_success

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/1"

        with patch("shutil.copy2"), patch("subprocess.run", side_effect=fake_run):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abcdef1234",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="swai-factory/agentic-devtools",
                base_sha="a" * 40,
            )

        assert result == "https://github.com/org/repo/pull/1"
        assert any("fetch" in c and ("a" * 40) in c for c in git_calls)
        checkout = next(c for c in git_calls if "checkout" in c and "-B" in c)
        assert checkout[-1] == "a" * 40

    def test_falls_back_to_head_when_base_sha_fetch_fails(self, tmp_path: Path) -> None:
        """A failed base-sha fetch falls back to branching off the current HEAD."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock(returncode=0, stdout="", stderr="")
        git_fetch_fail = MagicMock(returncode=1, stdout="", stderr="not found")
        git_calls: list[list[str]] = []

        def fake_run(cmd: list, **_: object) -> MagicMock:
            git_calls.append(list(cmd))
            if "fetch" in cmd:
                return git_fetch_fail
            return git_success

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/2"

        with patch("shutil.copy2"), patch("subprocess.run", side_effect=fake_run):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abcdef1234",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="swai-factory/agentic-devtools",
                base_sha="b" * 40,
            )

        assert result == "https://github.com/org/repo/pull/2"
        checkout = next(c for c in git_calls if "checkout" in c and "-B" in c)
        assert len(checkout) == 6
        assert checkout[-1] == "audit/instruction-update-abcdef12"

    def test_clears_materialized_audit_batches_before_staging(self, tmp_path: Path) -> None:
        """The instruction branch resets materialized audit-batches before git add."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock(returncode=0, stdout="", stderr="")
        git_diff_with_materialized = MagicMock(returncode=0, stdout="audit-batches/example.md\n", stderr="")
        git_calls: list[list[str]] = []
        expected_diff_cmd = ["git", "-C", str(repo_path), "diff", "--name-only", "--cached", "--", "audit-batches"]

        def fake_run(cmd: list, **_: object) -> MagicMock:
            git_calls.append(list(cmd))
            if cmd == expected_diff_cmd:
                return git_diff_with_materialized
            return git_success

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/4"

        with patch("shutil.copy2"), patch("subprocess.run", side_effect=fake_run):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abcdef1234",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="swai-factory/agentic-devtools",
            )

        assert result == "https://github.com/org/repo/pull/4"
        restore_index = self._find_git_call_index(git_calls, "restore")
        add_index = self._find_git_call_index(git_calls, "add")
        if restore_index is None:
            pytest.fail("Expected git restore ... -- audit-batches command to be executed")
        if add_index is None:
            pytest.fail("Expected git add command to be executed")
        restore_call = git_calls[restore_index]
        assert len(restore_call) >= self._MIN_GIT_COMMAND_LENGTH
        assert restore_call[:4] == ["git", "-C", str(repo_path), "restore"]
        assert "--staged" in restore_call
        assert "--source=HEAD" not in restore_call
        assert "--worktree" not in restore_call
        assert restore_call[-2:] == ["--", "audit-batches"]
        assert restore_index < add_index
        assert expected_diff_cmd in git_calls

    def test_skips_restore_when_audit_batches_not_materialized(self, tmp_path: Path) -> None:
        """No restore call is made when no staged audit-batches changes exist."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# Updated")

        git_success = MagicMock(returncode=0, stdout="", stderr="")
        git_calls: list[list[str]] = []
        expected_diff_cmd = ["git", "-C", str(repo_path), "diff", "--name-only", "--cached", "--", "audit-batches"]

        def fake_run(cmd: list, **_: object) -> MagicMock:
            git_calls.append(list(cmd))
            if cmd == expected_diff_cmd:
                return MagicMock(returncode=0, stdout="", stderr="")
            return git_success

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/6"

        with patch("shutil.copy2"), patch("subprocess.run", side_effect=fake_run):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abcdef1234",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="swai-factory/agentic-devtools",
            )

        assert result == "https://github.com/org/repo/pull/6"
        assert expected_diff_cmd in git_calls
        assert not any(
            len(cmd) >= self._MIN_GIT_COMMAND_LENGTH and cmd[:4] == ["git", "-C", str(repo_path), "restore"]
            for cmd in git_calls
        )

    def test_stages_only_instruction_paths_not_audit_batches(self, tmp_path: Path) -> None:
        """git add pathspec includes only modified/created instruction files."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / "specs").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# Updated")
        (agent_output_dir / "specs" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock(returncode=0, stdout="", stderr="")
        git_calls: list[list[str]] = []

        def fake_run(cmd: list, **_: object) -> MagicMock:
            git_calls.append(list(cmd))
            return git_success

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/5"

        modified_files = [".github/copilot-instructions.md"]
        created_files = ["specs/copilot-instructions.md"]

        with patch("shutil.copy2"), patch("subprocess.run", side_effect=fake_run):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abcdef1234",
                modified_files=modified_files,
                created_files=created_files,
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="swai-factory/agentic-devtools",
            )

        assert result == "https://github.com/org/repo/pull/5"
        add_call = self._find_git_call(git_calls, "add")
        assert add_call is not None, "Expected git add command to be executed"
        separator_index = add_call.index("--")
        staged_paths = add_call[separator_index + 1 :]
        assert staged_paths == modified_files + created_files
        assert not any(path.startswith("audit-batches/") for path in staged_paths)

    @pytest.mark.parametrize("base_sha", ["-badsha", "abc1234"])
    def test_invalid_base_sha_falls_back_to_head_without_fetch(self, tmp_path: Path, base_sha: str) -> None:
        """Malformed or ambiguous base_sha values are ignored instead of being fetched."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock(returncode=0, stdout="", stderr="")
        git_calls: list[list[str]] = []

        def fake_run(cmd: list, **_: object) -> MagicMock:
            git_calls.append(list(cmd))
            return git_success

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/3"

        with patch("shutil.copy2"), patch("subprocess.run", side_effect=fake_run):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abcdef1234",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="swai-factory/agentic-devtools",
                base_sha=base_sha,
            )

        assert result == "https://github.com/org/repo/pull/3"
        assert not any("fetch" in c for c in git_calls)
        checkout = next(c for c in git_calls if "checkout" in c and "-B" in c)
        assert checkout[-1] == "audit/instruction-update-abcdef12"

    def test_git_command_failure_returns_empty_string(self, tmp_path: Path) -> None:
        """When a git command fails, returns empty string."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        mock_failure = MagicMock()
        mock_failure.returncode = 1
        mock_failure.stdout = ""
        mock_failure.stderr = "fatal: branch already exists"

        mock_provider = MagicMock()

        with patch("shutil.copy2"), patch("subprocess.run", return_value=mock_failure):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="org/repo",
            )

        assert result == ""
        mock_provider.add_label.assert_not_called()

    def test_pr_create_failure_returns_empty_string(self, tmp_path: Path) -> None:
        """When provider.create_pull_request() returns empty string, function returns ''."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock()
        git_success.returncode = 0
        git_success.stdout = ""
        git_success.stderr = ""

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = ""  # PR creation failed

        with patch("shutil.copy2"), patch("subprocess.run", return_value=git_success):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="org/repo",
            )

        assert result == ""
        mock_provider.add_label.assert_not_called()

    def test_label_failure_is_non_fatal_after_pr_creation(self, tmp_path: Path) -> None:
        """PR creation still succeeds if auto-merge label application fails."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock()
        git_success.returncode = 0
        git_success.stdout = ""
        git_success.stderr = ""

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/88"
        mock_provider.add_label.side_effect = RuntimeError("label failed")

        with patch("shutil.copy2"), patch("subprocess.run", return_value=git_success):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="org/repo",
            )

        assert result == "https://github.com/org/repo/pull/88"
        mock_provider.add_label.assert_called_once_with(88, "ai-auto-merge-allowed")

    def test_pr_url_without_number_skips_auto_merge_label(self, tmp_path: Path) -> None:
        """PR URLs without /pull/<number> are accepted and skip best-effort labeling."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock()
        git_success.returncode = 0
        git_success.stdout = ""
        git_success.stderr = ""

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/compare/main...branch"

        with patch("shutil.copy2"), patch("subprocess.run", return_value=git_success):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="org/repo",
            )

        assert result == "https://github.com/org/repo/compare/main...branch"
        mock_provider.add_label.assert_not_called()

    def test_branch_name_uses_first_8_chars_of_batch_id(self, tmp_path: Path) -> None:
        """Branch creation resets/reuses a deterministic name derived from batch_id."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / "f.md").parent.mkdir(parents=True, exist_ok=True)
        (agent_output_dir / "f.md").write_text("# x")

        git_success = MagicMock()
        git_success.returncode = 0
        git_success.stdout = ""
        git_success.stderr = ""

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/1"

        subprocess_calls: list[MagicMock] = []

        def capture_run(cmd: list, **kwargs: object) -> MagicMock:
            subprocess_calls.append(MagicMock(cmd=cmd))
            return git_success

        with patch("shutil.copy2"), patch("subprocess.run", side_effect=capture_run):
            _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abcdef1234567890",
                modified_files=["f.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="desc",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="swai-factory/agentic-devtools",
            )

        # First git call should be checkout -B audit/instruction-update-<first8>
        first_cmd = subprocess_calls[0].cmd
        assert "checkout" in first_cmd
        assert "-B" in first_cmd
        assert "audit/instruction-update-abcdef12" in first_cmd

        # Push call must use --force so retries after a partial failure are idempotent
        push_cmd = next((c.cmd for c in subprocess_calls if "push" in c.cmd), None)
        assert push_cmd is not None
        assert "--force" in push_cmd

    def test_does_not_run_destructive_reset_hard(self, tmp_path: Path) -> None:
        """The branch setup should not call `git reset --hard`."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / "f.md").parent.mkdir(parents=True, exist_ok=True)
        (agent_output_dir / "f.md").write_text("# x")

        git_success = MagicMock()
        git_success.returncode = 0
        git_success.stdout = ""
        git_success.stderr = ""

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/1"

        subprocess_calls: list[list[str]] = []

        def capture_run(cmd: list, **kwargs: object) -> MagicMock:
            subprocess_calls.append(cmd)
            return git_success

        with patch("shutil.copy2"), patch("subprocess.run", side_effect=capture_run):
            _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abcdef1234567890",
                modified_files=["f.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="desc",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="swai-factory/agentic-devtools",
            )

        assert not any(cmd[:6] == ["git", "-C", str(repo_path), "reset", "--hard", "HEAD"] for cmd in subprocess_calls)

    def test_created_files_are_copied_and_staged(self, tmp_path: Path) -> None:
        """Both modified and created files are copied and staged."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / "src").mkdir(parents=True)
        (agent_output_dir / "src" / "new.md").write_text("# New instructions")

        git_success = MagicMock()
        git_success.returncode = 0
        git_success.stdout = ""
        git_success.stderr = ""

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/55"

        copied: list[tuple[str, str]] = []

        def fake_copy(src: str, dst: str) -> None:
            copied.append((src, dst))

        with patch("shutil.copy2", side_effect=fake_copy), patch("subprocess.run", return_value=git_success):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[],
                created_files=["src/new.md"],
                agent_output_dir=agent_output_dir,
                description="desc",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="swai-factory/agentic-devtools",
            )

        assert result == "https://github.com/org/repo/pull/55"
        assert len(copied) == 1
        assert copied[0][0] == str(agent_output_dir / "src" / "new.md")

    def test_commit_message_follows_convention_when_tracking_issue_provided(self, tmp_path: Path) -> None:
        """Commit message includes scope and footer when tracking_issue + github_repo are given."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock()
        git_success.returncode = 0
        git_success.stdout = ""
        git_success.stderr = ""

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/42"

        git_calls: list[list[str]] = []

        def fake_run(cmd: list, **kwargs: object) -> MagicMock:
            git_calls.append(list(cmd))
            return git_success

        with patch("shutil.copy2"), patch("subprocess.run", side_effect=fake_run):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345-long",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="swai-factory/agentic-devtools",
            )

        assert result == "https://github.com/org/repo/pull/42"

        # Find the commit call and verify message contains scope + footer
        commit_call = next((c for c in git_calls if "commit" in c and "-m" in c), None)
        assert commit_call is not None
        msg_index = commit_call.index("-m") + 1
        commit_msg = commit_call[msg_index]
        assert "chore(#2029):" in commit_msg
        # Footer: message should end with the bare issue reference
        assert commit_msg.strip().endswith("#2029")

        # provider.create_pull_request was called with the scoped PR title
        mock_provider.create_pull_request.assert_called_once()
        call_kwargs = mock_provider.create_pull_request.call_args
        assert "chore(#2029):" in call_kwargs.kwargs["title"]

    def test_commit_message_without_tracking_issue_fails_fast(self, tmp_path: Path) -> None:
        """When tracking_issue is missing, the instruction PR creation is rejected."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock()
        git_success.returncode = 0
        git_success.stdout = ""
        git_success.stderr = ""

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/10"

        with patch("shutil.copy2"), patch("subprocess.run", return_value=git_success):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=None,
                github_repo="",
            )
        assert result == ""

    def test_missing_gh_token_fails_fast(self, tmp_path: Path) -> None:
        """When neither GH_TOKEN nor SPECKIT_PR_TOKEN is present, PR creation is rejected."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        mock_provider = MagicMock()

        with (
            patch.dict(os.environ, {"GH_TOKEN": "", "SPECKIT_PR_TOKEN": ""}, clear=False),
            patch("shutil.copy2") as mock_copy,
            patch("subprocess.run") as mock_run,
        ):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="org/repo",
            )

        assert result == ""
        mock_copy.assert_not_called()
        mock_run.assert_not_called()
        mock_provider.create_pull_request.assert_not_called()

    def test_gh_token_env_var_accepted_for_pr_creation(self, tmp_path: Path) -> None:
        """GH_TOKEN alone (without SPECKIT_PR_TOKEN) should pass the token check."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock(returncode=0, stdout="", stderr="")
        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/99"

        with (
            patch.dict(os.environ, {"GH_TOKEN": "some-gh-token", "SPECKIT_PR_TOKEN": ""}, clear=False),
            patch("shutil.copy2"),
            patch("subprocess.run", return_value=git_success),
        ):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="org/repo",
            )

        assert result == "https://github.com/org/repo/pull/99"

    def test_speckit_pr_token_propagated_to_gh_token_for_pr_creation(self, tmp_path: Path) -> None:
        """When only SPECKIT_PR_TOKEN is set, GH_TOKEN is propagated so gh pr create can authenticate."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock(returncode=0, stdout="", stderr="")
        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/99"

        captured_gh_token: list[str] = []

        def fake_create_pr(**_: object) -> str:
            captured_gh_token.append(os.environ.get("GH_TOKEN", ""))
            return "https://github.com/org/repo/pull/99"

        mock_provider.create_pull_request.side_effect = fake_create_pr

        with (
            patch.dict(os.environ, {"GH_TOKEN": "", "SPECKIT_PR_TOKEN": "speckit-secret"}, clear=False),
            patch("shutil.copy2"),
            patch("subprocess.run", return_value=git_success),
        ):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="org/repo",
            )

        assert result == "https://github.com/org/repo/pull/99"
        # GH_TOKEN must be populated from SPECKIT_PR_TOKEN so that gh pr create
        # can authenticate even when GH_TOKEN was absent/blank initially.
        assert captured_gh_token == ["speckit-secret"]

    def test_whitespace_gh_token_falls_back_to_speckit_pr_token(self, tmp_path: Path) -> None:
        """GH_TOKEN set to whitespace must fall back to SPECKIT_PR_TOKEN (not fail)."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock(returncode=0, stdout="", stderr="")
        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/99"

        captured_gh_token: list[str] = []

        def fake_create_pr(**_: object) -> str:
            captured_gh_token.append(os.environ.get("GH_TOKEN", ""))
            return "https://github.com/org/repo/pull/99"

        mock_provider.create_pull_request.side_effect = fake_create_pr

        with (
            patch.dict(os.environ, {"GH_TOKEN": "   ", "SPECKIT_PR_TOKEN": "speckit-secret"}, clear=False),
            patch("shutil.copy2"),
            patch("subprocess.run", return_value=git_success),
        ):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="org/repo",
            )

        assert result == "https://github.com/org/repo/pull/99"
        # GH_TOKEN must be set to the stripped SPECKIT_PR_TOKEN value since the
        # original GH_TOKEN was whitespace-only.
        assert captured_gh_token == ["speckit-secret"]

    def test_push_uses_bare_origin_not_token_url(self, tmp_path: Path) -> None:
        """Push must target bare 'origin', not a PAT-embedded URL."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_calls: list[list] = []
        git_success = MagicMock(returncode=0, stdout="", stderr="")

        def fake_run(cmd: list, **_: object) -> MagicMock:
            git_calls.append(list(cmd))
            return git_success

        mock_provider = MagicMock()
        mock_provider.create_pull_request.return_value = "https://github.com/org/repo/pull/1"

        with (
            patch.dict(os.environ, {"GH_TOKEN": "some-gh-token"}, clear=False),
            patch("shutil.copy2"),
            patch("subprocess.run", side_effect=fake_run),
        ):
            _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="org/repo",
            )

        push_calls = [c for c in git_calls if "push" in c]
        assert push_calls, "Expected at least one git push call"
        push_cmd = push_calls[0]
        # Must push to plain 'origin', never embed a token in the remote URL
        assert "origin" in push_cmd, "Push must target 'origin'"
        assert not any("x-access-token" in str(arg) for arg in push_cmd), "PAT must not be embedded in the push URL"
        assert not any("some-gh-token" in str(arg) for arg in push_cmd), (
            "GH_TOKEN must not appear in git push arguments"
        )
        # Verify the complete push command structure
        assert "--force" in push_cmd, "Push must be force push"
        assert any("HEAD:refs/heads/" in str(arg) for arg in push_cmd), "Push must use HEAD:refs/heads/<branch> refspec"

    def test_git_push_error_does_not_leak_gh_token(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        """GH_TOKEN must not appear in logger output when git push fails.

        With bare-origin push, no token is embedded in the git command, so
        token values cannot leak through git error messages.
        """
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        secret = "my-secret-gh-token"
        git_success = MagicMock(returncode=0, stdout="", stderr="")
        git_push_failure = MagicMock(
            returncode=128,
            stdout="",
            stderr="fatal: remote: Write access to repository not granted.",
        )

        def fake_run(cmd: list, **kwargs: object) -> MagicMock:
            if "push" in cmd:
                return git_push_failure
            return git_success

        mock_provider = MagicMock()

        with (
            patch.dict(os.environ, {"GH_TOKEN": secret}, clear=False),
            patch("shutil.copy2"),
            patch("subprocess.run", side_effect=fake_run),
            caplog.at_level(logging.ERROR, logger="agentic_devtools.cli.git.remote_push"),
        ):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="org/repo",
            )

        assert result == ""
        # The GH_TOKEN value must not appear in any log message (it's not embedded
        # in the push URL, so git errors cannot contain it)
        for record in caplog.records:
            assert secret not in record.getMessage(), f"Token leaked in log record: {record.getMessage()}"

    def test_cwd_changed_to_repo_path_before_create_pull_request(self, tmp_path: Path) -> None:
        """provider.create_pull_request() is called while cwd is set to repo_path."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        agent_output_dir = tmp_path / "agent-output"
        (agent_output_dir / ".github").mkdir(parents=True)
        (agent_output_dir / ".github" / "copilot-instructions.md").write_text("# New")

        git_success = MagicMock()
        git_success.returncode = 0
        git_success.stdout = ""
        git_success.stderr = ""

        observed_cwd: list[str] = []

        mock_provider = MagicMock()

        def capture_cwd_and_return_url(*, title: str, body: str, **_: object) -> str:
            observed_cwd.append(os.getcwd())
            return "https://github.com/org/repo/pull/77"

        mock_provider.create_pull_request.side_effect = capture_cwd_and_return_url

        original_cwd = os.getcwd()
        with patch("shutil.copy2"), patch("subprocess.run", return_value=git_success):
            result = _create_instruction_pr(
                repo_path=str(repo_path),
                batch_id="abc12345",
                modified_files=[".github/copilot-instructions.md"],
                created_files=[],
                agent_output_dir=agent_output_dir,
                description="## PR Body",
                provider=mock_provider,
                tracking_issue=2029,
                github_repo="org/repo",
            )

        assert result == "https://github.com/org/repo/pull/77"
        assert len(observed_cwd) == 1
        assert str(repo_path) == observed_cwd[0]
        # cwd is restored after the call
        assert os.getcwd() == original_cwd


class TestApplyAuditResultsFileReadErrors:
    """Tests for error handling when instruction files cannot be read."""

    def test_unreadable_existing_file_skipped_gracefully(self, tmp_path: Path) -> None:
        """UnicodeDecodeError reading an existing file is caught; file is skipped."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        (repo_path / ".github").mkdir()
        # Write a valid UTF-8 file in the repo
        (repo_path / ".github" / "copilot-instructions.md").write_text("# Same")

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        # Agent output also identical — but simulate read failure on the repo copy
        (agent_output / "copilot-instructions.md").write_text("# Same")

        provider = MagicMock()

        # Patch Path.read_text to raise UnicodeDecodeError for the repo-side file
        original_read_text = Path.read_text

        def fake_read_text(
            self: Path,
            encoding: str | None = None,
            errors: str | None = None,
        ) -> str:
            if "repo" in str(self):
                raise UnicodeDecodeError("utf-8", b"", 0, 1, "invalid")
            return original_read_text(self, encoding, errors)

        with patch.object(Path, "read_text", fake_read_text):
            result = apply_audit_results(
                provider=provider,
                batch_id="test-batch",
                output_dir=str(output_dir),
                pr_numbers=[1],
                repo_path=str(repo_path),
            )

        # File was skipped; no changes detected (apply skips unreadable files)
        assert result["changes_found"] is False

    def test_unreadable_agent_output_modified_file_aborts_batch(self, tmp_path: Path) -> None:
        """UnicodeDecodeError reading agent output for a modified file aborts the batch."""
        repo_path = tmp_path / "repo"
        (repo_path / ".github").mkdir(parents=True)
        (repo_path / ".github" / "copilot-instructions.md").write_text("# Existing")

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("# Updated")

        provider = MagicMock()
        original_read_text = Path.read_text

        def fake_read_text(
            self: Path,
            encoding: str | None = None,
            errors: str | None = None,
        ) -> str:
            if "agent-output" in str(self):
                raise UnicodeDecodeError("utf-8", b"", 0, 1, "invalid")
            return original_read_text(self, encoding, errors)

        with patch.object(Path, "read_text", fake_read_text):
            result = apply_audit_results(
                provider=provider,
                batch_id="test-batch",
                output_dir=str(output_dir),
                pr_numbers=[1],
                repo_path=str(repo_path),
            )

        assert result["outcome"] == OUTCOME_READ_ERROR

    def test_unreadable_new_file_aborts_batch(self, tmp_path: Path) -> None:
        """A new file that cannot be decoded aborts the batch with OUTCOME_READ_ERROR."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_bytes(b"\xff\xfe invalid utf-8")

        provider = MagicMock()
        result = apply_audit_results(
            provider=provider,
            batch_id="test-batch",
            output_dir=str(output_dir),
            pr_numbers=[1],
            repo_path=str(repo_path),
        )

        assert result["outcome"] == OUTCOME_READ_ERROR


class TestApplyAuditResultsInstructionSizeCap:
    """Tests for the instruction-file growth control (loud failure over the cap)."""

    def test_oversized_modified_file_fails_the_batch(self, tmp_path: Path) -> None:
        """A proposed update over the line cap aborts the batch instead of opening a PR."""
        repo_path = tmp_path / "repo"
        github_dir = repo_path / ".github"
        github_dir.mkdir(parents=True)
        (github_dir / "copilot-instructions.md").write_text("# Original")

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("\n".join(["line"] * (MAX_INSTRUCTION_FILE_LINES + 1)))

        provider = MagicMock()
        with patch("agentic_devtools.cli.audit.apply._create_instruction_pr") as mock_create_pr:
            result = apply_audit_results(
                provider=provider,
                batch_id="test-batch",
                output_dir=str(output_dir),
                pr_numbers=[1],
                repo_path=str(repo_path),
            )

        assert result["outcome"] == OUTCOME_OVERSIZED_INSTRUCTIONS
        assert ".github/copilot-instructions.md" in result["error"]
        mock_create_pr.assert_not_called()


class TestApplyAuditResultsSymlinkGuard:
    """Tests for symlink traversal protection in apply_audit_results()."""

    def test_symlink_in_agent_output_pointing_outside_is_skipped(self, tmp_path: Path, monkeypatch) -> None:
        """A file in agent-output/ that resolves outside agent-output is skipped."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output"
        agent_output.mkdir(parents=True)

        # A real instruction file in agent-output that (via the mock) resolves
        # outside agent-output — a cross-platform stand-in for a symlink escape.
        (agent_output / "AGENTS.md").write_text("# Malicious instructions")

        outside = (tmp_path / "evil").resolve()
        real_resolve = Path.resolve

        def fake_resolve(self, *args, **kwargs):
            if self.name == "AGENTS.md":
                return outside / "AGENTS.md"
            return real_resolve(self, *args, **kwargs)

        monkeypatch.setattr(Path, "resolve", fake_resolve)

        provider = MagicMock()
        result = apply_audit_results(
            provider=provider,
            batch_id="test-batch",
            output_dir=str(output_dir),
            pr_numbers=[1],
            repo_path=str(repo_path),
        )

        # Skipped file produced no changes; PR creation was NOT triggered.
        assert result["changes_found"] is False
        provider.create_pull_request.assert_not_called()

    def test_resolve_oserror_on_md_file_skips_gracefully(self, tmp_path: Path) -> None:
        """OSError from Path.resolve() on the agent-output file skips it gracefully."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("# Changed")

        provider = MagicMock()

        original_resolve = Path.resolve

        def fake_resolve(self: Path, strict: bool = False) -> Path:
            if "agent-output" in str(self) and self.name == "copilot-instructions.md":
                raise OSError("simulated resolve error")
            return original_resolve(self, strict=strict)

        with patch.object(Path, "resolve", fake_resolve):
            result = apply_audit_results(
                provider=provider,
                batch_id="test-batch",
                output_dir=str(output_dir),
                pr_numbers=[1],
                repo_path=str(repo_path),
            )

        assert result["changes_found"] is False

    def test_resolve_oserror_on_target_path_skips_gracefully(self, tmp_path: Path) -> None:
        """OSError from Path.resolve() on the repo-side target_path skips the file."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("# Changed")

        provider = MagicMock()

        original_resolve = Path.resolve

        def fake_resolve(self: Path, strict: bool = False) -> Path:
            # Raise only when resolving the repo-side (target) path, not the agent-output one
            if str(repo_path) in str(self) and self.name == "copilot-instructions.md":
                raise OSError("simulated resolve error on target")
            return original_resolve(self, strict=strict)

        with patch.object(Path, "resolve", fake_resolve):
            result = apply_audit_results(
                provider=provider,
                batch_id="test-batch",
                output_dir=str(output_dir),
                pr_numbers=[1],
                repo_path=str(repo_path),
            )

        assert result["changes_found"] is False

    def test_symlink_target_path_outside_repo_root_is_skipped(self, tmp_path: Path) -> None:
        """A target_path that resolves outside the repo root is skipped."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("# Changed")

        provider = MagicMock()

        # Resolve the agent-output file path normally; make the target_path escape the repo root
        original_resolve = Path.resolve

        def fake_resolve(self: Path, strict: bool = False) -> Path:
            resolved = original_resolve(self, strict=strict)
            # Make the target path (inside repo) appear to resolve outside the repo
            if str(repo_path) in str(self) and self.name == "copilot-instructions.md":
                return tmp_path / "outside" / "copilot-instructions.md"
            return resolved

        with patch.object(Path, "resolve", fake_resolve):
            result = apply_audit_results(
                provider=provider,
                batch_id="test-batch",
                output_dir=str(output_dir),
                pr_numbers=[1],
                repo_path=str(repo_path),
            )

        assert result["changes_found"] is False
        provider.create_pull_request.assert_not_called()


class TestApplyAuditResultsExceptionHandler:
    """Tests for unexpected exception handling in apply_audit_results()."""

    def test_unexpected_exception_in_create_pr_releases_labels(self, tmp_path: Path) -> None:
        """If _create_instruction_pr raises unexpectedly, in-progress labels are released."""
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        (repo_path / ".github").mkdir()
        (repo_path / ".github" / "copilot-instructions.md").write_text("# Old")

        output_dir = tmp_path / "output"
        agent_output = output_dir / "agent-output" / ".github"
        agent_output.mkdir(parents=True)
        (agent_output / "copilot-instructions.md").write_text("# New")

        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.audit.apply._create_instruction_pr",
                side_effect=RuntimeError("unexpected filesystem error"),
            ),
            patch("agentic_devtools.cli.audit.apply.cleanup_failed_batch") as mock_cleanup,
        ):
            result = apply_audit_results(
                provider=provider,
                batch_id="test-batch",
                output_dir=str(output_dir),
                pr_numbers=[42, 43],
                repo_path=str(repo_path),
                tracking_issue=2029,
                github_repo="org/repo",
            )

        # Result shows changes were found but PR URL is empty (exception suppressed)
        assert result["changes_found"] is True
        assert result["pr_url"] == ""
        # Cleanup called with all pr_numbers to release in-progress labels
        mock_cleanup.assert_called_once_with(provider, [42, 43], [])


class TestExtractPrNumberFromUrl:
    """Tests for _extract_pr_number_from_url()."""

    def test_returns_pr_number_when_present(self) -> None:
        assert _extract_pr_number_from_url("https://github.com/org/repo/pull/42") == 42

    def test_returns_none_when_url_has_no_pull_segment(self) -> None:
        assert _extract_pr_number_from_url("https://github.com/org/repo/compare/main...branch") is None

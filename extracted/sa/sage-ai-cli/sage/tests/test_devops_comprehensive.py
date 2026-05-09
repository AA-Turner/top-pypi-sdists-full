"""Comprehensive tests for sage/devops modules."""

import subprocess
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch, Mock

import pytest

from sage.devops.git import GitOps, GitStatus, GitCommit
from sage.devops.ci_cd import (
    PipelineStatus,
    JobStatus,
    CIJob,
    CIPipeline,
    TestResult,
    TestSummary,
    CICDMonitor,
)
from sage.devops.github import (
    PRState,
    CheckStatus,
    GitHubCheck,
    PullRequest,
    Issue,
    GitHubOps,
)


# =============================================================================
# Tests for GitStatus Dataclass
# =============================================================================


class TestGitStatus:
    """Tests for GitStatus dataclass."""

    def test_create(self):
        """Create git status."""
        status = GitStatus(
            branch="main",
            is_clean=True,
        )
        assert status.branch == "main"
        assert status.is_clean is True

    def test_default_lists(self):
        """Default lists are empty."""
        status = GitStatus(branch="main", is_clean=True)
        assert status.staged_files == []
        assert status.modified_files == []
        assert status.untracked_files == []

    def test_with_files(self):
        """Status with files."""
        status = GitStatus(
            branch="main",
            is_clean=False,
            staged_files=["file1.py"],
            modified_files=["file2.py"],
            untracked_files=["file3.py"],
        )
        assert len(status.staged_files) == 1
        assert len(status.modified_files) == 1
        assert len(status.untracked_files) == 1


# =============================================================================
# Tests for GitCommit Dataclass
# =============================================================================


class TestGitCommit:
    """Tests for GitCommit dataclass."""

    def test_create(self):
        """Create git commit."""
        commit = GitCommit(
            sha="abc123",
            message="Fix bug",
            author="Test User",
            date="2024-01-01",
        )
        assert commit.sha == "abc123"
        assert commit.message == "Fix bug"
        assert commit.author == "Test User"


# =============================================================================
# Tests for GitOps
# =============================================================================


class TestGitOps:
    """Tests for GitOps class."""

    def test_init_with_repo(self, tmp_path):
        """Initialize with valid repo path."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)
        assert ops.repo_path == tmp_path

    def test_init_invalid_repo(self, tmp_path):
        """Initialize with invalid repo raises error."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            with pytest.raises(ValueError):
                GitOps(tmp_path)

    def test_get_status(self, tmp_path):
        """Get git status."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="## main\nM file1.py\n?? file2.py"
            )
            status = ops.get_status()
            assert status.branch == "main"
            assert "file2.py" in status.untracked_files

    def test_get_current_branch(self, tmp_path):
        """Get current branch."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            mock_run.return_value = MagicMock(stdout="feature-branch\n")
            branch = ops.get_current_branch()
            assert branch == "feature-branch"

    def test_get_diff(self, tmp_path):
        """Get diff."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            mock_run.return_value = MagicMock(stdout="diff content")
            diff = ops.get_diff()
            assert diff == "diff content"

    def test_get_diff_staged(self, tmp_path):
        """Get staged diff."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            mock_run.return_value = MagicMock(stdout="staged diff")
            diff = ops.get_diff(staged=True)
            assert diff == "staged diff"
            mock_run.assert_called_once()
            assert "--staged" in mock_run.call_args[0][0]

    def test_get_log(self, tmp_path):
        """Get commit log."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="abc123|Fix bug|Author|2024-01-01\ndef456|Add feature|Author2|2024-01-02"
            )
            commits = ops.get_log(count=2)
            assert len(commits) == 2
            assert commits[0].sha == "abc123"
            assert commits[0].message == "Fix bug"

    def test_stage_files(self, tmp_path):
        """Stage files."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            ops.stage_files(["file1.py", "file2.py"])
            mock_run.assert_called_once()
            assert "add" in mock_run.call_args[0][0]

    def test_stage_files_empty(self, tmp_path):
        """Stage empty list does nothing."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            ops.stage_files([])
            mock_run.assert_not_called()

    def test_commit(self, tmp_path):
        """Create commit."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            mock_run.return_value = MagicMock(stdout="abc123\n")
            sha = ops.commit("Test message")
            assert sha == "abc123"

    def test_create_branch(self, tmp_path):
        """Create branch."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            ops.create_branch("feature-1")
            assert mock_run.call_count == 2  # branch + checkout

    def test_create_branch_no_checkout(self, tmp_path):
        """Create branch without checkout."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            ops.create_branch("feature-1", checkout=False)
            mock_run.assert_called_once()

    def test_checkout(self, tmp_path):
        """Checkout branch."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            ops.checkout("main")
            mock_run.assert_called_once()

    def test_pull(self, tmp_path):
        """Pull from remote."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            ops.pull()
            mock_run.assert_called_once()

    def test_pull_with_branch(self, tmp_path):
        """Pull specific branch."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            ops.pull("upstream", "main")
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            assert "upstream" in args
            assert "main" in args

    def test_push(self, tmp_path):
        """Push to remote."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            ops.push()
            mock_run.assert_called_once()

    def test_stash(self, tmp_path):
        """Stash changes."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            ops.stash()
            mock_run.assert_called_once()

    def test_stash_with_message(self, tmp_path):
        """Stash with message."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            ops.stash("WIP changes")
            args = mock_run.call_args[0][0]
            assert "-m" in args
            assert "WIP changes" in args

    def test_stash_pop(self, tmp_path):
        """Pop stash."""
        (tmp_path / ".git").mkdir()
        ops = GitOps(tmp_path)

        with patch.object(ops, "_run_git") as mock_run:
            ops.stash_pop()
            mock_run.assert_called_once()


# =============================================================================
# Tests for PipelineStatus Enum
# =============================================================================


class TestPipelineStatus:
    """Tests for PipelineStatus enum."""

    def test_pending(self):
        """PENDING status."""
        assert PipelineStatus.PENDING.name == "PENDING"

    def test_running(self):
        """RUNNING status."""
        assert PipelineStatus.RUNNING.name == "RUNNING"

    def test_success(self):
        """SUCCESS status."""
        assert PipelineStatus.SUCCESS.name == "SUCCESS"

    def test_failed(self):
        """FAILED status."""
        assert PipelineStatus.FAILED.name == "FAILED"

    def test_cancelled(self):
        """CANCELLED status."""
        assert PipelineStatus.CANCELLED.name == "CANCELLED"


# =============================================================================
# Tests for JobStatus Enum
# =============================================================================


class TestJobStatus:
    """Tests for JobStatus enum."""

    def test_all_values(self):
        """All job status values exist."""
        assert JobStatus.PENDING.name == "PENDING"
        assert JobStatus.RUNNING.name == "RUNNING"
        assert JobStatus.SUCCESS.name == "SUCCESS"
        assert JobStatus.FAILED.name == "FAILED"
        assert JobStatus.SKIPPED.name == "SKIPPED"
        assert JobStatus.CANCELLED.name == "CANCELLED"


# =============================================================================
# Tests for CIJob Dataclass
# =============================================================================


class TestCIJob:
    """Tests for CIJob dataclass."""

    def test_create_minimal(self):
        """Create with minimal params."""
        job = CIJob(name="test", status=JobStatus.SUCCESS)
        assert job.name == "test"
        assert job.status == JobStatus.SUCCESS
        assert job.duration_seconds is None

    def test_create_full(self):
        """Create with all params."""
        job = CIJob(
            name="build",
            status=JobStatus.FAILED,
            duration_seconds=120.5,
            error_message="Build failed",
        )
        assert job.duration_seconds == 120.5
        assert job.error_message == "Build failed"


# =============================================================================
# Tests for CIPipeline Dataclass
# =============================================================================


class TestCIPipeline:
    """Tests for CIPipeline dataclass."""

    def test_create(self):
        """Create pipeline."""
        pipeline = CIPipeline(
            id="123",
            status=PipelineStatus.SUCCESS,
            branch="main",
            commit_sha="abc123",
        )
        assert pipeline.id == "123"
        assert pipeline.branch == "main"

    def test_is_complete_success(self):
        """Pipeline complete on success."""
        pipeline = CIPipeline(
            id="1", status=PipelineStatus.SUCCESS,
            branch="main", commit_sha="abc",
        )
        assert pipeline.is_complete is True

    def test_is_complete_failed(self):
        """Pipeline complete on failure."""
        pipeline = CIPipeline(
            id="1", status=PipelineStatus.FAILED,
            branch="main", commit_sha="abc",
        )
        assert pipeline.is_complete is True

    def test_is_complete_running(self):
        """Pipeline not complete when running."""
        pipeline = CIPipeline(
            id="1", status=PipelineStatus.RUNNING,
            branch="main", commit_sha="abc",
        )
        assert pipeline.is_complete is False

    def test_failed_jobs(self):
        """Get failed jobs."""
        pipeline = CIPipeline(
            id="1", status=PipelineStatus.FAILED,
            branch="main", commit_sha="abc",
            jobs=[
                CIJob(name="build", status=JobStatus.SUCCESS),
                CIJob(name="test", status=JobStatus.FAILED),
                CIJob(name="lint", status=JobStatus.FAILED),
            ],
        )
        failed = pipeline.failed_jobs
        assert len(failed) == 2
        assert all(j.status == JobStatus.FAILED for j in failed)


# =============================================================================
# Tests for TestResult Dataclass
# =============================================================================


class TestTestResult:
    """Tests for TestResult dataclass."""

    def test_passed(self):
        """Passed test result."""
        result = TestResult(name="test_add", passed=True)
        assert result.passed is True

    def test_failed(self):
        """Failed test result."""
        result = TestResult(
            name="test_sub",
            passed=False,
            error_message="AssertionError",
        )
        assert result.passed is False
        assert result.error_message == "AssertionError"


# =============================================================================
# Tests for TestSummary Dataclass
# =============================================================================


class TestTestSummary:
    """Tests for TestSummary dataclass."""

    def test_create(self):
        """Create test summary."""
        summary = TestSummary(
            total=10,
            passed=8,
            failed=1,
            skipped=1,
        )
        assert summary.total == 10
        assert summary.passed == 8

    def test_success_rate(self):
        """Calculate success rate."""
        summary = TestSummary(total=10, passed=8, failed=1, skipped=1)
        assert summary.success_rate == 80.0

    def test_success_rate_zero_total(self):
        """Success rate with zero total."""
        summary = TestSummary(total=0, passed=0, failed=0, skipped=0)
        assert summary.success_rate == 100.0


# =============================================================================
# Tests for CICDMonitor
# =============================================================================


class TestCICDMonitor:
    """Tests for CICDMonitor class."""

    def test_init(self, tmp_path):
        """Initialize monitor."""
        monitor = CICDMonitor(tmp_path)
        assert monitor.repo_path == tmp_path
        assert monitor.provider == "github"

    def test_init_with_github_actions(self, tmp_path):
        """Initialize with GitHub Actions."""
        workflows = tmp_path / ".github" / "workflows"
        workflows.mkdir(parents=True)
        (workflows / "ci.yml").write_text("name: CI")

        monitor = CICDMonitor(tmp_path)
        assert monitor.has_github_actions is True

    def test_init_without_ci(self, tmp_path):
        """Initialize without CI files."""
        monitor = CICDMonitor(tmp_path)
        assert monitor.has_github_actions is False
        assert monitor.has_gitlab_ci is False

    def test_get_pipelines_no_github(self, tmp_path):
        """Get pipelines without GitHub Actions."""
        monitor = CICDMonitor(tmp_path)
        pipelines = monitor.get_pipelines()
        assert pipelines == []

    def test_get_workflow_files(self, tmp_path):
        """Get workflow files."""
        workflows = tmp_path / ".github" / "workflows"
        workflows.mkdir(parents=True)
        (workflows / "ci.yml").write_text("name: CI")
        (workflows / "deploy.yaml").write_text("name: Deploy")

        monitor = CICDMonitor(tmp_path)
        files = monitor.get_workflow_files()
        assert len(files) == 2

    def test_validate_workflow_not_found(self, tmp_path):
        """Validate non-existent workflow."""
        monitor = CICDMonitor(tmp_path)
        errors = monitor.validate_workflow(tmp_path / "missing.yml")
        assert len(errors) == 1
        assert "not found" in errors[0]

    def test_validate_workflow_valid_yaml(self, tmp_path):
        """Validate valid YAML workflow."""
        workflow = tmp_path / "ci.yml"
        workflow.write_text("name: CI\non: push")

        monitor = CICDMonitor(tmp_path)
        errors = monitor.validate_workflow(workflow)
        assert len(errors) == 0


# =============================================================================
# Tests for PRState Enum
# =============================================================================


class TestPRState:
    """Tests for PRState enum."""

    def test_open(self):
        """OPEN state."""
        assert PRState.OPEN.name == "OPEN"

    def test_closed(self):
        """CLOSED state."""
        assert PRState.CLOSED.name == "CLOSED"

    def test_merged(self):
        """MERGED state."""
        assert PRState.MERGED.name == "MERGED"


# =============================================================================
# Tests for CheckStatus Enum
# =============================================================================


class TestCheckStatus:
    """Tests for CheckStatus enum."""

    def test_all_values(self):
        """All check status values exist."""
        assert CheckStatus.PENDING.name == "PENDING"
        assert CheckStatus.IN_PROGRESS.name == "IN_PROGRESS"
        assert CheckStatus.SUCCESS.name == "SUCCESS"
        assert CheckStatus.FAILURE.name == "FAILURE"
        assert CheckStatus.CANCELLED.name == "CANCELLED"
        assert CheckStatus.SKIPPED.name == "SKIPPED"
        assert CheckStatus.NEUTRAL.name == "NEUTRAL"


# =============================================================================
# Tests for GitHubCheck Dataclass
# =============================================================================


class TestGitHubCheck:
    """Tests for GitHubCheck dataclass."""

    def test_create(self):
        """Create check."""
        check = GitHubCheck(name="build", status=CheckStatus.SUCCESS)
        assert check.name == "build"
        assert check.status == CheckStatus.SUCCESS


# =============================================================================
# Tests for PullRequest Dataclass
# =============================================================================


class TestPullRequest:
    """Tests for PullRequest dataclass."""

    def test_create(self):
        """Create PR."""
        pr = PullRequest(
            number=123,
            title="Add feature",
            state=PRState.OPEN,
            head_branch="feature",
            base_branch="main",
            author="user1",
        )
        assert pr.number == 123
        assert pr.title == "Add feature"

    def test_all_checks_passed_empty(self):
        """All checks passed with no checks."""
        pr = PullRequest(
            number=1, title="Test",
            state=PRState.OPEN,
            head_branch="feature", base_branch="main",
            author="user",
        )
        assert pr.all_checks_passed is True

    def test_all_checks_passed_success(self):
        """All checks passed with success."""
        pr = PullRequest(
            number=1, title="Test",
            state=PRState.OPEN,
            head_branch="feature", base_branch="main",
            author="user",
            checks=[
                GitHubCheck(name="build", status=CheckStatus.SUCCESS),
                GitHubCheck(name="test", status=CheckStatus.SUCCESS),
            ],
        )
        assert pr.all_checks_passed is True

    def test_all_checks_passed_with_skipped(self):
        """All checks passed with skipped."""
        pr = PullRequest(
            number=1, title="Test",
            state=PRState.OPEN,
            head_branch="feature", base_branch="main",
            author="user",
            checks=[
                GitHubCheck(name="build", status=CheckStatus.SUCCESS),
                GitHubCheck(name="test", status=CheckStatus.SKIPPED),
            ],
        )
        assert pr.all_checks_passed is True

    def test_all_checks_passed_failure(self):
        """All checks passed with failure."""
        pr = PullRequest(
            number=1, title="Test",
            state=PRState.OPEN,
            head_branch="feature", base_branch="main",
            author="user",
            checks=[
                GitHubCheck(name="build", status=CheckStatus.SUCCESS),
                GitHubCheck(name="test", status=CheckStatus.FAILURE),
            ],
        )
        assert pr.all_checks_passed is False


# =============================================================================
# Tests for Issue Dataclass
# =============================================================================


class TestIssue:
    """Tests for Issue dataclass."""

    def test_create(self):
        """Create issue."""
        issue = Issue(
            number=456,
            title="Bug report",
            state="open",
            author="reporter",
        )
        assert issue.number == 456
        assert issue.title == "Bug report"

    def test_with_labels(self):
        """Issue with labels."""
        issue = Issue(
            number=1,
            title="Bug",
            state="open",
            author="user",
            labels=["bug", "priority:high"],
        )
        assert len(issue.labels) == 2


# =============================================================================
# Tests for GitHubOps
# =============================================================================


class TestGitHubOps:
    """Tests for GitHubOps class."""

    def test_init(self, tmp_path):
        """Initialize ops."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            ops = GitHubOps(tmp_path)
            assert ops.repo_path == tmp_path
            assert ops.gh_available is True

    def test_init_gh_not_available(self, tmp_path):
        """Initialize without gh CLI."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            ops = GitHubOps(tmp_path)
            assert ops.gh_available is False

    def test_run_gh_not_available(self, tmp_path):
        """Run gh when not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            ops = GitHubOps(tmp_path)

            with pytest.raises(RuntimeError) as exc:
                ops._run_gh(["repo", "view"])
            assert "not available" in str(exc.value)

    def test_get_repo_info_not_available(self, tmp_path):
        """Get repo info when gh not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            ops = GitHubOps(tmp_path)

            info = ops.get_repo_info()
            assert info == {}

    def test_list_prs_not_available(self, tmp_path):
        """List PRs when gh not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            ops = GitHubOps(tmp_path)

            prs = ops.list_prs()
            assert prs == []

    def test_get_pr_not_available(self, tmp_path):
        """Get PR when gh not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            ops = GitHubOps(tmp_path)

            pr = ops.get_pr(123)
            assert pr is None

    def test_create_pr_not_available(self, tmp_path):
        """Create PR when gh not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            ops = GitHubOps(tmp_path)

            pr = ops.create_pr("Test PR")
            assert pr is None

    def test_list_issues_not_available(self, tmp_path):
        """List issues when gh not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            ops = GitHubOps(tmp_path)

            issues = ops.list_issues()
            assert issues == []

    def test_get_workflow_runs_not_available(self, tmp_path):
        """Get workflow runs when gh not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            ops = GitHubOps(tmp_path)

            runs = ops.get_workflow_runs()
            assert runs == []

    def test_get_workflow_run_logs_not_available(self, tmp_path):
        """Get logs when gh not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            ops = GitHubOps(tmp_path)

            logs = ops.get_workflow_run_logs(123)
            assert logs is None

    def test_rerun_workflow_not_available(self, tmp_path):
        """Rerun workflow when gh not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            ops = GitHubOps(tmp_path)

            result = ops.rerun_workflow(123)
            assert result is False

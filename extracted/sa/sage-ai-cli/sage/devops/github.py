"""GitHub operations module for SAGE DevOps.

This module provides GitHub-specific operations including:
- Pull request management
- Issue management
- Actions workflow integration
- Repository information

NOTE: This is a stub implementation. Full functionality coming soon.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any

from sage.devops.models import CIPipeline, JobStatus, PipelineStatus, GitResult


class PRState(Enum):
    """State of a pull request."""

    OPEN = auto()
    CLOSED = auto()
    MERGED = auto()


class CheckStatus(Enum):
    """Status of a check/workflow."""

    PENDING = auto()
    IN_PROGRESS = auto()
    SUCCESS = auto()
    FAILURE = auto()
    CANCELLED = auto()
    SKIPPED = auto()
    NEUTRAL = auto()


@dataclass
class GitHubCheck:
    """A GitHub check or workflow run."""

    name: str
    status: CheckStatus
    conclusion: str | None = None
    url: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


@dataclass
class PullRequest:
    """A GitHub pull request."""

    number: int
    title: str
    state: PRState
    head_branch: str
    base_branch: str
    author: str
    body: str | None = None
    url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    checks: list[GitHubCheck] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    reviewers: list[str] = field(default_factory=list)

    @property
    def all_checks_passed(self) -> bool:
        """Check if all checks passed."""
        if not self.checks:
            return True
        return all(
            c.status == CheckStatus.SUCCESS or c.status == CheckStatus.SKIPPED for c in self.checks
        )


@dataclass
class Issue:
    """A GitHub issue."""

    number: int
    title: str
    state: str
    author: str
    body: str | None = None
    url: str | None = None
    created_at: datetime | None = None
    labels: list[str] = field(default_factory=list)
    assignees: list[str] = field(default_factory=list)


class GitHubOps:
    """GitHub operations handler.

    Provides GitHub-specific operations using the gh CLI.
    Requires gh CLI to be installed and authenticated.
    """

    def __init__(self, repo_path: Path | str | None = None):
        """Initialize GitHubOps.

        Args:
            repo_path: Path to the repository.
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self._validate_setup()

    def _validate_setup(self) -> None:
        """Validate GitHub CLI is available."""
        try:
            result = subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.gh_available = result.returncode == 0
        except FileNotFoundError:
            self.gh_available = False

    def _run_gh(
        self,
        args: list[str],
        check: bool = True,
    ) -> subprocess.CompletedProcess:
        """Run a gh CLI command."""
        if not self.gh_available:
            raise RuntimeError("GitHub CLI (gh) is not available")

        cmd = ["gh"] + args
        return subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=check,
        )

    def get_repo_info(self) -> dict[str, Any]:
        """Get repository information."""
        if not self.gh_available:
            return {}

        try:
            result = self._run_gh(["repo", "view", "--json", "name,owner,url,defaultBranchRef"])
            data: dict[str, Any] = json.loads(result.stdout)
            return data
        except Exception:
            return {}

    def pr_list(self, state: str = "open", limit: int = 10) -> list[PullRequest]:
        """Alias for list_prs() for backward compatibility."""
        return self.list_prs(state, limit)

    def pr_create(self, title: str, body: str | None = None, base: str | None = None, head: str | None = None, draft: bool = False) -> PullRequest | None:
        """Alias for create_pr() for backward compatibility."""
        return self.create_pr(title, body, base, head, draft)

    def list_prs(
        self,
        state: str = "open",
        limit: int = 10,
    ) -> list[PullRequest]:
        """List pull requests.

        Args:
            state: PR state ('open', 'closed', 'merged', 'all').
            limit: Maximum number of PRs to return.

        Returns:
            List of pull requests.
        """
        if not self.gh_available:
            return []

        try:
            result = self._run_gh(
                [
                    "pr",
                    "list",
                    "--state",
                    state,
                    "--limit",
                    str(limit),
                    "--json",
                    "number,title,state,headRefName,baseRefName,author,body,url,createdAt,labels",
                ]
            )
            data = json.loads(result.stdout)

            prs = []
            for item in data:
                state_map = {
                    "OPEN": PRState.OPEN,
                    "CLOSED": PRState.CLOSED,
                    "MERGED": PRState.MERGED,
                }
                prs.append(
                    PullRequest(
                        number=item["number"],
                        title=item["title"],
                        state=state_map.get(item["state"], PRState.OPEN),
                        head_branch=item["headRefName"],
                        base_branch=item["baseRefName"],
                        author=item["author"]["login"] if item.get("author") else "unknown",
                        body=item.get("body"),
                        url=item.get("url"),
                        labels=[l["name"] for l in item.get("labels", [])],
                    )
                )
            return prs
        except Exception:
            return []

    def get_pr(self, number: int) -> PullRequest | None:
        """Get a specific pull request.

        Args:
            number: PR number.

        Returns:
            The pull request, or None if not found.
        """
        if not self.gh_available:
            return None

        try:
            result = self._run_gh(
                [
                    "pr",
                    "view",
                    str(number),
                    "--json",
                    "number,title,state,headRefName,baseRefName,author,body,url,createdAt,labels,statusCheckRollup",
                ]
            )
            item = json.loads(result.stdout)

            state_map = {"OPEN": PRState.OPEN, "CLOSED": PRState.CLOSED, "MERGED": PRState.MERGED}

            checks = []
            for check in item.get("statusCheckRollup", []):
                status_map = {
                    "PENDING": CheckStatus.PENDING,
                    "IN_PROGRESS": CheckStatus.IN_PROGRESS,
                    "SUCCESS": CheckStatus.SUCCESS,
                    "FAILURE": CheckStatus.FAILURE,
                    "CANCELLED": CheckStatus.CANCELLED,
                }
                checks.append(
                    GitHubCheck(
                        name=check.get("name", "unknown"),
                        status=status_map.get(check.get("status"), CheckStatus.PENDING),
                        conclusion=check.get("conclusion"),
                    )
                )

            return PullRequest(
                number=item["number"],
                title=item["title"],
                state=state_map.get(item["state"], PRState.OPEN),
                head_branch=item["headRefName"],
                base_branch=item["baseRefName"],
                author=item["author"]["login"] if item.get("author") else "unknown",
                body=item.get("body"),
                url=item.get("url"),
                labels=[l["name"] for l in item.get("labels", [])],
                checks=checks,
            )
        except Exception:
            return None

    def create_pr(
        self,
        title: str,
        body: str | None = None,
        base: str | None = None,
        head: str | None = None,
        draft: bool = False,
    ) -> PullRequest | None:
        """Create a pull request.

        Args:
            title: PR title.
            body: PR body/description.
            base: Base branch (default: repo default branch).
            head: Head branch (default: current branch).
            draft: Create as draft PR.

        Returns:
            The created PR, or None if failed.
        """
        if not self.gh_available:
            return None

        args = ["pr", "create", "--title", title]
        if body:
            args.extend(["--body", body])
        if base:
            args.extend(["--base", base])
        if head:
            args.extend(["--head", head])
        if draft:
            args.append("--draft")

        try:
            result = self._run_gh(args)
            # Parse PR URL from output to get number
            url = result.stdout.strip()
            if url:
                # URL is like https://github.com/owner/repo/pull/123
                number = int(url.split("/")[-1])
                return self.get_pr(number)
        except Exception:
            pass
        return None

    def list_issues(
        self,
        state: str = "open",
        limit: int = 10,
    ) -> list[Issue]:
        """List issues.

        Args:
            state: Issue state ('open', 'closed', 'all').
            limit: Maximum number of issues to return.

        Returns:
            List of issues.
        """
        if not self.gh_available:
            return []

        try:
            result = self._run_gh(
                [
                    "issue",
                    "list",
                    "--state",
                    state,
                    "--limit",
                    str(limit),
                    "--json",
                    "number,title,state,author,body,url,createdAt,labels,assignees",
                ]
            )
            data = json.loads(result.stdout)

            issues = []
            for item in data:
                issues.append(
                    Issue(
                        number=item["number"],
                        title=item["title"],
                        state=item["state"],
                        author=item["author"]["login"] if item.get("author") else "unknown",
                        body=item.get("body"),
                        url=item.get("url"),
                        labels=[l["name"] for l in item.get("labels", [])],
                        assignees=[a["login"] for a in item.get("assignees", [])],
                    )
                )
            return issues
        except Exception:
            return []

    def run_list(
        self,
        workflow: str | None = None,
        branch: str | None = None,
        limit: int = 10,
    ) -> list[CIPipeline]:
        """List workflow runs. Alias for get_workflow_runs returning objects."""
        # Use CICDMonitor's implementation if available, or re-implement here
        # For simplicity and to avoid circular imports, we'll re-implement using gh CLI
        try:
            args = ["run", "list", "--limit", str(limit), "--json", "databaseId,displayTitle,status,conclusion,url,createdAt,headBranch,workflowName,headSha"]
            if workflow:
                args.extend(["--workflow", workflow])
            if branch:
                args.extend(["--branch", branch])

            result = self._run_gh(args)
            data = json.loads(result.stdout)

            runs = []
            for item in data:
                status_map = {
                    "queued": PipelineStatus.PENDING,
                    "in_progress": PipelineStatus.RUNNING,
                    "completed": PipelineStatus.SUCCESS,
                }
                if item.get("conclusion") == "failure":
                    status = PipelineStatus.FAILED
                elif item.get("conclusion") == "cancelled":
                    status = PipelineStatus.CANCELLED
                else:
                    status = status_map.get(item.get("status", ""), PipelineStatus.UNKNOWN)

                runs.append(
                    CIPipeline(
                        id=str(item["databaseId"]),
                        status=status,
                        branch=item.get("headBranch", ""),
                        commit_sha=item.get("headSha", "")[:7],
                        url=item.get("url"),
                        conclusion=item.get("conclusion"),
                        workflow_name=item.get("workflowName", "unknown"),
                        head_branch=item.get("headBranch", "unknown"),
                    )
                )
            return runs
        except Exception:
            return []

    def get_workflow_runs(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get recent workflow runs."""
        if not self.gh_available:
            return []

        try:
            result = self._run_gh(
                [
                    "run",
                    "list",
                    "--limit",
                    str(limit),
                    "--json",
                    "databaseId,displayTitle,status,conclusion,url,createdAt,headBranch,workflowName",
                ]
            )
            data: list[dict[str, Any]] = json.loads(result.stdout)
            return data
        except Exception:
            return []

    def get_workflow_run_logs(self, run_id: int) -> str | None:
        """Get logs for a workflow run."""
        if not self.gh_available:
            return None

        try:
            result = self._run_gh(["run", "view", str(run_id), "--log"])
            return str(result.stdout) if result.stdout else None
        except Exception:
            return None

    def run_rerun(self, run_id: int | str, failed_only: bool = True) -> GitResult:
        """Re-run a workflow run."""
        if not self.gh_available:
            return GitResult(success=False, error="GitHub CLI not available")

        args = ["run", "rerun", str(run_id)]
        if failed_only:
            args.append("--failed")

        try:
            result = self._run_gh(args)
            return GitResult(success=True, output=result.stdout)
        except Exception as e:
            return GitResult(success=False, error=str(e))

    def rerun_workflow(self, run_id: int) -> bool:
        """Alias for run_rerun for backward compatibility."""
        return self.run_rerun(run_id).success

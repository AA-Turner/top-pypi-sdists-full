"""GitHub Pull Request fetcher using gh CLI."""

import json
import os
import re
import shutil
import subprocess
from datetime import datetime
from typing import Optional

from ...core.models import PullRequestEntity
from ...utils.logger import log


class PRFetcher:
    """Fetches pull requests using gh CLI (supports private repos)."""

    # Pattern to extract owner/repo from GitHub URLs
    GITHUB_URL_PATTERN = re.compile(
        r"(?:https?://)?(?:www\.)?github\.com[/:]([^/]+)/([^/.]+)(?:\.git)?/?$"
    )

    def __init__(
        self,
        owner: str,
        repo: str,
        token: Optional[str] = None,
    ):
        """Initialize PR fetcher.

        Args:
            owner: GitHub repository owner
            repo: GitHub repository name
            token: GitHub personal access token (ignored, uses gh CLI auth)
        """
        self.owner = owner
        self.repo = repo
        self.repo_path = f"{owner}/{repo}"

        # Find gh CLI binary
        self.gh_path = self._find_gh_cli()
        if not self.gh_path:
            log.warning(
                "gh CLI not found. Install with 'brew install gh' and authenticate with 'gh auth login'. "
                "PR fetching will be skipped."
            )

    def _find_gh_cli(self) -> Optional[str]:
        """Find the gh CLI binary path."""
        # Check common locations
        paths_to_check = [
            shutil.which("gh"),
            "/opt/homebrew/bin/gh",
            "/usr/local/bin/gh",
            "/usr/bin/gh",
        ]
        for path in paths_to_check:
            if path and shutil.os.path.isfile(path):
                return path
        return None

    def _run_gh(self, args: list[str]) -> Optional[str]:
        """Run a gh CLI command and return output."""
        if not self.gh_path:
            return None
        try:
            # Copy environment but remove GITHUB_TOKEN to let gh use its own OAuth
            env = os.environ.copy()
            env.pop("GITHUB_TOKEN", None)
            env.pop("GH_TOKEN", None)

            result = subprocess.run(
                [self.gh_path] + args,
                capture_output=True,
                text=True,
                timeout=120,
                env=env,
            )
            if result.returncode == 0:
                return result.stdout
            else:
                log.error(f"gh CLI error: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            log.error("gh CLI command timed out")
            return None
        except Exception as e:
            log.error(f"gh CLI error: {e}")
            return None

    @classmethod
    def extract_repo_info(cls, remote_url: str) -> tuple[Optional[str], Optional[str]]:
        """Extract owner and repo name from a GitHub remote URL.

        Args:
            remote_url: Git remote URL (HTTPS or SSH format)

        Returns:
            Tuple of (owner, repo) or (None, None) if not a GitHub URL

        Examples:
            >>> PRFetcher.extract_repo_info("https://github.com/owner/repo.git")
            ('owner', 'repo')
            >>> PRFetcher.extract_repo_info("git@github.com:owner/repo.git")
            ('owner', 'repo')
        """
        # Handle SSH format: git@github.com:owner/repo.git
        if remote_url.startswith("git@github.com:"):
            parts = remote_url.replace("git@github.com:", "").replace(".git", "").split("/")
            if len(parts) >= 2:
                return parts[0], parts[1]

        # Handle HTTPS format
        match = cls.GITHUB_URL_PATTERN.match(remote_url)
        if match:
            return match.group(1), match.group(2)

        return None, None

    def fetch_prs(
        self,
        state: str = "all",
        limit: Optional[int] = 100,
        since: Optional[datetime] = None,
    ) -> list[PullRequestEntity]:
        """Fetch pull requests from the repository using gh CLI.

        Args:
            state: PR state filter ("open", "closed", "all")
            limit: Maximum number of PRs to fetch (None for all)
            since: Only fetch PRs updated after this datetime

        Returns:
            List of PullRequestEntity objects
        """
        if not self.gh_path:
            log.error("gh CLI not available. Cannot fetch PRs.")
            return []

        prs = []

        # Map state to gh CLI format
        states_to_fetch = []
        if state == "all":
            states_to_fetch = ["open", "closed", "merged"]
        elif state == "closed":
            states_to_fetch = ["closed", "merged"]
        else:
            states_to_fetch = [state]

        for pr_state in states_to_fetch:
            # Build gh pr list command - request minimal fields to avoid GraphQL limits
            args = [
                "pr", "list",
                "-R", self.repo_path,
                "--state", pr_state,
                "--limit", str(limit or 100),
                "--json", "number,title,body,state,createdAt,author,mergedAt,labels,additions,deletions,baseRefName,headRefName"
            ]

            output = self._run_gh(args)
            if not output:
                continue

            try:
                pr_list = json.loads(output)
            except json.JSONDecodeError as e:
                log.error(f"Failed to parse gh output: {e}")
                continue

            for pr_data in pr_list:
                # Check date filter
                if since:
                    created_at = self._parse_datetime(pr_data.get("createdAt"))
                    if created_at and created_at < since:
                        continue

                pr_entity = self._extract_pr_from_json(pr_data)
                prs.append(pr_entity)

                if len(prs) % 10 == 0:
                    log.info(f"Fetched {len(prs)} PRs...")

                # Check limit
                if limit and len(prs) >= limit:
                    break

            if limit and len(prs) >= limit:
                break

        log.info(f"Fetched {len(prs)} pull requests from {self.repo_path}")
        return prs

    def fetch_pr_files(self, pr_number: int) -> list[str]:
        """Get files changed in a specific PR.

        Args:
            pr_number: Pull request number

        Returns:
            List of file paths that were modified
        """
        if not self.gh_path:
            return []

        args = [
            "pr", "view", str(pr_number),
            "-R", self.repo_path,
            "--json", "files"
        ]

        output = self._run_gh(args)
        if not output:
            return []

        try:
            data = json.loads(output)
            return [f.get("path", "") for f in data.get("files", [])]
        except json.JSONDecodeError:
            return []

    def _parse_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
        """Parse ISO datetime string."""
        if not dt_str:
            return None
        try:
            # Handle ISO format with Z suffix
            dt_str = dt_str.replace("Z", "+00:00")
            return datetime.fromisoformat(dt_str)
        except (ValueError, AttributeError):
            return None

    def _extract_pr_from_json(self, pr_data: dict) -> PullRequestEntity:
        """Extract PR data from gh CLI JSON output.

        Args:
            pr_data: PR data from gh CLI

        Returns:
            PullRequestEntity with extracted data
        """
        # Determine state
        state = pr_data.get("state", "open").lower()
        if pr_data.get("mergedAt"):
            state = "merged"

        # Get reviewers
        reviewers = set()
        for req in pr_data.get("reviewRequests", []):
            if isinstance(req, dict) and req.get("login"):
                reviewers.add(req["login"])
        for review in pr_data.get("reviews", []):
            if isinstance(review, dict) and review.get("author", {}).get("login"):
                reviewers.add(review["author"]["login"])

        # Get commit SHAs
        commit_shas = []
        for commit in pr_data.get("commits", []):
            if isinstance(commit, dict) and commit.get("oid"):
                commit_shas.append(commit["oid"])

        # Get files changed
        files_changed = []
        for f in pr_data.get("files", []):
            if isinstance(f, dict) and f.get("path"):
                files_changed.append(f["path"])

        # Get labels
        labels = []
        for label in pr_data.get("labels", []):
            if isinstance(label, dict) and label.get("name"):
                labels.append(label["name"])

        # Get author
        author = "unknown"
        author_data = pr_data.get("author")
        if isinstance(author_data, dict):
            author = author_data.get("login", "unknown")

        return PullRequestEntity(
            number=pr_data.get("number", 0),
            title=pr_data.get("title", ""),
            description=pr_data.get("body"),
            state=state,
            created_at=self._parse_datetime(pr_data.get("createdAt")),
            author=author,
            merged_at=self._parse_datetime(pr_data.get("mergedAt")),
            reviewers=list(reviewers),
            labels=labels,
            additions=pr_data.get("additions", 0),
            deletions=pr_data.get("deletions", 0),
            files_changed=files_changed,
            commit_shas=commit_shas,
            base_branch=pr_data.get("baseRefName", "main"),
            head_branch=pr_data.get("headRefName", ""),
        )

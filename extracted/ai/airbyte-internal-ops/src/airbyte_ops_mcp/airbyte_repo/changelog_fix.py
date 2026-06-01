# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Changelog date fixing and checking utilities for Airbyte connectors.

This module provides functionality to fix and check changelog entry dates by looking up
the actual PR merge dates from GitHub.
"""

from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from airbyte_ops_mcp.airbyte_repo.bump_version import (
    AIRBYTE_GITHUB_REPO,
    get_connector_doc_path,
)
from airbyte_ops_mcp.airbyte_repo.list_connectors import get_all_connectors
from airbyte_ops_mcp.github_api import GitHubAPIError, get_pr_merge_date


class ChangelogIssueType(StrEnum):
    """Types of changelog issues that can be detected."""

    PR_MISMATCH = "pr_mismatch"


@dataclass
class ChangelogDateFix:
    """A single changelog date fix."""

    line_number: int
    version: str
    pr_number: int
    old_date: datetime.date
    new_date: datetime.date

    @property
    def changed(self) -> bool:
        """Return True if the date was changed."""
        return self.old_date != self.new_date


@dataclass
class ChangelogIssue:
    """A single changelog issue found during checking."""

    line_number: int
    version: str
    issue_type: ChangelogIssueType
    message: str


@dataclass
class ChangelogCheckResult:
    """Result of checking changelog for a connector."""

    connector: str
    doc_path: Path | None
    date_issues: list[ChangelogDateFix]
    pr_mismatch_warnings: list[ChangelogIssue]
    errors: list[str]

    @property
    def has_issues(self) -> bool:
        """Return True if any issues were found."""
        return (
            any(fix.changed for fix in self.date_issues)
            or len(self.pr_mismatch_warnings) > 0
        )

    @property
    def issue_count(self) -> int:
        """Return the total number of issues found."""
        return sum(1 for fix in self.date_issues if fix.changed) + len(
            self.pr_mismatch_warnings
        )


@dataclass
class ChangelogFixResult:
    """Result of fixing changelog dates for a connector."""

    connector: str
    doc_path: Path | None
    fixes: list[ChangelogDateFix]
    warnings: list[ChangelogIssue]
    errors: list[str]
    dry_run: bool

    @property
    def has_changes(self) -> bool:
        """Return True if any dates were changed."""
        return any(fix.changed for fix in self.fixes)

    @property
    def changed_count(self) -> int:
        """Return the number of dates that were changed."""
        return sum(1 for fix in self.fixes if fix.changed)


def _parse_changelog_entries(
    content: str,
    github_repo: str = AIRBYTE_GITHUB_REPO,
) -> list[tuple[int, str, str, int, int, str]]:
    """Parse changelog entries from markdown content.

    Args:
        content: The markdown content of the documentation file.
        github_repo: GitHub repository for PR links.

    Returns:
        List of tuples: (line_number, version, date_str, displayed_pr_number, url_pr_number, full_line)
    """
    # Regex to parse changelog table rows in the format:
    # | version | date | [pr_num](url) | comment |
    changelog_entry_re = (
        # Match table row start and capture semantic version (e.g., "1.2.3")
        r"^\| *(?P<version>[0-9]+\.[0-9]+\.[0-9]+) *\| *"
        # Capture date in ISO format YYYY-MM-DD
        r"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2}) *\| *"
        # Capture displayed PR number (may be in brackets as markdown link)
        r"\[?(?P<displayed_pr>[0-9]+)\]?\(https://github.com/"
        # GitHub repo portion (escaped to handle special chars)
        + re.escape(github_repo)
        # Capture PR number from URL path
        + r"/pull/(?P<url_pr>[0-9]+)\) *\| *"
        # Capture comment text until end of row
        r"(?P<comment>.*?) *\| *$"
    )

    entries = []
    lines = content.splitlines()

    for line_num, line in enumerate(lines, start=1):
        match = re.match(changelog_entry_re, line)
        if match:
            version = match.group("version")
            date_str = match.group("date")
            displayed_pr = int(match.group("displayed_pr"))
            url_pr = int(match.group("url_pr"))
            entries.append((line_num, version, date_str, displayed_pr, url_pr, line))

    return entries


def check_changelog(
    repo_path: str | Path,
    connector_name: str,
    lookback_days: int | None = None,
    github_repo: str = AIRBYTE_GITHUB_REPO,
    token: str | None = None,
) -> ChangelogCheckResult:
    """Check changelog for issues (incorrect dates, mismatched PR numbers).

    Args:
        repo_path: Path to the Airbyte monorepo.
        connector_name: Technical name of the connector (e.g., "source-github").
        lookback_days: Only check entries with dates within this many days. None for all.
        github_repo: GitHub repository for PR links.
        token: GitHub API token. If None, will be resolved from environment.

    Returns:
        ChangelogCheckResult with details of any issues found.
    """
    repo_path = Path(repo_path)
    date_issues: list[ChangelogDateFix] = []
    pr_mismatch_warnings: list[ChangelogIssue] = []
    errors: list[str] = []

    doc_path = get_connector_doc_path(repo_path, connector_name)
    if doc_path is None or not doc_path.exists():
        return ChangelogCheckResult(
            connector=connector_name,
            doc_path=None,
            date_issues=[],
            pr_mismatch_warnings=[],
            errors=[f"Documentation file not found for {connector_name}"],
        )

    content = doc_path.read_text()
    entries = _parse_changelog_entries(content, github_repo)

    if not entries:
        return ChangelogCheckResult(
            connector=connector_name,
            doc_path=doc_path,
            date_issues=[],
            pr_mismatch_warnings=[],
            errors=[],
        )

    owner, repo = github_repo.split("/")
    cutoff_date = None
    if lookback_days is not None:
        cutoff_date = datetime.date.today() - datetime.timedelta(days=lookback_days)

    for line_num, version, date_str, displayed_pr, url_pr, _full_line in entries:
        entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        # Skip entries older than the lookback threshold
        if cutoff_date is not None and entry_date < cutoff_date:
            continue

        if displayed_pr != url_pr:
            pr_mismatch_warnings.append(
                ChangelogIssue(
                    line_number=line_num,
                    version=version,
                    issue_type=ChangelogIssueType.PR_MISMATCH,
                    message=f"Displayed PR number ({displayed_pr}) does not match URL PR number ({url_pr})",
                )
            )

        merge_date = None
        try:
            merge_date = get_pr_merge_date(owner, repo, url_pr, token)
        except GitHubAPIError as e:
            errors.append(f"Failed to fetch PR {url_pr}: {e}")
            continue

        if merge_date is None:
            errors.append(f"PR {url_pr} is not merged")
            continue

        date_issues.append(
            ChangelogDateFix(
                line_number=line_num,
                version=version,
                pr_number=url_pr,
                old_date=entry_date,
                new_date=merge_date,
            )
        )

    return ChangelogCheckResult(
        connector=connector_name,
        doc_path=doc_path,
        date_issues=date_issues,
        pr_mismatch_warnings=pr_mismatch_warnings,
        errors=errors,
    )


def fix_changelog_dates(
    repo_path: str | Path,
    connector_name: str,
    dry_run: bool = False,
    lookback_days: int | None = None,
    github_repo: str = AIRBYTE_GITHUB_REPO,
    token: str | None = None,
) -> ChangelogFixResult:
    """Fix changelog dates for a connector by looking up PR merge dates.

    Args:
        repo_path: Path to the Airbyte monorepo.
        connector_name: Technical name of the connector (e.g., "source-github").
        dry_run: If True, don't actually modify the file.
        lookback_days: Only fix entries with dates within this many days. None for all.
        github_repo: GitHub repository for PR links.
        token: GitHub API token. If None, will be resolved from environment.

    Returns:
        ChangelogFixResult with details of the fixes applied.
    """
    repo_path = Path(repo_path)
    fixes: list[ChangelogDateFix] = []
    warnings: list[ChangelogIssue] = []
    errors: list[str] = []

    doc_path = get_connector_doc_path(repo_path, connector_name)
    if doc_path is None or not doc_path.exists():
        return ChangelogFixResult(
            connector=connector_name,
            doc_path=None,
            fixes=[],
            warnings=[],
            errors=[f"Documentation file not found for {connector_name}"],
            dry_run=dry_run,
        )

    content = doc_path.read_text()
    entries = _parse_changelog_entries(content, github_repo)

    if not entries:
        return ChangelogFixResult(
            connector=connector_name,
            doc_path=doc_path,
            fixes=[],
            warnings=[],
            errors=[],
            dry_run=dry_run,
        )

    owner, repo = github_repo.split("/")
    lines = content.splitlines()
    # Track which lines need to be modified: line_num (1-indexed) -> new_line
    line_replacements: dict[int, str] = {}
    cutoff_date = None
    if lookback_days is not None:
        cutoff_date = datetime.date.today() - datetime.timedelta(days=lookback_days)

    for line_num, version, date_str, displayed_pr, url_pr, full_line in entries:
        entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        # Skip entries older than the lookback threshold
        if cutoff_date is not None and entry_date < cutoff_date:
            continue

        if displayed_pr != url_pr:
            warnings.append(
                ChangelogIssue(
                    line_number=line_num,
                    version=version,
                    issue_type=ChangelogIssueType.PR_MISMATCH,
                    message=f"Displayed PR number ({displayed_pr}) does not match URL PR number ({url_pr})",
                )
            )

        merge_date = None
        try:
            merge_date = get_pr_merge_date(owner, repo, url_pr, token)
        except GitHubAPIError as e:
            errors.append(f"Failed to fetch PR {url_pr}: {e}")
            continue

        if merge_date is None:
            errors.append(f"PR {url_pr} is not merged")
            continue

        fix = ChangelogDateFix(
            line_number=line_num,
            version=version,
            pr_number=url_pr,
            old_date=entry_date,
            new_date=merge_date,
        )
        fixes.append(fix)

        if fix.changed:
            new_line = full_line.replace(date_str, merge_date.strftime("%Y-%m-%d"))
            line_replacements[line_num] = new_line

    # Apply line replacements by line number to avoid issues with duplicate lines
    if line_replacements:
        for line_num, new_line in line_replacements.items():
            lines[line_num - 1] = new_line  # Convert 1-indexed to 0-indexed
        new_content = "\n".join(lines)
        if content.endswith("\n"):
            new_content += "\n"
    else:
        new_content = content

    if not dry_run and new_content != content:
        doc_path.write_text(new_content)

    return ChangelogFixResult(
        connector=connector_name,
        doc_path=doc_path,
        fixes=fixes,
        warnings=warnings,
        errors=errors,
        dry_run=dry_run,
    )


def check_all_changelogs(
    repo_path: str | Path,
    lookback_days: int | None = None,
    github_repo: str = AIRBYTE_GITHUB_REPO,
    token: str | None = None,
) -> list[ChangelogCheckResult]:
    """Check changelogs for all connectors in the repository.

    Args:
        repo_path: Path to the Airbyte monorepo.
        lookback_days: Only check entries with dates within this many days. None for all.
        github_repo: GitHub repository for PR links.
        token: GitHub API token. If None, will be resolved from environment.

    Returns:
        List of ChangelogCheckResult for each connector processed.
    """
    repo_path = Path(repo_path)
    connectors = get_all_connectors(repo_path)

    results = []
    for connector_name in sorted(connectors):
        result = check_changelog(
            repo_path=repo_path,
            connector_name=connector_name,
            lookback_days=lookback_days,
            github_repo=github_repo,
            token=token,
        )
        results.append(result)

    return results


def fix_all_changelog_dates(
    repo_path: str | Path,
    dry_run: bool = False,
    lookback_days: int | None = None,
    github_repo: str = AIRBYTE_GITHUB_REPO,
    token: str | None = None,
) -> list[ChangelogFixResult]:
    """Fix changelog dates for all connectors in the repository.

    Args:
        repo_path: Path to the Airbyte monorepo.
        dry_run: If True, don't actually modify files.
        lookback_days: Only fix entries with dates within this many days. None for all.
        github_repo: GitHub repository for PR links.
        token: GitHub API token. If None, will be resolved from environment.

    Returns:
        List of ChangelogFixResult for each connector processed.
    """
    repo_path = Path(repo_path)
    connectors = get_all_connectors(repo_path)

    results = []
    for connector_name in sorted(connectors):
        result = fix_changelog_dates(
            repo_path=repo_path,
            connector_name=connector_name,
            dry_run=dry_run,
            lookback_days=lookback_days,
            github_repo=github_repo,
            token=token,
        )
        results.append(result)

    return results

"""Artifact collection for the retro-spec command.

Gathers issue body, comments, related PRs, PR diffs, and commit messages
from the GitHub API for synthesis into a retroactive spec.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field

# Default diff budget limits
_DEFAULT_FILE_DIFF_MAX = 4000
_DEFAULT_DIFF_BUDGET = 80_000
_FILE_DIFF_TRUNCATION_MARKER = "\n[Diff truncated: per-file diff limit reached.]\n"
_SHORT_FILE_DIFF_TRUNCATION_MARKER = "[truncated]"

# Conventional Commit scope pattern matching issue references like:
# feat(#42): ... | fix(#10/#42): ... | feat(#5, #42): ... | feat(#42)!: ...
_CONV_COMMIT_SCOPE_RE = re.compile(r"\(([^)]*#\d+[^)]*)\)!?:")


@dataclass
class IssueArtifact:
    """Collected issue data.

    Attributes:
        number: Issue number.
        title: Issue title.
        body: Issue body content.
        comments: List of comment bodies.
        labels: List of label names.
        milestone: Milestone title, if any.
        state: Issue state (e.g., 'closed').
    """

    number: int
    title: str
    body: str
    comments: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    milestone: str = ""
    state: str = "closed"


@dataclass
class PRArtifact:
    """Collected PR data.

    Attributes:
        number: PR number.
        title: PR title.
        body: PR body content.
        state: PR state (e.g., 'merged').
        merged_at: Merge timestamp string for ordering.
    """

    number: int
    title: str
    body: str
    state: str = "merged"
    merged_at: str = ""


def _get_diff_budget() -> int:
    """Get cumulative diff budget from environment or default."""
    raw = os.environ.get("AGDT_RETRO_SPEC_DIFF_BUDGET", "")
    if raw:
        try:
            val = int(raw)
            if val > 0:
                return val
        except ValueError:
            pass
        print(
            f"Warning: Invalid AGDT_RETRO_SPEC_DIFF_BUDGET value '{raw}', using default {_DEFAULT_DIFF_BUDGET}.",
            file=sys.stderr,
        )
    return _DEFAULT_DIFF_BUDGET


def get_diff_budget() -> int:
    """Get cumulative diff budget from environment or default."""
    return _get_diff_budget()


def _get_file_diff_max() -> int:
    """Get per-file diff max from environment or default."""
    raw = os.environ.get("AGDT_RETRO_SPEC_FILE_DIFF_MAX", "")
    if raw:
        try:
            val = int(raw)
            if val > 0:
                return val
        except ValueError:
            pass
        print(
            f"Warning: Invalid AGDT_RETRO_SPEC_FILE_DIFF_MAX value '{raw}', using default {_DEFAULT_FILE_DIFF_MAX}.",
            file=sys.stderr,
        )
    return _DEFAULT_FILE_DIFF_MAX


def fetch_issue(owner: str, repo: str, issue_number: int) -> IssueArtifact:
    """Fetch issue body, comments, labels, and milestone from GitHub.

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
        issue_number: The issue number to fetch.

    Returns:
        IssueArtifact with collected data.

    Raises:
        SystemExit: If the issue is not found or gh CLI is unavailable.
    """
    try:
        result = subprocess.run(
            [
                "gh",
                "api",
                f"/repos/{owner}/{repo}/issues/{issue_number}",
            ],
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError as exc:
        if isinstance(exc, FileNotFoundError):
            print(
                "Error: Could not execute GitHub CLI (`gh`). "
                "Install GitHub CLI before running this command.\n"
                "If not already authenticated after installation, run: `gh auth login`",
                file=sys.stderr,
            )
        else:
            print(
                "Error: Could not execute GitHub CLI (`gh`). Verify that `gh` "
                "is executable and accessible from your PATH.",
                file=sys.stderr,
            )
        print(f"Details: {exc}", file=sys.stderr)
        sys.exit(1)

    if result.returncode != 0:
        stderr_text = result.stderr.strip()
        if "404" in stderr_text or "Not Found" in stderr_text:
            print(
                f"Error: Issue #{issue_number} not found. This may be because:\n"
                f"  • The issue number is incorrect\n"
                f"  • Your token does not have sufficient permissions\n"
                f"Verify the issue exists at https://github.com/{owner}/{repo}/issues/{issue_number}",
                file=sys.stderr,
            )
        elif "rate limit" in stderr_text.lower():
            print(
                f"Error: GitHub API rate limit exceeded while fetching issue #{issue_number}.\n"
                "Wait for the rate limit to reset and try again.",
                file=sys.stderr,
            )
        else:
            print(
                f"Error: Could not fetch issue #{issue_number}. "
                f"Ensure the issue exists and your token has access.\n"
                f"Details: {stderr_text}",
                file=sys.stderr,
            )
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(
            f"Error: Unexpected response when fetching issue #{issue_number}. "
            "The GitHub API did not return valid JSON.",
            file=sys.stderr,
        )
        sys.exit(1)
    if not isinstance(data, dict):
        print(
            f"Error: Unexpected response when fetching issue #{issue_number}. "
            "The GitHub API returned an object in an unsupported format.",
            file=sys.stderr,
        )
        sys.exit(1)

    state = data.get("state", "")
    if state != "closed":
        print(
            f"Error: Issue #{issue_number} is not closed (state: {state}). "
            "The retro-spec command only works with closed/implemented issues.",
            file=sys.stderr,
        )
        sys.exit(1)

    raw_title = data.get("title", "")
    title = raw_title.strip() if isinstance(raw_title, str) else ""
    if not title:
        title = f"Issue #{issue_number}"
    body = data.get("body", "") or ""
    if not isinstance(body, str):
        body = ""
    raw_labels = data.get("labels", [])
    labels = (
        [
            label["name"]
            for label in raw_labels
            if isinstance(label, dict) and isinstance(label.get("name"), str) and label["name"]
        ]
        if isinstance(raw_labels, list)
        else []
    )
    milestone_data = data.get("milestone")
    milestone = milestone_data.get("title", "") if isinstance(milestone_data, dict) else ""
    if not isinstance(milestone, str):
        milestone = ""

    # Fetch comments
    comments: list[str] = []
    try:
        comments_result = subprocess.run(
            [
                "gh",
                "api",
                f"/repos/{owner}/{repo}/issues/{issue_number}/comments",
                "--jq",
                ".[].body | @json",
            ],
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError:
        comments_result = subprocess.CompletedProcess([], 1, "", "")
    if comments_result.returncode == 0 and comments_result.stdout.strip():
        for line in comments_result.stdout.splitlines():
            if not line.strip():
                continue
            try:
                comment = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(comment, str) and comment:
                comments.append(comment)

    return IssueArtifact(
        number=issue_number,
        title=title,
        body=body,
        comments=comments,
        labels=labels,
        milestone=milestone,
        state=state,
    )


def discover_related_prs(owner: str, repo: str, issue_number: int) -> list[PRArtifact]:
    """Discover PRs that reference the given issue via keywords or conventional commit scope.

    Two-pass discovery:
    1. Primary: Search for PRs with closing keywords (closes/fixes/resolves/relates to #N)
    2. Secondary: Search PR titles for Conventional Commit scope patterns containing #N

    Results are deduplicated by PR number and sorted by merge date ascending.

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
        issue_number: The issue number to search for.

    Returns:
        Deduplicated list of PRArtifact objects for related merged PRs.
    """
    seen: set[int] = set()
    artifacts: list[PRArtifact] = []

    # Primary search: closing keywords
    primary_prs = _search_prs_by_keywords(owner, repo, issue_number)
    for pr in primary_prs:
        if pr.number not in seen:
            seen.add(pr.number)
            artifacts.append(pr)

    # Secondary search: conventional commit scope in title
    secondary_prs = _search_prs_by_title_scope(owner, repo, issue_number)
    for pr in secondary_prs:
        if pr.number not in seen:
            seen.add(pr.number)
            artifacts.append(pr)

    # Sort by merge date ascending
    artifacts.sort(key=lambda pr: pr.merged_at)
    return artifacts


def _search_prs_by_keywords(owner: str, repo: str, issue_number: int) -> list[PRArtifact]:
    """Search for merged PRs with closing keywords referencing the issue."""
    try:
        result = subprocess.run(
            [
                "gh",
                "pr",
                "list",
                "--repo",
                f"{owner}/{repo}",
                "--state",
                "merged",
                "--search",
                (
                    f"closes #{issue_number} OR fixes #{issue_number}"
                    f" OR resolves #{issue_number} OR relates to #{issue_number}"
                ),
                "--json",
                "number,title,body,state,mergedAt",
            ],
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError:
        return []
    if result.returncode != 0:
        return []

    try:
        prs = json.loads(result.stdout) if result.stdout.strip() else []
    except json.JSONDecodeError:
        return []

    if not isinstance(prs, list):
        return []
    artifacts: list[PRArtifact] = []
    for pr in prs:
        artifact = _pr_artifact_from_payload(pr)
        if artifact is not None:
            artifacts.append(artifact)
    return artifacts


def _search_prs_by_title_scope(owner: str, repo: str, issue_number: int) -> list[PRArtifact]:
    """Search for merged PRs with Conventional Commit scope containing issue number."""
    try:
        result = subprocess.run(
            [
                "gh",
                "pr",
                "list",
                "--repo",
                f"{owner}/{repo}",
                "--state",
                "merged",
                "--search",
                f"#{issue_number} in:title",
                "--json",
                "number,title,body,state,mergedAt",
            ],
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError:
        return []
    if result.returncode != 0:
        return []

    try:
        prs = json.loads(result.stdout) if result.stdout.strip() else []
    except json.JSONDecodeError:
        return []

    # Filter: only include PRs whose title has a conventional commit scope containing #N
    artifacts: list[PRArtifact] = []
    if not isinstance(prs, list):
        return []
    for pr in prs:
        artifact = _pr_artifact_from_payload(pr)
        if artifact is None:
            continue
        title = artifact.title
        match = _CONV_COMMIT_SCOPE_RE.search(title)
        if match and re.search(rf"(?<!\d)#{issue_number}(?!\d)", match.group(1)):
            artifacts.append(artifact)
    return artifacts


def _pr_artifact_from_payload(payload: object) -> PRArtifact | None:
    """Normalize one GitHub PR response entry, ignoring malformed entries."""
    if not isinstance(payload, dict):
        return None
    number = payload.get("number", 0)
    title = payload.get("title", "")
    # bool is a subclass of int; reject booleans explicitly so that a JSON
    # payload with "number": true is not accepted as a valid PR identifier.
    if isinstance(number, bool) or not isinstance(number, int) or number <= 0 or not isinstance(title, str):
        return None
    body = payload.get("body", "") or ""
    if not isinstance(body, str):
        body = ""
    state = payload.get("state", "MERGED")
    if not isinstance(state, str):
        state = "MERGED"
    merged_at = payload.get("mergedAt", "") or ""
    if not isinstance(merged_at, str):
        merged_at = ""
    return PRArtifact(
        number=number,
        title=title,
        body=body,
        state=state,
        merged_at=merged_at,
    )


def fetch_pr_diffs(owner: str, repo: str, pr_number: int) -> list[str]:
    """Retrieve per-file diffs for a PR with budget management.

    Each file diff is capped at AGDT_RETRO_SPEC_FILE_DIFF_MAX chars.
    Overall cumulative budget is capped at AGDT_RETRO_SPEC_DIFF_BUDGET chars.
    Files are returned in ascending lexical order by path.

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
        pr_number: The PR number.

    Returns:
        List of per-file diff strings (budget-managed).
    """
    file_diff_max = _get_file_diff_max()
    diff_budget = _get_diff_budget()

    try:
        result = subprocess.run(
            [
                "gh",
                "pr",
                "diff",
                str(pr_number),
                "--repo",
                f"{owner}/{repo}",
            ],
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError:
        return [f"[Could not retrieve diff for PR #{pr_number}]"]
    if result.returncode != 0:
        return [f"[Could not retrieve diff for PR #{pr_number}]"]

    # Split into per-file chunks
    raw_diff = result.stdout
    file_diffs = _split_diff_by_file(raw_diff)

    # Sort by file path (lexical ascending)
    file_diffs.sort(key=lambda fd: fd[0])

    # Apply budget
    output: list[str] = []
    budget_used = 0
    budget_exhausted = False
    for path, content in file_diffs:
        remaining = diff_budget - budget_used
        if remaining <= 0:
            budget_exhausted = True
            break

        truncated = content
        if len(content) > file_diff_max:
            truncated = _truncate_diff_to_per_file_cap(content, file_diff_max)
        entry = f"--- {path} ---\n{truncated}"
        if len(entry) > remaining:
            # Drop the file entirely rather than including a partial entry —
            # synthesis quality is better served by omitting incomplete diffs.
            budget_exhausted = True
            break

        output.append(entry)
        budget_used += len(entry)

    if budget_exhausted:
        output.append("[Diff budget exhausted: subsequent PR files were omitted from this retroactive spec.]")
    return output


def _truncate_diff_to_per_file_cap(content: str, file_diff_max: int) -> str:
    """Return a per-file diff body that never exceeds ``file_diff_max`` chars.

    Prefers the full truncation marker when it fits, falls back to the compact
    ``[truncated]`` marker when only that fits, and otherwise omits the marker
    so the retained diff prefix can still consume the full cap.
    """
    if len(content) <= file_diff_max:
        return content
    if file_diff_max <= 0:
        return ""

    marker = ""
    if len(_FILE_DIFF_TRUNCATION_MARKER) <= file_diff_max:
        marker = _FILE_DIFF_TRUNCATION_MARKER
    elif len(_SHORT_FILE_DIFF_TRUNCATION_MARKER) <= file_diff_max:
        marker = _SHORT_FILE_DIFF_TRUNCATION_MARKER

    cap = max(0, file_diff_max - len(marker))
    return content[:cap] + marker


def _split_diff_by_file(raw_diff: str) -> list[tuple[str, str]]:
    """Split a unified diff into per-file chunks.

    Returns list of (file_path, diff_content) tuples.
    """
    chunks: list[tuple[str, str]] = []
    current_path = ""
    current_lines: list[str] = []

    for line in raw_diff.splitlines(keepends=True):
        if line.startswith("diff --git "):
            if current_path and current_lines:
                chunks.append((current_path, "".join(current_lines)))
            # Extract path from "diff --git a/path b/path"
            parts = line.split(" b/", 1)
            current_path = parts[1].strip() if len(parts) > 1 else ""
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_path and current_lines:
        chunks.append((current_path, "".join(current_lines)))

    return chunks


def fetch_pr_diff(owner: str, repo: str, pr_number: int) -> str:
    """Retrieve the full diff for a PR (legacy single-string interface).

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
        pr_number: The PR number.

    Returns:
        The diff content or a summary for large PRs.
    """
    diffs = fetch_pr_diffs(owner, repo, pr_number)
    return "\n".join(diffs)


def collect_commit_messages(owner: str, repo: str, pr_number: int) -> list[str]:
    """Collect commit messages from a PR.

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
        pr_number: The PR number.

    Returns:
        List of commit message strings.
    """
    try:
        result = subprocess.run(
            [
                "gh",
                "pr",
                "view",
                str(pr_number),
                "--repo",
                f"{owner}/{repo}",
                "--json",
                "commits",
                "--jq",
                ".commits[].messageHeadline",
            ],
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError:
        return []
    if result.returncode != 0:
        return []

    messages = [m for m in result.stdout.strip().split("\n") if m]
    return messages

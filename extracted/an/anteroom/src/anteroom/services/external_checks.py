"""External reality checks for mission items via the ``gh`` CLI (#1306).

Checks whether a GitHub issue is closed and whether merged PRs exist that
close it.  All functions fail closed — subprocess errors, timeouts, and
parse failures return ``False`` / empty results so the caller never
auto-reconciles on bad data.
"""

from __future__ import annotations

import json
import logging
import re
import subprocess
from typing import Any

logger = logging.getLogger(__name__)

_GH_TIMEOUT = 10  # seconds
_REPO_PATTERN = re.compile(r"^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$")

# Cache for the local repo's owner/name (derived once per process).
_cached_repo: tuple[str, str] | None = None


def _resolve_repo(repo: str | None) -> tuple[str, str] | None:
    """Return ``(owner, name)`` for the given *repo* or the local git remote.

    Returns ``None`` on failure so callers can degrade gracefully.
    """
    global _cached_repo  # noqa: PLW0603

    if repo is not None:
        if not _REPO_PATTERN.match(repo):
            logger.warning("Rejected repo string that does not match owner/name pattern: %r", repo)
            return None
        parts = repo.split("/", 1)
        return (parts[0], parts[1])

    if _cached_repo is not None:
        return _cached_repo

    try:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "owner,name"],
            capture_output=True,
            text=True,
            timeout=_GH_TIMEOUT,
        )
        if result.returncode != 0:
            logger.debug("gh repo view failed: %s", result.stderr.strip())
            return None
        data = json.loads(result.stdout)
        owner = data.get("owner", {}).get("login", "")
        name = data.get("name", "")
        if owner and name:
            _cached_repo = (owner, name)
            return _cached_repo
        return None
    except Exception:
        logger.debug("Failed to resolve local repo", exc_info=True)
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def check_issue_closed(issue_number: int, repo: str | None = None) -> bool:
    """Return ``True`` if GitHub issue *issue_number* is in ``CLOSED`` state."""
    cmd = ["gh", "issue", "view", str(issue_number), "--json", "state", "--jq", ".state"]
    if repo is not None:
        if not _REPO_PATTERN.match(repo):
            return False
        cmd.extend(["--repo", repo])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=_GH_TIMEOUT)
        if result.returncode != 0:
            logger.debug("gh issue view failed (rc=%d): %s", result.returncode, result.stderr.strip())
            return False
        return result.stdout.strip().upper() == "CLOSED"
    except Exception:
        logger.debug("check_issue_closed failed for #%d", issue_number, exc_info=True)
        return False


def check_closing_prs(issue_number: int, repo: str | None = None) -> list[int]:
    """Return PR numbers of merged PRs that close issue *issue_number*.

    Uses the GitHub GraphQL ``closedByPullRequestsReferences`` field — the
    canonical truth source for which PRs close an issue.  Returns an empty
    list on any error (fail closed).
    """
    resolved = _resolve_repo(repo)
    if resolved is None:
        return []

    owner, name = resolved
    query = (
        "query($owner: String!, $repo: String!, $number: Int!) {"
        "  repository(owner: $owner, name: $repo) {"
        "    issue(number: $number) {"
        "      closedByPullRequestsReferences(first: 10, userLinkedOnly: false) {"
        "        nodes { number merged }"
        "      }"
        "    }"
        "  }"
        "}"
    )

    cmd = [
        "gh",
        "api",
        "graphql",
        "-f",
        f"owner={owner}",
        "-f",
        f"repo={name}",
        "-F",
        f"number={issue_number}",
        "-f",
        f"query={query}",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=_GH_TIMEOUT)
        if result.returncode != 0:
            logger.debug("gh api graphql failed (rc=%d): %s", result.returncode, result.stderr.strip())
            return []
        data: dict[str, Any] = json.loads(result.stdout)
        nodes = (
            data.get("data", {})
            .get("repository", {})
            .get("issue", {})
            .get("closedByPullRequestsReferences", {})
            .get("nodes", [])
        )
        return [n["number"] for n in nodes[:20] if n.get("merged") is True]
    except Exception:
        logger.debug("check_closing_prs failed for #%d", issue_number, exc_info=True)
        return []


def check_external_completion(issue_number: int, repo: str | None = None) -> tuple[bool, str | None]:
    """Check whether issue *issue_number* was completed externally.

    The **issue-closed** check is the sole decision signal.  The PR lookup
    only enriches the reason string.  If the PR lookup fails but the issue
    is closed, the item is still auto-reconciled with a degraded reason.

    Returns ``(True, reason)`` when the issue is closed, ``(False, None)``
    otherwise.  Fails closed on any error.
    """
    if not check_issue_closed(issue_number, repo):
        return (False, None)

    # Issue is closed — build an evidence-backed reason string.
    closing_prs = check_closing_prs(issue_number, repo)
    if closing_prs:
        pr_list = ", ".join(f"#{n}" for n in closing_prs)
        return (True, f"Issue #{issue_number} closed; merged closing PR(s): {pr_list}")

    return (True, f"Issue #{issue_number} closed externally")

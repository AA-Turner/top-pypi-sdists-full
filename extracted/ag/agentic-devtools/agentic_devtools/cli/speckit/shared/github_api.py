"""Shared GitHub API helpers for speckit nest and retro-spec commands.

Provides thin wrappers over GitHubHierarchyDetector.build_metadata() for
parent/child relationship discovery. Does NOT re-implement REST-first
discovery or GraphQL parent lookup — reuses existing rate-limit tracking,
exponential backoff, and run_safe(..., shell=False) logic in the speckit
hierarchy_detector.
"""

from __future__ import annotations

import re
import sys

from agentic_devtools.hierarchy.github_detector import GitHubHierarchyDetector

# Matches "HTTP 403" as a whole word (avoids matching digits like 1403 or 4030)
_HTTP_403_RE = re.compile(r"\bHTTP 403\b")


def _exit_with_error(message: str) -> None:
    """Print an actionable error message and exit with status 1."""
    print(message, file=sys.stderr)
    sys.exit(1)


def discover_children(owner: str, repo: str, issue_number: int) -> list[int]:
    """Discover child issue numbers for the given issue.

    Delegates to discover_relationships() for consistent error handling across
    403, network, and detector validation failures.

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
        issue_number: The parent issue number.

    Returns:
        List of child issue numbers (in-repo only; cross-repo keys are
        already silently dropped by the underlying detector).

    Raises:
        SystemExit: When the GitHub API returns a 403, is unreachable, or the
            detector raises a user-fixable ValueError.
    """
    _, children = discover_relationships(owner, repo, issue_number)
    return children


def discover_parent(owner: str, repo: str, issue_number: int) -> int | None:
    """Discover the parent issue number for the given issue.

    Delegates to discover_relationships() for consistent error handling across
    403, network, and detector validation failures.

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
        issue_number: The child issue number.

    Returns:
        Parent issue number, or None if no parent relationship exists.

    Raises:
        SystemExit: When the GitHub API returns a 403, is unreachable, or the
            detector raises a user-fixable ValueError.
    """
    parent, _ = discover_relationships(owner, repo, issue_number)
    return parent


def discover_relationships(owner: str, repo: str, issue_number: int) -> tuple[int | None, list[int]]:
    """Discover both parent and children for the given issue in a single API call.

    Avoids duplicate build_hierarchy_tree API calls by making a single
    build_metadata() call and extracting both parent and children.

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
        issue_number: The issue number to query.

    Returns:
        Tuple of (parent_number_or_None, list_of_child_numbers).

    Raises:
        SystemExit: When the GitHub API returns a 403 (suggests required scopes)
            or is unreachable (suggests connectivity check).
    """
    try:
        detector = GitHubHierarchyDetector(owner, repo)
        metadata = detector.build_metadata(issue_number)
    except Exception as exc:
        msg = str(exc)
        if _HTTP_403_RE.search(msg):
            _exit_with_error(
                f"Error: GitHub API returned 403 for issue #{issue_number}. "
                "Ensure your token has the 'repo' scope for private repositories "
                "or 'public_repo' for public repositories."
            )
        if "Could not resolve" in msg or "Network" in msg or "unreachable" in msg:
            _exit_with_error(
                f"Error: Unable to reach GitHub API for issue #{issue_number}. "
                "Check network connectivity and token configuration."
            )
        if isinstance(exc, ValueError):
            # build_metadata raises ValueError subclasses for actionable, user-fixable
            # detector failures (missing gh/auth/404/rate-limit/configuration).
            _exit_with_error(f"Error: Unable to discover hierarchy relationships for issue #{issue_number}: {msg}")
        raise

    parent = metadata.parent
    children: list[int] = []
    seen_children: set[int] = set()

    def _append_if_new(child_number: int) -> None:
        if child_number in seen_children:
            return
        seen_children.add(child_number)
        children.append(child_number)

    for child in metadata.children:
        _append_if_new(child.number)
    for child in metadata.informational_children:
        _append_if_new(child.number)
    return parent, children

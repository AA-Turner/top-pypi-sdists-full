"""Pure-Python branch name construction and issue-key normalization.

This module implements FR-001, FR-002, and FR-009 of the worktree setup feature.
The sanitization algorithm is a pure-Python port of
``.github/scripts/speckit-trigger/sanitize-branch-name.sh`` (the shell script is
the reference specification, not a runtime dependency — see FR-007's no-subprocess
mandate).

The functions here are reusable by both the LangChain nodes and any future caller.
"""

from __future__ import annotations

import re

# Matches a normalized issue key that is safe to embed in a branch name / path:
# either a numeric GitHub issue number or a Jira key.
_ACCEPTED_KEY_PATTERN = re.compile(r"^(?:[0-9]+|[A-Z][A-Z0-9]+-[0-9]+)$", re.IGNORECASE)

# Stop words filtered out of branch descriptions (mirrors the shell reference).
_STOP_WORDS = frozenset(
    {
        "i",
        "a",
        "an",
        "the",
        "to",
        "for",
        "of",
        "in",
        "on",
        "at",
        "by",
        "with",
        "from",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "should",
        "could",
        "can",
        "may",
        "might",
        "must",
        "shall",
        "this",
        "that",
        "these",
        "those",
        "my",
        "your",
        "our",
        "their",
        "want",
        "need",
        "add",
        "get",
        "set",
        "as",
        "so",
    }
)

_MAX_WORDS = 4
_MAX_LENGTH = 50


def normalize_issue_key(issue_key: str) -> str:
    """Normalize an issue key for use in branch names and worktree paths.

    Strips a single leading ``#`` from GitHub numeric keys (``#42`` → ``42``) and
    preserves Jira keys unchanged (``PROJECT-1234`` → ``PROJECT-1234``).

    Args:
        issue_key: Raw issue-key input.

    Returns:
        The normalized issue key.

    Raises:
        ValueError: If ``issue_key`` is empty/whitespace-only, or the normalized
            value is not a valid GitHub issue number or Jira key (e.g. it contains
            ``/``, ``..``, whitespace, or other separators that could corrupt a
            branch name or a filesystem path constructed from the key).
    """
    if not isinstance(issue_key, str):  # defensive: callers may pass corrupted state
        raise ValueError(f"issue_key must be a string, got {type(issue_key).__name__}")

    stripped = issue_key.strip()
    if not stripped:
        raise ValueError("issue_key must not be empty or whitespace-only")

    normalized = stripped.lstrip("#").strip()
    if not normalized:
        raise ValueError("issue_key must not be empty after stripping '#'")

    if not _ACCEPTED_KEY_PATTERN.match(normalized):
        raise ValueError(
            f"issue_key {issue_key!r} does not normalize to a valid GitHub issue "
            f"number or Jira key (got {normalized!r}); values containing '/', '..', "
            f"whitespace, or other separators are rejected to prevent branch-name "
            f"and path corruption"
        )

    return normalized


def sanitize_branch_description(description: str) -> str:
    """Sanitize a free-form description into a branch-safe slug (FR-009).

    Ports the algorithm from ``sanitize-branch-name.sh``:

    1. Lowercase the input.
    2. Replace every non-alphanumeric character (including existing hyphens) with a
       space.
    3. Drop stop words and words shorter than 3 characters.
    4. Take the first 4 remaining meaningful words and join them with hyphens.
    5. Collapse consecutive hyphens, strip leading/trailing hyphens, truncate to 50
       characters.
    6. If no meaningful words remain, fall back to a simple slug of the original
       description (lowercase, non-alphanumeric → hyphen, deduplicated, trimmed,
       truncated to 50 characters).

    Args:
        description: The free-form description (e.g. a GitHub issue title).

    Returns:
        A sanitized branch-description slug. May be an empty string when the input
        has no alphanumeric content at all.
    """
    if not isinstance(description, str):  # defensive against corrupted state
        description = str(description)

    lowered = description.lower()
    # Replace every non-[a-z0-9] character with a space, then split on whitespace.
    spaced = re.sub(r"[^a-z0-9]", " ", lowered)
    words = spaced.split()

    meaningful = [word for word in words if len(word) >= 3 and word not in _STOP_WORDS]

    if meaningful:
        result = "-".join(meaningful[:_MAX_WORDS])
    else:
        # Fallback: slug of the original title.
        result = re.sub(r"[^a-z0-9]", "-", lowered)

    # Collapse consecutive hyphens and strip leading/trailing hyphens.
    result = re.sub(r"-+", "-", result).strip("-")
    # Truncate to max length, then strip a possible trailing hyphen from the cut.
    result = result[:_MAX_LENGTH].rstrip("-")
    return result


def build_branch_name(issue_key: str, description: str, prefix: str = "feature") -> str:
    """Build a ``{prefix}/{normalized-issue-key}/{sanitized-description}`` branch name.

    Args:
        issue_key: Raw issue key (normalized via :func:`normalize_issue_key`).
        description: Free-form branch description (sanitized via
            :func:`sanitize_branch_description`).
        prefix: Branch-type prefix (default ``"feature"``).

    Returns:
        The fully constructed branch name. When the sanitized description is empty,
        a stable ``implementation`` fallback segment is used so the branch always
        has three components.

    Raises:
        ValueError: If ``issue_key`` is invalid (see :func:`normalize_issue_key`).
    """
    normalized_key = normalize_issue_key(issue_key)
    sanitized = sanitize_branch_description(description) or "implementation"
    return f"{prefix}/{normalized_key}/{sanitized}"

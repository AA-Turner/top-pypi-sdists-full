"""Commit message formatting helpers for speckit commands.

Builds Conventional Commits messages with optional Co-authored-by trailer.
The Co-authored-by trailer MUST appear before the mandatory #ISSUE footer
line, and the #ISSUE footer line MUST be the last line of the commit message
(per spec.md clarification and this repository's commit convention).
"""

from __future__ import annotations

_COPILOT_CO_AUTHOR = "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"


def format_commit_message(
    commit_type: str,
    scope: str,
    description: str,
    issue: str | int | None = None,
    co_authored: bool = False,
) -> str:
    """Format a Conventional Commits message with optional Co-authored-by trailer.

    Args:
        commit_type: Commit type (e.g., 'refactor', 'docs').
        scope: Commit scope (e.g., '#1864').
        description: Commit summary description.
        issue: Issue reference for the footer (e.g., '#1864' or 1864). When
            None, no issue footer is appended.
        co_authored: Whether to include the Co-authored-by trailer.

    Returns:
        Formatted commit message string.
    """
    title = f"{commit_type}({scope}): {description}"

    parts: list[str] = [title, ""]
    if co_authored:
        parts.append(_COPILOT_CO_AUTHOR)
    if issue is not None:
        issue_ref = f"#{issue}" if isinstance(issue, int) else issue
        parts.append(issue_ref)

    return "\n".join(parts)

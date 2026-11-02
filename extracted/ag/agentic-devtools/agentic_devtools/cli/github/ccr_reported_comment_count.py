"""Focused helpers for CCR review-body parsing."""

from __future__ import annotations

import agentic_devtools.cli.github.ccr_review_format as _format


def parse_reported_comment_count(body: str) -> int | None:
    """Parse Copilot's self-reported posted-comment count from *body*.

    Matches, in priority order:

    - ``"generated no comments"`` / ``"generated no new comments"`` → ``0``
    - ``"generated N comment(s)"`` → ``N``
    - ``"**Comments generated:** N [new]"`` (new CCR metrics footer) → ``N``

    Args:
        body: Full review body text.

    Returns:
        An integer count, or ``None`` when no recognised count pattern is
        present (callers fail closed on ``None``).
    """
    if not body:
        return None
    if _format._GENERATED_NONE_RE.search(body):
        return 0
    match = _format._GENERATED_N_RE.search(body)
    if match:
        return int(match.group(1))
    match = _format._METRICS_GENERATED_RE.search(body)
    if match:
        return int(match.group(1))
    return None

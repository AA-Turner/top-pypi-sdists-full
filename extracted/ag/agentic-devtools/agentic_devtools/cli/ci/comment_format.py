"""Formatting helpers for AI PR Loop-owned issue comments."""

from __future__ import annotations

AI_PR_LOOP_COMMENT_LABEL = "🤖 AI PR Loop ·"
_LABEL_SUFFIX = f"\n\n{AI_PR_LOOP_COMMENT_LABEL}"
_SINGLE_NEWLINE_LABEL_SUFFIX = f"\n{AI_PR_LOOP_COMMENT_LABEL}"


def format_ai_pr_loop_comment(body: str) -> str:
    """Append the visible terminal label once to a loop-owned comment body."""
    if not isinstance(body, str):
        raise TypeError("AI PR Loop comment body must be a string")
    normalized = normalize_ai_pr_loop_comment(body)
    if normalized is None:
        raise ValueError("AI PR Loop comment has a malformed terminal label")
    if normalized != body:
        return body
    return f"{body}{_LABEL_SUFFIX}"


def normalize_ai_pr_loop_comment(body: str) -> str | None:
    """Remove only the exact terminal label suffix, or reject malformed endings."""
    if not isinstance(body, str):
        return None
    if body.endswith(_LABEL_SUFFIX):
        normalized = body[: -len(_LABEL_SUFFIX)]
        final_line = normalized.splitlines()[-1:]
        if final_line and final_line[0].strip() == AI_PR_LOOP_COMMENT_LABEL:
            return None
        return normalized
    if body.endswith(_SINGLE_NEWLINE_LABEL_SUFFIX):
        return None
    final_line = body.splitlines()[-1:]
    if final_line and final_line[0].strip() == AI_PR_LOOP_COMMENT_LABEL:
        return None
    return body

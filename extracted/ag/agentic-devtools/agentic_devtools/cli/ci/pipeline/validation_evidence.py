"""Pure helpers for validation-evidence gate state and comments."""

import re
from collections.abc import Iterable
from datetime import UTC, datetime
from enum import Enum

from agentic_devtools.cli.ci.models import (
    CLOUD_CODING_AGENT_LOGINS,
    IssueCommentInfo,
    is_copilot_login,
)

EVIDENCE_REQUIRED_LABEL = "ai-validation-evidence-required"
RECOVERY_MARKER = "<!-- agdt:validation-evidence-recovery:v1 -->"
BLOCKER_MARKER = "<!-- agdt:validation-evidence-blocked:v1 -->"
GATE_STATE_KEY = "validation_evidence_gate"
FOLLOWUP_KEY = "validation_evidence_followup"

_EVIDENCE_AUTHORS_CASEFOLDED = frozenset(login.casefold() for login in CLOUD_CODING_AGENT_LOGINS | {"Copilot"})
_FULL_SHA_PATTERN = re.compile(r"[0-9a-fA-F]{40}")
_HEAD_TOKEN_PATTERN = re.compile(r"\b[0-9a-fA-F]{7,40}\b")
_EVIDENCE_HEADING_PATTERN = re.compile(r"^##[ \t]+Validation evidence[ \t]*$", re.IGNORECASE)
_TIMESTAMP_OFFSET_PATTERN = re.compile(r"(?:Z|[+-]\d{2}:?\d{2})$", re.IGNORECASE)


class EvidenceGateState(str, Enum):  # noqa: UP042
    """Possible outcomes for an opt-in validation-evidence gate."""

    NOT_APPLICABLE = "not_applicable"
    SATISFIED = "satisfied"
    MISSING = "missing"
    UNKNOWN = "unknown"


def is_evidence_author(login: object) -> bool:
    """Return whether a login belongs to a Cloud Coding Agent evidence author."""
    return isinstance(login, str) and login.casefold() in _EVIDENCE_AUTHORS_CASEFOLDED


def _advance_backtick_fence(line: str, fence_length: int) -> tuple[int, bool]:
    leading_spaces = len(line) - len(line.lstrip(" "))
    if leading_spaces > 3:
        return fence_length, bool(fence_length)

    stripped_line = line[leading_spaces:].rstrip(" \t")
    if fence_length:
        is_closer = stripped_line.startswith("`") and not stripped_line.strip("`")
        if is_closer and len(stripped_line) >= fence_length:
            return 0, True
        return fence_length, True
    if stripped_line.startswith("```"):
        opening_length = len(stripped_line) - len(stripped_line.lstrip("`"))
        if "`" in stripped_line[opening_length:]:
            return 0, False
        return opening_length, True
    return 0, False


def find_head_evidence(comments: Iterable[IssueCommentInfo], head_sha: str) -> IssueCommentInfo | None:
    """Return the last evidence comment that names the supplied full PR head SHA."""
    if not isinstance(head_sha, str) or _FULL_SHA_PATTERN.fullmatch(head_sha) is None:
        return None

    qualifying_comment = None
    for comment in comments:
        if not is_evidence_author(comment.author):
            continue

        fence_length = 0
        has_heading = False
        for line in comment.body.splitlines():
            fence_length, in_fence = _advance_backtick_fence(line, fence_length)
            if in_fence:
                continue
            stripped_line = line.lstrip()
            if stripped_line.startswith(">"):
                continue
            if _EVIDENCE_HEADING_PATTERN.fullmatch(line):
                has_heading = True
                break

        if has_heading and any(
            head_sha.casefold().startswith(token.casefold()) for token in _HEAD_TOKEN_PATTERN.findall(comment.body)
        ):
            qualifying_comment = comment

    return qualifying_comment


def find_marker_comment(comments: Iterable[IssueCommentInfo], marker: str) -> IssueCommentInfo | None:
    """Return the first eligible comment containing an unquoted marker line."""
    for comment in comments:
        if is_copilot_login(comment.author) or is_evidence_author(comment.author):
            continue

        fence_length = 0
        for line in comment.body.splitlines():
            fence_length, in_fence = _advance_backtick_fence(line, fence_length)
            if in_fence:
                continue
            stripped_line = line.lstrip()
            if stripped_line.startswith(">"):
                continue
            if line.strip() == marker:
                return comment

    return None


def agent_replied_after(comments: Iterable[IssueCommentInfo], anchor: IssueCommentInfo) -> bool:
    """Return whether an evidence author replied after the timezone-aware anchor."""
    anchor_time = anchor.created_at
    if not isinstance(anchor_time, str) or _TIMESTAMP_OFFSET_PATTERN.search(anchor_time) is None:
        return False
    try:
        normalized_anchor = anchor_time[:-1] + "+00:00" if anchor_time[-1:].casefold() == "z" else anchor_time
        parsed_anchor = datetime.fromisoformat(normalized_anchor)
        if parsed_anchor.tzinfo is None or parsed_anchor.utcoffset() is None:
            return False
        anchor_utc = parsed_anchor.astimezone(UTC)
    except OverflowError, ValueError:
        return False

    for comment in comments:
        if not is_evidence_author(comment.author):
            continue
        comment_time = comment.created_at
        if not isinstance(comment_time, str) or _TIMESTAMP_OFFSET_PATTERN.search(comment_time) is None:
            continue
        normalized_comment = comment_time[:-1] + "+00:00" if comment_time[-1:].casefold() == "z" else comment_time
        try:
            parsed_comment = datetime.fromisoformat(normalized_comment)
            if parsed_comment.tzinfo is None or parsed_comment.utcoffset() is None:
                continue
            if parsed_comment.astimezone(UTC) > anchor_utc:
                return True
        except OverflowError, ValueError:
            continue

    return False


def build_recovery_request(head_sha: str) -> str:
    """Build a bounded request for one current-head validation-evidence receipt."""
    return (
        "@copilot\n\n"
        "Please post ONE final PR comment headed `## Validation evidence` naming "
        f"the exact current head SHA `{head_sha}` (or the new head SHA if you push). "
        "Include the actual validation commands you ran, including "
        "`python -m pytest tests/unit/cli/ci/pipeline/validation_evidence` and "
        "`bash scripts/targeted-checks.sh`, the platform, Python version, pytest "
        "version, and the results for each command. Do not make code changes unless "
        "validation fails.\n\n"
        f"{RECOVERY_MARKER}"
    )


def build_blocker_comment(head_sha: str) -> str:
    """Build a human-facing blocker notice when one recovery left evidence missing."""
    return (
        f"Validation evidence is still missing for head `{head_sha}` after one "
        "recovery. The loop will not publish this change. A human can unblock it "
        "by obtaining or verifying an agent-authored `## Validation evidence` "
        "comment for this exact head (from a configured Cloud Coding Agent identity "
        "or `Copilot`), or by removing the "
        f"`{EVIDENCE_REQUIRED_LABEL}` label.\n\n"
        f"{BLOCKER_MARKER}"
    )

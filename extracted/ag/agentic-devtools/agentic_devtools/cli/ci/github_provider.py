"""GitHub Actions CI platform provider.

Implements the ``CIPlatformProvider`` interface for GitHub Actions,
using the ``gh`` CLI for API calls consistent with existing codebase patterns.
"""

from __future__ import annotations

import asyncio
import hashlib
import importlib
import json
import logging
import os
import re
from collections.abc import Iterable, Sequence
from datetime import UTC, datetime
from math import isfinite
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast
from urllib.parse import quote

from agentic_devtools.cli.ci.agent_assignment import AgentAssignmentResult, assign_issue_to_agent
from agentic_devtools.cli.ci.exceptions import MalformedEventError
from agentic_devtools.cli.ci.finalization_state import FinalizedReviewKey, PRCommentFinalizationStateStore
from agentic_devtools.cli.ci.job_logs import UNKNOWN_STEP_SENTINEL
from agentic_devtools.cli.ci.models import (
    COPILOT_COMMENT_LOGINS,
    COPILOT_SESSION_EVENT_STARTED,
    CheckRunStatus,
    CommentResolution,
    EventPayload,
    FailedCheckContext,
    FinalizationResult,
    IssueCommentInfo,
    IssueEvent,
    IssueFacts,
    NoChangePRBrief,
    PRMetadata,
    PRTreeState,
    ReviewCommentDeletionResult,
    ReviewCommentInfo,
    ReviewInfo,
    SquashResult,
    VerificationVerdict,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.reconciliation import config
from agentic_devtools.cli.ci.resolution.engine import TieredResolutionEngine
from agentic_devtools.cli.ci.resolution.github_adapter import (
    GitHubResolutionContext,
    GitHubReviewThread,
    GitHubThreadComment,
)
from agentic_devtools.cli.ci.resolution.models import ResolutionVerdict, ThreadResolutionState, TierResult
from agentic_devtools.cli.ci.resolution.protocols import EvaluationTier, ResolutionContext, ReviewThread
from agentic_devtools.cli.ci.resolution.reply_formatter import ReplyFormatter
from agentic_devtools.cli.ci.resolution.state_persistence import (
    clear_resolution_state,
    increment_iteration,
    is_tentative_expired,
    load_resolution_state,
    mark_abandoned,
    save_resolution_state,
)
from agentic_devtools.cli.ci.resolution.tiers.automation_markers import AutomationMarkerTier
from agentic_devtools.cli.ci.resolution.tiers.outdated import OutdatedTier
from agentic_devtools.cli.ci.resolution.tiers.sdk_evaluation import SdkEvaluationTier
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError, retry_with_backoff
from agentic_devtools.cli.git.commit_template import _derive_issue_link_from_key, resolve_commit_message_from_template
from agentic_devtools.cli.github.ccr_review_format import extract_suppressed_comment_entries, parse_suppressed_count
from agentic_devtools.cli.subprocess_utils import run_safe
from agentic_devtools.config import load_platform_config
from agentic_devtools.state import get_state_dir

logger = logging.getLogger(__name__)


def _decode_observation_watermark(value: str) -> tuple[int, int, str]:
    """Decode the persisted review/comment/commit observation watermark."""
    if not value:
        return 0, 0, ""
    try:
        decoded = json.loads(value)
    except json.JSONDecodeError:
        return 0, 0, value
    if not isinstance(decoded, dict):
        return 0, 0, value
    review = decoded.get("review", 0)
    comment = decoded.get("comment", 0)
    commit = decoded.get("commit", "")
    return (
        review if isinstance(review, int) and review >= 0 else 0,
        comment if isinstance(comment, int) and comment >= 0 else 0,
        commit if isinstance(commit, str) else "",
    )


_NOT_FOUND_RE = re.compile(r"\b(?:HTTP )?404\b|\bnot found\b", re.IGNORECASE)
_COOLDOWN_COMPONENT_RE = re.compile(r"[A-Za-z0-9_.-]{1,128}")

if TYPE_CHECKING:
    from agentic_devtools.cli.audit.models import ClaimResult, ClosedPRInfo
    from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun
    from agentic_devtools.cli.ci.scheduler import DispatchEvent, EligiblePR

_resolve_review_threads_module = importlib.import_module("agentic_devtools.cli.github.resolve_review_threads")
_resolve_review_threads = _resolve_review_threads_module.resolve_review_threads
_unresolve_review_threads = _resolve_review_threads_module.unresolve_review_threads

_ADDRESSED_REPLY_BODY = "Addressed on the updated PR branch."
_LEGACY_ADDRESSED_REPLY_PREFIXES = ("addressed by fix commit",)
_RESOLUTION_TIER_MARKER_PREFIX = "<!-- agdt:resolution-tier:"
_RESOLUTION_TIER_ABANDONED_MARKER = "<!-- agdt:resolution-tier:abandoned -->"
_RESOLUTION_UNCONFIRMED_MARKER = "<!-- agdt:resolution-tier:unconfirmed-commit-change -->"
_RESOLUTION_THREAD_RESOLVED_TEXT = "**thread resolved**"
_RESOLUTION_THREAD_LEFT_OPEN_TEXT = "**thread left open**"
_THREAD_RESOLUTION_STATE_DIRNAME = "thread-resolution"
_SYNTHETIC_THREAD_KEY_PREFIX = "__agdt-thread-"
_REVIEW_THREADS_QUERY = """
query($owner: String!, $repoName: String!, $prNumber: Int!, $threadsCursor: String) {
  repository(owner: $owner, name: $repoName) {
    pullRequest(number: $prNumber) {
      reviewThreads(first: 100, after: $threadsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          startLine
          comments(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes {
              databaseId
              body
              createdAt
              author { login }
              commit { oid }
            }
          }
        }
      }
    }
  }
}
"""

_THREAD_COMMENTS_QUERY = """
query($threadId: ID!, $commentsCursor: String) {
  node(id: $threadId) {
    ... on PullRequestReviewThread {
      comments(first: 100, after: $commentsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          databaseId
          body
          createdAt
          author { login }
          commit { oid }
        }
      }
    }
  }
}
"""

_MARKDOWN_FENCE_LINE_RE = re.compile(r"^(?P<indent>[ \t]{0,3})(?P<fence>`{3,}|~{3,})(?P<rest>.*)$")

# Matches 5xx status codes as whole tokens so that unrelated digits (e.g.
# "1502 rows" or "version 504") are not misclassified as transient HTTP errors.
_TRANSIENT_HTTP_STATUS_RE = re.compile(r"\b(502|503|504)\b")

_BRANCH_TYPE_MAP = {
    "fix": "fix",
    "bugfix": "fix",
    "hotfix": "fix",
    "feat": "feat",
    "feature": "feat",
    "docs": "docs",
    "doc": "docs",
    "refactor": "refactor",
    "perf": "perf",
    "test": "test",
    "tests": "test",
    "build": "build",
    "ci": "ci",
    "chore": "chore",
    "revert": "revert",
    "style": "style",
}


def _require_speckit_pr_token(action: str) -> str:
    """Return SPECKIT_PR_TOKEN or raise a clear configuration error."""
    token = os.environ.get("SPECKIT_PR_TOKEN", "").strip()
    if not token:
        raise RuntimeError(f"SPECKIT_PR_TOKEN is required to {action}.")
    return token


_BRANCH_JIRA_KEY_RE = re.compile(r"^([A-Z][A-Z0-9]+-\d+)(?:$|[-_/])")
_BRANCH_GITHUB_KEY_RE = re.compile(r"^(\d+)(?:$|[-_/])")
_SUBJECT_GITHUB_ISSUE_RE = re.compile(r"#(\d+)\b")
_CONVERSATIONAL_STARTERS = (
    "here ",
    "here's ",
    "i'll ",
    "i've ",
    "i ",
    "sure,",
    "below is",
    "certainly ",
    "the following",
    "this commit",
)
_SDK_CONVENTIONAL_TYPE_PREFIX_RE = re.compile(
    r"^(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(?:\([^)]*\))?(?:!)?:\s+(?P<subject>.+)$",
    flags=re.IGNORECASE,
)
# Supported trailing footer tokens from COMMIT_CONVENTION adapters:
# - GitHub issue refs: #123
# - Jira keys: PROJECT-1234
# - Jira markdown links: [PROJECT-1234](...)
_SDK_ISSUE_REFERENCE_PATTERN = r"(?:#\d+|[A-Z][A-Z0-9]+-\d+|\[[A-Z][A-Z0-9]+-\d+\]\([^)]+\))"
_SDK_FOOTER_LINE_RE = re.compile(
    rf"^(?:{_SDK_ISSUE_REFERENCE_PATTERN})(?:\s*(?:,|/)\s*(?:{_SDK_ISSUE_REFERENCE_PATTERN}))*$"
)
_SDK_BREAKING_CHANGE_FOOTER_RE = re.compile(r"^BREAKING CHANGE:\s+\S.*$", flags=re.IGNORECASE)


def _comment_is_suppressed(comment: dict[str, Any]) -> bool:
    """Return True when API payload indicates the review comment is minimized/suppressed.

    The minimized keys are defensive only. All three call sites
    (:meth:`GitHubActionsProvider.list_review_comments`,
    :meth:`GitHubActionsProvider._fetch_review_comment_by_id`,
    :meth:`GitHubActionsProvider.list_all_review_comments`) pass REST
    ``/pulls/...`` review-comment payloads, and those endpoints never return
    ``is_suppressed`` / ``is_minimized`` / ``minimized`` / ``minimized_reason``:
    minimization is exposed only through GraphQL
    (``PullRequestReviewComment.isMinimized`` / ``minimizedReason``), which no
    query in this module selects. So this helper returns ``False`` for every
    real API comment, and ``is_suppressed=True`` is in practice set only by
    :func:`_parse_suppressed_from_review_body` (negative sentinel IDs).
    """
    return bool(
        comment.get("is_suppressed")
        or comment.get("is_minimized")
        or comment.get("minimized")
        or bool(comment.get("minimized_reason"))
    )


def _parse_optional_positive_int(value: object) -> int | None:
    """Parse a positive integer from an optional API field."""
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


# ---------------------------------------------------------------------------
# Suppressed-comment recovery from Copilot review body
# ---------------------------------------------------------------------------

# --- GraphQL queries for scheduler eligible-PR listing ---

_MAX_PR_PAGES = 20  # Max pagination pages for eligible-PR listings (up to 25 PRs per page × 20 pages = 500 PRs total)
_MAX_DISPATCH_HISTORY_EVENTS = 10  # Max dispatch events to collect from run history
_MAX_DISPATCH_HISTORY_RUNS = 30  # Max candidate runs to inspect (bounds per-run detail API calls)
_PR_NUMBER_FROM_RUN_NAME = re.compile(r"\bPR\s*#(\d+)\b", flags=re.IGNORECASE)


def _parse_inputs_pr_number(inputs: dict | None) -> int:
    """Parse ``pr_number`` from workflow dispatch ``inputs``.

    Mirrors the quote-and-space stripping logic in
    ``_parse_workflow_dispatch_event`` so behaviour is consistent.

    Returns ``0`` when *inputs* is ``None``/empty, the key is absent, or
    the value is not a valid positive integer.
    """
    if not inputs:
        return 0
    pr_number_str = str(inputs.get("pr_number", "") or "")
    pr_number_str = pr_number_str.strip(" ")
    quoted_match = re.fullmatch(r'"([0-9]+)"|\'([0-9]+)\'', pr_number_str)
    if quoted_match:
        pr_number_str = quoted_match.group(1) or quoted_match.group(2)
    if re.fullmatch(r"[0-9]+", pr_number_str):
        pr_number = int(pr_number_str)
        return pr_number if pr_number > 0 else 0
    return 0


_ELIGIBLE_PRS_QUERY = """
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    pullRequests(
      states: OPEN
      first: 25
      orderBy: { field: CREATED_AT, direction: ASC }
    ) {
      nodes {
        number
        createdAt
        isCrossRepository
        headRefName
        headRefOid
        labels(first: 100) {
          nodes { name }
        }
        closingIssuesReferences(first: 100) {
          nodes {
            labels(first: 100) {
              nodes { name }
            }
          }
        }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""

_ELIGIBLE_PRS_QUERY_WITH_CURSOR = """
query($owner: String!, $name: String!, $endCursor: String!) {
  repository(owner: $owner, name: $name) {
    pullRequests(
      states: OPEN
      first: 25
      after: $endCursor
      orderBy: { field: CREATED_AT, direction: ASC }
    ) {
      nodes {
        number
        createdAt
        isCrossRepository
        headRefName
        headRefOid
        labels(first: 100) {
          nodes { name }
        }
        closingIssuesReferences(first: 100) {
          nodes {
            labels(first: 100) {
              nodes { name }
            }
          }
        }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""

_RELEVANT_PRS_QUERY = """
query($owner: String!, $name: String!, $after: String, $first: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequests(states: OPEN, first: $first, after: $after, orderBy: {field: CREATED_AT, direction: ASC}) {
      nodes {
        number
        title
        headRefName
        headRefOid
        baseRefName
        isDraft
        isCrossRepository
        headRepository { nameWithOwner }
        repository { nameWithOwner }
        labels(first: 100) { nodes { name } }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""

_NO_CHANGE_CANDIDATE_PRS_QUERY = """
query($owner: String!, $name: String!, $after: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(
      states: OPEN
      first: 100
      after: $after
      orderBy: { field: CREATED_AT, direction: ASC }
    ) {
      nodes {
        number
        body
        additions
        deletions
        changedFiles
        headRefName
        isCrossRepository
        author {
          __typename
          login
        }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""


def _linked_issue_label_names(pr_node: dict[str, Any]) -> list[str]:
    """Extract label names from a PR node's ``closingIssuesReferences`` payload.

    Args:
        pr_node: A ``pullRequests.nodes`` entry from the eligible-PR GraphQL query.

    Returns:
        Label names found on the PR's linked issues. Returns an empty list when
        the PR has no linked issue or the payload has an unexpected shape.
    """
    references = pr_node.get("closingIssuesReferences")
    if not isinstance(references, dict):
        return []
    issue_nodes = references.get("nodes")
    if not isinstance(issue_nodes, list):
        return []

    names: list[str] = []
    for issue_node in issue_nodes:
        if not isinstance(issue_node, dict):
            continue
        labels = issue_node.get("labels")
        if not isinstance(labels, dict):
            continue
        label_nodes = labels.get("nodes")
        if not isinstance(label_nodes, list):
            continue
        for label_node in label_nodes:
            if not isinstance(label_node, dict):
                continue
            name = label_node.get("name")
            if isinstance(name, str) and name:
                names.append(name)
    return names


def _validated_linked_issue_label_names(pr_node: dict[str, Any], *, pr_number: int) -> list[str]:
    """Extract linked-issue label names and fail closed on malformed GraphQL shapes."""
    references = pr_node.get("closingIssuesReferences")
    if not isinstance(references, dict):
        raise RuntimeError(
            f"PR #{pr_number}: unexpected 'closingIssuesReferences' shape "
            f"({type(references).__name__!r}), expected dict."
        )

    page_info = references.get("pageInfo")
    if not isinstance(page_info, dict):
        raise RuntimeError(
            f"PR #{pr_number}: unexpected 'closingIssuesReferences.pageInfo' shape "
            f"({type(page_info).__name__!r}), expected dict."
        )
    _has_next_page = page_info.get("hasNextPage")
    if not isinstance(_has_next_page, bool):
        raise RuntimeError(
            f"PR #{pr_number}: unexpected 'closingIssuesReferences.pageInfo.hasNextPage' shape "
            f"({type(_has_next_page).__name__!r}), expected bool."
        )
    if _has_next_page:
        raise RuntimeError(
            f"PR #{pr_number} has more than 100 closing issue references; "
            "cannot safely evaluate the one-generation deferral cap."
        )

    issue_nodes = references.get("nodes")
    if not isinstance(issue_nodes, list):
        raise RuntimeError(
            f"PR #{pr_number}: unexpected 'closingIssuesReferences.nodes' shape "
            f"({type(issue_nodes).__name__!r}), expected list."
        )

    names: list[str] = []
    for issue_index, issue_node in enumerate(issue_nodes):
        if not isinstance(issue_node, dict):
            raise RuntimeError(
                f"PR #{pr_number}: unexpected 'closingIssuesReferences.nodes[{issue_index}]' shape "
                f"({type(issue_node).__name__!r}), expected dict."
            )
        labels = issue_node.get("labels")
        if not isinstance(labels, dict):
            raise RuntimeError(
                f"PR #{pr_number}: unexpected 'closingIssuesReferences.nodes[{issue_index}].labels' shape "
                f"({type(labels).__name__!r}), expected dict."
            )
        label_page_info = labels.get("pageInfo")
        if not isinstance(label_page_info, dict):
            raise RuntimeError(
                f"PR #{pr_number}: unexpected 'closingIssuesReferences.nodes[{issue_index}].labels.pageInfo' "
                f"shape ({type(label_page_info).__name__!r}), expected dict."
            )
        _label_has_next = label_page_info.get("hasNextPage")
        if not isinstance(_label_has_next, bool):
            raise RuntimeError(
                f"PR #{pr_number}: unexpected 'closingIssuesReferences.nodes[{issue_index}]"
                f".labels.pageInfo.hasNextPage' shape ({type(_label_has_next).__name__!r}), expected bool."
            )
        if _label_has_next:
            raise RuntimeError(
                f"PR #{pr_number}: linked issue #{issue_index + 1} has more than 100 labels; "
                "cannot safely evaluate the one-generation deferral cap."
            )
        label_nodes = labels.get("nodes")
        if not isinstance(label_nodes, list):
            raise RuntimeError(
                f"PR #{pr_number}: unexpected 'closingIssuesReferences.nodes[{issue_index}].labels.nodes' shape "
                f"({type(label_nodes).__name__!r}), expected list."
            )
        for label_index, label_node in enumerate(label_nodes):
            if not isinstance(label_node, dict):
                raise RuntimeError(
                    "PR "
                    f"#{pr_number}: unexpected 'closingIssuesReferences.nodes[{issue_index}].labels.nodes"
                    f"[{label_index}]' shape ({type(label_node).__name__!r}), expected dict."
                )
            name = label_node.get("name")
            if not isinstance(name, str):
                raise RuntimeError(
                    "PR "
                    f"#{pr_number}: unexpected 'closingIssuesReferences.nodes[{issue_index}].labels.nodes"
                    f"[{label_index}].name' shape ({type(name).__name__!r}), expected str."
                )
            if name:
                names.append(name)
    return names


def _graphql_error_text(message: object) -> str:
    """Return a printable message for one GraphQL error entry.

    GraphQL error objects are untyped external data: ``message`` may be absent,
    ``null``, a number or even a nested object.  Anything that is not a non-empty
    string is rendered defensively so that joining the messages can never raise
    :class:`TypeError` and hide the underlying failure.
    """
    if isinstance(message, str):
        return message if message.strip() else "Unknown GraphQL error"
    if message is None:
        return "Unknown GraphQL error"
    return str(message)


def _raise_for_graphql_errors(
    data: object,
    *,
    context: str,
    provider: str = "github",
    credential_identity: str = "",
    retry_after: float | None = None,
    reset_timestamp: float | None = None,
    remaining: int | None = None,
) -> None:
    """Raise when a parsed GraphQL payload contains an ``errors`` array.

    Transient conditions (``RATE_LIMITED``, internal server error phrases, ``timed out``,
    and similar transient phrases surfaced in the error message) raise :class:`RetryableError` so
    that the surrounding :func:`retry_with_backoff` decorator can retry the call.
    All other GraphQL errors raise :class:`RuntimeError`.

    Rate-limited responses (``RATE_LIMITED`` type or ``"rate limit"`` in the message) are
    raised with ``is_rate_limit=True`` so that the retry decorator can persist a cooldown
    and the pipeline can emit exit code 6 rather than treating the failure as a transient
    server error.

    .. note::
        Raw HTTP status codes such as ``503`` are intentionally *not* matched because
        numeric tokens like ``503`` can appear legitimately in domain error messages
        (e.g. "Could not resolve to an Issue with the number of 503").  Transient
        conditions are detected via the structured ``type`` field (``RATE_LIMITED``) and
        explicit server-error phrases (``"internal server error"``, ``"timed out"``,
        ``"temporarily unavailable"``).
    """
    if not isinstance(data, dict):
        return
    errors = data.get("errors")
    if not isinstance(errors, list) or not errors:
        return
    messages = [_graphql_error_text(error.get("message")) for error in errors if isinstance(error, dict)]
    if not messages:
        messages = ["Unknown GraphQL error"]
    error_str = "; ".join(messages)
    # Mirror the transient-detection logic used by the thread-comment pagination path
    # (github_provider.py ~line 1777) so that RATE_LIMITED and server errors embedded
    # in HTTP-200 GraphQL responses are retried rather than raised as hard failures.
    # Avoid the bare HTTP-status-code regex: a number like 503 can appear legitimately
    # in domain error messages (e.g. "Could not resolve to an Issue with the number of
    # 503"), so matching it as a transient indicator would misclassify permanent errors.
    # Rely on the structured `type` field and explicit server-error phrases instead.
    error_types = {
        error["type"].upper() for error in errors if isinstance(error, dict) and isinstance(error.get("type"), str)
    }
    lower = error_str.lower()
    server_error_indicators = ("internal server error", "timed out", "temporarily unavailable")
    is_rate_limited = "RATE_LIMITED" in error_types or "rate limit" in lower
    is_server_error = any(ind in lower for ind in server_error_indicators)
    if is_rate_limited:
        if retry_after is not None:
            graphql_source = "retry-after"
        elif reset_timestamp is not None:
            graphql_source = "x-ratelimit-reset"
        else:
            graphql_source = "graphql-rate-limited"
        raise RetryableError(
            f"{context}: {error_str}",
            retry_after=retry_after,
            reset_timestamp=reset_timestamp,
            remaining=remaining,
            provider=provider,
            credential_identity=credential_identity,
            source=graphql_source,
            is_rate_limit=True,
        )
    if is_server_error:
        raise RetryableError(
            f"{context}: {error_str}",
            provider=provider,
            credential_identity=credential_identity,
            is_rate_limit=False,
        )
    raise RuntimeError(f"{context}: {error_str}")


# Suppressed-comment recovery from a Copilot review body.
def _parse_suppressed_from_review_body(review_body: str, *, source_review_id: int = 0) -> list[ReviewCommentInfo]:
    """Parse suppressed comments from a Copilot review body.

    Delegates block/entry extraction to the shared CCR parser
    (:func:`agentic_devtools.cli.github.ccr_review_format.extract_suppressed_comment_entries`),
    which understands **both** the legacy ``<details><summary>… suppressed …</summary>``
    format and the new CCR private-preview format (a
    ``### Comments suppressed due to low confidence (N)`` heading inside a
    ``<details><summary>Review details</summary>`` block).  Each recovered
    ``(path, body)`` pair is wrapped as a ``ReviewCommentInfo`` with
    ``is_suppressed=True`` and a unique negative sentinel ID.

    When the body declares a suppressed count that yields no recoverable
    entries, a warning is logged: the gate blocks the merge on the count while
    the repair agent receives nothing to act on, so the mismatch must be visible
    in diagnostics rather than inferred from an empty dispatch comment.

    Args:
        review_body: Full review body text (may contain HTML).
        source_review_id: Review ID that owns ``review_body``.

    Returns:
        List of ``ReviewCommentInfo`` with ``is_suppressed=True`` and negative
        sentinel IDs. Returns empty list if no suppressed block is found.
    """
    entries: list[ReviewCommentInfo] = []
    sentinel_id = -1
    for path, body in extract_suppressed_comment_entries(review_body):
        entries.append(
            ReviewCommentInfo(
                id=sentinel_id,
                path=path,
                body=body,
                html_url="",
                is_suppressed=True,
                source_review_id=source_review_id,
            )
        )
        sentinel_id -= 1

    if not entries:
        declared = parse_suppressed_count(review_body)
        if declared > 0:
            logger.warning(
                "Review body declares %d suppressed comment(s) but no entries could be recovered "
                "from it; the repair dispatch will omit them",
                declared,
            )

    return entries


def _deduplicate_review_comments(
    rest_comments: list[ReviewCommentInfo],
    suppressed_comments: list[ReviewCommentInfo],
) -> list[ReviewCommentInfo]:
    """Merge REST and suppressed comments, removing exact duplicates.

    When a suppressed comment matches a REST comment (after path and body
    normalization), the REST entry is preserved and the suppressed duplicate
    is dropped.

    Args:
        rest_comments: Comments from the REST API (non-suppressed).
        suppressed_comments: Synthetic comments parsed from the review body.

    Returns:
        Merged list: all REST comments followed by non-duplicate suppressed ones.
    """
    if not suppressed_comments:
        return list(rest_comments)

    def _normalize_path(path: str) -> str:
        p = path.strip()
        if p.startswith("/"):
            p = p[1:]
        return p

    def _normalize_body(body: str) -> str:
        return body.replace("\r\n", "\n").strip()

    rest_keys: set[tuple[str, str]] = set()
    for c in rest_comments:
        rest_keys.add((_normalize_path(c.path), _normalize_body(c.body)))

    filtered: list[ReviewCommentInfo] = []
    for c in suppressed_comments:
        key = (_normalize_path(c.path), _normalize_body(c.body))
        if key not in rest_keys:
            filtered.append(c)

    return list(rest_comments) + filtered


def _is_transient_gh_failure(stderr: str) -> bool:
    """Return True when stderr indicates a retryable transient GitHub/CLI failure."""
    stderr_lower = stderr.lower()
    if "rate limit" in stderr_lower or "secondary rate limit" in stderr_lower:
        return True
    return bool(re.search(r"\b(?:http|status(?: code)?)\D*(429|500|502|503|504)\b", stderr_lower))


def _is_rate_limit_gh_failure(stderr: str) -> bool:
    """Return True when stderr specifically indicates a GitHub rate limit."""
    stderr_lower = stderr.lower()
    return "rate limit" in stderr_lower or bool(_GH_RATE_LIMIT_STATUS_RE.search(stderr_lower))


_GH_STATUS_RE = re.compile(r"\b(?:HTTP/\d(?:\.\d)?\s+|HTTP\s+|status(?:\s+code)?\s*[:=]?\s*)(\d{3})\b", re.IGNORECASE)
_GH_RATE_LIMIT_STATUS_RE = re.compile(
    r"\b(?:http(?:/\d(?:\.\d)?)?|status(?:\s+code)?)\s*[:=]?\s*429\b",
    re.IGNORECASE,
)


def _parse_gh_api_output(raw: str) -> tuple[int | None, dict[str, str], str]:
    """Strip ``gh api --include`` headers while retaining the response body."""
    lines = raw.splitlines(keepends=True)
    header_start: int | None = None
    body_start: int | None = None
    status: int | None = None
    parsed_headers: dict[str, str] = {}
    body_chunks: list[str] = []

    def _starts_response_header_block(index: int) -> bool:
        """Recognize a later response only when its headers have a blank terminator."""
        cursor = index + 1
        while cursor < len(lines):
            candidate = lines[cursor]
            if candidate.strip() == "":
                return True
            if re.match(r"^[!-9;-~]+:", candidate.strip()) is None:
                return False
            cursor += 1
        return False

    for index, line in enumerate(lines):
        match = re.match(r"^HTTP/\S+\s+(\d{3})", line.strip(), re.IGNORECASE)
        if match and (header_start is None or _starts_response_header_block(index)):
            if body_start is not None:
                body_chunks.append("".join(lines[body_start:index]))
            header_start = index
            body_start = None
            status = int(match.group(1))
            parsed_headers = {}
            continue
        if header_start is None:
            continue
        if line.strip() == "" and body_start is None:
            body_start = index + 1
            continue
        if body_start is None and ":" in line:
            name, value = line.split(":", 1)
            key = name.strip().lower()
            parsed_headers[key] = f"{parsed_headers[key]},{value.strip()}" if key in parsed_headers else value.strip()
    if header_start is None:
        return None, {}, raw
    if body_start is not None:
        body_chunks.append("".join(lines[body_start:]))
    body = "".join(body_chunks)
    return status, parsed_headers, body


def _parse_rate_limit_headers(headers: dict[str, str]) -> tuple[float | None, float | None, int | None]:
    """Parse rate-limit headers without allowing malformed values to escape."""
    retry_after_values: list[float] = []
    reset_values: list[float] = []
    remaining_values: list[int] = []

    for value in headers.get("retry-after", "").split(","):
        try:
            candidate = float(value.strip())
            if isfinite(candidate) and candidate >= 0:
                retry_after_values.append(candidate)
        except (TypeError, ValueError):
            continue
    for value in headers.get("x-ratelimit-reset", "").split(","):
        try:
            candidate = float(value.strip())
            if isfinite(candidate) and candidate > 0:
                reset_values.append(candidate)
        except (TypeError, ValueError):
            continue
    for value in headers.get("x-ratelimit-remaining", "").split(","):
        try:
            candidate = int(value.strip())
            if candidate >= 0:
                remaining_values.append(candidate)
        except (TypeError, ValueError):
            continue
    retry_after = max(retry_after_values) if retry_after_values else None
    reset = max(reset_values) if reset_values else None
    remaining = min(remaining_values) if remaining_values else None
    return retry_after, reset, remaining


def _credential_identity_for_token(token: str | None) -> str:
    """Return an environment-variable name, never the credential value."""
    configured = os.environ.get("AI_PR_LOOP_CREDENTIAL_IDENTITY", "").strip()
    if token:
        for name in (
            "COPILOT_GITHUB_TOKEN",
            "SPECKIT_PR_TOKEN",
            "AGDT_PR_APPROVER_PAT",
            "REPO_VARIABLE_WRITER_PAT",
            "GH_TOKEN",
        ):
            if os.environ.get(name, "").strip() == token:
                return name
        if configured and _COOLDOWN_COMPONENT_RE.fullmatch(configured):
            return configured
        return "explicit-token"
    if configured and _COOLDOWN_COMPONENT_RE.fullmatch(configured):
        return configured
    if token is None:
        return "GH_TOKEN"
    for name in (
        "COPILOT_GITHUB_TOKEN",
        "SPECKIT_PR_TOKEN",
        "AGDT_PR_APPROVER_PAT",
        "REPO_VARIABLE_WRITER_PAT",
        "GH_TOKEN",
    ):
        if os.environ.get(name, "").strip():
            return name
    return "GH_TOKEN"


def _sanitize_gh_error(text: str) -> str:
    """Keep provider errors useful without exposing credentials or response bodies."""
    sanitized = re.sub(r"(?i)(authorization\s*:\s*bearer\s+|token\s*[=:]\s*)\S+", r"\1[REDACTED]", text)
    sanitized = re.sub(r"(?i)\b(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]+\b", "[REDACTED]", sanitized)
    return sanitized[:512]


def _normalize_bot_login(login: str, is_bot: bool) -> str:
    """Return a bot login in the ``name[bot]`` form the REST API reports.

    ``gh pr list --json author`` reports an app author as ``copilot-swe-agent``
    or ``app/copilot-swe-agent`` depending on the ``gh`` version, while the REST
    API reports ``copilot-swe-agent[bot]``. Normalizing here keeps author
    comparisons in one shape regardless of which listing produced the login.
    """
    normalized = login.removeprefix("app/")
    if is_bot and normalized and not normalized.endswith("[bot]"):
        return f"{normalized}[bot]"
    return normalized


#: Control characters are never valid in repository paths read from an untrusted
#: PR body. Other disallowed forms such as ``:`` / ``?`` and dot-segment
#: traversal are checked separately in :func:`_is_safe_repo_path`. Ordinary
#: filename punctuation is allowed and percent-encoded later by
#: :func:`urllib.parse.quote` before interpolating the path into an API endpoint.
_REPO_PATH_CONTROL_CHARS_RE = re.compile(r"[\x00-\x1f\x7f]")


def _is_safe_repo_path(path: str) -> bool:
    """Return True when *path* is a plain repository-relative file path."""
    if not path or path.startswith(("/", "-")) or path.endswith("/"):
        return False
    if _REPO_PATH_CONTROL_CHARS_RE.search(path):
        return False
    parts = path.split("/")
    return all(part not in {"", ".", ".."} for part in parts)


_OMITTED_LOG_NOTE = "[… condensed output omitted to fit comment size limit …]"
_TRIMMED_CONTENT_NOTE = "[… embedded content trimmed to fit comment size limit …]"
#: Cumulative condensed-log budget for a dispatch that also carries review comments.
#: Kept low so the actionable comment bodies keep their share of the comment.
_MAX_CONDENSED_LOG_BUDGET = 24_000
#: Cumulative condensed-log budget for a CI-only dispatch, where the logs are the
#: only actionable content and can therefore claim more of the comment.
_MAX_CONDENSED_LOG_BUDGET_CI_ONLY = 40_000
_MAX_COMMENT_BODY_CHARS = 60_000
_FENCE_BLOCK_RE = re.compile(r"(`{3,})[^\n]*\n.*?\n\1", re.DOTALL)


def _condensed_log_budget(repair_type: str) -> int:
    """Return the cumulative condensed-log budget for *repair_type*.

    A CI-only dispatch carries no review comments, so its logs may claim a larger
    share of the comment than a ``"both"`` dispatch, where the comment bodies are
    the primary actionable content.
    """
    return _MAX_CONDENSED_LOG_BUDGET_CI_ONLY if repair_type == "ci" else _MAX_CONDENSED_LOG_BUDGET


def _resolve_repair_skills(repair_type: str) -> tuple[str, str]:
    """Return ``(agent_filename, prompt_filename)`` for a repair type.

    Single source of truth for the repair skill filenames embedded in repair
    comments. ``"ci"`` maps to the ci-repair skills; ``"review"`` and ``"both"``
    map to the evaluate-and-respond skills (matching dispatch behaviour).
    """
    if repair_type == "ci":
        return (
            "agdt.address-copilot-review.ci-repair.agent.md",
            "agdt.address-copilot-review.ci-repair.prompt.md",
        )
    return (
        "agdt.address-copilot-review.evaluate-and-respond.agent.md",
        "agdt.address-copilot-review.evaluate-and-respond.prompt.md",
    )


def _read_repo_file(relative_path: str, *, max_bytes: int = 64_000) -> str:
    """Read a repo-root-relative UTF-8 file; return ``""`` on any error.

    The repo root is ``GITHUB_WORKSPACE`` (the GitHub Actions checkout root)
    when set, else the current working directory. Files larger than
    ``max_bytes`` are truncated with a ``[… file truncated …]`` marker.
    """
    try:
        repo_root = os.environ.get("GITHUB_WORKSPACE") or os.getcwd()
        content = (Path(repo_root) / relative_path).read_text(encoding="utf-8")
    except Exception:
        return ""
    encoded = content.encode("utf-8")
    if len(encoded) > max_bytes:
        return encoded[:max_bytes].decode("utf-8", errors="ignore") + "\n[… file truncated …]"
    return content


def _fence(content: str, lang: str = "") -> str:
    """Wrap ``content`` in a code fence that cannot be terminated early.

    Uses one more backtick than the longest backtick run found in ``content``
    (at least three), so embedded fences, ``<details>`` blocks, or ``@mentions``
    can never break the surrounding comment structure.
    """
    longest_run = max((len(match) for match in re.findall(r"`+", content)), default=0)
    ticks = "`" * max(3, longest_run + 1)
    return f"{ticks}{lang}\n{content}\n{ticks}"


#: Sentinel opening the suppressed-comment deferral marker in a deferral issue body.
#: See ``docs/suppressed-comment-triage-contract.md`` — the marker is the **first**
#: line of the body and carries the authoritative ``finding_count``.
SUPPRESSED_DEFERRAL_ISSUE_MARKER = "<!-- ai-pr-loop:suppressed-comment-deferral "


def _render_deferral_issue_body(
    *,
    pr_number: int,
    review_id: int,
    base_sha: str,
    findings: list[tuple[str, str]],
) -> str:
    """Render the deferral issue body consumed by the suppressed-triage agent.

    Implements the input contract in ``docs/suppressed-comment-triage-contract.md``:
    marker first line, then one ``### Finding {i} — `path` `` section per finding in
    review-body order, each body reproduced verbatim inside a dynamically sized
    fence so an embedded fence cannot terminate it early.
    """
    payload = json.dumps(
        {
            "pr": pr_number,
            "review_id": review_id,
            "base_sha": base_sha,
            "finding_count": len(findings),
        }
    )
    lines = [
        f"{SUPPRESSED_DEFERRAL_ISSUE_MARKER}{payload} -->",
        "",
        "## Deferred suppressed findings",
        "",
        f"Source: PR #{pr_number}, Copilot review {review_id}, base commit `{base_sha}`.",
        "",
    ]
    for index, (path, comment_body) in enumerate(findings, start=1):
        lines.append(f"### Finding {index} — `{path}`")
        lines.append("")
        lines.append(_fence(comment_body, "text"))
        lines.append("")
    body = "\n".join(lines).rstrip() + "\n"
    if len(body) > _MAX_COMMENT_BODY_CHARS:
        raise RuntimeError(
            f"Deferral issue body ({len(body)} chars) exceeds GitHub limit "
            f"({_MAX_COMMENT_BODY_CHARS} chars); cannot trim findings verbatim."
        )
    return body


_COMMENT_SECTION_MARKER = "<!-- repair-comment-section -->"
#: A CI failure section is recognised by its own ``### Failure {n} from …`` heading (the
#: heading text is escaped by :func:`_escape_summary_text`, so a check name can never forge
#: one). Unlike the comment sections it needs no hidden marker: the heading is matched on a
#: single line, which keeps a fence whose prefix ends mid-line classifiable.
#:
#: The ``Comment`` alternative deliberately stays **multi-line**: requiring
#: :data:`_COMMENT_SECTION_MARKER` on its own line at column 0, immediately followed by the
#: heading line, is the anti-forgery mechanism — a review-comment body cannot fake a section
#: boundary with a lone ``### Comment 1 - …`` line.
_SECTION_MARKER_RE = re.compile(
    rf"(?m)(?:^[ \t]*###[ \t]+(Failure) \d+ from [^\n]*$|"
    rf"^{re.escape(_COMMENT_SECTION_MARKER)}\n[ \t]*###[ \t]+(Comment) \d+[^\n]*$)"
)


def _section_marker_name(match: re.Match[str]) -> str:
    """Return the semantic section name matched by :data:`_SECTION_MARKER_RE`."""
    return match.group(1) or match.group(2) or ""


def _classify_fence_priority(section: str) -> int:
    """Map the last structural section seen before a fence to a trim priority.

    Lower numbers are trimmed first. The repair comment renders each failing CI check
    (heading ``### Failure {n} from …``) and each review comment (heading
    ``### Comment {n} - …``) as its own top-level block and deliberately preserves the
    actionable comment bodies for as long as possible:

    0. CI condensed logs
    2. Review-comment bodies and any other fenced content
    """
    return 0 if section == "Failure" else 2


def _split_fence_gaps(body: str, spans: Sequence[tuple[int, int]]) -> tuple[str, list[int]]:
    """Return ``(cleaned, cum)`` describing every fence's fence-stripped prefix.

    *spans* must be the complete, in-order ``_FENCE_BLOCK_RE.finditer(body)`` spans
    (including fences the caller will later skip), because a fence's prefix is defined
    with *all* fences stripped.

    ``_FENCE_BLOCK_RE.sub("", body[: spans[i][0]])`` is exactly the concatenation of the
    non-fence gaps preceding fence *i*, so every fence's cleaned prefix is a plain string
    prefix of ``cleaned`` (the concatenation of all gaps) of length ``cum[i]``.
    """
    gaps: list[str] = []
    cum: list[int] = []
    total = 0
    pos = 0
    for start, end in spans:
        gaps.append(body[pos:start])
        total += start - pos
        cum.append(total)
        pos = end
    return "".join(gaps), cum


def _priorities_from_cleaned(cleaned: str, cum: Sequence[int]) -> list[int]:
    """Rank every fence from the fence-stripped prefixes produced by :func:`_split_fence_gaps`.

    Pure function of ``(cleaned, cum)``, which is what makes the trim loop's memoisation
    sound. Scanning ``cleaned`` once yields every structural marker; markers starting
    before a prefix's final line are shared with that prefix, and only that final
    (possibly truncated) line has to be re-tested, because its ``$`` anchor binds to the
    prefix end rather than to the rest of ``cleaned``.
    """
    section_marks = [(m.start(), _section_marker_name(m)) for m in _SECTION_MARKER_RE.finditer(cleaned)]

    priorities: list[int] = []
    section_idx = 0
    section = ""
    for end in cum:
        # Cleaned prefixes grow monotonically, so the marker cursor only moves forward.
        line_start = cleaned.rfind("\n", 0, end) + 1
        while section_idx < len(section_marks) and section_marks[section_idx][0] < line_start:
            section = section_marks[section_idx][1]
            section_idx += 1

        cur_section = section
        partial_line = cleaned[line_start:end]
        if partial_line:
            section_match = _SECTION_MARKER_RE.search(partial_line)
            if section_match is not None:
                cur_section = _section_marker_name(section_match)

        priorities.append(_classify_fence_priority(cur_section))
    return priorities


def _drop_trailing_partial_html_comment(text: str) -> str:
    """Drop a trailing unterminated ``<!--`` (or a partial prefix of one) from *text*.

    A hard character-offset truncation can land inside a structural marker such as
    ``<!-- repair-section:author-comments -->``. The surviving ``<!--`` is never closed,
    so GitHub renders everything after it as comment content — for the repair dispatch
    that can hide whole sections of the instructions. Cutting back to the start of the
    line holding the partial opener loses one already-truncated line and keeps the
    rendered body honest.

    Args:
        text: Body text that may end inside an HTML comment opener.

    Returns:
        *text* unchanged when it holds no unterminated opener, otherwise the text
        truncated at the newline preceding that opener.
    """

    def _inside_markdown_fence(index: int) -> bool:
        active_fence: tuple[str, int] | None = None
        for line in text[:index].splitlines():
            match = _MARKDOWN_FENCE_LINE_RE.match(line)
            if match is None:
                continue
            fence = match.group("fence")
            rest = match.group("rest")
            if active_fence is None:
                if fence.startswith("`") and "`" in rest:
                    continue
                active_fence = (fence[0], len(fence))
                continue
            fence_char, minimum_length = active_fence
            if fence[0] == fence_char and len(fence) >= minimum_length and not rest.strip():
                active_fence = None
        return active_fence is not None

    cut = -1
    opener = text.rfind("<!--")
    while opener != -1:
        if text.find("-->", opener + 4) == -1 and not _inside_markdown_fence(opener):
            cut = opener
            break
        opener = text.rfind("<!--", 0, opener)
    if cut == -1 and text.endswith("<!-"):
        partial = len(text) - 3
        if not _inside_markdown_fence(partial):
            cut = partial
    if cut == -1 and text.endswith("<!"):
        partial = len(text) - 2
        if not _inside_markdown_fence(partial):
            cut = partial
    if cut == -1:
        return text
    newline = text.rfind("\n", 0, cut)
    return text[: newline + 1]


def _enforce_comment_size_limit(body: str, *, hard_limit: int = _MAX_COMMENT_BODY_CHARS) -> str:
    """Trim lower-priority embedded fences until ``body`` fits ``hard_limit``.

    Reference material (CI condensed logs) is removed before actionable
    review-comment bodies, so large comment bodies stay intact whenever earlier
    trimming can bring the comment under GitHub's limit.
    """
    marker_block = _fence(_TRIMMED_CONTENT_NOTE)
    marker_len = len(marker_block)
    cached_cleaned: str | None = None
    cached_cum: list[int] = []
    priorities: list[int] = []
    while len(body) > hard_limit:
        # The priority pass needs every fence, including the ones too small to trim,
        # because a fence's priority is derived from the prefix with *all* fences stripped.
        spans = [m.span() for m in _FENCE_BLOCK_RE.finditer(body)]
        trimmable = [i for i, (start, end) in enumerate(spans) if end - start > marker_len]
        if not trimmable:
            break
        cleaned, cum = _split_fence_gaps(body, spans)
        # Replacing a fence with the (also fenced) marker normally leaves every non-fence
        # gap untouched, so the marker scan is reused whenever its exact inputs repeat.
        if cleaned != cached_cleaned or cum != cached_cum:
            cached_cleaned, cached_cum = cleaned, cum
            priorities = _priorities_from_cleaned(cleaned, cum)
        # Largest fence wins ties within a priority, then the earliest.
        chosen = min(trimmable, key=lambda i: (priorities[i], spans[i][0] - spans[i][1], spans[i][0]))
        start, end = spans[chosen]
        body = body[:start] + marker_block + body[end:]

    if len(body) > hard_limit:
        suffix = "\n" + marker_block
        if body.rstrip().endswith("</details>"):
            suffix += "\n</details>"
        keep = max(0, hard_limit - len(suffix))
        body = _drop_trailing_partial_html_comment(body[:keep]) + suffix
    # Final guarantee: suffix itself may exceed hard_limit for pathologically small limits.
    return body[:hard_limit]


def _escape_summary_text(text: str) -> str:
    """Escape HTML/markdown metacharacters so *text* is safe inside a section heading.

    Angle brackets are escaped so a check name or file path can never inject a nested
    tag, square brackets so the label cannot be parsed as markdown link syntax, and
    newlines so the label can never forge a second structural line that
    :data:`_SECTION_MARKER_RE` would match.
    """
    return (
        text.replace("&", "&amp;")
        .replace("\r", "&#13;")
        .replace("\n", "&#10;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("[", "&#91;")
        .replace("]", "&#93;")
    )


def _escape_comment_metadata_text(text: str) -> str:
    """Escape structural characters so single-line metadata cannot forge comment markers.

    The ``**File:**`` metadata line is rendered outside a fenced code block, so a raw
    path containing newlines or ``<...>`` comment delimiters could otherwise inject
    synthetic section markers into the repair-dispatch body. Preserve printable
    characters verbatim, but render control characters and the structurally
    significant ``<`` / matching ``>`` delimiters with JSON-style escapes that the
    consumer can decode when it needs the literal path.
    """
    escaped: list[str] = []
    for char in text:
        if char == "\\":
            escaped.append("\\\\")
        elif char == "\n":
            escaped.append("\\n")
        elif char == "\r":
            escaped.append("\\r")
        elif char == "\t":
            escaped.append("\\t")
        elif char in "<>" or ord(char) < 0x20 or ord(char) == 0x7F:
            escaped.append(f"\\u{ord(char):04x}")
        else:
            escaped.append(char)
    return "".join(escaped)


def _build_repair_intro_line(*, has_review_context: bool) -> str:
    """Build the first line of a repair dispatch comment when no comment section is emitted.

    The line MUST begin with ``@copilot`` (see :func:`_build_repair_comment`). Only two
    branches survive:

    * a review with no fetched comments — the ask phrased against the review itself
    * no context at all — a bare ``@copilot`` mention

    The comment-count and CI wording that this function used to produce now lives in the
    section lead-ins (:func:`_author_section_lead_in`, :func:`_agent_section_lead_in` and
    :func:`_ci_section_lead_in`), each adjacent to the blocks it introduces.

    Args:
        has_review_context: Whether a concrete review triggered this dispatch.
    """
    if has_review_context:
        return (
            "@copilot - please evaluate the review that was just left by a Code Review Agent "
            "and address any feedback you find to be valid:"
        )
    return "@copilot"


def _partition_review_comments(
    review_comments: list[ReviewCommentInfo],
) -> tuple[list[ReviewCommentInfo], list[ReviewCommentInfo]]:
    """Split *review_comments* into ``(author_comments, agent_comments)``.

    A comment belongs to the author section iff it is **both** suppressed **and**
    carries no ``html_url``. Both conditions are required:

    * ``is_suppressed`` alone is not sufficient — an API-minimised comment is
      suppressed yet still carries a real ``#discussion_r`` anchor, so it stays in
      the Code Review Agent section where its thread can be replied to.
    * ``not html_url`` alone is not sufficient — an unsuppressed comment that happens
      to have an empty URL also stays in the Code Review Agent section.

    Args:
        review_comments: Review comments in dispatch order.

    Returns:
        ``(author_comments, agent_comments)``, each preserving input relative order.
    """
    author_comments = [c for c in review_comments if c.is_suppressed and not c.html_url]
    agent_comments = [c for c in review_comments if not (c.is_suppressed and not c.html_url)]
    return author_comments, agent_comments


def _shared_decision_block() -> list[str]:
    """Return the ``parts`` entries carrying the four-option decision framework.

    The framework is orthogonal to *who* raised a finding — the decision space is
    identical for a PR-author comment and a Code Review Agent comment — so it is
    emitted **once** per dispatch, above every comment section, rather than being
    duplicated per section. Only the reply/record contract stays section-specific
    (:func:`_author_section_lead_in`, :func:`_agent_section_lead_in`).

    Returns:
        ``parts`` entries starting with the block's own leading blank entry.
    """
    return [
        "",
        "## How to decide on each comment",
        "",
        (
            "I don't want you to blindly implement the suggestions. Instead, please evaluate each comment "
            "against the codebase and address it with code changes only if you believe that doing so would "
            "increase the overall quality of the code changes in this PR. It is also possible that a comment "
            "points out a valid problem with the code, but either does not suggest the optimal solution, or "
            "the suggested solution is out of scope for the current PR and the related issue (if there is "
            "one). Therefore, for each comment you have 4 options:"
        ),
        "",
        (
            "1. Accept the comment and implement it as suggested. Where the comment identifies a problem "
            "without proposing a specific fix, implement the fix you judge best."
        ),
        (
            "2. Accept the problem pointed out by the comment, but reject the solution as suboptimal, and "
            "instead implement the optimal solution."
        ),
        (
            "3. Reject that a real problem has been identified by the comment, and assert that the related "
            "code is better left as is."
        ),
        (
            "4. Accept the problem pointed out by the comment, but classify it as out of scope for the "
            "current PR and the related issue (if there is one). In this case a follow-up issue should be "
            "created."
        ),
    ]


def _author_opening_paragraph(count: int) -> str:
    """Return the ``@copilot`` paragraph opening a dispatch that carries author comments.

    Keeps the PR author's first-person voice and its singular/plural forms. Where the
    decisions are to be recorded is stated by :func:`_author_section_lead_in`, under the
    section's own heading.

    Args:
        count: Number of author comments the dispatch carries. Never ``0``.
    """
    tail = (
        "so I would like you to evaluate each comment against the codebase and address it with code changes "
        "only if you believe that doing so would increase the overall quality of the code changes in this PR:"
    )
    if count == 1:
        head = (
            "@copilot - please evaluate the following comment that I had about a certain part of the code "
            "changes in this PR. I am unsure whether a change is needed here or not,"
        )
    else:
        head = (
            f"@copilot - please evaluate the following {count} comments that I had about certain parts of the "
            "code changes in this PR. I am unsure whether changes are needed here or not,"
        )
    return f"{head} {tail}"


def _author_section_lead_in() -> list[str]:
    """Return the ``parts`` entries introducing the PR author's own comments.

    The section is delimited by its hidden marker *and* by a visible heading; the
    heading is authoritative for a reading agent, the marker is a machine-readable
    copy for tooling that reads the comment back through the REST API. The recording
    contract sits immediately under the heading, above the comment blocks it governs.

    The singular/plural comment-count wording lives in
    :func:`_author_opening_paragraph`, which opens the dispatch body.
    """
    return [
        "",
        "<!-- repair-section:author-comments -->",
        "## Comments from the PR author",
        "",
        (
            "These comments have no review thread of their own. Record your decision on each one — the option "
            "you chose and the rationale behind it — in the summary comment you post on the PR when you have "
            "completed your work, so I know what was decided in each case and why."
        ),
    ]


def _author_shortfall_notice(
    *,
    declared: int,
    recovered: int,
    repository_full_name: str,
    pr_number: int,
    review_id: int,
) -> list[str]:
    """Return the ``parts`` entries naming an undelivered-author-comment shortfall.

    The Copilot gate blocks the PR on the count the review *declared*, while this
    dispatch can only render what the parser actually *recovered*. When the two
    disagree the shortfall must be stated in the dispatch body itself, otherwise the
    repair agent sees nothing to act on and the gate keeps blocking forever.

    Args:
        declared: Suppressed-comment count declared by the review body.
        recovered: Number of author comment blocks this dispatch renders.
        repository_full_name: Full repository name (e.g., ``"owner/repo"``).
        pr_number: Pull request number.
        review_id: Review whose body carries the undelivered findings.

    Returns:
        ``parts`` entries starting with the notice's own leading blank entry. The
        recovery command is appended only when the repository, PR number and review
        id needed to build it are all available.
    """
    noun = "finding" if declared == 1 else "findings"
    verb = "was" if declared == 1 else "were"
    notice = f"_{declared} {noun} {verb} declared in the review but {recovered} could be recovered."
    if repository_full_name and "/" in repository_full_name and pr_number and review_id:
        command = f"gh api \"repos/{repository_full_name}/pulls/{pr_number}/reviews/{review_id}\" --jq '.body'"
        notice += f" Fetch the review body for the rest: `{command}`."
    return ["", f"{notice}_"]


def _agent_opening_paragraph(count: int, *, is_first_section: bool) -> str:
    """Return the paragraph naming how many Code Review Agent comments the dispatch carries.

    Args:
        count: Number of Code Review Agent comments. Never ``0``.
        is_first_section: Whether the Code Review Agent section is the first comment
            section in the body. When it is, this paragraph opens the whole body and
            therefore carries the mandatory ``@copilot`` prefix.
    """
    opener = "@copilot - there" if is_first_section else "Additionally, there"
    if count == 1:
        return f"{opener} was a comment left by the Code Review Agent."
    return f"{opener} were {count} comments left by the Code Review Agent."


def _agent_section_lead_in(count: int, *, is_first_section: bool) -> list[str]:
    """Return the ``parts`` entries introducing the Code Review Agent's comments.

    The section is delimited by its hidden marker *and* by a visible heading; the
    heading is authoritative for a reading agent, the marker is a machine-readable
    copy for tooling that reads the comment back through the REST API. The per-thread
    reply contract — the only thing that differs from the author section — sits
    immediately under the heading, above the comment blocks it governs.

    The four-option decision framework is *not* emitted here: it is shared with the
    author section and emitted once by :func:`_shared_decision_block`.

    Args:
        count: Number of Code Review Agent comments that follow. Never ``0``.
        is_first_section: Whether this is the first comment section in the body. When
            it is not, the count paragraph is restated inside the section, because the
            body opened on the author section's paragraph instead.
    """
    closing = (
        "For these comments, please reply to each one with your decision and the rationale behind it. If you "
        "made changes as a result of the comment, link the commit where the changes can be found in the reply. "
        "If you create a follow-up issue (option 4), link the follow-up issue in the reply. If you decided on "
        "option 4 but fail to create the follow-up issue for whatever reason, include everything needed to "
        "create it (title, body, labels, issue type, etc.) in a `<details>` block at the end of your reply to "
        "that comment. After you have replied to each comment, ensure that it is resolved and closed as well, "
        "so that those comments no longer block a merge."
    )
    entries = [
        "",
        "<!-- repair-section:code-review-agent-comments -->",
        "## Comments from the Code Review Agent",
        "",
    ]
    if not is_first_section:
        entries.extend([_agent_opening_paragraph(count, is_first_section=False), ""])
    entries.append(closing)
    return entries


def _ci_section_lead_in(count: int, *, is_first_section: bool) -> list[str]:
    """Return the ``parts`` entries introducing the failing CI checks.

    Args:
        count: Number of failing checks that follow, used to pick the singular/plural
            wording.
        is_first_section: Whether this is the first section in the body. When it is
            not, the lead-in contributes the single blank line that separates it from
            the preceding section. It never appends a trailing blank — the first CI
            failure block supplies that itself.
    """
    noun = "failure" if count == 1 else "failures"
    heading = ["", "## CI failures"]
    if is_first_section:
        return [f"@copilot please fix the following ci {noun}:", *heading]
    return ["", f"Additionally, CI checks are failing — please fix the following ci {noun}:", *heading]


def _render_comment_block(
    *,
    number: int,
    comment: ReviewCommentInfo,
    filename: str,
    fallback_review_id: int,
    emit_source_review_id: bool,
) -> list[str]:
    """Render one review comment as its own top-level heading block.

    The same renderer serves both sections; section membership is supplied by the
    caller through *emit_source_review_id* and is never derived from the comment's
    own fields.

    Args:
        number: Global, monotonic 1-based counter over the emitted order.
        comment: The review comment to render.
        filename: Already-disambiguated label filename (basename, or the full path
            when the basename alone would be ambiguous).
        fallback_review_id: Review ID used for the hidden source-review marker when
            the comment carries none of its own.
        emit_source_review_id: Whether this block belongs to the author section, and
            therefore carries the hidden ``<!-- source-review-id:{id} -->`` marker
            instead of a link to an inline thread. For Code Review Agent blocks that
            lack an ``html_url`` (unsuppressed but unlinked), a
            ``<!-- agent-comment-id:{id} -->`` marker is emitted instead as an
            alternative identifier channel for recovery.

    Returns:
        ``parts`` entries starting with the block's own leading blank entry and
        ending on the comment body fence.
    """
    label = f"Comment {number} - {_escape_summary_text(filename)}"
    if comment.line is not None:
        label += f":{comment.line}"

    block = ["", _COMMENT_SECTION_MARKER, f"### {label}"]
    source_review_id = comment.source_review_id or fallback_review_id
    if emit_source_review_id and source_review_id:
        block.append(f"<!-- source-review-id:{source_review_id} -->")
    elif not emit_source_review_id and not comment.html_url and comment.id:
        block.append(f"<!-- agent-comment-id:{comment.id} -->")
    block.append("")
    if comment.html_url:
        block.append(f"**Link to original comment:** {comment.html_url}")
    escaped_path = _escape_comment_metadata_text(comment.path)
    path_ticks = "`" * max(1, max((len(m) for m in re.findall(r"`+", escaped_path)), default=0) + 1)
    block.append(f"**File:** {path_ticks}{escaped_path}{path_ticks}")
    if comment.line is not None:
        start = comment.start_line if comment.start_line is not None else comment.line
        range_ = f"{start}" if start == comment.line else f"{start}–{comment.line}"
        block.append(f"**Lines:** {range_}")
    block.extend(["", "Comment:", _fence(comment.body)])
    return block


def _build_repair_comment(
    *,
    head_sha: str,
    repair_type: str,
    failed_checks: list[CheckRunStatus],
    review_comments: list[ReviewCommentInfo],
    repository_full_name: str = "",
    pr_number: int = 0,
    review_id: int = 0,
    check_contexts: dict[int, FailedCheckContext] | None = None,
    declared_author_comment_count: int = 0,
    declared_author_comment_counts_by_review: dict[int, int] | None = None,
) -> str:
    """Build the @copilot-tagged comment body for repair dispatch.

    The comment MUST begin with ``@copilot`` for reliable AI agent session
    triggering. This is a hard requirement — comments that tag @copilot
    but don't begin with @copilot have been observed to trigger agent
    sessions unreliably.

    The layout leads with an opening ``@copilot`` paragraph, followed — whenever at
    least one comment section is emitted — by a single shared four-option decision
    framework that governs both sections. The actionable feedback is then partitioned
    into up to two comment sections — the PR author's own comments first, the Code
    Review Agent's comments second — each introduced by a hidden section marker, a
    visible section heading and the section's own reply/record contract. Every review
    comment is rendered as its own ``### Comment {n} - …`` block (file, line range and
    full body), numbered globally and monotonically across both sections. A Code Review
    Agent block opens with a link to the original inline comment, placed above
    ``**File:**``; an author block carries no link at all because it has no inline
    thread of its own. A ``## CI failures`` section with one ``### Failure {n} from
    {check}`` block per failing check (condensed job logs and a link to the failing job)
    follows. The ``## Instructions`` block names the agent skill, points at the
    prompt file as the authoritative dispatch-format contract and the originating
    review thread comes last.

    Nothing is rendered inside a ``<details>`` block: collapsed content has been
    observed not to reach the cloud coding agent at all.

    Args:
        head_sha: Current HEAD SHA for context.
        repair_type: ``"review"``, ``"ci"``, or ``"both"``.
        failed_checks: List of failed check runs (for CI repair context).
        review_comments: Rich review comment metadata (for review repair context).
        repository_full_name: Full repository name (e.g., ``"owner/repo"``).
        pr_number: Pull request number (for building review and comment URLs).
        review_id: ID of the Copilot review that triggered this dispatch.
            Used for the dedup marker and review URL.
        check_contexts: Mapping of ``check.id`` to its :class:`FailedCheckContext`
            (full display name and per-failing-step condensed logs). A check's
            condensed output is embedded only when present with non-empty logs.
        declared_author_comment_count: Suppressed-comment count the review body
            *declared*. When it exceeds the number of author comments actually
            recovered, a one-line notice naming the shortfall (and the fetch that
            recovers the rest) is emitted inside the author section — which is then
            emitted even when nothing was recovered at all. Defaults to ``0``, which
            can never exceed the recovered count and so never emits the notice.
        declared_author_comment_counts_by_review: Optional per-review declared
            suppressed-comment counts. When present, each review whose declared count
            exceeds its recovered author comments emits its own shortfall notice and
            recovery fetch.

    Returns:
        Comment body string beginning with ``@copilot``.
    """
    has_review = repair_type in ("review", "both")
    has_review_comments = has_review and bool(review_comments)
    has_ci = repair_type in ("ci", "both") and bool(failed_checks)
    check_contexts = check_contexts or {}
    has_explicit_declared_author_comment_counts_by_review = declared_author_comment_counts_by_review is not None
    declared_author_comment_counts_by_review = {
        source_review_id: declared
        for source_review_id, declared in (declared_author_comment_counts_by_review or {}).items()
        if declared > 0
    }
    total_declared_author_comment_count = (
        sum(declared_author_comment_counts_by_review.values())
        if has_explicit_declared_author_comment_counts_by_review
        else declared_author_comment_count
    )

    def _review_url_for(source_review_id: int) -> str:
        if has_review and source_review_id and repository_full_name and "/" in repository_full_name and pr_number:
            return f"https://github.com/{repository_full_name}/pull/{pr_number}#pullrequestreview-{source_review_id}"
        return ""

    review_url = _review_url_for(review_id)

    has_review_context = has_review and bool(review_id)

    # --- Fallback for empty context ---
    if (
        not review_comments
        and not failed_checks
        and not has_review_context
        and total_declared_author_comment_count == 0
    ):
        return "\n".join(
            [
                _build_repair_intro_line(has_review_context=has_review_context),
                "",
                f"Please review the PR and fix any issues found. Current HEAD: `{head_sha[:8]}`.",
                "",
                "---",
                f"*Automated repair dispatch for commit `{head_sha[:8]}` (type: {repair_type})*",
            ]
        )

    # --- Resolve skill filenames (single source of truth) ---
    agent_skill, prompt_skill = _resolve_repair_skills(repair_type)
    if repository_full_name and "/" in repository_full_name:
        # Pin the skill links to the PR's HEAD (matching dispatch_conflict_repair) so that a PR
        # that changes either skill file links to the current version, not the stale main copy.
        skill_ref = head_sha or "main"
        agent_url = f"https://github.com/{repository_full_name}/blob/{skill_ref}/.github/agents/{agent_skill}"
        prompt_url = f"https://github.com/{repository_full_name}/blob/{skill_ref}/.github/prompts/{prompt_skill}"
        agent_link = f"[`.github/agents/{agent_skill}`]({agent_url})"
        prompt_link = f"[`.github/prompts/{prompt_skill}`]({prompt_url})"
    else:
        agent_link = f"`.github/agents/{agent_skill}`"
        prompt_link = f"`.github/prompts/{prompt_skill}`"

    # --- Partition the comments into the author and Code Review Agent sections ---
    author_comments, agent_comments = _partition_review_comments(review_comments) if has_review_comments else ([], [])

    # The basename map stays global over the full list so a name that is ambiguous
    # across sections still renders with its full path in both.
    basename_paths: dict[str, set[str]] = {}
    for comment in review_comments:
        basename = comment.path.rsplit("/", 1)[-1] if "/" in comment.path else comment.path
        basename_paths.setdefault(basename, set()).add(comment.path)

    def _label_filename(comment: ReviewCommentInfo) -> str:
        basename = comment.path.rsplit("/", 1)[-1] if "/" in comment.path else comment.path
        # Fall back to the full path when the basename alone would be ambiguous.
        return comment.path if len(basename_paths.get(basename, set())) > 1 else basename

    number = 1
    is_first = True
    parts: list[str] = []

    # --- Author comments (the PR author's own feedback — no inline threads) ---
    recovered_author_comment_counts_by_review: dict[int, int] = {}
    for comment in author_comments:
        source_review_id = comment.source_review_id or review_id
        recovered_author_comment_counts_by_review[source_review_id] = (
            recovered_author_comment_counts_by_review.get(source_review_id, 0) + 1
        )
    author_shortfalls = (
        [
            (
                source_review_id,
                declared,
                recovered_author_comment_counts_by_review.get(source_review_id, 0),
            )
            for source_review_id, declared in declared_author_comment_counts_by_review.items()
            if declared > recovered_author_comment_counts_by_review.get(source_review_id, 0)
        ]
        if has_explicit_declared_author_comment_counts_by_review
        else (
            [(review_id, declared_author_comment_count, len(author_comments))]
            if declared_author_comment_count > len(author_comments)
            else []
        )
    )
    author_shortfall = bool(author_shortfalls)
    has_author_section = bool(author_comments or author_shortfall)

    # --- Opening paragraph + the decision framework shared by both comment sections ---
    if has_author_section or agent_comments:
        if has_author_section:
            lead_in_count = len(author_comments) if author_comments else total_declared_author_comment_count
            parts.append(_author_opening_paragraph(lead_in_count))
        else:
            parts.append(_agent_opening_paragraph(len(agent_comments), is_first_section=True))
        parts.extend(_shared_decision_block())
        is_first = False

    if has_author_section:
        parts.extend(_author_section_lead_in())
        for source_review_id, declared, recovered in author_shortfalls:
            parts.extend(
                _author_shortfall_notice(
                    declared=declared,
                    recovered=recovered,
                    repository_full_name=repository_full_name,
                    pr_number=pr_number,
                    review_id=source_review_id,
                )
            )
        for comment in author_comments:
            parts.extend(
                _render_comment_block(
                    number=number,
                    comment=comment,
                    filename=_label_filename(comment),
                    fallback_review_id=review_id,
                    emit_source_review_id=True,
                )
            )
            number += 1

    # --- Code Review Agent comments (each has its own inline thread) ---
    if agent_comments:
        parts.extend(_agent_section_lead_in(len(agent_comments), is_first_section=not has_author_section))
        for comment in agent_comments:
            parts.extend(
                _render_comment_block(
                    number=number,
                    comment=comment,
                    filename=_label_filename(comment),
                    fallback_review_id=review_id,
                    emit_source_review_id=False,
                )
            )
            number += 1

    # --- First line: the review ask, only when no comment section was emitted ---
    # This must be resolved before the CI section so that a "both" dispatch whose
    # comment list came back empty still leads with the review ask.
    if is_first and (has_review_context or not has_ci):
        parts.insert(0, _build_repair_intro_line(has_review_context=has_review_context))
        is_first = False

    # --- One heading block per failing check (actionable content) ---
    if has_ci:
        parts.extend(_ci_section_lead_in(len(failed_checks), is_first_section=is_first))
        log_budget = _condensed_log_budget(repair_type)

        cumulative_log_chars = 0
        budget_exhausted = False
        for nf, check in enumerate(failed_checks, 1):
            ctx = check_contexts.get(check.id)
            raw_name = ctx.display_name if ctx and ctx.display_name else check.name
            name = _escape_summary_text(raw_name)
            rendered_logs: list[str] = []
            omitted_logs = False
            for step in ctx.step_logs if ctx else ():
                log_text = step.condensed_log
                if not log_text:
                    continue
                if budget_exhausted or cumulative_log_chars + len(log_text) > log_budget:
                    budget_exhausted = True
                    omitted_logs = True
                    continue
                cumulative_log_chars += len(log_text)
                if step.step_name and step.step_name != UNKNOWN_STEP_SENTINEL:
                    safe_step = step.step_name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    rendered_logs.append(f"**Failing step:** {safe_step}")
                    rendered_logs.append("")
                rendered_logs.append(_fence(log_text))
                rendered_logs.append("")

            parts.append("")
            parts.append(f"### Failure {nf} from {name}")
            parts.append("")
            parts.append(f"**Conclusion:** `{check.conclusion}`")
            parts.append("")
            parts.extend(rendered_logs)
            if omitted_logs:
                parts.append(_OMITTED_LOG_NOTE)
                parts.append("")
            if check.html_url:
                parts.append(f"**Link to failing ci job that the preceding logs were pulled from:** {check.html_url}")
                parts.append("")
            # The next block supplies its own leading blank, so no block ends on one.
            while parts[-1] == "":
                parts.pop()

    # --- Instructions block (prompt link only — it carries the authoritative format contract) ---
    parts.append("")
    parts.append("## Instructions")
    parts.append("")
    parts.append(f"You are the {agent_link} agent.")
    parts.append(f"The authoritative dispatch-format instructions for this run are in {prompt_link}.")
    parts.append("Read and follow both referenced files before beginning your work.")

    # --- Original Code Review Thread block ---
    if review_url:
        parts.append("")
        parts.append("## Original Code Review Thread")
        parts.append("")
        parts.append(f"This comment was triggered by this [Review]({review_url}) thread.")

    body = "\n".join(parts)

    # --- Dedup marker (appended at the very end) ---
    # The marker is placed at the very end of the body so that when a cloud
    # agent quotes only the top of this comment in its completion reply, the
    # quote truncation can never split the HTML comment and leave an
    # unterminated "<!--" that swallows the rest of the reply. Dedup detection
    # (is_duplicate_trigger / find_comment) matches the marker anywhere in the
    # body via substring/regex, so end placement does not affect deduplication.
    if has_review and review_id:
        now_iso = datetime.now(UTC).isoformat()
        marker = f"<!-- copilot-trigger:{review_id}:{now_iso} -->"
        # Reserve room for the marker (plus the "\n\n" separator) so size
        # enforcement can never truncate it away — the marker must always
        # survive for deduplication to work.
        reserved = len(marker) + 2
        body = _enforce_comment_size_limit(body, hard_limit=max(0, _MAX_COMMENT_BODY_CHARS - reserved))
        return f"{body}\n\n{marker}"

    return _enforce_comment_size_limit(body)


def _gh_api(
    endpoint: str,
    *,
    method: str = "GET",
    body: dict | None = None,
    paginate: bool = False,
    include_headers: bool = True,
    token: str | None = None,
    headers: dict[str, str] | None = None,
    credential_identity: str | None = None,
    response_metadata: dict[str, float | int | None] | None = None,
) -> str:
    """Call the GitHub API via the ``gh`` CLI.

    Args:
        endpoint: API endpoint path (e.g., "/repos/{owner}/{repo}/pulls/1").
        method: HTTP method.
        body: JSON body for POST/PATCH/PUT requests.
        paginate: Whether to use --paginate for list endpoints.
        include_headers: Whether to request and parse ``gh api --include`` headers.
        token: Optional token to use instead of the default ``GH_TOKEN``.
            When provided, the subprocess environment is overridden so that
            ``gh`` authenticates with this token.
        headers: Optional HTTP headers passed via repeated ``-H`` args.
        credential_identity: Optional logical environment-variable name for
            cooldown scoping; token contents are never recorded.

    Returns:
        Raw response body as string.

    Raises:
        RetryableError: On rate limit (HTTP 403/429) or transient failure.
        RuntimeError: On non-retryable API errors.
    """
    cmd = ["gh", "api", endpoint, "--method", method]
    if include_headers:
        cmd.append("--include")
    if paginate:
        cmd.append("--paginate")
    if body is not None:
        cmd.extend(["--input", "-"])
    if headers:
        for key, value in headers.items():
            cmd.extend(["-H", f"{key}: {value}"])

    env: dict[str, str] | None = None
    if token:
        env = {**os.environ, "GH_TOKEN": token}

    result = run_safe(
        cmd,
        capture_output=True,
        text=True,
        shell=False,
        input=json.dumps(body) if body else None,
        env=env,
    )

    if include_headers:
        status, response_headers, response_body = _parse_gh_api_output(result.stdout or "")
    else:
        status, response_headers, response_body = None, {}, result.stdout or ""
    stderr = result.stderr.strip()
    stderr_status_match = _GH_STATUS_RE.search(stderr)
    if status is None and stderr_status_match:
        status = int(stderr_status_match.group(1))
    retry_after, reset_timestamp, remaining = _parse_rate_limit_headers(response_headers)
    stderr_lower = stderr.lower()
    rate_indicator = "rate limit" in stderr_lower or "secondary rate limit" in stderr_lower
    has_rate_headers = retry_after is not None or remaining == 0
    is_rate_limit = (
        rate_indicator or status == 429 or (status == 403 and has_rate_headers) or (status is None and has_rate_headers)
    )
    identity = credential_identity or _credential_identity_for_token(token)
    if result.returncode != 0:
        if is_rate_limit:
            raise RetryableError(
                f"GitHub API rate limited (HTTP {status or 429})",
                retry_after=retry_after,
                reset_timestamp=reset_timestamp,
                remaining=remaining,
                provider="github",
                credential_identity=identity,
                source=(
                    "retry-after"
                    if retry_after is not None
                    else "x-ratelimit-reset"
                    if reset_timestamp is not None
                    else "fallback"
                ),
                is_rate_limit=True,
            )
        transient_status = status
        if transient_status is None:
            bare_status_match = re.search(r"(?<![/\w])(500|502|503|504)\b", stderr)
            if bare_status_match:
                transient_status = int(bare_status_match.group(1))
        if transient_status in {500, 502, 503, 504}:
            raise RetryableError(
                f"GitHub API server error (HTTP {transient_status})",
                provider="github",
                credential_identity=identity,
                is_rate_limit=False,
            )
        raise RuntimeError(
            f"GitHub API error: {_sanitize_gh_error(stderr) if stderr else f'exit code {result.returncode}'}"
        )

    if response_metadata is not None:
        response_metadata.update(
            retry_after=retry_after,
            reset_timestamp=reset_timestamp,
            remaining=remaining,
        )
    return response_body


# Matches any https:// URL of the form <host>/<owner>/<repo>/pull/<number>.
# Intentionally not anchored to github.com so GHES custom hostnames are supported.
_EXISTING_PR_URL_RE = re.compile(r"https://[^/\s]+/[^/\s]+/[^/\s]+/pull/\d+")


def _extract_existing_pr_url(text: str) -> str:
    """Extract an existing PR URL from a ``gh pr create`` failure message.

    ``gh pr create`` exits non-zero when an open PR already exists for the
    current branch, printing a message that includes the existing PR URL, e.g.::

        a pull request for branch "X" into branch "Y" already exists:
        https://github.com/owner/repo/pull/123

    Only an "already exists" message is treated as reuse (``gh`` prints this
    solely for an *open* PR), so a genuinely failed creation still returns "".

    Args:
        text: Combined stderr/stdout text from the failed ``gh pr create``.

    Returns:
        The existing open PR URL, or "" when the text is not an "already exists" message.
    """
    if "already exists" not in text.lower():
        return ""
    match = _EXISTING_PR_URL_RE.search(text)
    return match.group(0) if match else ""


def _parse_paginated_json(raw: str) -> Any:
    """Parse potentially concatenated JSON from ``gh api --paginate``.

    ``gh api --paginate`` may emit multiple JSON documents (one per page)
    for non-array endpoints. This handles both single documents and
    concatenated documents by attempting incremental parsing.

    Returns:
        Merged result — arrays are concatenated; objects with array
        values have those arrays merged across pages.
    """
    raw = raw.strip()
    if not raw:
        return []

    # Try single document first (most common case / single page)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Parse concatenated JSON documents
    decoder = json.JSONDecoder()
    results: list[Any] = []
    idx = 0
    while idx < len(raw):
        while idx < len(raw) and raw[idx] in " \t\n\r":
            idx += 1
        if idx >= len(raw):  # pragma: no cover — strip() above removes trailing ws
            break
        try:
            obj, end_idx = decoder.raw_decode(raw, idx)
        except json.JSONDecodeError as exc:
            snippet = raw[idx : idx + 80]
            raise json.JSONDecodeError(
                f"Failed to parse concatenated JSON at index {idx} (snippet: {snippet!r}): {exc.msg}",
                raw,
                idx,
            ) from exc
        results.append(obj)
        idx = end_idx

    if not results:  # pragma: no cover — non-empty stripped input always yields results or raises
        return []

    # If all pages are arrays, concatenate them
    if isinstance(results[0], list):
        merged: list[Any] = []
        for r in results:
            if isinstance(r, list):
                merged.extend(r)
            else:  # pragma: no cover
                pass
        return merged

    # For objects (e.g., check_runs wrapped response), merge array values.
    # Note: For non-list keys, only the first page's value is preserved.
    # If a later page has a different scalar value for the same key, a warning
    # is logged since this indicates an unexpected response shape.
    if isinstance(results[0], dict):
        merged_dict: dict[str, Any] = {}
        for r in results:
            if not isinstance(r, dict):
                continue
            for key, value in r.items():
                if key not in merged_dict:
                    merged_dict[key] = value
                elif isinstance(value, list) and isinstance(merged_dict[key], list):
                    merged_dict[key].extend(value)
                elif not isinstance(value, list) and merged_dict[key] != value:
                    logger.warning(
                        "_parse_paginated_json: scalar key %r differs across pages "
                        "(first=%r, later=%r); keeping first page value",
                        key,
                        merged_dict[key],
                        value,
                    )
        return merged_dict

    return results


class GitHubActionsProvider(CIPlatformProvider):
    """GitHub Actions implementation of the CI platform provider.

    Uses the ``gh`` CLI for all API interactions, with retry logic
    for transient failures and rate limiting.
    """

    provider_name = "github"

    def __init__(self, repo: str = "") -> None:
        """Initialize the GitHub Actions provider.

        Args:
            repo: Repository in "owner/repo" format. If empty, uses the
                current repository context from ``gh``.
        """
        self._repo = repo
        self._thread_signals_cache: dict[int, dict[int, tuple[bool, bool, bool | None, str, str | None]]] = {}
        self._thread_identity_cache: dict[int, dict[str, tuple[bool, tuple[int, ...]]]] = {}
        self._approver_login_cache: str | None = None
        self._pr_token_login_cache: str | None = None

    def delete_review_comments(
        self,
        pr_number: int,
        *,
        execute: bool = False,
        author_substring: str | None = None,
    ) -> ReviewCommentDeletionResult:
        """Stub: bulk deletion of agdt-review scaffolding comments is Azure DevOps-only.

        The ``agdt-review`` thread-scaffolding workflow that this command cleans up
        is an Azure DevOps review-tooling concept; GitHub PR review comments are
        managed through the GitHub resolution engine instead.

        Raises:
            NotImplementedError: Always — run ``agdt-delete-pr-review-comments``
                against an Azure DevOps repository, or implement this method on
                ``GitHubActionsProvider``.
        """
        raise NotImplementedError(
            "GitHubActionsProvider.delete_review_comments() is not implemented: "
            "agdt-review scaffolding comment threads are an Azure DevOps review-tooling "
            "concept. Run agdt-delete-pr-review-comments against an Azure DevOps repository, "
            "or implement delete_review_comments on GitHubActionsProvider."
        )

    def _repo_api(self, path: str) -> str:
        """Build a repository-scoped API path.

        Falls back to the ``GITHUB_REPOSITORY`` environment variable when no
        explicit repo was passed to the constructor, mirroring
        :meth:`_resolve_repo`. This ensures REST calls are correctly scoped to
        ``/repos/{owner}/{repo}`` in the GitHub Actions runner context, where the
        provider is often constructed without an explicit repo (e.g. the
        round-robin scheduler). Without this fallback the path is emitted without
        the ``/repos/{owner}/{repo}`` prefix and every call returns HTTP 404.
        """
        repo = self._repo or os.environ.get("GITHUB_REPOSITORY", "")
        if repo:
            return f"/repos/{repo}{path}"
        return path

    def parse_event(self, raw_payload: dict, event_name: str) -> EventPayload:
        """Parse a GitHub Actions event payload."""
        try:
            if event_name in ("pull_request", "pull_request_target"):
                return self._parse_pull_request_event(raw_payload)
            if event_name == "pull_request_review":
                return self._parse_pull_request_review_event(raw_payload, event_name)
            if event_name == "issue_comment":
                return self._parse_issue_comment_event(raw_payload, event_name)
            if event_name == "issues":
                return self._parse_issues_event(raw_payload)
            if event_name == "workflow_run":
                return self._parse_workflow_run_event(raw_payload, event_name)
            if event_name == "workflow_dispatch":
                return self._parse_workflow_dispatch_event(raw_payload)
        except (KeyError, TypeError) as exc:
            raise MalformedEventError(event_name, str(exc)) from exc

        raise MalformedEventError(event_name, f"unsupported event type: {event_name}")

    def _parse_pull_request_event(self, raw: dict) -> EventPayload:
        pr = raw["pull_request"]
        action = raw.get("action", "")

        # Detect edit-change metadata for edited events
        title_changed = False
        body_changed = False
        base_changed = False
        edit_changes_known = False
        changes = raw.get("changes")
        if action == "edited" and isinstance(changes, dict):
            edit_changes_known = True
            title_changed = "title" in changes
            body_changed = "body" in changes
            base_changed = "base" in changes

        return EventPayload(
            pr_number=pr["number"],
            head_branch=pr["head"]["ref"],
            head_sha=pr["head"]["sha"],
            base_branch=pr["base"]["ref"],
            action=action,
            repository_full_name=raw.get("repository", {}).get("full_name", ""),
            sender_login=raw.get("sender", {}).get("login", ""),
            title_changed=title_changed,
            body_changed=body_changed,
            base_changed=base_changed,
            edit_changes_known=edit_changes_known,
        )

    def _parse_pull_request_review_event(self, raw: dict, event_name: str) -> EventPayload:
        pr = raw.get("pull_request")
        if pr is None:
            raise MalformedEventError(event_name, "missing 'pull_request' field")
        return EventPayload(
            pr_number=pr["number"],
            head_branch=pr["head"]["ref"],
            head_sha=pr["head"]["sha"],
            base_branch=pr["base"]["ref"],
            action=raw.get("action", ""),
            repository_full_name=raw.get("repository", {}).get("full_name", ""),
            sender_login=raw.get("sender", {}).get("login", ""),
        )

    def _parse_issues_event(self, raw: dict) -> EventPayload:
        label = raw.get("label", {})
        return EventPayload(
            action=raw.get("action", ""),
            trigger_label=label.get("name", ""),
            repository_full_name=raw.get("repository", {}).get("full_name", ""),
            sender_login=raw.get("sender", {}).get("login", ""),
        )

    def _parse_issue_comment_event(self, raw: dict, event_name: str) -> EventPayload:
        issue = raw.get("issue")
        if issue is None:
            raise MalformedEventError(event_name, "missing 'issue' field")
        if issue.get("pull_request") is None:
            raise MalformedEventError(event_name, "issue_comment is not on a pull request")
        issue_number = issue.get("number")
        if not isinstance(issue_number, int) or issue_number <= 0:
            raise MalformedEventError(event_name, "missing or invalid 'issue.number' field")
        commenter_login = raw.get("comment", {}).get("user", {}).get("login", "")
        return EventPayload(
            pr_number=issue_number,
            action="comment_created",
            repository_full_name=raw.get("repository", {}).get("full_name", ""),
            sender_login=commenter_login or raw.get("sender", {}).get("login", ""),
        )

    def _parse_workflow_run_event(self, raw: dict, event_name: str) -> EventPayload:
        wf = raw.get("workflow_run")
        if wf is None:
            raise MalformedEventError(event_name, "missing 'workflow_run' field")

        # Try to extract PR info from the workflow run
        pr_number = 0
        base_branch = ""
        prs = wf.get("pull_requests", [])
        if prs:
            pr_number = prs[0].get("number", 0)
            base_branch = prs[0].get("base", {}).get("ref", "")

        return EventPayload(
            pr_number=pr_number,
            head_branch=wf.get("head_branch", ""),
            head_sha=wf.get("head_sha", ""),
            base_branch=base_branch,
            action=raw.get("action", ""),
            repository_full_name=raw.get("repository", {}).get("full_name", ""),
            sender_login=raw.get("sender", {}).get("login", ""),
        )

    def _parse_workflow_dispatch_event(self, raw: dict) -> EventPayload:
        """Parse a workflow_dispatch event, extracting pr_number from inputs.

        Treats the dispatch as equivalent to a ``workflow_run`` completion event
        (action="completed") so the orchestrator routes it to the squash-wait path.
        """
        inputs = raw.get("inputs") or {}
        pr_number_str = str(inputs.get("pr_number", "") or "")
        pr_number_str = pr_number_str.strip(" ")
        quoted_pr_number_match = re.fullmatch(r'"([0-9]+)"|\'([0-9]+)\'', pr_number_str)
        if quoted_pr_number_match:
            pr_number_str = quoted_pr_number_match.group(1) or quoted_pr_number_match.group(2)
        if re.fullmatch(r"[0-9]+", pr_number_str):
            pr_number = int(pr_number_str)
        else:
            pr_number = 0
        return EventPayload(
            pr_number=pr_number,
            action="completed",
            repository_full_name=raw.get("repository", {}).get("full_name", ""),
            sender_login=raw.get("sender", {}).get("login", ""),
        )

    @retry_with_backoff()
    def get_pr_metadata(self, pr_number: int) -> PRMetadata:
        """Retrieve PR metadata via gh CLI."""
        response = _gh_api(self._repo_api(f"/pulls/{pr_number}"))
        data = json.loads(response)
        return PRMetadata(
            number=data["number"],
            title=data["title"],
            head_branch=data["head"]["ref"],
            head_sha=data["head"]["sha"],
            base_branch=data["base"]["ref"],
            head_repo_full_name=data.get("head", {}).get("repo", {}).get("full_name", ""),
            base_repo_full_name=data.get("base", {}).get("repo", {}).get("full_name", ""),
            labels=[lbl["name"] for lbl in data.get("labels", [])],
            requested_reviewers=[reviewer["login"] for reviewer in data.get("requested_reviewers", [])],
            is_draft=data.get("draft", False),
            mergeable=data.get("mergeable"),
            mergeable_state=data.get("mergeable_state", ""),
        )

    @retry_with_backoff()
    def list_relevant_pull_requests(
        self,
        *,
        cursor: str | None = None,
        limit: int = 25,
    ) -> tuple[list[PRMetadata], str | None]:
        """List a cursor-paginated page of open pull-request metadata."""
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
            raise ValueError("limit must be an integer between 1 and 100")
        if cursor is not None and not isinstance(cursor, str):
            raise ValueError("cursor must be a string or None")

        repo = self._resolve_repo()
        owner, repo_name = repo.split("/", 1)
        from agentic_devtools.cli.ci.scheduler import SKIP_LABEL

        response = _gh_api(
            "/graphql",
            method="POST",
            body={
                "query": _RELEVANT_PRS_QUERY,
                "variables": {
                    "owner": owner,
                    "name": repo_name,
                    "after": cursor,
                    "first": limit,
                },
            },
        )
        data = json.loads(response)
        if not isinstance(data, dict):
            raise RuntimeError(
                f"Malformed relevant pull-request inventory response: expected object, got {type(data).__name__}"
            )
        errors = data.get("errors")
        if isinstance(errors, list) and errors:
            messages = [error.get("message", "Unknown GraphQL error") for error in errors if isinstance(error, dict)]
            raise RuntimeError(
                "Relevant pull-request inventory query failed: " + "; ".join(messages or ["unknown error"])
            )
        response_data = data.get("data")
        repository = response_data.get("repository") if isinstance(response_data, dict) else None
        pull_requests = repository.get("pullRequests") if isinstance(repository, dict) else None
        if not isinstance(pull_requests, dict):
            raise RuntimeError("Malformed relevant pull-request inventory response")
        nodes = pull_requests.get("nodes")
        page_info = pull_requests.get("pageInfo")
        if not isinstance(nodes, list) or not isinstance(page_info, dict):
            raise RuntimeError("Malformed relevant pull-request inventory response")

        metadata: list[PRMetadata] = []
        for node in nodes:
            if not isinstance(node, dict):
                raise RuntimeError("Malformed relevant pull-request inventory node")
            if node.get("isCrossRepository") is True:
                continue
            number = node.get("number")
            title = node.get("title")
            head_ref = node.get("headRefName")
            head_sha = node.get("headRefOid")
            base_ref = node.get("baseRefName")
            if (
                not isinstance(number, int)
                or number <= 0
                or not isinstance(title, str)
                or not isinstance(head_ref, str)
                or not isinstance(head_sha, str)
                or not isinstance(base_ref, str)
            ):
                raise RuntimeError("Malformed relevant pull-request inventory node")
            labels_container = node.get("labels")
            labels_payload = labels_container.get("nodes", []) if isinstance(labels_container, dict) else []
            labels = (
                [
                    label["name"]
                    for label in labels_payload
                    if isinstance(label, dict) and isinstance(label.get("name"), str)
                ]
                if isinstance(labels_payload, list)
                else []
            )
            if SKIP_LABEL in labels:
                continue
            head_repository = node.get("headRepository")
            base_repository = node.get("repository")
            metadata.append(
                PRMetadata(
                    number=number,
                    title=title,
                    head_branch=head_ref,
                    head_sha=head_sha,
                    base_branch=base_ref,
                    head_repo_full_name=head_repository.get("nameWithOwner", "")
                    if isinstance(head_repository, dict) and isinstance(head_repository.get("nameWithOwner"), str)
                    else "",
                    base_repo_full_name=base_repository.get("nameWithOwner", "")
                    if isinstance(base_repository, dict) and isinstance(base_repository.get("nameWithOwner"), str)
                    else "",
                    labels=labels,
                    is_draft=node.get("isDraft", False) if isinstance(node.get("isDraft"), bool) else False,
                )
            )

        has_next = page_info.get("hasNextPage")
        next_cursor = page_info.get("endCursor")
        if not isinstance(has_next, bool) or (has_next and not isinstance(next_cursor, str)):
            raise RuntimeError("Malformed relevant pull-request inventory page info")
        return metadata, next_cursor if has_next else None

    def get_pr_copilot_attribution(self, pr_number: int, *, observation_watermark: str = "") -> dict[str, bool | str]:
        """Identify Copilot-authored reviews/comments and pushes since a watermark."""
        if not isinstance(pr_number, int) or isinstance(pr_number, bool) or pr_number <= 0:
            raise ValueError("pr_number must be a positive integer")
        review_watermark, comment_watermark, commit_watermark = _decode_observation_watermark(observation_watermark)
        reviews = self.list_reviews(pr_number)
        comments = self.list_issue_comments(pr_number)
        new_reviews = [review for review in reviews if review.id > review_watermark]
        new_comments = [comment for comment in comments if comment.id > comment_watermark]
        has_review = any(review.user in COPILOT_COMMENT_LOGINS for review in new_reviews)
        has_review = has_review or any(comment.author in COPILOT_COMMENT_LOGINS for comment in new_comments)
        metadata = self.get_pr_metadata(pr_number)
        if commit_watermark:
            from agentic_devtools.cli.ci.push_attribution import list_commits_since_watermark

            per_page = 100
            scan_state: dict[str, bool] = {}
            commits = list_commits_since_watermark(
                self._repo or os.environ.get("GITHUB_REPOSITORY", ""),
                commit_watermark,
                pr_number=pr_number,
                per_page=per_page,
                max_pages=config.MAX_PAGINATION_PAGES_PER_RUN,
                scan_state=scan_state,
            )
            watermark_scan_incomplete = bool(commit_watermark) and not scan_state.get("watermark_found", False)
            has_push = any(
                isinstance(commit, dict)
                and any(
                    isinstance(commit.get(actor), dict) and commit[actor].get("login") in COPILOT_COMMENT_LOGINS
                    for actor in ("author", "committer")
                )
                for commit in commits
            )
            if watermark_scan_incomplete:
                logger.warning(
                    "Commit watermark %r was not found; treating push attribution as unknown", commit_watermark
                )
                has_push = True
        else:
            head_author = self.get_commit_author_login(metadata.head_sha) if metadata.head_sha else ""
            has_push = head_author in COPILOT_COMMENT_LOGINS
        return {
            "review": has_review,
            "push": has_push,
            "observation_watermark": json.dumps(
                {
                    "commit": metadata.head_sha,
                    "review": max((review.id for review in reviews), default=review_watermark),
                    "comment": max((comment.id for comment in comments), default=comment_watermark),
                },
                separators=(",", ":"),
            ),
        }

    @retry_with_backoff()
    def get_commit_author_login(self, sha: str) -> str:
        """Return the GitHub login for the commit associated with ``sha``.

        Prefers ``author.login`` and falls back to ``committer.login``.
        Returns an empty string when neither can be resolved to a GitHub user.
        """
        response = _gh_api(self._repo_api(f"/commits/{sha}"))
        data = json.loads(response)

        for key in ("author", "committer"):
            actor = data.get(key)
            if isinstance(actor, dict):
                login = actor.get("login")
                if isinstance(login, str) and login:
                    return login
        return ""

    @retry_with_backoff()
    def list_check_runs(self, head_sha: str) -> list[CheckRunStatus]:
        """List check runs for a commit SHA."""
        response = _gh_api(self._repo_api(f"/commits/{head_sha}/check-runs"), paginate=True)
        data = _parse_paginated_json(response)
        return [
            CheckRunStatus(
                id=cr["id"],
                name=cr["name"],
                status=cr["status"],
                conclusion=cr.get("conclusion") or "",
                html_url=cr.get("html_url") or "",
            )
            for cr in data.get("check_runs", [])
        ]

    @retry_with_backoff()
    def list_reviews(self, pr_number: int) -> list[ReviewInfo]:
        """List reviews for a pull request."""
        response = _gh_api(self._repo_api(f"/pulls/{pr_number}/reviews"), paginate=True)
        reviews = _parse_paginated_json(response)
        return [
            ReviewInfo(
                id=r["id"],
                user=r["user"]["login"],
                state=r["state"],
                body=r.get("body") or "",
                commit_sha=r.get("commit_id") or "",
                submitted_at=r.get("submitted_at") or "",
            )
            for r in reviews
        ]

    @retry_with_backoff()
    def post_comment(self, pr_number: int, body: str) -> int:
        """Post a comment on a PR issue."""
        response = _gh_api(
            self._repo_api(f"/issues/{pr_number}/comments"),
            method="POST",
            body={"body": body},
        )
        data = json.loads(response)
        return data["id"]

    @retry_with_backoff()
    def post_comment_as_pr_token(self, pr_number: int, body: str) -> int:
        """Post a PR comment authenticated with ``SPECKIT_PR_TOKEN``."""
        token = _require_speckit_pr_token("post PR comments")
        response = _gh_api(
            self._repo_api(f"/issues/{pr_number}/comments"),
            method="POST",
            body={"body": body},
            token=token,
        )
        data = json.loads(response)
        return data["id"]

    @retry_with_backoff()
    def update_comment(self, comment_id: int, body: str) -> None:
        """Update an existing comment."""
        _gh_api(
            self._repo_api(f"/issues/comments/{comment_id}"),
            method="PATCH",
            body={"body": body},
        )

    @retry_with_backoff()
    def find_comment(self, pr_number: int, marker: str) -> tuple[int, str] | None:
        """Find the newest comment (by id) containing a marker string."""
        response = _gh_api(self._repo_api(f"/issues/{pr_number}/comments"), paginate=True)
        comments = _parse_paginated_json(response)
        matching = [c for c in comments if marker in c.get("body", "")]
        if not matching:
            return None
        newest = max(matching, key=lambda c: c["id"])
        return (newest["id"], newest["body"])

    @retry_with_backoff()
    def list_issue_comments(self, issue_or_pr_number: int) -> list[IssueCommentInfo]:
        """List issue/PR conversation comments ordered by API response order."""
        response = _gh_api(self._repo_api(f"/issues/{issue_or_pr_number}/comments"), paginate=True)
        comments = _parse_paginated_json(response)
        return [
            IssueCommentInfo(
                id=int(comment.get("id", 0)),
                author=(comment.get("user") or {}).get("login", ""),
                body=comment.get("body", "") or "",
                created_at=comment.get("created_at", "") or "",
            )
            for comment in comments
            if comment.get("id")
        ]

    def list_review_thread_states(self, pr_number: int) -> dict[int, tuple[bool, bool]]:
        """Return review comment -> (is_resolved, has_reply) mapping via GraphQL threads."""
        signals = self._fetch_thread_signals_by_comment_id(pr_number)
        return {
            comment_id: (is_resolved, has_reply)
            for comment_id, (
                is_resolved,
                has_reply,
                _is_outdated,
                _latest_body,
                _latest_author_login,
            ) in signals.items()
        }

    def list_review_threads_by_thread_id(self, pr_number: int) -> dict[str, tuple[bool, tuple[int, ...]]]:
        """Return review thread id -> (is_resolved, comment databaseIds) for a pull request.

        Companion to :meth:`list_review_thread_states`, which is keyed by review
        *comment* id and therefore cannot distinguish one thread carrying three
        comments from three single-comment threads. Callers that need to count or
        reason about threads themselves should use this method instead.

        Both methods are served by the same cached GraphQL fetch
        (``_fetch_thread_signals_by_comment_id``), so calling this method costs no
        additional round-trip when thread signals were already loaded for the PR.

        This method is intentionally not part of the ``CIPlatformProvider``
        abstract surface: callers must duck-type it via ``getattr`` and degrade
        gracefully when a provider does not expose it.

        Args:
            pr_number: Pull request number.

        Returns:
            Mapping of thread key to ``(is_resolved, comment_ids)``. The key is the
            thread's GraphQL node id; threads whose node id is missing or not a
            non-empty string fall back to a synthetic positional key so that every
            thread is still represented exactly once. ``comment_ids`` contains the
            thread's review comment ``databaseId`` values in API order, omitting
            comments whose ``databaseId`` is absent or not an integer.
        """
        self._fetch_thread_signals_by_comment_id(pr_number)
        return dict(self._thread_identity_cache.get(pr_number) or {})

    def _collect_thread_comments(self, thread: dict[str, Any]) -> list[dict[str, Any]]:
        """Return every comment node of a review thread, following inner pagination.

        The ``reviewThreads`` query only returns the first 100 comments per thread.
        When more exist, the remaining pages are fetched via ``_THREAD_COMMENTS_QUERY``
        so that reply detection and latest-comment projections see the whole thread.

        Args:
            thread: A ``reviewThreads`` node with ``id`` and a ``comments`` connection.

        Returns:
            Comment nodes of the thread in API order.  This is a best-effort
            result: when pagination metadata is malformed (``hasNextPage=true``
            but no ``endCursor``) or the thread has no node id, a warning is
            logged and a truncated prefix is returned rather than raising, so
            callers should not assume the list is complete in those cases.
        """
        comments_data = thread.get("comments") or {}
        comment_nodes: list[dict[str, Any]] = list(comments_data.get("nodes") or [])
        page_info = comments_data.get("pageInfo")
        if not isinstance(page_info, dict):
            page_info = {}
        has_next_page = page_info.get("hasNextPage") is True
        cursor = page_info.get("endCursor") if has_next_page else None
        if has_next_page and not cursor:
            logger.warning(
                "Review thread comments pageInfo has hasNextPage=true but no endCursor; "
                "comment list is truncated and thread signals may be incomplete."
            )
            return comment_nodes
        if not cursor:
            return comment_nodes

        thread_id = thread.get("id")
        if not isinstance(thread_id, str) or not thread_id:
            logger.warning(
                "Review thread has more than %d comments but no node id; "
                "comment list is truncated and thread signals may be incomplete.",
                len(comment_nodes),
            )
            return comment_nodes

        while cursor:
            next_comments = self._fetch_thread_comment_page(thread_id, cursor)
            comment_nodes.extend(next_comments.get("nodes") or [])
            next_page_info = next_comments.get("pageInfo") or {}
            next_has_next_page = next_page_info.get("hasNextPage") is True
            cursor = next_page_info.get("endCursor") if next_has_next_page else None
            if next_has_next_page and not cursor:
                logger.warning(
                    "Review thread comments continuation pageInfo has hasNextPage=true but no endCursor; "
                    "comment list is truncated and thread signals may be incomplete."
                )
                break

        return comment_nodes

    @retry_with_backoff()
    def _fetch_thread_comment_page(self, thread_id: str, cursor: str) -> dict[str, Any]:
        """Fetch one page of comments for a review thread and validate the response.

        Args:
            thread_id: GraphQL node id of the review thread.
            cursor: Pagination cursor for the comments connection.

        Returns:
            The ``comments`` connection dict (with ``nodes`` and ``pageInfo``).

        Raises:
            RuntimeError: When the GraphQL response contains errors or an unexpected shape.
        """
        response_metadata: dict[str, float | int | None] = {}
        response = _gh_api(
            "graphql",
            method="POST",
            body={
                "query": _THREAD_COMMENTS_QUERY,
                "variables": {"threadId": thread_id, "commentsCursor": cursor},
            },
            response_metadata=response_metadata,
        )
        data = json.loads(response)
        _raise_for_graphql_errors(
            data,
            context="Thread comment pagination GraphQL error",
            provider="github",
            credential_identity=_credential_identity_for_token(None),
            retry_after=cast(float | None, response_metadata.get("retry_after")),
            reset_timestamp=cast(float | None, response_metadata.get("reset_timestamp")),
            remaining=cast(int | None, response_metadata.get("remaining")),
        )
        node = (data.get("data") or {}).get("node")
        if not isinstance(node, dict):
            raise RuntimeError(
                f"Thread comment pagination returned unexpected node shape for thread {thread_id!r}: "
                f"expected a dict, got {type(node).__name__}"
            )
        comments = node.get("comments")
        if not isinstance(comments, dict):
            raise RuntimeError(
                f"Thread comment pagination returned unexpected comments shape for thread {thread_id!r}: "
                f"expected a dict, got {type(comments).__name__}"
            )
        return comments

    @retry_with_backoff()
    def _fetch_thread_signals_by_comment_id(
        self, pr_number: int
    ) -> dict[int, tuple[bool, bool, bool | None, str, str | None]]:
        """Return thread-level signals keyed by review comment databaseId.

        Threads with more than 100 comments are paginated so that every comment
        is represented in the mapping (see ``_collect_thread_comments``).

        Maps each review comment ID to:
        - thread isResolved status
        - whether thread has replies
        - thread isOutdated status
        - latest thread comment body (used by automation-marker tier)
        - latest thread comment author login (used by SWE-agent-reply tier)

        As a side effect, the thread-keyed projection consumed by
        ``list_review_threads_by_thread_id`` is cached from the same response.
        """
        cached = self._thread_signals_cache.get(pr_number)
        if cached is not None:
            return cached

        owner, repo_name = self._resolve_repo().split("/", maxsplit=1)
        cursor: str | None = None
        result: dict[int, tuple[bool, bool, bool | None, str, str | None]] = {}
        threads_by_id: dict[str, tuple[bool, tuple[int, ...]]] = {}
        thread_index = 0

        while True:
            variables: dict[str, Any] = {
                "owner": owner,
                "repoName": repo_name,
                "prNumber": pr_number,
            }
            if cursor is not None:
                variables["threadsCursor"] = cursor
            response_metadata: dict[str, float | int | None] = {}
            response = _gh_api(
                "graphql",
                method="POST",
                body={"query": _REVIEW_THREADS_QUERY, "variables": variables},
                response_metadata=response_metadata,
            )
            data = json.loads(response)
            _raise_for_graphql_errors(
                data,
                context="Review thread signals GraphQL error",
                provider="github",
                credential_identity=_credential_identity_for_token(None),
                retry_after=cast(float | None, response_metadata.get("retry_after")),
                reset_timestamp=cast(float | None, response_metadata.get("reset_timestamp")),
                remaining=cast(int | None, response_metadata.get("remaining")),
            )
            repository = (data.get("data") or {}).get("repository")
            if not isinstance(repository, dict):
                raise RuntimeError("Review thread signals GraphQL error: missing data.repository")
            pull_request = repository.get("pullRequest")
            if not isinstance(pull_request, dict):
                raise RuntimeError("Review thread signals GraphQL error: missing data.repository.pullRequest")
            thread_data = pull_request.get("reviewThreads")
            if not isinstance(thread_data, dict):
                raise RuntimeError(
                    "Review thread signals GraphQL error: missing data.repository.pullRequest.reviewThreads"
                )
            for thread in thread_data.get("nodes", []):
                is_resolved = bool(thread.get("isResolved", False))
                is_outdated: bool | None = thread.get("isOutdated")
                comment_nodes = self._collect_thread_comments(thread)
                has_reply = len(comment_nodes) > 1
                latest_comment_body = ""
                latest_comment_author_login: str | None = None
                if comment_nodes:
                    latest_comment_body = str(comment_nodes[-1].get("body") or "")
                    latest_comment_author_login = ((comment_nodes[-1].get("author") or {}).get("login")) or None
                comment_ids: list[int] = []
                for node in comment_nodes:
                    comment_id = node.get("databaseId")
                    if isinstance(comment_id, int):
                        comment_ids.append(comment_id)
                        result[comment_id] = (
                            is_resolved,
                            has_reply,
                            is_outdated,
                            latest_comment_body,
                            latest_comment_author_login,
                        )
                thread_id = thread.get("id")
                thread_key = (
                    thread_id
                    if isinstance(thread_id, str) and thread_id
                    else f"{_SYNTHETIC_THREAD_KEY_PREFIX}{thread_index}"
                )
                threads_by_id[thread_key] = (is_resolved, tuple(comment_ids))
                thread_index += 1

            page_info = thread_data.get("pageInfo", {})
            if page_info.get("hasNextPage") is True and page_info.get("endCursor"):
                cursor = page_info["endCursor"]
            else:
                break

        self._thread_signals_cache[pr_number] = result
        self._thread_identity_cache[pr_number] = threads_by_id
        return result

    @retry_with_backoff()
    def _fetch_outdated_by_comment_id(self, pr_number: int) -> dict[int, bool | None]:
        """Return isOutdated status per comment databaseId via GraphQL thread query."""
        signals = self._fetch_thread_signals_by_comment_id(pr_number)
        return {
            comment_id: is_outdated
            for comment_id, (
                _is_resolved,
                _has_reply,
                is_outdated,
                _latest_body,
                _latest_author_login,
            ) in signals.items()
        }

    @retry_with_backoff()
    def _fetch_latest_thread_comment_body_by_comment_id(self, pr_number: int) -> dict[int, str]:
        """Return the latest thread comment body per review comment databaseId."""
        signals = self._fetch_thread_signals_by_comment_id(pr_number)
        return {
            comment_id: latest_body
            for comment_id, (
                _is_resolved,
                _has_reply,
                _is_outdated,
                latest_body,
                _latest_author_login,
            ) in signals.items()
        }

    @retry_with_backoff()
    def _fetch_latest_thread_comment_author_login_by_comment_id(self, pr_number: int) -> dict[int, str | None]:
        """Return the latest thread comment author login per review comment databaseId."""
        signals = self._fetch_thread_signals_by_comment_id(pr_number)
        return {
            comment_id: latest_author_login
            for comment_id, (
                _is_resolved,
                _has_reply,
                _is_outdated,
                _latest_body,
                latest_author_login,
            ) in signals.items()
        }

    @retry_with_backoff()
    def count_unresolved_review_threads(self, pr_number: int) -> int:
        """Count unresolved review comment threads on a pull request.

        Reuses the existing thread signals query and counts threads whose
        isResolved status is False. Each unique thread is counted once
        regardless of how many comments it contains.
        """
        owner, repo_name = self._resolve_repo().split("/", maxsplit=1)
        cursor: str | None = None
        unresolved = 0

        while True:
            variables: dict[str, Any] = {
                "owner": owner,
                "repoName": repo_name,
                "prNumber": pr_number,
            }
            if cursor is not None:
                variables["threadsCursor"] = cursor
            response_metadata: dict[str, float | int | None] = {}
            response = _gh_api(
                "graphql",
                method="POST",
                body={"query": _REVIEW_THREADS_QUERY, "variables": variables},
                response_metadata=response_metadata,
            )
            data = json.loads(response)
            _raise_for_graphql_errors(
                data,
                context="Count unresolved review threads GraphQL error",
                provider="github",
                credential_identity=_credential_identity_for_token(None),
                retry_after=cast(float | None, response_metadata.get("retry_after")),
                reset_timestamp=cast(float | None, response_metadata.get("reset_timestamp")),
                remaining=cast(int | None, response_metadata.get("remaining")),
            )
            repository = (data.get("data") or {}).get("repository")
            if not isinstance(repository, dict):
                raise RuntimeError("Count unresolved review threads GraphQL error: missing data.repository")
            pull_request = repository.get("pullRequest")
            if not isinstance(pull_request, dict):
                raise RuntimeError("Count unresolved review threads GraphQL error: missing data.repository.pullRequest")
            thread_data = pull_request.get("reviewThreads")
            if not isinstance(thread_data, dict):
                raise RuntimeError(
                    "Count unresolved review threads GraphQL error: missing data.repository.pullRequest.reviewThreads"
                )
            for thread in thread_data.get("nodes", []):
                if not thread.get("isResolved", False):
                    unresolved += 1

            page_info = thread_data.get("pageInfo", {})
            if page_info.get("hasNextPage") is True and page_info.get("endCursor"):
                cursor = page_info["endCursor"]
            else:
                break

        return unresolved

    @retry_with_backoff()
    def approve_pr(self, pr_number: int, head_sha: str, body: str) -> bool:
        """Approve a pull request.

        Uses ``AGDT_PR_APPROVER_PAT`` when set so that the approval comes from
        a separate identity (GitHub prevents approving your own PR).  When the
        variable is unset or empty the approval is skipped with a warning.

        Returns:
            ``True`` when approval was submitted, ``False`` when skipped.
        """
        approver_token = os.environ.get("AGDT_PR_APPROVER_PAT", "").strip()
        if not approver_token:
            logger.warning(
                "AGDT_PR_APPROVER_PAT is not configured. "
                "Cannot approve PR without a dedicated approver token. "
                "See repository documentation for setup instructions."
            )
            return False

        try:
            _gh_api(
                self._repo_api(f"/pulls/{pr_number}/reviews"),
                method="POST",
                body={"commit_id": head_sha, "event": "APPROVE", "body": body},
                token=approver_token,
            )
            return True
        except RuntimeError as exc:
            stderr = str(exc)
            if "401" in stderr or "Bad credentials" in stderr.lower():
                logger.warning(
                    "AGDT_PR_APPROVER_PAT authentication failed (401). "
                    "The token may be expired or invalid. "
                    "Skipping PR approval. Rotate the secret and retry."
                )
                return False
            raise

    def get_approver_login(self) -> str:
        """Return the GitHub login for the approver PAT identity.

        Calls ``GET /user`` authenticated with ``AGDT_PR_APPROVER_PAT`` to resolve
        the actual login.  Returns ``""`` when the token is absent, expired, or the
        API call fails so that callers can safely skip the check.

        The resolved value (including the empty-string result) is cached on the
        provider instance, so at most one ``GET /user`` request is issued per
        instance even when the snapshot is rebuilt multiple times per PR.
        """
        if self._approver_login_cache is not None:
            return self._approver_login_cache
        self._approver_login_cache = self._resolve_approver_login()
        return self._approver_login_cache

    def _resolve_approver_login(self) -> str:
        """Resolve the approver-PAT login via ``GET /user`` (uncached)."""
        approver_token = os.environ.get("AGDT_PR_APPROVER_PAT", "").strip()
        if not approver_token:
            return ""
        try:
            response = _gh_api("/user", token=approver_token)
            data = json.loads(response)
            login = data.get("login", "")
            return login if isinstance(login, str) else ""
        except ProviderRateLimitError:
            raise
        except Exception:
            logger.debug("get_approver_login: failed to resolve approver PAT login", exc_info=True)
            return ""

    def get_pr_token_login(self) -> str:
        """Return the GitHub login for the PR-token identity (``SPECKIT_PR_TOKEN``).

        Calls ``GET /user`` authenticated with ``SPECKIT_PR_TOKEN`` to resolve
        the actual login used when posting comments and dispatching repairs.
        Returns ``""`` when the token is absent, expired, or the API call fails
        so that callers can safely treat an empty result as a configuration error.

        The resolved value (including the empty-string result) is cached on the
        provider instance, so at most one ``GET /user`` request is issued per
        instance.
        """
        if self._pr_token_login_cache is not None:
            return self._pr_token_login_cache
        self._pr_token_login_cache = self._resolve_pr_token_login()
        return self._pr_token_login_cache

    def _resolve_pr_token_login(self) -> str:
        """Resolve the SPECKIT_PR_TOKEN login via ``GET /user`` (uncached)."""
        token = os.environ.get("SPECKIT_PR_TOKEN", "").strip()
        if not token:
            return ""
        try:
            response = _gh_api("/user", token=token)
            data = json.loads(response)
            login = data.get("login", "")
            return login if isinstance(login, str) else ""
        except ProviderRateLimitError:
            raise
        except Exception:
            logger.debug("get_pr_token_login: failed to resolve SPECKIT_PR_TOKEN login", exc_info=True)
            return ""

    @retry_with_backoff()
    def merge_pr(self, pr_number: int, head_sha: str, method: str, *, commit_title: str | None = None) -> None:
        """Merge a pull request.

        ``commit_title`` maps to GitHub's ``commit_title`` field, so it only
        controls the squash commit subject line.
        """
        body: dict[str, str] = {"sha": head_sha, "merge_method": method}
        if commit_title and method == "squash":
            body["commit_title"] = commit_title
        _gh_api(
            self._repo_api(f"/pulls/{pr_number}/merge"),
            method="PUT",
            body=body,
        )

    @retry_with_backoff()
    def delete_branch(self, branch: str) -> None:
        """Delete a remote branch via the GitHub API.

        Uses ``DELETE /repos/{owner}/{repo}/git/refs/heads/{branch}``.
        """
        _gh_api(
            self._repo_api(f"/git/refs/heads/{quote(branch, safe='')}"),
            method="DELETE",
        )

    @retry_with_backoff()
    def get_ref_sha(self, ref: str) -> str:
        """Return the current tip SHA for a git ref.

        Uses ``GET /repos/{owner}/{repo}/git/ref/heads/{ref}`` to resolve the
        latest commit SHA on a branch.  Returns an empty string when the ref
        cannot be resolved (e.g. the branch doesn't exist or the API call fails).

        Args:
            ref: Branch name (without ``refs/heads/`` prefix).

        Returns:
            Full commit SHA string, or ``""`` on failure.
        """
        try:
            response = _gh_api(self._repo_api(f"/git/ref/heads/{quote(ref, safe='')}"))
        except RuntimeError:
            return ""
        data = json.loads(response)
        return data.get("object", {}).get("sha", "")

    @retry_with_backoff()
    def publish_pr(self, pr_number: int) -> None:
        """Mark a draft PR as ready for review via gh pr ready command."""
        cmd = ["gh", "pr", "ready", str(pr_number)]
        if self._repo:
            cmd.extend(["--repo", self._repo])
        result = run_safe(cmd, capture_output=True, text=True, shell=False)
        if result.returncode != 0:
            error_message = result.stderr.strip() or result.stdout.strip() or "Unknown error"
            credential_identity = _credential_identity_for_token(None)
            if _is_rate_limit_gh_failure(error_message):
                raise RetryableError(
                    f"GitHub PR publish rate limited: {_sanitize_gh_error(error_message)}",
                    provider="github",
                    credential_identity=credential_identity,
                    source="fallback",
                    is_rate_limit=True,
                )
            if _is_transient_gh_failure(error_message):
                raise RetryableError(
                    f"GitHub PR publish transient failure: {_sanitize_gh_error(error_message)}",
                    provider="github",
                    credential_identity=credential_identity,
                    is_rate_limit=False,
                )
            raise RuntimeError(f"Failed to publish PR #{pr_number}: {error_message}")

    @retry_with_backoff()
    def request_reviewer(self, pr_number: int, reviewer: str) -> None:
        """Request a reviewer for a pull request."""
        _gh_api(
            self._repo_api(f"/pulls/{pr_number}/requested_reviewers"),
            method="POST",
            body={"reviewers": [reviewer]},
        )

    @retry_with_backoff()
    def graphql(self, *, query: str, variables: dict | None = None) -> dict:
        """Execute a GraphQL query or mutation against the GitHub API.

        Uses the ``gh api graphql`` endpoint with the provided query and variables.

        Returns:
            Parsed JSON response as a dictionary.
        """
        body: dict = {"query": query}
        if variables:
            body["variables"] = variables
        response_metadata: dict[str, float | int | None] = {}
        response = _gh_api(
            "graphql",
            method="POST",
            body=body,
            response_metadata=response_metadata,
        )
        data = json.loads(response)
        _raise_for_graphql_errors(
            data,
            context="GitHub GraphQL API returned errors",
            provider="github",
            credential_identity=_credential_identity_for_token(None),
            retry_after=cast(float | None, response_metadata.get("retry_after")),
            reset_timestamp=cast(float | None, response_metadata.get("reset_timestamp")),
            remaining=cast(int | None, response_metadata.get("remaining")),
        )
        return data

    @retry_with_backoff()
    def list_pr_files(self, pr_number: int) -> list[str]:
        """List files changed in a pull request."""
        response = _gh_api(self._repo_api(f"/pulls/{pr_number}/files"), paginate=True)
        files = _parse_paginated_json(response)
        return [f["filename"] for f in files]

    @retry_with_backoff()
    def get_check_annotations(self, check_run_id: int, limit: int) -> list[str]:
        """Get annotations from a check run."""
        response = _gh_api(self._repo_api(f"/check-runs/{check_run_id}/annotations"))
        annotations = json.loads(response)
        return [a.get("message", "") for a in annotations[:limit]]

    def dispatch_repair(
        self,
        pr_number: int,
        head_sha: str,
        repair_type: str,
        failed_checks: list[CheckRunStatus],
        review_comments: list[ReviewCommentInfo],
        review_id: int = 0,
        declared_author_comment_count: int = 0,
        declared_author_comment_counts_by_review: dict[int, int] | None = None,
    ) -> int:
        """Post a @copilot-tagged comment to trigger an AI agent repair session.

        The comment MUST begin with ``@copilot`` for reliable agent triggering.
        Uses ``SPECKIT_PR_TOKEN`` for authentication to ensure
        ``issues:write`` access.  ``COPILOT_GITHUB_TOKEN`` is fine-grained and
        lacks this permission, causing 403 errors when posting comments.

        Links the repair agent/prompt files (they are present in the dispatched
        agent's own checkout) and embeds, for CI repair, the condensed output of
        each failing job, so the dispatched agent has the actionable context
        inline without extra fetches.

        ``declared_author_comment_count`` is the suppressed-comment count the review
        body declared; when it exceeds the number of author comments recovered, the
        body carries a notice naming the shortfall and the recovery fetch. When
        ``declared_author_comment_counts_by_review`` is present, that notice is
        emitted separately for each affected review body.
        """
        from agentic_devtools.cli.ci.job_logs import fetch_failed_check_context  # noqa: PLC0415

        repo = self._repo or os.environ.get("GITHUB_REPOSITORY", "")

        # Use SPECKIT_PR_TOKEN for posting comments (has issues:write permission).
        # COPILOT_GITHUB_TOKEN is fine-grained and lacks issues:write access.
        token = _require_speckit_pr_token("dispatch repair comments")

        # For CI repair, build a context (full check name + per-failing-step logs)
        # for each failing job so the dispatched agent has full context inline.
        run_event_cache: dict[int, str] = {}
        check_contexts: dict[int, FailedCheckContext] = {}
        if repair_type in ("ci", "both"):
            for check in failed_checks:
                ctx = fetch_failed_check_context(check, repo=repo, token=token, run_event_cache=run_event_cache)
                if ctx is not None:
                    check_contexts[check.id] = ctx

        body = _build_repair_comment(
            head_sha=head_sha,
            repair_type=repair_type,
            failed_checks=failed_checks,
            review_comments=review_comments,
            repository_full_name=repo,
            pr_number=pr_number,
            review_id=review_id,
            check_contexts=check_contexts,
            declared_author_comment_count=declared_author_comment_count,
            declared_author_comment_counts_by_review=declared_author_comment_counts_by_review,
        )

        response = self._post_repair_comment(pr_number=pr_number, body=body, token=token)
        data = json.loads(response)
        return data["id"]

    def dispatch_conflict_repair(
        self,
        pr_number: int,
        head_sha: str,
        base_sha: str,
        base_branch: str,
        head_branch: str,
    ) -> int:
        """Post a @copilot-tagged comment to resolve base-branch merge conflicts.

        The comment begins with ``@copilot`` and embeds the cloud-agent-safe
        conflict-resolution prompt file so the dispatched agent has full
        instructions inline.  Uses ``SPECKIT_PR_TOKEN`` for authentication
        (``issues:write`` permission required; ``COPILOT_GITHUB_TOKEN`` lacks it).

        Args:
            pr_number: Pull request number.
            head_sha: Current HEAD SHA of the PR branch.
            base_sha: Current tip SHA of the base branch.
            base_branch: Name of the base/target branch.
            head_branch: Name of the PR head/source branch.

        Returns:
            The ID of the posted comment.
        """
        from agentic_devtools.cli.ci.guards import build_conflict_repair_marker  # noqa: PLC0415

        token = _require_speckit_pr_token("dispatch conflict repair comments")

        prompt_path = ".github/prompts/agdt.resolve-merge-conflicts.cloud-agent.prompt.md"
        prompt_content = _read_repo_file(prompt_path)

        conflict_marker = build_conflict_repair_marker(base_sha=base_sha, head_sha=head_sha)

        prompt_label = "agdt.resolve-merge-conflicts.cloud-agent"
        repo = self._repo or os.environ.get("GITHUB_REPOSITORY", "")

        # Build the @copilot comment body
        lines: list[str] = []
        lines.append(
            f"@copilot - This PR branch (`{head_branch}`) has merge conflicts with "
            f"`{base_branch}`. Please resolve them by merging `origin/{base_branch}` "
            f"(do NOT rebase, amend, or force-push)."
        )
        lines.append("")
        lines.append("<details>")
        lines.append("<summary>Details</summary>")
        lines.append("")
        lines.append("<details>")
        lines.append("<summary>Instructions</summary>")
        lines.append("")
        if repo and "/" in repo:
            prompt_ref = head_sha or base_branch
            prompt_url = f"https://github.com/{repo}/blob/{prompt_ref}/{prompt_path}"
            prompt_link = f"[`./{prompt_path}`]({prompt_url})"
        else:
            prompt_link = f"`./{prompt_path}`"
        lines.append(f"Follow the cloud-agent-safe instructions in {prompt_link}.")
        if prompt_content:
            lines.append("")
            lines.append("<details>")
            lines.append(f"<summary>{prompt_label} complete content</summary>")
            lines.append("")
            lines.append(_fence(prompt_content))
            lines.append("</details>")
        lines.append("")
        lines.append("</details>")
        lines.append("")
        lines.append("</details>")

        body = "\n".join(lines)
        # Append the conflict-repair dedup marker at the very end (after the
        # closing </details>) so that a top-of-comment quote truncation in a
        # cloud agent's reply can never split the HTML comment and leave an
        # unterminated "<!--". should_dispatch_conflict_repair matches the
        # marker anywhere in the body, so end placement does not affect
        # deduplication.
        reserved = len(conflict_marker) + 2
        body = _enforce_comment_size_limit(body, hard_limit=max(0, _MAX_COMMENT_BODY_CHARS - reserved))
        body = f"{body}\n\n{conflict_marker}"
        response = self._post_repair_comment(pr_number=pr_number, body=body, token=token)
        data = json.loads(response)
        return data["id"]

    @retry_with_backoff()
    def _post_repair_comment(self, *, pr_number: int, body: str, token: str | None) -> str:
        return _gh_api(
            self._repo_api(f"/issues/{pr_number}/comments"),
            method="POST",
            body={"body": body},
            token=token,
        )

    @retry_with_backoff()
    def list_review_comments(self, pr_number: int, review_id: int) -> list[ReviewCommentInfo]:
        """List inline comments from a specific review.

        After fetching REST inline comments, also recovers suppressed comments
        from the review body ``<details>`` block (when ``review_id > 0``).
        Suppressed comments are deduplicated against REST comments and merged
        into the result with ``is_suppressed=True``.
        """
        comments, review_body_recovery_complete = self._list_review_comments_with_recovery_status(pr_number, review_id)
        self._set_review_comment_recovery_complete(
            pr_number=pr_number,
            review_id=review_id,
            recovery_complete=review_body_recovery_complete,
        )
        return comments

    def _set_review_comment_recovery_complete(self, *, pr_number: int, review_id: int, recovery_complete: bool) -> None:
        """Cache whether suppressed-comment recovery completed for one review."""
        status = getattr(self, "_review_comment_recovery_complete", None)
        if not isinstance(status, dict):
            status = {}
            setattr(self, "_review_comment_recovery_complete", status)
        status[(pr_number, review_id)] = recovery_complete

    def _was_review_comment_recovery_complete(self, *, pr_number: int, review_id: int) -> bool:
        """Return cached suppressed-comment recovery status for one review.

        Defaults to ``True`` when no status was recorded so tests or callers that
        stub ``list_review_comments()`` continue to exercise the normal path.
        """
        status = getattr(self, "_review_comment_recovery_complete", None)
        if not isinstance(status, dict):
            return True
        cached = status.get((pr_number, review_id))
        return cached if isinstance(cached, bool) else True

    def _list_review_comments_with_recovery_status(
        self, pr_number: int, review_id: int
    ) -> tuple[list[ReviewCommentInfo], bool]:
        """List review comments and report whether suppressed-comment recovery completed."""
        response = _gh_api(
            self._repo_api(f"/pulls/{pr_number}/reviews/{review_id}/comments"),
            paginate=True,
        )
        comments = _parse_paginated_json(response)
        rest_comments = [
            ReviewCommentInfo(
                id=int(c["id"]),
                path=c.get("path", ""),
                body=c.get("body", ""),
                html_url=c.get("html_url", ""),
                is_suppressed=_comment_is_suppressed(c),
                start_line=c.get("start_line") if c.get("start_line") is not None else c.get("line"),
                end_line=c.get("line"),
                line=c.get("line"),
                position=c.get("position"),
                diff_hunk=c.get("diff_hunk", ""),
                commit_id=c.get("commit_id") or "",
                original_commit_id=c.get("original_commit_id") or "",
                source_review_id=(
                    int(c["pull_request_review_id"]) if c.get("pull_request_review_id") is not None else review_id
                ),
                author_login=((c.get("user") or {}).get("login", "") if isinstance(c.get("user"), dict) else ""),
                in_reply_to_id=_parse_optional_positive_int(c.get("in_reply_to_id")),
            )
            for c in comments
        ]

        review_body_recovery_complete = review_id <= 0
        # Recover suppressed comments from the review body (FR-001, FR-006, FR-008)
        if review_id > 0:
            review_body_recovery_complete = True
            try:
                review_response = _gh_api(
                    self._repo_api(f"/pulls/{pr_number}/reviews/{review_id}"),
                )
                review_data = json.loads(review_response)
                review_body = review_data.get("body", "") or ""
                suppressed = _parse_suppressed_from_review_body(review_body, source_review_id=review_id)
                if suppressed:
                    rest_comments = _deduplicate_review_comments(rest_comments, suppressed)
            except ProviderRateLimitError as exc:
                if exc.is_rate_limit:
                    raise
                logger.warning(
                    "PR #%d: Failed to recover suppressed comments from review %d body",
                    pr_number,
                    review_id,
                )
                review_body_recovery_complete = False
            except Exception:
                logger.warning(
                    "PR #%d: Failed to recover suppressed comments from review %d body",
                    pr_number,
                    review_id,
                )
                review_body_recovery_complete = False

        return rest_comments, review_body_recovery_complete

    @retry_with_backoff()
    def list_pr_issue_events(self, pr_number: int) -> list[IssueEvent]:
        """List Copilot session events for a pull request from the Issues Events API.

        Calls ``GET /repos/{owner}/{repo}/issues/{pr_number}/events`` with
        pagination and returns only Copilot session events
        (copilot_work_finished, copilot_work_finished_failure, copilot_work_started)
        in ascending chronological order.
        """
        from agentic_devtools.cli.ci.models import _COPILOT_SESSION_EVENTS  # noqa: PLC0415

        response = _gh_api(self._repo_api(f"/issues/{pr_number}/events"), paginate=True)
        raw_events = _parse_paginated_json(response)
        events: list[IssueEvent] = []
        for ev in raw_events:
            event_type = ev.get("event", "")
            if event_type not in _COPILOT_SESSION_EVENTS:
                continue
            actor = ev.get("actor") or {}
            events.append(
                IssueEvent(
                    id=int(ev.get("id", 0)),
                    event=event_type,
                    created_at=ev.get("created_at", ""),
                    actor_login=actor.get("login", "") if isinstance(actor, dict) else "",
                )
            )
        events.sort(key=lambda e: e.id)
        return events

    @retry_with_backoff()
    def get_pr_diff(self, pr_number: int) -> str:
        """Get the unified diff for a pull request via ``gh pr diff``."""
        result = run_safe(
            ["gh", "pr", "diff", str(pr_number), "--repo", self._repo],
            capture_output=True,
            text=True,
            shell=False,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()
            if _is_transient_gh_failure(stderr):
                raise RetryableError(
                    f"gh pr diff failed: {stderr}",
                    is_rate_limit=_is_rate_limit_gh_failure(stderr),
                )
            raise RuntimeError(f"gh pr diff failed: {stderr}")
        return result.stdout

    @retry_with_backoff()
    def get_commit_range_diff(self, base_sha: str, head_sha: str) -> str:
        """Get unified diff for ``base_sha...head_sha`` via GitHub compare API."""
        result = run_safe(
            [
                "gh",
                "api",
                self._repo_api(f"/compare/{base_sha}...{head_sha}"),
                "--method",
                "GET",
                "-H",
                "Accept: application/vnd.github.v3.diff",
            ],
            capture_output=True,
            text=True,
            shell=False,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()
            if _is_transient_gh_failure(stderr):
                raise RetryableError(
                    f"gh api compare diff failed: {stderr}",
                    is_rate_limit=_is_rate_limit_gh_failure(stderr),
                )
            raise RuntimeError(f"gh api compare diff failed: {stderr}")
        return result.stdout

    def _run_git(self, args: Iterable[str], *, stdin_text: str | None = None) -> str:
        """Run git command and return stdout or raise on failure.

        Args:
            args: Git arguments (without the leading ``git``).
            stdin_text: When provided, is written to the command's stdin.
        """
        args = list(args)
        result = run_safe(
            ["git", *args],
            capture_output=True,
            text=True,
            shell=False,
            input=stdin_text,
        )
        if result.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
        return result.stdout

    @retry_with_backoff()
    def _list_review_comment_ids(self, pr_number: int, review_id: int) -> list[int]:
        """Return numeric review comment IDs for a given review."""
        response = _gh_api(
            self._repo_api(f"/pulls/{pr_number}/reviews/{review_id}/comments"),
            paginate=True,
        )
        comments = _parse_paginated_json(response)
        return [int(c["id"]) for c in comments if c.get("id")]

    @retry_with_backoff()
    def _reply_to_review_comment(self, pr_number: int, comment_id: int, body: str = _ADDRESSED_REPLY_BODY) -> None:
        """Post addressed reply to a single review comment."""
        _gh_api(
            self._repo_api(f"/pulls/{pr_number}/comments/{comment_id}/replies"),
            method="POST",
            body={"body": body},
        )

    @retry_with_backoff()
    def _list_addressed_reply_parent_comment_ids(self, pr_number: int) -> set[int]:
        """Return parent comment IDs that already have an addressed reply.

        Structured resolution-tier replies are considered addressed only when they
        indicate a resolved outcome, so tentative/abandoned lifecycle replies do
        not suppress the final resolved audit reply.
        """
        response = _gh_api(
            self._repo_api(f"/pulls/{pr_number}/comments"),
            paginate=True,
        )
        comments = _parse_paginated_json(response)
        return {
            int(comment["in_reply_to_id"])
            for comment in comments
            if comment.get("in_reply_to_id")
            and (
                str(comment.get("body", "")).strip().lower() == _ADDRESSED_REPLY_BODY.lower()
                or str(comment.get("body", "")).strip().lower().startswith(_LEGACY_ADDRESSED_REPLY_PREFIXES)
                or (
                    _RESOLUTION_TIER_MARKER_PREFIX in str(comment.get("body", ""))
                    and _RESOLUTION_THREAD_RESOLVED_TEXT in str(comment.get("body", "")).strip().lower()
                )
            )
        }

    @retry_with_backoff()
    def _list_abandoned_reply_parent_comment_ids(self, pr_number: int) -> set[int]:
        """Return parent comment IDs that already have an abandoned-resolution reply.

        Unlike :meth:`_list_addressed_reply_parent_comment_ids`, this method only
        matches the specific abandoned marker so that an earlier tentative-resolution
        reply does not suppress the abandoned notification on TTL expiry.
        """
        response = _gh_api(
            self._repo_api(f"/pulls/{pr_number}/comments"),
            paginate=True,
        )
        comments = _parse_paginated_json(response)
        return {
            int(comment["in_reply_to_id"])
            for comment in comments
            if comment.get("in_reply_to_id") and _RESOLUTION_TIER_ABANDONED_MARKER in str(comment.get("body", ""))
        }

    @retry_with_backoff()
    def _list_unresolve_reply_parent_comment_ids(self, pr_number: int) -> set[int]:
        """Return parent comment IDs that already have a 'Thread left open' reply.

        Used to prevent posting duplicate UNRESOLVE audit replies on the same
        thread across repeated AI PR Loop runs.  Only replies that contain both
        the resolution-tier HTML marker and the "Thread left open" status text
        are matched; tentative or resolved tier replies are excluded.
        """
        response = _gh_api(
            self._repo_api(f"/pulls/{pr_number}/comments"),
            paginate=True,
        )
        comments = _parse_paginated_json(response)
        return {
            int(comment["in_reply_to_id"])
            for comment in comments
            if comment.get("in_reply_to_id")
            and _RESOLUTION_TIER_MARKER_PREFIX in str(comment.get("body", ""))
            and _RESOLUTION_THREAD_LEFT_OPEN_TEXT in str(comment.get("body", "")).strip().lower()
        }

    @retry_with_backoff()
    def _list_unconfirmed_resolved_comment_ids(self, pr_number: int) -> set[int]:
        """Return parent comment IDs that have an unconfirmed-commit-change marker reply.

        These threads were resolved by default because HEAD changed but the SDK
        could not confirm resolution. They are eligible for re-evaluation on
        subsequent loop iterations.
        """
        response = _gh_api(
            self._repo_api(f"/pulls/{pr_number}/comments"),
            paginate=True,
        )
        comments = _parse_paginated_json(response)
        # Only treat a thread as unconfirmed when the *latest* reply on that parent contains the marker.
        # Determine "latest" by created_at to avoid relying on API ordering.
        latest_reply_by_parent: dict[int, dict] = {}
        for comment in comments:
            parent_id = comment.get("in_reply_to_id")
            if parent_id is None:
                continue
            try:
                pid = int(parent_id)
            except (TypeError, ValueError):
                continue
            created_at = str(comment.get("created_at", ""))
            prev = latest_reply_by_parent.get(pid)
            prev_created_at = str(prev.get("created_at", "")) if prev is not None else ""
            if prev is None or prev_created_at <= created_at:
                latest_reply_by_parent[pid] = comment
        return {
            parent_id
            for parent_id, comment in latest_reply_by_parent.items()
            if _RESOLUTION_UNCONFIRMED_MARKER in str(comment.get("body", ""))
        }

    def _has_existing_addressed_reply(
        self,
        pr_number: int,
        comment_id: int,
        addressed_reply_parent_comment_ids: set[int] | None = None,
    ) -> bool:
        """Check whether a review comment already has an addressed reply."""
        parent_comment_ids = (
            addressed_reply_parent_comment_ids
            if addressed_reply_parent_comment_ids is not None
            else self._list_addressed_reply_parent_comment_ids(pr_number)
        )
        return comment_id in parent_comment_ids

    def _fetch_review_comment_by_id(self, pr_number: int, comment_id: int) -> ReviewCommentInfo | None:
        """Fetch a single review comment by its ID for re-evaluation purposes."""
        try:
            response = _gh_api(
                self._repo_api(f"/pulls/comments/{comment_id}"),
            )
            c = json.loads(response)
            return ReviewCommentInfo(
                id=int(c["id"]),
                path=c.get("path", ""),
                body=c.get("body", ""),
                html_url=c.get("html_url", ""),
                is_suppressed=_comment_is_suppressed(c),
                start_line=c.get("start_line") if c.get("start_line") is not None else c.get("line"),
                end_line=c.get("line"),
                line=c.get("line"),
                position=c.get("position"),
                diff_hunk=c.get("diff_hunk", ""),
                commit_id=c.get("commit_id") or "",
                original_commit_id=c.get("original_commit_id") or "",
            )
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.warning(
                "Failed to fetch review comment %d for PR #%d: %s",
                comment_id,
                pr_number,
                exc,
            )
            return None

    def _resolution_state_dir(self) -> Path:
        """Return the state directory for tentative thread lifecycle tracking."""
        return get_state_dir() / _THREAD_RESOLUTION_STATE_DIRNAME

    @staticmethod
    def _model_id_for_tier_result(result: TierResult) -> str | None:
        if result.tier_name == "sdk_evaluation":
            return os.environ.get("COPILOT_MODEL", "claude-opus-4.6")
        if result.tier_name == "sdk_evaluation_fallback":
            return os.environ.get("COPILOT_FALLBACK_MODEL", "claude-sonnet-4.6")
        return None

    @staticmethod
    def _resolve_issue_type_from_branch(head_branch: str) -> str:
        """Resolve a Conventional Commit type from the branch prefix."""
        if not head_branch:
            return "chore"
        prefix = head_branch.split("/", 1)[0].lower()
        return _BRANCH_TYPE_MAP.get(prefix, "chore")

    @staticmethod
    def _resolve_issue_key_from_branch(head_branch: str) -> str | None:
        """Resolve an issue key from a branch name."""
        if not head_branch:
            return None
        parts = [part for part in head_branch.split("/") if part]
        if not parts:
            return None
        if len(parts) > 1 and parts[0].lower() in _BRANCH_TYPE_MAP:
            candidate = parts[1]
        elif len(parts) == 1:
            candidate = parts[0]
        else:
            return None
        jira_match = _BRANCH_JIRA_KEY_RE.match(candidate)
        if jira_match:
            return jira_match.group(1)
        github_match = _BRANCH_GITHUB_KEY_RE.match(candidate)
        if github_match:
            return github_match.group(1)
        return None

    @staticmethod
    def _extract_github_key_from_subjects(subjects: list[str]) -> str | None:
        """Extract the first ``#NNN`` reference from commit subjects."""
        for subject in subjects:
            match = _SUBJECT_GITHUB_ISSUE_RE.search(subject)
            if match:
                return match.group(1)
        return None

    def _resolve_issue_key_adapter_aware(
        self,
        head_branch: str,
        commit_subjects: list[str],
        git_root: Path,
    ) -> str | None:
        """Resolve issue key from branch with adapter-aware GitHub fallback.

        For a ``github``-adapter repository, a Jira-style branch key is
        discarded and replaced with the first ``#NNN`` reference found in
        *commit_subjects*.  When the branch yields no recognisable key at all
        (``None``), the same subject-scan fallback is applied for
        ``github``-adapter repos so that branches without a numeric segment
        (e.g. ``fix/description/without-number``) can still resolve an issue
        key from commit messages like ``fix(#2262): …``.

        Numeric keys returned by branch parsing are unambiguous for all
        adapters and are returned immediately without an adapter check.
        """
        issue_key = self._resolve_issue_key_from_branch(head_branch)
        # Numeric keys are adapter-independent — no further resolution needed.
        if issue_key is not None and issue_key.isdigit():
            return issue_key
        # For None or Jira-style keys, check the adapter to decide whether to
        # fall back to subject extraction.
        try:
            issue_adapter = str(load_platform_config(str(git_root)).get("issue_adapter", "jira")).lower()
        except Exception:
            return issue_key
        if issue_adapter == "github":
            # Discard Jira-style keys and branch-less (None) keys alike: for a
            # GitHub-issue-tracker repo the authoritative numeric reference is
            # the ``#NNN`` in commit subjects.
            return self._extract_github_key_from_subjects(commit_subjects)
        return issue_key

    @staticmethod
    def _format_squash_issue_reference(issue_key: str, git_root: Path | None) -> tuple[str, str]:
        """Format squash fallback scope/footer using the repo's issue adapter."""
        issue_adapter = "github"
        if git_root is not None:
            issue_adapter = str(load_platform_config(str(git_root)).get("issue_adapter", "github")).lower()

        if issue_adapter == "markdown":
            return f"({issue_key})", issue_key

        if issue_adapter == "jira":
            issue_link = _derive_issue_link_from_key(issue_key, git_root) if git_root is not None else None
            return f"({issue_key})", f"[{issue_key}]({issue_link})" if issue_link else issue_key

        if issue_key.isdigit():
            return f"(#{issue_key})", f"#{issue_key}"
        return f"({issue_key})", issue_key

    def _build_squash_commit_message(
        self,
        head_sha: str,
        commit_subjects: list[str],
        issue_key: str | None = None,
        git_root: Path | None = None,
    ) -> str:
        """Build a deterministic squash commit message."""
        unique_subjects = [subject.strip() for subject in commit_subjects if subject.strip()]
        scope = ""
        footer = ""
        if issue_key:
            scope, footer = self._format_squash_issue_reference(issue_key, git_root)
        if not unique_subjects:
            if footer:
                return f"chore{scope}: post-repair squash for {head_sha[:8]}\n\n{footer}"
            return f"chore: post-repair squash for {head_sha[:8]}"
        if len(unique_subjects) == 1:
            if footer:
                return f"{unique_subjects[0]}\n\n{footer}"
            return unique_subjects[0]
        bullets = "\n".join(f"- {subject}" for subject in unique_subjects[:10])
        message = f"chore{scope}: squash post-repair updates\n\n{bullets}\n\nAutomated squash for `{head_sha[:8]}`."
        if footer:
            return f"{message}\n\n{footer}"
        return message

    @staticmethod
    def _clean_sdk_commit_message(raw: str, max_length: int = 100) -> str | None:
        """Strip fences/conversational prefixes and return a clean title.

        Returns title text suitable for template rendering, or ``None`` when
        SDK output should be discarded and deterministic fallback should apply.
        """
        message = raw.strip()
        if not message:
            return None

        # Strip markdown fences.
        if message.startswith("```"):
            lines = message.splitlines()
            if len(lines) >= 3 and lines[0].startswith("```") and lines[-1].strip() == "```":
                message = "\n".join(lines[1:-1]).strip()

        # Strip "commit message:" prefix.
        if message.lower().startswith("commit message:"):
            message = message.split(":", 1)[1].strip()

        if not message:
            return None

        title = message.splitlines()[0].strip()
        title = GitHubActionsProvider._strip_sdk_conventional_title_prefix(title)
        if title.lower().startswith(_CONVERSATIONAL_STARTERS):
            logger.warning(
                "Rejecting SDK commit message with conversational opener: %r",
                title[:60],
            )
            return None

        if len(title) > max_length:
            title = title[:max_length].rstrip()
        if not title:
            return None
        return title

    @staticmethod
    def _strip_sdk_conventional_title_prefix(title: str) -> str:
        """Strip a leading conventional-commit prefix from an SDK title when present."""
        match = _SDK_CONVENTIONAL_TYPE_PREFIX_RE.match(title.strip())
        if not match:
            return title.strip()
        return match.group("subject").strip()

    @staticmethod
    def _is_sdk_footer_line(line: str) -> bool:
        """Return True when a line is a commit footer that templates should regenerate."""
        stripped = line.strip()
        if not stripped:
            return False
        return bool(_SDK_FOOTER_LINE_RE.fullmatch(stripped) or _SDK_BREAKING_CHANGE_FOOTER_RE.fullmatch(stripped))

    @staticmethod
    def _strip_trailing_sdk_footer_lines(body: str) -> str:
        """Strip trailing issue-reference / BREAKING CHANGE footers from SDK body text."""
        lines = body.splitlines()
        end = len(lines) - 1
        while end >= 0 and not lines[end].strip():
            end -= 1
        while end >= 0 and GitHubActionsProvider._is_sdk_footer_line(lines[end]):
            end -= 1
            while end >= 0 and not lines[end].strip():
                end -= 1
        return "\n".join(lines[: end + 1]).rstrip()

    @staticmethod
    def _render_squash_message_from_sdk(
        raw: str,
        *,
        issue_key: str | None,
        issue_type: str,
        git_root: Path | None = None,
    ) -> str | None:
        """Render a final squash commit message from raw SDK output via template."""
        message = raw.strip()
        if not message:
            return None
        if message.startswith("```"):
            lines = message.splitlines()
            if len(lines) >= 3 and lines[0].startswith("```") and lines[-1].strip() == "```":
                message = "\n".join(lines[1:-1]).strip()
        if message.lower().startswith("commit message:"):
            message = message.split(":", 1)[1].strip()
        if not message:
            return None
        title = GitHubActionsProvider._clean_sdk_commit_message(message)
        if not title:
            return None
        lines = message.splitlines()
        body = "\n".join(lines[1:]).strip()
        body = GitHubActionsProvider._strip_trailing_sdk_footer_lines(body)
        context: dict[str, str] = {
            "issueType": issue_type,
            "commitMessageTitle": title,
        }
        if issue_key:
            context["issueKey"] = issue_key
        if body:
            context["commitMessageBody"] = body
        return resolve_commit_message_from_template(git_root, context=context)

    def _generate_commit_message_via_sdk(
        self,
        *,
        head_sha: str,
        commit_subjects: list[str],
        head_branch: str | None = None,
        issue_key: str | None = None,
        timeout_seconds: int = 60,
    ) -> str | None:
        """Attempt to generate a squash commit message via Copilot SDK.

        Args:
            head_sha: SHA of the head commit being squashed.
            commit_subjects: List of commit subject lines to summarise.
            head_branch: Branch name used to derive the issue type and, when
                *issue_key* is not supplied, the issue key.
            issue_key: Pre-resolved issue key.  When provided this value is
                used directly in the template render context, bypassing the
                internal ``_resolve_issue_key_adapter_aware`` call.  Pass the
                key already computed by ``_squash_and_force_push`` so that
                both the SDK path and the deterministic fallback path use the
                **same** adapter-aware key rather than re-deriving it
                independently.
            timeout_seconds: Maximum seconds to wait for an SDK response.
        """
        token = os.environ.get("COPILOT_GITHUB_TOKEN", "").strip()
        if not token:
            return None

        try:
            from copilot import CopilotClient
            from copilot.session import PermissionHandler
        except Exception as exc:  # pragma: no cover - optional dependency/runtime
            logger.warning(
                "Copilot SDK unavailable for squash commit message generation: %s",
                exc,
            )
            return None

        model = os.environ.get("COPILOT_MODEL", "claude-opus-4.6")
        unique_subjects = [subject.strip() for subject in commit_subjects if subject.strip()]
        subjects_text = "\n".join(f"- {subject}" for subject in unique_subjects[:20]) or "- (none)"
        prompt = (
            "Generate a concise Conventional Commit message for squashing this pull request.\n"
            "Return plain commit message text only (subject + optional body), no markdown fences.\n\n"
            f"Head SHA: {head_sha}\n"
            "Commit subjects:\n"
            f"{subjects_text}\n"
        )
        # Resolve the repo root via git so adapter config is found correctly even when
        # the workflow runs from a subdirectory (Path.cwd() would miss .github/agdt-config.json).
        try:
            git_root = Path(self._run_git(["rev-parse", "--show-toplevel"]).strip())
        except RuntimeError:
            logger.warning("Could not determine git repo root; falling back to cwd for adapter config")
            git_root = Path.cwd()

        # Capture the caller-supplied key so the closure can reference it.
        resolved_issue_key = issue_key

        async def _run() -> str | None:
            client = None
            session = None
            content_parts: list[str] = []
            error_messages: list[str] = []
            done = asyncio.Event()
            try:
                client = CopilotClient(github_token=token)
                await client.start()
                try:
                    session = await client.create_session(
                        model=model,
                        on_permission_request=PermissionHandler.approve_all,
                        infinite_sessions={"enabled": False},
                        github_token=token,
                    )
                except TypeError as exc:
                    if "unexpected keyword argument" not in str(exc) or "github_token" not in str(exc):
                        raise  # pragma: no cover - defensive re-raise for unrelated TypeErrors
                    session = await client.create_session(
                        model=model,
                        on_permission_request=PermissionHandler.approve_all,
                        infinite_sessions={"enabled": False},
                    )

                def on_event(event: Any) -> None:
                    event_type = getattr(getattr(event, "type", None), "value", "")
                    if event_type == "assistant.message":
                        content_parts.append(getattr(getattr(event, "data", None), "content", ""))
                    elif event_type == "session.idle":
                        done.set()
                    elif event_type in {"error", "session.error", "assistant.error"}:
                        msg = getattr(getattr(event, "data", None), "message", None) or str(getattr(event, "data", ""))
                        error_messages.append(f"{event_type}: {msg}")
                        done.set()
                    else:  # pragma: no cover
                        pass

                session.on(on_event)
                await session.send(prompt)
                await done.wait()

                if error_messages:
                    logger.warning("Copilot SDK returned errors for squash message: %s", "; ".join(error_messages))
                    return None

                raw = (content_parts[-1] if content_parts else "").strip()
                if not raw:
                    return None
                issue_type = self._resolve_issue_type_from_branch(head_branch or "")
                # Use the pre-resolved key when the caller supplied one.  This
                # ensures the SDK render path and the deterministic fallback
                # path always share the same adapter-aware resolution rather
                # than independently re-deriving it (which can diverge in edge
                # cases such as cwd changes or config-file timing).
                effective_issue_key: str | None
                if resolved_issue_key is not None:
                    effective_issue_key = resolved_issue_key
                else:
                    effective_issue_key = self._resolve_issue_key_adapter_aware(
                        head_branch or "", commit_subjects, git_root
                    )
                return GitHubActionsProvider._render_squash_message_from_sdk(
                    raw,
                    issue_key=effective_issue_key,
                    issue_type=issue_type,
                    git_root=git_root,
                )
            except Exception as exc:  # pragma: no cover - defensive runtime fallback
                logger.warning("Copilot SDK commit message generation failed: %s", exc)
                return None
            finally:
                if session is not None:
                    try:
                        await session.disconnect()
                    except Exception:  # pragma: no cover - defensive cleanup
                        pass
                else:  # pragma: no cover
                    pass
                if client is not None:
                    try:
                        await client.stop()
                    except Exception:  # pragma: no cover - defensive cleanup
                        pass

        try:
            return asyncio.run(asyncio.wait_for(_run(), timeout=timeout_seconds))
        except TimeoutError:
            logger.warning("Copilot SDK commit message generation timed out after %ss", timeout_seconds)
            return None
        except RuntimeError as exc:  # pragma: no cover - defensive runtime fallback
            logger.warning("Copilot SDK commit message generation could not start event loop: %s", exc)
            return None

    def _resolve_conflicted_file_content_via_sdk(
        self,
        *,
        file_path: str,
        conflict_content: str,
        base_branch: str,
        head_branch: str,
        timeout_seconds: int = 90,
    ) -> str | None:
        """Attempt to resolve a single conflicted file via Copilot SDK."""
        token = os.environ.get("COPILOT_GITHUB_TOKEN", "").strip()
        if not token:
            return None

        try:
            from copilot import CopilotClient
            from copilot.session import PermissionHandler
        except Exception as exc:  # pragma: no cover - optional dependency/runtime
            logger.warning(
                "Copilot SDK unavailable for conflict resolution: %s",
                exc,
            )
            return None

        model = os.environ.get("COPILOT_MODEL", "claude-opus-4.6")
        prompt = (
            "You are resolving a git rebase conflict.\n"
            "Preserve valid changes from both sides where possible.\n"
            "Output ONLY the final resolved file content with all conflict markers removed.\n"
            "Do not wrap output in markdown fences.\n\n"
            f"Base branch: {base_branch}\n"
            f"Head branch: {head_branch}\n"
            f"File path: {file_path}\n\n"
            "Conflicted file content:\n"
            f"{conflict_content}\n"
        )

        async def _run() -> str | None:
            client = None
            session = None
            content_parts: list[str] = []
            error_messages: list[str] = []
            done = asyncio.Event()
            try:
                client = CopilotClient(github_token=token)
                await client.start()
                try:
                    session = await client.create_session(
                        model=model,
                        on_permission_request=PermissionHandler.approve_all,
                        infinite_sessions={"enabled": False},
                        github_token=token,
                    )
                except TypeError as exc:
                    if "unexpected keyword argument" not in str(exc) or "github_token" not in str(exc):
                        raise  # pragma: no cover - defensive re-raise for unrelated TypeErrors
                    session = await client.create_session(
                        model=model,
                        on_permission_request=PermissionHandler.approve_all,
                        infinite_sessions={"enabled": False},
                    )

                def on_event(event: Any) -> None:
                    event_type = getattr(getattr(event, "type", None), "value", "")
                    if event_type == "assistant.message":
                        content_parts.append(getattr(getattr(event, "data", None), "content", ""))
                    elif event_type == "session.idle":
                        done.set()
                    elif event_type in {"error", "session.error", "assistant.error"}:
                        msg = getattr(getattr(event, "data", None), "message", None) or str(getattr(event, "data", ""))
                        error_messages.append(f"{event_type}: {msg}")
                        done.set()
                    else:  # pragma: no cover
                        pass

                session.on(on_event)
                await session.send(prompt)
                await done.wait()

                if error_messages:
                    logger.warning(
                        "Copilot SDK returned errors while resolving %s: %s",
                        file_path,
                        "; ".join(error_messages),
                    )
                    return None

                raw = content_parts[-1] if content_parts else ""
                if raw == "":
                    return None

                if raw.startswith("```"):
                    lines = raw.splitlines()
                    if len(lines) >= 3 and lines[0].startswith("```") and lines[-1].strip() == "```":
                        raw = "\n".join(lines[1:-1])
                return raw
            except Exception as exc:  # pragma: no cover - defensive runtime fallback
                logger.warning("Copilot SDK conflict resolution failed for %s: %s", file_path, exc)
                return None
            finally:
                if session is not None:
                    try:
                        await session.disconnect()
                    except Exception:  # pragma: no cover - defensive cleanup
                        pass
                else:  # pragma: no cover
                    pass
                if client is not None:
                    try:
                        await client.stop()
                    except Exception:  # pragma: no cover - defensive cleanup
                        pass

        try:
            return asyncio.run(asyncio.wait_for(_run(), timeout=timeout_seconds))
        except TimeoutError:
            logger.warning("Copilot SDK conflict resolution timed out for %s after %ss", file_path, timeout_seconds)
            return None
        except RuntimeError as exc:  # pragma: no cover - defensive runtime fallback
            logger.warning("Copilot SDK conflict resolution could not start event loop for %s: %s", file_path, exc)
            return None

    def _resolve_rebase_conflicts_via_sdk(
        self,
        *,
        base_branch: str,
        head_branch: str,
        max_rounds: int = 5,
    ) -> bool:
        """Best-effort auto-resolution of in-progress rebase conflicts via Copilot SDK."""

        def _has_conflict_markers(content: str) -> bool:
            return bool(re.search(r"(?m)^(<<<<<<<|=======|>>>>>>>)(?: .*)?$", content))

        for round_index in range(max_rounds):
            conflicted_raw = self._run_git(["diff", "--name-only", "--diff-filter=U"])
            conflicted_files = [line.strip() for line in conflicted_raw.splitlines() if line.strip()]
            if not conflicted_files:
                logger.warning("No conflicted files found while attempting rebase conflict resolution.")
                return False

            logger.info(
                "Attempting Copilot SDK conflict resolution for %d file(s) (round %d/%d).",
                len(conflicted_files),
                round_index + 1,
                max_rounds,
            )

            for file_path in conflicted_files:
                path = Path(file_path)
                try:
                    conflict_content = path.read_text(encoding="utf-8")
                except Exception as exc:
                    logger.warning("Failed to read conflicted file %s: %s", file_path, exc)
                    return False

                resolved_content = self._resolve_conflicted_file_content_via_sdk(
                    file_path=file_path,
                    conflict_content=conflict_content,
                    base_branch=base_branch,
                    head_branch=head_branch,
                )
                if resolved_content is None:
                    logger.warning("Copilot SDK did not return a resolution for %s.", file_path)
                    return False

                if _has_conflict_markers(resolved_content):
                    logger.warning(
                        "Copilot SDK returned unresolved conflict markers for %s; refusing to stage.",
                        file_path,
                    )
                    return False

                path.write_text(resolved_content, encoding="utf-8")
                self._run_git(["add", file_path])

            try:
                self._run_git(["-c", "core.editor=true", "rebase", "--continue"])
                logger.info("Rebase conflict resolution completed successfully.")
                return True
            except RuntimeError as exc:
                still_conflicted = self._run_git(["diff", "--name-only", "--diff-filter=U"]).strip()
                if not still_conflicted:
                    logger.warning("`git rebase --continue` failed without remaining conflicts: %s", exc)
                    return False
                logger.warning(
                    "Rebase still has conflicts after SDK resolution round %d: %s",
                    round_index + 1,
                    exc,
                )

        logger.warning("Exceeded maximum conflict-resolution rounds (%d).", max_rounds)
        return False

    def _squash_and_force_push(
        self,
        *,
        base_branch: str,
        head_branch: str,
        head_sha: str,
        reset_to_remote: bool = False,
    ) -> None:
        """Squash commits on head branch into one and force-push with lease."""
        self._run_git(["fetch", "origin", base_branch, head_branch])
        self._run_git(["checkout", head_branch])
        if reset_to_remote:
            self._run_git(["reset", "--hard", f"origin/{head_branch}"])
        merge_base = self._run_git(["merge-base", "HEAD", f"origin/{base_branch}"]).strip()
        commit_count = int(self._run_git(["rev-list", "--count", f"{merge_base}..HEAD"]).strip() or "0")
        if commit_count > 1:
            subjects_raw = self._run_git(["log", "--format=%s", f"{merge_base}..HEAD"])
            commit_subjects = [line for line in subjects_raw.splitlines() if line.strip()]
            try:
                git_root = Path(self._run_git(["rev-parse", "--show-toplevel"]).strip())
            except RuntimeError:
                logger.warning("Could not determine git repo root; falling back to cwd for adapter config")
                git_root = Path.cwd()
            issue_key = self._resolve_issue_key_adapter_aware(head_branch, commit_subjects, git_root)
            commit_message = self._generate_commit_message_via_sdk(
                head_sha=head_sha,
                commit_subjects=commit_subjects,
                head_branch=head_branch,
                issue_key=issue_key,
            ) or self._build_squash_commit_message(
                head_sha,
                commit_subjects,
                issue_key=issue_key,
                git_root=git_root,
            )
            self._run_git(["reset", "--soft", merge_base])
            self._run_git(["commit", "-m", commit_message])
        rebase_target = f"origin/{base_branch}"
        try:
            logger.info("Rebasing squashed branch onto %s", rebase_target)
            self._run_git(["rebase", rebase_target])
            logger.info("Rebase onto %s completed successfully", rebase_target)
        except RuntimeError as exc:
            logger.warning("Rebase onto %s failed: %s", rebase_target, exc)
            logger.info("Attempting conflict resolution via Copilot SDK while rebase is in progress")
            try:
                resolved = self._resolve_rebase_conflicts_via_sdk(
                    base_branch=base_branch,
                    head_branch=head_branch,
                )
            except RuntimeError as resolve_exc:
                logger.warning("Conflict resolution helper raised: %s", resolve_exc)
                resolved = False
            if not resolved:
                logger.warning(
                    "Could not auto-resolve rebase conflicts. Aborting rebase and proceeding with squashed commit."
                )
                try:
                    self._run_git(["rebase", "--abort"])
                except RuntimeError as abort_exc:
                    raise RuntimeError(f"`git rebase --abort` failed: {abort_exc}") from abort_exc
        self._run_git(["push", "--force-with-lease", "origin", f"HEAD:{head_branch}"])

    def squash_before_publish(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
    ) -> None:
        """Squash commits and push branch before draft PR publish."""
        logger.info("Squashing PR #%d before publish", pr_number)
        self._squash_and_force_push(base_branch=base_branch, head_branch=head_branch, head_sha=head_sha)

    def count_commits_above_merge_base(
        self,
        *,
        base_branch: str,
        head_sha: str,
    ) -> int:
        """Return commit count above merge-base between origin/base and ``head_sha``."""
        self._run_git(["fetch", "origin", base_branch])
        self._run_git(["fetch", "origin", head_sha])
        merge_base = self._run_git(["merge-base", head_sha, f"origin/{base_branch}"]).strip()
        commit_count_raw = self._run_git(["rev-list", "--count", f"{merge_base}..{head_sha}"]).strip()
        return int(commit_count_raw or "0")

    def count_commits_behind(self, *, pr_number: int, base_branch: str, head_branch: str) -> int:
        """Return how many commits head_branch is behind base_branch using compare API.

        Uses ``gh api /repos/{owner}/{repo}/compare/{base}...{head}`` and reads
        ``behind_by`` directly.
        """
        repo = self._resolve_repo()
        compare_ref = f"{quote(base_branch, safe='')}...{quote(head_branch, safe='')}"
        cmd = [
            "gh",
            "api",
            f"/repos/{repo}/compare/{compare_ref}",
            "--jq",
            ".behind_by",
        ]
        try:
            result = run_safe(cmd, capture_output=True, text=True, shell=False)
        except Exception as exc:
            raise RuntimeError(f"PR #{pr_number}: compare API request failed") from exc
        if result.returncode != 0:
            stderr = result.stderr.strip()
            message = stderr or f"exit code {result.returncode}"
            raise RuntimeError(f"PR #{pr_number}: compare API failed: {message}")
        return int(result.stdout.strip() or "0")

    def compute_diff_hash(self, *, base_branch: str, sha: str) -> str | None:
        """Compute a rebase-invariant fingerprint of ``git diff origin/{base_branch}...{sha}``.

        Used by :func:`evaluate_copilot_gate_verdict` to verify that the PR diff
        has not changed since a prior-commit Copilot review (content-hash freshness).

        The fingerprint is ``git patch-id --verbatim`` of a low-context
        (``-U1``) three-dot diff rather than a hash of the raw diff text.

        A raw diff hash is *not* rebase-invariant because ``index <blob>..<blob>``
        lines and ``@@ ... @@`` hunk-headers both move when the base branch
        advances — ``patch-id`` ignores those.  Using ``-U1`` (one context line)
        rather than ``-U0`` (zero context) preserves enough location information
        to distinguish identical ``+``/``-`` hunks at different occurrences in the
        same file.  ``-U0`` removes all context so two ``-old\n+new`` substitutions
        at different positions would hash identically.

        The one remaining limitation: if the base branch advances a line that is
        the *immediate* neighbor of the PR hunk (within the 1-line context
        window), the fingerprint changes even though the PR content is unchanged.
        In practice such changes cause a rebase conflict, so a conflict-free pure
        rebase cannot trigger a false ``REASON_CONTENT_CHANGED``.

        ``--verbatim`` is required (not ``--stable``): ``--stable`` ignores
        whitespace within the patch and therefore collides on whitespace-only
        edits, which are real changes.

        The low-context diff still distinguishes binary content changes (the
        ``Binary files …`` line is preserved), rename targets, mode changes,
        deletes vs creates, and whitespace-only edits.

        When the diff is empty, ``patch-id`` emits nothing; a namespaced
        ``sha256:<digest>`` of the empty diff text is returned so that a pure
        rebase of a net-empty PR preserves its fingerprint rather than causing
        the freshness gate to request a new review.

        Returns:
            A namespaced fingerprint of the diff (``patch-id:<id>`` or
            ``sha256:<digest>``), or ``None`` if the SHA is not reachable locally
            and a targeted fetch also fails.

        Raises:
            RuntimeError: When fetching ``origin/{base_branch}`` fails, when
                ``git diff origin/{base_branch}...{sha}`` fails, or when
                ``git patch-id --verbatim`` fails.
        """
        try:
            self._run_git(["fetch", "origin", base_branch])
        except Exception as exc:
            raise RuntimeError(f"compute_diff_hash: failed to fetch base branch {base_branch}: {exc}") from exc

        # Ensure the target SHA is available locally.
        try:
            self._run_git(["cat-file", "-e", f"{sha}^{{commit}}"])
        except Exception:
            # SHA not available — attempt a targeted fetch.
            try:
                self._run_git(["fetch", "--no-tags", "origin", sha])
            except Exception:
                return None  # SHA unavailable; treat as unknown diff

        try:
            diff = self._run_git(["diff", "-U1", f"origin/{base_branch}...{sha}"])
        except Exception as exc:
            raise RuntimeError(f"compute_diff_hash: git diff origin/{base_branch}...{sha} failed: {exc}") from exc

        try:
            patch_id_output = self._run_git(["patch-id", "--verbatim"], stdin_text=diff)
        except Exception as exc:
            raise RuntimeError(f"compute_diff_hash: git patch-id --verbatim failed: {exc}") from exc

        # Output is "<patch-id> <commit-id>"; the commit id is all zeroes for stdin input.
        patch_id = patch_id_output.split(" ", 1)[0].strip()
        if not patch_id:
            # Empty diff — return a stable namespaced fingerprint so a pure rebase
            # of a net-empty PR compares equal on both sides rather than triggering
            # a fresh-review request.
            return f"sha256:{hashlib.sha256(diff.encode()).hexdigest()}"
        return f"patch-id:{patch_id}"

    def rebase_onto_base(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
    ) -> None:
        """Rebase head_branch onto base_branch and force-push with lease.

        Raises:
            RebaseConflictError: When conflicts cannot be auto-resolved.
            ForceWithLeaseError: When force-push-with-lease fails.
        """
        from agentic_devtools.cli.ci.pipeline.exceptions import (
            ForceWithLeaseError,
            RebaseConflictError,
        )

        self._run_git(["fetch", "origin", base_branch, head_branch])
        self._run_git(["checkout", head_branch])
        expected_head = self._run_git(["rev-parse", head_sha]).strip()
        current_head = self._run_git(["rev-parse", "HEAD"]).strip()
        if current_head != expected_head:
            raise RuntimeError(
                "Head SHA changed before rebase "
                f"(expected resolved {expected_head} from input {head_sha}, got {current_head}). "
                "The branch may have been updated by another process; aborting "
                "to avoid overwriting changes."
            )

        rebase_target = f"origin/{base_branch}"
        try:
            logger.info("PR #%d: Rebasing %s onto %s", pr_number, head_branch, rebase_target)
            self._run_git(["rebase", rebase_target])
            logger.info("PR #%d: Rebase onto %s completed successfully", pr_number, rebase_target)
        except RuntimeError as exc:
            logger.warning("PR #%d: Rebase onto %s failed: %s", pr_number, rebase_target, exc)
            logger.info("PR #%d: Attempting conflict resolution via Copilot SDK", pr_number)
            try:
                resolved = self._resolve_rebase_conflicts_via_sdk(
                    base_branch=base_branch,
                    head_branch=head_branch,
                )
            except RuntimeError as resolve_exc:
                logger.warning("PR #%d: Conflict resolution helper raised: %s", pr_number, resolve_exc)
                resolved = False
            if not resolved:
                logger.warning("PR #%d: Could not auto-resolve rebase conflicts. Aborting rebase.", pr_number)
                try:
                    self._run_git(["rebase", "--abort"])
                except RuntimeError as abort_exc:
                    raise RebaseConflictError(
                        f"Rebase conflicts unresolvable and abort failed: {abort_exc}"
                    ) from abort_exc
                raise RebaseConflictError("Rebase conflicts could not be auto-resolved") from exc

        try:
            self._run_git(["push", "--force-with-lease", "origin", f"HEAD:{head_branch}"])
        except RuntimeError as exc:
            raise ForceWithLeaseError(f"Force-push-with-lease failed: {exc}") from exc

    def reclaim_copilot_commit(
        self,
        *,
        pr_number: int,
        head_branch: str,
        head_sha: str,
    ) -> None:
        """Re-author the HEAD commit under the CI identity and force-push.

        "Launders" a Copilot-authored HEAD into a human-authored commit so the
        force-push emits a ``synchronize`` event from a human pusher and the
        required ``pull_request`` checks run (Copilot/automation pushes are
        suppressed by GitHub's automation-origin exception).

        Performs: fetch → checkout → HEAD-SHA safety check → ``commit --amend
        --reset-author`` → force-push-with-lease. The amend keeps the same tree
        (no content change); only the author/committer identity and SHA change.

        Raises:
            ForceWithLeaseError: When the force-push-with-lease fails.
            RuntimeError: When HEAD moved before the reclaim (concurrent update).
        """
        from agentic_devtools.cli.ci.pipeline.exceptions import ForceWithLeaseError

        self._run_git(["fetch", "origin", head_branch])
        self._run_git(["checkout", head_branch])
        expected_head = self._run_git(["rev-parse", head_sha]).strip()
        current_head = self._run_git(["rev-parse", "HEAD"]).strip()
        if current_head != expected_head:
            raise RuntimeError(
                "Head SHA changed before Copilot takeover "
                f"(expected resolved {expected_head} from input {head_sha}, got {current_head}). "
                "The branch may have been updated by another process; aborting to avoid clobbering."
            )

        # Re-author HEAD under the configured CI (human) identity without changing
        # the tree. --reset-author updates author + committer to the configured
        # git identity; --no-edit preserves the commit message.
        self._run_git(["commit", "--amend", "--reset-author", "--no-edit"])

        try:
            self._run_git(["push", "--force-with-lease", "origin", f"HEAD:{head_branch}"])
        except RuntimeError as exc:
            raise ForceWithLeaseError(f"Force-push-with-lease failed during Copilot takeover: {exc}") from exc

    def _resolve_repo(self) -> str:
        """Resolve the repository in ``owner/repo`` format."""
        repo = self._repo or os.environ.get("GITHUB_REPOSITORY", "")
        if "/" not in repo:
            raise RuntimeError("Repository must be in 'owner/repo' format for post-repair finalization.")
        return repo

    @staticmethod
    def _build_head_commit_line(head_sha: str, repo: str) -> str:
        """Build a HEAD commit link line for resolution replies.

        Returns an empty string if head_sha is missing or too short, or if
        repo is not a valid 'owner/repo' string (e.g. contains whitespace,
        extra slashes, or empty owner/repo segments).
        """
        if not head_sha or len(head_sha) < 7:
            return ""
        clean_repo = repo.strip()
        if re.search(r"\s", clean_repo):
            return ""
        owner_repo = clean_repo.split("/", 1)
        if len(owner_repo) != 2 or not owner_repo[0] or not owner_repo[1] or clean_repo.count("/") != 1:
            return ""
        short = head_sha[:7]
        return f"\n\n**HEAD**: [{short}](https://github.com/{clean_repo}/commit/{head_sha})"

    def finalize_post_repair(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
        review_id: int,
    ) -> FinalizationResult:
        """Perform soft post-repair finalization after Copilot pushes a fix commit.

        Implements commit-change guard and per-comment SDK verification:
        1. Fetches the review to get its commit_sha.
        2. Guards: skips if no new commit since the review (FR-001/002).
        3. For each unresolved comment, calls the Copilot SDK to verify
           whether the diff addresses the feedback (FR-004/005/006/007).
        4. Only replies and resolves threads where SDK responds COMMENT_RESOLVE.

        Returns:
            FinalizationResult with details about what was resolved/skipped.
        """
        repo = self._resolve_repo()
        review_key = FinalizedReviewKey(repository=repo, pr_number=pr_number, review_id=review_id)
        finalization_state_store = PRCommentFinalizationStateStore(self)
        if finalization_state_store.is_terminal(key=review_key):
            logger.info(
                "PR #%d review %d was permanently finalized earlier — skipping re-finalization",
                pr_number,
                review_id,
            )
            return FinalizationResult(skipped=True, reason="already_finalized")
        self._thread_signals_cache.pop(pr_number, None)
        self._thread_identity_cache.pop(pr_number, None)

        # --- Commit Guard (FR-001/002/014) ---
        reviews = self.list_reviews(pr_number)
        review = next((r for r in reviews if r.id == review_id), None)

        # FR-014: null/missing review or commit_sha → fail-safe skip
        if not review or not review.commit_sha:
            logger.error(
                "Cannot determine review commit SHA for review %d on PR #%d — skipping finalization (fail-safe)",
                review_id,
                pr_number,
            )
            return FinalizationResult(skipped=True, reason="unresolvable_review_commit_sha")

        # FR-001/002: no new commit since review → skip
        if review.commit_sha == head_sha:
            logger.warning(
                "No new commit since Copilot review %d on PR #%d (both at %s) — skipping finalization",
                review_id,
                pr_number,
                head_sha,
            )
            return FinalizationResult(skipped=True, reason="no_new_commit")

        # --- Per-Comment SDK Verification Loop (FR-004/005/006/007/008) ---
        comments = self.list_review_comments(pr_number, review_id)
        if not comments:
            review_body_recovery_complete = self._was_review_comment_recovery_complete(
                pr_number=pr_number,
                review_id=review_id,
            )
            if not review_body_recovery_complete:
                error = f"review #{review_id}: review comment recovery incomplete"
                logger.warning(
                    "PR #%d: Review %d comment recovery incomplete — skipping terminal no-comments marker",
                    pr_number,
                    review_id,
                )
                return FinalizationResult(reason="review_comment_recovery_incomplete", errors=(error,))
            logger.info("No review comments for review %d on PR #%d — nothing to finalize", review_id, pr_number)
            finalization_state_store.mark_terminal(key=review_key, reason="no_comments")
            return FinalizationResult(skipped=False, reason="no_comments")

        # Build diff context once for this review
        diff_context = self._build_verification_context_diff(review.commit_sha, head_sha)

        resolved_ids: list[int] = []
        has_unconfirmed_resolution = False
        unconfirmed_unresolve_ids: list[int] = []
        resolutions: list[CommentResolution] = []
        errors: list[str] = []

        # Check which comments already have addressed replies so we can avoid
        # duplicate replies while still requiring SDK verification before
        # resolving their threads.
        addressed_reply_parent_comment_ids = self._list_addressed_reply_parent_comment_ids(pr_number)
        # Narrower check for abandoned replies: only suppress the abandoned notification
        # if an abandoned-specific marker already exists. An earlier tentative reply with
        # a different resolution-tier marker must NOT suppress the TTL-expiry notification.
        abandoned_reply_parent_comment_ids = self._list_abandoned_reply_parent_comment_ids(pr_number)
        # Suppress duplicate "Thread left open" audit replies for threads that were
        # already evaluated as UNRESOLVE in a prior AI PR Loop run.
        unresolve_reply_parent_comment_ids = self._list_unresolve_reply_parent_comment_ids(pr_number)

        # --- Pre-filter already-resolved threads ---
        # Fetch thread resolution states to skip threads already resolved
        # (e.g., manually resolved by the user). Avoids wasted tier evaluations
        # and prevents counting manually-resolved threads as "unresolved".
        try:
            thread_states = self.list_review_thread_states(pr_number)
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.warning(
                "Failed to fetch thread resolution states for PR #%d: %s — will evaluate all comments",
                pr_number,
                exc,
            )
            thread_states = {}

        comments_for_sdk: list[tuple[ReviewCommentInfo, str]] = []
        for comment in comments:
            # Skip threads already resolved (e.g., manually resolved by a user).
            if thread_states.get(comment.id, (False, False))[0]:
                logger.debug(
                    "Comment %d on PR #%d is already resolved — skipping tier evaluation",
                    comment.id,
                    pr_number,
                )
                continue

            # Suppressed comments are intentionally left unresolved, but must still
            # be recorded so summaries stay informative. Negative-ID (synthetic)
            # entries are reported via ``suppressed_count`` rather than
            # ``unresolved_count`` — they have no GitHub thread and can never be
            # resolved, so counting them would block the gate forever. A
            # positive-ID suppressed comment (an API-minimised REST comment) is
            # still counted as unresolved, matching the snapshot.
            #
            # This branch is synthetic-only: the sole producer of ``is_suppressed=True``
            # is _parse_suppressed_from_review_body, which always assigns negative
            # sentinel IDs. Every other construction site derives the flag from
            # _comment_is_suppressed over a REST payload, which never carries the
            # minimized keys (see that helper's docstring). A genuinely minimized
            # inline comment therefore arrives here with ``is_suppressed=False`` and is
            # SDK-evaluated (and resolvable) like any other — skipping it cannot stall
            # the loop. If a future GraphQL-backed path ever sets ``is_suppressed`` on a
            # positive-ID comment, revisit this: snapshot.count_unresolved_prior_threads
            # skips only ``id < 0``, so such a comment would be counted as an unresolved
            # thread while never being evaluated or resolved here.
            if comment.is_suppressed:
                resolutions.append(
                    CommentResolution(
                        comment_id=comment.id,
                        verdict=VerificationVerdict.COMMENT_UNRESOLVE,
                    )
                )
                continue

            comment_context = self._build_comment_verification_context(comment, diff_context)
            comments_for_sdk.append((comment, comment_context))

        # Include previously unconfirmed-resolved threads for re-evaluation
        existing_comment_ids = {comment.id for comment, _ in comments_for_sdk}
        reevaluated_unconfirmed_comment_ids: set[int] = set()
        unconfirmed_reevaluation_complete = True
        try:
            unconfirmed_ids = self._list_unconfirmed_resolved_comment_ids(pr_number)
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.warning(
                "Failed to fetch unconfirmed resolved comment IDs for PR #%d: %s",
                pr_number,
                exc,
            )
            unconfirmed_ids = set()
            unconfirmed_reevaluation_complete = False
        for unconfirmed_id in unconfirmed_ids:
            if unconfirmed_id in existing_comment_ids:
                # Already in-scope for SDK verification, but still needs special handling
                # (confirmation replies / unresolve) as an unconfirmed-resolved thread.
                reevaluated_unconfirmed_comment_ids.add(unconfirmed_id)
                continue
            unconfirmed_comment = self._fetch_review_comment_by_id(pr_number, unconfirmed_id)
            if unconfirmed_comment is None:
                logger.warning(
                    "Failed to fetch unconfirmed resolved review comment %d on PR #%d; "
                    "keeping review non-terminal for re-evaluation safety",
                    unconfirmed_id,
                    pr_number,
                )
                unconfirmed_reevaluation_complete = False
                continue
            if unconfirmed_comment.is_suppressed:
                # Unreachable in practice for the same reason as the suppressed branch
                # above: _fetch_review_comment_by_id reads a REST payload, which never
                # carries the minimized keys _comment_is_suppressed looks for.
                unconfirmed_reevaluation_complete = False
                continue
            comment_context = self._build_comment_verification_context(unconfirmed_comment, diff_context)
            comments_for_sdk.append((unconfirmed_comment, comment_context))
            reevaluated_unconfirmed_comment_ids.add(unconfirmed_comment.id)

        state_dir: Path | None = None
        reply_formatter = ReplyFormatter()
        if comments_for_sdk:
            tier_results_by_comment_id: dict[int, TierResult] = {}
            try:
                is_outdated_by_id = self._fetch_outdated_by_comment_id(pr_number)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning(
                    "Failed to fetch thread outdated status for PR #%d: %s — is_outdated will be None",
                    pr_number,
                    exc,
                )
                is_outdated_by_id = {}
            try:
                latest_thread_comment_body_by_id = self._fetch_latest_thread_comment_body_by_comment_id(pr_number)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning(
                    "Failed to fetch latest thread comment body for PR #%d: %s",
                    pr_number,
                    exc,
                )
                latest_thread_comment_body_by_id = {}
            try:
                latest_thread_comment_author_login_by_id = self._fetch_latest_thread_comment_author_login_by_comment_id(
                    pr_number
                )
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning(
                    "Failed to fetch latest thread comment author login for PR #%d: %s",
                    pr_number,
                    exc,
                )
                latest_thread_comment_author_login_by_id = {}
            # Compute SWE agent context flags for the SWE agent reply tier (Bug 3).
            # swe_session_started_after_review: a copilot_work_started event exists
            # with created_at timestamp strictly after the review's submission time.
            # swe_agent_commented_on_pr: the SWE agent posted at least one issue comment
            # on the PR (catches both @copilot dispatch and "Fix with Copilot" button flows).
            swe_session_started_after_review = False
            swe_agent_commented_on_pr = False
            try:
                from datetime import datetime

                def _parse_ts(value: str | None) -> datetime | None:
                    if not isinstance(value, str) or not value:
                        return None
                    try:
                        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
                    except (ValueError, TypeError, AttributeError):
                        return None
                    return dt if dt.tzinfo is not None else dt.replace(tzinfo=UTC)

                issue_events = self.list_pr_issue_events(pr_number)
                issue_comments = self.list_issue_comments(pr_number)
                started_events = [e for e in issue_events if e.event == COPILOT_SESSION_EVENT_STARTED]

                review_submitted_at = _parse_ts(review.submitted_at) if review.submitted_at else None
                if review_submitted_at is not None:
                    swe_session_started_after_review = any(
                        (event_ts := _parse_ts(e.created_at)) is not None and event_ts > review_submitted_at
                        for e in started_events
                    )
                    swe_agent_commented_on_pr = any(
                        c.author in COPILOT_COMMENT_LOGINS
                        and (comment_ts := _parse_ts(c.created_at)) is not None
                        and comment_ts > review_submitted_at
                        for c in issue_comments
                    )
                else:
                    # No review timestamp available — cannot reliably correlate.
                    # Keep session flag False (fail closed) and retain the broad comment signal for logging/debug.
                    swe_session_started_after_review = False
                    swe_agent_commented_on_pr = any(c.author in COPILOT_COMMENT_LOGINS for c in issue_comments)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning(
                    "Failed to compute SWE agent context flags for PR #%d: %s",
                    pr_number,
                    exc,
                )
            sdk_verdicts = self._verify_comments_via_tiered_engine(
                comments_for_sdk,
                head_sha=head_sha,
                is_outdated_by_id=is_outdated_by_id,
                has_reply_by_id={
                    comment_id: has_reply for comment_id, (_is_resolved, has_reply) in thread_states.items()
                },
                latest_thread_comment_body_by_id=latest_thread_comment_body_by_id,
                latest_thread_comment_author_login_by_id=latest_thread_comment_author_login_by_id,
                tier_results_out=tier_results_by_comment_id,
                swe_session_started_after_review=swe_session_started_after_review,
                swe_agent_commented_on_pr=swe_agent_commented_on_pr,
            )
            for comment, _context in comments_for_sdk:
                verdict = sdk_verdicts.get(comment.id, VerificationVerdict.COMMENT_UNRESOLVE)
                tier_result = tier_results_by_comment_id.get(comment.id)
                if tier_result is None and comment.id not in sdk_verdicts:
                    # Engine returned no result and no verdict was produced for
                    # this comment. Construct a fallback result and resolve by
                    # default since HEAD has changed.
                    logger.warning(
                        "Comment %d on PR #%d: tier evaluation produced no result — "
                        "resolving by default with unconfirmed marker",
                        comment.id,
                        pr_number,
                    )
                    tier_result = TierResult(
                        verdict=ResolutionVerdict.RESOLVE,
                        confidence="low",
                        tier_name="engine_fallback",
                        explanation="SDK evaluation could not produce a verdict "
                        "— resolved by default due to HEAD change.",
                    )
                    verdict = VerificationVerdict.COMMENT_RESOLVE
                elif (
                    verdict == VerificationVerdict.COMMENT_RESOLVE
                    and tier_result is not None
                    and tier_result.verdict == ResolutionVerdict.TENTATIVE
                ):
                    # Resolve-by-default outcomes should bypass tentative lifecycle
                    # persistence/replies. Keep an explicit engine_fallback marker
                    # so the thread can be re-evaluated later.
                    tier_result = TierResult(
                        verdict=ResolutionVerdict.RESOLVE,
                        confidence=tier_result.confidence,
                        tier_name="engine_fallback",
                        explanation=tier_result.explanation,
                    )
                if tier_result is not None:
                    if state_dir is None:
                        state_dir = self._resolution_state_dir()
                    thread_id = str(comment.id)
                    if tier_result.verdict == ResolutionVerdict.TENTATIVE:
                        state = load_resolution_state(thread_id, state_dir)
                        if state is not None and state.verdict == ResolutionVerdict.ABANDONED:
                            # Thread was previously abandoned; do not re-enter the lifecycle.
                            # Retry posting the abandoned reply if it was not posted previously.
                            if comment.id not in abandoned_reply_parent_comment_ids:
                                self._reply_to_review_comment(
                                    pr_number,
                                    comment.id,
                                    body=reply_formatter.format_abandoned_reply(),
                                )
                        else:
                            is_new_state = state is None
                            if state is None:
                                state = ThreadResolutionState(
                                    thread_id=thread_id,
                                    verdict=ResolutionVerdict.TENTATIVE,
                                    tier_name=tier_result.tier_name,
                                    confidence=tier_result.confidence,
                                )
                                save_resolution_state(state, state_dir)
                            else:
                                state.verdict = ResolutionVerdict.TENTATIVE
                                state.tier_name = tier_result.tier_name
                                state.confidence = tier_result.confidence
                                state = increment_iteration(state, state_dir)
                            if is_tentative_expired(state):
                                mark_abandoned(thread_id, state_dir)
                                if comment.id not in abandoned_reply_parent_comment_ids:
                                    self._reply_to_review_comment(
                                        pr_number,
                                        comment.id,
                                        body=reply_formatter.format_abandoned_reply(),
                                    )
                            elif is_new_state and not self._has_existing_addressed_reply(
                                pr_number, comment.id, addressed_reply_parent_comment_ids
                            ):
                                self._reply_to_review_comment(
                                    pr_number,
                                    comment.id,
                                    body=reply_formatter.build_full_reply(
                                        tier_result,
                                        model_id=self._model_id_for_tier_result(tier_result),
                                    ),
                                )
                    else:
                        clear_resolution_state(thread_id, state_dir)
                if verdict == VerificationVerdict.COMMENT_RESOLVE:
                    if tier_result is not None and "fallback" in (tier_result.tier_name or ""):
                        has_unconfirmed_resolution = True
                    resolved_ids.append(comment.id)
                    has_existing_addressed_reply = self._has_existing_addressed_reply(
                        pr_number, comment.id, addressed_reply_parent_comment_ids
                    )
                    post_confirmation_reply = (
                        comment.id in reevaluated_unconfirmed_comment_ids
                        and tier_result is not None
                        and "fallback" not in (tier_result.tier_name or "")
                    )
                    if post_confirmation_reply or not has_existing_addressed_reply:
                        # Resolution reply format selection:
                        # ┌─ "fallback" in tier_name → format_unconfirmed_commit_change_reply()
                        # ├─ post_confirmation_reply (re-eval) → build_full_reply()
                        # ├─ tier_result available (normal) → build_full_reply()
                        # └─ tier_result is None → static fallback text
                        # All cases append HEAD commit link when head_sha is available.
                        if tier_result is not None and "fallback" in (tier_result.tier_name or ""):
                            reply_body = reply_formatter.format_unconfirmed_commit_change_reply(
                                tier_result,
                                model_id=self._model_id_for_tier_result(tier_result),
                            )
                        elif tier_result is not None:
                            reply_body = reply_formatter.build_full_reply(
                                tier_result,
                                model_id=self._model_id_for_tier_result(tier_result),
                            )
                        else:
                            reply_body = _ADDRESSED_REPLY_BODY
                        reply_body += self._build_head_commit_line(head_sha, repo)
                        self._reply_to_review_comment(pr_number, comment.id, body=reply_body)
                    resolutions.append(CommentResolution(comment_id=comment.id, verdict=verdict))
                else:
                    if (
                        verdict == VerificationVerdict.COMMENT_UNRESOLVE
                        and tier_result is not None
                        and tier_result.verdict == ResolutionVerdict.UNRESOLVE
                        and comment.id not in unresolve_reply_parent_comment_ids
                    ):
                        self._reply_to_review_comment(
                            pr_number,
                            comment.id,
                            body=reply_formatter.build_full_reply(
                                tier_result,
                                model_id=self._model_id_for_tier_result(tier_result),
                            ),
                        )
                    if (
                        verdict == VerificationVerdict.COMMENT_UNRESOLVE
                        and comment.id in reevaluated_unconfirmed_comment_ids
                    ):
                        unconfirmed_unresolve_ids.append(comment.id)
                    resolutions.append(CommentResolution(comment_id=comment.id, verdict=verdict))

        # Unresolve threads that were previously resolved with the unconfirmed marker
        # but are now vetoed by the SDK on re-evaluation
        if unconfirmed_unresolve_ids:
            unresolve_result = _unresolve_review_threads(
                pr_number,
                repo,
                comment_ids=sorted(unconfirmed_unresolve_ids),
            )
            if not bool(unresolve_result.get("verified", False)):
                errors.append("thread_unresolve_unverified")
            threads_failed = int(unresolve_result.get("threadsFailed", 0) or 0)
            if threads_failed > 0:
                errors.append(f"thread_unresolve_failed:{threads_failed}")

        # Resolve threads only for comments that were verified as addressed
        if resolved_ids:
            resolve_result = _resolve_review_threads(pr_number, repo, comment_ids=sorted(resolved_ids))
            details_by_comment_id: dict[int, dict[str, Any]] = {
                int(detail["commentId"]): detail
                for detail in resolve_result.get("details", [])
                if detail.get("commentId") is not None
            }
            updated_resolutions: list[CommentResolution] = []
            for resolution in resolutions:
                detail = details_by_comment_id.get(resolution.comment_id)
                thread_id = (
                    str(detail.get("threadId"))
                    if detail is not None and detail.get("threadId") is not None
                    else resolution.thread_id
                )
                error = resolution.error
                if resolution.verdict == VerificationVerdict.COMMENT_RESOLVE:
                    if detail is None:
                        error = "thread_resolution_missing"
                    else:
                        status = str(detail.get("status", ""))
                        if status not in {"resolved", "already_resolved"}:
                            error = str(detail.get("error") or f"thread_{status or 'unknown'}")
                updated_resolutions.append(
                    CommentResolution(
                        comment_id=resolution.comment_id,
                        thread_id=thread_id,
                        verdict=resolution.verdict,
                        error=error,
                    )
                )
            resolutions = updated_resolutions
            if not bool(resolve_result.get("verified", False)):
                errors.append("thread_resolution_unverified")
            threads_failed = int(resolve_result.get("threadsFailed", 0) or 0)
            if threads_failed > 0:
                errors.append(f"thread_resolution_failed:{threads_failed}")

        # Invalidate the thread-signals cache AFTER the resolve/unresolve mutations.
        # The pop at the top of this method only clears state captured before this
        # run; the pre-filter read above refills the cache with pre-resolution
        # state. Without this second pop, a later read on the same provider
        # instance (e.g. the post-invalidation snapshot refresh) would hit that
        # stale map and re-count just-resolved threads as unresolved.
        self._thread_signals_cache.pop(pr_number, None)
        self._thread_identity_cache.pop(pr_number, None)

        errors.extend(
            f"comment_{resolution.comment_id}:{resolution.error}" for resolution in resolutions if resolution.error
        )
        resolved_count = sum(
            1
            for resolution in resolutions
            if resolution.verdict == VerificationVerdict.COMMENT_RESOLVE and not resolution.error
        )
        unresolved_count = sum(
            1
            for resolution in resolutions
            if resolution.comment_id >= 0
            and (resolution.verdict != VerificationVerdict.COMMENT_RESOLVE or bool(resolution.error))
        )
        # Synthetic suppressed entries parsed out of a review body carry negative
        # sentinel IDs and have no GitHub thread, so they can never be pre-filtered
        # or resolved. Counting them as unresolved made the blocking thread count
        # grow without bound; report them separately instead. Sentinel IDs restart
        # at -1 for every review and therefore collide across reviews, so they must
        # be excluded rather than de-duplicated by ID.
        suppressed_count = sum(1 for resolution in resolutions if resolution.comment_id < 0)
        reason = "verified" if not errors else "verified_with_resolution_errors"

        result = FinalizationResult(
            skipped=False,
            reason=reason,
            resolved_count=resolved_count,
            unresolved_count=unresolved_count,
            suppressed_count=suppressed_count,
            resolutions=tuple(resolutions),
            errors=tuple(errors),
        )
        if (
            result.unresolved_count == 0
            and not result.errors
            and not has_unconfirmed_resolution
            and unconfirmed_reevaluation_complete
        ):
            finalization_state_store.mark_terminal(key=review_key, reason=result.reason)
        logger.info(
            "Finalization complete for PR #%d review %d: %d resolved, %d unresolved, %d suppressed",
            pr_number,
            review_id,
            result.resolved_count,
            result.unresolved_count,
            result.suppressed_count,
        )
        return result

    def _build_verification_context_diff(self, review_commit_sha: str, head_sha: str) -> str:
        """Fetch the diff between the review commit and HEAD for verification context.

        Returns the diff as a string, truncated to a 4000-token budget
        (approx 16000 chars using 4 chars/token heuristic).
        """
        max_chars = 16000
        try:
            result = run_safe(
                ["git", "diff", f"{review_commit_sha}..{head_sha}"],
                capture_output=True,
                text=True,
                shell=False,
            )
            diff = result.stdout if result.returncode == 0 else ""
        except Exception as exc:
            logger.warning("Failed to get diff for verification context: %s", exc)
            diff = ""

        if len(diff) > max_chars:
            diff = diff[:max_chars]
        return diff

    def _build_comment_verification_context(self, comment: ReviewCommentInfo, full_diff: str) -> str:
        """Build verification context for a specific comment.

        For line-anchored comments, extracts relevant portion of the diff.
        Falls back to diff_hunk when the file section cannot be found in the diff
        (e.g. no changes for that file, rename/copy, or path mismatch).
        For PR-level comments (no path), uses the full diff (already truncated).
        """
        if comment.path:
            target_header = f"diff --git a/{comment.path} b/{comment.path}"
            # Extract the section of the diff for this file
            lines = full_diff.split("\n")
            file_diff_lines: list[str] = []
            in_file = False
            for line in lines:
                if line == target_header:
                    in_file = True
                    file_diff_lines = [line]
                elif line.startswith("diff --git") and in_file:
                    break
                elif in_file:
                    file_diff_lines.append(line)
            if file_diff_lines:
                file_diff = "\n".join(file_diff_lines)
                if len(file_diff) > 4000:
                    return file_diff[:4000]
                return file_diff
            # File section not found — fall back to the original diff_hunk so the SDK
            # sees scoped context instead of unrelated changes from other files.
            # If no hunk is available, return empty context so verification defaults
            # to COMMENT_UNRESOLVE via the existing fail-safe path.
            return comment.diff_hunk

        if full_diff:
            return full_diff

        return comment.diff_hunk

    def _build_comment_verification_prompt(self, comment_body: str, diff_context: str) -> str:
        return (
            "You are a code review verification assistant. Your task is to determine whether "
            "a review comment has been addressed by the code changes in the diff.\n\n"
            "## Review Comment\n"
            f"{comment_body}\n\n"
            "## Diff (changes made since the review)\n"
            f"```diff\n{diff_context}\n```\n\n"
            "## Instructions\n"
            "Respond with EXACTLY one of these two values (nothing else):\n"
            "- COMMENT_RESOLVE — if the diff addresses the review comment\n"
            "- COMMENT_UNRESOLVE — if the diff does NOT address the review comment\n"
        )

    def _verify_comments_via_tiered_engine(
        self,
        comments: list[tuple[ReviewCommentInfo, str]],
        *,
        head_sha: str,
        is_outdated_by_id: dict[int, bool | None] | None = None,
        has_reply_by_id: dict[int, bool] | None = None,
        latest_thread_comment_body_by_id: dict[int, str] | None = None,
        latest_thread_comment_author_login_by_id: dict[int, str | None] | None = None,
        tier_results_out: dict[int, TierResult] | None = None,
        swe_session_started_after_review: bool = False,
        swe_agent_commented_on_pr: bool = False,
    ) -> dict[int, VerificationVerdict]:
        """Verify comments through the tiered resolution engine."""

        from agentic_devtools.cli.ci.resolution.tiers.diff_heuristic import DiffHeuristicTier
        from agentic_devtools.cli.ci.resolution.tiers.swe_agent_reply import SweAgentReplyTier
        from agentic_devtools.cli.ci.resolution.tiers.thread_evaluated import ThreadEvaluatedTier

        engine = TieredResolutionEngine(
            cast(
                list[EvaluationTier],
                [
                    OutdatedTier(),
                    AutomationMarkerTier(),
                    SweAgentReplyTier(),
                    ThreadEvaluatedTier(),
                    DiffHeuristicTier(),
                    SdkEvaluationTier(
                        sdk_caller=self._run_prompt_via_sdk,
                        fallback_caller=self._run_prompt_via_sdk_fallback,
                    ),
                ],
            )
        )

        verdicts: dict[int, VerificationVerdict] = {}
        for comment, diff_context in comments:
            # FR-003 guard: if the comment was originally placed on what is now the
            # current HEAD commit (i.e., no commits have been pushed since the comment
            # was posted), there are no newer changes to evaluate against — skip tier
            # evaluation. Use original_commit_id (the commit when the comment was first
            # posted) rather than commit_id, which GitHub may remap to HEAD after a
            # squash/force-push.
            effective_commit_id = comment.original_commit_id or comment.commit_id
            if effective_commit_id and effective_commit_id == head_sha:
                verdicts[comment.id] = VerificationVerdict.COMMENT_UNRESOLVE
                continue
            latest_thread_comment_body = (
                latest_thread_comment_body_by_id.get(comment.id)
                if latest_thread_comment_body_by_id is not None
                else None
            )
            latest_thread_comment_author_login = (
                latest_thread_comment_author_login_by_id.get(comment.id)
                if latest_thread_comment_author_login_by_id is not None
                else None
            )
            has_reply = has_reply_by_id.get(comment.id, False) if has_reply_by_id is not None else False
            thread_comments = [
                GitHubThreadComment(
                    body=comment.body,
                    created_at="",
                    author_login=None,
                    database_id=comment.id,
                )
            ]
            if latest_thread_comment_body and has_reply:
                thread_comments.append(
                    GitHubThreadComment(
                        body=latest_thread_comment_body,
                        created_at="",
                        author_login=latest_thread_comment_author_login,
                        database_id=None,
                    )
                )
            thread = GitHubReviewThread(
                thread_id=str(comment.id),
                file_path=comment.path or None,
                start_line=comment.start_line or comment.line,
                end_line=comment.end_line or comment.line,
                is_outdated=is_outdated_by_id.get(comment.id) if is_outdated_by_id is not None else None,
                comments=thread_comments,
                originating_review_commit_oid=comment.commit_id,
            )
            context = GitHubResolutionContext(
                diff_text=diff_context,
                head_commit_oid=head_sha,
                swe_session_started_after_review=swe_session_started_after_review,
                swe_agent_commented_on_pr=swe_agent_commented_on_pr,
            )
            result = engine.evaluate_thread(cast(ReviewThread, thread), cast(ResolutionContext, context))
            if tier_results_out is not None:
                tier_results_out[comment.id] = result
            if result.verdict == ResolutionVerdict.RESOLVE:
                verdicts[comment.id] = VerificationVerdict.COMMENT_RESOLVE
            elif result.verdict == ResolutionVerdict.UNRESOLVE:
                verdicts[comment.id] = VerificationVerdict.COMMENT_UNRESOLVE
            elif result.verdict == ResolutionVerdict.TENTATIVE:
                verdicts[comment.id] = VerificationVerdict.COMMENT_RESOLVE
            else:  # pragma: no cover - exhaustive guard for future enum extension
                raise ValueError(f"Unsupported resolution verdict: {result.verdict}")
            logger.debug(
                "Comment %d: tier verdict %s → verification %s (tier=%s)",
                comment.id,
                result.verdict.value,
                verdicts[comment.id].value,
                result.tier_name,
            )
        return verdicts

    def _verify_comments_via_sdk(  # pragma: no cover - optional runtime SDK integration
        self,
        comments: list[tuple[int, str, str]] | list[tuple[ReviewCommentInfo, str]],
        timeout_seconds: int = 60,
        *,
        head_sha: str | None = None,
    ) -> dict[int, VerificationVerdict]:
        """Verify multiple comments in one SDK session to reduce startup overhead."""
        if not comments:
            return {}

        normalized_comments: list[tuple[ReviewCommentInfo, str]] = []
        for item in comments:
            if isinstance(item[0], ReviewCommentInfo):
                comment, diff_context = item
                normalized_comments.append((comment, diff_context))
            else:
                comment_id, comment_body, diff_context = item
                normalized_comments.append(
                    (
                        ReviewCommentInfo(
                            id=comment_id,
                            path="",
                            body=comment_body,
                            html_url="",
                        ),
                        diff_context,
                    )
                )

        if head_sha:
            return self._verify_comments_via_tiered_engine(normalized_comments, head_sha=head_sha)

        token = os.environ.get("COPILOT_GITHUB_TOKEN", "").strip()
        if not token:
            logger.warning("COPILOT_GITHUB_TOKEN not set — defaulting to COMMENT_UNRESOLVE (fail-safe)")
            return {comment.id: VerificationVerdict.COMMENT_UNRESOLVE for comment, _diff_context in normalized_comments}

        try:
            from copilot import CopilotClient
            from copilot.session import PermissionHandler
        except Exception as exc:
            logger.warning(
                "Copilot SDK unavailable for comment verification: %s",
                exc,
            )
            return {comment.id: VerificationVerdict.COMMENT_UNRESOLVE for comment, _diff_context in normalized_comments}

        model = os.environ.get("COPILOT_MODEL", "claude-opus-4.6")

        async def _run() -> dict[int, VerificationVerdict]:
            client = None
            session = None
            try:
                client = CopilotClient(github_token=token)
                await client.start()
                try:
                    session = await client.create_session(
                        model=model,
                        on_permission_request=PermissionHandler.approve_all,
                        infinite_sessions={"enabled": False},
                        github_token=token,
                    )
                except TypeError as exc:
                    if "unexpected keyword argument" not in str(exc) or "github_token" not in str(exc):
                        raise
                    session = await client.create_session(
                        model=model,
                        on_permission_request=PermissionHandler.approve_all,
                        infinite_sessions={"enabled": False},
                    )

                current_content_parts: list[str] | None = None
                current_done: asyncio.Event | None = None

                def on_event(event: Any) -> None:
                    if current_content_parts is None or current_done is None:
                        return
                    event_type = getattr(getattr(event, "type", None), "value", "")
                    if event_type == "assistant.message":
                        current_content_parts.append(getattr(getattr(event, "data", None), "content", ""))
                    elif event_type in {"session.idle", "error", "session.error", "assistant.error"}:
                        current_done.set()

                session.on(on_event)

                verdicts: dict[int, VerificationVerdict] = {}
                for comment, diff_context in normalized_comments:
                    comment_id = comment.id
                    comment_body = comment.body
                    if not diff_context:
                        logger.warning("Empty diff context — defaulting to COMMENT_UNRESOLVE")
                        verdicts[comment_id] = VerificationVerdict.COMMENT_UNRESOLVE
                        continue

                    current_content_parts = []
                    current_done = asyncio.Event()
                    prompt = self._build_comment_verification_prompt(comment_body, diff_context)
                    await session.send(prompt)
                    try:
                        await asyncio.wait_for(current_done.wait(), timeout=timeout_seconds)
                    except TimeoutError:
                        logger.warning(
                            "Copilot SDK comment verification timed out after %ds for comment %d",
                            timeout_seconds,
                            comment_id,
                        )
                        verdicts[comment_id] = VerificationVerdict.COMMENT_UNRESOLVE
                        continue

                    raw = (current_content_parts[-1] if current_content_parts else "").strip()
                    if "COMMENT_RESOLVE" in raw and "COMMENT_UNRESOLVE" not in raw:
                        verdicts[comment_id] = VerificationVerdict.COMMENT_RESOLVE
                    else:
                        verdicts[comment_id] = VerificationVerdict.COMMENT_UNRESOLVE
                return verdicts
            finally:
                if session is not None:
                    try:
                        await session.disconnect()
                    except Exception:
                        pass
                if client is not None:
                    try:
                        await client.stop()
                    except Exception:
                        pass

        total_timeout = timeout_seconds * len(normalized_comments)
        try:
            return asyncio.run(asyncio.wait_for(_run(), timeout=total_timeout))
        except TimeoutError:
            logger.warning("Copilot SDK comment batch verification timed out after %ds", total_timeout)
            return {comment.id: VerificationVerdict.COMMENT_UNRESOLVE for comment, _diff_context in normalized_comments}
        except Exception as exc:
            logger.warning("Copilot SDK comment batch verification failed: %s", exc)
            return {comment.id: VerificationVerdict.COMMENT_UNRESOLVE for comment, _diff_context in normalized_comments}

    def _run_prompt_via_sdk_fallback(self, prompt: str, timeout_seconds: int = 60) -> str:
        """Run a single prompt via fallback model."""
        return self._run_prompt_via_sdk(
            prompt,
            timeout_seconds=timeout_seconds,
            model=os.environ.get("COPILOT_FALLBACK_MODEL", "claude-sonnet-4.6"),
        )

    def _run_prompt_via_sdk(
        self,
        prompt: str,
        timeout_seconds: int = 60,
        *,
        model: str | None = None,
    ) -> str:
        """Run a single prompt via Copilot SDK and return raw assistant output."""
        token = os.environ.get("COPILOT_GITHUB_TOKEN", "").strip()
        if not token:
            raise RuntimeError("COPILOT_GITHUB_TOKEN not set")

        try:
            from copilot import CopilotClient
            from copilot.session import PermissionHandler
        except Exception as exc:
            error = exc
            raise RuntimeError(f"Copilot SDK unavailable: {error}") from error

        selected_model = model or os.environ.get("COPILOT_MODEL", "claude-opus-4.6")

        async def _run() -> str:  # pragma: no cover - optional runtime SDK integration
            client = None
            session = None
            content_parts: list[str] = []
            error_messages: list[str] = []
            done = asyncio.Event()

            try:
                client = CopilotClient(github_token=token)
                await client.start()
                try:
                    session = await client.create_session(
                        model=selected_model,
                        on_permission_request=PermissionHandler.approve_all,
                        infinite_sessions={"enabled": False},
                        github_token=token,
                    )
                except TypeError as exc:
                    if "unexpected keyword argument" not in str(exc) or "github_token" not in str(exc):
                        raise
                    session = await client.create_session(
                        model=selected_model,
                        on_permission_request=PermissionHandler.approve_all,
                        infinite_sessions={"enabled": False},
                    )

                from typing import Any as _Any

                def on_event(event: _Any) -> None:
                    event_type = getattr(getattr(event, "type", None), "value", "")
                    if event_type == "assistant.message":
                        content_parts.append(getattr(getattr(event, "data", None), "content", ""))
                    elif event_type == "session.idle":
                        done.set()
                    elif event_type in {"error", "session.error", "assistant.error"}:
                        msg = getattr(getattr(event, "data", None), "message", None) or str(getattr(event, "data", ""))
                        error_messages.append(f"{event_type}: {msg}")
                        done.set()

                session.on(on_event)
                await session.send(prompt)
                await asyncio.wait_for(done.wait(), timeout=timeout_seconds)

                if error_messages:
                    raise RuntimeError("; ".join(error_messages))

                raw = (content_parts[-1] if content_parts else "").strip()
                if not raw:
                    raise RuntimeError("empty SDK response")
                return raw
            finally:
                if session is not None:
                    try:
                        await session.disconnect()
                    except Exception:
                        pass
                if client is not None:
                    try:
                        await client.stop()
                    except Exception:
                        pass

        try:
            return asyncio.run(asyncio.wait_for(_run(), timeout=timeout_seconds))
        except TimeoutError as exc:  # pragma: no cover
            raise RuntimeError(f"Copilot SDK prompt timed out after {timeout_seconds}s") from exc
        except RuntimeError:
            raise
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Copilot SDK prompt failed: {exc}") from exc

    def _verify_comment_via_sdk(
        self,
        comment_body: str,
        diff_context: str,
        timeout_seconds: int = 60,
    ) -> VerificationVerdict:
        """Verify whether a review comment has been addressed by the diff via Copilot SDK.

        Returns COMMENT_RESOLVE if addressed, COMMENT_UNRESOLVE otherwise.
        Defaults to COMMENT_UNRESOLVE on any error (fail-safe).
        """
        if not diff_context:
            logger.warning("Empty diff context — defaulting to COMMENT_UNRESOLVE")
            return VerificationVerdict.COMMENT_UNRESOLVE

        prompt = self._build_comment_verification_prompt(comment_body, diff_context)
        try:
            raw = self._run_prompt_via_sdk(prompt, timeout_seconds=timeout_seconds)
        except RuntimeError as exc:
            logger.warning("Copilot SDK comment verification failed: %s", exc)
            return VerificationVerdict.COMMENT_UNRESOLVE

        if "COMMENT_RESOLVE" in raw and "COMMENT_UNRESOLVE" not in raw:
            return VerificationVerdict.COMMENT_RESOLVE
        return VerificationVerdict.COMMENT_UNRESOLVE

    def squash_post_repair(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
    ) -> SquashResult:
        """Squash post-repair commits into a single clean commit.

        Responsible strictly for commit hygiene — converting multiple commits
        into a single well-formed commit via soft reset + commit, rebase, and force-push.

        Review requests are handled explicitly by ``RequestReviewAction`` in the
        pipeline after squash completes; this method does NOT trigger or request
        reviews.

        Called by squash workflows (pipeline SquashAction and squash-wait
        finalization) after verifying preconditions.

        Returns:
            SquashResult recording the pre-squash tree (of ``head_sha``, which
            carried the pre-squash CI result) and the post-squash tree (of the
            final force-pushed HEAD). Callers compare the two to verify the
            squash preserved the tree before reusing the pre-squash CI result.
        """
        # 0. Capture the pre-squash tree of ``head_sha`` (the commit whose CI
        #    result the caller may want to reuse). Fetch it first since the local
        #    checkout may be stale. Resolution failures are non-fatal — an empty
        #    tree simply means the caller cannot prove tree preservation.
        before_tree = self._resolve_tree_sha(head_sha, fetch=True)

        # 1. Squash and force-push
        self._squash_and_force_push(base_branch=base_branch, head_branch=head_branch, head_sha=head_sha)

        # 1b. Guard against the race where Copilot SWE agent pushes another
        #     commit during finalization — re-fetch and hard-reset to remote
        #     head branch before re-checking commit count.
        self._squash_and_force_push(
            base_branch=base_branch,
            head_branch=head_branch,
            head_sha=head_sha,
            reset_to_remote=True,
        )

        # 1c. Capture the actual post-squash tree and commit SHA of the final
        #     force-pushed HEAD. The commit SHA is needed by the runner to verify
        #     that the refreshed snapshot still points to the squashed commit.
        after_tree = self._resolve_tree_sha("HEAD")
        after_sha = self._resolve_commit_sha("HEAD")

        # 2. Ensure PR is published if still draft (edge-case safety)
        pr_meta = self.get_pr_metadata(pr_number)
        if pr_meta.is_draft:
            self.publish_pr(pr_number)

        return SquashResult(before_tree=before_tree, after_tree=after_tree, after_sha=after_sha)

    def _resolve_tree_sha(self, ref: str, *, fetch: bool = False) -> str:
        """Resolve the git tree SHA for ``ref`` (e.g. a commit SHA or ``HEAD``).

        When ``fetch`` is True, first fetches ``ref`` from origin so that a
        commit SHA not present in the local clone can still be resolved.
        Returns an empty string when the tree cannot be resolved.
        """
        try:
            if fetch:
                self._run_git(["fetch", "origin", ref])
            return self._run_git(["rev-parse", f"{ref}^{{tree}}"]).strip()
        except RuntimeError as exc:
            logger.warning("Could not resolve tree SHA for %s: %s", ref, exc)
            return ""

    def _resolve_commit_sha(self, ref: str) -> str:
        """Resolve the full commit SHA for ``ref`` (e.g. ``HEAD``).

        Returns an empty string when the commit cannot be resolved.
        """
        try:
            return self._run_git(["rev-parse", ref]).strip()
        except RuntimeError as exc:
            logger.warning("Could not resolve commit SHA for %s: %s", ref, exc)
            return ""

    @retry_with_backoff()
    def list_workflow_runs(
        self,
        workflow_id: str,
        *,
        window_hours: int = 24,
        status: str | None = "completed",
        include_dispatch_inputs: bool = False,
        max_dispatch_enrichments: int | None = None,
    ) -> list[WorkflowRun]:
        """List recent workflow runs for a workflow.

        Queries the GitHub Actions API for runs within the specified time
        window, paginating through all results.

        Args:
            workflow_id: Workflow file name or numeric ID.
            window_hours: How far back to look for runs (in hours).
            status: Filter runs by status (e.g. ``"completed"``). Pass
                ``None`` to omit the status filter and include in-progress
                and queued runs as well. Defaults to ``"completed"`` to
                preserve backward-compatible behaviour for all existing
                callers.
            include_dispatch_inputs: When ``True``, fetch each
                ``workflow_dispatch`` run's details and parse
                ``inputs.pr_number`` when ``pull_requests[]`` is empty.
            max_dispatch_enrichments: Maximum number of ``workflow_dispatch``
                detail lookups to perform when ``include_dispatch_inputs`` is
                ``True``.  ``None`` (default) means no limit; pass a positive
                integer to bound the N+1 REST calls and protect API quota.

        Returns:
            List of WorkflowRun instances.
        """
        from datetime import datetime, timedelta

        from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun

        cutoff = datetime.now(UTC) - timedelta(hours=window_hours)
        cutoff_str = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")

        status_param = f"status={quote(status, safe='')}&" if status is not None else ""

        runs: list[WorkflowRun] = []
        page = 1
        dispatch_enrichments = 0
        while True:
            endpoint = self._repo_api(
                f"/actions/workflows/{quote(workflow_id, safe='')}/runs"
                f"?{status_param}per_page=100&page={page}&created=%3E%3D{cutoff_str}"
            )
            response = _gh_api(endpoint)
            data = json.loads(response)
            page_runs = data.get("workflow_runs", [])
            if not page_runs:
                break

            for r in page_runs:
                pull_requests = r.get("pull_requests") or []
                first_pr = pull_requests[0] if pull_requests and isinstance(pull_requests[0], dict) else None
                pr_number = first_pr.get("number", 0) if first_pr else 0
                run_id_raw = r.get("id")
                run_id = run_id_raw if isinstance(run_id_raw, int) else 0
                if include_dispatch_inputs and pr_number <= 0 and r.get("event") == "workflow_dispatch" and run_id > 0:
                    if max_dispatch_enrichments is None or dispatch_enrichments < max_dispatch_enrichments:
                        try:
                            run_detail_raw = _gh_api(self._repo_api(f"/actions/runs/{run_id}"))
                            run_detail = json.loads(run_detail_raw)
                            pr_number = _parse_inputs_pr_number(run_detail.get("inputs"))
                            dispatch_enrichments += 1
                        except Exception as exc:
                            raise RuntimeError(f"dispatch detail lookup for run {run_id} failed: {exc}") from exc
                runs.append(
                    WorkflowRun(
                        id=run_id,
                        name=r.get("display_title", "") or r.get("name", ""),
                        conclusion=r.get("conclusion") or "",
                        run_attempt=r.get("run_attempt", 1),
                        created_at=r.get("created_at", ""),
                        event=r.get("event", ""),
                        head_branch=r.get("head_branch", ""),
                        html_url=r.get("html_url", ""),
                        triggering_actor=r.get("triggering_actor", {}).get("login", "")
                        if isinstance(r.get("triggering_actor"), dict)
                        else "",
                        repository_full_name=r.get("repository", {}).get("full_name", "")
                        if isinstance(r.get("repository"), dict)
                        else "",
                        pr_number=pr_number,
                    )
                )

            # If the page returned fewer than 100 results, we've reached the last page.
            if len(page_runs) < 100:
                break
            page += 1

        return runs

    @retry_with_backoff()
    def rerun_workflow(self, run_id: int) -> None:
        """Trigger a re-run of all jobs for the given workflow run.

        Args:
            run_id: The workflow run ID to re-run.

        Raises:
            RuntimeError: If the re-run API call fails.
        """
        endpoint = self._repo_api(f"/actions/runs/{run_id}/rerun")
        _gh_api(endpoint, method="POST")

    # --- Scheduler-related methods (round-robin PR dispatch) ---

    @retry_with_backoff()
    def list_eligible_prs(self, max_prs: int | None = None) -> list[EligiblePR]:
        """List eligible PRs via GraphQL, filtering out forks/ignored/human-blocked.

        Each returned PR is enriched with ``labels_to_propagate`` — the allowlisted
        labels carried by the PR's ``closingIssuesReferences`` (linked issues) that
        the PR itself does not yet have. Those labels also count towards the
        auto-merge signal, so a PR whose linked issue allows auto-merge is not
        classified as human-blocked.

        Returns:
            Sorted list (oldest-first) of EligiblePR dataclasses.
        """
        return self._list_pr_inventory(max_prs, exclude_human_blocked=True, exclude_audit_handoff=True)

    def list_supervisor_prs(self, max_prs: int | None = None) -> list[EligiblePR]:
        """List supervisor PR inventory, excluding only forks and ignored PRs.

        The report-only supervisor must classify human-blocked and audit-handoff
        PRs explicitly, so this listing avoids those scheduler-only exclusions.
        """
        return self._list_pr_inventory(max_prs, exclude_human_blocked=False, exclude_audit_handoff=False)

    def _list_pr_inventory(
        self,
        max_prs: int | None,
        *,
        exclude_human_blocked: bool,
        exclude_audit_handoff: bool,
    ) -> list[EligiblePR]:
        from agentic_devtools.cli.ci.scheduler import (
            AUDIT_EVAL_BRANCH_SUBSTR,
            AUTO_MERGE_LABEL,
            SKIP_LABEL,
            filter_eligible_prs,
            select_labels_to_propagate,
        )

        repo = self._resolve_repo()
        owner, repo_name = repo.split("/", 1)

        # Fetch open PRs via GraphQL (paginated)
        eligible_prs: list[EligiblePR] = []
        effective_max = max_prs if isinstance(max_prs, int) and max_prs > 0 else None
        end_cursor: str | None = None
        for _ in range(_MAX_PR_PAGES):
            variables: dict[str, Any] = {"owner": owner, "name": repo_name}
            if end_cursor:
                variables["endCursor"] = end_cursor
                query = _ELIGIBLE_PRS_QUERY_WITH_CURSOR
            else:
                query = _ELIGIBLE_PRS_QUERY

            response_metadata: dict[str, float | int | None] = {}
            response = _gh_api(
                "/graphql",
                method="POST",
                body={"query": query, "variables": variables},
                response_metadata=response_metadata,
            )
            data = json.loads(response)
            retry_after_raw = response_metadata.get("retry_after")
            reset_timestamp_raw = response_metadata.get("reset_timestamp")
            remaining_raw = response_metadata.get("remaining")
            _raise_for_graphql_errors(
                data,
                context="Eligible PR GraphQL query failed",
                provider="github",
                credential_identity=_credential_identity_for_token(None),
                retry_after=float(retry_after_raw) if isinstance(retry_after_raw, (int, float)) else None,
                reset_timestamp=float(reset_timestamp_raw) if isinstance(reset_timestamp_raw, (int, float)) else None,
                remaining=int(remaining_raw) if isinstance(remaining_raw, int) else None,
            )
            pr_data = data.get("data", {}).get("repository", {}).get("pullRequests", {})
            nodes = pr_data.get("nodes", [])

            for node in nodes:
                if not isinstance(node, dict):
                    continue
                raw_label_nodes = node.get("labels", {}).get("nodes", [])
                if not isinstance(raw_label_nodes, list):
                    raw_label_nodes = []
                label_nodes = [lbl for lbl in raw_label_nodes if isinstance(lbl, dict)]
                labels = [lbl.get("name", "") for lbl in label_nodes]
                pr_number = node.get("number", 0)
                if not isinstance(pr_number, int) or pr_number <= 0:
                    continue

                # Cheap in-memory filters first — skip before any REST calls
                if node.get("isCrossRepository", False):
                    continue
                if SKIP_LABEL in labels:
                    continue

                labels_to_propagate = select_labels_to_propagate(
                    labels,
                    _linked_issue_label_names(node),
                )
                head_ref_name = str(node.get("headRefName", "") or "")
                touches_audit_agent_output = False
                if exclude_audit_handoff and AUDIT_EVAL_BRANCH_SUBSTR in head_ref_name.lower():
                    try:
                        touches_audit_agent_output = self._touches_audit_agent_output(pr_number)
                    except Exception as exc:
                        if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                            raise
                        # On API failure, fail-safe: do not exclude the PR.
                        logger.warning(
                            "Failed to evaluate audit agent-output paths for PR #%d: %s",
                            pr_number,
                            exc,
                        )
                        touches_audit_agent_output = False

                is_human_blocked = False
                has_auto_merge = AUTO_MERGE_LABEL in labels or AUTO_MERGE_LABEL in labels_to_propagate
                if exclude_human_blocked and not has_auto_merge:
                    # Check if human-blocked: CI passing + approved + missing auto-merge label
                    head_sha = node.get("headRefOid", "")
                    if head_sha:
                        try:
                            is_human_blocked = self._is_human_blocked(pr_number, head_sha)
                        except Exception as exc:
                            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                                raise
                            # On API failure, fail-safe: assume NOT human-blocked
                            logger.warning(
                                "Failed to evaluate human-blocked state for PR #%d: %s",
                                pr_number,
                                exc,
                            )
                            is_human_blocked = False

                candidate = {
                    "number": pr_number,
                    "createdAt": node.get("createdAt", ""),
                    "isCrossRepository": node.get("isCrossRepository", False),
                    "headRefName": head_ref_name,
                    "head_ref": head_ref_name,
                    "labels": label_nodes,
                    "is_human_blocked": is_human_blocked,
                    "touches_audit_agent_output": touches_audit_agent_output,
                    "labels_to_propagate": labels_to_propagate,
                }
                eligible_prs.extend(
                    filter_eligible_prs(
                        [candidate],
                        exclude_human_blocked=exclude_human_blocked,
                        exclude_audit_handoff=exclude_audit_handoff,
                    )
                )
                if effective_max is not None and len(eligible_prs) >= effective_max:
                    return eligible_prs[:effective_max]

            page_info = pr_data.get("pageInfo", {})
            if not page_info.get("hasNextPage", False):
                break
            end_cursor = page_info.get("endCursor")
            if not end_cursor:
                break

        return eligible_prs

    def list_open_copilot_pr_briefs(self) -> list[dict[str, Any]]:
        """List open PRs whose head branch contains ``copilot``, oldest-first.

        Applies only the cheap head-branch prefilter via ``gh pr list``; the
        agent-output and HEAD-author gates are applied by the caller. Returns a
        list of ``{"number": int, "head_branch": str, "created_at": str}`` dicts
        sorted oldest-first by ``created_at``.
        """
        repo = self._resolve_repo()
        cmd = [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--state",
            "open",
            "--json",
            "number,headRefName,createdAt",
            "--limit",
            "200",
        ]
        result = run_safe(cmd, capture_output=True, text=True, shell=False)
        if result.returncode != 0:
            stderr = (result.stderr or "").strip()
            raise RuntimeError(f"gh pr list failed: {stderr or f'exit code {result.returncode}'}")

        try:
            nodes = json.loads(result.stdout or "[]")
        except json.JSONDecodeError as exc:
            raise RuntimeError("gh pr list returned invalid JSON output") from exc
        briefs: list[dict[str, Any]] = []
        for node in nodes:
            if not isinstance(node, dict):
                continue
            number = node.get("number")
            head = str(node.get("headRefName", "") or "")
            if isinstance(number, int) and number > 0 and "copilot" in head.lower():
                briefs.append(
                    {
                        "number": number,
                        "head_branch": head,
                        "created_at": str(node.get("createdAt", "") or ""),
                    }
                )
        # Sort oldest-first; treat missing/empty timestamps as newest so they
        # don't incorrectly jump ahead of PRs with real timestamps.
        briefs.sort(key=lambda b: b["created_at"] or "\xff\xff\xff\xff")
        return briefs

    def _touches_audit_agent_output(self, pr_number: int) -> bool:
        """Return True when a PR includes audit evaluation agent-output files."""
        from agentic_devtools.cli.ci.scheduler import (  # noqa: PLC0415
            AUDIT_AGENT_OUTPUT_PATH_PREFIX,
            AUDIT_AGENT_OUTPUT_PATH_SUBSTR,
        )

        changed_files = self.list_pr_files(pr_number)
        for file_path in changed_files:
            normalized = str(file_path).replace("\\", "/")
            if normalized.startswith(AUDIT_AGENT_OUTPUT_PATH_PREFIX) and AUDIT_AGENT_OUTPUT_PATH_SUBSTR in normalized:
                return True
        return False

    def _is_human_blocked(self, pr_number: int, head_sha: str) -> bool:
        """Check if a PR is human-blocked (CI passing + approved + no auto-merge label).

        This is a heuristic check — API failures return False (fail-safe).
        """
        # Check if PR has an approval
        try:
            reviews_response = _gh_api(self._repo_api(f"/pulls/{pr_number}/reviews"), paginate=True)
            reviews_data = _parse_paginated_json(reviews_response)
            if isinstance(reviews_data, list):
                reviews = reviews_data
            else:
                logger.warning(
                    "Unexpected reviews payload type for PR #%d: %s",
                    pr_number,
                    type(reviews_data).__name__,
                )
                reviews = []
            reviews = sorted(
                reviews,
                key=lambda review: (
                    review.get("submitted_at") or "",
                    review.get("id") or 0,
                ),
            )
            reviewer_states: dict[str, str] = {}
            for review in reviews:
                reviewer = review.get("user", {}).get("login")
                state = review.get("state")
                if not reviewer or not isinstance(state, str):
                    continue
                if state == "DISMISSED":
                    reviewer_states.pop(reviewer, None)
                    continue
                if state in {"APPROVED", "CHANGES_REQUESTED"}:
                    reviewer_states[reviewer] = state
            has_approval = "APPROVED" in reviewer_states.values()
            has_changes_requested = "CHANGES_REQUESTED" in reviewer_states.values()
        except (RuntimeError, json.JSONDecodeError):
            return False

        if not has_approval or has_changes_requested:
            return False

        # Check combined commit status
        try:
            status_response = _gh_api(self._repo_api(f"/commits/{head_sha}/status"))
            status_data = json.loads(status_response)
            combined_state = status_data.get("state", "unknown")
            total_count = status_data.get("total_count", -1)
        except (RuntimeError, json.JSONDecodeError):
            return False

        # Check check-runs
        try:
            checks_response = _gh_api(self._repo_api(f"/commits/{head_sha}/check-runs"), paginate=True)
            checks_data = _parse_paginated_json(checks_response)
            if isinstance(checks_data, dict):
                check_runs = checks_data.get("check_runs", [])
            else:
                logger.warning(
                    "Unexpected check-runs payload type for PR #%d (sha %s): %s",
                    pr_number,
                    head_sha,
                    type(checks_data).__name__,
                )
                return False
            failing_checks = [
                cr
                for cr in check_runs
                if cr.get("status") != "completed" or cr.get("conclusion") not in ("success", "skipped", "neutral")
            ]
            check_runs_ok = len(failing_checks) == 0
        except (RuntimeError, json.JSONDecodeError):
            return False

        # CI is passing when check-runs are clean and either combined status is success
        # or there are no legacy statuses (total_count == 0)
        ci_passing = check_runs_ok and (combined_state == "success" or total_count == 0)

        return ci_passing

    def get_recent_dispatch_history(self, workflow: str) -> list[DispatchEvent]:
        """Get recent dispatch events by parsing workflow run metadata.

        For each candidate run the method first fetches the individual run
        detail (``GET /repos/{owner}/{repo}/actions/runs/{run_id}``) to read
        ``inputs.pr_number`` — the only reliable source for
        ``workflow_dispatch`` runs, since the list-runs endpoint does not
        include dispatch inputs and ``pull_requests[]`` is almost always
        empty for such runs.  The existing ``pull_requests[].number`` and
        run-name regex signals are kept as secondary/tertiary fallbacks.

        In-progress runs are included (``status=None`` passed to
        ``list_workflow_runs``) so that a just-dispatched run is visible on
        the immediately following scheduler cycle even before it completes.

        The total number of runs inspected is capped at
        ``_MAX_DISPATCH_HISTORY_RUNS`` to bound the number of per-run
        detail REST calls made in a single invocation.  Each per-run fetch
        is wrapped in its own ``try/except`` so a failed or
        permission-denied call is silently skipped rather than aborting the
        whole history resolution.

        Returns:
            List of DispatchEvent sorted most-recent-first.
        """
        from agentic_devtools.cli.ci.scheduler import DispatchEvent

        runs = self.list_workflow_runs(workflow, window_hours=24, status=None)
        events: list[DispatchEvent] = []
        runs_inspected = 0

        for run in sorted(runs, key=lambda r: r.created_at, reverse=True):
            if runs_inspected >= _MAX_DISPATCH_HISTORY_RUNS:
                break
            runs_inspected += 1

            pr_num = 0

            # Primary (workflow_dispatch): fetch run detail for inputs.pr_number — the only
            # reliable source for workflow_dispatch runs.
            if run.event == "workflow_dispatch":
                try:
                    run_detail_raw = _gh_api(self._repo_api(f"/actions/runs/{run.id}"))
                    run_detail = json.loads(run_detail_raw)
                    pr_num = _parse_inputs_pr_number(run_detail.get("inputs"))
                except RetryableError as exc:
                    # Rate-limit or transient server error — stop to avoid hammering the API.
                    if exc.is_rate_limit:
                        raise ProviderRateLimitError(
                            retry_after_seconds=exc.retry_after,
                            reset_timestamp=exc.reset_timestamp,
                            remaining=exc.remaining,
                            provider=exc.provider,
                            credential_identity=exc.credential_identity,
                            source=exc.source,
                            is_rate_limit=True,
                        ) from exc
                    break
                except Exception as exc:
                    logger.debug("Failed to fetch run detail for run %s: %s", run.id, exc)

            # Secondary fallback: pull_requests[].number (often empty for workflow_dispatch
            # runs, but available for PR-event runs).
            if pr_num <= 0 and run.pr_number > 0:
                pr_num = run.pr_number
            # Tertiary fallback: run-name regex (fragile but better than nothing).
            if pr_num <= 0:
                match = _PR_NUMBER_FROM_RUN_NAME.search(run.name or "")
                if match:
                    pr_num = int(match.group(1))

            if pr_num > 0:
                events.append(DispatchEvent(pr_number=pr_num, created_at=run.created_at))

            if len(events) >= _MAX_DISPATCH_HISTORY_EVENTS:
                break

        return events

    def dispatch_workflow(self, workflow: str, inputs: dict[str, str]) -> None:
        """Dispatch a workflow via ``gh workflow run``.

        Args:
            workflow: Workflow file name (e.g., "ai-pr-loop.yml").
            inputs: Dictionary of input field names to values.

        Raises:
            ProviderRateLimitError: If the dispatch fails due to a rate limit.
            RuntimeError: If the dispatch fails for any other reason.
        """
        repo = self._resolve_repo()
        cmd = ["gh", "workflow", "run", workflow, "--repo", repo]
        for key, value in inputs.items():
            cmd.extend(["--field", f"{key}={value}"])

        result = run_safe(cmd, capture_output=True, text=True, shell=False)
        if result.returncode != 0:
            stderr = result.stderr.strip()
            stderr_lower = stderr.lower()
            status_match = _GH_STATUS_RE.search(stderr)
            if "rate limit" in stderr_lower or (status_match is not None and int(status_match.group(1)) == 429):
                raise ProviderRateLimitError(
                    provider="github",
                    source="dispatch-stderr",
                )
            raise RuntimeError(f"Workflow dispatch failed: {stderr}")

    @retry_with_backoff()
    def get_variable(self, name: str, *, use_writer_token: bool = False) -> str | None:
        """Read a repository Actions variable by name.

        Uses the default GH_TOKEN when it has actions:read (or actions:write)
        access to repository Actions variables. When ``use_writer_token`` is
        true, the read uses ``REPO_VARIABLE_WRITER_PAT`` instead so the write
        credential can recover cooldown state even if the primary PR token is
        rate limited.

        Returns:
            The variable value as a string, or None if not found.
        """
        from agentic_devtools.cli.ci.exceptions import VariableWriteError

        token: str | None = None
        if use_writer_token:
            token = os.environ.get("REPO_VARIABLE_WRITER_PAT", "").strip()
            if not token:
                raise VariableWriteError("REPO_VARIABLE_WRITER_PAT is not configured")
        try:
            response = _gh_api(self._repo_api(f"/actions/variables/{name}"), token=token)
            data = json.loads(response)
            return data.get("value")
        except RuntimeError as exc:
            if re.search(r"\b404\b", str(exc)):
                return None
            raise

    @retry_with_backoff()
    def set_variable(self, name: str, value: str) -> None:
        """Write a repository Actions variable using REPO_VARIABLE_WRITER_PAT.

        Raises:
            VariableWriteError: When the write cannot be performed.
        """
        from agentic_devtools.cli.ci.exceptions import VariableWriteError

        token = os.environ.get("REPO_VARIABLE_WRITER_PAT", "").strip()
        if not token:
            raise VariableWriteError("REPO_VARIABLE_WRITER_PAT is not configured")

        try:
            # Try PATCH first (update existing)
            _gh_api(
                self._repo_api(f"/actions/variables/{name}"),
                method="PATCH",
                body={"name": name, "value": value},
                token=token,
            )
        except RuntimeError as exc:
            if re.search(r"\b404\b", str(exc)):
                # Variable doesn't exist yet — create it
                try:
                    _gh_api(
                        self._repo_api("/actions/variables"),
                        method="POST",
                        body={"name": name, "value": value},
                        token=token,
                    )
                except RuntimeError as create_exc:
                    raise VariableWriteError(f"Failed to create variable {name}: {create_exc}") from create_exc
            else:
                raise VariableWriteError(f"Failed to set variable {name}: {exc}") from exc

    @retry_with_backoff()
    def validate_variable_token(self) -> bool:
        """Validate REPO_VARIABLE_WRITER_PAT by attempting to list variables.

        Returns:
            True if the token is valid and has sufficient permissions.
        """
        token = os.environ.get("REPO_VARIABLE_WRITER_PAT", "").strip()
        if not token:
            return False
        try:
            _gh_api(self._repo_api("/actions/variables?per_page=1"), token=token)
            return True
        except RuntimeError:
            return False

    # ------------------------------------------------------------------
    # Audit methods
    # ------------------------------------------------------------------

    @retry_with_backoff()
    def list_closed_prs(
        self,
        *,
        exclude_labels: list[str],
        limit: int,
        state: str = "closed",
    ) -> list[ClosedPRInfo]:
        """List closed PRs excluding those with specified labels.

        Uses the GitHub Search API for reliable label exclusion.
        The Search API returns results sorted by ``updated_at`` descending
        (most recently updated first), so PRs that receive new activity after
        being closed can appear ahead of more recently closed ones.  Results
        are then sorted client-side by ``closed_at`` descending (newest-closed
        first) before being returned.

        Args:
            exclude_labels: Labels to exclude from results.
            limit: Maximum number of PRs to return.
            state: PR state filter (default "closed").

        Returns:
            List of ClosedPRInfo instances sorted by closed_at desc.
        """
        from agentic_devtools.cli.audit.models import ClosedPRInfo

        # Build search query
        label_exclusions = " ".join(f'-label:"{lbl}"' for lbl in exclude_labels)
        query = f"is:pr is:{state} {label_exclusions}"
        if self._repo:
            query = f"repo:{self._repo} {query}"

        encoded_query = quote(query, safe="")

        all_items: list[Any] = []
        page = 1
        while len(all_items) < limit:
            remaining = limit - len(all_items)
            per_page = min(remaining, 100)
            endpoint = f"/search/issues?q={encoded_query}&sort=updated&order=desc&per_page={per_page}&page={page}"
            response = _gh_api(endpoint)
            data = json.loads(response)
            items = data.get("items", [])
            if not items:
                break
            all_items.extend(items)
            if len(items) < per_page:
                break  # reached last page
            page += 1

        results: list[ClosedPRInfo] = []
        for item in all_items[:limit]:
            pr_number = item.get("number", 0)
            closed_at = item.get("closed_at", "")
            # Determine if merged.  The /search/issues endpoint includes a
            # ``pull_request`` object but ``merged_at`` is not always present
            # in that object.  When the key is absent, fall back to a dedicated
            # /pulls/{number} lookup which reliably exposes the ``merged`` flag.
            pr_data = item.get("pull_request", {})
            if "merged_at" in pr_data:
                merged = bool(pr_data["merged_at"])
            else:
                merged = self._get_pr_merged_status(pr_number)

            html_url = item.get("html_url", "")
            results.append(
                ClosedPRInfo(
                    number=pr_number,
                    title=item.get("title", ""),
                    url=html_url,
                    state=state,
                    closed_at=closed_at,
                    merged=merged,
                )
            )

        # Sort by closed_at descending (newest first)
        results.sort(key=lambda pr: pr.closed_at, reverse=True)
        return results

    def _get_pr_merged_status(self, pr_number: int) -> bool:
        """Fetch the merged status for a PR via the pulls endpoint.

        Used as a fallback when the search API does not include ``merged_at``
        in the ``pull_request`` object of a search result.  Returns ``False``
        when the repository is not configured or the lookup fails.

        Args:
            pr_number: PR number to inspect.

        Returns:
            True if the PR was merged, False otherwise or on lookup error.
        """
        if not self._repo:
            return False
        try:
            response = _gh_api(self._repo_api(f"/pulls/{pr_number}"))
            data = json.loads(response)
            return bool(data.get("merged"))
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.debug(
                "Failed to fetch merged status for PR %d via pulls endpoint; defaulting to False",
                pr_number,
            )
            return False

    @retry_with_backoff()
    def find_deferral_issue(self, *, pr_number: int, review_id: int) -> int | None:
        """Return the open deferral issue already filed for ``(pr_number, review_id)``.

        Makes deferral recoverable: when an earlier run created the issue but failed
        before posting the PR marker, no state records the issue number, so the next
        run would otherwise file a duplicate.  Open issues carrying
        :data:`SUPPRESSED_FOLLOW_UP_LABEL` are matched on the issue-body marker
        payload published in ``docs/suppressed-comment-triage-contract.md``, which is
        the same authority the reaper reads.
        """
        from agentic_devtools.cli.ci.pipeline.gate_verdict import SUPPRESSED_FOLLOW_UP_LABEL  # noqa: PLC0415
        from agentic_devtools.cli.ci.suppressed_reaper import parse_deferral_payload  # noqa: PLC0415

        query = f'is:issue is:open label:"{SUPPRESSED_FOLLOW_UP_LABEL}"'
        if self._repo:
            query = f"repo:{self._repo} {query}"
        encoded_query = quote(query, safe="")
        response = _gh_api(f"/search/issues?q={encoded_query}&per_page=100", paginate=True)
        data = _parse_paginated_json(response)
        if not isinstance(data, dict):
            raise RuntimeError("Unexpected GitHub Search API response: expected top-level object.")
        items = data.get("items")
        if not isinstance(items, list):
            raise RuntimeError("Unexpected GitHub Search API response: 'items' is missing or not a list.")
        for item in items:
            if not isinstance(item, dict):
                raise RuntimeError("Unexpected GitHub Search API response: found non-object item in 'items'.")
            payload = parse_deferral_payload(item.get("body") or "")
            if payload is None or payload["pr"] != pr_number or payload["review_id"] != review_id:
                continue
            number = item.get("number")
            if isinstance(number, int) and not isinstance(number, bool) and number > 0:
                return number
            raise RuntimeError(
                "Unexpected GitHub Search API response: matched deferral marker with missing or invalid issue number."
            )
        return None

    def create_deferral_issue(
        self,
        *,
        pr_number: int,
        review_id: int,
        base_sha: str,
        findings: list[tuple[str, str]],
        labels: list[str],
    ) -> int:
        """Create the suppressed-comment deferral issue using SPECKIT_PR_TOKEN.

        The body follows ``docs/suppressed-comment-triage-contract.md``: the
        ``ai-pr-loop:suppressed-comment-deferral`` marker is the first line, and each
        finding is reproduced verbatim inside a dynamically sized fence.
        """
        token = os.environ.get("SPECKIT_PR_TOKEN", "").strip()
        if not token:
            raise RuntimeError("SPECKIT_PR_TOKEN is required to create suppressed-comment deferral issues.")

        title = f"Triage deferred suppressed review comments from PR #{pr_number}"
        body = _render_deferral_issue_body(
            pr_number=pr_number,
            review_id=review_id,
            base_sha=base_sha,
            findings=findings,
        )

        response = _gh_api(
            self._repo_api("/issues"),
            method="POST",
            body={"title": title, "body": body, "labels": labels},
            token=token,
        )
        data = json.loads(response)
        issue_number = data.get("number")
        if isinstance(issue_number, bool) or not isinstance(issue_number, int) or issue_number <= 0:
            raise RuntimeError("Failed to create deferral issue: missing issue number in response.")
        return issue_number

    @retry_with_backoff()
    def dispatch_suppressed_triage(
        self,
        *,
        issue_number: int,
        pr_number: int,
        review_id: int,
    ) -> AgentAssignmentResult:
        """Dispatch the suppressed-comment triage agent via coding-agent assignment."""
        if not os.environ.get("SPECKIT_PR_TOKEN", "").strip():
            raise RuntimeError("SPECKIT_PR_TOKEN is required to dispatch suppressed-comment triage.")

        prompt_file = ".github/agents/agdt.suppressed-comment-triage.evaluate.agent.md"
        prompt_content = _read_repo_file(prompt_file)
        if not prompt_content:
            raise RuntimeError(
                f"Could not read required agent prompt file '{prompt_file}'. "
                "Ensure the file exists in the repository checkout (GITHUB_WORKSPACE)."
            )
        problem_statement = _enforce_comment_size_limit(
            "\n".join(
                [
                    "Triage the deferred suppressed review comments recorded in this issue.",
                    "",
                    f"- Source PR: #{pr_number}",
                    f"- Copilot review: {review_id}",
                    "",
                    "The findings, and the output contract you must satisfy, are in the issue body.",
                    "",
                    "Agent prompt file path:",
                    f"- `{prompt_file}`",
                    "",
                    "Embedded agent prompt:",
                    _fence(prompt_content, "markdown"),
                ]
            )
        )

        result = assign_issue_to_agent(
            repo=self._repo,
            issue_number=issue_number,
            problem_statement=problem_statement,
            custom_instructions=problem_statement,
            custom_agent="agdt.suppressed-comment-triage.evaluate",
            base_branch="main",
            token_env_vars=("SPECKIT_PR_TOKEN",),
        )
        if not result.success:
            raise RuntimeError(f"Failed to dispatch suppressed-comment triage: {result.error}")
        if not result.session_confirmed:
            logger.warning(
                "Issue #%d suppressed-triage dispatch succeeded but session-start event was not confirmed "
                "(session_confirmed=False)",
                issue_number,
            )
        return result

    @retry_with_backoff()
    def count_open_issues_with_label(self, label: str) -> int:
        """Return the number of open issues carrying *label* via the Search API."""
        query = f'is:issue is:open label:"{label}"'
        if self._repo:
            query = f"repo:{self._repo} {query}"
        encoded_query = quote(query, safe="")
        response = _gh_api(f"/search/issues?q={encoded_query}&per_page=1")
        data = json.loads(response)
        total = data.get("total_count")
        if not isinstance(total, int) or isinstance(total, bool):
            raise RuntimeError(
                f"Unexpected GitHub Search API response for label {label!r}: 'total_count' is {total!r} (expected int)."
            )
        return total

    @retry_with_backoff()
    def list_linked_issue_labels(self, pr_number: int) -> list[str]:
        """Return label names on the PR's ``closingIssuesReferences`` issues."""
        query = """
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      closingIssuesReferences(first: 100) {
        pageInfo { hasNextPage }
        nodes {
          labels(first: 100) {
            pageInfo { hasNextPage }
            nodes { name }
          }
        }
      }
    }
  }
}
"""
        owner, repo_name = self._resolve_repo().split("/", 1)
        response = self.graphql(
            query=query,
            variables={"owner": owner, "repo": repo_name, "number": pr_number},
        )
        repository = response.get("data", {}).get("repository")
        if not isinstance(repository, dict):
            raise RuntimeError(
                f"Unexpected GraphQL response for PR #{pr_number}: "
                f"'repository' is {type(repository).__name__!r}, expected dict."
            )
        pr_node = repository.get("pullRequest")
        if not isinstance(pr_node, dict):
            raise RuntimeError(
                f"Unexpected GraphQL response for PR #{pr_number}: "
                f"'pullRequest' is {type(pr_node).__name__!r}, expected dict."
            )
        return _validated_linked_issue_label_names(pr_node, pr_number=pr_number)

    @retry_with_backoff()
    def list_prs_with_label(self, label: str) -> list[int]:
        """List numbers of PRs that currently carry the given label.

        Uses the GitHub Search API. Both open and closed PRs are included so a
        stuck label is found regardless of PR state. All pages are fetched so
        that skipped PRs on the first page cannot permanently block later ones.

        Sorted by ``updated`` ascending: labelling a PR bumps its ``updated_at``
        so recently-labelled PRs appear last, while older stuck PRs (higher
        priority for reaping) appear first.

        Args:
            label: Label name to filter on.

        Returns:
            PR numbers carrying the label.
        """
        query = f'is:pr label:"{label}"'
        repo = self._repo or os.environ.get("GITHUB_REPOSITORY", "")
        if repo:
            query = f"repo:{repo} {query}"
        encoded_query = quote(query, safe="")
        endpoint = f"/search/issues?q={encoded_query}&per_page=100&sort=updated&order=asc"
        response = _gh_api(endpoint, paginate=True)
        data = _parse_paginated_json(response)
        items = data.get("items", []) if isinstance(data, dict) else []
        return [int(item["number"]) for item in items if item.get("number")]

    @retry_with_backoff()
    def get_label_applied_at(self, pr_number: int, label: str) -> datetime | None:
        """Return when a label was most recently applied to a PR.

        Inspects the issue events timeline for ``labeled`` events matching the
        given label and returns the timestamp of the most recent one.

        Args:
            pr_number: PR number to inspect.
            label: Label name to look up.

        Returns:
            Timezone-aware datetime of the most recent ``labeled`` event for the
            label, or None when no such event is found.
        """
        endpoint = self._repo_api(f"/issues/{pr_number}/events")
        response = _gh_api(endpoint, paginate=True)
        events = _parse_paginated_json(response)
        if not isinstance(events, list):
            return None

        latest: datetime | None = None
        for event in events:
            if event.get("event") != "labeled":
                continue
            if event.get("label", {}).get("name") != label:
                continue
            created_at = event.get("created_at")
            if not created_at:
                continue
            try:
                applied = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
            except ValueError:
                continue
            if latest is None or applied > latest:
                latest = applied
        return latest

    @retry_with_backoff()
    def create_audit_tracking_issue(self, *, batch_id: str, pr_numbers: list[int]) -> int:
        """Create a tracking issue for one audit batch using SPECKIT_PR_TOKEN."""
        token = os.environ.get("SPECKIT_PR_TOKEN", "").strip()
        if not token:
            raise RuntimeError("SPECKIT_PR_TOKEN is required to create audit tracking issues.")

        short_batch = batch_id[:8]
        title = f"Review feedback audit — batch {short_batch}"
        pr_list = ", ".join(f"#{n}" for n in pr_numbers) if pr_numbers else "(none)"
        body = "\n".join(
            [
                "# Review Feedback Audit Tracking Issue",
                "",
                f"- **Batch ID:** `{batch_id}`",
                f"- **PR count:** {len(pr_numbers)}",
                f"- **PR numbers:** {pr_list}",
                "",
                "This issue tracks evaluation dispatch and apply results for this batch.",
            ]
        )

        response = _gh_api(
            self._repo_api("/issues"),
            method="POST",
            body={"title": title, "body": body},
            token=token,
        )
        data = json.loads(response)
        issue_number = data.get("number")
        if not isinstance(issue_number, int):
            raise RuntimeError("Failed to create audit tracking issue: missing issue number in response.")
        return issue_number

    @retry_with_backoff()
    def dispatch_audit_evaluation(
        self,
        *,
        tracking_issue: int,
        batch_id: str,
        batch_branch: str,
        batch_dir: str,
        pr_numbers: list[int],
    ) -> AgentAssignmentResult:
        """Dispatch the review-feedback audit evaluation agent via coding-agent assignment."""
        if not os.environ.get("SPECKIT_PR_TOKEN", "").strip():
            raise RuntimeError("SPECKIT_PR_TOKEN is required to dispatch audit evaluation.")

        prompt_file = ".github/agents/agdt.review-feedback-audit.evaluate.agent.md"
        prompt_content = _read_repo_file(prompt_file)
        if not prompt_content:
            raise RuntimeError(
                f"Could not read required agent prompt file '{prompt_file}'. "
                "Ensure the file exists in the repository checkout (GITHUB_WORKSPACE)."
            )
        pr_csv = ", ".join(f"#{n}" for n in pr_numbers) if pr_numbers else "(none)"
        problem_statement = _enforce_comment_size_limit(
            "\n".join(
                [
                    "Run the Review Feedback Audit evaluation agent for this batch.",
                    "",
                    f"- Batch ID: `{batch_id}`",
                    f"- Batch branch: `{batch_branch}`",
                    f"- PRs in batch: {pr_csv}",
                    "",
                    "Use these prepared input files from the batch branch:",
                    f"- `{batch_dir}/batch-summary.md`",
                    f"- `{batch_dir}/batch-data.md`",
                    f"- `{batch_dir}/instruction-files.md`",
                    "",
                    "Write results back to the same batch branch under:",
                    f"- `{batch_dir}/agent-output/`",
                    "  - modified/created instruction files: `AGENTS.md` for directory-scoped "
                    "guidance, `.github/copilot-instructions.md` for repository-wide guidance "
                    "(preserve repo-relative paths)",
                    "  - `audit-summary-report.md`",
                    "",
                    "Agent prompt file path:",
                    f"- `{prompt_file}`",
                    "",
                    "Embedded agent prompt:",
                    _fence(prompt_content, "markdown"),
                ]
            )
        )

        result = assign_issue_to_agent(
            repo=self._repo,
            issue_number=tracking_issue,
            problem_statement=problem_statement,
            custom_instructions=problem_statement,
            custom_agent="agdt.review-feedback-audit.evaluate",
            base_branch="main",
            token_env_vars=("SPECKIT_PR_TOKEN",),
        )
        if not result.success:
            raise RuntimeError(f"Failed to dispatch audit evaluation: {result.error}")
        if not result.session_confirmed:
            logger.warning(
                "Issue #%d audit dispatch succeeded but session-start event was not confirmed "
                "(session_confirmed=False)",
                tracking_issue,
            )
        return result

    @retry_with_backoff()
    def claim_pr_for_audit(self, pr_number: int, label: str) -> ClaimResult:
        """Claim a PR for audit via GET-then-POST label pattern.

        Args:
            pr_number: PR number to claim.
            label: Label to use as claim marker.

        Returns:
            ClaimResult.CLAIMED or ClaimResult.ALREADY_CLAIMED.
        """
        from agentic_devtools.cli.audit.models import ClaimResult

        # Check current labels
        endpoint = self._repo_api(f"/issues/{pr_number}/labels")
        response = _gh_api(endpoint)
        labels = json.loads(response)
        existing_names = [lbl.get("name", "") for lbl in labels]

        if label in existing_names:
            return ClaimResult.ALREADY_CLAIMED

        # Add claim label
        self.add_label(pr_number, label)
        return ClaimResult.CLAIMED

    @retry_with_backoff()
    def add_label(self, pr_number: int, label: str) -> None:
        """Add a label to a PR (idempotent).

        Args:
            pr_number: PR number.
            label: Label name to add.
        """
        endpoint = self._repo_api(f"/issues/{pr_number}/labels")
        _gh_api(endpoint, method="POST", body={"labels": [label]})

    @retry_with_backoff()
    def remove_label(self, pr_number: int, label: str) -> None:
        """Remove a label from a PR (idempotent).

        If the label is not present, the 404 error is swallowed.

        Args:
            pr_number: PR number.
            label: Label name to remove.
        """
        encoded_label = quote(label, safe="")
        endpoint = self._repo_api(f"/issues/{pr_number}/labels/{encoded_label}")
        try:
            _gh_api(endpoint, method="DELETE")
        except RuntimeError as e:
            # Swallow 404 (label not present) for idempotent behavior
            if "404" in str(e):
                return
            raise

    @retry_with_backoff()
    def count_prs_without_labels(
        self,
        *,
        exclude_labels: list[str],
        state: str = "closed",
    ) -> int:
        """Count closed PRs without any of the specified labels.

        Uses the GitHub Search API total_count for efficiency.

        Args:
            exclude_labels: Labels whose absence qualifies a PR for counting.
            state: PR state filter.

        Returns:
            Count of matching PRs.
        """
        label_exclusions = " ".join(f'-label:"{lbl}"' for lbl in exclude_labels)
        query = f"is:pr is:{state} {label_exclusions}"
        if self._repo:
            query = f"repo:{self._repo} {query}"

        encoded_query = quote(query, safe="")
        endpoint = f"/search/issues?q={encoded_query}&per_page=1"

        response = _gh_api(endpoint)
        data = json.loads(response)
        return data.get("total_count", 0)

    @retry_with_backoff()
    def list_all_review_comments(self, pr_number: int) -> list[ReviewCommentInfo]:
        """List all review comments for a PR with pagination.

        Fetches all inline review comments regardless of which review
        they belong to.

        Args:
            pr_number: PR number.

        Returns:
            List of ReviewCommentInfo for all review comments.
        """
        endpoint = self._repo_api(f"/pulls/{pr_number}/comments")
        response = _gh_api(endpoint, paginate=True)
        comments_data = _parse_paginated_json(response)

        results: list[ReviewCommentInfo] = []
        for c in comments_data:
            source_review_id = c.get("pull_request_review_id")
            results.append(
                ReviewCommentInfo(
                    id=c.get("id", 0),
                    path=c.get("path", ""),
                    body=c.get("body", ""),
                    html_url=c.get("html_url", ""),
                    is_suppressed=_comment_is_suppressed(c),
                    start_line=c.get("start_line"),
                    end_line=c.get("line"),
                    line=c.get("line"),
                    position=c.get("position"),
                    diff_hunk=c.get("diff_hunk", ""),
                    commit_id=c.get("commit_id", ""),
                    original_commit_id=c.get("original_commit_id", ""),
                    source_review_id=int(source_review_id) if source_review_id is not None else 0,
                    author_login=c.get("user", {}).get("login", ""),
                    in_reply_to_id=c.get("in_reply_to_id"),
                )
            )
        return results

    def create_pull_request(
        self,
        title: str,
        body: str,
        *,
        draft: bool = True,
    ) -> str:
        """Create a pull request on the current branch using the gh CLI.

        Args:
            title: PR title.
            body: PR body/description (Markdown).
            draft: Whether to create the PR as a draft (default True).

        Returns:
            URL of the created PR, or empty string on failure.
        """
        cmd = ["gh", "pr", "create", "--title", title, "--body", body]
        if draft:
            cmd.append("--draft")
        if self._repo:
            cmd.extend(["--repo", self._repo])
        result = run_safe(cmd, capture_output=True, text=True, shell=False)
        if result.returncode != 0:
            # gh may emit the "already exists" message on stdout, stderr, or split
            # across both streams depending on the version. Combine them so the
            # idempotency check is robust regardless of which stream is used.
            combined = f"{result.stdout}\n{result.stderr}".strip()
            # Idempotency: when an open PR already exists for this branch, gh
            # exits non-zero but prints the existing PR URL. Reuse it instead of
            # reporting a failure (a force-pushed branch already reflects the new
            # content). A genuine failure still returns "" as before.
            existing_url = _extract_existing_pr_url(combined)
            if existing_url:
                logger.info("PR already exists for this branch; reusing existing PR: %s", existing_url)
                return existing_url
            logger.error("gh pr create failed: %s", combined)
            return ""
        return result.stdout.strip()

    def list_no_change_candidate_prs(self) -> list[NoChangePRBrief]:
        """List open PRs with the author, body and diff statistics.

        The listing is fully paginated oldest-first (continuing until
        ``hasNextPage`` is false) so that no eligible empty-diff follow-up PR
        is invisible behind a fixed page cap. Each page carries everything the
        no-change reaper needs to reject a PR (conditions 1, 2 and 4 of the
        contract), so the more expensive compare/tree calls only ever run for a
        genuine candidate.
        """
        repo = self._resolve_repo()
        owner, repo_name = repo.split("/", 1)
        briefs: list[NoChangePRBrief] = []
        end_cursor: str | None = None
        while True:
            data = self.graphql(
                query=_NO_CHANGE_CANDIDATE_PRS_QUERY,
                variables={"owner": owner, "name": repo_name, "after": end_cursor},
            )
            errors = data.get("errors")
            if isinstance(errors, list) and errors:
                messages = [
                    error.get("message", "Unknown GraphQL error") for error in errors if isinstance(error, dict)
                ]
                if not messages:
                    messages = ["Unknown GraphQL error"]
                raise RuntimeError("No-change candidate PR GraphQL query failed: " + "; ".join(messages))

            pr_data = data.get("data", {}).get("repository", {}).get("pullRequests", {})
            nodes = pr_data.get("nodes", [])
            if not isinstance(nodes, list):
                nodes = []
            for node in nodes:
                if not isinstance(node, dict):
                    continue
                number = node.get("number")
                if not isinstance(number, int) or number <= 0:
                    continue
                author = node.get("author")
                login = str(author.get("login", "") or "") if isinstance(author, dict) else ""
                briefs.append(
                    NoChangePRBrief(
                        number=number,
                        author_login=_normalize_bot_login(
                            login,
                            isinstance(author, dict) and author.get("__typename") == "Bot",
                        ),
                        body=str(node.get("body", "") or ""),
                        changed_files=int(node.get("changedFiles") or 0),
                        additions=int(node.get("additions") or 0),
                        deletions=int(node.get("deletions") or 0),
                        head_branch=str(node.get("headRefName", "") or ""),
                        is_cross_repository=bool(node.get("isCrossRepository")),
                    )
                )

            page_info = pr_data.get("pageInfo", {})
            if not isinstance(page_info, dict) or not page_info.get("hasNextPage", False):
                break
            next_cursor = page_info.get("endCursor")
            if not isinstance(next_cursor, str) or not next_cursor:
                break
            end_cursor = next_cursor

        return briefs

    @retry_with_backoff()
    def get_pr_tree_state(self, pr_number: int) -> PRTreeState:
        """Return the PR's merge base plus the trees at the merge base and HEAD.

        ``GET /repos/{owner}/{repo}/compare/{base}...{head}`` yields both the
        merge-base commit and its tree; the HEAD tree is read from the commit
        object. The tree comparison is what makes the empty-diff check
        authoritative — a revert can produce zero changed files on a non-empty
        history.
        """
        metadata = self.get_pr_metadata(pr_number)
        base_sha = self.get_ref_sha(metadata.base_branch)
        if not base_sha:
            raise RuntimeError(f"Could not resolve base branch '{metadata.base_branch}' for PR #{pr_number}")

        compare = json.loads(
            _gh_api(self._repo_api(f"/compare/{quote(base_sha, safe='')}...{quote(metadata.head_sha, safe='')}"))
        )
        merge_base = compare.get("merge_base_commit") or {}
        merge_base_sha = str(merge_base.get("sha", "") or "")
        merge_base_tree = str((merge_base.get("commit") or {}).get("tree", {}).get("sha", "") or "")

        head_commit = json.loads(_gh_api(self._repo_api(f"/git/commits/{quote(metadata.head_sha, safe='')}")))
        head_tree = str((head_commit.get("tree") or {}).get("sha", "") or "")

        return PRTreeState(
            merge_base_sha=merge_base_sha,
            merge_base_tree_sha=merge_base_tree,
            head_tree_sha=head_tree,
            head_sha=metadata.head_sha,
        )

    @retry_with_backoff()
    def get_issue_facts(self, issue_number: int) -> IssueFacts:
        """Return an issue target's lowercased state, raw body, and resource kind."""
        data = json.loads(_gh_api(self._repo_api(f"/issues/{issue_number}")))
        return IssueFacts(
            number=issue_number,
            state=str(data.get("state", "") or "").lower(),
            body=str(data.get("body", "") or ""),
            resource_kind="pull_request" if isinstance(data.get("pull_request"), dict) else "issue",
        )

    @retry_with_backoff()
    def get_file_line_count(self, ref: str, path: str) -> int | None:
        """Return the line count of a repository file at *ref*, or None if absent.

        The path comes from an untrusted PR body, so it is rejected unless it is
        a plain repository-relative path; it is then percent-encoded into the
        contents endpoint. The contents metadata is fetched first and must name a
        regular file; directory and other non-file entries are rejected rather
        than treating their JSON representation as file content. A 404 means the
        file does not exist at *ref* and is reported as ``None`` rather than
        raised, because an unresolvable citation is an expected outcome, not an
        error.
        """
        if not _is_safe_repo_path(path):
            return None
        endpoint = f"/contents/{quote(path, safe='/')}?ref={quote(ref, safe='')}"
        try:
            metadata = json.loads(_gh_api(self._repo_api(endpoint)))
        except RuntimeError as exc:
            if _NOT_FOUND_RE.search(str(exc)):
                return None
            raise
        if not isinstance(metadata, dict) or metadata.get("type") != "file":
            return None
        try:
            raw = _gh_api(
                self._repo_api(endpoint),
                headers={"Accept": "application/vnd.github.raw"},
                include_headers=False,
            )
        except RuntimeError as exc:
            if _NOT_FOUND_RE.search(str(exc)):
                return None
            raise
        if not raw:
            return 0
        return len(raw.splitlines())

    @retry_with_backoff()
    def post_issue_comment(self, issue_number: int, body: str) -> int:
        """Post a comment on an issue and return the created comment ID.

        Raises:
            ValueError: If *body* exceeds the GitHub comment size limit.  Silently
                truncating the audit record would leave a misleading trail, so the
                caller is expected to ensure the body fits before calling this method.
        """
        if len(body) > _MAX_COMMENT_BODY_CHARS:
            raise ValueError(
                f"Comment body for issue #{issue_number} exceeds the "
                f"{_MAX_COMMENT_BODY_CHARS:,}-character limit "
                f"({len(body):,} chars); refusing to post a truncated audit record"
            )
        response = _gh_api(
            self._repo_api(f"/issues/{issue_number}/comments"),
            method="POST",
            body={"body": body},
        )
        data = json.loads(response)
        comment_id = data.get("id")
        if not isinstance(comment_id, int):
            raise RuntimeError(f"Failed to post comment on issue #{issue_number}: response carried no comment ID")
        return comment_id

    @retry_with_backoff()
    def close_issue(self, issue_number: int, *, reason: str = "completed") -> None:
        """Close an issue with an explicit state reason."""
        if reason not in ("completed", "not_planned"):
            raise ValueError(f"reason must be 'completed' or 'not_planned', got {reason!r}")
        _gh_api(
            self._repo_api(f"/issues/{issue_number}"),
            method="PATCH",
            body={"state": "closed", "state_reason": reason},
        )

    def close_pr(self, pr_number: int, *, comment: str | None = None) -> None:
        """Close a pull request without merging, optionally commenting first.

        The comment post is deliberately outside the retried unit: it carries its
        own retry, so retrying it together with the close would post duplicate
        comments whenever the close itself hits a transient failure.
        """
        if comment:
            self.post_issue_comment(pr_number, comment)
        self._patch_pr_closed(pr_number)

    @retry_with_backoff()
    def _patch_pr_closed(self, pr_number: int) -> None:
        """Set a pull request's state to ``closed``."""
        _gh_api(self._repo_api(f"/pulls/{pr_number}"), method="PATCH", body={"state": "closed"})

"""Reaper for no-change suppressed-comment triage follow-up pull requests.

GitHub forces the Copilot coding agent to open a pull request even when it
concludes that no change is warranted. Those pull requests are structurally
empty and must be closed automatically, or they accumulate as backlog.

The design principle is **the empty diff is authoritative; the sentinel is only
a filter**. No string is ever trusted on its own: a pull request is closed only
when all five conditions of
[`docs/suppressed-comment-triage-contract.md`](../../../docs/suppressed-comment-triage-contract.md)
hold at once. Anything else leaves the pull request open for a human, so the
worst incidental-match outcome is closing an already-empty pull request — a
no-op.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from agentic_devtools.cli.ci.models import IssueFacts, NoChangePRBrief

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)

#: The only author whose no-change follow-up pull requests are ever reaped.
COPILOT_AGENT_AUTHOR = "copilot-swe-agent[bot]"
COPILOT_BRANCH_PREFIX = "copilot/"

# The four expressions below are the ones published in the contract document.
# ``tests/workflows/test_suppressed_comment_triage_contract.py`` asserts that the
# published copies still match what the triage agent is instructed to emit, so a
# drift between this module and the contract is caught in CI.
SENTINEL_RE = re.compile(r"(?m)^[ \t]*SUPPRESSED_COMMENTS_EVALUATION_NO_CHANGES_NEEDED[ \t]*$")
MARKER_RE = re.compile(
    r"(?m)^[ \t]*<!--[ \t]*agdt:suppressed-eval:no-changes-needed[ \t]+"
    r"review-id:(\d+)[ \t]+deferred-issue:(\d+)[ \t]*-->[ \t]*$"
)
DEFERRAL_MARKER_RE = re.compile(
    r"(?m)^[ \t]*<!--[ \t]*ai-pr-loop:suppressed-comment-deferral[ \t]+(\{.*\})[ \t]*-->[ \t]*$"
)
#: Pattern for a 40-character lowercase hexadecimal SHA-1 / SHA-256 digest.
_FORTY_HEX_RE = re.compile(r"^[0-9a-f]{40}$")
#: The trusted workflow identity that posts deferral issue comments.
_REAPER_COMMENT_AUTHOR = "github-actions[bot]"
ROW_RE = re.compile(
    r"(?m)^\|[ \t]*(\d+)[ \t]*\|[ \t]*`([^`]+)`[ \t]*\|[ \t]*`([a-z-]+)`[ \t]*\|[ \t]*(.+?)[ \t]*\|[ \t]*$"
)

#: The closed verdict vocabulary. Any other token fails the citation check.
VERDICTS = frozenset({"valid-fix", "valid-no-action", "invalid", "stale", "unparseable"})
#: Verdicts that must never appear in a shape-B (no-change) pull request:
#: ``valid-fix`` contradicts the empty diff, ``unparseable`` needs a human.
BLOCKING_VERDICTS = frozenset({"valid-fix", "unparseable"})
#: The verdict exempt from citation resolution — the cited file is gone.
STALE_VERDICT = "stale"

#: A citation is split on its final ``:line`` suffix. Path safety is still
#: enforced before the provider sees the value, but spaces inside a valid
#: repository-relative path are allowed.
_CITATION_RE = re.compile(r"^(?P<path>.+):(?P<line>\d+)$")

_VERDICT_TABLE_HEADER = ("| # | Location | Verdict | Justification |", "| - | -------- | ------- | ------------- |")
_FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})(.*)$")
_FENCE_CLOSE_RE_TEMPLATE = r"^[ \t]*{char}{{{min_length},}}[ \t]*$"


@dataclass(frozen=True)
class VerdictRow:
    """One parsed row of the verdict table.

    Attributes:
        index: The finding index from the issue body (table column ``#``).
        location: The backticked ``path:line`` citation, or the token ``stale``.
        verdict: The backticked verdict token.
        justification: The finding-specific reasoning cell.
    """

    index: int
    location: str
    verdict: str
    justification: str


@dataclass(frozen=True)
class ReapDecision:
    """Outcome of evaluating one candidate pull request.

    Attributes:
        pr_number: The evaluated pull request.
        should_close: Whether every close condition held.
        reason: Stable token naming the condition that failed, or ``"eligible"``.
        deferred_issue: The deferral issue from the anchored marker, when parsed.
        verdict_table: The verdict table rebuilt from the parsed rows, posted to
            the deferral issue on close. ``None`` when the rows were not
            validated.
        evaluated_head_sha: The PR HEAD SHA whose tree identity and citations
            were validated. ``None`` when the PR was rejected before the
            authoritative tree check ran.
        resume_after_issue_close: Whether the deferral issue was already closed
            by a prior partially-successful finalization attempt whose verdict
            table comment is present. When True, finalization resumes by closing
            the PR and deleting the branch without reposting the issue comment
            or re-closing the issue.
    """

    pr_number: int
    should_close: bool
    reason: str
    deferred_issue: int | None = None
    verdict_table: str | None = None
    evaluated_head_sha: str | None = None
    resume_after_issue_close: bool = False


class HeadChangedError(RuntimeError):
    """Raised when a PR's HEAD changed after eligibility was evaluated."""


def parse_no_change_marker(body: str) -> tuple[int, int] | None:
    """Return ``(review_id, deferred_issue)`` from the anchored marker in *body*.

    Only the raw pull request body is ever passed here — a marker quoted in a
    review comment or appearing inside the diff is never seen by the reaper.

    Args:
        body: Raw pull request body.

    Returns:
        The marker's ``review-id`` and ``deferred-issue``, or ``None`` when the
        anchored marker is absent or appears more than once (an ambiguous body
        is never acted upon).
    """
    matches = MARKER_RE.findall(body or "")
    if len(matches) != 1:
        return None
    review_id, deferred_issue = matches[0]
    return int(review_id), int(deferred_issue)


def has_sentinel(body: str) -> bool:
    """Return True when the no-change sentinel sits on a line of its own."""
    return SENTINEL_RE.search(body or "") is not None


def parse_deferral_payload(issue_body: str) -> dict | None:
    """Return the JSON payload of the issue-side deferral marker.

    The contract requires the marker to be the **first** line of the issue body.
    A body where the marker appears later (e.g. in a quoted example or fenced
    block) is rejected. Duplicate matches are also rejected — ambiguous bodies are
    never acted upon.

    Args:
        issue_body: Raw body of the deferral issue.

    Returns:
        The decoded payload when exactly one marker is present on the first line,
        its JSON parses, all four required fields (``pr``, ``review_id``,
        ``base_sha``, ``finding_count``) are present and well-typed (``pr``,
        ``review_id``, and ``finding_count`` are positive integers; ``base_sha``
        is a 40-character lowercase hex string), and all IDs/counts are positive.
        ``None`` otherwise. The marker pattern only ever captures a braced object,
        so a successful parse is always a dict.
    """
    body = issue_body or ""
    matches = DEFERRAL_MARKER_RE.findall(body)
    if len(matches) != 1:
        return None
    # The contract requires the marker to be the first line of the issue body.
    # Verify that the match starts at position 0 (or after only whitespace on the
    # same line) by checking that the first line of the body contains the match.
    first_line = body.split("\n", 1)[0]
    if not DEFERRAL_MARKER_RE.search(first_line):
        return None
    try:
        payload = json.loads(matches[0])
    except json.JSONDecodeError:
        return None
    if not _is_integer(payload.get("review_id")) or not _is_integer(payload.get("finding_count")):
        return None
    if not _is_integer(payload.get("pr")):
        return None
    if not isinstance(payload.get("base_sha"), str) or not _FORTY_HEX_RE.match(payload["base_sha"]):
        return None
    if payload["review_id"] <= 0 or payload["finding_count"] <= 0 or payload["pr"] <= 0:
        return None
    return payload


def _is_integer(value: object) -> bool:
    """Return True for a genuine ``int`` — ``bool`` is an ``int`` subclass."""
    return isinstance(value, int) and not isinstance(value, bool)


def parse_verdict_rows(body: str) -> list[VerdictRow]:
    """Parse the single contiguous contract verdict table from *body*.

    Only an unfenced table with the fixed two-line header is accepted. Row-shaped
    lines that appear outside that one table — for example as isolated prose or
    inside a later second table — are rejected by returning an empty list.
    """
    tables: list[list[VerdictRow]] = []
    open_fence_char: str | None = None
    open_fence_length = 0
    lines = (body or "").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if open_fence_char is None:
            opening_fence = _parse_opening_fence(line)
            if opening_fence is not None:
                open_fence_char, open_fence_length = opening_fence
                index += 1
                continue
        elif _is_closing_fence(line, open_fence_char, open_fence_length):
            open_fence_char = None
            open_fence_length = 0
            index += 1
            continue
        if open_fence_char is not None:
            index += 1
            continue
        if line == _VERDICT_TABLE_HEADER[0]:
            if index + 1 >= len(lines) or lines[index + 1] != _VERDICT_TABLE_HEADER[1]:
                return []
            rows: list[VerdictRow] = []
            index += 2
            while index < len(lines):
                row_match = ROW_RE.fullmatch(lines[index])
                if row_match is None:
                    break
                number, location, verdict, justification = row_match.groups()
                rows.append(
                    VerdictRow(
                        index=int(number),
                        location=location,
                        verdict=verdict,
                        justification=justification,
                    )
                )
                index += 1
            if not rows:
                return []
            tables.append(rows)
            continue
        if ROW_RE.fullmatch(line):
            return []
        index += 1
    if len(tables) != 1:
        return []
    return tables[0]


def _parse_opening_fence(line: str) -> tuple[str, int] | None:
    """Return the CommonMark fence character and length for an opening fence line."""
    match = _FENCE_RE.match(line)
    if match is None:
        return None
    fence = match.group(1)
    return fence[0], len(fence)


def _is_closing_fence(line: str, fence_char: str, minimum_length: int) -> bool:
    """Return True when *line* closes the active CommonMark fenced code block."""
    return (
        re.match(
            _FENCE_CLOSE_RE_TEMPLATE.format(char=re.escape(fence_char), min_length=minimum_length),
            line,
        )
        is not None
    )


def render_verdict_table(rows: list[VerdictRow]) -> str:
    """Rebuild the verdict table from parsed rows.

    The table posted to the deferral issue is rebuilt rather than sliced out of
    the pull request body, so only the four parsed cells of each validated row
    are ever reproduced.
    """
    lines = list(_VERDICT_TABLE_HEADER)
    lines.extend(f"| {row.index} | `{row.location}` | `{row.verdict}` | {row.justification} |" for row in rows)
    return "\n".join(lines)


def build_deferral_issue_comment(pr_number: int, verdict_table: str) -> str:
    """Build the completion comment posted to the deferral issue."""
    return "\n".join(
        [
            f"Triage completed in #{pr_number}: no changes were warranted.",
            "",
            verdict_table,
            "",
            f"Closing this issue as completed and closing #{pr_number}, whose diff is empty.",
        ]
    )


def is_empty_diff(brief: NoChangePRBrief) -> bool:
    """Return True when the pull request reports no changed files and no lines."""
    return brief.changed_files == 0 and brief.additions == 0 and brief.deletions == 0


def _citation_resolves(provider: CIPlatformProvider, ref: str, location: str) -> bool:
    """Return True when ``path:line`` names an existing line at *ref*."""
    match = _CITATION_RE.match(location)
    if match is None:
        return False
    path = match.group("path")
    if path.startswith("/") or path.startswith("-") or ".." in path.split("/"):
        return False
    line = int(match.group("line"))
    if line < 1:
        return False
    line_count = provider.get_file_line_count(ref, path)
    return line_count is not None and line <= line_count


def _validate_rows(
    provider: CIPlatformProvider,
    rows: list[VerdictRow],
    *,
    finding_count: int,
    merge_base_sha: str,
) -> str | None:
    """Return the failing reason token for *rows*, or ``None`` when they pass."""
    if len(rows) != finding_count:
        return "row-count-mismatch"
    if [row.index for row in rows] != list(range(1, finding_count + 1)):
        return "row-numbering-mismatch"
    for row in rows:
        if row.verdict not in VERDICTS:
            return "unknown-verdict"
        if row.verdict in BLOCKING_VERDICTS:
            return "blocking-verdict"
        if row.verdict == STALE_VERDICT:
            if row.location != STALE_VERDICT:
                return "stale-location-mismatch"
            continue
        if not _citation_resolves(provider, merge_base_sha, row.location):
            return "unresolved-citation"
    return None


def evaluate_pr(provider: CIPlatformProvider, brief: NoChangePRBrief) -> ReapDecision:
    """Decide whether one candidate pull request may be closed.

    Conditions are checked cheapest-first so that the overwhelming majority of
    open pull requests are rejected from the listing data alone, without any
    further API call.

    Args:
        provider: CI platform provider instance.
        brief: Listing data for the candidate pull request.

    Returns:
        A :class:`ReapDecision`. ``should_close`` is True only when all five
        contract conditions hold.
    """
    pr_number = brief.number

    if not is_empty_diff(brief):
        return ReapDecision(pr_number, False, "non-empty-diff")
    if brief.author_login != COPILOT_AGENT_AUTHOR:
        return ReapDecision(pr_number, False, "not-agent-author")

    marker = parse_no_change_marker(brief.body)
    if marker is None:
        return ReapDecision(pr_number, False, "no-marker")
    review_id, deferred_issue = marker

    if not has_sentinel(brief.body):
        return ReapDecision(pr_number, False, "no-sentinel", deferred_issue)

    issue: IssueFacts = provider.get_issue_facts(deferred_issue)
    if issue.resource_kind != "issue":
        return ReapDecision(pr_number, False, "deferred-target-not-issue", deferred_issue)
    payload = parse_deferral_payload(issue.body)
    if payload is None:
        return ReapDecision(pr_number, False, "deferral-marker-missing", deferred_issue)
    if payload["review_id"] != review_id:
        return ReapDecision(pr_number, False, "review-id-mismatch", deferred_issue)

    tree_state = provider.get_pr_tree_state(pr_number)
    if not tree_state.tree_identical:
        return ReapDecision(pr_number, False, "tree-mismatch", deferred_issue)

    rows = parse_verdict_rows(brief.body)
    failure = _validate_rows(
        provider,
        rows,
        finding_count=payload["finding_count"],
        merge_base_sha=tree_state.merge_base_sha,
    )
    if failure is not None:
        return ReapDecision(pr_number, False, failure, deferred_issue)

    verdict_table = render_verdict_table(rows)
    resume_after_issue_close = False
    issue_state = issue.state.lower()
    if issue_state == "closed":
        issue_comment_body = build_deferral_issue_comment(pr_number, verdict_table)
        if not any(
            issue_comment.body == issue_comment_body and issue_comment.author == _REAPER_COMMENT_AUTHOR
            for issue_comment in provider.list_issue_comments(deferred_issue)
        ):
            return ReapDecision(pr_number, False, "deferral-issue-not-open", deferred_issue)
        resume_after_issue_close = True
    elif issue_state != "open":
        return ReapDecision(pr_number, False, "deferral-issue-not-open", deferred_issue)

    return ReapDecision(
        pr_number,
        True,
        "eligible",
        deferred_issue,
        verdict_table,
        tree_state.head_sha or None,
        resume_after_issue_close,
    )


def close_no_change_pr(provider: CIPlatformProvider, brief: NoChangePRBrief, decision: ReapDecision) -> None:
    """Close an eligible pull request and finalize its deferral issue.

    The verdict table is posted to the deferral issue after the PR HEAD SHA is
    re-checked, then the deferral issue is closed as completed, then the pull
    request is closed. When resuming after a prior issue-close success, the
    issue comment and issue close are skipped. The branch is deleted only after
    the pull request close succeeds, so a failed close never strands a pull
    request whose branch is gone.

    Args:
        provider: CI platform provider instance.
        brief: Listing data for the pull request being closed.
        decision: The eligible decision produced by :func:`evaluate_pr`.

    Raises:
        ValueError: If *decision* is not an eligible decision.
    """
    if (
        not decision.should_close
        or decision.deferred_issue is None
        or decision.verdict_table is None
        or not decision.evaluated_head_sha
    ):
        raise ValueError(f"PR #{brief.number} is not eligible for closing (reason: {decision.reason})")

    if decision.pr_number != brief.number:
        raise ValueError(
            f"Decision is for PR #{decision.pr_number} but brief is for PR #{brief.number}; refusing to close"
        )

    current_head_sha = provider.get_pr_metadata(brief.number).head_sha
    if current_head_sha != decision.evaluated_head_sha:
        raise HeadChangedError(
            f"PR #{brief.number} head changed after evaluation ({decision.evaluated_head_sha} -> {current_head_sha})"
        )

    issue_number = decision.deferred_issue
    if not decision.resume_after_issue_close:
        provider.post_issue_comment(
            issue_number,
            build_deferral_issue_comment(brief.number, decision.verdict_table),
        )
        provider.close_issue(issue_number, reason="completed")
    provider.close_pr(
        brief.number,
        comment=f"Closed automatically: empty diff, no changes warranted. Verdicts recorded on #{issue_number}.",
    )

    if brief.is_cross_repository or not brief.head_branch or not brief.head_branch.startswith(COPILOT_BRANCH_PREFIX):
        return
    try:
        # Re-read the live branch ref immediately before deletion.  A commit could
        # have been pushed between the HEAD check earlier in this function and now
        # (after the issue/PR mutations).  Using get_ref_sha avoids stale PR metadata
        # returned by the pull endpoint after the PR is closed.  Skip deletion when
        # the branch tip has advanced so we never delete a branch that carries new work.
        current_sha_before_delete = provider.get_ref_sha(brief.head_branch)
        if current_sha_before_delete != decision.evaluated_head_sha:
            logger.warning(
                "Branch %s tip changed after PR close (%s -> %s); skipping deletion",
                brief.head_branch,
                decision.evaluated_head_sha,
                current_sha_before_delete,
            )
            return
        provider.delete_branch(brief.head_branch)
    except Exception:
        logger.warning(
            "Failed to delete branch %s after closing PR #%d",
            brief.head_branch,
            brief.number,
            exc_info=True,
        )


def reap_no_change_prs(
    provider: CIPlatformProvider,
    *,
    max_prs: int | None = None,
    dry_run: bool = False,
) -> dict:
    """Close every open no-change suppressed-triage follow-up pull request.

    Args:
        provider: CI platform provider instance.
        max_prs: Maximum number of pull requests to close in one run. ``None``
            means no limit. Evaluation of further candidates stops once the
            limit is reached.
        dry_run: When True, report the pull requests that would be closed
            without performing any mutation.

    Returns:
        Summary dict with keys ``checked`` (int), ``closed`` (list of
        ``{"pr", "issue"}`` dicts), ``skipped`` (list of ``{"pr", "reason"}``
        dicts) and ``dry_run`` (bool).

    Raises:
        ValueError: If *max_prs* is not a positive integer.
    """
    if max_prs is not None and max_prs < 1:
        raise ValueError(f"max_prs must be a positive integer (>= 1) or None, got {max_prs!r}")

    result: dict = {"checked": 0, "closed": [], "skipped": [], "dry_run": dry_run}

    for brief in provider.list_no_change_candidate_prs():
        if max_prs is not None and len(result["closed"]) >= max_prs:
            break
        result["checked"] += 1
        try:
            decision = evaluate_pr(provider, brief)
        except Exception:
            logger.warning("Failed to evaluate PR #%d; leaving it open", brief.number, exc_info=True)
            result["skipped"].append({"pr": brief.number, "reason": "evaluation-failed"})
            continue

        if not decision.should_close:
            logger.info("PR #%d not closed: %s", brief.number, decision.reason)
            result["skipped"].append({"pr": brief.number, "reason": decision.reason})
            continue

        if dry_run:
            result["closed"].append({"pr": brief.number, "issue": decision.deferred_issue})
            continue

        try:
            close_no_change_pr(provider, brief, decision)
        except HeadChangedError:
            logger.info("PR #%d not closed: head-changed", brief.number)
            result["skipped"].append({"pr": brief.number, "reason": "head-changed"})
            continue
        except Exception:
            logger.warning("Failed to close PR #%d", brief.number, exc_info=True)
            result["skipped"].append({"pr": brief.number, "reason": "close-failed"})
            continue

        logger.info("Closed no-change PR #%d and deferral issue #%s", brief.number, decision.deferred_issue)
        result["closed"].append({"pr": brief.number, "issue": decision.deferred_issue})

    return result

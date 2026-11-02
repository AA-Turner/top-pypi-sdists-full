"""Summary comment rendering and posting for the pipeline."""

from __future__ import annotations

import html
import logging
import os

from agentic_devtools.cli.ci.comment_format import normalize_ai_pr_loop_comment
from agentic_devtools.cli.ci.pipeline.models import (
    ActionDecision,
    ActionResult,
    PipelineRunSummary,
)
from agentic_devtools.cli.ci.pipeline.session_evidence_summary import _render_state_snapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider, trusted_loop_comment_logins
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)

SUMMARY_SENTINEL = "<!-- agdt:ai-pr-loop-summary -->"
SUMMARY_COLLAPSED_SENTINEL = "<!-- agdt:ai-pr-loop-summary-collapsed -->"
SUMMARY_FALLBACK_MARKERS = (
    f"{SUMMARY_SENTINEL}\n\n#### 🤖 AI PR Loop Run",
    f"{SUMMARY_SENTINEL}\n\n**🤖 AI PR Loop Run**",
)

# Maximum length of the rendered preconditions cell. Wide enough to carry
# several failing keys without clipping mid-word.
_PRECONDITION_CLIP_LENGTH = 120


def _sanitize_cell(value: str) -> str:
    """Sanitize a Markdown table cell value.

    Replaces newlines with <br> and escapes pipe characters to prevent
    broken table formatting when values come from exception messages or
    multi-line details strings.
    """
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    escaped = html.escape(normalized, quote=False)
    return escaped.replace("|", "\\|").replace("\n", "<br>")


def _sanitize_single_line(value: str) -> str:
    """Sanitize text inserted into single-line header content."""
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    single_line = " ".join(part for part in normalized.split("\n") if part)
    return html.escape(single_line.strip(), quote=False)


def _sanitize_run_url(url: str) -> str:
    """Normalize run URL by stripping line breaks and surrounding whitespace."""
    return url.replace("\r", "").replace("\n", "").strip()


def _is_editable_summary_comment_author(*, author: str, trusted_authors: set[str]) -> bool:
    """Return True only for a verified comment identity.

    Fails closed: an empty/unknown author is treated as not editable to avoid
    accidentally editing comments posted by a deleted or anonymous user.
    """
    normalized_author = author.strip().casefold()
    return bool(normalized_author and normalized_author in trusted_authors)


def _summary_state_signature(body: str) -> str | None:
    """Return a summary identity independent of its active/collapsed sentinel.

    Malformed terminal labels have no stable identity: callers skip signature-based
    deduplication, while provider writes continue to reject the malformed suffix.
    """
    normalized = normalize_ai_pr_loop_comment(body)
    if normalized is None:
        return None
    return normalized.replace(SUMMARY_COLLAPSED_SENTINEL, SUMMARY_SENTINEL, 1)


_DECISION_ICONS = {
    ActionDecision.EXECUTE: "✅",
    ActionDecision.SKIP: "⬜",
    ActionDecision.BLOCKED: "🚫",
    ActionDecision.BLOCKED_BY_GUARD: "🚫",
    ActionDecision.FAILED: "❌",
}

_DECISION_LABELS = {
    ActionDecision.EXECUTE: "**executed**",
    ActionDecision.SKIP: "skipped",
    ActionDecision.BLOCKED: "blocked",
    ActionDecision.BLOCKED_BY_GUARD: "blocked (guards)",
    ActionDecision.FAILED: "**failed**",
}

_APPROVER_PREFLIGHT_CAPABILITIES = frozenset(
    {"identity", "repository_visibility", "repository_role", "review_eligibility"}
)
_APPROVER_PREFLIGHT_DIAGNOSTIC = "Required approver capability is missing, denied, or unknown."


def _emit_approver_preflight_alerts(results: list[ActionResult]) -> None:
    """Surface blocked approver capabilities using fixed, allowlisted content."""
    for result in results:
        capability = next(
            (allowed for allowed in _APPROVER_PREFLIGHT_CAPABILITIES if result.capability == allowed),
            None,
        )
        if result.name != "approve" or result.decision is not ActionDecision.BLOCKED or capability is None:
            continue

        status = result.http_status if type(result.http_status) is int else None
        status_text = f" (HTTP status: {status})" if status is not None else ""
        alert = f"Approver preflight blocked: `{capability}` — {_APPROVER_PREFLIGHT_DIAGNOSTIC}{status_text}"
        step_summary_path = os.environ.get("GITHUB_STEP_SUMMARY", "")
        if step_summary_path:
            try:
                with open(step_summary_path, "a", encoding="utf-8") as step_summary:
                    step_summary.write(f"- {alert}\n")
            except OSError:
                logger.warning("Failed to append approver preflight alert to GitHub step summary")
        print(f"::warning::Approver preflight blocked: {capability} — {_APPROVER_PREFLIGHT_DIAGNOSTIC}{status_text}")


def render_summary_comment(summary: PipelineRunSummary) -> str:
    """Render the pipeline run summary as a markdown comment.

    Includes:
    - Header with trigger reason and link to workflow run
    - Action evaluation table (collapsed)
    - Collapsed state snapshot details
    """
    lines: list[str] = []

    # Sentinel for identification
    lines.append(SUMMARY_SENTINEL)
    lines.append("")

    # Header with trigger reason and link
    header = "#### 🤖 AI PR Loop Run"
    trigger_reason = _sanitize_single_line(summary.trigger_reason)
    run_url = _sanitize_run_url(summary.run_url)
    if trigger_reason:
        header += f" — Trigger Reason: {trigger_reason}"
    if run_url:
        header += f" — [View Logs]({run_url})"
    lines.append(header)
    lines.append("")
    for result in summary.results:
        if result.dedup_limit_reached:
            lines.append(f"**Repair budget exhausted** — {_sanitize_single_line(result.details)}")
            if result.repair_exhaustion_marker:
                lines.append(result.repair_exhaustion_marker)
            lines.append("")

    # Outer Details wrapper — keeps the sentinel and header visible while
    # collapsing the action table and state snapshot behind a single toggle.
    lines.append("<details>")
    lines.append("     <summary>Details</summary>")
    lines.append("")

    # Action table (collapsed)
    lines.append("<details>")
    lines.append("     <summary>Actions table</summary>")
    lines.append("")
    lines.append("| Action | Preconditions | Result |")
    lines.append("|--------|--------------|--------|")

    for result in summary.results:
        icon = _DECISION_ICONS.get(result.decision, "❓")
        label = _DECISION_LABELS.get(result.decision, result.decision.value)
        precond_text = _sanitize_cell(_format_preconditions(result))
        detail_parts: list[str] = []
        if result.details and result.decision in {
            ActionDecision.EXECUTE,
            ActionDecision.FAILED,
            ActionDecision.SKIP,
            ActionDecision.BLOCKED,
            ActionDecision.BLOCKED_BY_GUARD,
        }:
            detail_parts.append(_sanitize_cell(result.details))
        if result.error and result.decision == ActionDecision.FAILED:
            detail_parts.append(f"error: {_sanitize_cell(result.error)}")
        detail_text = f" ({'; '.join(detail_parts)})" if detail_parts else ""
        lines.append(f"| {_sanitize_cell(result.name)} | {icon} {precond_text} | {label}{detail_text} |")

    lines.append("")
    lines.append("</details>")
    lines.append("")

    # State snapshot (collapsed)
    if summary.snapshot:
        lines.append("<details>")
        lines.append("     <summary>State snapshot</summary>")
        lines.append("")
        lines.append(
            _render_state_snapshot(
                summary.snapshot,
                summary.derived_unresolved_threads,
                summary.session_evidence,
            )
        )
        lines.append("</details>")
        lines.append("")

    # Close outer Details wrapper
    lines.append("</details>")
    lines.append("")

    return "\n".join(lines)


def _format_preconditions(result: ActionResult) -> str:
    """Format preconditions into a short summary string.

    Every failing precondition is rendered, not just the first one: a composite
    skip has more than one cause and showing a single key makes the posted
    comment undiagnosable.
    """
    if not result.preconditions:
        return "—"

    # Show every failing precondition so composite skips are fully diagnosable
    parts = [f"✗ {key}" for key, value in result.preconditions.items() if not value]
    if not parts:
        parts.append("all passed")

    return ", ".join(parts)[:_PRECONDITION_CLIP_LENGTH]


def collapse_prior_summaries(
    provider: CIPlatformProvider,
    pr_number: int,
    *,
    keep_active_id: int | None = None,
) -> int:
    """Find and collapse prior summary comments.

    Finds comments with the active sentinel and replaces it with the
    collapsed sentinel. If ``keep_active_id`` is supplied, that comment
    is preserved as active.

    Returns:
        Number of comments collapsed.
    """
    collapsed_count = 0

    list_issue_comments = getattr(provider, "list_issue_comments", None)
    if callable(list_issue_comments):
        trusted_authors = trusted_loop_comment_logins(provider)
        comments = list_issue_comments(pr_number)
        get_pr_token_login = getattr(provider, "get_pr_token_login", None)
        pr_token_login = get_pr_token_login().strip().casefold() if callable(get_pr_token_login) else ""
        newer_collapsed_summaries: dict[str, int] = {}
        for comment in comments:
            body = comment.body or ""
            author = comment.author or ""
            if (
                not body.startswith(SUMMARY_COLLAPSED_SENTINEL)
                or "AI PR Loop Run" not in body
                or not _is_editable_summary_comment_author(author=author, trusted_authors=trusted_authors)
            ):
                continue
            signature = _summary_state_signature(body)
            if signature is not None:
                newer_collapsed_summaries[signature] = max(
                    comment.id,
                    newer_collapsed_summaries.get(signature, 0),
                )

        for comment in comments:
            if keep_active_id is not None and comment.id == keep_active_id:
                continue
            body = comment.body or ""
            if SUMMARY_SENTINEL not in body or SUMMARY_COLLAPSED_SENTINEL in body:
                continue
            # Same safeguards as the fallback path: only collapse comments that
            # start with the sentinel and contain the expected pipeline header,
            # to avoid editing unrelated bot comments that happen to quote the marker.
            if not body.startswith(SUMMARY_SENTINEL) or "AI PR Loop Run" not in body:
                logger.info(
                    "PR #%d: Skipping comment %d — body does not match expected pipeline format",
                    pr_number,
                    comment.id,
                )
                continue
            author = comment.author or ""
            if not _is_editable_summary_comment_author(author=author, trusted_authors=trusted_authors):
                logger.info("PR #%d: Skipping non-bot summary marker comment %d", pr_number, comment.id)
                continue
            signature = _summary_state_signature(body)
            if signature is not None and newer_collapsed_summaries.get(signature, 0) > comment.id:
                continue
            if author.strip().casefold() == pr_token_login:
                continue
            collapsed_body = body.replace(SUMMARY_SENTINEL, SUMMARY_COLLAPSED_SENTINEL, 1)
            try:
                provider.update_comment(comment.id, collapsed_body)
                collapsed_count += 1
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError):
                    raise
                logger.warning("PR #%d: Failed to collapse comment %d: %s", pr_number, comment.id, exc)
        return collapsed_count

    # Fallback: use provider's find_comment to locate summaries.
    # Search for concrete summary header variants to stay format-agnostic
    # while avoiding broad sentinel-only substring matches.
    # We may need to iterate; find_comment returns first match
    while True:
        found: tuple[int, str] | None = None
        for marker in SUMMARY_FALLBACK_MARKERS:
            found = provider.find_comment(pr_number, marker)
            if found is not None:
                break
        if found is None:
            break

        comment_id, body = found
        if keep_active_id is not None and comment_id == keep_active_id:
            break

        # Safeguard: only collapse comments whose body starts with the sentinel and
        # contains the expected pipeline header, to avoid editing unrelated user
        # comments that happen to include the marker text.
        if not body.startswith(SUMMARY_SENTINEL) or "AI PR Loop Run" not in body:
            logger.info(
                "PR #%d: Skipping comment %d in fallback path — body does not match expected pipeline format",
                pr_number,
                comment_id,
            )
            break

        # Replace sentinel only
        collapsed_body = body.replace(SUMMARY_SENTINEL, SUMMARY_COLLAPSED_SENTINEL, 1)

        try:
            provider.update_comment(comment_id, collapsed_body)
            collapsed_count += 1
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError):
                raise
            logger.warning("PR #%d: Failed to collapse comment %d: %s", pr_number, comment_id, exc)
            break

    return collapsed_count


def _find_active_summary_comment(
    provider: CIPlatformProvider,
    pr_number: int,
) -> tuple[int, str] | None:
    """Find an existing active summary comment for the given PR."""
    list_issue_comments = getattr(provider, "list_issue_comments", None)
    if callable(list_issue_comments):
        try:
            trusted_authors = trusted_loop_comment_logins(provider)
            comments = list_issue_comments(pr_number)
            if isinstance(comments, list):
                newer_collapsed_summaries: dict[str, int] = {}
                for comment in comments:
                    body = comment.body or ""
                    author = comment.author or ""
                    if (
                        body.startswith(SUMMARY_COLLAPSED_SENTINEL)
                        and "AI PR Loop Run" in body
                        and _is_editable_summary_comment_author(author=author, trusted_authors=trusted_authors)
                    ):
                        signature = _summary_state_signature(body)
                        if signature is not None:
                            newer_collapsed_summaries[signature] = max(
                                comment.id,
                                newer_collapsed_summaries.get(signature, 0),
                            )

                active_comments: list[tuple[int, str]] = []
                for comment in comments:
                    body = comment.body or ""
                    if (
                        SUMMARY_COLLAPSED_SENTINEL in body
                        or not body.startswith(SUMMARY_SENTINEL)
                        or "AI PR Loop Run" not in body
                    ):
                        continue
                    author = comment.author or ""
                    if not _is_editable_summary_comment_author(author=author, trusted_authors=trusted_authors):
                        continue
                    signature = _summary_state_signature(body)
                    if signature is not None and newer_collapsed_summaries.get(signature, 0) > comment.id:
                        continue
                    normalized_body = normalize_ai_pr_loop_comment(body)
                    if normalized_body is not None:
                        active_comments.append((comment.id, normalized_body))
                if active_comments:
                    return max(active_comments, key=lambda item: item[0])
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError):
                raise
            logger.warning("PR #%d: Failed to list issue comments: %s", pr_number, exc)
        return None

    # Fallback to find_comment
    try:
        for marker in SUMMARY_FALLBACK_MARKERS:
            found = provider.find_comment(pr_number, marker)
            if found is not None:
                comment_id, body = found
                if body.startswith(SUMMARY_SENTINEL) and "AI PR Loop Run" in body:
                    normalized_body = normalize_ai_pr_loop_comment(body)
                    if normalized_body is not None:
                        return (comment_id, normalized_body)
    except Exception as exc:
        if isinstance(exc, ProviderRateLimitError):
            raise
        logger.warning("PR #%d: Failed to find summary comment: %s", pr_number, exc)
    return None


def _normalize_summary_for_comparison(body: str) -> str:
    """Normalize a summary comment body by standardizing the header line.

    Used to detect identical no-op passes where updating the comment in place
    would produce no semantic change to the actions table or state snapshot.
    """
    normalized_body = normalize_ai_pr_loop_comment(body)
    if normalized_body is not None:
        body = normalized_body

    lines: list[str] = []
    for line in body.splitlines():
        if line.startswith("#### 🤖 AI PR Loop Run") or line.startswith("**🤖 AI PR Loop Run**"):
            lines.append("#### 🤖 AI PR Loop Run")
        else:
            lines.append(line)
    return "\n".join(lines).strip()


def _is_identical_noop_pass(summary: PipelineRunSummary, existing_body: str, new_body: str) -> bool:
    """Return True if this run made no progress and matches the existing summary."""
    if any(r.decision in (ActionDecision.EXECUTE, ActionDecision.FAILED) for r in summary.results):
        return False
    return _normalize_summary_for_comparison(existing_body) == _normalize_summary_for_comparison(new_body)


def post_summary_comment(
    provider: CIPlatformProvider,
    pr_number: int,
    summary: PipelineRunSummary,
) -> bool:
    """Post or update a pipeline summary comment.

    Strictly updates the existing summary comment in place (``provider.update_comment``).
    Only posts a new comment if none exists.
    Suppresses updates on identical no-op passes.
    Collapses surplus duplicate summary comments if multiple active summaries exist.

    Returns True on success, False on failure (non-fatal).
    """
    comment_body = render_summary_comment(summary)
    _emit_approver_preflight_alerts(summary.results)
    # Locate existing active summary comment
    existing_comment = _find_active_summary_comment(provider, pr_number)
    existing_id = existing_comment[0] if existing_comment else None

    # Collapse any surplus prior summaries, keeping existing_id active
    try:
        collapsed = collapse_prior_summaries(provider, pr_number, keep_active_id=existing_id)
        if collapsed:
            logger.info("PR #%d: Collapsed %d prior summary comment(s)", pr_number, collapsed)
    except Exception as exc:
        if isinstance(exc, ProviderRateLimitError):
            raise
        logger.warning("PR #%d: Failed to collapse prior summaries: %s", pr_number, exc)

    if existing_comment is not None:
        comment_id, existing_body = existing_comment
        if _is_identical_noop_pass(summary, existing_body, comment_body):
            logger.info("PR #%d: Suppressing summary comment update on identical no-op pass", pr_number)
            return True

        try:
            provider.update_comment(comment_id, comment_body)
            logger.info("PR #%d: Updated pipeline summary comment %d in place", pr_number, comment_id)
            return True
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError):
                raise
            logger.warning("PR #%d: Failed to update summary comment %d: %s", pr_number, comment_id, exc)
            return False

    # No existing active summary comment — post a new one
    try:
        provider.post_comment(pr_number, comment_body)
        logger.info("PR #%d: Posted pipeline summary comment", pr_number)
        return True
    except Exception as exc:
        if isinstance(exc, ProviderRateLimitError):
            raise
        logger.warning("PR #%d: Failed to post summary comment: %s", pr_number, exc)
        return False

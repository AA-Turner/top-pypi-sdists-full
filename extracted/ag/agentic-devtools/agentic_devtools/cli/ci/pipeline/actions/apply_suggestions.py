"""Apply suggestions action — auto-applies review suggestions before repair dispatch.

Supports two types of suggestions:
1. Standard ``suggestion`` fenced blocks in comment bodies (via GraphQL)
2. Copilot "Suggested changeset" diffs (via page HTML scraping fallback)

The page-scraping fallback activates when no standard suggestion blocks are found
but an actionable Copilot review exists with inline comments.
"""

from __future__ import annotations

import logging
import os

from agentic_devtools.cli.ci.pipeline.discovery import (
    DiscoveryAttempt,
    DiscoveryOutcome,
    has_inline_evidence,
    run_discovery,
)
from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.suggestions import (
    ApplySuggestionsResult,
    apply_suggestions_with_bisection,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)

# Safety threshold: do not apply more than this many suggestions in one action
_MAX_SUGGESTIONS_THRESHOLD = 50

# Maximum number of autofix cycles per PR before permanently skipping
_MAX_AUTOFIX_CYCLES = 20


def _raise_if_rate_limit(exc: Exception) -> None:
    if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
        raise


class ApplySuggestionsAction:
    """Apply autofixable review suggestions via GraphQL before repair dispatch.

    Positioned after GuardsAction and PublishAction, before DispatchRepairAction.
    When suggestions are successfully applied, sets ``invalidates_snapshot = True``
    to trigger a snapshot refresh for downstream actions.

    Preconditions:
    - Actionable Copilot review exists with suggestions
    - Suggestion count ≤ threshold (50)
    - Not blocked by guards (fork, privileged paths, etc.)
    """

    @property
    def name(self) -> str:
        return "apply_suggestions"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate whether suggestions can be applied.

        Checks that:
        1. Feature is enabled via ENABLE_AUTO_APPLY_SUGGESTIONS env var
        2. There is an actionable Copilot review with inline comments
        3. The review has suggestions that can be applied
        """
        preconditions: dict[str, bool] = {}

        # Feature gate: repository variable must explicitly enable this action.
        # Defaults to disabled for safety — operator must set ENABLE_AUTO_APPLY_SUGGESTIONS=true
        # in repository Actions variables to activate.
        enabled = os.environ.get("ENABLE_AUTO_APPLY_SUGGESTIONS", "").lower() == "true"
        preconditions["feature_enabled"] = enabled
        if not enabled:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Auto-apply suggestions disabled (ENABLE_AUTO_APPLY_SUGGESTIONS != 'true')",
            )

        # Must have an actionable review:
        # - CHANGES_REQUESTED is actionable when a Copilot review exists
        # - COMMENTED is actionable only when inline count is non-zero (or unknown=-1)
        # - OR: unresolved threads exist from reviews not owned by the gate verdict
        #   (suggestions may still be applicable even though the review is no longer
        #   the one the gate verdict accounts for)
        has_actionable_review = snapshot.copilot_review_id > 0 and (
            snapshot.review_state == "CHANGES_REQUESTED"
            or (snapshot.review_state == "COMMENTED" and snapshot.copilot_review_inline_count != 0)
        )
        has_repairable_threads = snapshot.repairable_threads > 0
        preconditions["has_actionable_review"] = has_actionable_review or has_repairable_threads

        if not has_actionable_review and not has_repairable_threads:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="No actionable Copilot review with suggestions",
            )

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details="Actionable review detected — will attempt to apply suggestions",
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Execute suggestion application via the discovery orchestrator.

        1. Check autofix cycle limit
        2. Run discovery orchestrator (GraphQL → REST → HTML)
        3. If inconclusive, post deferral marker
        4. Check threshold
        5. Attempt batch apply
        6. Fall back to bisection on conflict
        7. Populate ExclusionContext for downstream actions
        """
        # Check autofix cycle limit — prevents infinite loops where review
        # suggestions repeatedly fail CI after being applied.
        # _count_prior_autofix_comments handles its own exceptions (fail-open, returns 0).
        prior_autofix_count = _count_prior_autofix_comments(provider, snapshot.pr_number)
        if prior_autofix_count >= _MAX_AUTOFIX_CYCLES:
            logger.warning(
                "PR #%d: Autofix cycle limit reached (%d/%d) — skipping",
                snapshot.pr_number,
                prior_autofix_count,
                _MAX_AUTOFIX_CYCLES,
            )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions={"cycle_limit_reached": True},
                details=f"Autofix cycle limit reached ({prior_autofix_count}/{_MAX_AUTOFIX_CYCLES})",
            )

        # Resolve repo name for HTML strategy
        repo = getattr(provider, "_repo", None) or os.environ.get("GITHUB_REPOSITORY", "")

        # Run discovery orchestrator (priority: GraphQL → REST → HTML)
        suggestions, discovery_attempts, pr_node_id = run_discovery(
            provider,
            snapshot,
            repo=repo,
        )

        # Format discovery diagnostics for details
        discovery_details = _format_discovery_details(discovery_attempts, snapshot)

        if not suggestions:
            # Only try the legacy Copilot autofix fallback when the html-scrape
            # strategy confirmed candidate autofix entries exist (outcome=SUCCESS).
            # When html-scrape already returned EMPTY there is nothing to apply,
            # so invoking the fallback would just re-scrape the PR page a second
            # time and add avoidable latency.
            fallback_result = None
            if _html_scrape_succeeded(discovery_attempts):
                try:
                    fallback_result = _try_legacy_autofix_fallback(provider, snapshot, repo)
                except Exception as exc:
                    _raise_if_rate_limit(exc)
                    logger.warning(
                        "PR #%d: Legacy autofix fallback raised — treating as no suggestions",
                        snapshot.pr_number,
                        exc_info=True,
                    )
                    fallback_result = None
            if fallback_result is not None:
                if fallback_result.get("exclusion_ctx"):
                    derived.set("exclusion_context", fallback_result["exclusion_ctx"])
                action_result = fallback_result["action_result"]
                if action_result.decision == ActionDecision.EXECUTE:
                    derived.set("autofix_applied_this_iteration", True)
                return action_result

            # Post deferral marker if inconclusive (inline evidence exists
            # but no suggestions discovered)
            if has_inline_evidence(snapshot) and _all_discovery_attempts_empty(discovery_attempts):
                _post_deferral_if_needed(provider, snapshot)

            details = f"No applicable suggestions found. {discovery_details}"
            logger.info("PR #%d: %s", snapshot.pr_number, details)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions={"suggestions_found": False},
                details=details,
            )

        # Check threshold (FR-011)
        if len(suggestions) > _MAX_SUGGESTIONS_THRESHOLD:
            logger.warning(
                "PR #%d: Suggestion count %d exceeds threshold %d — deferring to repair",
                snapshot.pr_number,
                len(suggestions),
                _MAX_SUGGESTIONS_THRESHOLD,
            )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions={"suggestions_found": True, "within_threshold": False},
                details=f"Suggestion count ({len(suggestions)}) exceeds threshold ({_MAX_SUGGESTIONS_THRESHOLD})",
            )

        suggestion_ids = [s.suggestion_id for s in suggestions]
        logger.info(
            "PR #%d: Applying %d suggestions via createCommitOnBranch (sources: %s)",
            snapshot.pr_number,
            len(suggestion_ids),
            ", ".join(sorted({s.discovery_source for s in suggestions})),
        )

        # Apply suggestions — batch first, bisection fallback on conflict
        try:
            result = apply_suggestions_with_bisection(
                provider,
                pr_node_id,
                suggestion_ids,
                suggestions=suggestions,
                head_ref=snapshot.head_branch,
                head_oid=snapshot.head_sha,
            )
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.warning("PR #%d: Failed to apply suggestions: %s", snapshot.pr_number, exc)
            # Return SKIP (not FAILED) to avoid halting pipeline per FR-010
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions={"suggestions_found": True, "within_threshold": True},
                details=f"Failed to apply suggestions: {exc}",
            )

        # If nothing was applied, return SKIP
        if not result.applied_ids:
            logger.info(
                "PR #%d: No suggestions could be applied (error=%s)",
                snapshot.pr_number,
                result.error,
            )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions={"suggestions_found": True, "within_threshold": True},
                details=f"No suggestions applied: {result.error or 'all conflicted'}",
            )

        # Build ExclusionContext — only mark a comment as resolved when ALL its
        # applicable suggestions were successfully applied. Partial application
        # (some suggestions conflicted/skipped) leaves the comment visible to the
        # repair agent so the remaining feedback is not silently dropped.
        applied_suggestion_ids_set = set(result.applied_ids)

        comment_suggestions: dict[int, list[str]] = {}
        for s in suggestions:
            comment_suggestions.setdefault(s.comment_database_id, []).append(s.suggestion_id)

        resolved_comment_ids: set[int] = {
            comment_id
            for comment_id, sids in comment_suggestions.items()
            if all(sid in applied_suggestion_ids_set for sid in sids)
        }

        exclusion_ctx = ExclusionContext(resolved_comment_ids=resolved_comment_ids)
        derived.set("exclusion_context", exclusion_ctx)

        logger.info(
            "PR #%d: Applied %d suggestions, skipped %d (commits=%s)",
            snapshot.pr_number,
            len(result.applied_ids),
            len(result.skipped_ids),
            result.commit_shas,
        )

        # Post summary comment (FR — User Story 5)
        _post_summary_comment(provider, snapshot.pr_number, result)

        # Signal to resolve_threads to skip SDK evaluation — remaining
        # threads haven't been addressed yet (no repair has run).
        derived.set("autofix_applied_this_iteration", True)

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions={"suggestions_found": True, "within_threshold": True},
            details=(
                f"Applied {len(result.applied_ids)} suggestions"
                f" (skipped={len(result.skipped_ids)}, commits={len(result.commit_shas)})"
                f" [{discovery_details}]"
            ),
            invalidates_snapshot=True,
        )


def _post_summary_comment(
    provider: CIPlatformProvider,
    pr_number: int,
    result: ApplySuggestionsResult,
) -> None:
    """Post a summary comment about applied suggestions."""
    if not result.applied_ids:
        return

    applied_count = len(result.applied_ids)
    skipped_count = len(result.skipped_ids)

    body_parts = [
        f"🔧 **Auto-applied {applied_count} suggestion{'s' if applied_count != 1 else ''}**",
    ]

    if result.commit_shas:
        commit_shas = [sha for sha in result.commit_shas if sha != "pending_refresh"]
        if commit_shas:
            sha_list = ", ".join(f"`{sha[:7]}`" for sha in commit_shas)
            commit_word = "commit" if len(commit_shas) == 1 else "commits"
            body_parts.append(f" in {commit_word} {sha_list}")

    if skipped_count > 0:
        suffix = "s" if skipped_count != 1 else ""
        skip_reason = "conflict/outdated"
        if result.error:
            first_nonempty_line = next((line.strip() for line in result.error.splitlines() if line.strip()), "")
            if first_nonempty_line:
                skip_reason = first_nonempty_line
        body_parts.append(f"\n\n⚠️ {skipped_count} suggestion{suffix} could not be applied ({skip_reason}).")

    body = "".join(body_parts)

    try:
        provider.post_comment(pr_number, body)
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.warning("PR #%d: Failed to post suggestion summary comment: %s", pr_number, exc)


def _count_prior_autofix_comments(
    provider: CIPlatformProvider,
    pr_number: int,
) -> int:
    """Count prior autofix summary comments to enforce cycle limit.

    Counts PR issue comments containing the distinctive autofix summary prefix.
    This provides a persistent, cross-run counter without requiring external state.
    """
    try:
        comments = provider.list_issue_comments(pr_number)
    except Exception as exc:
        _raise_if_rate_limit(exc)
        return 0

    count = 0
    for comment in comments:
        body = getattr(comment, "body", "") or ""
        if "🔧 **Auto-applied" in body:
            count += 1
    return count


def _format_discovery_details(
    attempts: list[DiscoveryAttempt],
    snapshot: PRStateSnapshot,
) -> str:
    """Format discovery attempt diagnostics into a human-readable string."""
    if not attempts:
        return "no discovery attempts"
    parts = []
    for a in attempts:
        status = a.outcome.value
        if a.error_message:
            normalized = " ".join(a.error_message.split())
            status += f"({normalized[:200]})"
        elif a.suggestion_count:
            status += f"({a.suggestion_count})"
        parts.append(f"{a.method}={status}")
    inline_info = f"inline_comments={snapshot.copilot_review_inline_count}"
    return f"{inline_info}, sources=[{', '.join(parts)}]"


def _all_discovery_attempts_empty(attempts: list[DiscoveryAttempt]) -> bool:
    """Return True when every recorded discovery attempt was inconclusive/empty."""
    return bool(attempts) and all(a.outcome is DiscoveryOutcome.EMPTY for a in attempts)


def _html_scrape_succeeded(attempts: list[DiscoveryAttempt]) -> bool:
    """Return True when the html-scrape strategy returned SUCCESS outcome.

    ``html_discover`` returns outcome=SUCCESS (with suggestion_count > 0) when it
    detects diff entries on the PR page but does not convert them to SuggestedChange
    objects itself — the conversion is done by the legacy ``apply_pr_suggestions``
    flow.  Checking for SUCCESS here avoids a redundant re-scrape when the HTML
    strategy already confirmed nothing was present (outcome=EMPTY).
    """
    return any(a.method == "html-scrape" and a.outcome is DiscoveryOutcome.SUCCESS for a in attempts)


def _post_deferral_if_needed(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
) -> None:
    """Post a deferral marker if discovery was inconclusive."""
    try:
        from agentic_devtools.cli.ci.pipeline.deferral import post_deferral_marker

        post_deferral_marker(provider, snapshot.pr_number, snapshot.copilot_review_id)
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.warning(
            "PR #%d: Failed to post deferral marker: %s",
            snapshot.pr_number,
            exc,
        )


def _try_legacy_autofix_fallback(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    _repo: str,
) -> dict | None:
    """Try legacy Copilot autofix fallback for HTML-based suggestions.

    This handles the case where HTML-scraped suggestions require the full
    apply_pr_suggestions flow (direct diff application via Contents API)
    rather than the createCommitOnBranch mutation.

    Returns a dict with ``action_result`` and ``exclusion_ctx`` if suggestions
    were found and processed, or None if nothing was found.
    """
    return _apply_copilot_autofix_suggestions(provider, snapshot)


def _apply_copilot_autofix_suggestions(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
) -> dict | None:
    """Try to apply Copilot 'Suggested changeset' diffs via page HTML scraping.

    This is the fallback for when standard ```suggestion blocks are not found.
    Copilot code review uses a proprietary "autofix" format that stores suggestion
    diffs in embedded React partial JSON within the PR page HTML.

    Returns a dict with ``action_result`` (ActionResult) and ``exclusion_ctx``
    (ExclusionContext or None) if suggestions were found and processed, or None
    if no Copilot autofix suggestions exist.

    On any error, returns None (fail-open, per FR-010 — does not halt the pipeline).
    """
    from agentic_devtools.cli.github.apply_thread_autofix import apply_pr_suggestions

    # Resolve repo name from provider or environment
    repo = getattr(provider, "_repo", None) or os.environ.get("GITHUB_REPOSITORY", "")
    if not repo:
        logger.warning(
            "PR #%d: Copilot autofix fallback skipped — repo could not be determined "
            "(set GITHUB_REPOSITORY or ensure provider._repo is populated)",
            snapshot.pr_number,
        )
        return None

    logger.info(
        "PR #%d: No standard suggestion blocks found, trying Copilot autofix fallback",
        snapshot.pr_number,
    )

    try:
        result = apply_pr_suggestions(
            pr_number=snapshot.pr_number,
            repo=repo,
            comment_ids=None,
            message="Apply suggestions from code review",
            resolve=True,
        )
    except SystemExit:
        # apply_pr_suggestions may call sys.exit on fatal errors (e.g., gh not found)
        # In pipeline context, treat as non-fatal skip
        logger.warning(
            "PR #%d: Copilot autofix fallback exited — treating as skip",
            snapshot.pr_number,
        )
        return None
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.warning(
            "PR #%d: Copilot autofix fallback error: %s",
            snapshot.pr_number,
            exc,
        )
        return None

    applied = result.get("applied", 0)
    skipped = result.get("skipped", 0)
    commit = result.get("commit")

    if applied == 0 and skipped == 0:
        # No Copilot autofix suggestions found at all
        return None

    logger.info(
        "PR #%d: Copilot autofix — applied %d, skipped %d, commit=%s",
        snapshot.pr_number,
        applied,
        skipped,
        commit[:12] if commit else "none",
    )

    # Threads are already resolved by apply_pr_suggestions via GraphQL.
    # The snapshot refresh (triggered by invalidates_snapshot=True) will pick
    # up the resolved state. No ExclusionContext is needed here.
    exclusion_ctx = None

    if applied > 0:
        action_result = ActionResult(
            name="apply_suggestions",
            decision=ActionDecision.EXECUTE,
            preconditions={"suggestions_found": True, "within_threshold": True},
            details=(
                f"Copilot autofix: applied {applied} suggestion(s)"
                f"{f', skipped {skipped}' if skipped else ''}"
                f" (commit={commit[:12] if commit else 'none'})"
            ),
            invalidates_snapshot=True,
        )
    else:
        action_result = ActionResult(
            name="apply_suggestions",
            decision=ActionDecision.SKIP,
            preconditions={"suggestions_found": True, "within_threshold": True},
            details=f"Copilot autofix: all {skipped} suggestions conflicted/stale",
        )

    return {"action_result": action_result, "exclusion_ctx": exclusion_ctx}

"""Merge action — merges PR when all conditions are met."""

from __future__ import annotations

import logging

from agentic_devtools.cli.ci.guards import LABEL_AUTO_MERGE_ALLOWED
from agentic_devtools.cli.ci.pipeline.deferral import find_suppressed_deferral_state
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    copilot_review_gate_passed,
    suppressed_deferral_recorded,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot import (
    DerivedState,
    PRStateSnapshot,
    has_non_copilot_changes_requested_on_head,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)


def _build_squash_commit_title(snapshot: PRStateSnapshot) -> str:
    """Build a descriptive commit title for squash merges.

    Uses the PR title as the commit subject line with the PR number appended.
    """
    if snapshot.title:
        return f"{snapshot.title} (#{snapshot.pr_number})"
    return f"PR #{snapshot.pr_number}"


class MergeAction:
    """Merge the PR when fully ready.

    Preconditions:
    - Approved: precise approver-PAT approval on HEAD
    - CI passing
    - `ai-auto-merge-allowed` label present
    - PR is mergeable
    - No unresolved threads
    - No pending Copilot review
    - No effective non-Copilot CHANGES_REQUESTED review on HEAD
    - Copilot review on HEAD exists and is non-actionable (clean)

    Idempotency: Already merged → skip merge_pr call, resume post-merge operations
    (``snapshot.mergeable_state == "merged"``).
    """

    @property
    def name(self) -> str:
        return "merge"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate whether the PR can be merged."""
        preconditions: dict[str, bool] = {}

        repair_dispatched = derived.get("repair_dispatched", False)
        preconditions["no_repair_dispatched"] = not repair_dispatched
        if repair_dispatched:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Repair dispatched — deferring merge",
            )

        # Not a draft — use derived so PublishAction's same-run effect is visible
        is_not_draft = not derived.is_draft
        preconditions["not_draft"] = is_not_draft
        if not is_not_draft:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="PR is a draft",
            )

        # Must have the precise loop/code-owner approval on HEAD. This stays False when
        # approver-login resolution is unavailable and approval could not be submitted,
        # which fail-closes merge rather than letting an unrelated human approval satisfy
        # the branch-protection gate. Same-run approval is still visible because
        # ApproveAction.execute() sets ``has_approver_approval_on_head`` on derived state.
        has_approval = derived.has_approver_approval_on_head
        preconditions["approved"] = has_approval
        if not has_approval:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="PR not approved by loop/code-owner on HEAD",
            )

        # CI passing
        preconditions["ci_passing"] = snapshot.ci_status == "passing"
        if snapshot.ci_status != "passing":
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=f"CI is {snapshot.ci_status}",
            )

        # Auto-merge label
        has_label = LABEL_AUTO_MERGE_ALLOWED in snapshot.labels
        preconditions["has_auto_merge_label"] = has_label
        if not has_label:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Missing 'ai-auto-merge-allowed' label",
            )

        # Mergeable
        is_mergeable = snapshot.mergeable is not False  # None treated as potentially mergeable
        preconditions["mergeable"] = is_mergeable
        if not is_mergeable:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="PR is not mergeable",
            )

        # Review-thread state must be known. When the provider cannot report it, the
        # unresolved-thread count is unknown — fail closed rather than merge on a
        # count that only looks clean because a capability is missing.
        thread_state_known = not derived.unresolved_threads_degraded
        preconditions["thread_state_known"] = thread_state_known
        if not thread_state_known:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Unresolved thread count is degraded / unknown (provider cannot report review-thread state)",
            )

        # No unresolved threads — consult derived state so same-run ResolveThreadsAction
        # effects are visible (avoids a second workflow trigger after thread resolution).
        unresolved = derived.unresolved_threads
        preconditions["no_unresolved_threads"] = unresolved == 0
        if unresolved > 0:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=f"{unresolved} unresolved thread(s)",
            )

        # No pending Copilot review (check derived in case request_review just ran)
        has_pending_review = derived.copilot_review_pending
        preconditions["no_pending_review"] = not has_pending_review
        if has_pending_review:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Copilot review is pending",
            )

        # No non-Copilot CHANGES_REQUESTED on HEAD
        has_human_changes_requested = has_non_copilot_changes_requested_on_head(snapshot.reviews, snapshot.head_sha)
        preconditions["no_human_changes_requested"] = not has_human_changes_requested
        if has_human_changes_requested:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Non-Copilot reviewer requested changes on current HEAD",
            )

        # Shared gate predicate: this is the single source of truth used by squash too.
        # It handles the verdict path (including the fail-closed suppressed-only bypass)
        # and legacy fallback when no verdict is available.
        deferred_review_id = derived.get("suppressed_deferral_review_id")
        review_clean = copilot_review_gate_passed(
            snapshot,
            unresolved_threads=derived.unresolved_threads,
            deferred_review_id=deferred_review_id if isinstance(deferred_review_id, int) else None,
        )
        gate_verdict = snapshot.copilot_gate_verdict
        if gate_verdict is not None:
            preconditions["gate_verdict_passed"] = gate_verdict.passed
            if not gate_verdict.passed:
                deferral_cleared = suppressed_deferral_recorded(
                    gate_verdict,
                    deferred_review_id=deferred_review_id if isinstance(deferred_review_id, int) else None,
                    head_changed_since_review=snapshot.head_changed_since_review,
                    unresolved_threads=derived.unresolved_threads,
                )
                preconditions["suppressed_deferral_recorded"] = deferral_cleared
                preconditions["suppressed_comments_evaluated"] = review_clean and not deferral_cleared
                if review_clean:
                    logger.info(
                        "PR #%d: Suppressed-only gate block cleared by %s (review %d) — proceeding with merge",
                        snapshot.pr_number,
                        "suppressed-comment deferral" if deferral_cleared else "repair-satisfied marker",
                        gate_verdict.review_id,
                    )
        else:
            # Legacy path: check review existence and cleanliness separately.
            has_copilot_review = snapshot.copilot_review_id > 0 and bool(snapshot.review_state)
            preconditions["has_copilot_review"] = has_copilot_review
            if not has_copilot_review:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.SKIP,
                    preconditions=preconditions,
                    details="No Copilot review on HEAD",
                )

            preconditions["review_clean"] = review_clean

        if not review_clean:
            if gate_verdict is not None:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.SKIP,
                    preconditions=preconditions,
                    details=f"Copilot gate: {gate_verdict.reason} — {gate_verdict.details}",
                )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=(
                    f"Copilot review is actionable "
                    f"(state={snapshot.review_state}, inline={snapshot.copilot_review_inline_count})"
                ),
            )

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details="All merge conditions met",
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Execute the merge."""
        # Use squash merge for multi-commit PRs to maintain clean history
        commit_count = getattr(derived, "commit_count", snapshot.commit_count)
        if commit_count > 1:
            method = "squash"
            commit_title = _build_squash_commit_title(snapshot)
        else:
            method = "rebase"
            commit_title = None

        # Idempotency: skip the merge call when the PR is already merged.  This
        # happens on a re-trigger after a post-merge dispatch failure: the first
        # run merged the PR (setting mergeable_state="merged" in the GitHub API
        # response), but dispatch_suppressed_triage raised so the run returned
        # FAILED.  Closed/merged PRs are still enumerated when the pipeline is
        # re-triggered manually, so without this guard the re-trigger would call
        # merge_pr again (receiving a 405 "not mergeable"), return FAILED from
        # the exception handler above, and never reach the dispatch block.
        already_merged = snapshot.mergeable_state == "merged"
        if already_merged:
            logger.info(
                "PR #%d: Already merged (mergeable_state=%s) — skipping merge, resuming post-merge operations",
                snapshot.pr_number,
                snapshot.mergeable_state,
            )
        else:
            try:
                if method == "squash" and commit_title:
                    provider.merge_pr(snapshot.pr_number, snapshot.head_sha, method, commit_title=commit_title)
                else:
                    provider.merge_pr(snapshot.pr_number, snapshot.head_sha, method)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError):
                    raise
                logger.error("PR #%d: Merge failed: %s", snapshot.pr_number, exc)
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.FAILED,
                    error=str(exc),
                    details="merge_pr call failed",
                )

        # Delete the source branch after successful merge
        if snapshot.head_branch:
            try:
                provider.delete_branch(snapshot.head_branch)
                logger.info("PR #%d: Deleted branch %s", snapshot.pr_number, snapshot.head_branch)
            except Exception as exc:
                # Branch deletion is best-effort; don't fail the merge action
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning(
                    "PR #%d: Failed to delete branch %s: %s",
                    snapshot.pr_number,
                    snapshot.head_branch,
                    exc,
                )

        # Dispatch the suppressed-comment triage agent after a successful merge so that
        # its working tree is based on `main` containing the parent PR's changes.
        # `suppressed_deferral_issue_number` is populated either by DeferSuppressedAction in
        # the same run, or recovered from the durable PR marker on every subsequent run
        # (PRStateSnapshot.suppressed_deferral_issue_number).  When the snapshot was built
        # outside the suppressed-only blocked-verdict branch (e.g. after a CI repair that
        # cleared the gate), those fields are None; do a best-effort recovery here so that
        # the already-filed triage issue is still dispatched after merge.
        deferral_issue = derived.get("suppressed_deferral_issue_number")
        deferral_review_id = derived.get("suppressed_deferral_review_id")
        if deferral_issue is None or deferral_review_id is None:
            list_issue_comments = getattr(provider, "list_issue_comments", None)
            if callable(list_issue_comments):
                try:
                    pr_token_login: str | None = None
                    get_pr_token_login = getattr(provider, "get_pr_token_login", None)
                    if callable(get_pr_token_login):
                        try:
                            pr_token_login = get_pr_token_login()
                        except Exception as exc:
                            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                                raise
                            pass
                    extra_authors = frozenset({pr_token_login.casefold()}) if pr_token_login else None
                    issue_comments = list_issue_comments(snapshot.pr_number)
                    deferral_review_id, deferral_issue = find_suppressed_deferral_state(issue_comments, extra_authors)
                except Exception as exc:
                    if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                        raise
                    logger.debug(
                        "PR #%d: Failed to recover suppressed deferral state from issue comments: %s",
                        snapshot.pr_number,
                        str(exc)[:200],
                    )
        if deferral_issue is not None and deferral_review_id is not None:
            try:
                provider.dispatch_suppressed_triage(
                    issue_number=deferral_issue,
                    pr_number=snapshot.pr_number,
                    review_id=deferral_review_id,
                )
                logger.info(
                    "PR #%d: Dispatched suppressed-comment triage for issue #%d",
                    snapshot.pr_number,
                    deferral_issue,
                )
            except Exception as exc:
                # Dispatch failed after the merge has already succeeded.  Return FAILED
                # so the pipeline run records the failure faithfully and operators can
                # investigate.  The suppressed-deferral marker is durable on the PR, so
                # the issue number and review ID survive a pipeline re-trigger: a manual
                # re-run of this workflow will recover the marker and retry the dispatch.
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.error(
                    "PR #%d: Suppressed-comment triage dispatch failed (issue #%d) — "
                    "re-trigger this pipeline run to retry dispatch: %s",
                    snapshot.pr_number,
                    deferral_issue,
                    exc,
                )
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.FAILED,
                    error=str(exc),
                    details="suppressed-comment triage dispatch failed after merge",
                )

        logger.info("PR #%d: Merged successfully (method=%s)", snapshot.pr_number, method)
        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            details=f"PR merged via {method}",
        )

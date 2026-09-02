"""Dispatch conflict-resolution action — hands unresolvable merge conflicts to the cloud agent.

When ``RebaseAction`` cannot auto-resolve a rebase (or the provider reports the
PR as ``dirty``), the loop would otherwise stall: squash, request_review,
approve and merge all skip and a human has to comment
``@copilot resolve the merge conflicts`` by hand.  This action closes that gap by
dispatching the cloud-agent conflict-repair comment automatically.

Safety properties
-----------------

* **Deduplicated** by the existing ``<!-- agdt:conflict-repair:... -->`` marker
  (same head+base within ``DISPATCH_IDEMPOTENCY_TTL_MINUTES``).
* **Bounded**: at most ``MAX_CONFLICT_REPAIR_ATTEMPTS`` dispatches per HEAD SHA.
  A successful resolution pushes a new commit, which resets the budget.  When the
  budget is exhausted the action escalates to a human once per HEAD and blocks.
* **Fails closed**: any lookup error (base SHA, attempt count, dedup marker)
  suppresses the dispatch for this run rather than risking comment spam.

Marker trust boundary
---------------------

``agentic_devtools/cli/ci/evaluator/snapshot.py`` treats the conflict-repair
marker as *synthesizable*: when the HTML-comment balancer has to append a
closing ``-->`` to a truncated agent comment, the resulting marker is escaped
(``&lt;!--``) and, as a final safety check, persistence is refused when
sanitisation would introduce a control marker that was not already present.
So a cloud-agent reply can never *manufacture* a well-formed marker.

It can still *quote* one verbatim.  Because both
``should_dispatch_conflict_repair`` and ``count_conflict_repair_dispatches``
are identity-scoped to the ``SPECKIT_PR_TOKEN`` login (resolved via
``get_pr_token_login``), a Copilot-authored quote is ignored entirely — it
neither triggers deduplication nor inflates the attempt count.  A malformed
marker makes the TTL check fail *open* (re-dispatch allowed) by design;
the per-HEAD attempt cap is what bounds the resulting retries.
"""

from __future__ import annotations

import logging

from agentic_devtools.cli.ci.guards import (
    MAX_CONFLICT_REPAIR_ATTEMPTS,
    build_conflict_repair_escalation_marker,
    count_conflict_repair_dispatches,
    should_dispatch_conflict_repair,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.session_detector import is_copilot_session_active_via_agent_task
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)


def _raise_if_rate_limit(exc: Exception) -> None:
    """Re-raise actual provider rate limits so the pipeline can persist cooldown state."""
    if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
        raise


#: Provider mergeability state that means "conflicts with the base branch".
_CONFLICTED_MERGEABLE_STATE = "dirty"


class DispatchConflictResolutionAction:
    """Dispatch a cloud-agent conflict-repair comment when the PR has merge conflicts.

    Preconditions:
    - A merge conflict was detected (``RebaseAction`` published ``rebase_conflict``,
      or the provider reports ``mergeable_state == "dirty"``)
    - No repair dispatched in this run
    - No active Copilot coding session

    Idempotency: an in-TTL dispatch marker for the same head+base suppresses
    re-dispatch; the per-HEAD attempt cap escalates instead of retrying forever.
    """

    @property
    def name(self) -> str:
        return "dispatch_conflict_resolution"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate whether a conflict-repair dispatch is needed."""
        preconditions: dict[str, bool] = {}

        rebase_conflict = bool(derived.get("rebase_conflict", False))
        provider_conflict = snapshot.mergeable_state.strip().lower() == _CONFLICTED_MERGEABLE_STATE
        conflict_detected = rebase_conflict or provider_conflict
        preconditions["merge_conflict_detected"] = conflict_detected
        if not conflict_detected:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="No merge conflict detected — nothing to dispatch",
            )

        repair_dispatched = bool(derived.get("repair_dispatched", False))
        preconditions["no_repair_dispatched"] = not repair_dispatched
        if repair_dispatched:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Repair already dispatched in this run — deferring conflict repair",
            )

        active_session = is_copilot_session_active_via_agent_task(snapshot.base_repo_full_name, snapshot.pr_number)
        preconditions["no_active_session"] = not active_session
        if active_session:
            # A conflict-repair session is already in flight for this conflicted
            # snapshot. Keep downstream review/approval/merge actions blocked in
            # this run so they cannot act on the pre-resolution HEAD.
            derived.set("repair_dispatched", True)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Copilot session active — deferring conflict repair",
            )

        source = "rebase conflict" if rebase_conflict else "provider mergeable_state=dirty"
        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details=f"Merge conflict detected ({source}) — conflict repair needed",
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Dispatch the conflict-repair comment, deduplicated and attempt-bounded."""
        # Any execution path here means this run observed a conflicted PR and
        # entered conflict-repair handling. Block downstream
        # request_review/approve/merge actions for the rest of this run even when
        # the dispatch is deduplicated, capped, or fail-closed.
        derived.set("repair_dispatched", True)

        try:
            base_sha = provider.get_ref_sha(snapshot.base_branch)
        except Exception as exc:
            _raise_if_rate_limit(exc)
            logger.warning("PR #%d: Failed to resolve base branch SHA: %s", snapshot.pr_number, exc)
            base_sha = ""

        if not base_sha:
            # Without a base SHA the dedup marker cannot be built correctly, so a
            # dispatch here would be un-deduplicable. Fail closed and retry next run.
            logger.warning(
                "PR #%d: Base branch SHA unavailable — skipping conflict-repair dispatch",
                snapshot.pr_number,
            )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details="Base branch SHA unavailable — cannot dispatch a deduplicable conflict repair",
            )

        try:
            dispatch_login = provider.get_pr_token_login()
        except Exception as exc:
            _raise_if_rate_limit(exc)
            logger.warning("PR #%d: Failed to resolve dispatch identity login: %s", snapshot.pr_number, exc)
            dispatch_login = ""

        if not dispatch_login:
            # Without knowing which identity posts the dispatch comment, the
            # attempt counter and escalation check cannot be scoped to the real
            # author.  Fail closed to avoid miscounting or spurious escalation.
            logger.warning(
                "PR #%d: PR-token login unavailable — skipping conflict-repair dispatch",
                snapshot.pr_number,
            )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details="PR-token login unavailable — cannot authenticate dispatch identity",
            )

        try:
            attempts = count_conflict_repair_dispatches(provider, snapshot.pr_number, snapshot.head_sha, dispatch_login)
        except Exception as exc:
            _raise_if_rate_limit(exc)
            logger.warning("PR #%d: Failed to count conflict-repair dispatches: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                error=str(exc),
                details="Could not determine conflict-repair attempt count — skipping dispatch",
            )

        if attempts >= MAX_CONFLICT_REPAIR_ATTEMPTS:
            self._escalate(provider, snapshot, attempts, dispatch_login)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.BLOCKED,
                limit_reached=True,
                details=(
                    f"Conflict-repair attempt limit reached ({attempts}/{MAX_CONFLICT_REPAIR_ATTEMPTS} "
                    f"for HEAD {snapshot.head_sha[:8]}) — human resolution required"
                ),
            )

        try:
            allowed = should_dispatch_conflict_repair(
                provider,
                snapshot.pr_number,
                snapshot.head_sha,
                base_sha,
                dispatch_login=dispatch_login,
            )
        except Exception as exc:
            _raise_if_rate_limit(exc)
            logger.warning("PR #%d: Conflict-repair dedup check failed: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                error=str(exc),
                details="Could not verify conflict-repair dedup marker — skipping dispatch",
            )

        if not allowed:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details="Conflict repair already dispatched for this head+base within the dedup TTL",
            )

        try:
            comment_id = provider.dispatch_conflict_repair(
                pr_number=snapshot.pr_number,
                head_sha=snapshot.head_sha,
                base_sha=base_sha,
                base_branch=snapshot.base_branch,
                head_branch=snapshot.head_branch,
            )
        except Exception as exc:
            _raise_if_rate_limit(exc)
            logger.error("PR #%d: Conflict-repair dispatch failed: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="dispatch_conflict_repair call failed",
            )

        logger.info(
            "PR #%d: Conflict repair dispatched (attempt %d/%d, comment_id=%d)",
            snapshot.pr_number,
            attempts + 1,
            MAX_CONFLICT_REPAIR_ATTEMPTS,
            comment_id,
        )

        # HEAD is expected to move once the cloud agent pushes the merge commit;
        # downstream actions must not act on the pre-resolution snapshot.
        derived.set("repair_dispatched", True)

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            details=(
                f"Conflict repair dispatched (attempt {attempts + 1}/{MAX_CONFLICT_REPAIR_ATTEMPTS}, "
                f"comment_id={comment_id})"
            ),
        )

    def _escalate(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        attempts: int,
        dispatch_login: str = "",
    ) -> None:
        """Post a one-per-HEAD human-attention notice when retries are exhausted.

        The notice deliberately does NOT mention ``@copilot``: the point of
        escalation is that the cloud agent already failed to resolve the
        conflicts, so re-triggering it would just burn another attempt.

        ``dispatch_login`` restricts the already-posted check to comments
        authored by the authenticated automation identity, preventing a PR
        participant from suppressing the escalation by pre-posting the
        predictable per-HEAD marker.
        """
        marker = build_conflict_repair_escalation_marker(head_sha=snapshot.head_sha)
        try:
            already_posted = any(
                marker in c.body and (not dispatch_login or c.author == dispatch_login)
                for c in provider.list_issue_comments(snapshot.pr_number)
            )
            if already_posted:
                logger.info(
                    "PR #%d: Conflict-repair escalation already posted for HEAD %s",
                    snapshot.pr_number,
                    snapshot.head_sha[:8],
                )
                return

            body = (
                f"{marker}\n"
                "### ⚠️ Merge conflicts require human resolution\n\n"
                f"The AI PR loop dispatched {attempts} automated conflict-resolution "
                f"attempt(s) for HEAD `{snapshot.head_sha[:8]}` without success, so it "
                "has stopped retrying.\n\n"
                "Resolve the conflicts manually by merging the current base branch into "
                "the PR branch (do not rebase or force-push), then push the result. "
                "The loop resumes automatically on the new commit."
            )
            provider.post_comment_as_pr_token(snapshot.pr_number, body)
            logger.warning(
                "PR #%d: Conflict-repair attempts exhausted — escalated to humans",
                snapshot.pr_number,
            )
        except Exception as exc:
            # Escalation is advisory; the BLOCKED decision is what stops the loop.
            logger.warning("PR #%d: Failed to post conflict-repair escalation: %s", snapshot.pr_number, exc)

"""Squash action — squashes commits when multiple exist.

Responsible strictly for commit hygiene. Review requests are handled
explicitly by RequestReviewAction after squash completes.
"""

from __future__ import annotations

import logging

from agentic_devtools.cli.ci.pipeline.gate_verdict import copilot_review_gate_passed
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.session_detector import is_copilot_session_active_via_agent_task
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)


class SquashAction:
    """Squash commits when more than one exists above merge-base.

    Responsible strictly for commit hygiene — converting multiple commits into
    a single well-formed commit. Does NOT trigger or rely on triggering Copilot
    review as a side effect of force-push.

    The squash is **deferred until the PR is merge-ready**: repair commits are
    allowed to accumulate during the review cycle and are collapsed once, when the
    Copilot review gate passes. A squashing run invalidates the snapshot and is
    therefore structurally barred from approving or merging, so squashing on every
    repair round cost one extra loop visit per round. The invariant that a PR lands
    on the base branch as exactly one commit is unchanged — only its enforcement
    timing moves. (``MergeAction`` also falls back to a squash merge whenever more
    than one commit remains.)

    After successful squash, sets ``invalidates_snapshot=True`` because the HEAD
    SHA has changed. ``RequestReviewAction`` (which opts into
    ``runs_after_invalidation``) will then explicitly request review on the new
    squashed HEAD.

    When the squash preserved the tree (the actual post-squash tree matches the
    pre-squash ``head_sha`` tree returned by ``squash_post_repair``) and pre-squash
    CI was ``passing``, ``execute`` sets two run-scoped derived entries:
    ``squash_preserved_green`` (True) and ``squash_preserved_green_sha`` (the
    post-squash commit SHA from ``SquashResult.after_sha``). The runner carries
    both across the post-invalidation snapshot refresh, but only restores the flag
    when the refreshed ``head_sha`` matches ``squash_preserved_green_sha`` — a
    concurrent push that moves HEAD to a different commit fails closed and defers to
    fresh CI. The flag is consumed **only** by ``RequestReviewAction`` to relax its
    ``ci_passing`` precondition on the freshly squashed HEAD (whose required checks
    have not re-reported yet), saving one ``ai-pr-loop`` cycle. It is never consumed
    by ``ApproveAction`` or ``MergeAction`` — they keep their own independent CI gate
    on the real HEAD and are structurally halted in the same run as a squash.

    Preconditions:
    - Commits above merge-base > 1
    - Copilot review gate passed on HEAD (same predicate ApproveAction evaluates)
    - All review threads resolved
    - CI passing (actionable checks green — same gate as RequestReviewAction)
    - No repair dispatched in this run (keeps HEAD stable for the repair cycle)
    - No active Copilot coding session (pending review does NOT block squash)

    Idempotency: Already 1 commit → skip.
    """

    @property
    def name(self) -> str:
        return "squash"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate whether squash is needed."""
        preconditions: dict[str, bool] = {}

        # Must have more than 1 commit
        preconditions["commits_gt_1"] = snapshot.commit_count > 1
        if snapshot.commit_count <= 1:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=f"Only {snapshot.commit_count} commit(s) — nothing to squash",
            )

        unresolved_threads = derived.get("unresolved_threads", snapshot.unresolved_threads)

        # Squash is deferred until the PR is merge-ready. Collapsing the branch
        # mid-cycle costs an extra loop visit, because a squashing run invalidates the
        # snapshot and is therefore structurally barred from approving or merging.
        # Repair commits are allowed to accumulate during the review cycle and are
        # squashed once, when the review has gone clean — paying that cost a single
        # time instead of once per repair round. The final invariant is unchanged: the
        # PR still lands on the base branch as exactly one commit.
        #
        # The predicate is the same one ApproveAction evaluates (gate verdict, with the
        # fail-closed suppressed-only bypass, falling back to the legacy clean-review
        # check when no verdict is available), so squash never fires before the review
        # that unblocks approval.
        gate_passed = copilot_review_gate_passed(snapshot, unresolved_threads=unresolved_threads)
        preconditions["review_clean"] = gate_passed
        if not gate_passed:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=(
                    f"{snapshot.commit_count} commits retained — squash deferred until the Copilot review gate passes"
                ),
            )

        preconditions["all_threads_resolved"] = unresolved_threads == 0
        if unresolved_threads > 0:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=(
                    f"unresolved_threads: {unresolved_threads} thread(s) still open — "
                    "squash blocked until all review threads are resolved"
                ),
            )

        # CI must be passing before squashing — prevents duplicate repair dispatches
        # for new SHAs created by premature squash (same gate as RequestReviewAction).
        ci_passing = snapshot.ci_status == "passing"
        preconditions["ci_passing"] = ci_passing
        if not ci_passing:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=f"CI is {snapshot.ci_status} — deferring squash",
            )

        # Repair dispatch in this run should keep HEAD stable for the repair cycle.
        repair_dispatched = getattr(derived, "repair_dispatched", False)
        preconditions["no_repair_dispatched"] = not repair_dispatched
        if repair_dispatched:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Repair dispatched — deferring squash",
            )

        # No active Copilot session (coding/repair only — pending review does NOT block squash)
        active_session = is_copilot_session_active_via_agent_task(snapshot.base_repo_full_name, snapshot.pr_number)
        preconditions["no_active_session"] = not active_session
        if active_session:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Copilot session active — deferring squash",
            )

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details=f"{snapshot.commit_count} commits to squash",
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Execute the squash operation."""
        try:
            squash_result = provider.squash_post_repair(
                pr_number=snapshot.pr_number,
                base_branch=snapshot.base_branch,
                head_branch=snapshot.head_branch,
                head_sha=snapshot.head_sha,
            )
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.error("PR #%d: Squash failed: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="squash_post_repair failed",
            )

        logger.info("PR #%d: Squashed commits", snapshot.pr_number)
        derived.set("commit_count", 1)

        # Run-scoped optimization flag consumed ONLY by RequestReviewAction.
        #
        # A squash that ran in THIS run, was preceded by green CI, and preserved the
        # tree means the pre-squash green CI result still applies to the identical
        # post-squash tree. This lets RequestReviewAction request a review on the new
        # squashed HEAD in the same run without waiting for the post-squash SHA's
        # checks to re-report — requesting a review is a non-gating side effect.
        #
        # Tree preservation is verified against the ACTUAL before/after tree identity
        # returned by squash_post_repair, but the optimization still requires the
        # documented ``commits_behind == 0`` precondition from the pre-execution
        # snapshot. squash_post_repair may refetch base/head and perform a second
        # reset/squash to absorb a commit pushed during finalization, and the base or
        # head can move before the refreshed snapshot; in those races the resulting
        # tree differs even though ``commits_behind`` was 0 beforehand. Comparing the
        # real trees ensures the flag is never carried onto newly introduced code,
        # while the behind-base guard preserves the contract that a rebase onto newer
        # base code never reuses the prior green result in the same run.
        #
        # This flag is NEVER consumed by ApproveAction or MergeAction. They keep their
        # own independent CI gate on the real HEAD and are structurally halted in the
        # same run as a squash (they lack runs_after_invalidation), so this can never
        # approve/merge against unreported checks.
        pre_squash_green = snapshot.ci_status == "passing"
        if squash_result.tree_preserved and pre_squash_green and snapshot.commits_behind == 0:
            derived.set("squash_preserved_green", True)
            derived.set("squash_preserved_green_sha", squash_result.after_sha)

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            details=f"Squashed {snapshot.commit_count} commits into 1",
            invalidates_snapshot=True,
        )

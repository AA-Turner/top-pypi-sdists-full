"""Defer suppressed-only review rounds to a follow-up triage issue.

When a Copilot review round produces **only** suppressed findings, every one of
them sits on a non-executable path, and the PR's diff contains no executable file
at all, the loop stops manufacturing repair rounds: it files a follow-up issue
carrying the recovered findings, assigns the suppressed-comment triage agent to
it, and records a deferral marker on the PR so approve/merge may proceed.

The full trigger is the ten-condition, fail-closed predicate
:func:`~agentic_devtools.cli.ci.pipeline.gate_verdict.suppressed_deferral_eligible`.
Its snapshot-only subset is evaluated in :meth:`DeferSuppressedAction.evaluate`;
the three provider-backed conditions (prior executable posted findings, the open
deferral backlog, and linked-issue labels) are resolved in
:meth:`DeferSuppressedAction.execute` so their API cost is paid only by PRs that
already satisfy everything else.  On top of the predicate the action requires the
parent PR to carry ``ai-auto-merge-allowed``, because the triage agent is dispatched
post-merge by ``MergeAction`` and that path never runs for a PR the loop does not
merge itself.
"""

from __future__ import annotations

import logging
import os

from agentic_devtools.cli.ci.guards import LABEL_AUTO_MERGE_ALLOWED
from agentic_devtools.cli.ci.models import is_copilot_login
from agentic_devtools.cli.ci.pipeline.deferral import post_suppressed_deferral_marker
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    SUPPRESSED_FOLLOW_UP_LABEL,
    is_executable_path,
    suppressed_deferral_eligible,
    suppressed_deferral_snapshot_eligible,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.github.ccr_review_format import extract_suppressed_comment_entries
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)


def _raise_if_rate_limit(exc: Exception) -> None:
    """Re-raise actual provider rate limits so the pipeline can persist cooldown state."""
    if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
        raise


#: Environment variable gating the whole feature.  Defaults to disabled.
FEATURE_FLAG_ENV = "ENABLE_SUPPRESSED_DEFERRAL"

#: Environment variable overriding the open-deferral circuit breaker (condition 8).
MAX_OPEN_DEFERRALS_ENV = "SUPPRESSED_DEFERRAL_MAX_OPEN"

#: Default circuit-breaker ceiling for open deferral issues.
DEFAULT_MAX_OPEN_DEFERRALS = 5


def _max_open_deferrals() -> int:
    """Return the configured open-deferral ceiling, falling back to the default."""
    raw = os.environ.get(MAX_OPEN_DEFERRALS_ENV, "").strip()
    if not raw:
        return DEFAULT_MAX_OPEN_DEFERRALS
    try:
        return int(raw)
    except ValueError:
        logger.warning(
            "%s=%r is not an integer — using default ceiling %d",
            MAX_OPEN_DEFERRALS_ENV,
            raw,
            DEFAULT_MAX_OPEN_DEFERRALS,
        )
        return DEFAULT_MAX_OPEN_DEFERRALS


def suppressed_findings(snapshot: PRStateSnapshot) -> list[tuple[str, str]]:
    """Return the ``(path, body)`` suppressed entries of the gate-evaluated review.

    Reads the body of the review the gate verdict actually evaluated (which may
    differ from ``copilot_review_id``) and recovers its suppressed entries.
    Returns an empty list when the verdict carries no review id or the review is
    not present in the snapshot.
    """
    verdict = snapshot.copilot_gate_verdict
    if verdict is None or verdict.review_id <= 0:
        return []
    for review in snapshot.reviews:
        if review.id == verdict.review_id:
            return extract_suppressed_comment_entries(review.body)
    return []


def count_prior_executable_posted_findings(provider: CIPlatformProvider, pr_number: int) -> int:
    """Count posted Copilot review comments on executable paths (condition 7).

    Posted findings are real inline review comments; suppressed entries never
    appear here.  Fails **closed** by raising on a provider error — the caller
    treats an unknown prior-finding history as ineligible for deferral.
    """
    comments = provider.list_all_review_comments(pr_number)
    return sum(
        1
        for comment in comments
        if not comment.is_suppressed and is_copilot_login(comment.author_login) and is_executable_path(comment.path)
    )


class DeferSuppressedAction:
    """File a triage follow-up for a specs-only suppressed-only review round.

    Positioned between ``ApplySuggestionsAction`` and ``DispatchRepairAction``:
    autofixable suggestions are still applied first, and the deferral marker this
    action posts is what stops the downstream repair dispatch.

    Preconditions:
    - ``ENABLE_SUPPRESSED_DEFERRAL`` is ``true``
    - the PR carries ``ai-auto-merge-allowed``: triage dispatch happens only on the
      loop's own merge path (:class:`~agentic_devtools.cli.ci.pipeline.actions.merge.MergeAction`),
      so deferring a PR the loop will never merge would leave the follow-up issue
      filed but never assigned
    - all ten trigger conditions hold (see
      :func:`~agentic_devtools.cli.ci.pipeline.gate_verdict.suppressed_deferral_eligible`)
    """

    @property
    def name(self) -> str:
        return "defer_suppressed"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate the feature flag and the snapshot-only trigger conditions."""
        preconditions: dict[str, bool] = {}

        enabled = os.environ.get(FEATURE_FLAG_ENV, "").lower() == "true"
        preconditions["feature_enabled"] = enabled
        if not enabled:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=f"Suppressed-comment deferral disabled ({FEATURE_FLAG_ENV} != 'true')",
            )

        # Design constraint (not one of the ten snapshot-based conditions): triage
        # dispatch runs post-merge inside MergeAction, which only ever acts on
        # auto-merge PRs.  Deferring a PR the loop will not merge itself would file an
        # issue that nothing later assigns, so such a PR keeps its repair rounds.
        # The label copy in execute() is conditional on this same check so that the
        # create_deferral_issue contract is satisfied even if this guard is later relaxed.
        auto_merge_parent = LABEL_AUTO_MERGE_ALLOWED in snapshot.labels
        preconditions["auto_merge_parent"] = auto_merge_parent
        if not auto_merge_parent:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=f"PR does not carry {LABEL_AUTO_MERGE_ALLOWED}; triage dispatch would never run",
            )

        # A deferral already recorded for this review needs no second one; the
        # approve/merge bypass reads the existing marker.
        verdict = snapshot.copilot_gate_verdict
        already_deferred = (
            verdict is not None
            and verdict.review_id > 0
            and derived.get("suppressed_deferral_review_id") == verdict.review_id
        )
        preconditions["not_already_deferred"] = not already_deferred
        if already_deferred:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Suppressed comments already deferred for this review",
            )

        eligible = suppressed_deferral_snapshot_eligible(
            verdict,
            head_changed_since_review=snapshot.head_changed_since_review,
            unresolved_threads=derived.unresolved_threads,
            suppressed_paths=[path for path, _body in suppressed_findings(snapshot)],
            changed_files=snapshot.files,
            pr_labels=snapshot.labels,
        )
        preconditions["snapshot_conditions_met"] = eligible
        if not eligible:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Not a deferrable specs-only suppressed-only review round",
            )

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details="Specs-only suppressed-only round — checking deferral backlog and linked issues",
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Resolve the provider-backed conditions, then file and record the deferral."""
        verdict = snapshot.copilot_gate_verdict
        if verdict is None:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details="No gate verdict to defer",
            )

        # Mirrors the `auto_merge_parent` precondition in evaluate(): without the label
        # MergeAction never runs, so the follow-up issue would never be dispatched.
        if LABEL_AUTO_MERGE_ALLOWED not in snapshot.labels:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions={"auto_merge_parent": False},
                details=f"PR does not carry {LABEL_AUTO_MERGE_ALLOWED}; triage dispatch would never run",
            )

        findings = suppressed_findings(snapshot)

        try:
            prior_executable_posted_findings = count_prior_executable_posted_findings(provider, snapshot.pr_number)
            open_deferral_count = provider.count_open_issues_with_label(SUPPRESSED_FOLLOW_UP_LABEL)
            linked_issue_labels = provider.list_linked_issue_labels(snapshot.pr_number)
        except Exception as exc:
            # Fail closed: an unknown history, backlog or label set is not a
            # licence to skip the remaining review rounds.
            _raise_if_rate_limit(exc)
            logger.warning(
                "PR #%d: Could not resolve deferral preconditions (%s) — not deferring",
                snapshot.pr_number,
                exc,
            )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions={"preconditions_resolved": False},
                details=f"Deferral preconditions could not be resolved: {exc}",
            )

        # Issue creation is not atomic with the marker post: a run that created
        # the issue but failed to post the marker leaves no PR state recording the
        # issue number.  Recover that orphaned issue *before* the eligibility check
        # so that an at-ceiling backlog does not block recovery — the orphaned issue
        # already counts against the ceiling and should not require capacity for a
        # second slot.
        try:
            issue_number: int | None = provider.find_deferral_issue(
                pr_number=snapshot.pr_number,
                review_id=verdict.review_id,
            )
        except Exception as exc:
            _raise_if_rate_limit(exc)
            logger.warning(
                "PR #%d: Could not look up an existing deferral issue (%s) — not deferring",
                snapshot.pr_number,
                exc,
            )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions={"existing_deferral_resolved": False},
                details=f"Existing deferral issue lookup failed: {exc}",
            )

        effective_open_deferral_count = open_deferral_count
        if issue_number is not None:
            logger.info(
                "PR #%d: Reusing existing deferral issue #%d for review %d",
                snapshot.pr_number,
                issue_number,
                verdict.review_id,
            )
            # Revalidate every provider-backed condition even when an orphaned
            # issue is recoverable.  Only the recovered issue itself is exempt
            # from the backlog ceiling because it already consumes one slot.
            effective_open_deferral_count = max(open_deferral_count - 1, 0)

        eligible = suppressed_deferral_eligible(
            verdict,
            head_changed_since_review=snapshot.head_changed_since_review,
            unresolved_threads=derived.unresolved_threads,
            suppressed_paths=[path for path, _body in findings],
            changed_files=snapshot.files,
            prior_executable_posted_findings=prior_executable_posted_findings,
            pr_labels=snapshot.labels,
            linked_issue_labels=linked_issue_labels,
            open_deferral_count=effective_open_deferral_count,
            max_open_deferrals=_max_open_deferrals(),
        )
        if not eligible:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions={"all_conditions_met": False},
                details=(
                    "Deferral conditions not met "
                    f"(prior_executable_posted_findings={prior_executable_posted_findings}, "
                    f"open_deferrals={effective_open_deferral_count})"
                ),
            )

        if issue_number is None:
            # No orphaned issue to recover — the full eligibility check passed, so
            # a fresh issue may be created.  Only copy ai-auto-merge-allowed when the
            # parent carries it (deferral only reaches this point for auto-merge PRs,
            # but the conditional keeps the label-copy contract explicit).
            labels = [SUPPRESSED_FOLLOW_UP_LABEL] + (
                [LABEL_AUTO_MERGE_ALLOWED] if LABEL_AUTO_MERGE_ALLOWED in snapshot.labels else []
            )

            try:
                issue_number = provider.create_deferral_issue(
                    pr_number=snapshot.pr_number,
                    review_id=verdict.review_id,
                    base_sha=snapshot.head_sha,
                    findings=findings,
                    labels=labels,
                )
            except Exception as exc:
                _raise_if_rate_limit(exc)
                logger.error("PR #%d: Suppressed-comment deferral failed: %s", snapshot.pr_number, exc)
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.FAILED,
                    error=str(exc),
                    details="Failed to create the deferral issue",
                )

        # The marker is the durable evidence approve/merge and repair dispatch
        # read.  Without it the deferral must not clear the gate, so a failed
        # post is a failed action even though the issue now exists — the next run
        # recovers that issue via `find_deferral_issue` and retries the post.
        if not post_suppressed_deferral_marker(provider, snapshot.pr_number, verdict.review_id, issue_number):
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error="deferral marker not posted",
                details=f"Deferral issue #{issue_number} filed but the PR marker could not be posted",
            )

        # The triage agent bases its work on `main`; dispatching before the parent
        # PR merges would cause it to inspect a tree that does not contain the PR
        # changes.  MergeAction reads these derived keys and dispatches post-merge.
        derived.set("suppressed_deferral_review_id", verdict.review_id)
        derived.set("suppressed_deferral_issue_number", issue_number)
        logger.info(
            "PR #%d: Deferred %d suppressed finding(s) from review %d to issue #%d; "
            "triage dispatch will occur after merge",
            snapshot.pr_number,
            len(findings),
            verdict.review_id,
            issue_number,
        )
        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            details=f"Deferred {len(findings)} suppressed finding(s) to issue #{issue_number}",
        )

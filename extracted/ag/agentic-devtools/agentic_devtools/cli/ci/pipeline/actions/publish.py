"""Publish action — publishes draft PRs."""

from __future__ import annotations

import logging

from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryOutcome, classify_initial_delivery
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.session_detector import (
    SessionOutcome,
    SessionState,
    is_copilot_session_active_via_agent_task,
)
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.title_utils import is_wip_title as _is_wip_title
from agentic_devtools.cli.ci.pipeline.title_utils import wip_normalized_title as _wip_normalized_title
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)

_PUBLISH_AFTER_BRANCH_PREP_DETAILS = "Published draft PR after pre-publish branch preparation"


def _evaluate_publish_eligibility(
    action_name: str,
    snapshot: PRStateSnapshot,
    derived: DerivedState,
) -> ActionResult:
    preconditions: dict[str, bool] = {}

    is_draft = derived.is_draft
    preconditions["is_draft"] = is_draft
    if not is_draft:
        return ActionResult(
            name=action_name,
            decision=ActionDecision.SKIP,
            preconditions=preconditions,
            details="PR is not a draft",
        )

    has_changes = derived.has_changes
    preconditions["has_changes"] = has_changes
    if not has_changes:
        return ActionResult(
            name=action_name,
            decision=ActionDecision.SKIP,
            preconditions=preconditions,
            details="PR has no file changes",
        )

    is_wip = _is_wip_title(snapshot.title)
    session_state = derived.get("latest_session_state")
    completion_confirmed = isinstance(session_state, SessionState) and session_state.outcome is SessionOutcome.FINISHED
    initial_delivery = (
        classify_initial_delivery(
            derived.get("provider"),
            snapshot.pr_number,
            completion_confirmed=completion_confirmed,
            initial_plan_sha=None,
        )
        if is_wip
        else InitialDeliveryOutcome.UNKNOWN
    )
    successful_wip_recovery = is_wip and has_changes and initial_delivery is InitialDeliveryOutcome.DELIVERED
    preconditions["not_wip"] = not is_wip or successful_wip_recovery
    if is_wip and not successful_wip_recovery:
        return ActionResult(
            name=action_name,
            decision=ActionDecision.SKIP,
            preconditions=preconditions,
            details=(
                "PR title is WIP"
                if not completion_confirmed
                else "Initial delivery is empty or unknown — WIP publication blocked"
            ),
        )

    active_session = is_copilot_session_active_via_agent_task(
        snapshot.base_repo_full_name,
        snapshot.pr_number,
        head_branch=snapshot.head_branch,
        pr_id=snapshot.pr_id,
        head_sha=snapshot.head_sha,
        provider=derived.get("provider"),
    )
    preconditions["no_active_session"] = active_session is False
    if active_session is not False:
        return ActionResult(
            name=action_name,
            decision=ActionDecision.SKIP,
            preconditions=preconditions,
            details="Copilot session active or inventory unavailable — publish blocked",
        )

    return ActionResult(
        name=action_name,
        decision=ActionDecision.EXECUTE,
        preconditions=preconditions,
        details="Draft PR ready to publish",
    )


class PublishAction:
    """Publish a draft PR when it has changes and is ready for review.

    Preconditions:
    - PR is draft
    - PR has file changes
    - A fresh non-empty diff is verified after branch preparation
    - PR title is not WIP, unless a completed Copilot session left a non-empty
      WIP draft whose fresh lifecycle inventory confirms no active writer.

    Idempotency: Already published → skip.
    """

    may_invalidate_snapshot = True
    preserves_diff_fingerprint = True

    @property
    def name(self) -> str:
        return "publish"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate whether the PR should be published."""
        return _evaluate_publish_eligibility(self.name, snapshot, derived)

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Squash before publish + publish the PR."""
        normalized_title: str | None = None
        if _is_wip_title(snapshot.title):
            session_state = derived.get("latest_session_state")
            if (
                not derived.is_draft
                or not derived.has_changes
                or not isinstance(session_state, SessionState)
                or session_state.outcome is not SessionOutcome.FINISHED
                or classify_initial_delivery(
                    provider,
                    snapshot.pr_number,
                    completion_confirmed=True,
                    initial_plan_sha=None,
                )
                is not InitialDeliveryOutcome.DELIVERED
            ):
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.SKIP,
                    details="WIP publication requires confirmed completed delivery and changed files",
                )

            # Compute and validate the normalized title before invoking the
            # squash side effect, so a bad title never force-pushes the branch.
            normalized_title = _wip_normalized_title(snapshot.title)
            if not normalized_title:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.FAILED,
                    error="WIP title has no title text to preserve",
                    details="Could not normalize successful WIP draft title",
                )

        # Squash before publish
        try:
            provider.squash_before_publish(
                pr_number=snapshot.pr_number,
                base_branch=snapshot.base_branch,
                head_branch=snapshot.head_branch,
                head_sha=snapshot.head_sha,
            )
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                setattr(exc, "invalidates_snapshot", True)
                setattr(exc, "preserves_diff_fingerprint", True)
                raise
            logger.error("PR #%d: squash_before_publish failed: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="squash_before_publish failed",
                invalidates_snapshot=True,
                preserves_diff_fingerprint=True,
            )

        return self._publish_prepared_pr(provider, snapshot, derived, normalized_title)

    @staticmethod
    def _has_verified_delivery_after_preparation(provider: CIPlatformProvider, pr_number: int) -> bool:
        """Recheck delivery after branch preparation while preserving rate-limit signals."""
        try:
            return (
                classify_initial_delivery(
                    provider,
                    pr_number,
                    completion_confirmed=True,
                    initial_plan_sha=None,
                )
                is InitialDeliveryOutcome.DELIVERED
            )
        except ProviderRateLimitError as exc:
            if not exc.is_rate_limit:
                return False
            setattr(exc, "invalidates_snapshot", True)
            setattr(exc, "preserves_diff_fingerprint", True)
            raise

    def _publish_prepared_pr(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
        normalized_title: str | None,
    ) -> ActionResult:
        """Recheck the prepared draft diff, normalize any WIP title, and publish."""
        if not self._has_verified_delivery_after_preparation(provider, snapshot.pr_number):
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details="PR delivery evidence is empty or unavailable after branch preparation",
                invalidates_snapshot=True,
                preserves_diff_fingerprint=True,
            )

        if normalized_title is not None:
            try:
                provider.update_pr_title(snapshot.pr_number, normalized_title)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    setattr(exc, "invalidates_snapshot", True)
                    setattr(exc, "preserves_diff_fingerprint", True)
                    raise
                logger.error("PR #%d: Failed to remove WIP title prefix: %s", snapshot.pr_number, exc)
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.FAILED,
                    error=str(exc),
                    details="Failed to normalize successful WIP draft title",
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        # Publish
        try:
            provider.publish_pr(snapshot.pr_number)
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                setattr(exc, "invalidates_snapshot", True)
                setattr(exc, "preserves_diff_fingerprint", True)
                raise
            logger.error("PR #%d: publish_pr failed: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="publish_pr failed",
                invalidates_snapshot=True,
                preserves_diff_fingerprint=True,
            )

        # Update derived state
        derived.set("is_draft", False)
        logger.info(
            "PR #%d: Published (draft → ready) after pre-publish branch preparation",
            snapshot.pr_number,
        )

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            details=_PUBLISH_AFTER_BRANCH_PREP_DETAILS,
            invalidates_snapshot=True,
            preserves_diff_fingerprint=True,
        )

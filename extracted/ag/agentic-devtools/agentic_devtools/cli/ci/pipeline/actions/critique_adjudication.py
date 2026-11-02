"""Action that adjudicates completed critique tasks in the live pipeline."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.evaluator.models import PostAgentSnapshot


class CritiqueAdjudicationAction:
    """Adjudicate completed no-commit critique tasks in the live PR pipeline."""

    terminates_run = True

    def __init__(self, lock_token: str) -> None:
        self._lock_token = lock_token
        self._snapshot: PostAgentSnapshot | None = None

    @property
    def name(self) -> str:
        return "adjudicate_critique"

    def _owns_evaluator_lock(self, provider: CIPlatformProvider, pr_number: int) -> bool:
        from agentic_devtools.cli.ci.evaluator.lock import check_lock_status

        try:
            status = check_lock_status(provider, pr_number)
        except ProviderRateLimitError as exc:
            if exc.is_rate_limit:
                raise
            return False
        except Exception:
            return False
        return bool(self._lock_token and status.is_locked and not status.is_stale and status.holder == self._lock_token)

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Run only when a completed critique task is eligible for adjudication."""
        self._snapshot = None
        provider = derived.get("provider")
        if provider is None or not self._lock_token:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.BLOCKED,
                details="Evaluator lock ownership could not be verified",
            )
        try:
            if not self._owns_evaluator_lock(provider, snapshot.pr_number):
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.BLOCKED,
                    details="Evaluator lock is not held by this pipeline run",
                )
            from agentic_devtools.cli.ci.evaluator.classifier import classify_post_agent_state
            from agentic_devtools.cli.ci.evaluator.snapshot_builder import build_snapshot

            provider.invalidate_agent_task_inventory(snapshot.pr_number)
            post_agent_snapshot = build_snapshot(
                provider,
                snapshot.pr_number,
                snapshot.base_repo_full_name,
                current_lock_token=self._lock_token,
            )
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            return ActionResult(
                name=self.name,
                decision=ActionDecision.BLOCKED,
                error=str(exc),
                details="Critique task state could not be verified",
            )
        from agentic_devtools.cli.ci.evaluator.models import PostAgentClassification

        if classify_post_agent_state(post_agent_snapshot) is not PostAgentClassification.critique_adjudication:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details="No completed critique task requires adjudication",
            )
        self._snapshot = post_agent_snapshot
        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            details="Completed critique task is eligible for adjudication",
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Persist the guarded adjudication outcome for the completed task."""
        if self._snapshot is None:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details="No eligible critique task was verified",
            )
        if not self._owns_evaluator_lock(provider, snapshot.pr_number):
            self._snapshot = None
            return ActionResult(
                name=self.name,
                decision=ActionDecision.BLOCKED,
                details="Evaluator lock ownership changed before critique adjudication",
            )
        verified_snapshot = self._snapshot
        self._snapshot = None
        try:
            provider.invalidate_agent_task_inventory(snapshot.pr_number)
            from agentic_devtools.cli.ci.evaluator.classifier import classify_post_agent_state
            from agentic_devtools.cli.ci.evaluator.snapshot_builder import build_snapshot

            current_snapshot = build_snapshot(
                provider,
                snapshot.pr_number,
                snapshot.base_repo_full_name,
                current_lock_token=self._lock_token,
            )
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            return ActionResult(
                name=self.name,
                decision=ActionDecision.BLOCKED,
                error=str(exc),
                details="Critique task completion could not be reverified before adjudication",
            )
        from agentic_devtools.cli.ci.evaluator.models import PostAgentClassification

        if (
            current_snapshot.critique_task != verified_snapshot.critique_task
            or current_snapshot.current_head_sha != verified_snapshot.current_head_sha
            or current_snapshot.review_id != verified_snapshot.review_id
            or current_snapshot.latest_agent_comment is None
            or verified_snapshot.latest_agent_comment is None
            or current_snapshot.latest_agent_comment.id != verified_snapshot.latest_agent_comment.id
            or classify_post_agent_state(current_snapshot) is not PostAgentClassification.critique_adjudication
        ):
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details="Critique task completion changed before adjudication",
            )
        if not self._owns_evaluator_lock(provider, snapshot.pr_number):
            return ActionResult(
                name=self.name,
                decision=ActionDecision.BLOCKED,
                details="Evaluator lock ownership changed before critique adjudication",
            )
        from agentic_devtools.cli.ci.evaluator.critique_actions import adjudicate_critique

        result = adjudicate_critique(
            provider,
            current_snapshot,
            ownership_guard=lambda: self._owns_evaluator_lock(provider, snapshot.pr_number),
        )
        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE if result.success else ActionDecision.FAILED,
            error=(result.error_details or "Critique adjudication failed") if not result.success else "",
            details=result.error_details or "Critique task adjudication completed",
        )

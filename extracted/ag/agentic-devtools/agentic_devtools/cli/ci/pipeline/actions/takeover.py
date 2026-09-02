"""Take-over action — reclaims takeover-eligible HEAD commits under a human identity.

GitHub does not run ``pull_request`` workflows for commits pushed by the Copilot
coding agent when the push originates from an automation (the "except when the
push comes from an automation" exception of the *Require approval for workflow
runs* policy). As a result the required status checks never report on a
takeover-eligible automation-authored HEAD and the PR is stuck at "Expected —
waiting for status to be reported".

This action detects a takeover-eligible HEAD commit and re-authors it under
the CI (human) identity via ``git commit --amend --reset-author`` +
force-push. The force-push emits a ``synchronize`` event from a human pusher,
which triggers the required checks normally. The amend keeps the same tree, so
the diff (and any existing Copilot review content-hash) is preserved.
"""

from __future__ import annotations

import logging

from agentic_devtools.cli.ci.models import TAKEOVER_HEAD_AUTHOR_LOGINS
from agentic_devtools.cli.ci.pipeline.exceptions import ForceWithLeaseError
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.session_detector import is_copilot_session_active_via_agent_task
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)


class TakeOverAutomationCommitAction:
    """Reclaim a Copilot or automation-authored HEAD commit under the CI (human) identity.

    When the PR's HEAD commit was authored by Copilot or another automation
    identity (e.g. ``github-actions[bot]``), GitHub suppresses the
    ``pull_request`` workflow runs (automation-origin exception), leaving the
    required checks unreported. This action re-authors the commit under the
    human CI identity and force-pushes so the checks run.

    Preconditions:
    - HEAD commit authored by a recognized Copilot or automation identity
      (``head_author_login`` in ``TAKEOVER_HEAD_AUTHOR_LOGINS``)
    - No active Copilot coding session (don't race mid-work pushes)

    Workflow-file changes are intentionally allowed for this action when the
    loop token (``SPECKIT_PR_TOKEN``) has ``workflow`` scope (as configured
    for this repository). This scope requirement is an external prerequisite;
    if missing, the
    force-push can fail in ``reclaim_copilot_commit`` and this action returns
    ``FAILED``.

    Idempotency: After reclaim the new HEAD is authored by the CI identity, so
    the precondition is false on the next run. Sets ``invalidates_snapshot=True``
    because HEAD changed; the redispatched loop evaluates the fresh human HEAD.
    """

    @property
    def name(self) -> str:
        return "takeover"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate whether the automation-authored HEAD must be reclaimed."""
        preconditions: dict[str, bool] = {}

        head_author = snapshot.head_author_login
        is_takeover_author = head_author.casefold() in {login.casefold() for login in TAKEOVER_HEAD_AUTHOR_LOGINS}
        preconditions["head_authored_by_takeover_author"] = is_takeover_author
        if not is_takeover_author:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=(
                    f"HEAD authored by '{head_author or 'unknown'}'"
                    " — not a takeover-eligible commit; nothing to take over"
                ),
            )

        active_session = is_copilot_session_active_via_agent_task(snapshot.base_repo_full_name, snapshot.pr_number)
        preconditions["no_active_session"] = not active_session
        if active_session:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Copilot session active — deferring takeover until Copilot finishes",
            )

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details=f"HEAD authored by '{head_author}' — reclaiming under human identity to trigger checks",
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Reclaim the takeover-eligible HEAD commit by re-authoring and force-pushing."""
        try:
            provider.reclaim_copilot_commit(
                pr_number=snapshot.pr_number,
                head_branch=snapshot.head_branch,
                head_sha=snapshot.head_sha,
            )
        except ForceWithLeaseError as exc:
            logger.error("PR #%d: takeover force-push failed: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details=(
                    "Force-push-with-lease failed during takeover"
                    " — remote rejected update (concurrent update and/or insufficient permissions)"
                ),
            )
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.error("PR #%d: takeover failed: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="reclaim_copilot_commit failed",
            )

        logger.info(
            "PR #%d: Reclaimed takeover-eligible HEAD %s under human identity to trigger checks",
            snapshot.pr_number,
            snapshot.head_sha[:8],
        )
        # The reclaimed HEAD is now human-authored; reflect that in derived state.
        derived.set("head_author_login", "")

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            details="Reclaimed takeover-eligible HEAD under human identity; checks will run on the re-pushed commit",
            invalidates_snapshot=True,
        )


TakeOverCopilotCommitAction = TakeOverAutomationCommitAction

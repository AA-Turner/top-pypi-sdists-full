"""Blocked state detection for work-on-issue workflows."""

from __future__ import annotations

from datetime import datetime, timezone

from .config import PolicyConfig
from .context import WorkflowContext
from .types import BlockedDecision, DecisionResult

_FAILURE_KEYWORDS = frozenset({"error", "fail", "exception", "traceback"})


def _is_failure_outcome(outcome: str) -> bool:
    """Return True if the outcome string indicates a failure."""
    outcome_lower = outcome.lower()
    return any(kw in outcome_lower for kw in _FAILURE_KEYWORDS)


def BlockedStateDetector(
    context: WorkflowContext,
    policy: PolicyConfig,
) -> DecisionResult[BlockedDecision]:
    """Detect whether a workflow is blocked based on progress patterns.

    Detects two patterns:
    1. Time-without-progress: Current step has exceeded blocked_after_minutes
       based solely on elapsed time since the step was entered.
    2. Repetitive-identical-failure: 3 or more consecutive identical error
       strings in recent_outcomes. Only outcome strings that indicate a
       failure (containing "error", "fail", "exception", or "traceback",
       case-insensitively) are eligible for this pattern.

    Args:
        context: Current workflow execution context.
        policy: Loaded policy configuration.

    Returns:
        DecisionResult with BlockedDecision enum value and rationale.
    """
    blocked_after = policy.work_on_issue.blocked_after_minutes

    # Pattern 1: Time-without-progress in current step
    if context.step_history:
        current_step = context.step_history[-1]
        entered_at_str = current_step.get("entered_at", "")
        if isinstance(entered_at_str, str) and entered_at_str:
            try:
                entered_at = datetime.fromisoformat(entered_at_str.replace("Z", "+00:00"))
                if entered_at.tzinfo is None:
                    entered_at = entered_at.replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                minutes_in_step = (now - entered_at).total_seconds() / 60.0

                if minutes_in_step > blocked_after:
                    rationale = (
                        f"Blocked: {minutes_in_step:.1f}/{blocked_after} minutes "
                        f"without progress in step '{current_step.get('step', 'unknown')}'."
                    )
                    if len(rationale) > 500:
                        rationale = rationale[:497] + "..."
                    return DecisionResult(
                        decision=BlockedDecision.blocked,
                        rationale=rationale,
                        metadata={
                            "pattern": "time_without_progress",
                            "minutes_in_step": minutes_in_step,
                            "threshold": blocked_after,
                        },
                    )
            except (ValueError, TypeError):
                pass  # Invalid timestamp, skip this check

    # Pattern 2: Repetitive-identical-failure
    if len(context.recent_outcomes) >= 3:
        # Check last 3 consecutive outcomes for identity and failure indication
        last_three = context.recent_outcomes[-3:]
        if last_three[0] == last_three[1] == last_three[2] and last_three[0] and _is_failure_outcome(last_three[0]):
            consecutive_count = 0
            reference = context.recent_outcomes[-1]
            for outcome in reversed(context.recent_outcomes):
                if outcome == reference:
                    consecutive_count += 1
                else:
                    break

            rationale = f"Blocked: {consecutive_count} consecutive identical failures detected ('{reference[:100]}')."
            return DecisionResult(
                decision=BlockedDecision.blocked,
                rationale=rationale,
                metadata={
                    "pattern": "repetitive_failure",
                    "consecutive_count": consecutive_count,
                    "failure_sample": reference[:200],
                },
            )

    # Neither pattern matched
    rationale = "Workflow is progressing normally. No blocked conditions detected."
    return DecisionResult(
        decision=BlockedDecision.progressing,
        rationale=rationale,
        metadata={},
    )

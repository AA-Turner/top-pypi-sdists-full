"""Retry evaluation for workflow operations."""

from __future__ import annotations

from .types import DecisionResult, RetryDecision


def RetryEvaluator(
    current_retry_count: int,
    retry_budget: int,
    error_output: str | None = None,
) -> DecisionResult[RetryDecision]:
    """Evaluate whether a failed operation should be retried.

    Args:
        current_retry_count: Number of retries already attempted.
        retry_budget: Maximum allowed retries from policy.
        error_output: Optional error output from the failed operation.

    Returns:
        DecisionResult with RetryDecision enum value and strategy_hint metadata.
    """
    if current_retry_count < 0 or retry_budget < 0:
        rationale = (
            f"Invalid retry parameters: current_retry_count={current_retry_count}, "
            f"retry_budget={retry_budget}. Both must be non-negative. Stopping."
        )
        return DecisionResult(
            decision=RetryDecision.stop,
            rationale=rationale,
            metadata={"current_retry_count": current_retry_count, "retry_budget": retry_budget},
        )

    if retry_budget == 0:
        rationale = "Retry budget is 0. Immediate stop required."
        return DecisionResult(
            decision=RetryDecision.stop,
            rationale=rationale,
            metadata={"current_retry_count": current_retry_count, "retry_budget": retry_budget},
        )

    if current_retry_count < retry_budget:
        remaining = retry_budget - current_retry_count - 1
        # Determine strategy hint based on retry count
        if current_retry_count == 0:
            strategy_hint = "retry_same"
        elif current_retry_count < retry_budget - 1:
            strategy_hint = "retry_with_alternative"
        else:
            strategy_hint = "escalate_to_human"

        rationale = f"Retry permitted: attempt {current_retry_count + 1}/{retry_budget}. {remaining} retries remaining."
        return DecisionResult(
            decision=RetryDecision.retry,
            rationale=rationale,
            metadata={
                "current_retry_count": current_retry_count,
                "retry_budget": retry_budget,
                "strategy_hint": strategy_hint,
            },
        )

    # Retries exhausted
    rationale = f"Retries exhausted: {current_retry_count}/{retry_budget}. Cannot retry further."
    return DecisionResult(
        decision=RetryDecision.stop,
        rationale=rationale,
        metadata={"current_retry_count": current_retry_count, "retry_budget": retry_budget},
    )

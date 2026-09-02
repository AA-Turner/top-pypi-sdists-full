"""Budget enforcement evaluator."""

from __future__ import annotations

from .config import PolicyConfig
from .context import WorkflowContext
from .types import BudgetDecision, BudgetViolation, DecisionResult


def BudgetEvaluator(
    context: WorkflowContext,
    policy: PolicyConfig,
) -> DecisionResult[BudgetDecision]:
    """Evaluate whether any budget constraints have been exceeded.

    Checks 3 dimensions: tokens, time, retries. Skips dimensions where
    measurement is unavailable. Reports ALL violations, not just the first.

    Threshold semantics: actual > limit means violation (not >=).

    Args:
        context: Current workflow execution context.
        policy: Loaded policy configuration.

    Returns:
        DecisionResult with BudgetDecision enum value and rationale.
    """
    violations: list[BudgetViolation] = []
    skipped_dimensions: list[str] = []

    # Token budget check
    if context.tokens_consumed is None:
        skipped_dimensions.append("token_budget")
    elif context.tokens_consumed > policy.shared.max_tokens:
        violations.append(
            BudgetViolation(
                constraint_name="token_budget",
                configured_limit=policy.shared.max_tokens,
                actual_value=context.tokens_consumed,
                message=(f"Token consumption {context.tokens_consumed}/{policy.shared.max_tokens} exceeded budget."),
            )
        )

    # Time budget check
    if context.elapsed_minutes > policy.shared.max_wall_clock_minutes:
        violations.append(
            BudgetViolation(
                constraint_name="time_budget",
                configured_limit=policy.shared.max_wall_clock_minutes,
                actual_value=context.elapsed_minutes,
                message=(
                    f"Elapsed time {context.elapsed_minutes}/{policy.shared.max_wall_clock_minutes} "
                    f"minutes exceeded budget."
                ),
            )
        )

    # Retry budget check
    retry_budget = policy.work_on_issue.retry_budget
    for operation, count in context.retry_counts.items():
        if count > retry_budget:
            violations.append(
                BudgetViolation(
                    constraint_name="retry_budget",
                    configured_limit=retry_budget,
                    actual_value=count,
                    message=(f"Retries for '{operation}': {count}/{retry_budget} exceeded budget."),
                )
            )

    if violations:
        parts = [v.message for v in violations]
        rationale = " ".join(parts)
        if len(rationale) > 500:
            rationale = rationale[:497] + "..."
        return DecisionResult(
            decision=BudgetDecision.halt,
            rationale=rationale,
            metadata={
                "violations": tuple(violations),
                "skipped_dimensions": tuple(skipped_dimensions),
            },
        )

    rationale_parts = ["All budget constraints within limits."]
    if skipped_dimensions:
        rationale_parts.append(f"Skipped dimensions: {', '.join(skipped_dimensions)}.")
    rationale = " ".join(rationale_parts)

    return DecisionResult(
        decision=BudgetDecision.continue_,
        rationale=rationale,
        metadata={"violations": (), "skipped_dimensions": tuple(skipped_dimensions)},
    )

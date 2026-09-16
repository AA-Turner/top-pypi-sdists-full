"""Tri-state condition evaluation and freshness handling."""

from __future__ import annotations

from collections.abc import Mapping

from agentic_devtools.cli.ci.reconciliation.models import DynamicCondition, TriStateValue
from agentic_devtools.cli.ci.reconciliation.scope import evaluate_candidate_filter


class TriStateConditionEvaluator:
    """Evaluates configured boolean expressions over tri-state inputs."""

    def evaluate(self, expression: str, conditions: Mapping[str, DynamicCondition]) -> TriStateValue:
        values = {name: condition.value for name, condition in conditions.items()}
        result, _ = evaluate_candidate_filter(expression, values)
        return result


def merge_partial_conditions(
    *,
    current: Mapping[str, DynamicCondition],
    observed: Mapping[str, DynamicCondition],
) -> dict[str, DynamicCondition]:
    """Merge partial provider observations without fabricating missing evidence."""
    merged = dict(current)
    for name, condition in observed.items():
        merged[name] = condition
    return merged


def evaluate_freshness(
    *,
    condition: DynamicCondition,
    current_monotonic_seconds: float,
) -> TriStateValue:
    """Return unknown when a condition is stale or monotonic reconstruction failed."""
    elapsed = current_monotonic_seconds - condition.observed_monotonic_seconds
    if elapsed < 0:
        return TriStateValue.UNKNOWN
    if elapsed > condition.freshness_seconds:
        return TriStateValue.UNKNOWN
    return condition.value

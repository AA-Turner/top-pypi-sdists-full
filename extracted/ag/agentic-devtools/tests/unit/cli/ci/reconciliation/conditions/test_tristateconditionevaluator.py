"""Tests for TriStateConditionEvaluator and freshness utilities."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.conditions import (
    TriStateConditionEvaluator,
    evaluate_freshness,
    merge_partial_conditions,
)
from agentic_devtools.cli.ci.reconciliation.models import DynamicCondition, TriStateValue


def _condition(name: str, value: TriStateValue, observed_monotonic: float, freshness: int = 30) -> DynamicCondition:
    return DynamicCondition(
        name=name,
        value=value,
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=observed_monotonic,
        freshness_seconds=freshness,
    )


def test_evaluator_handles_true_and_unknown_results() -> None:
    evaluator = TriStateConditionEvaluator()
    conditions = {
        "target_branch_match": _condition("target_branch_match", TriStateValue.TRUE, 10),
        "author_association": _condition("author_association", TriStateValue.TRUE, 10),
        "draft_state": _condition("draft_state", TriStateValue.FALSE, 10),
        "mergeability_state": _condition("mergeability_state", TriStateValue.TRUE, 10),
        "unresolved_reviews": _condition("unresolved_reviews", TriStateValue.TRUE, 10),
        "labels": _condition("labels", TriStateValue.TRUE, 10),
    }
    assert evaluator.evaluate("target_branch_match AND NOT draft_state", conditions) == TriStateValue.TRUE
    assert evaluator.evaluate("target_branch_match AND missing_field", conditions) == TriStateValue.UNKNOWN


def test_merge_partial_conditions_replaces_only_observed_keys() -> None:
    current = {"a": _condition("a", TriStateValue.FALSE, 10)}
    observed = {"b": _condition("b", TriStateValue.TRUE, 20)}
    merged = merge_partial_conditions(current=current, observed=observed)
    assert set(merged) == {"a", "b"}


def test_evaluate_freshness_handles_stale_and_discontinuous_clock() -> None:
    fresh = evaluate_freshness(
        condition=_condition("a", TriStateValue.TRUE, observed_monotonic=10, freshness=20), current_monotonic_seconds=20
    )
    stale = evaluate_freshness(
        condition=_condition("a", TriStateValue.TRUE, observed_monotonic=10, freshness=5), current_monotonic_seconds=20
    )
    discontinuity = evaluate_freshness(
        condition=_condition("a", TriStateValue.TRUE, observed_monotonic=20, freshness=10), current_monotonic_seconds=10
    )
    assert fresh == TriStateValue.TRUE
    assert stale == TriStateValue.UNKNOWN
    assert discontinuity == TriStateValue.UNKNOWN

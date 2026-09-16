"""Tests for ShadowGateEvaluator."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.models import DynamicCondition, ScopeClassification, TriStateValue
from agentic_devtools.cli.ci.reconciliation.shadow_gate import ShadowGateEvaluator


def _condition(
    name: str, value: TriStateValue, observed_monotonic: float, freshness_seconds: int = 30
) -> DynamicCondition:
    return DynamicCondition(
        name=name,
        value=value,
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=observed_monotonic,
        freshness_seconds=freshness_seconds,
    )


def test_shadow_gate_blocks_superseded_and_non_active_scope() -> None:
    evaluator = ShadowGateEvaluator()
    result_superseded = evaluator.evaluate(
        expression="target_branch_match",
        conditions={"target_branch_match": _condition("target_branch_match", TriStateValue.TRUE, 10)},
        required_condition_names=("target_branch_match",),
        current_monotonic_seconds=20,
        scope_classification=ScopeClassification.ACTIVE,
        superseded=True,
    )
    result_scope = evaluator.evaluate(
        expression="target_branch_match",
        conditions={"target_branch_match": _condition("target_branch_match", TriStateValue.TRUE, 10)},
        required_condition_names=("target_branch_match",),
        current_monotonic_seconds=20,
        scope_classification=ScopeClassification.PENDING_UNVERIFIED,
        superseded=False,
    )
    assert not result_superseded.actionable
    assert result_scope.reason == "not_active_scope"


def test_shadow_gate_requires_fresh_required_conditions() -> None:
    evaluator = ShadowGateEvaluator()
    missing = evaluator.evaluate(
        expression="target_branch_match",
        conditions={},
        required_condition_names=("target_branch_match",),
        current_monotonic_seconds=20,
        scope_classification=ScopeClassification.ACTIVE,
        superseded=False,
    )
    stale = evaluator.evaluate(
        expression="target_branch_match",
        conditions={
            "target_branch_match": _condition("target_branch_match", TriStateValue.TRUE, 0, freshness_seconds=5)
        },
        required_condition_names=("target_branch_match",),
        current_monotonic_seconds=20,
        scope_classification=ScopeClassification.ACTIVE,
        superseded=False,
    )
    assert missing.value == TriStateValue.UNKNOWN
    assert stale.value == TriStateValue.UNKNOWN


def test_shadow_gate_allows_actionable_true_expression() -> None:
    evaluator = ShadowGateEvaluator()
    result = evaluator.evaluate(
        expression="target_branch_match",
        conditions={"target_branch_match": _condition("target_branch_match", TriStateValue.TRUE, 10)},
        required_condition_names=("target_branch_match",),
        current_monotonic_seconds=20,
        scope_classification=ScopeClassification.ACTIVE,
        superseded=False,
    )
    assert result.actionable
    assert result.value == TriStateValue.TRUE

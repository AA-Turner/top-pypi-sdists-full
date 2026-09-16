"""Shadow-gate evaluation for trusted reconciliation execution safety."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from agentic_devtools.cli.ci.reconciliation.conditions import TriStateConditionEvaluator, evaluate_freshness
from agentic_devtools.cli.ci.reconciliation.models import DynamicCondition, ScopeClassification, TriStateValue


@dataclass(frozen=True)
class ShadowGateResult:
    """Result of shadow-gate evaluation."""

    value: TriStateValue
    actionable: bool
    reason: str


class ShadowGateEvaluator:
    """Performs deterministic fail-closed gate checks."""

    def __init__(self) -> None:
        self._evaluator = TriStateConditionEvaluator()

    def evaluate(
        self,
        *,
        expression: str,
        conditions: Mapping[str, DynamicCondition],
        required_condition_names: tuple[str, ...],
        current_monotonic_seconds: float,
        scope_classification: ScopeClassification,
        superseded: bool,
    ) -> ShadowGateResult:
        if superseded:
            return ShadowGateResult(TriStateValue.UNKNOWN, False, "superseded")
        if scope_classification != ScopeClassification.ACTIVE:
            return ShadowGateResult(TriStateValue.FALSE, False, "not_active_scope")
        for name in required_condition_names:
            condition = conditions.get(name)
            if condition is None:
                return ShadowGateResult(TriStateValue.UNKNOWN, False, f"missing:{name}")
            freshness = evaluate_freshness(
                condition=condition,
                current_monotonic_seconds=current_monotonic_seconds,
            )
            if freshness == TriStateValue.UNKNOWN:
                return ShadowGateResult(TriStateValue.UNKNOWN, False, f"stale_or_unknown:{name}")
        value = self._evaluator.evaluate(expression, conditions)
        return ShadowGateResult(value=value, actionable=value == TriStateValue.TRUE, reason="evaluated")

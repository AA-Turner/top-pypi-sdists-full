"""Workflow tests for partial condition observation handling."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.conditions import merge_partial_conditions
from agentic_devtools.cli.ci.reconciliation.models import DynamicCondition, TriStateValue


def test_partial_observation_merges_independent_condition_updates() -> None:
    base = {
        "target_branch_match": DynamicCondition(
            name="target_branch_match",
            value=TriStateValue.TRUE,
            observed_at_utc_z="2026-09-15T12:00:00Z",
            observed_monotonic_seconds=10.0,
        )
    }
    observed = {
        "unresolved_reviews": DynamicCondition(
            name="unresolved_reviews",
            value=TriStateValue.UNKNOWN,
            observed_at_utc_z="2026-09-15T12:10:00Z",
            observed_monotonic_seconds=20.0,
        )
    }
    merged = merge_partial_conditions(current=base, observed=observed)
    assert set(merged) == {"target_branch_match", "unresolved_reviews"}

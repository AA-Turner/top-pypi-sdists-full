from __future__ import annotations

import pytest
from matrx_graph import (
    ActionTier,
    BackoffStrategy,
    EdgeKind,
    NodeCategory,
    RetryPolicy,
    RunStatus,
)


def test_action_tier_values():
    assert ActionTier.PURE.value == "pure"
    assert ActionTier.IDEMPOTENT.value == "idempotent"
    assert ActionTier.SIDE_EFFECT.value == "side_effect"
    assert ActionTier.NON_DETERMINISTIC.value == "non_deterministic"


def test_edge_kind_values():
    assert {k.value for k in EdgeKind} == {
        "data",
        "control",
        "conditional",
        "error",
        "stream",
    }


def test_node_category_values():
    expected = {
        "control",
        "data",
        "tool",
        "llm",
        "agent",
        "subgraph",
        "io",
        "custom",
        "plan",
        "pipe",
    }
    assert {c.value for c in NodeCategory} == expected


def test_retry_policy_default():
    p = RetryPolicy.default()
    assert p.max_attempts == 1
    assert p.backoff is BackoffStrategy.NONE
    assert p.retry_on == ()


def test_retry_policy_exponential():
    p = RetryPolicy.with_exponential(max_attempts=5)
    assert p.max_attempts == 5
    assert p.backoff is BackoffStrategy.EXPONENTIAL_JITTER
    assert "TimeoutError" in p.retry_on


def test_retry_policy_is_frozen():
    p = RetryPolicy.default()
    with pytest.raises(Exception):
        p.max_attempts = 5  # type: ignore[misc]


def test_run_status_values():
    assert {s.value for s in RunStatus} == {
        "pending",
        "running",
        "paused",
        "interrupted",
        "awaiting_input",
        "errored",
        "completed",
        "failed",
        "cancelled",
    }


def test_retry_policy_max_attempts_bounds():
    with pytest.raises(Exception):
        RetryPolicy(max_attempts=0)
    with pytest.raises(Exception):
        RetryPolicy(max_attempts=21)
    RetryPolicy(max_attempts=20)  # upper bound ok

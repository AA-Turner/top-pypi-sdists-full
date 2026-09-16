"""Tests for deterministic reconciliation identifiers."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.identifiers import (
    deterministic_id,
    make_correlation_id,
    make_decision_id,
    make_idempotency_key,
    make_observation_id,
)


def test_deterministic_id_is_stable() -> None:
    assert deterministic_id("a", 1) == deterministic_id("a", 1)


def test_observation_and_decision_ids_have_expected_length() -> None:
    observation_id = make_observation_id("owner/repo", 42, "2026-09-15T12:00:00Z", "sha")
    decision_id = make_decision_id("owner/repo", 42, observation_id, "allowed")
    assert len(observation_id) == 24
    assert len(decision_id) == 24


def test_idempotency_and_correlation_ids_are_distinct() -> None:
    observation_id = make_observation_id("owner/repo", 42, "2026-09-15T12:00:00Z", "sha")
    decision_id = make_decision_id("owner/repo", 42, observation_id, "allowed")
    assert make_idempotency_key("record", "allowed", "digest") != make_correlation_id(observation_id, decision_id)

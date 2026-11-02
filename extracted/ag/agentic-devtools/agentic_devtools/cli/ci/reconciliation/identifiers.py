"""Deterministic identifiers for trusted reconciliation entities."""

from __future__ import annotations

import hashlib


def deterministic_id(*parts: object, length: int = 16) -> str:
    """Return a deterministic identifier from arbitrary parts."""
    joined = "|".join(str(part) for part in parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:length]


def make_observation_id(repo: str, pr_number: int, observed_at_utc_z: str, change_id: str) -> str:
    """Create a deterministic observation identifier."""
    return deterministic_id("observation", repo, pr_number, observed_at_utc_z, change_id, length=24)


def make_decision_id(repo: str, pr_number: int, observation_id: str, decision_status: str) -> str:
    """Create a deterministic decision identifier."""
    return deterministic_id("decision", repo, pr_number, observation_id, decision_status, length=24)


def make_idempotency_key(record_id: str, action: str, evidence_digest: str) -> str:
    """Create an idempotency key for replay-safe transitions."""
    return deterministic_id("idempotency", record_id, action, evidence_digest, length=24)


def make_correlation_id(observation_id: str, decision_id: str) -> str:
    """Create a stable observation/decision correlation id."""
    return deterministic_id("correlation", observation_id, decision_id, length=24)

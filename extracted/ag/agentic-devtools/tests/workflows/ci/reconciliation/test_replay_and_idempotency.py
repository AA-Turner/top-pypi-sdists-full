"""Replay/idempotency workflow tests for trusted reconciliation."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.identifiers import make_idempotency_key


def test_idempotency_key_is_stable_across_replay() -> None:
    first = make_idempotency_key("record", "allowed", "digest")
    second = make_idempotency_key("record", "allowed", "digest")
    assert first == second

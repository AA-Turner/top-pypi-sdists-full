"""Tests for SessionOutcome."""

from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome


def test_session_outcome_values() -> None:
    assert {outcome.value for outcome in SessionOutcome} == {
        "active",
        "expired",
        "failed",
        "finished",
        "none",
        "unknown",
    }

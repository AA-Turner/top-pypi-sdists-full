"""Unit tests for CleanupAction."""

from agentic_devtools.orchestration.hierarchy.retry import CleanupAction


def test_cleanup_action_values_are_stable() -> None:
    assert CleanupAction.DISCARD_UNVERIFIED_STATE.value == "discard_unverified_state"

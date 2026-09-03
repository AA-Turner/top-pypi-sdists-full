"""Unit tests for TerminalCleanup."""

import pytest

from agentic_devtools.orchestration.hierarchy.retry import CleanupAction, TerminalCleanup


def test_terminal_cleanup_rejects_unknown_outcome() -> None:
    """Terminal cleanup outcomes are restricted to success and failed."""
    with pytest.raises(ValueError, match="success.*failed"):
        TerminalCleanup(action=CleanupAction.CHECKPOINT_RESTORE, outcome="unknown")


def test_terminal_cleanup_serializes_valid_outcome() -> None:
    """Terminal cleanup serialization uses enum values and the supplied outcome."""
    cleanup = TerminalCleanup(action=CleanupAction.DISCARD_UNVERIFIED_STATE, outcome="success")
    assert cleanup.to_dict() == {"action": "discard_unverified_state", "outcome": "success"}

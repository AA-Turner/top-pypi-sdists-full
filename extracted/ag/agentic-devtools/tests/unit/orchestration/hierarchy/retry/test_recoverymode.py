"""Unit tests for the RecoveryMode enum (FR-017)."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.retry import RecoveryMode


def test_recovery_mode_values_are_strings() -> None:
    """RecoveryMode is a StrEnum — each member serialises as its string value."""
    assert RecoveryMode.CHECKPOINT_RESTORE == "checkpoint_restore"
    assert RecoveryMode.PERSISTED_CHECKPOINT_RESUME == "persisted_checkpoint_resume"


def test_recovery_mode_membership() -> None:
    """All expected RecoveryMode members are present."""
    names = {m.name for m in RecoveryMode}
    assert "CHECKPOINT_RESTORE" in names
    assert "PERSISTED_CHECKPOINT_RESUME" in names

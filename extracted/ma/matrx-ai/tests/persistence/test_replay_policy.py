from matrx_ai.persistence.replay import RECOVERABLE_RETRY_ERRORS


def test_coordinator_hard_deadline_is_auto_replayable() -> None:
    """A cancelled flush with fully preserved ops must finish after DB recovery."""
    assert any("commit hard-deadline" in marker for marker in RECOVERABLE_RETRY_ERRORS)

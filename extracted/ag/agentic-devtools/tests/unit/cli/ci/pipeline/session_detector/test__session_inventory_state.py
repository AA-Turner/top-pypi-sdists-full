from agentic_devtools.cli.ci.pipeline.session_detector import (
    SessionOutcome,
    _normalize_session_inventory,
    _session_inventory_state,
)


def test_incomplete_inventory_does_not_prove_absence() -> None:
    result = _session_inventory_state(SessionOutcome.NONE, inventory=_normalize_session_inventory(None))
    assert result.outcome is SessionOutcome.UNKNOWN


def test_complete_inventory_preserves_outcome() -> None:
    result = _session_inventory_state(SessionOutcome.NONE, inventory=_normalize_session_inventory([]))
    assert result.outcome is SessionOutcome.NONE


def test_incomplete_inventory_keeps_positive_activity() -> None:
    result = _session_inventory_state(SessionOutcome.ACTIVE, inventory=_normalize_session_inventory([None]))
    assert result.outcome is SessionOutcome.ACTIVE
    assert result.failure_source == "agent-task-inventory"

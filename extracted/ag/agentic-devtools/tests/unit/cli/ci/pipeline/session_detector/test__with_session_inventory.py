from agentic_devtools.cli.ci.models import AgentTaskInventoryLoadResult, FailureCategory
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState, _with_session_inventory


def test_partial_metadata_survives_active_result() -> None:
    inventory = AgentTaskInventoryLoadResult((), complete=False)
    result = _with_session_inventory(SessionState(SessionOutcome.ACTIVE), inventory)
    assert result.outcome is SessionOutcome.ACTIVE
    assert result.inventory_availability == inventory.availability


def test_complete_inventory_does_not_overwrite_lifecycle_metadata() -> None:
    state = SessionState(SessionOutcome.UNKNOWN, failure_category=FailureCategory.HTTP_NOT_FOUND, http_status=404)
    assert _with_session_inventory(state, AgentTaskInventoryLoadResult(())) is state


def test_unrelated_raw_incompleteness_cannot_prove_expiry() -> None:
    result = _with_session_inventory(
        SessionState(SessionOutcome.EXPIRED),
        AgentTaskInventoryLoadResult((), complete=False),
    )
    assert result.outcome is SessionOutcome.UNKNOWN


def test_partial_raw_evidence_preserves_more_specific_lifecycle_failure() -> None:
    state = SessionState(SessionOutcome.UNKNOWN, failure_category=FailureCategory.HTTP_NOT_FOUND, http_status=404)
    result = _with_session_inventory(state, AgentTaskInventoryLoadResult((), complete=False))
    assert result.failure_category is FailureCategory.HTTP_NOT_FOUND
    assert result.http_status == 404

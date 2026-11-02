import pytest

from agentic_devtools.cli.ci.models import AgentTaskInventoryLoadResult
from agentic_devtools.cli.ci.pipeline.session_detector import _normalize_session_inventory


def test_complete_empty_legacy_list() -> None:
    result = _normalize_session_inventory([])
    assert result.complete
    assert result.tasks == ()


def test_malformed_legacy_list_is_incomplete() -> None:
    result = _normalize_session_inventory([None])
    assert not result.complete
    assert result.failure_category == "malformed_response"


@pytest.mark.parametrize("state", [None, "unknown", {}, ["running"]])
def test_unknown_states_never_prove_absence(state: object) -> None:
    result = _normalize_session_inventory([{"state": state}])
    assert not result.complete
    assert result.failure_category == "unknown_task_state"


def test_normalizes_successful_typed_unknown_rows() -> None:
    result = _normalize_session_inventory(AgentTaskInventoryLoadResult(({"state": "unexpected"},)))
    assert not result.complete
    assert result.failure_category == "unknown_task_state"


def test_preserves_incomplete_typed_failure() -> None:
    original = AgentTaskInventoryLoadResult((), complete=False, http_status=500)
    assert _normalize_session_inventory(original) is original

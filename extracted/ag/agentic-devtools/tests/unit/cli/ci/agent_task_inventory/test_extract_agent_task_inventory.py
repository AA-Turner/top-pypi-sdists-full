"""Tests for provider response envelope validation."""

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import (
    AgentTaskInventoryLoadResult,
    extract_agent_task_inventory,
)


@pytest.mark.parametrize("payload", [[], {"tasks": []}, {"tasks": [], "status": 200}, [{"id": "legacy"}]])
def test_preserves_legacy_lists(payload: object) -> None:
    expected = payload["tasks"] if isinstance(payload, dict) else payload
    assert extract_agent_task_inventory(payload) == expected


@pytest.mark.parametrize(
    ("status", "category"),
    [(401, "authentication"), (403, "permission"), (404, "http_not_found"), (500, "provider_unavailable")],
)
def test_http_failure_precedes_success_shaped_rows(status: int, category: str) -> None:
    result = extract_agent_task_inventory({"tasks": [], "status": status})
    assert isinstance(result, AgentTaskInventoryLoadResult)
    assert result.http_status == status
    assert result.failure_category == category
    assert result.availability == "unavailable"
    assert not result.complete


@pytest.mark.parametrize("payload", [None, {}, {"tasks": "invalid"}, ""])
def test_malformed_envelopes_remain_explicit_errors(payload: object) -> None:
    with pytest.raises(ValueError, match="no task list"):
        extract_agent_task_inventory(payload)


@pytest.mark.parametrize(
    "payload",
    [
        {"tasks": [], "error": "failed"},
        {"tasks": [], "errors": []},
        {"tasks": [], "message": "failed"},
        {"tasks": [], "status": "error"},
        {"tasks": [], "status": "failed"},
        {"tasks": [], "status": "success"},
        {"tasks": [], "status": None},
        {"tasks": [], "status": False},
        {"tasks": [], "error": None},
        {"tasks": [], "errors": []},
        {"tasks": [], "message": ""},
        {"tasks": [], "status": []},
        {"tasks": [], "status": 99},
        {"tasks": [], "status": 600},
        {"tasks": [], "status": 404.0},
    ],
)
def test_error_shaped_envelopes_cannot_be_complete(payload: object) -> None:
    with pytest.raises(ValueError, match="invalid page envelope"):
        extract_agent_task_inventory(payload)

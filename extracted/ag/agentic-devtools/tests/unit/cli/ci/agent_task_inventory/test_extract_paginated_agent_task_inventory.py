"""Per-document validation must precede task-page aggregation."""

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import (
    AgentTaskInventoryLoadResult,
    extract_paginated_agent_task_inventory,
)


@pytest.mark.parametrize("raw", ["", "  ", "null", "[]", '"text"', "false", "1", "{}"])
def test_invalid_inventory_is_unavailable(raw: str) -> None:
    result = extract_paginated_agent_task_inventory(raw)
    assert isinstance(result, AgentTaskInventoryLoadResult)
    assert not result.complete
    assert result.availability == "unavailable"


@pytest.mark.parametrize(
    "page",
    [
        '{"tasks": null}',
        '{"tasks": "bad"}',
        "null",
        "[]",
        '{"tasks": [], "status": 500}',
        '{"tasks": [], "error": "failed"}',
        '{"tasks": [], "errors": []}',
        '{"tasks": [], "message": "failed"}',
        "invalid",
    ],
)
def test_later_failure_preserves_rows_and_incompleteness(page: str) -> None:
    result = extract_paginated_agent_task_inventory('{"tasks": [{"id": "first"}], "status": 200}\n' + page)
    assert isinstance(result, AgentTaskInventoryLoadResult)
    assert result.tasks == ({"id": "first"},)
    assert not result.complete
    assert result.availability == "partial"
    assert result.incomplete_reasons
    if "500" in page:
        assert result.http_status == 500


def test_later_error_envelope_preserves_rows_and_http_diagnostic() -> None:
    result = extract_paginated_agent_task_inventory(
        '{"tasks": [{"id": "first"}]}\n{"tasks": [], "status": 200, "error": null}'
    )
    assert isinstance(result, AgentTaskInventoryLoadResult)
    assert result.tasks == ({"id": "first"},)
    assert not result.complete
    assert result.availability == "partial"
    assert result.failure_category == "malformed_response"
    assert result.http_status == 200


def test_valid_pages_merge_without_losing_rows() -> None:
    assert extract_paginated_agent_task_inventory(
        '{"tasks": [{"id": "first"}]}\n{"tasks": []}\n{"tasks": [{"id": "last"}]}'
    ) == [{"id": "first"}, {"id": "last"}]


def test_valid_later_page_cannot_erase_earlier_failure() -> None:
    result = extract_paginated_agent_task_inventory('{"tasks": null}\n{"tasks": [{"id": "last"}]}')
    assert isinstance(result, AgentTaskInventoryLoadResult)
    assert not result.complete
    assert result.tasks == ({"id": "last"},)

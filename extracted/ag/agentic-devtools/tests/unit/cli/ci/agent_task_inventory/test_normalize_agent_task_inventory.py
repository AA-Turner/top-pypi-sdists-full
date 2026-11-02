"""Tests for shared normalization at provider inventory boundaries."""

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import (
    AgentTaskInventoryLoadResult,
    normalize_agent_task_inventory,
)
from agentic_devtools.cli.ci.models import AgentTaskInventory, AgentTaskLifecycle


def test_preserves_raw_typed_results() -> None:
    result = AgentTaskInventoryLoadResult(({"state": "running"},), False)
    assert normalize_agent_task_inventory(result) is result


def test_preserves_lifecycle_inventory_typing() -> None:
    task = AgentTaskLifecycle("task", "owner/repo", 42, "branch", "running", "")
    result = AgentTaskInventory((task,))
    assert normalize_agent_task_inventory(result) is result


def test_validates_legacy_raw_rows() -> None:
    row = {"state": "running"}
    result = normalize_agent_task_inventory([row, None])
    assert result.tasks == (row,)
    assert result.availability == "partial"
    assert result.failure_category == "malformed_response"


def test_valid_empty_legacy_list_is_complete() -> None:
    assert normalize_agent_task_inventory([]).complete


def test_legacy_none_never_establishes_absence() -> None:
    result = normalize_agent_task_inventory(None)
    assert result.availability == "unavailable"
    assert result.failure_category == "provider_unavailable"


@pytest.mark.parametrize("value", [(), {}, 42, "rows"])
def test_other_legacy_values_are_malformed(value) -> None:
    result = normalize_agent_task_inventory(value)
    assert result.availability == "unavailable"
    assert result.failure_category == "malformed_response"

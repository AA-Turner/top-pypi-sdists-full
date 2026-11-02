"""Tests for retaining usable rows and rejection reasons."""

from agentic_devtools.cli.ci.agent_task_inventory import _filter_agent_task_rows


def test_preserves_raw_rows_and_all_failure_reasons() -> None:
    row = {"state": "running", "additional": {"field": "unchanged"}}
    result = _filter_agent_task_rows([None, row, {"state": "future"}])
    assert result.tasks == (row,)
    assert result.tasks[0] is row
    assert result.incomplete_reasons == ("row 0: malformed_response", "row 2: unknown_task_state")
    assert result.failure_category == "malformed_response"

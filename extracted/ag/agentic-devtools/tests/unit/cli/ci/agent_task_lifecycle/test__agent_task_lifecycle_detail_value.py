"""Tests for resolving aliased Agent Task detail values."""

from agentic_devtools.cli.ci.agent_task_lifecycle import _agent_task_lifecycle_detail_value


def test_prefers_record_alias_before_metadata() -> None:
    assert _agent_task_lifecycle_detail_value({"state": None, "metadata": {"state": "running"}}, "state") is None


def test_reads_aliases_from_metadata_and_returns_none_when_missing() -> None:
    record = {"metadata": {"status": "running"}}

    assert _agent_task_lifecycle_detail_value(record, "state", "status") == "running"
    assert _agent_task_lifecycle_detail_value(record, "session_id") is None

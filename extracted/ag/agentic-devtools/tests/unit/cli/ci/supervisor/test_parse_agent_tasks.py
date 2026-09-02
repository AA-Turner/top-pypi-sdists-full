"""Tests for parsing the agent-task list response."""

import json

from agentic_devtools.cli.ci.supervisor import parse_agent_tasks


def test_parse_agent_tasks_accepts_json_list() -> None:
    assert parse_agent_tasks(json.dumps([{"id": "one"}])) == [{"id": "one"}]


def test_parse_agent_tasks_returns_empty_for_invalid_payload() -> None:
    assert parse_agent_tasks("not-json") == []
    assert parse_agent_tasks(None) == []
    assert parse_agent_tasks(json.dumps({"tasks": []})) == []


def test_parse_agent_tasks_filters_non_object_entries() -> None:
    assert parse_agent_tasks(json.dumps([{"id": "one"}, "bad", 3])) == [{"id": "one"}]

"""Tests for _assignment_state()."""

from agentic_devtools.cli.ci.agent_assignment import _assignment_state


def test_returns_none_for_non_dict_payload() -> None:
    assert _assignment_state([]) is None


def test_detects_nested_copilot_identity() -> None:
    payload = {"assignees": [{"app": {"login": "Copilot"}}]}
    assert _assignment_state(payload) is True


def test_returns_none_for_malformed_assignee_entries() -> None:
    payload = {"assignees": [{"login": "octocat"}, None]}
    assert _assignment_state(payload) is None


def test_returns_true_when_malformed_entries_still_include_copilot_identity() -> None:
    payload = {"assignees": [None, {"login": "copilot-swe-agent[bot]"}]}
    assert _assignment_state(payload) is True


def test_returns_none_for_non_dict_singular_assignee() -> None:
    assert _assignment_state({"assignee": []}) is None


def test_returns_none_for_malformed_nested_assignee_entry() -> None:
    payload: dict[str, list[dict[str, list[object]]]] = {"assignees": [{"user": []}]}
    assert _assignment_state(payload) is None

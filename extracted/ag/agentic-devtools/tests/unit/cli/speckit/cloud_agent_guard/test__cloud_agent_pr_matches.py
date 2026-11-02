"""Tests for _cloud_agent_pr_matches."""

from __future__ import annotations

from agentic_devtools.cli.speckit.cloud_agent_guard import _cloud_agent_pr_matches


def test_returns_false_for_non_dict_input() -> None:
    assert _cloud_agent_pr_matches(None, issue_number=7, phase=1) is False


def test_returns_false_for_phase_mismatch() -> None:
    pull_request = {
        "user": {"login": "copilot-swe-agent"},
        "base": {"ref": "main"},
        "body": (
            "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
            "issue=7 phase=2 hierarchy=feature correlation_id=123e4567-e89b-12d3-a456-426614174000 -->"
        ),
    }
    assert _cloud_agent_pr_matches(pull_request, issue_number=7, phase=1) is False


def test_returns_false_for_phase_three_hierarchy_mismatch_on_specific_lookup() -> None:
    pull_request = {
        "user": {"login": "copilot-swe-agent"},
        "base": {"ref": "speckit/7/phase-2-clarify"},
        "body": (
            "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
            "issue=7 phase=3 hierarchy=feature correlation_id=123e4567-e89b-12d3-a456-426614174000 -->"
        ),
    }
    assert _cloud_agent_pr_matches(pull_request, issue_number=7, phase=3, hierarchy_level="task") is False


def test_uses_marker_hierarchy_for_any_phase_lookup() -> None:
    pull_request = {
        "user": {"login": "copilot-swe-agent"},
        "base": {"ref": "main"},
        "body": (
            "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
            "issue=7 phase=3 hierarchy=task correlation_id=123e4567-e89b-12d3-a456-426614174000 -->"
        ),
    }
    assert _cloud_agent_pr_matches(pull_request, issue_number=7, phase=3) is True

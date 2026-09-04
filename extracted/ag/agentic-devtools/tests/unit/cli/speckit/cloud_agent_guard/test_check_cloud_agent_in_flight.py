"""Tests for the shared Cloud Agent in-flight guard."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.cloud_agent_guard import (
    check_cloud_agent_in_flight,
)


def _marker(issue: int = 7, phase: int = 1, hierarchy: str = "feature") -> str:
    return (
        "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
        f"issue={issue} phase={phase} hierarchy={hierarchy} "
        "correlation_id=123e4567-e89b-12d3-a456-426614174000 -->"
    )


@pytest.mark.parametrize(
    ("labels", "pulls", "phase", "expected_reason"),
    [
        ([{"name": "speckit:agent-assigned-phase-2"}], [], 0, "label"),
        (
            [],
            [{"number": 44, "user": {"login": "COPILOT-SWE-AGENT[bot]"}, "base": {"ref": "main"}, "body": _marker()}],
            1,
            "pull-request",
        ),
        ([{"name": "speckit:agent-assigned-phase-2"}], [], 1, "none"),
    ],
)
def test_detects_matching_labels_and_pull_requests(
    labels: list[dict], pulls: list[dict], phase: int, expected_reason: str
) -> None:
    with patch(
        "agentic_devtools.cli.speckit.cloud_agent_guard._gh_api_call",
        side_effect=[json.dumps(labels), json.dumps(pulls)],
    ):
        result = check_cloud_agent_in_flight("owner/repo", 7, phase=phase, token="secret")

    assert result.in_flight is (expected_reason != "none")
    assert result.reason == expected_reason
    assert result.matched_label == ("speckit:agent-assigned-phase-2" if expected_reason == "label" else None)
    assert result.matched_pr_number == (44 if expected_reason == "pull-request" else None)


def test_ignores_fallback_nonmatching_and_malformed_pull_requests() -> None:
    pulls = [
        {"number": 1, "user": {"login": "someone"}, "base": {"ref": "main"}, "body": _marker()},
        {"number": 2, "user": {"login": "copilot-swe-agent"}, "base": {"ref": "wrong"}, "body": _marker()},
        {
            "number": 3,
            "user": {"login": "copilot-swe-agent"},
            "base": {"ref": "main"},
            "body": "speckit:agent-fallback",
        },
    ]
    with patch(
        "agentic_devtools.cli.speckit.cloud_agent_guard._gh_api_call",
        side_effect=[json.dumps([]), json.dumps(pulls)],
    ):
        result = check_cloud_agent_in_flight("owner/repo", 7, phase=1, token="secret")

    assert result.in_flight is False
    assert result.reason == "none"


def test_ignores_malformed_label_entries_and_phase_mismatch() -> None:
    pulls = [{"user": {"login": "copilot-swe-agent"}, "base": {"ref": "main"}, "body": _marker(7, 2)}]
    with patch(
        "agentic_devtools.cli.speckit.cloud_agent_guard._gh_api_call",
        side_effect=[json.dumps([None, {"name": 123}]), json.dumps(pulls)],
    ):
        result = check_cloud_agent_in_flight("owner/repo", 7, phase=1, token="secret")

    assert result.in_flight is False


def test_ignores_pull_request_with_unsupported_marker_hierarchy() -> None:
    pulls = [
        {
            "number": 44,
            "user": {"login": "copilot-swe-agent[bot]"},
            "base": {"ref": "speckit/7/phase-2-clarify"},
            "body": _marker(7, 3, "invalid"),
        }
    ]
    with patch(
        "agentic_devtools.cli.speckit.cloud_agent_guard._gh_api_call",
        side_effect=[json.dumps([]), json.dumps(pulls)],
    ):
        result = check_cloud_agent_in_flight("owner/repo", 7, phase=3, token="secret")

    assert result.in_flight is False
    assert result.reason == "none"


def test_specific_phase_three_lookup_requires_matching_hierarchy_level() -> None:
    pulls = [
        {
            "number": 44,
            "user": {"login": "copilot-swe-agent[bot]"},
            "base": {"ref": "speckit/7/phase-2-clarify"},
            "body": _marker(7, 3, "feature"),
        }
    ]
    with patch(
        "agentic_devtools.cli.speckit.cloud_agent_guard._gh_api_call",
        side_effect=[json.dumps([]), json.dumps(pulls)],
    ):
        result = check_cloud_agent_in_flight("owner/repo", 7, phase=3, hierarchy_level="task", token="secret")

    assert result.in_flight is False
    assert result.reason == "none"


def test_any_phase_lookup_uses_marker_hierarchy_for_task_pull_request() -> None:
    pulls = [
        {
            "number": 44,
            "user": {"login": "copilot-swe-agent[bot]"},
            "base": {"ref": "main"},
            "body": _marker(7, 3, "task"),
        }
    ]
    with patch(
        "agentic_devtools.cli.speckit.cloud_agent_guard._gh_api_call",
        side_effect=[json.dumps([]), json.dumps(pulls)],
    ):
        result = check_cloud_agent_in_flight("owner/repo", 7, phase=0, token="secret")

    assert result.in_flight is True
    assert result.reason == "pull-request"
    assert result.matched_pr_number == 44


def test_rejects_invalid_hierarchy_level() -> None:
    with pytest.raises(ValueError, match="hierarchy_level"):
        check_cloud_agent_in_flight("owner/repo", 7, hierarchy_level="invalid", token="secret")


@pytest.mark.parametrize("payload", ["", "   \n\t  "])
def test_raises_on_empty_paginated_payload(payload: str) -> None:
    with patch(
        "agentic_devtools.cli.speckit.cloud_agent_guard._gh_api_call",
        side_effect=[payload, json.dumps([])],
    ):
        with pytest.raises(RuntimeError, match="empty response"):
            check_cloud_agent_in_flight("owner/repo", 7, token="secret")


@pytest.mark.parametrize("payload", ["{}", "null"])
def test_raises_on_non_array_paginated_labels_payload(payload: str) -> None:
    with patch(
        "agentic_devtools.cli.speckit.cloud_agent_guard._gh_api_call",
        side_effect=[payload, json.dumps([])],
    ):
        with pytest.raises(RuntimeError, match="non-array response"):
            check_cloud_agent_in_flight("owner/repo", 7, token="secret")


@pytest.mark.parametrize("payload", ["{}", "null"])
def test_raises_on_non_array_paginated_pulls_payload(payload: str) -> None:
    with patch(
        "agentic_devtools.cli.speckit.cloud_agent_guard._gh_api_call",
        side_effect=[json.dumps([]), payload],
    ):
        with pytest.raises(RuntimeError, match="non-array response"):
            check_cloud_agent_in_flight("owner/repo", 7, token="secret")


def test_uses_token_fallback_and_paginated_documents() -> None:
    with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "", "COPILOT_GITHUB_TOKEN": "fallback"}, clear=False):
        with patch(
            "agentic_devtools.cli.speckit.cloud_agent_guard._gh_api_call",
            side_effect=[json.dumps([]) + "\n" + json.dumps([]), json.dumps([])],
        ) as api:
            result = check_cloud_agent_in_flight("owner/repo", 7)

    assert result.in_flight is False
    assert api.call_args.kwargs["token"] == "fallback"

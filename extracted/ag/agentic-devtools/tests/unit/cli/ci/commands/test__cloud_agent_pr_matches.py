"""Tests for the _cloud_agent_pr_matches helper."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.commands import _cloud_agent_pr_matches


class TestCloudAgentPrMatches:
    """Unit tests for _cloud_agent_pr_matches."""

    @pytest.mark.parametrize(
        ("pr", "expected"),
        [
            (None, False),
            ({}, False),
            ({"user": {"login": "someone"}}, False),
            (
                {
                    "user": {"login": "copilot-swe-agent[bot]"},
                    "head": {"ref": "speckit/7/phase-1"},
                    "base": {"ref": "main"},
                    "body": (
                        "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
                        "issue=7 phase=1 hierarchy=feature "
                        "correlation_id=123e4567-e89b-12d3-a456-426614174000 -->"
                    ),
                },
                True,
            ),
            (
                {
                    "user": {"login": "copilot-swe-agent"},
                    "head": {"ref": "other"},
                    "base": {"ref": "main"},
                    "body": (
                        "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
                        "issue=7 phase=1 hierarchy=feature "
                        "correlation_id=123e4567-e89b-12d3-a456-426614174000 -->"
                    ),
                },
                True,
            ),
            (
                {
                    "user": {"login": "copilot-swe-agent[bot]"},
                    "head": {"ref": "speckit/7/phase-1"},
                    "base": {"ref": "wrong-base"},
                    "body": (
                        "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
                        "issue=7 phase=1 hierarchy=feature "
                        "correlation_id=123e4567-e89b-12d3-a456-426614174000 -->"
                    ),
                },
                False,
            ),
            (
                {
                    "user": {"login": "copilot-swe-agent[bot]"},
                    "head": {"ref": "other"},
                    "body": None,
                },
                False,
            ),
            (
                {
                    "user": {"login": "copilot-swe-agent[bot]"},
                    "head": {"ref": "speckit/7/phase-1"},
                    "base": {"ref": "main"},
                    "body": None,
                },
                False,
            ),
            (
                {
                    "user": {"login": "copilot-swe-agent[bot]"},
                    "head": {"ref": "other"},
                    "body": (
                        "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
                        "issue=8 phase=1 hierarchy=feature correlation_id=abc -->"
                    ),
                },
                False,
            ),
        ],
    )
    def test_cloud_agent_pr_matching(self, pr: object, expected: bool) -> None:
        assert _cloud_agent_pr_matches(pr, issue_number=7, phase=1) is expected

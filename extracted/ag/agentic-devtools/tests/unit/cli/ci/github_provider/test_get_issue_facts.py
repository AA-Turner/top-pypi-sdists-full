"""Tests for GitHubActionsProvider.get_issue_facts()."""

from __future__ import annotations

import json
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


class TestGetIssueFacts:
    """Tests for the minimal issue read used to cross-check a deferral issue."""

    def test_returns_lowercased_state_and_body(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        payload = json.dumps({"state": "OPEN", "body": "deferral"})
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=payload) as mock_api:
            facts = provider.get_issue_facts(1240)

        assert facts.number == 1240
        assert facts.state == "open"
        assert facts.body == "deferral"
        assert mock_api.call_args.args[0].endswith("/issues/1240")

    def test_missing_fields_degrade_to_empty_strings(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps({"body": None})):
            facts = provider.get_issue_facts(3)

        assert facts.state == ""
        assert facts.body == ""

    def test_marks_pull_request_targets(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        payload = json.dumps({"state": "open", "body": "body", "pull_request": {"url": "https://example.test"}})
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=payload):
            facts = provider.get_issue_facts(9)

        assert facts.resource_kind == "pull_request"

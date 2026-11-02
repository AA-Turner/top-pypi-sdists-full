"""Tests for the JiraProvider idempotency capability."""

from __future__ import annotations

from agentic_devtools.adapters.jira_provider import JiraProvider
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response


class TestJiraProviderCreateIssueKeySearch:
    """Tests for JiraProvider.create_issue."""

    def test_create_issue_with_orchestration_key_finds_existing(self):
        session = _make_mock_session()
        search_response = _make_response(200, {"issues": [{"key": "PROJ-99", "id": "10099"}]})
        session.request.return_value = search_response

        body = "Content\n\n<!-- agdt-orch-key:" + "a" * 64 + " -->"
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Title", body, "task", dry_run=False)
        assert result.status == "existing"
        assert result.identifier == "PROJ-99"

    def test_create_issue_orch_key_search_empty(self):
        session = _make_mock_session()
        search_response = _make_response(200, {"issues": []})
        create_response = _make_response(201, {"key": "PROJ-10", "id": "10010"})
        session.request.side_effect = [search_response, create_response]

        body = "Content\n\n<!-- agdt-orch-key:" + "c" * 64 + " -->"
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Title", body, "task", dry_run=False)
        assert result.status == "created"
        assert result.identifier == "PROJ-10"

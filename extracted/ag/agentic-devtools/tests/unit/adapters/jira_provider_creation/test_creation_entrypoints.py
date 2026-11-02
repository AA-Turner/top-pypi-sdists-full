"""Tests for Jira issue-creation facade entry points."""

from __future__ import annotations

from agentic_devtools.adapters.issue_provider import PreCreateLookup, ProviderIssueResult
from agentic_devtools.adapters.jira_provider import JiraProvider
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response


def _provider() -> JiraProvider:
    session = _make_mock_session()
    session.request.return_value = _make_response(201, {"id": "10001", "key": "PROJ-1"})
    return JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)


def test_create_issue_with_precreate_lookup_uses_public_creation_flow():
    provider = _provider()
    lookup = PreCreateLookup(orchestration_key="key", issue=None)

    result = provider.create_issue_with_precreate_lookup(
        "Title",
        "Body",
        "task",
        idempotency_key="key",
        precreate_lookup=lookup,
    )

    assert result.status == "created"
    assert result.identifier == "PROJ-1"


def test_create_issue_returns_result_recovered_after_request(monkeypatch):
    provider = _provider()
    recovered = ProviderIssueResult("PROJ-2", "https://jira.example.com/browse/PROJ-2", "existing")
    monkeypatch.setattr(provider, "_request_issue_creation", lambda *_args, **_kwargs: (None, recovered))
    lookup = PreCreateLookup(orchestration_key="key", issue=None)

    result = provider.create_issue(
        "Title",
        "Body",
        "task",
        idempotency_key="key",
        precreate_lookup=lookup,
    )

    assert result.status == "existing"
    assert result.identifier == "PROJ-2"

"""Tests for idempotency-cache lookups during issue creation."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import ProviderIssueResult
from agentic_devtools.adapters.jira_provider import JiraProvider
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session


def test_find_existing_issue_reuses_cached_idempotency_result():
    provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
    cached = ProviderIssueResult("PROJ-1", "https://jira.example.com/browse/PROJ-1", "created")
    provider._idempotency_keys["key"] = cached

    result = provider._find_existing_issue("key", None, "key", "key", None)

    assert result is not None
    assert result.identifier == cached.identifier
    assert result.status == "existing"


def test_find_existing_issue_returns_none_without_orchestration_key():
    provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())

    assert provider._find_existing_issue(None, None, None, "", None) is None


def test_find_existing_issue_does_not_cache_unkeyed_lookup(monkeypatch):
    provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
    existing = ProviderIssueResult("PROJ-2", "https://jira.example.com/browse/PROJ-2", "existing")
    monkeypatch.setattr(provider, "_find_by_orchestration_key", lambda _key: existing)

    result = provider._find_existing_issue(None, None, "legacy-key", "legacy-key", None)

    assert result is not None
    assert result.identifier == existing.identifier
    assert not provider._idempotency_keys


def test_issue_creation_request_propagates_transient_without_lookup_key(monkeypatch):
    provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())

    def fail_request(*_args, **_kwargs):
        raise TransientError("temporary outage", status_code=503)

    monkeypatch.setattr(provider, "_request", fail_request)
    with pytest.raises(TransientError, match="temporary outage"):
        provider._request_issue_creation("", "https://jira.example.com/issue", {})

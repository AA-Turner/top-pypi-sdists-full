"""Tests for Jira issue creation result construction."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.exceptions import HierarchyLinkError
from agentic_devtools.adapters.issue_provider import ProviderIssueResult, ProviderLinkResult
from agentic_devtools.adapters.jira_provider import JiraProvider
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response


def _provider() -> JiraProvider:
    return JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())


class TestCreatedIssueResult:
    def test_created_result_is_cached_without_hierarchy_result(self):
        provider = _provider()
        response = _make_response(200, {"id": "10001", "key": " PROJ-1 "})

        result = provider._build_created_issue_result(response, "key", None, "task")

        assert result.identifier == "PROJ-1"
        assert result.status == "created"
        assert result.hierarchy_link_result is None
        assert provider._idempotency_keys["key"] == ProviderIssueResult(
            "PROJ-1", "https://jira.example.com/browse/PROJ-1", "created", {"id": "10001"}
        )

    def test_created_result_includes_non_epic_parent_link(self):
        provider = _provider()
        response = _make_response(200, {"key": "PROJ-2"})

        result = provider._build_created_issue_result(response, None, "PROJ-1", "task")

        assert result.hierarchy_link_result == ProviderLinkResult("PROJ-1", "PROJ-2", "linked")

    @pytest.mark.parametrize("payload", [[1], {"key": 1}, {"key": ""}])
    def test_created_result_rejects_malformed_response(self, payload):
        provider = _provider()

        with pytest.raises(ValueError):
            provider._build_created_issue_result(_make_response(200, payload), None, None, "task")


class TestRecoveredIssueResult:
    def test_recovered_result_without_parent_is_cached(self):
        provider = _provider()
        recovered = ProviderIssueResult("PROJ-3", "https://jira.example.com/browse/PROJ-3", "existing")

        result = provider._build_recovered_issue_result(recovered, "key", None, "task")

        assert result.status == "existing"
        assert provider._idempotency_keys["key"] == result

    def test_recovered_epic_does_not_link_to_parent(self):
        provider = _provider()
        recovered = ProviderIssueResult("PROJ-3", "https://jira.example.com/browse/PROJ-3", "existing")

        result = provider._build_recovered_issue_result(recovered, None, "PROJ-1", "epic")

        assert result.hierarchy_link_result is None

    def test_recovered_issue_links_to_parent(self, monkeypatch):
        provider = _provider()
        recovered = ProviderIssueResult("PROJ-3", "https://jira.example.com/browse/PROJ-3", "existing")
        linked = ProviderLinkResult("PROJ-1", "PROJ-3", "already-linked")
        monkeypatch.setattr(provider, "link_subissue", lambda *_args, **_kwargs: linked)

        result = provider._build_recovered_issue_result(recovered, "key", "PROJ-1", "task")

        assert result.hierarchy_link_result == linked
        assert provider._idempotency_keys["key"].hierarchy_link_result == linked

    def test_recovered_issue_links_to_parent_without_idempotency_key(self, monkeypatch):
        provider = _provider()
        recovered = ProviderIssueResult("PROJ-3", "https://jira.example.com/browse/PROJ-3", "existing")
        linked = ProviderLinkResult("PROJ-1", "PROJ-3", "already-linked")
        monkeypatch.setattr(provider, "link_subissue", lambda *_args, **_kwargs: linked)

        result = provider._build_recovered_issue_result(recovered, None, "PROJ-1", "task")

        assert result.hierarchy_link_result == linked

    def test_recovered_issue_wraps_parent_link_failure(self, monkeypatch):
        provider = _provider()
        recovered = ProviderIssueResult("PROJ-3", "https://jira.example.com/browse/PROJ-3", "existing")

        def fail_link(*_args, **_kwargs):
            raise RuntimeError("link failed")

        monkeypatch.setattr(provider, "link_subissue", fail_link)
        with pytest.raises(HierarchyLinkError):
            provider._build_recovered_issue_result(recovered, None, "PROJ-1", "task")

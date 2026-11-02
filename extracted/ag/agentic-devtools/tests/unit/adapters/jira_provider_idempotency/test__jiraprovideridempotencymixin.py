"""Tests for the JiraProvider idempotency capability."""

from __future__ import annotations

import hashlib
from typing import Any
from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.exceptions import HierarchyLinkError
from agentic_devtools.adapters.issue_provider import (
    ProviderIssueResult,
)
from agentic_devtools.adapters.jira_provider import JiraProvider
from agentic_devtools.adapters.orchestration_key import embed_orchestration_key, generate_orchestration_key
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response


class TestJiraProviderIdempotencyKey:
    """Tests for create_issue idempotency_key deduplication."""

    def test_same_key_returns_existing(self):
        session = _make_mock_session()

        def mock_request(method, url, **kwargs):
            if method == "GET":
                return _make_response(200, {"issues": []})
            return _make_response(201, {"key": "PROJ-1", "id": "10001"})

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        first = provider.create_issue("Title", "Body", "task", idempotency_key="key-1", dry_run=False)
        assert first.status == "created"

        second = provider.create_issue("Title", "Body", "task", idempotency_key="key-1", dry_run=False)
        assert second.status == "existing"
        assert second.identifier == first.identifier
        # The first call searches the digest and legacy raw marker before POST;
        # the second call short-circuits via the in-memory cache.
        assert session.request.call_count == 3

    def test_same_key_hit_returns_detached_metadata_copy(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-1", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        first = provider.create_issue("Title", "Body", "task", idempotency_key="key-1", dry_run=False)
        second = provider.create_issue("Title", "Body", "task", idempotency_key="key-1", dry_run=False)

        second.metadata["mutated"] = "yes"
        third = provider.create_issue("Title", "Body", "task", idempotency_key="key-1", dry_run=False)

        assert first.metadata == {"id": "10001"}
        assert third.metadata == {"id": "10001"}

    def test_same_key_cache_hit_wraps_parent_link_failure(self, monkeypatch):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-1", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        cached = ProviderIssueResult(identifier="PROJ-1", url="u/1", status="existing")
        key = "key-1"
        normalized_key = hashlib.sha256(key.encode("utf-8")).hexdigest()
        provider._idempotency_keys[normalized_key] = cached

        def fail_link(parent_id, child_id, *, dry_run=False):
            raise RuntimeError("link failed")

        monkeypatch.setattr(provider, "link_subissue", fail_link)

        with pytest.raises(HierarchyLinkError, match="already exists.*linking.*failed") as exc_info:
            provider.create_issue("Title", "Body", "task", parent_id="PROJ-2", idempotency_key=key, dry_run=False)

        assert exc_info.value.created_result == cached
        assert exc_info.value.stage == "link_subissue"
        assert isinstance(exc_info.value.cause, RuntimeError)

    def test_different_keys_both_create(self):
        session = _make_mock_session()
        counter = {"n": 0}

        def mock_request(method, url, **kwargs):
            if method == "GET":
                return _make_response(200, {"issues": []})
            counter["n"] += 1
            return _make_response(201, {"key": f"PROJ-{counter['n']}", "id": str(10000 + counter["n"])})

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        first = provider.create_issue("Title 1", "Body", "task", idempotency_key="key-1", dry_run=False)
        second = provider.create_issue("Title 2", "Body", "task", idempotency_key="key-2", dry_run=False)
        assert first.identifier != second.identifier
        # Each create searches the digest and legacy raw marker before its POST.
        assert session.request.call_count == 6

    def test_none_key_skips_dedup(self):
        session = _make_mock_session()
        counter = {"n": 0}

        def mock_request(method, url, **kwargs):
            counter["n"] += 1
            return _make_response(201, {"key": f"PROJ-{counter['n']}", "id": str(10000 + counter["n"])})

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        first = provider.create_issue("Title", "Body", "task", idempotency_key=None, dry_run=False)
        second = provider.create_issue("Title", "Body", "task", idempotency_key=None, dry_run=False)
        assert first.identifier != second.identifier
        assert session.request.call_count == 2

    def test_empty_key_skips_dedup(self):
        session = _make_mock_session()
        counter = {"n": 0}

        def mock_request(method, url, **kwargs):
            counter["n"] += 1
            return _make_response(201, {"key": f"PROJ-{counter['n']}", "id": str(10000 + counter["n"])})

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        first = provider.create_issue("Title", "Body", "task", idempotency_key="", dry_run=False)
        second = provider.create_issue("Title", "Body", "task", idempotency_key="", dry_run=False)
        assert first.identifier != second.identifier
        assert session.request.call_count == 2

    def test_whitespace_key_skips_dedup(self):
        session = _make_mock_session()
        counter = {"n": 0}

        def mock_request(method, url, **kwargs):
            counter["n"] += 1
            return _make_response(201, {"key": f"PROJ-{counter['n']}", "id": str(10000 + counter["n"])})

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        first = provider.create_issue("Title", "Body", "task", idempotency_key="   ", dry_run=False)
        second = provider.create_issue("Title", "Body", "task", idempotency_key="   ", dry_run=False)
        assert first.identifier != second.identifier
        assert session.request.call_count == 2

    def test_key_is_stripped_before_dedup_lookup(self):
        session = _make_mock_session()

        def mock_request(method, url, **kwargs):
            if method == "GET":
                return _make_response(200, {"issues": []})
            return _make_response(201, {"key": "PROJ-1", "id": "10001"})

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        first = provider.create_issue("Title", "Body", "task", idempotency_key="key-1", dry_run=False)
        second = provider.create_issue("Title", "Body", "task", idempotency_key=" key-1 ", dry_run=False)
        assert first.status == "created"
        assert second.status == "existing"
        # The first call searches both digest and legacy raw markers before POST.
        assert session.request.call_count == 3

    def test_jql_escapes_quotes_and_backslashes_in_key(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(200, {"issues": []})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        provider.find_existing_issue('key" OR project = "OTHER\\path')

        queries = [call.kwargs["params"]["jql"] for call in session.request.call_args_list]
        key = hashlib.sha256(b'key" OR project = "OTHER\\path').hexdigest()
        assert queries[0] == f'project = "PROJ" AND description ~ "agdt-orch-key:{key}"'
        assert queries[1] == 'project = "PROJ" AND description ~ "agdt-orch-key:key\\" OR project = \\"OTHER\\\\path"'

    def test_idempotency_key_takes_precedence_over_body_orchestration_key(self):
        """The supplied idempotency key replaces a conflicting body marker."""
        session = _make_mock_session()
        orch_key = generate_orchestration_key("create_issue", "epic.features[0]")
        search_response = _make_response(200, {"issues": [{"key": "PROJ-99", "id": "10099"}]})
        session.request.return_value = search_response

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        body = embed_orchestration_key("Body", orch_key)

        result = provider.create_issue("Title", body, "task", idempotency_key="unique-key", dry_run=False)
        assert result.status == "existing"
        assert result.identifier == "PROJ-99"
        query = session.request.call_args.kwargs["params"]["jql"]
        unique_key = hashlib.sha256(b"unique-key").hexdigest()
        assert f"agdt-orch-key:{unique_key}" in query
        assert f"agdt-orch-key:{orch_key}" not in query

    def test_idempotency_key_replaces_a_body_orchestration_marker(self):
        session = _make_mock_session()
        captured: dict[str, Any] = {}
        body_key = generate_orchestration_key("create_issue", "another-tree", "epic")
        supplied_key = generate_orchestration_key("create_issue", "active-tree", "epic")

        def mock_request(method, url, **kwargs):
            if method == "GET":
                captured["jql"] = kwargs["params"]["jql"]
                return _make_response(200, {"issues": []})
            captured["description"] = kwargs["json"]["fields"]["description"]
            return _make_response(201, {"key": "PROJ-1", "id": "10001"})

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        provider.create_issue(
            "Title",
            embed_orchestration_key("Body", body_key),
            "task",
            idempotency_key=supplied_key,
            dry_run=False,
        )

        assert f"agdt-orch-key:{supplied_key}" in captured["jql"]
        assert f"agdt-orch-key:{supplied_key}" in captured["description"]
        assert f"agdt-orch-key:{body_key}" not in captured["description"]

    def test_idempotency_key_is_embedded_in_description(self):
        """The idempotency key must be persisted in the issue body, not just in memory."""
        session = _make_mock_session()
        captured: dict[str, Any] = {}

        def mock_request(method, url, **kwargs):
            if method == "GET":
                return _make_response(200, {"issues": []})
            captured["description"] = kwargs["json"]["fields"]["description"]
            return _make_response(201, {"key": "PROJ-1", "id": "10001"})

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        orch_key = generate_orchestration_key("create_issue", "epic.features[0]")
        provider.create_issue("Title", "Body", "task", idempotency_key=orch_key, dry_run=False)

        assert f"<!-- agdt-orch-key:{orch_key} -->" in captured["description"]

    def test_fresh_provider_instance_recovers_via_durable_key(self):
        """A fresh provider (no in-memory cache) must recover via a durable JQL search.

        Simulates a rerun after Jira created the issue but before the caller
        persisted the identifier â€” the second, unrelated ``JiraProvider``
        instance must find the existing issue instead of creating a duplicate.
        """
        orch_key = generate_orchestration_key("create_issue", "epic.features[0]")
        first_session = _make_mock_session()
        created_description: dict[str, Any] = {}

        def first_mock_request(method, url, **kwargs):
            if method == "GET":
                return _make_response(200, {"issues": []})
            created_description["value"] = kwargs["json"]["fields"]["description"]
            return _make_response(201, {"key": "PROJ-1", "id": "10001"})

        first_session.request.side_effect = first_mock_request
        first_provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=first_session)
        first_result = first_provider.create_issue("Title", "Body", "task", idempotency_key=orch_key, dry_run=False)
        assert first_result.status == "created"

        # A brand-new provider instance has no in-memory idempotency cache.
        second_session = _make_mock_session()

        def second_mock_request(method, url, **kwargs):
            assert method == "GET"
            assert orch_key in kwargs["params"]["jql"]
            return _make_response(200, {"issues": [{"key": "PROJ-1", "id": "10001"}]})

        second_session.request.side_effect = second_mock_request
        second_provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=second_session)
        second_result = second_provider.create_issue("Title", "Body", "task", idempotency_key=orch_key, dry_run=False)

        assert second_result.status == "existing"
        assert second_result.identifier == "PROJ-1"
        # Only the recovery search was issued â€” no duplicate create POST.
        assert second_session.request.call_count == 1


class TestJiraProviderExistingIssueQueries:
    """Tests for existing issue queries used by Jira idempotency."""

    def test_find_by_orchestration_key_exception_propagates(self):
        """FR-009: Network errors propagate instead of being swallowed."""
        session = _make_mock_session()
        session.request.side_effect = Exception("network error")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(Exception, match="network error"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_transient_error_reraises(self):
        session = _make_mock_session()
        session.request.side_effect = TransientError("rate limited", status_code=429)
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(TransientError, match="rate limited"):
            provider._find_by_orchestration_key("abc123")

    def test_find_existing_issue_multi_match_raises(self):
        """FR-008: Multiple issues matching same key raises ValueError."""
        session = _make_mock_session()
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {
            "issues": [
                {"key": "PROJ-1", "fields": {"description": "body1"}},
                {"key": "PROJ-2", "fields": {"description": "body2"}},
            ]
        }
        session.request.return_value = resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Ambiguous"):
            provider.find_existing_issue("some-key")

    def test_find_existing_issue_non_dict_response_raises(self):
        """find_existing_issue raises ValueError when Jira returns a non-dict payload."""
        session = _make_mock_session()
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = ["unexpected", "list"]
        session.request.return_value = resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="expected a JSON object from Jira search"):
            provider.find_existing_issue("some-key")

    def test_find_existing_issue_non_list_issues_raises(self):
        """find_existing_issue raises ValueError when 'issues' field is not a list."""
        session = _make_mock_session()
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"issues": "not-a-list"}
        session.request.return_value = resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="expected 'issues' to be a list"):
            provider.find_existing_issue("some-key")

    def test_find_existing_issue_non_dict_issue_entry_raises(self):
        """find_existing_issue raises ValueError when an issue entry is not a dict."""
        session = _make_mock_session()
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"issues": ["PROJ-1"]}  # string instead of dict
        session.request.return_value = resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="expected issue entry to be a JSON object"):
            provider.find_existing_issue("some-key")

    def test_find_existing_issue_missing_key_field_raises(self):
        """find_existing_issue raises ValueError when issue dict has no 'key' field."""
        session = _make_mock_session()
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"issues": [{"id": "10001", "fields": {}}]}  # no 'key'
        session.request.return_value = resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="expected issue 'key' to be a non-empty string"):
            provider.find_existing_issue("some-key")

    def test_find_existing_issue_null_key_raises(self):
        """find_existing_issue raises ValueError when issue 'key' is null."""
        session = _make_mock_session()
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"issues": [{"key": None, "id": "10001"}]}
        session.request.return_value = resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="expected issue 'key' to be a non-empty string"):
            provider.find_existing_issue("some-key")

    def test_find_existing_issue_whitespace_key_raises(self):
        """find_existing_issue raises ValueError when issue 'key' is whitespace-only."""
        session = _make_mock_session()
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"issues": [{"key": "   ", "id": "10001"}]}
        session.request.return_value = resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="expected issue 'key' to be a non-empty string"):
            provider.find_existing_issue("some-key")

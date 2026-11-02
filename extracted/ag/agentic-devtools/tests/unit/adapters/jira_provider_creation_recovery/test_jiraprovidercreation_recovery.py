"""Tests for the JiraProvider creation capability."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.exceptions import HierarchyLinkError
from agentic_devtools.adapters.issue_provider import (
    PreCreateLookup,
    ProviderIssueResult,
    ProviderLinkResult,
)
from agentic_devtools.adapters.jira_provider import JiraProvider
from agentic_devtools.adapters.orchestration_key import embed_orchestration_key
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response


class TestJiraProviderCreateIssueRecovery:
    """Tests for JiraProvider.create_issue."""

    def test_create_issue_recovers_committed_create_after_transient_response(self):
        key = "f" * 64
        session = _make_mock_session()
        session.request.side_effect = [
            _make_response(503, text="Service unavailable"),
            _make_response(200, {"issues": []}),
            _make_response(200, {"issues": [{"key": "PROJ-10", "id": "10010"}]}),
        ]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=key,
            precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
        )

        assert result.status == "existing"
        assert result.identifier == "PROJ-10"
        assert session.request.call_count == 3
        assert [call.args[0] for call in session.request.call_args_list] == ["POST", "GET", "GET"]

    def test_create_issue_returns_recovered_issue_with_hierarchy_result(self, monkeypatch):
        key = "f" * 64
        session = _make_mock_session()
        session.request.side_effect = [
            _make_response(200, {"issues": []}),
            _make_response(503, text="Service unavailable"),
            _make_response(200, {"issues": [{"key": "PROJ-10", "id": "10010"}]}),
        ]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        provider._epic_link_field = "customfield_10008"
        link_result = ProviderLinkResult("PROJ-1", "PROJ-10", "already-linked")
        link_calls = []

        def link_subissue(parent_id, child_id, *, dry_run=False):
            link_calls.append((parent_id, child_id))
            return link_result

        monkeypatch.setattr(provider, "link_subissue", link_subissue)

        create_issue = getattr(provider.create_issue, "__wrapped__")
        result = create_issue(
            provider,
            "Title",
            embed_orchestration_key("Body", key),
            "task",
            parent_id="PROJ-1",
        )

        assert result.status == "existing"
        assert result.identifier == "PROJ-10"
        assert result.hierarchy_link_result == link_result
        assert link_calls == [("PROJ-1", "PROJ-10")]
        assert [call.args[0] for call in session.request.call_args_list] == ["GET", "POST", "GET"]

    def test_create_issue_caches_recovered_hierarchy_result(self, monkeypatch):
        key = "f" * 64
        session = _make_mock_session()
        session.request.side_effect = [
            _make_response(503, text="Service unavailable"),
            _make_response(200, {"issues": [{"key": "PROJ-10", "id": "10010"}]}),
        ]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        provider._epic_link_field = "customfield_10008"
        link_result = ProviderLinkResult("PROJ-1", "PROJ-10", "already-linked")
        monkeypatch.setattr(provider, "link_subissue", lambda *_args, **_kwargs: link_result)

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            parent_id="PROJ-1",
            idempotency_key=key,
            precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
        )

        assert result.status == "existing"
        assert result.hierarchy_link_result == link_result
        assert provider._idempotency_keys[key].hierarchy_link_result == link_result

    def test_create_issue_recovery_wraps_parent_link_failure(self, monkeypatch):
        key = "f" * 64
        session = _make_mock_session()
        session.request.side_effect = [
            _make_response(503, text="Service unavailable"),
            _make_response(200, {"issues": [{"key": "PROJ-10", "id": "10010"}]}),
        ]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        provider._epic_link_field = "customfield_10008"

        def fail_link(*_args, **_kwargs):
            raise RuntimeError("link failed")

        monkeypatch.setattr(provider, "link_subissue", fail_link)
        create_issue = getattr(provider.create_issue, "__wrapped__")

        with pytest.raises(HierarchyLinkError, match="already exists") as exc_info:
            create_issue(
                provider,
                "Title",
                "Body",
                "task",
                parent_id="PROJ-1",
                idempotency_key=key,
                precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
            )

        assert exc_info.value.created_result.identifier == "PROJ-10"
        assert exc_info.value.created_result.status == "existing"
        assert exc_info.value.stage == "link_subissue"
        assert provider._idempotency_keys[key].identifier == "PROJ-10"
        assert provider._idempotency_keys[key].status == "existing"
        assert [call.args[0] for call in session.request.call_args_list] == ["POST", "GET"]

    @pytest.mark.parametrize(
        ("lookup_error", "expected_create_attempts"),
        [
            (None, 1),
            (RuntimeError("search unavailable"), 1),
            (TransientError("search unavailable", status_code=503), 1),
        ],
    )
    def test_create_issue_stops_after_unresolved_transient_create(
        self, monkeypatch, lookup_error, expected_create_attempts
    ):
        monkeypatch.setattr("agentic_devtools.adapters.retry.time.sleep", lambda *_args, **_kwargs: None)
        key = "a" * 64
        session = _make_mock_session()
        session.request.return_value = _make_response(503, text="Service unavailable")
        session.request.side_effect = None
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        if lookup_error is None:

            def lookup(_key):
                return None
        else:

            def lookup(_key):
                raise lookup_error

        monkeypatch.setattr(provider, "_find_by_orchestration_key", lookup)

        with pytest.raises(RuntimeError, match="outcome is uncertain"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key=key,
                precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
            )

        assert sum(call.args[0] == "POST" for call in session.request.call_args_list) == expected_create_attempts

    def test_create_issue_retries_when_recovery_lookup_is_transient(self, monkeypatch):
        monkeypatch.setattr("agentic_devtools.adapters.retry.time.sleep", lambda *_args, **_kwargs: None)
        key = "a" * 64
        session = _make_mock_session()
        session.request.return_value = _make_response(503, text="Service unavailable")
        recovered = ProviderIssueResult(identifier="PROJ-10", url="u/10", status="existing")
        lookups = iter([TransientError("search unavailable", status_code=503), recovered])

        def lookup(_key):
            result = next(lookups)
            if isinstance(result, TransientError):
                raise result
            return result

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        monkeypatch.setattr(provider, "_find_by_orchestration_key", lookup)

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=key,
            precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
        )

        assert result.status == "existing"
        assert [call.args[0] for call in session.request.call_args_list] == ["POST"]

    def test_create_issue_rechecks_after_transient_recovery_lookup(self, monkeypatch):
        monkeypatch.setattr("agentic_devtools.adapters.retry.time.sleep", lambda *_args, **_kwargs: None)
        key = "a" * 64
        session = _make_mock_session()
        session.request.return_value = _make_response(503, text="Service unavailable")
        recovered = ProviderIssueResult(identifier="PROJ-10", url="u/10", status="existing")
        lookups = iter([None, TransientError("search unavailable", status_code=503), recovered])

        def lookup(_key):
            result = next(lookups)
            if isinstance(result, TransientError):
                raise result
            return result

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        monkeypatch.setattr(provider, "_find_by_orchestration_key", lookup)

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=key,
            precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
        )

        assert result.status == "existing"
        assert [call.args[0] for call in session.request.call_args_list] == ["POST"]

    def test_create_issue_stops_when_retry_lookup_fails(self, monkeypatch):
        monkeypatch.setattr("agentic_devtools.adapters.retry.time.sleep", lambda *_args, **_kwargs: None)
        key = "a" * 64
        session = _make_mock_session()
        session.request.return_value = _make_response(503, text="Service unavailable")
        lookups = iter([None, RuntimeError("search unavailable")])

        def lookup(_key):
            result = next(lookups)
            if isinstance(result, Exception):
                raise result
            return result

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        monkeypatch.setattr(provider, "_find_by_orchestration_key", lookup)

        with pytest.raises(RuntimeError, match="outcome is uncertain"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key=key,
                precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
            )

        assert [call.args[0] for call in session.request.call_args_list] == ["POST"]

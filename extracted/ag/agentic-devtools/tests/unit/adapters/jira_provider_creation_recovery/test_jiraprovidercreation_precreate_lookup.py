"""Tests for the JiraProvider creation capability."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.exceptions import HierarchyLinkError
from agentic_devtools.adapters.issue_provider import (
    DefinitiveCreationFailure,
    PreCreateLookup,
    ProviderIssueResult,
)
from agentic_devtools.adapters.jira_provider import JiraProvider
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response


class TestJiraProviderCreateIssuePrecreateLookup:
    """Tests for JiraProvider.create_issue."""

    def test_create_issue_reuses_precreate_lookup_miss(self, monkeypatch):
        key = "d" * 64
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-10", "id": "10010"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        monkeypatch.setattr(
            provider,
            "_find_by_orchestration_key",
            lambda _key: pytest.fail("pre-create lookup miss must not be searched again"),
        )

        result = provider.create_issue_with_precreate_lookup(
            "Title",
            "Body",
            "task",
            idempotency_key=key,
            precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
        )

        assert result.status == "created"
        assert result.identifier == "PROJ-10"
        assert session.request.call_count == 1

    def test_create_issue_reuses_precreate_lookup_match(self, monkeypatch):
        key = "e" * 64
        existing = ProviderIssueResult(identifier="PROJ-99", url="u/99", status="existing")
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        monkeypatch.setattr(
            provider,
            "_find_by_orchestration_key",
            lambda _key: pytest.fail("pre-create lookup match must be reused"),
        )

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=key,
            precreate_lookup=PreCreateLookup(orchestration_key=key, issue=existing),
        )

        assert result.status == "existing"
        assert result.identifier == "PROJ-99"
        assert session.request.call_count == 0

    def test_create_issue_precreate_match_wraps_parent_link_failure(self, monkeypatch):
        key = "f" * 64
        existing = ProviderIssueResult(identifier="PROJ-99", url="u/99", status="existing")
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        monkeypatch.setattr(
            provider,
            "link_subissue",
            lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("link failed")),
        )

        with pytest.raises(HierarchyLinkError) as exc_info:
            provider.create_issue(
                "Title",
                "Body",
                "task",
                parent_id="PROJ-1",
                idempotency_key=key,
                precreate_lookup=PreCreateLookup(orchestration_key=key, issue=existing),
            )

        assert exc_info.value.created_result is existing
        assert exc_info.value.stage == "link_subissue"
        assert str(exc_info.value.cause) == "link failed"
        assert session.request.call_count == 0

    def test_create_issue_rejects_mismatched_precreate_lookup_key(self):
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=_make_mock_session(),
        )

        with pytest.raises(DefinitiveCreationFailure, match="must match"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key="key-1",
                precreate_lookup=PreCreateLookup(orchestration_key="key-2", issue=None),
            )

    def test_create_issue_rejects_unverified_legacy_match(self, monkeypatch):
        tree_key = "a" * 64
        legacy_key = "b" * 64
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=_make_mock_session(),
        )
        monkeypatch.setattr(
            provider,
            "_find_by_orchestration_key",
            lambda key: (
                ProviderIssueResult(identifier="PROJ-99", url="u/99", status="existing") if key == legacy_key else None
            ),
        )

        with pytest.raises(DefinitiveCreationFailure, match="(?i)unverified legacy.*e1"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key=tree_key,
                precreate_lookup=PreCreateLookup(
                    orchestration_key=tree_key,
                    issue=None,
                    legacy_orchestration_key=legacy_key,
                    node_ref="e1",
                ),
            )

    def test_create_issue_reuses_verified_legacy_match(self, monkeypatch):
        tree_key = "e" * 64
        legacy_key = "f" * 64
        existing = ProviderIssueResult(identifier="PROJ-99", url="u/99", status="existing")
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=_make_mock_session(),
        )
        monkeypatch.setattr(
            provider,
            "_find_by_orchestration_key",
            lambda key: existing if key == legacy_key else None,
        )

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=tree_key,
            precreate_lookup=PreCreateLookup(
                orchestration_key=tree_key,
                issue=None,
                legacy_orchestration_key=legacy_key,
                legacy_adoption_permitted=True,
                node_ref="e1",
            ),
        )

        assert result.status == "existing"
        assert result.identifier == existing.identifier

    def test_create_issue_accepts_same_match_for_both_keys(self, monkeypatch):
        tree_key = "a" * 64
        legacy_key = "b" * 64
        existing = ProviderIssueResult(identifier="PROJ-99", url="u/99", status="existing")
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=_make_mock_session(),
        )
        monkeypatch.setattr(provider, "_find_by_orchestration_key", lambda _key: existing)

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=tree_key,
            precreate_lookup=PreCreateLookup(
                orchestration_key=tree_key,
                issue=existing,
                legacy_orchestration_key=legacy_key,
                node_ref="e1",
            ),
        )

        assert result.status == "existing"
        assert result.identifier == existing.identifier

    @pytest.mark.parametrize(
        ("legacy_key", "node_ref", "permitted"),
        [("", "e1", False), ("b" * 64, None, False), ("b" * 64, "e1", 1)],
    )
    def test_create_issue_rejects_invalid_legacy_lookup(self, legacy_key, node_ref, permitted):
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=_make_mock_session(),
        )

        with pytest.raises(DefinitiveCreationFailure, match="legacy candidate is invalid"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key="a" * 64,
                precreate_lookup=PreCreateLookup(
                    orchestration_key="a" * 64,
                    issue=None,
                    legacy_orchestration_key=legacy_key,
                    legacy_adoption_permitted=permitted,
                    node_ref=node_ref,
                ),
            )

    def test_create_issue_rejects_precreate_match_conflicting_with_cache(self):
        tree_key = "a" * 64
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=_make_mock_session(),
        )
        provider._idempotency_keys[tree_key] = ProviderIssueResult(identifier="PROJ-98", url="u/98", status="existing")

        with pytest.raises(DefinitiveCreationFailure, match="Ambiguous tree-scoped lookup"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key=tree_key,
                precreate_lookup=PreCreateLookup(
                    orchestration_key=tree_key,
                    issue=ProviderIssueResult(identifier="PROJ-99", url="u/99", status="existing"),
                ),
            )

    def test_create_issue_accepts_precreate_match_matching_cache(self):
        tree_key = "a" * 64
        existing = ProviderIssueResult(identifier="PROJ-98", url="u/98", status="existing")
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=_make_mock_session(),
        )
        provider._idempotency_keys[tree_key] = existing

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=tree_key,
            precreate_lookup=PreCreateLookup(orchestration_key=tree_key, issue=existing),
        )

        assert result.status == "existing"
        assert result.identifier == existing.identifier

    def test_create_issue_rejects_ambiguous_tree_and_legacy_matches(self, monkeypatch):
        tree_key = "c" * 64
        legacy_key = "d" * 64
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=_make_mock_session(),
        )
        monkeypatch.setattr(
            provider,
            "_find_by_orchestration_key",
            lambda key: (
                ProviderIssueResult(identifier="PROJ-99", url="u/99", status="existing") if key == legacy_key else None
            ),
        )

        with pytest.raises(DefinitiveCreationFailure, match="(?i)ambiguous.*e1"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key=tree_key,
                precreate_lookup=PreCreateLookup(
                    orchestration_key=tree_key,
                    issue=ProviderIssueResult(identifier="PROJ-98", url="u/98", status="existing"),
                    legacy_orchestration_key=legacy_key,
                    node_ref="e1",
                ),
            )

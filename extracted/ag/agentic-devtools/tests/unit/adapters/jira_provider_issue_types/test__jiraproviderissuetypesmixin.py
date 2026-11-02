"""Tests for the JiraProvider issue types capability."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.exceptions import AdapterValidationError
from agentic_devtools.adapters.issue_provider import (
    DefinitiveCreationFailure,
    HierarchyValidationProvider,
    IssueProvider,
)
from agentic_devtools.adapters.jira_provider import JiraProvider
from tests.unit.adapters.conftest import build_jira_contract_provider
from tests.unit.adapters.issue_provider import _contract_scenarios as contract
from tests.unit.adapters.jira_provider._fixtures import (
    _assert_jira_provider_conforms,
    _make_mock_session,
    _make_response,
)


class TestJiraProviderNormalizeIssueType:
    """Tests for _normalize_issue_type with canonical neutral keys."""

    def test_valid_types_resolve(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert provider._normalize_issue_type("epic") == "Epic"
        assert provider._normalize_issue_type("feature") == "Story"
        assert provider._normalize_issue_type("subtask") == "Sub-task"
        assert provider._normalize_issue_type("task") == "Task"
        assert provider._normalize_issue_type("bug") == "Bug"

    def test_case_insensitive(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert provider._normalize_issue_type("EPIC") == "Epic"
        assert provider._normalize_issue_type("Feature") == "Story"

    def test_invalid_type_raises_valueerror(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        with pytest.raises(DefinitiveCreationFailure, match="Unsupported issue type"):
            provider._normalize_issue_type("story")

    def test_invalid_type_error_includes_sorted_valid_types(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        with pytest.raises(DefinitiveCreationFailure, match=r"\['bug', 'epic', 'feature', 'subtask', 'task'\]"):
            provider._normalize_issue_type("invalid")

    def test_empty_type_raises_definitive_creation_failure(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        with pytest.raises(DefinitiveCreationFailure, match="non-empty string"):
            provider._normalize_issue_type("")


class TestJiraProviderSetIssueType:
    """Tests for JiraProvider.set_issue_type."""

    def test_set_issue_type_success(self):
        session = _make_mock_session()
        get_response = _make_response(200, {"fields": {"issuetype": {"name": "Task"}}})
        put_response = _make_response(204)
        session.request.side_effect = [get_response, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.set_issue_type("  PROJ-1  ", "feature", dry_run=False)
        assert result.status == "updated"
        assert result.identifier == "PROJ-1"
        assert result.metadata["issue_type"] == "Story"
        call_args_list = session.request.call_args_list
        assert "/issue/PROJ-1?fields=issuetype" in call_args_list[0][0][1]
        assert "/issue/PROJ-1" in call_args_list[1][0][1]

    def test_set_issue_type_dry_run(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.set_issue_type("  PROJ-1  ", "bug", dry_run=True)
        assert result.status == "dry-run"
        assert result.identifier == "PROJ-1"
        assert result.metadata["issue_type"] == "Bug"
        session.request.assert_not_called()

    def test_set_issue_type_unknown_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Unsupported issue type"):
            provider.set_issue_type("PROJ-1", "story", dry_run=False)

    def test_set_issue_type_noop_when_matches(self):
        session = _make_mock_session()
        get_response = _make_response(200, {"fields": {"issuetype": {"name": "Bug"}}})
        session.request.return_value = get_response

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.set_issue_type("PROJ-1", "bug", dry_run=False)
        assert result.status == "no-op"
        assert result.metadata["issue_type"] == "Bug"
        # Only one GET call â€” no PUT
        assert session.request.call_count == 1

    def test_set_issue_type_empty_identifier_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="identifier must be non-empty"):
            provider.set_issue_type("", "bug", dry_run=False)

    def test_set_issue_type_whitespace_identifier_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="identifier must be non-empty"):
            provider.set_issue_type("   ", "bug", dry_run=False)

    def test_set_issue_type_not_found_raises(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(404)
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="not found"):
            provider.set_issue_type("PROJ-999", "bug", dry_run=False)

    def test_set_issue_type_empty_identifier_raises_before_dryrun(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="identifier must be non-empty"):
            provider.set_issue_type("", "bug", dry_run=True)

    def test_set_issue_type_non_dict_get_response_raises(self):
        """set_issue_type raises ValueError when the GET response is not a dict."""
        session = _make_mock_session()
        session.request.return_value = _make_response(200, [{"unexpected": "list"}])
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Unexpected response type"):
            provider.set_issue_type("PROJ-1", "bug", dry_run=False)

    def test_set_issue_type_fields_is_list_proceeds_to_put(self):
        """When GET response has `fields` as a list (non-dict), current_type falls back to '' and PUT proceeds."""
        session = _make_mock_session()
        # GET returns a dict but with `fields` as a non-empty list â€” a truthy non-dict value.
        # Without the isinstance guard, .get("issuetype") would raise AttributeError.
        get_response = _make_response(200, {"fields": ["unexpected", "list"]})
        put_response = _make_response(204)
        session.request.side_effect = [get_response, put_response]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.set_issue_type("PROJ-1", "bug", dry_run=False)
        assert result.status == "updated"
        assert session.request.call_count == 2


class TestJiraProviderResolveIdentifier:
    """Tests for JiraProvider.resolve_identifier."""

    def test_resolve_success(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(200, {"key": "PROJ-1", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.resolve_identifier("PROJ-1", dry_run=False)
        assert result.status == "resolved"
        assert result.identifier == "PROJ-1"
        assert result.metadata["internal_id"] == "10001"

    def test_resolve_dry_run(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.resolve_identifier("PROJ-1", dry_run=True)
        assert result.status == "dry-run"
        assert result.identifier == "PROJ-1"
        assert result.url == ""
        assert result.metadata == {}
        session.request.assert_not_called()

    def test_resolve_empty_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="identifier must be non-empty"):
            provider.resolve_identifier("", dry_run=False)

    def test_resolve_whitespace_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="identifier must be non-empty"):
            provider.resolve_identifier("   ", dry_run=False)

    def test_resolve_empty_raises_before_dryrun_check(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="identifier must be non-empty"):
            provider.resolve_identifier("", dry_run=True)

    def test_resolve_not_found_raises(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(404)
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="not found"):
            provider.resolve_identifier("PROJ-999", dry_run=False)

    def test_resolve_non_dict_json_raises_valueerror(self):
        """resolve_identifier raises ValueError when Jira returns a non-dict JSON payload."""
        session = _make_mock_session()
        session.request.return_value = _make_response(200, [{"unexpected": "list"}])
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Unexpected response type"):
            provider.resolve_identifier("PROJ-1", dry_run=False)

    def test_resolve_trailing_slash_stripped(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(200, {"key": "PROJ-1", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com/", session=session)
        result = provider.resolve_identifier("PROJ-1", dry_run=False)
        assert "jira.example.com/browse/PROJ-1" in result.url
        assert "//" not in result.url.replace("https://", "")

    def test_resolve_strips_whitespace_live(self):
        """resolve_identifier strips surrounding whitespace before the API call."""
        session = _make_mock_session()
        session.request.return_value = _make_response(200, {"key": "PROJ-1", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.resolve_identifier("  PROJ-1  ", dry_run=False)
        assert result.identifier == "PROJ-1"
        call_url = session.request.call_args[0][1]
        assert "PROJ-1" in call_url
        assert "  " not in call_url

    def test_resolve_strips_whitespace_dry_run(self):
        """resolve_identifier dry-run returns stripped identifier."""
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.resolve_identifier("  PROJ-1  ", dry_run=True)
        assert result.identifier == "PROJ-1"
        session.request.assert_not_called()

    def test_resolve_non_string_key_in_response_falls_back_to_identifier(self):
        """When Jira returns a non-string key, the original identifier is used."""
        session = _make_mock_session()
        session.request.return_value = _make_response(200, {"key": 12345, "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.resolve_identifier("PROJ-1", dry_run=False)
        assert result.identifier == "PROJ-1"
        assert "PROJ-1" in result.url

    def test_resolve_whitespace_key_in_response_falls_back_to_identifier(self):
        """When Jira returns a whitespace-only key, the original identifier is used."""
        session = _make_mock_session()
        session.request.return_value = _make_response(200, {"key": "   ", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.resolve_identifier("PROJ-1", dry_run=False)
        assert result.identifier == "PROJ-1"
        assert "PROJ-1" in result.url

    def test_resolve_padded_key_in_response_is_stripped(self):
        """When Jira returns a key with surrounding whitespace, the stripped value is used."""
        session = _make_mock_session()
        session.request.return_value = _make_response(200, {"key": "  PROJ-1  ", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.resolve_identifier("PROJ-1", dry_run=False)
        assert result.identifier == "PROJ-1"
        assert "PROJ-1" in result.url


class TestJiraProviderNormalizeIdentifier:
    """Tests for JiraProvider.normalize_identifier."""

    def test_returns_unchanged(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert provider.normalize_identifier("PROJ-123") == "PROJ-123"

    def test_strips_surrounding_whitespace(self):
        """normalize_identifier strips surrounding whitespace to return canonical form."""
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert provider.normalize_identifier("  PROJ-123  ") == "PROJ-123"

    def test_empty_raises(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        with pytest.raises(ValueError, match="identifier must be non-empty"):
            provider.normalize_identifier("")

    def test_whitespace_raises(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        with pytest.raises(ValueError, match="identifier must be non-empty"):
            provider.normalize_identifier("   ")


class TestJiraProviderFormatIdentifier:
    """Tests for JiraProvider.format_identifier."""

    def test_returns_unchanged(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert provider.format_identifier("PROJ-123") == "PROJ-123"

    def test_strips_surrounding_whitespace(self):
        """format_identifier strips surrounding whitespace before returning."""
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert provider.format_identifier("  PROJ-123  ") == "PROJ-123"

    def test_empty_raises(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        with pytest.raises(ValueError, match="identifier must be non-empty"):
            provider.format_identifier("")

    def test_whitespace_raises(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        with pytest.raises(ValueError, match="identifier must be non-empty"):
            provider.format_identifier("   ")


class TestJiraProviderProtocolConformance:
    """Tests for IssueProvider protocol conformance."""

    def test_isinstance_issue_provider(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert isinstance(provider, IssueProvider)

    def test_mypy_conformance(self):
        """Static type check: JiraProvider satisfies IssueProvider."""
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        _assert_jira_provider_conforms(provider)


class TestJiraContract(
    contract.TestContractCreateIssue,
    contract.TestContractCreateIssueDryRun,
    contract.TestContractCreateIssueIdempotent,
    contract.TestContractSetIssueType,
    contract.TestContractSetIssueTypeTransition,
    contract.TestContractSetIssueTypeDryRun,
    contract.TestContractLinkSubissue,
    contract.TestContractLinkSubissueDryRun,
    contract.TestContractAddBlockedBy,
    contract.TestContractAddBlockedByDryRun,
    contract.TestContractApplyLabels,
    contract.TestContractApplyLabelsDryRun,
    contract.TestContractApplyLabelsIdempotent,
    contract.TestContractIdempotentRelink,
    contract.TestContractIdempotentBlockedBy,
    contract.TestContractResolveIdentifier,
    contract.TestContractResolveIdentifierDryRun,
    contract.TestContractNormalizeIdentifier,
    contract.TestContractFormatIdentifier,
    contract.TestContractTransientError,
    contract.TestContractNonTransientApiFailure,
):
    """Runs the shared contract suite against JiraProvider (fake REST session)."""

    sample_identifier = "CONTRACT-1"
    non_transient_exc_type = Exception

    @pytest.fixture()
    def provider(self):
        prov, session = build_jira_contract_provider()
        self._session = session
        return prov

    def boundary_calls(self, provider):
        return self._session.call_count

    def seed_issue(self, provider):
        return provider.create_issue("Seed", "Seed body", "task").identifier

    def seed_two_issues(self, provider):
        first = provider.create_issue("First", "first body", "task").identifier
        second = provider.create_issue("Second", "second body", "task").identifier
        return first, second

    def make_transient_create_provider(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(429, text="rate limited")
        return JiraProvider(project_key="CONTRACT", base_url="https://jira.test", session=session)

    def make_non_transient_create_provider(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(400, text="bad request")
        return JiraProvider(project_key="CONTRACT", base_url="https://jira.test", session=session)


class TestJiraProviderHierarchyValidation:
    """Provider-contract hierarchy validation for Jira (FR-001, FR-016)."""

    def _provider(self):
        return JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=_make_mock_session(),
        )

    def test_validate_issue_type_accepts_supported_types(self):
        provider = self._provider()
        for issue_type in ("epic", "feature", "task", "bug", "subtask"):
            assert provider.validate_issue_type(issue_type) is None

    def test_validate_issue_type_is_case_insensitive(self):
        assert self._provider().validate_issue_type("Subtask") is None

    def test_validate_issue_type_rejects_unsupported_type(self):
        with pytest.raises(AdapterValidationError):
            self._provider().validate_issue_type("saga")

    def test_validate_issue_type_rejects_empty_string(self):
        with pytest.raises(AdapterValidationError):
            self._provider().validate_issue_type("  ")

    def test_validate_issue_type_rejects_non_string(self):
        with pytest.raises(AdapterValidationError):
            self._provider().validate_issue_type(None)  # type: ignore[arg-type]

    def test_validate_hierarchy_pair_accepts_valid_pairs(self):
        provider = self._provider()
        assert provider.validate_hierarchy_pair("feature", "epic") is None
        assert provider.validate_hierarchy_pair("subtask", "feature") is None

    def test_validate_hierarchy_pair_rejects_same_level(self):
        with pytest.raises(AdapterValidationError):
            self._provider().validate_hierarchy_pair("feature", "feature")

    def test_validate_hierarchy_pair_rejects_inverted_pair(self):
        with pytest.raises(AdapterValidationError):
            self._provider().validate_hierarchy_pair("epic", "feature")

    def test_provider_is_hierarchy_validation_capable(self):
        assert isinstance(self._provider(), HierarchyValidationProvider)

"""Tests for JiraProvider — all class methods in one test file per 1:1:1 policy."""

from __future__ import annotations

import json
import os
from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.adapters.exceptions import AdapterValidationError
from agentic_devtools.adapters.issue_provider import (
    HierarchyValidationProvider,
    IssueProvider,
    ProviderIssueResult,
)
from agentic_devtools.adapters.jira_provider import JiraProvider
from agentic_devtools.adapters.orchestration_key import embed_orchestration_key, generate_orchestration_key
from agentic_devtools.adapters.retry import TransientError


def _make_mock_session():
    """Create a mock requests session."""
    return MagicMock()


def _make_response(status_code=200, json_data=None, text=None):
    """Create a mock response."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data or {}
    resp.text = text if text is not None else json.dumps(json_data or {})
    resp.raise_for_status = MagicMock()
    if status_code >= 400:
        resp.raise_for_status.side_effect = Exception(f"HTTP {status_code}")
    return resp


# ======================================================================
# Constructor & Configuration
# ======================================================================


class TestJiraProviderInit:
    """Tests for JiraProvider.__init__ validation and configuration."""

    def test_empty_project_key_raises(self):
        with pytest.raises(ValueError, match="project_key must be non-empty"):
            JiraProvider(project_key="", base_url="https://jira.example.com", session=_make_mock_session())

    def test_whitespace_project_key_raises(self):
        with pytest.raises(ValueError, match="project_key must be non-empty"):
            JiraProvider(project_key="   ", base_url="https://jira.example.com", session=_make_mock_session())

    def test_empty_base_url_no_env_raises(self):
        with patch.dict(os.environ, {"JIRA_BASE_URL": ""}, clear=False):
            with pytest.raises(ValueError, match="Jira base URL is not configured"):
                JiraProvider(project_key="PROJ", base_url="", session=_make_mock_session())

    def test_base_url_from_env(self):
        with patch.dict(os.environ, {"JIRA_BASE_URL": "https://from-env.example.com"}, clear=False):
            provider = JiraProvider(project_key="PROJ", base_url=None, session=_make_mock_session())
        assert provider._base_url == "https://from-env.example.com"

    def test_base_url_strips_trailing_slash(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com/", session=_make_mock_session())
        assert provider._base_url == "https://jira.example.com"

    def test_project_key_is_stripped_before_storage(self):
        provider = JiraProvider(project_key=" PROJ ", base_url="https://jira.example.com", session=_make_mock_session())
        assert provider.project_key == "PROJ"

    def test_base_url_strips_surrounding_whitespace(self):
        provider = JiraProvider(
            project_key="PROJ",
            base_url=" https://jira.example.com/path/ ",
            session=_make_mock_session(),
        )
        assert provider._base_url == "https://jira.example.com/path"

    def test_issue_type_map_empty_value_raises(self):
        with pytest.raises(ValueError, match="issue_type_map value"):
            JiraProvider(
                project_key="PROJ",
                base_url="https://jira.example.com",
                session=_make_mock_session(),
                issue_type_map={"epic": ""},
            )

    def test_issue_type_map_whitespace_value_raises(self):
        with pytest.raises(ValueError, match="issue_type_map value"):
            JiraProvider(
                project_key="PROJ",
                base_url="https://jira.example.com",
                session=_make_mock_session(),
                issue_type_map={"epic": "   "},
            )

    def test_issue_type_map_unknown_key_raises(self):
        with pytest.raises(ValueError, match="issue_type_map key"):
            JiraProvider(
                project_key="PROJ",
                base_url="https://jira.example.com",
                session=_make_mock_session(),
                issue_type_map={"story": "Story"},
            )

    def test_issue_type_map_invalid_key_raises(self):
        with pytest.raises(ValueError, match="issue_type_map key"):
            JiraProvider(
                project_key="PROJ",
                base_url="https://jira.example.com",
                session=_make_mock_session(),
                issue_type_map={"unknown_type": "SomeJiraType"},
            )

    def test_issue_type_map_non_string_key_raises(self):
        """Constructor raises ValueError when issue_type_map has a non-string key."""
        with pytest.raises(ValueError, match="issue_type_map key must be a string"):
            JiraProvider(
                project_key="PROJ",
                base_url="https://jira.example.com",
                session=_make_mock_session(),
                issue_type_map={42: "Story"},  # type: ignore[arg-type]
            )

    def test_issue_type_map_uppercase_key_accepted(self):
        """Uppercase keys are normalized to lowercase and accepted."""
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=_make_mock_session(),
            issue_type_map={"EPIC": "UpperEpos"},
        )
        assert provider._effective_type_map["epic"] == "UpperEpos"

    def test_issue_type_map_overrides_defaults(self):
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=_make_mock_session(),
            issue_type_map={"epic": "Epos"},
        )
        assert provider._effective_type_map["epic"] == "Epos"
        # Other defaults still present
        assert provider._effective_type_map["task"] == "Task"

    def test_issue_type_map_strips_override_values(self):
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=_make_mock_session(),
            issue_type_map={"epic": " Epos "},
        )
        assert provider._effective_type_map["epic"] == "Epos"

    def test_no_custom_map_uses_defaults(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert provider._effective_type_map["epic"] == "Epic"
        assert provider._effective_type_map["feature"] == "Story"
        assert provider._effective_type_map["subtask"] == "Sub-task"

    def test_project_key_property(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert provider.project_key == "PROJ"


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
        with pytest.raises(ValueError, match="Unsupported issue type"):
            provider._normalize_issue_type("story")

    def test_invalid_type_error_includes_sorted_valid_types(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        with pytest.raises(ValueError, match=r"\['bug', 'epic', 'feature', 'subtask', 'task'\]"):
            provider._normalize_issue_type("invalid")


# ======================================================================
# create_issue
# ======================================================================


class TestJiraProviderCreateIssue:
    """Tests for JiraProvider.create_issue."""

    def test_create_issue_success(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-1", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Title", "Body", "task", dry_run=False)
        assert isinstance(result, ProviderIssueResult)
        assert result.identifier == "PROJ-1"
        assert result.status == "created"

    def test_create_issue_dry_run(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Title", "Body", "epic", dry_run=True)
        assert result.status == "dry-run"
        assert result.identifier == ""
        session.request.assert_not_called()

    def test_create_issue_dry_run_invalid_type_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Unsupported issue type"):
            provider.create_issue("Title", "Body", "invalid-type", dry_run=True)
        session.request.assert_not_called()

    def test_create_issue_empty_title_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="title must be non-empty"):
            provider.create_issue("", "Body", "task")

    def test_create_issue_whitespace_title_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="title must be non-empty"):
            provider.create_issue("   ", "Body", "task")

    def test_create_issue_empty_parent_id_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="parent_id must be a non-empty string"):
            provider.create_issue("Title", "Body", "task", parent_id="")

    def test_create_issue_whitespace_parent_id_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="parent_id must be a non-empty string"):
            provider.create_issue("Title", "Body", "task", parent_id="   ")

    def test_create_issue_strips_parent_id_in_payload(self):
        """parent_id with surrounding whitespace is stripped before being sent to Jira."""
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-5", "id": "10005"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Sub", "Body", "subtask", parent_id="  PROJ-1  ", dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["fields"]["parent"] == {"key": "PROJ-1"}

    def test_create_epic_with_native_type(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-2", "id": "10002"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Epic Title", "Body", "epic", dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["fields"]["issuetype"]["name"] == "Epic"

    def test_create_epic_sets_epic_name_field(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-2", "id": "10002"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("My Epic Name", "Body", "epic", dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["fields"]["customfield_10006"] == "My Epic Name"

    def test_create_non_epic_does_not_set_epic_name_field(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-3", "id": "10003"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Task Title", "Body", "task", dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert "customfield_10006" not in payload["fields"]

    def test_create_issue_with_parent_sets_epic_link(self):
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        create_response = _make_response(201, {"key": "PROJ-3", "id": "10003"})
        session.request.side_effect = [field_response, create_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Child", "Body", "feature", parent_id="PROJ-1", dry_run=False)
        assert result.status == "created"

    def test_create_issue_with_parent_subtask(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-5", "id": "10005"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Sub", "Body", "subtask", parent_id="PROJ-1", dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["fields"]["parent"] == {"key": "PROJ-1"}

    def test_create_epic_with_parent_skips_linking(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-6", "id": "10006"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Epic", "Body", "epic", parent_id="PROJ-1", dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert "parent" not in payload["fields"]

    def test_create_issue_with_labels(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-7", "id": "10007"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Title", "Body", "task", labels=["label1", "label2"], dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["fields"]["labels"] == ["label1", "label2"]

    def test_create_issue_labels_normalized_and_filtered(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-17", "id": "10017"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        mixed_labels = [" label1 ", "", "label1", "  ", "label2", 42]
        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            labels=cast("list[str]", mixed_labels),
            dry_run=False,
        )
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["fields"]["labels"] == ["label1", "label2"]

    def test_create_issue_empty_labels_excluded_from_payload(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-8", "id": "10008"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Title", "Body", "task", labels=[], dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert "labels" not in payload["fields"]

    def test_create_issue_no_labels_excluded_from_payload(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-9", "id": "10009"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Title", "Body", "task", dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert "labels" not in payload["fields"]

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

    def test_create_issue_feature_maps_to_story(self):
        """create_issue with issue_type='feature' maps to Jira's 'Story' type."""
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-11", "id": "10011"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.create_issue("Feature Title", "Body", "feature", dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["fields"]["issuetype"]["name"] == "Story"

    def test_create_issue_custom_type_map(self):
        """create_issue with custom issue_type_map uses overridden type names and still sets epic fields."""
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-12", "id": "10012"})
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=session,
            issue_type_map={"epic": "Epos", "feature": "Anforderung"},
        )
        result = provider.create_issue("Title", "Body", "epic", dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["fields"]["issuetype"]["name"] == "Epos"
        # customfield_10006 must be set even when the Jira-native name is "Epos" (not "epic")
        assert payload["fields"]["customfield_10006"] == "Title"

    def test_create_epic_custom_type_with_parent_skips_linking(self):
        """Custom epic type skips parent linking (no parent field, no epic-link field)."""
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-13", "id": "10013"})
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=session,
            issue_type_map={"epic": "Epos"},
        )
        result = provider.create_issue("Epos Title", "Body", "epic", parent_id="PROJ-1", dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        # Parent field must NOT be set for epics (same as default "epic" behavior)
        assert "parent" not in payload["fields"]

    def test_create_subtask_custom_type_sets_parent_field(self):
        """Custom subtask type still sets the parent field."""
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-14", "id": "10014"})
        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=session,
            issue_type_map={"subtask": "Teilaufgabe"},
        )
        result = provider.create_issue("Sub", "Body", "subtask", parent_id="PROJ-1", dry_run=False)
        assert result.status == "created"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["fields"]["issuetype"]["name"] == "Teilaufgabe"
        assert payload["fields"]["parent"] == {"key": "PROJ-1"}

    def test_create_issue_non_dict_response_raises(self):
        """create_issue raises ValueError when Jira returns a non-dict JSON payload."""
        session = _make_mock_session()
        session.request.return_value = _make_response(201, [{"unexpected": "list"}])
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Unexpected response type"):
            provider.create_issue("Title", "Body", "task", dry_run=False)

    def test_create_issue_missing_key_in_response_raises(self):
        """create_issue raises ValueError when Jira response omits the issue key."""
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="valid issue key"):
            provider.create_issue("Title", "Body", "task", dry_run=False)

    def test_create_issue_empty_key_in_response_raises(self):
        """create_issue raises ValueError when Jira response contains an empty issue key."""
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "  ", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="valid issue key"):
            provider.create_issue("Title", "Body", "task", dry_run=False)

    def test_create_issue_non_string_key_in_response_raises(self):
        """create_issue raises ValueError when Jira response contains a non-string issue key."""
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": 12345, "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="valid issue key"):
            provider.create_issue("Title", "Body", "task", dry_run=False)


class TestJiraProviderIdempotencyKey:
    """Tests for create_issue idempotency_key deduplication."""

    def test_same_key_returns_existing(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-1", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        first = provider.create_issue("Title", "Body", "task", idempotency_key="key-1", dry_run=False)
        assert first.status == "created"

        second = provider.create_issue("Title", "Body", "task", idempotency_key="key-1", dry_run=False)
        assert second.status == "existing"
        assert second.identifier == first.identifier
        # Only one API call was made (second was deduplicated)
        assert session.request.call_count == 1

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

    def test_different_keys_both_create(self):
        session = _make_mock_session()
        counter = {"n": 0}

        def mock_request(method, url, **kwargs):
            counter["n"] += 1
            return _make_response(201, {"key": f"PROJ-{counter['n']}", "id": str(10000 + counter["n"])})

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        first = provider.create_issue("Title 1", "Body", "task", idempotency_key="key-1", dry_run=False)
        second = provider.create_issue("Title 2", "Body", "task", idempotency_key="key-2", dry_run=False)
        assert first.identifier != second.identifier
        assert session.request.call_count == 2

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
        session.request.return_value = _make_response(201, {"key": "PROJ-1", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        first = provider.create_issue("Title", "Body", "task", idempotency_key="key-1", dry_run=False)
        second = provider.create_issue("Title", "Body", "task", idempotency_key=" key-1 ", dry_run=False)
        assert first.status == "created"
        assert second.status == "existing"
        assert session.request.call_count == 1

    def test_orch_key_still_works_with_idempotency_key(self):
        """Orchestration-key and idempotency_key are independent dedup mechanisms."""
        session = _make_mock_session()
        orch_key = generate_orchestration_key("create_issue", "epic.features[0]")
        search_response = _make_response(200, {"issues": [{"key": "PROJ-99", "id": "10099"}]})
        session.request.return_value = search_response

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        body = embed_orchestration_key("Body", orch_key)

        result = provider.create_issue("Title", body, "task", idempotency_key="unique-key", dry_run=False)
        assert result.status == "existing"
        assert result.identifier == "PROJ-99"


# ======================================================================
# set_issue_type
# ======================================================================


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
        # Only one GET call — no PUT
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
        # GET returns a dict but with `fields` as a non-empty list — a truthy non-dict value.
        # Without the isinstance guard, .get("issuetype") would raise AttributeError.
        get_response = _make_response(200, {"fields": ["unexpected", "list"]})
        put_response = _make_response(204)
        session.request.side_effect = [get_response, put_response]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.set_issue_type("PROJ-1", "bug", dry_run=False)
        assert result.status == "updated"
        assert session.request.call_count == 2


# ======================================================================
# apply_labels
# ======================================================================


class TestJiraProviderApplyLabels:
    """Tests for JiraProvider.apply_labels (multi-label, ProviderIssueResult)."""

    def test_apply_new_labels(self):
        session = _make_mock_session()
        get_response = _make_response(200, {"fields": {"labels": ["existing"]}})
        put_response = _make_response(204)
        session.request.side_effect = [get_response, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", ["new-label"], dry_run=False)
        assert isinstance(result, ProviderIssueResult)
        assert result.status == "updated"
        assert result.identifier == "PROJ-1"
        assert "new-label" in result.metadata["labels"]

    def test_apply_all_existing_returns_noop(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(200, {"fields": {"labels": ["bug"]}})

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", ["bug"], dry_run=False)
        assert result.status == "no-op"
        assert result.metadata["labels"] == ["bug"]

    def test_apply_empty_labels_returns_noop(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(200, {"fields": {"labels": ["existing"]}})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", [], dry_run=False)
        assert result.status == "no-op"
        assert result.metadata["labels"] == ["existing"]
        assert session.request.call_count == 1

    def test_apply_labels_dry_run(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", ["label1", "label2"], dry_run=True)
        assert result.status == "dry-run"
        # Dry-run preview reports only the requested labels; no HTTP request is made.
        assert result.metadata["labels"] == ["label1", "label2"]
        session.request.assert_not_called()

    def test_apply_labels_dry_run_deduplicates_metadata(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", ["label2", "label1", "label2"], dry_run=True)
        assert result.status == "dry-run"
        assert result.metadata["labels"] == ["label1", "label2"]
        session.request.assert_not_called()

    def test_apply_labels_dry_run_does_not_read_existing_labels(self):
        """Dry-run returns immediately without issuing a GET, even for a missing issue."""
        session = _make_mock_session()
        session.request.return_value = _make_response(404)
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-404", ["label1"], dry_run=True)
        assert result.status == "dry-run"
        assert result.metadata["labels"] == ["label1"]
        session.request.assert_not_called()

    def test_apply_labels_empty_identifier_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="identifier must be non-empty"):
            provider.apply_labels("", ["label1"], dry_run=False)
        session.request.assert_not_called()

    def test_apply_labels_whitespace_identifier_raises_before_dry_run(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="identifier must be non-empty"):
            provider.apply_labels("   ", ["label1"], dry_run=True)
        session.request.assert_not_called()

    def test_apply_labels_not_found_raises_valueerror(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(404)
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="not found"):
            provider.apply_labels("PROJ-404", ["label1"], dry_run=False)
        assert session.request.call_count == 1

    @pytest.mark.parametrize("labels_value", [None, "bug"])
    def test_apply_labels_coerces_non_list_labels_to_empty_list(self, labels_value):
        session = _make_mock_session()
        get_response = _make_response(200, {"fields": {"labels": labels_value}})
        put_response = _make_response(204)
        session.request.side_effect = [get_response, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", ["new-label"], dry_run=False)
        assert result.status == "updated"

    def test_apply_labels_uses_update_add_payload(self):
        session = _make_mock_session()
        get_response = _make_response(200, {"fields": {"labels": []}})
        put_response = _make_response(204)
        session.request.side_effect = [get_response, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        provider.apply_labels("PROJ-1", ["a", "b"], dry_run=False)

        put_call = session.request.call_args_list[1]
        payload = put_call.kwargs.get("json") or put_call[1].get("json")
        assert payload == {"update": {"labels": [{"add": "a"}, {"add": "b"}]}}

    def test_apply_labels_deduplicates_update_payload(self):
        session = _make_mock_session()
        get_response = _make_response(200, {"fields": {"labels": []}})
        put_response = _make_response(204)
        session.request.side_effect = [get_response, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", ["b", "a", "b"], dry_run=False)

        put_call = session.request.call_args_list[1]
        payload = put_call.kwargs.get("json") or put_call[1].get("json")
        assert payload == {"update": {"labels": [{"add": "b"}, {"add": "a"}]}}
        assert result.metadata["labels"] == ["a", "b"]

    def test_apply_labels_metadata_sorted(self):
        session = _make_mock_session()
        get_response = _make_response(200, {"fields": {"labels": ["z-label"]}})
        put_response = _make_response(204)
        session.request.side_effect = [get_response, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", ["a-label"], dry_run=False)
        assert result.metadata["labels"] == ["a-label", "z-label"]

    def test_apply_all_existing_multiple_labels_sorted(self):
        """Multiple existing labels returned sorted in metadata on no-op."""
        session = _make_mock_session()
        session.request.return_value = _make_response(200, {"fields": {"labels": ["zebra", "alpha"]}})

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", ["zebra", "alpha"], dry_run=False)
        assert result.status == "no-op"
        assert result.metadata["labels"] == ["alpha", "zebra"]

    def test_apply_labels_filters_empty_input_labels(self):
        """Empty and whitespace-only input labels are silently filtered out."""
        session = _make_mock_session()
        session.request.return_value = _make_response(200, {"fields": {"labels": ["existing"]}})

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", ["", "   "], dry_run=False)
        assert result.status == "no-op"
        assert result.metadata["labels"] == ["existing"]
        assert session.request.call_count == 1

    def test_apply_labels_strips_whitespace_input_labels(self):
        """Input labels with surrounding whitespace are stripped before use."""
        session = _make_mock_session()
        get_response = _make_response(200, {"fields": {"labels": []}})
        put_response = _make_response(204)
        session.request.side_effect = [get_response, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", ["  new-label  "], dry_run=False)
        assert result.status == "updated"
        assert result.metadata["labels"] == ["new-label"]
        put_call = session.request.call_args_list[1]
        payload = put_call.kwargs.get("json") or put_call[1].get("json")
        assert payload == {"update": {"labels": [{"add": "new-label"}]}}

    @pytest.mark.parametrize("bad_value", [42, None, True, ["nested"]])
    def test_apply_labels_filters_non_string_existing_labels(self, bad_value):
        """Non-string values in Jira's labels field are filtered out."""
        session = _make_mock_session()
        get_response = _make_response(200, {"fields": {"labels": [bad_value, "valid-label"]}})
        put_response = _make_response(204)
        session.request.side_effect = [get_response, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", ["new-label"], dry_run=False)
        assert result.status == "updated"
        assert "new-label" in result.metadata["labels"]
        assert "valid-label" in result.metadata["labels"]

    def test_apply_labels_strips_whitespace_identifier(self):
        """apply_labels strips surrounding whitespace from the identifier."""
        session = _make_mock_session()
        get_response = _make_response(200, {"fields": {"labels": []}})
        put_response = _make_response(204)
        session.request.side_effect = [get_response, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("  PROJ-1  ", ["label"], dry_run=False)
        assert result.status == "updated"
        assert result.identifier == "PROJ-1"
        get_url = session.request.call_args_list[0][0][1]
        assert "PROJ-1" in get_url
        assert "  " not in get_url

    def test_apply_labels_non_dict_json_raises_valueerror(self):
        """apply_labels raises ValueError when Jira returns a non-dict JSON payload."""
        session = _make_mock_session()
        session.request.return_value = _make_response(200, [{"unexpected": "list"}])
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Unexpected response type"):
            provider.apply_labels("PROJ-1", ["label"], dry_run=False)

    def test_apply_labels_fields_is_list_treats_existing_as_empty(self):
        """When Jira returns `fields` as a list (non-dict), existing labels default to [] and new labels are applied."""
        session = _make_mock_session()
        # GET returns a dict but with `fields` as a non-empty list — a truthy non-dict value.
        # Without the isinstance guard, data.get("fields", {}).get("labels") would raise AttributeError.
        get_response = _make_response(200, {"fields": ["unexpected", "list"]})
        put_response = _make_response(204)
        session.request.side_effect = [get_response, put_response]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.apply_labels("PROJ-1", ["new-label"], dry_run=False)
        assert result.status == "updated"
        assert session.request.call_count == 2

    def test_apply_labels_strips_whitespace_from_existing_labels(self):
        """apply_labels strips surrounding whitespace from existing Jira labels before comparison."""
        session = _make_mock_session()
        # Jira returns " existing-label " with surrounding whitespace
        get_response = _make_response(200, {"fields": {"labels": [" existing-label "]}})
        session.request.return_value = get_response

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        # Requesting the same label without whitespace — should be a no-op after stripping
        result = provider.apply_labels("PROJ-1", ["existing-label"], dry_run=False)
        assert result.status == "no-op"
        # Only one GET call — no PUT was issued
        assert session.request.call_count == 1


# ======================================================================
# resolve_identifier
# ======================================================================


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


# ======================================================================
# link_subissue
# ======================================================================


class TestJiraProviderLinkSubissue:
    """Tests for JiraProvider.link_subissue."""

    def test_link_empty_parent_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="parent_id must be non-empty"):
            provider.link_subissue("", "PROJ-2", dry_run=False)
        session.request.assert_not_called()

    def test_link_empty_child_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="child_id must be non-empty"):
            provider.link_subissue("PROJ-1", "   ", dry_run=False)
        session.request.assert_not_called()

    def test_link_via_epic_link(self):
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        put_response = _make_response(204)
        session.request.side_effect = [field_response, get_no_parent, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert result.status == "linked"
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"

    def test_link_dry_run(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=True)
        assert result.status == "dry-run"
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"
        session.request.assert_not_called()

    def test_link_falls_back_to_parent_for_inapplicable_field(self):
        """link_subissue falls back to parent field when epic-link field is not applicable."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        epic_fail = _make_response(400, text='{"errors":{"customfield_10008":"Field not on the appropriate screen"}}')
        parent_response = _make_response(204)
        session.request.side_effect = [field_response, get_no_parent, epic_fail, parent_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert result.status == "linked"
        # Verify the fallback PUT used the correct parent payload
        fallback_call = session.request.call_args_list[3]
        fallback_payload = fallback_call.kwargs.get("json") or fallback_call[1].get("json")
        assert fallback_payload == {"fields": {"parent": {"key": "PROJ-1"}}}

    @pytest.mark.parametrize(
        "indicator_phrase",
        [
            "not applicable",
            "cannot be set",
            "does not exist",
        ],
    )
    def test_link_falls_back_for_other_inapplicable_indicators(self, indicator_phrase):
        """link_subissue falls back to parent for all recognised indicators."""
        session = _make_mock_session()
        field_response = _make_response(
            200,
            [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}],
        )
        get_no_parent = _make_response(200, {"fields": {}})
        epic_fail = _make_response(
            400,
            text=f'{{"errors":{{"customfield_10008":"Field {indicator_phrase}"}}}}',
        )
        parent_response = _make_response(204)
        session.request.side_effect = [field_response, get_no_parent, epic_fail, parent_response]

        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=session,
        )
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert result.status == "linked"

    def test_link_raises_on_non_inapplicable_400(self):
        """link_subissue surfaces non-field-inapplicable 400 errors."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        epic_fail = _make_response(400, text='{"errors":{"permission":"You do not have permission"}}')
        # find_existing_link: field_response + get_no_parent (returns None)
        # link_subissue: epic_fail on PUT
        session.request.side_effect = [field_response, get_no_parent, epic_fail]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(Exception, match="HTTP 400"):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)

    def test_link_does_not_fallback_for_does_not_exist_error_on_other_field(self):
        """Fallback is skipped when the indicator is not tied to the epic-link field."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        epic_fail = _make_response(400, text='{"errors":{"summary":"Issue does not exist"}}')
        session.request.side_effect = [field_response, get_no_parent, epic_fail]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(Exception, match="HTTP 400"):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert session.request.call_count == 3

    def test_link_not_found_raises_valueerror(self):
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        not_found = _make_response(404)
        # find_existing_link returns None on 404, then PUT also gets 404
        session.request.side_effect = [field_response, not_found, not_found]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="not found"):
            provider.link_subissue("PROJ-1", "PROJ-404", dry_run=False)
        assert session.request.call_count == 3

    def test_link_fallback_not_found_raises_valueerror(self):
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        epic_fail = _make_response(400, text='{"errors":{"customfield_10008":"Field not applicable"}}')
        fallback_not_found = _make_response(404)
        session.request.side_effect = [field_response, get_no_parent, epic_fail, fallback_not_found]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="not found"):
            provider.link_subissue("PROJ-1", "PROJ-404", dry_run=False)
        assert session.request.call_count == 4

    def test_link_raises_on_non_validation_error(self):
        """link_subissue surfaces non-validation epic-link failures."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        epic_fail = _make_response(401)
        session.request.side_effect = [field_response, get_no_parent, epic_fail]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(Exception):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert session.request.call_count == 3

    def test_link_strips_whitespace_dry_run(self):
        """link_subissue strips surrounding whitespace from parent_id and child_id in dry-run."""
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("  PROJ-1  ", "  PROJ-2  ", dry_run=True)
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"
        session.request.assert_not_called()

    def test_link_strips_whitespace_live(self):
        """link_subissue strips surrounding whitespace before constructing the API URL."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        put_response = _make_response(204)
        session.request.side_effect = [field_response, get_no_parent, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("  PROJ-1  ", "  PROJ-2  ", dry_run=False)
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"
        # Verify the PUT URL used the stripped child_id
        put_call = session.request.call_args_list[2]
        put_url = put_call[0][1] if put_call[0] else put_call.kwargs.get("url", "")
        assert "PROJ-2" in put_url
        assert "  " not in put_url

    def test_link_already_linked_via_epic_field(self):
        """link_subissue returns already-linked when epic-link field already points to parent."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_linked = _make_response(200, {"fields": {"customfield_10008": "PROJ-1"}})
        session.request.side_effect = [field_response, get_linked]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert result.status == "already-linked"
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"
        assert session.request.call_count == 2

    def test_link_already_linked_via_parent_field(self):
        """link_subissue returns already-linked when parent field already set to parent_id."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_linked = _make_response(
            200,
            {"fields": {"customfield_10008": None, "parent": {"key": "PROJ-1", "id": "10001"}}},
        )
        session.request.side_effect = [field_response, get_linked]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert result.status == "already-linked"
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"
        assert session.request.call_count == 2

    def test_link_get_returns_non_dict_raises(self):
        """When GET response is non-dict, find_existing_link raises ValueError instead of proceeding."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        # GET returns a list instead of a dict (unexpected API shape).
        get_non_dict = _make_response(200, ["unexpected-list-response"])
        session.request.side_effect = [field_response, get_non_dict]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="find_existing_link: expected a JSON object from Jira"):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)

    def test_link_get_fields_is_list_proceeds_to_put(self):
        """When GET response has `fields` as a list (non-dict), idempotency check is skipped."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        # GET returns a dict but with `fields` as a non-empty list — a truthy non-dict value.
        # Without an isinstance guard, `get_data.get("fields") or {}` would keep the list
        # and the subsequent `.get()` call would raise AttributeError.
        get_fields_list = _make_response(200, {"fields": ["unexpected", "list"]})
        put_response = _make_response(204)
        session.request.side_effect = [field_response, get_fields_list, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert result.status == "linked"
        assert session.request.call_count == 3

    def test_link_put_returns_404_after_get_success_raises_valueerror(self):
        """When PUT returns 404 (issue deleted after GET), a ValueError is raised."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        put_not_found = _make_response(404)
        session.request.side_effect = [field_response, get_no_parent, put_not_found]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="not found"):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert session.request.call_count == 3


# ======================================================================
# add_blocked_by
# ======================================================================


class TestJiraProviderAddBlockedBy:
    """Tests for JiraProvider.add_blocked_by."""

    def test_add_blocked_by_success(self):
        session = _make_mock_session()
        get_resp = _make_response(200, {"fields": {"issuelinks": []}})
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"

    def test_add_blocked_by_dry_run(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=True)
        assert result.status == "dry-run"
        session.request.assert_not_called()

    def test_add_blocked_by_payload_direction(self):
        """Verifies POST payload has outwardIssue=blocked_by_id and inwardIssue=issue_id."""
        session = _make_mock_session()
        get_resp = _make_response(200, {"fields": {"issuelinks": []}})
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)

        # call_args is the last call (the POST)
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["outwardIssue"]["key"] == "PROJ-1"
        assert payload["inwardIssue"]["key"] == "PROJ-2"

    def test_add_blocked_by_already_linked_via_outward(self):
        """Returns already-linked when blocked_by_id appears as outwardIssue in existing links."""
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    {
                        "type": {"name": "Blocks"},
                        "outwardIssue": {"key": "PROJ-1"},
                    }
                ]
            }
        }
        session.request.return_value = _make_response(200, existing)
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "already-linked"
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"
        # Only the GET was made — no POST
        assert session.request.call_count == 1

    def test_add_blocked_by_inward_issue_is_opposite_direction_not_idempotent(self):
        """inwardIssue=blocked_by_id represents the opposite edge (issue_id blocks blocked_by_id).

        This is NOT the same as "issue_id is blocked by blocked_by_id", so the method
        must NOT return already-linked and must proceed to POST the new link.
        """
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    {
                        "type": {"name": "Blocks"},
                        "inwardIssue": {"key": "PROJ-1"},
                    }
                ]
            }
        }
        get_resp = _make_response(200, existing)
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        # The existing link is the wrong direction — a new link must be created
        assert result.status == "linked"
        # Both GET and POST were made
        assert session.request.call_count == 2

    def test_add_blocked_by_different_blocker_not_idempotent(self):
        """A different blocker in existing links does not trigger already-linked."""
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    {
                        "type": {"name": "Blocks"},
                        "outwardIssue": {"key": "PROJ-99"},
                    }
                ]
            }
        }
        get_resp = _make_response(200, existing)
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"

    def test_add_blocked_by_empty_issue_id_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="issue_id must be a non-empty string"):
            provider.add_blocked_by("", "PROJ-1", dry_run=False)

    def test_add_blocked_by_empty_blocked_by_id_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="blocked_by_id must be a non-empty string"):
            provider.add_blocked_by("PROJ-2", "", dry_run=False)

    def test_add_blocked_by_self_blocking_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Self-blocking is not allowed"):
            provider.add_blocked_by("PROJ-1", "PROJ-1", dry_run=False)

    def test_add_blocked_by_self_blocking_raises_in_dry_run(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Self-blocking is not allowed"):
            provider.add_blocked_by("PROJ-1", "PROJ-1", dry_run=True)
        session.request.assert_not_called()

    def test_add_blocked_by_self_blocking_detected_after_strip(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Self-blocking is not allowed"):
            provider.add_blocked_by("  PROJ-1", "PROJ-1  ", dry_run=False)
        session.request.assert_not_called()

    def test_add_blocked_by_issue_id_not_found_raises_valueerror(self):
        """GET 404 on issue_id during dependency check proceeds to POST which also 404s."""
        session = _make_mock_session()
        session.request.return_value = _make_response(404, text='{"errorMessages":["Issue does not exist"]}')
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(
            ValueError,
            match=r"issue_id='PROJ-2'.*blocked_by_id='PROJ-404'",
        ):
            provider.add_blocked_by("PROJ-2", "PROJ-404", dry_run=False)

    def test_add_blocked_by_post_not_found_raises_valueerror(self):
        """POST 404 raises ValueError that includes issue_id and blocked_by_id in the message."""
        session = _make_mock_session()
        get_resp = _make_response(200, {"fields": {"issuelinks": []}})
        post_resp = _make_response(404, text='{"errorMessages":["Issue does not exist"]}')
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(
            ValueError,
            match=r"issue_id='PROJ-2'.*blocked_by_id='PROJ-404'.*Issue does not exist",
        ):
            provider.add_blocked_by("PROJ-2", "PROJ-404", dry_run=False)

    def test_add_blocked_by_non_dict_link_entry_skipped(self):
        """Non-dict entries in issuelinks are skipped without error."""
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    "not-a-dict",
                    {"type": {"name": "Blocks"}, "outwardIssue": {"key": "PROJ-1"}},
                ]
            }
        }
        session.request.return_value = _make_response(200, existing)
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "already-linked"

    def test_add_blocked_by_non_dict_link_type_skipped(self):
        """Links with a non-dict type field are skipped without error."""
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    {"type": "Blocks", "outwardIssue": {"key": "PROJ-1"}},
                ]
            }
        }
        get_resp = _make_response(200, existing)
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        # The malformed link is skipped; a new link is created
        assert result.status == "linked"

    def test_add_blocked_by_non_blocks_link_type_not_idempotent(self):
        """A different link type (e.g. Relates) is not treated as already-linked."""
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    {"type": {"name": "Relates"}, "outwardIssue": {"key": "PROJ-1"}},
                ]
            }
        }
        get_resp = _make_response(200, existing)
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"

    def test_add_blocked_by_issuelinks_none_proceeds_to_post(self):
        """issuelinks=None in Jira response is treated as empty list; POST proceeds safely."""
        session = _make_mock_session()
        existing = {"fields": {"issuelinks": None}}
        get_resp = _make_response(200, existing)
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["outwardIssue"]["key"] == "PROJ-1"
        assert payload["inwardIssue"]["key"] == "PROJ-2"

    def test_add_blocked_by_type_name_none_skipped(self):
        """Link with type.name=None is skipped without AttributeError; POST proceeds safely."""
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    {"type": {"name": None}, "outwardIssue": {"key": "PROJ-1"}},
                ]
            }
        }
        get_resp = _make_response(200, existing)
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"

    def test_add_blocked_by_get_returns_non_dict_raises(self):
        """When GET response is a non-dict (e.g. list), find_existing_dependency raises ValueError."""
        session = _make_mock_session()
        # GET returns a list instead of a dict (unexpected API shape).
        get_non_dict = _make_response(200, ["unexpected-list-response"])
        session.request.return_value = get_non_dict
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="find_existing_dependency: expected a JSON object from Jira"):
            provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)

    def test_add_blocked_by_get_fields_is_list_proceeds_to_post(self):
        """When GET response has `fields` as a list (non-dict), idempotency check is skipped and POST proceeds."""
        session = _make_mock_session()
        # GET returns a dict but with `fields` as a non-empty list — a truthy non-dict value.
        # Without the isinstance guard, fields.get("issuelinks") would raise AttributeError.
        get_fields_list = _make_response(200, {"fields": ["unexpected", "list"]})
        post_resp = _make_response(201)
        session.request.side_effect = [get_fields_list, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"
        assert session.request.call_count == 2

    def test_add_blocked_by_outward_issue_non_dict_skipped(self):
        """outwardIssue present but non-dict (e.g. string/list) does not raise and proceeds to POST."""
        session = _make_mock_session()
        # outwardIssue is a string — truthy, but not a dict. Without isinstance guard
        # the `or {}` default is skipped and .get("key") raises AttributeError.
        get_resp = _make_response(
            200,
            {
                "fields": {
                    "issuelinks": [
                        {
                            "type": {"name": "Blocks"},
                            "outwardIssue": "PROJ-1",  # string, not a dict
                        }
                    ]
                }
            },
        )
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"
        assert session.request.call_count == 2


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


# ======================================================================
# Protocol conformance
# ======================================================================


def _assert_jira_provider_conforms(p: IssueProvider) -> None:
    """Typed helper for mypy static verification of protocol conformance."""


class TestJiraProviderProtocolConformance:
    """Tests for IssueProvider protocol conformance."""

    def test_isinstance_issue_provider(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert isinstance(provider, IssueProvider)

    def test_mypy_conformance(self):
        """Static type check: JiraProvider satisfies IssueProvider."""
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        _assert_jira_provider_conforms(provider)


# ======================================================================
# Epic hierarchy flow
# ======================================================================


class TestJiraEpicHierarchyFlow:
    """End-to-end flow tests for epic hierarchy creation."""

    def test_create_epic_with_children(self):
        """Create 1 epic + 5 children with correct parent linking."""
        session = _make_mock_session()
        issue_counter = {"n": 0}

        def mock_request(method, url, **kwargs):
            if "/field" in url:
                return _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
            if method == "POST" and "/issue" in url:
                issue_counter["n"] += 1
                return _make_response(201, {"key": f"PROJ-{issue_counter['n']}", "id": str(10000 + issue_counter["n"])})
            if method == "PUT":
                return _make_response(204)
            return _make_response(200)

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        parent_result = provider.create_issue("Epic Title", "Epic body", "epic", dry_run=False)
        assert parent_result.status == "created"
        parent_key = parent_result.identifier

        children = []
        for i in range(5):
            result = provider.create_issue(f"Feature {i}", f"Body {i}", "feature", parent_id=parent_key, dry_run=False)
            assert result.status == "created"
            children.append(result)

        assert len(children) == 5

    def test_epic_feature_subtask_hierarchy(self):
        """Create epic → feature (parent_id=epic) → subtask (parent_id=feature)."""
        session = _make_mock_session()
        issue_counter = {"n": 0}

        def mock_request(method, url, **kwargs):
            if "/field" in url:
                return _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
            if method == "POST" and "/issue" in url:
                issue_counter["n"] += 1
                return _make_response(201, {"key": f"PROJ-{issue_counter['n']}", "id": str(10000 + issue_counter["n"])})
            return _make_response(200)

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        epic = provider.create_issue("Epic", "Body", "epic", dry_run=False)
        feature = provider.create_issue("Feature", "Body", "feature", parent_id=epic.identifier, dry_run=False)
        subtask = provider.create_issue("Subtask", "Body", "subtask", parent_id=feature.identifier, dry_run=False)

        assert epic.status == "created"
        assert feature.status == "created"
        assert subtask.status == "created"

        # Verify subtask has parent field set
        subtask_call = session.request.call_args_list[-1]
        subtask_payload = subtask_call.kwargs.get("json") or subtask_call[1].get("json")
        assert subtask_payload["fields"]["parent"] == {"key": feature.identifier}

    def test_blocking_dependencies(self):
        """Wire blocking dependencies between Jira issues."""
        session = _make_mock_session()
        issue_counter = {"n": 0}

        def mock_request(method, url, **kwargs):
            if method == "POST" and "/issue" in url and "Link" not in url:
                issue_counter["n"] += 1
                return _make_response(201, {"key": f"PROJ-{issue_counter['n']}", "id": str(10000 + issue_counter["n"])})
            if method == "POST" and "issueLink" in url:
                return _make_response(201)
            return _make_response(200)

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        issues = []
        for i in range(3):
            result = provider.create_issue(f"Task {i}", f"Body {i}", "task", dry_run=False)
            issues.append(result)

        dep1 = provider.add_blocked_by(issues[1].identifier, issues[0].identifier, dry_run=False)
        assert dep1.status == "linked"
        dep2 = provider.add_blocked_by(issues[2].identifier, issues[1].identifier, dry_run=False)
        assert dep2.status == "linked"


# ======================================================================
# Dry-run manifest
# ======================================================================


class TestJiraProviderDryRunManifest:
    """Tests for dry-run manifest accumulation."""

    def test_dry_run_accumulates_issues(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        provider.create_issue("Title 1", "Body", "epic", dry_run=True)
        provider.create_issue("Title 2", "Body", "feature", dry_run=True)
        manifest = provider.get_dry_run_manifest()
        assert len(manifest["issues"]) == 2

    def test_dry_run_accumulates_dependencies(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        provider.link_subissue("PROJ-1", "PROJ-2", dry_run=True)
        provider.add_blocked_by("PROJ-3", "PROJ-4", dry_run=True)
        manifest = provider.get_dry_run_manifest()
        assert len(manifest["dependencies"]) == 2

    def test_dry_run_manifest_full_flow(self):
        """10 issues + 8 dependencies all marked dry-run."""
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        for i in range(10):
            result = provider.create_issue(f"Issue {i}", f"Body {i}", "task", dry_run=True)
            assert result.status == "dry-run"

        for i in range(8):
            result = provider.add_blocked_by(f"PROJ-{i + 1}", f"PROJ-{i}", dry_run=True)
            assert result.status == "dry-run"

        manifest = provider.get_dry_run_manifest()
        assert len(manifest["issues"]) == 10
        assert len(manifest["dependencies"]) == 8
        session.request.assert_not_called()


# ======================================================================
# Idempotent rerun flow
# ======================================================================


class TestJiraIdempotentRerunFlow:
    """Verify idempotent re-run creates 0 duplicates for Jira provider."""

    def test_jira_rerun_finds_existing(self):
        orch_key = generate_orchestration_key("create_issue", "epic.features[0]")
        session = _make_mock_session()

        def mock_request(method, url, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            resp.text = "{}"
            resp.raise_for_status = MagicMock()
            if "/search" in url:
                resp.json.return_value = {"issues": [{"key": "PROJ-99", "id": "10099"}]}
            else:
                resp.json.return_value = {}
            return resp

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        body = embed_orchestration_key("Body", orch_key)

        result = provider.create_issue("Title", body, "task", dry_run=False)
        assert result.status == "existing"
        assert result.identifier == "PROJ-99"


# ======================================================================
# Helpers / Session
# ======================================================================


class TestJiraProviderHelpers:
    """Tests for internal helper methods and session construction."""

    def test_api_url(self):
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert provider._api_url("/issue") == "https://jira.example.com/rest/api/2/issue"

    def test_request_transient_error(self):
        session = _make_mock_session()
        resp = _make_response(429)
        session.request.return_value = resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(TransientError, match="429"):
            provider._request("GET", "https://jira.example.com/test")

    def test_request_sets_default_timeout(self):
        session = _make_mock_session()
        session.request.return_value = _make_response(200)
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        provider._request("GET", "https://jira.example.com/test")
        assert session.request.call_args.kwargs["timeout"] == 30

    def test_is_field_inapplicable_error_from_field_errors_map(self):
        response = _make_response(400, {"errors": {"customfield_10008": "Field not applicable"}})
        assert JiraProvider._is_field_inapplicable_error(response, "customfield_10008")

    def test_is_field_inapplicable_error_from_error_messages(self):
        # Includes a non-string entry to verify the type-guard skips invalid items.
        response = _make_response(
            400,
            {"errorMessages": [123, "customfield_10008 cannot be set in this context"]},
        )
        assert JiraProvider._is_field_inapplicable_error(response, "customfield_10008")

    def test_is_field_inapplicable_error_error_messages_falls_back_to_text(self):
        response = _make_response(
            400,
            {"errorMessages": ["some other validation error"]},
            text="customfield_10008 not applicable",
        )
        assert JiraProvider._is_field_inapplicable_error(response, "customfield_10008")

    def test_is_field_inapplicable_error_scans_multiple_error_messages(self):
        response = _make_response(
            400,
            {
                "errorMessages": [
                    "first message without target field",
                    "customfield_10008 cannot be set in this context",
                ]
            },
        )
        assert JiraProvider._is_field_inapplicable_error(response, "customfield_10008")

    def test_is_field_inapplicable_error_ignores_non_string_field_error_value(self):
        response = _make_response(
            400,
            {
                "errors": {"customfield_10008": {"detail": "not a string"}},
                "errorMessages": ["customfield_10008 cannot be set in this context"],
            },
        )
        assert JiraProvider._is_field_inapplicable_error(response, "customfield_10008")

    def test_is_field_inapplicable_error_from_text_when_json_invalid(self):
        response = MagicMock()
        response.json.side_effect = ValueError("invalid json")
        response.text = "customfield_10008 does not exist"
        assert JiraProvider._is_field_inapplicable_error(response, "customfield_10008")

    def test_get_epic_link_field_cached(self):
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        session.request.return_value = field_response
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        first = provider._get_epic_link_field()
        second = provider._get_epic_link_field()
        assert first == second == "customfield_10008"
        assert session.request.call_count == 1

    def test_get_epic_link_field_fallback(self):
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_99999", "name": "Other Field", "schema": {}}])
        session.request.return_value = field_response
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider._get_epic_link_field()
        assert result == "customfield_10008"

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

    def test_find_existing_link_non_dict_response_raises(self):
        """find_existing_link raises ValueError when Jira returns a non-dict payload."""
        session = _make_mock_session()
        # field discovery
        field_resp = _make_response(
            200,
            [
                {
                    "id": "customfield_10014",
                    "name": "Epic Link",
                    "schema": {"custom": "com.pyxis.greenhopper.jira:gh-epic-link"},
                }
            ],
        )
        # issue GET returns a list instead of a dict
        issue_resp = MagicMock()
        issue_resp.status_code = 200
        issue_resp.raise_for_status = MagicMock()
        issue_resp.json.return_value = ["unexpected", "list"]
        session.request.side_effect = [field_resp, issue_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="find_existing_link: expected a JSON object from Jira"):
            provider.find_existing_link("PROJ-1", "PROJ-2")

    def test_find_existing_dependency_non_dict_response_raises(self):
        """find_existing_dependency raises ValueError when Jira returns a non-dict payload."""
        session = _make_mock_session()
        # issue GET returns a list instead of a dict
        issue_resp = MagicMock()
        issue_resp.status_code = 200
        issue_resp.raise_for_status = MagicMock()
        issue_resp.json.return_value = ["unexpected", "list"]
        session.request.return_value = issue_resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="find_existing_dependency: expected a JSON object from Jira"):
            provider.find_existing_dependency("PROJ-1", "PROJ-2")

    def test_find_existing_dependency_non_list_issuelinks_raises(self):
        """find_existing_dependency raises ValueError when fields.issuelinks is not a list."""
        session = _make_mock_session()
        issue_resp = MagicMock()
        issue_resp.status_code = 200
        issue_resp.raise_for_status = MagicMock()
        issue_resp.json.return_value = {"fields": {"issuelinks": {"unexpected": "shape"}}}
        session.request.return_value = issue_resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(
            ValueError,
            match=r"find_existing_dependency: expected fields\.issuelinks to be a list when present, got dict",
        ):
            provider.find_existing_dependency("PROJ-1", "PROJ-2")

    def test_build_session_bearer_auth(self):
        env = {
            "JIRA_API_TOKEN": "my-token",
            "JIRA_USER_EMAIL": "",
            "JIRA_EMAIL": "",
            "JIRA_USERNAME": "",
            "JIRA_AUTH_SCHEME": "bearer",
            "JIRA_SSL_VERIFY": "",
            "JIRA_CA_BUNDLE": "",
            "REQUESTS_CA_BUNDLE": "",
            "JIRA_BASE_URL": "https://jira.example.com",
        }
        with patch.dict(os.environ, env, clear=False):
            provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com")
        assert "Bearer" in provider._session.headers.get("Authorization", "")

    def test_build_session_identity_takes_precedence_over_bearer_scheme(self):
        env = {
            "JIRA_API_TOKEN": "my-token",
            "JIRA_USER_EMAIL": "user@example.com",
            "JIRA_EMAIL": "",
            "JIRA_USERNAME": "",
            "JIRA_AUTH_SCHEME": "bearer",
            "JIRA_SSL_VERIFY": "",
            "JIRA_CA_BUNDLE": "",
            "REQUESTS_CA_BUNDLE": "",
            "JIRA_BASE_URL": "https://jira.example.com",
        }
        with patch.dict(os.environ, env, clear=False):
            provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com")
        auth_header = provider._session.headers.get("Authorization", "")
        assert auth_header.startswith("Basic ")
        assert "Bearer" not in auth_header

    def test_build_session_basic_auth(self):
        env = {
            "JIRA_API_TOKEN": "my-token",
            "JIRA_USER_EMAIL": "user@example.com",
            "JIRA_EMAIL": "",
            "JIRA_USERNAME": "",
            "JIRA_AUTH_SCHEME": "basic",
            "JIRA_SSL_VERIFY": "",
            "JIRA_CA_BUNDLE": "",
            "REQUESTS_CA_BUNDLE": "",
            "JIRA_BASE_URL": "https://jira.example.com",
        }
        with patch.dict(os.environ, env, clear=False):
            provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com")
        assert "Basic" in provider._session.headers.get("Authorization", "")

    def test_build_session_ssl_verify_disabled(self):
        env = {
            "JIRA_API_TOKEN": "tok",
            "JIRA_USER_EMAIL": "",
            "JIRA_EMAIL": "",
            "JIRA_USERNAME": "",
            "JIRA_AUTH_SCHEME": "bearer",
            "JIRA_SSL_VERIFY": "0",
            "JIRA_CA_BUNDLE": "",
            "REQUESTS_CA_BUNDLE": "",
            "JIRA_BASE_URL": "https://jira.example.com",
        }
        with patch.dict(os.environ, env, clear=False):
            provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com")
        assert provider._session.verify is False

    def test_build_session_ssl_verify_custom_path(self):
        env = {
            "JIRA_API_TOKEN": "tok",
            "JIRA_USER_EMAIL": "",
            "JIRA_EMAIL": "",
            "JIRA_USERNAME": "",
            "JIRA_AUTH_SCHEME": "bearer",
            "JIRA_SSL_VERIFY": "/path/to/cert.pem",
            "JIRA_CA_BUNDLE": "",
            "REQUESTS_CA_BUNDLE": "",
            "JIRA_BASE_URL": "https://jira.example.com",
        }
        with patch.dict(os.environ, env, clear=False):
            provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com")
        assert provider._session.verify == "/path/to/cert.pem"

    def test_build_session_ca_bundle_env(self):
        env = {
            "JIRA_API_TOKEN": "tok",
            "JIRA_USER_EMAIL": "",
            "JIRA_EMAIL": "",
            "JIRA_USERNAME": "",
            "JIRA_AUTH_SCHEME": "bearer",
            "JIRA_SSL_VERIFY": "",
            "JIRA_CA_BUNDLE": "/custom/ca.pem",
            "REQUESTS_CA_BUNDLE": "",
            "JIRA_BASE_URL": "https://jira.example.com",
        }
        with patch.dict(os.environ, env, clear=False):
            provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com")
        assert provider._session.verify == "/custom/ca.pem"

    def test_build_session_no_token_no_auth(self):
        env = {
            "JIRA_API_TOKEN": "",
            "JIRA_COPILOT_PAT": "",
            "JIRA_USER_EMAIL": "",
            "JIRA_EMAIL": "",
            "JIRA_USERNAME": "",
            "JIRA_AUTH_SCHEME": "bearer",
            "JIRA_SSL_VERIFY": "",
            "JIRA_CA_BUNDLE": "",
            "REQUESTS_CA_BUNDLE": "",
            "JIRA_BASE_URL": "https://jira.example.com",
        }
        with patch.dict(os.environ, env, clear=False):
            provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com")
        assert "Authorization" not in provider._session.headers

    def test_build_session_identity_without_token_no_auth(self):
        env = {
            "JIRA_API_TOKEN": "",
            "JIRA_COPILOT_PAT": "",
            "JIRA_USER_EMAIL": "user@example.com",
            "JIRA_EMAIL": "",
            "JIRA_USERNAME": "",
            "JIRA_AUTH_SCHEME": "basic",
            "JIRA_SSL_VERIFY": "",
            "JIRA_CA_BUNDLE": "",
            "REQUESTS_CA_BUNDLE": "",
            "JIRA_BASE_URL": "https://jira.example.com",
        }
        with patch.dict(os.environ, env, clear=False):
            provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com")
        assert "Authorization" not in provider._session.headers

    def test_session_injection(self):
        """Injected session is used for requests."""
        session = _make_mock_session()
        session.request.return_value = _make_response(200, {"key": "PROJ-1", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        provider.resolve_identifier("PROJ-1", dry_run=False)
        session.request.assert_called_once()

    def test_get_epic_link_field_transient_error_raises(self):
        """_get_epic_link_field raises TransientError on 429/502/503."""
        session = _make_mock_session()
        resp = _make_response(429)
        session.request.return_value = resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(TransientError, match="429"):
            provider._get_epic_link_field()


# ======================================================================
# Provider-specific gap tests (T016-T019, T024)
# ======================================================================

_SLEEP = "agentic_devtools.adapters.retry.time.sleep"


class TestJiraProviderContractGaps:
    """Jira-specific gap tests complementing the shared contract suite."""

    def test_init_accepts_valid_project_key_and_base_url(self):
        """__init__ accepts a valid project key and base URL (T024)."""
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert provider.project_key == "PROJ"
        assert provider._base_url == "https://jira.example.com"

    def test_create_issue_happy_path_posts_to_issue_endpoint_with_payload(self):
        """create_issue POSTs to /rest/api/2/issue with the expected fields (T016)."""
        session = _make_mock_session()
        session.request.return_value = _make_response(201, {"key": "PROJ-1", "id": "10001"})
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        result = provider.create_issue("My Title", "My Body", "task", dry_run=False)

        assert result.status == "created"
        assert result.identifier == "PROJ-1"
        method, url = session.request.call_args.args[0], session.request.call_args.args[1]
        assert method == "POST"
        assert url == "https://jira.example.com/rest/api/2/issue"
        fields = session.request.call_args.kwargs["json"]["fields"]
        assert fields["project"] == {"key": "PROJ"}
        assert fields["summary"] == "My Title"
        assert fields["issuetype"] == {"name": "Task"}

    def test_create_issue_http_422_raises_via_raise_for_status(self):
        """create_issue surfaces a non-transient HTTP 422 via raise_for_status (T016)."""
        session = _make_mock_session()
        session.request.return_value = _make_response(422, text="Unprocessable")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        with pytest.raises(Exception, match="HTTP 422"):
            provider.create_issue("Title", "Body", "task", dry_run=False)

    def test_create_issue_retry_exhaustion_on_429(self, monkeypatch):
        """create_issue retries transient 429 and raises after 4 total attempts (T017)."""
        monkeypatch.setattr(_SLEEP, lambda *a, **k: None)
        session = _make_mock_session()
        session.request.return_value = _make_response(429, text="rate limited")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        with pytest.raises(TransientError):
            provider.create_issue("Title", "Body", "task", dry_run=False)
        assert session.request.call_count == 4

    def test_link_subissue_transient_502_raises(self, monkeypatch):
        """link_subissue raises TransientError on a transient 502 (T018)."""
        monkeypatch.setattr(_SLEEP, lambda *a, **k: None)
        session = _make_mock_session()
        session.request.return_value = _make_response(502, text="bad gateway")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        with pytest.raises(TransientError, match="502"):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)

    def test_link_subissue_transient_503_raises(self, monkeypatch):
        """link_subissue raises TransientError on a transient 503 (T018)."""
        monkeypatch.setattr(_SLEEP, lambda *a, **k: None)
        session = _make_mock_session()
        session.request.return_value = _make_response(503, text="unavailable")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        with pytest.raises(TransientError, match="503"):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)

    def test_add_blocked_by_transient_502_raises(self, monkeypatch):
        """add_blocked_by raises TransientError on a transient 502 (T019)."""
        monkeypatch.setattr(_SLEEP, lambda *a, **k: None)
        session = _make_mock_session()
        session.request.return_value = _make_response(502, text="bad gateway")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        with pytest.raises(TransientError, match="502"):
            provider.add_blocked_by("PROJ-1", "PROJ-2", dry_run=False)

    def test_add_blocked_by_transient_503_raises(self, monkeypatch):
        """add_blocked_by raises TransientError on a transient 503 (T019)."""
        monkeypatch.setattr(_SLEEP, lambda *a, **k: None)
        session = _make_mock_session()
        session.request.return_value = _make_response(503, text="unavailable")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        with pytest.raises(TransientError, match="503"):
            provider.add_blocked_by("PROJ-1", "PROJ-2", dry_run=False)


# ======================================================================
# Shared provider-contract scenarios wired to JiraProvider
# ======================================================================

from tests.unit.adapters.conftest import build_jira_contract_provider  # noqa: E402
from tests.unit.adapters.issue_provider import _contract_scenarios as contract  # noqa: E402


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


class TestJiraCreationFailurePropagation:
    """Jira creation failures propagate the ordinary adapter exception (FR-007).

    Jira embeds ``parent``/epic-link in the creation POST and has no separate
    post-create link stage, so no ``HierarchyLinkError`` wrapping is applied —
    a failed create with a parent surfaces the ordinary creation exception.
    """

    def test_create_issue_with_parent_failure_does_not_wrap_in_hierarchy_link_error(self):
        from agentic_devtools.adapters.exceptions import HierarchyLinkError

        session = _make_mock_session()
        session.request.return_value = _make_response(400, text="bad request")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(Exception) as exc_info:
            provider.create_issue("Sub", "Body", "subtask", parent_id="PROJ-1", dry_run=False)
        assert not isinstance(exc_info.value, HierarchyLinkError)

"""Tests for the JiraProvider creation capability."""

from __future__ import annotations

import hashlib
from typing import cast

import pytest

from agentic_devtools.adapters.exceptions import HierarchyLinkError
from agentic_devtools.adapters.issue_provider import (
    DefinitiveCreationFailure,
    ProviderIssueResult,
)
from agentic_devtools.adapters.jira_provider import JiraProvider
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response

_SLEEP = "agentic_devtools.adapters.retry.time.sleep"


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
        with pytest.raises(DefinitiveCreationFailure, match="Unsupported issue type"):
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
        assert result.hierarchy_link_result is not None
        assert result.hierarchy_link_result.source_id == "PROJ-1"
        assert result.hierarchy_link_result.target_id == "PROJ-5"
        assert result.hierarchy_link_result.status == "linked"
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

    def test_create_issue_finds_legacy_raw_orchestration_key(self):
        key = "legacy-key"
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        session = _make_mock_session()
        session.request.side_effect = [
            _make_response(200, {"issues": []}),
            _make_response(200, {"issues": [{"key": "PROJ-10", "id": "10010"}]}),
        ]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        result = provider.create_issue("Title", "Body", "task", idempotency_key=key)

        assert result.status == "existing"
        assert result.identifier == "PROJ-10"
        first_jql = session.request.call_args_list[0].kwargs["params"]["jql"]
        second_jql = session.request.call_args_list[1].kwargs["params"]["jql"]
        assert f"agdt-orch-key:{digest}" in first_jql
        assert f"agdt-orch-key:{key}" in second_jql
        assert [call.args[0] for call in session.request.call_args_list] == ["GET", "GET"]

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


class TestJiraProviderCreationContractGaps:
    """Jira-specific gap tests complementing the shared contract suite."""

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


class TestJiraCreationFailurePropagation:
    """Jira creation failures propagate the ordinary adapter exception (FR-007).

    Jira embeds ``parent``/epic-link in the creation POST and has no separate
    post-create link stage, so no ``HierarchyLinkError`` wrapping is applied â€”
    a failed create with a parent surfaces the ordinary creation exception.
    """

    def test_create_issue_with_parent_failure_does_not_wrap_in_hierarchy_link_error(self):

        session = _make_mock_session()
        session.request.return_value = _make_response(400, text="bad request")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(Exception) as exc_info:
            provider.create_issue("Sub", "Body", "subtask", parent_id="PROJ-1", dry_run=False)
        assert not isinstance(exc_info.value, HierarchyLinkError)

"""Tests for the JiraProvider labels capability."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import (
    ProviderIssueResult,
)
from agentic_devtools.adapters.jira_provider import JiraProvider
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response


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
        # GET returns a dict but with `fields` as a non-empty list â€” a truthy non-dict value.
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
        # Requesting the same label without whitespace â€” should be a no-op after stripping
        result = provider.apply_labels("PROJ-1", ["existing-label"], dry_run=False)
        assert result.status == "no-op"
        # Only one GET call â€” no PUT was issued
        assert session.request.call_count == 1

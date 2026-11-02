"""Tests for the JiraProvider http capability."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.jira_provider import JiraProvider
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response


class TestJiraProviderHttpHelpers:
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

    def test_is_field_inapplicable_error_does_not_fall_through_for_string_field_error(self):
        response = _make_response(
            400,
            {
                "errors": {"customfield_10008": "Unrelated field validation failure"},
                "errorMessages": ["customfield_10008 cannot be set in this context"],
            },
        )

        assert not JiraProvider._is_field_inapplicable_error(response, "customfield_10008")

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

    def test_is_field_inapplicable_error_returns_false_for_unrelated_error(self):
        response = _make_response(
            400,
            {"errors": "invalid", "errorMessages": "invalid"},
            text="Unrelated validation failure",
        )
        assert not JiraProvider._is_field_inapplicable_error(response, "customfield_10008")

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

    def test_get_epic_link_field_transient_error_raises(self):
        """_get_epic_link_field raises TransientError on 429/502/503."""
        session = _make_mock_session()
        resp = _make_response(429)
        session.request.return_value = resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(TransientError, match="429"):
            provider._get_epic_link_field()

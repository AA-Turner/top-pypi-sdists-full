"""Tests for the JiraProvider config capability."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from agentic_devtools.adapters.jira_provider import JiraProvider
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response


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


class TestJiraProviderSession:
    """Tests for internal helper methods and session construction."""

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


class TestJiraProviderConfigContractGaps:
    """Jira-specific gap tests complementing the shared contract suite."""

    def test_init_accepts_valid_project_key_and_base_url(self):
        """__init__ accepts a valid project key and base URL (T024)."""
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=_make_mock_session())
        assert provider.project_key == "PROJ"
        assert provider._base_url == "https://jira.example.com"

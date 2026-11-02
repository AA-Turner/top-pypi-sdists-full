"""Tests for _validate_jira_prerequisites."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from agentic_devtools.adapters.factory import _validate_jira_prerequisites
from agentic_devtools.epic_tree.errors import ConfigError


class TestValidateJiraPrerequisites:
    """Verify Jira prerequisite validation."""

    def test_jira_missing_project_key(self):
        """Missing project_key raises ConfigError."""
        with patch.dict(os.environ, {"JIRA_BASE_URL": "https://j.example.com", "JIRA_API_TOKEN": "tok"}, clear=True):
            with pytest.raises(ConfigError) as exc_info:
                _validate_jira_prerequisites({}, "/tmp/repo")
        assert "platform.jira.project_key" in str(exc_info.value)

    def test_jira_empty_project_key(self):
        """Empty project_key raises ConfigError."""
        with patch.dict(os.environ, {"JIRA_BASE_URL": "https://j.example.com", "JIRA_API_TOKEN": "tok"}, clear=True):
            with pytest.raises(ConfigError) as exc_info:
                _validate_jira_prerequisites({"project_key": "  "}, "/tmp/repo")
        assert "platform.jira.project_key" in str(exc_info.value)

    def test_jira_non_dict_config_raises_project_key_error(self):
        """Non-dict jira_config raises a clear ConfigError for missing project_key."""
        with patch.dict(os.environ, {"JIRA_BASE_URL": "https://j.example.com", "JIRA_API_TOKEN": "tok"}, clear=True):
            with pytest.raises(ConfigError) as exc_info:
                _validate_jira_prerequisites([], "/tmp/repo")
        assert "platform.jira.project_key" in str(exc_info.value)

    def test_jira_no_auth_token(self):
        """Neither JIRA_API_TOKEN nor JIRA_COPILOT_PAT set raises ConfigError."""
        env = {"JIRA_BASE_URL": "https://j.example.com"}
        with patch.dict(os.environ, env, clear=True):
            with pytest.raises(ConfigError) as exc_info:
                _validate_jira_prerequisites({"project_key": "PROJ"}, "/tmp/repo")
        assert "JIRA_API_TOKEN" in str(exc_info.value)
        assert "JIRA_COPILOT_PAT" in str(exc_info.value)

    def test_jira_no_base_url(self):
        """Neither config nor env JIRA_BASE_URL raises ConfigError."""
        env = {"JIRA_API_TOKEN": "tok"}
        with patch.dict(os.environ, env, clear=True):
            with pytest.raises(ConfigError) as exc_info:
                _validate_jira_prerequisites({"project_key": "PROJ"}, "/tmp/repo")
        assert "base_url" in str(exc_info.value).lower() or "JIRA_BASE_URL" in str(exc_info.value)

    def test_jira_basic_auth_no_identity(self):
        """JIRA_AUTH_SCHEME=basic without identity vars raises ConfigError."""
        env = {
            "JIRA_BASE_URL": "https://j.example.com",
            "JIRA_API_TOKEN": "tok",
            "JIRA_AUTH_SCHEME": "basic",
        }
        with patch.dict(os.environ, env, clear=True):
            with pytest.raises(ConfigError) as exc_info:
                _validate_jira_prerequisites({"project_key": "PROJ"}, "/tmp/repo")
        assert "identity" in str(exc_info.value).lower() or "JIRA_USER_EMAIL" in str(exc_info.value)

    def test_jira_happy_path(self):
        """Valid config returns (project_key, base_url) tuple."""
        env = {
            "JIRA_BASE_URL": "https://jira.example.com",
            "JIRA_API_TOKEN": "tok",
        }
        with patch.dict(os.environ, env, clear=True):
            result = _validate_jira_prerequisites({"project_key": "PROJ"}, "/tmp/repo")
        assert result == ("PROJ", "https://jira.example.com")

    def test_jira_base_url_from_config(self):
        """base_url resolved from config takes precedence over env."""
        env = {
            "JIRA_BASE_URL": "https://env.example.com",
            "JIRA_API_TOKEN": "tok",
        }
        with patch.dict(os.environ, env, clear=True):
            result = _validate_jira_prerequisites(
                {"project_key": "PROJ", "base_url": "https://config.example.com"},
                "/tmp/repo",
            )
        assert result == ("PROJ", "https://config.example.com")

    def test_jira_basic_auth_with_identity(self):
        """JIRA_AUTH_SCHEME=basic with identity passes."""
        env = {
            "JIRA_BASE_URL": "https://j.example.com",
            "JIRA_API_TOKEN": "tok",
            "JIRA_AUTH_SCHEME": "basic",
            "JIRA_USER_EMAIL": "user@example.com",
        }
        with patch.dict(os.environ, env, clear=True):
            result = _validate_jira_prerequisites({"project_key": "PROJ"}, "/tmp/repo")
        assert result == ("PROJ", "https://j.example.com")

    def test_jira_base_url_non_string_in_config(self):
        """Non-string base_url in config falls through to env var."""
        env = {
            "JIRA_BASE_URL": "https://env.example.com",
            "JIRA_API_TOKEN": "tok",
        }
        with patch.dict(os.environ, env, clear=True):
            result = _validate_jira_prerequisites(
                {"project_key": "PROJ", "base_url": 12345},
                "/tmp/repo",
            )
        assert result == ("PROJ", "https://env.example.com")

    def test_jira_whitespace_identity_env_var_raises(self):
        """Whitespace-only identity env var raises ConfigError even without JIRA_AUTH_SCHEME=basic."""
        env = {
            "JIRA_BASE_URL": "https://j.example.com",
            "JIRA_API_TOKEN": "tok",
            "JIRA_USER_EMAIL": "  ",
        }
        with patch.dict(os.environ, env, clear=True):
            with pytest.raises(ConfigError) as exc_info:
                _validate_jira_prerequisites({"project_key": "PROJ"}, "/tmp/repo")
        assert "JIRA_USER_EMAIL" in str(exc_info.value)

    def test_jira_identity_env_var_set_without_basic_scheme(self):
        """Identity env var set without JIRA_AUTH_SCHEME=basic passes when non-empty."""
        env = {
            "JIRA_BASE_URL": "https://j.example.com",
            "JIRA_API_TOKEN": "tok",
            "JIRA_USER_EMAIL": "user@example.com",
        }
        with patch.dict(os.environ, env, clear=True):
            result = _validate_jira_prerequisites({"project_key": "PROJ"}, "/tmp/repo")
        assert result == ("PROJ", "https://j.example.com")

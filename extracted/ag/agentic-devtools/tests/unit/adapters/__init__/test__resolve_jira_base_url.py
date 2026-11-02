"""Tests for :func:`agentic_devtools.adapters._resolve_jira_base_url`."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.adapters import _resolve_jira_base_url


class TestResolveJiraBaseUrl:
    """Verify Jira base URL fallback precedence."""

    def test_uses_project_config_base_url_when_git_root_provided(self, monkeypatch, tmp_path) -> None:
        """Probe callers can resolve Jira base URL from .agdt/config/project.json without env vars."""
        monkeypatch.delenv("JIRA_BASE_URL", raising=False)

        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "project.json").write_text('{"jira_base_url":"https://project.jira.com"}', encoding="utf-8")

        assert _resolve_jira_base_url(tmp_path) == "https://project.jira.com"

    def test_project_config_precedes_environment_base_url(self, monkeypatch, tmp_path) -> None:
        """When enabled, effective project config takes precedence over JIRA_BASE_URL."""
        monkeypatch.setenv("JIRA_BASE_URL", "https://env.jira.com")

        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "project.json").write_text('{"jira_base_url":"https://project.jira.com"}', encoding="utf-8")

        assert _resolve_jira_base_url(tmp_path) == "https://project.jira.com"

    def test_uses_state_base_url_when_project_config_missing(self, monkeypatch, tmp_path) -> None:
        """Probe callers can fall back to jira_base_url state when project config has no value."""
        monkeypatch.delenv("JIRA_BASE_URL", raising=False)

        def _mock_state_get_value(key: str, required: bool = False):  # noqa: ARG001
            if key == "jira_base_url":
                return "https://state.jira.com"
            return None

        with patch("agentic_devtools.state.get_value", side_effect=_mock_state_get_value):
            assert _resolve_jira_base_url(tmp_path) == "https://state.jira.com"

    def test_manual_mode_ignores_project_config_and_uses_state_then_env(self, monkeypatch, tmp_path) -> None:
        """Manual mode hides project.json, preserving state-before-env fallback precedence."""
        monkeypatch.setenv("JIRA_BASE_URL", "https://env.jira.com")

        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "project.json").write_text('{"jira_base_url":"https://project.jira.com"}', encoding="utf-8")

        def _mock_state_get_value(key: str, required: bool = False):  # noqa: ARG001
            if key == "config_mode":
                return "manual"
            if key == "jira_base_url":
                return "https://state.jira.com"
            return None

        with patch("agentic_devtools.state.get_value", side_effect=_mock_state_get_value):
            assert _resolve_jira_base_url(tmp_path) == "https://state.jira.com"

"""Tests for the get_issue_provider factory."""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.adapters.factory import get_issue_provider
from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.jira_provider import JiraProvider
from agentic_devtools.epic_tree.errors import ConfigError


def _mock_gh_auth_success(*args, **kwargs):
    """Mock run_safe for gh auth status returning success."""
    return subprocess.CompletedProcess(args=["gh", "auth", "status"], returncode=0, stdout="", stderr="")


class TestGetIssueProvider:
    """Verify factory resolution for all acceptance scenarios."""

    def test_github_from_config(self, tmp_path):
        """SC1: platform.issue_adapter = 'github' in config returns GitHubProvider."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "github", "github": {"repo": "owner/repo"}}}')

        with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
            provider = get_issue_provider(str(tmp_path))
        assert isinstance(provider, GitHubProvider)
        assert provider.owner_repo == "owner/repo"

    def test_jira_from_config(self, tmp_path):
        """SC2: platform.issue_adapter = 'jira' in config returns JiraProvider."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}}}')

        with patch.dict(os.environ, {"JIRA_BASE_URL": "https://jira.example.com", "JIRA_API_TOKEN": "tok"}, clear=True):
            provider = get_issue_provider(str(tmp_path))
        assert isinstance(provider, JiraProvider)
        assert provider.project_key == "PROJ"

    def test_unrecognized_adapter_raises_config_error(self, tmp_path):
        """SC3: Unrecognized value raises ConfigError with supported list."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "gitlab"}}')

        with pytest.raises(ConfigError) as exc_info:
            get_issue_provider(str(tmp_path))
        assert "gitlab" in str(exc_info.value)
        assert "github" in str(exc_info.value)
        assert "jira" in str(exc_info.value)

    def test_markdown_raises_config_error(self, tmp_path):
        """SC4: 'markdown' value raises ConfigError explaining it's for get_adapter only."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "markdown"}}')

        with pytest.raises(ConfigError) as exc_info:
            get_issue_provider(str(tmp_path))
        assert "markdown" in str(exc_info.value)
        assert "get_adapter" in str(exc_info.value)

    def test_missing_config_raises_config_error(self, tmp_path):
        """SC5: No config at all raises ConfigError with resolution sources."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("agentic_devtools.state.get_value", return_value=None):
                with pytest.raises(ConfigError) as exc_info:
                    get_issue_provider(str(tmp_path))
        msg = str(exc_info.value)
        assert "--provider" in msg
        assert "platform.issue_adapter" in msg
        assert "AGDT_ISSUE_ADAPTER" in msg

    def test_env_var_fallback(self, tmp_path):
        """Factory resolves from AGDT_ISSUE_ADAPTER env var."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"github": {"repo": "owner/repo"}}}')

        with patch.dict(os.environ, {"AGDT_ISSUE_ADAPTER": "github"}):
            with patch("agentic_devtools.state.get_value", return_value=None):
                with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
                    provider = get_issue_provider(str(tmp_path))
        assert isinstance(provider, GitHubProvider)

    def test_platform_not_a_dict_raises_config_error(self, tmp_path):
        """Platform value that is not a dict raises ConfigError."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": "invalid"}')

        with pytest.raises(ConfigError) as exc_info:
            get_issue_provider(str(tmp_path))
        assert "must be a mapping" in str(exc_info.value)

    def test_state_key_fallback(self, tmp_path):
        """Factory resolves from state key when config has no issue_adapter."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"github": {"repo": "owner/repo"}}}')

        with patch.dict(os.environ, {}, clear=False):
            # Remove AGDT_ISSUE_ADAPTER if set
            os.environ.pop("AGDT_ISSUE_ADAPTER", None)
            with patch("agentic_devtools.state.get_value", return_value="github"):
                with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
                    provider = get_issue_provider(str(tmp_path))
        assert isinstance(provider, GitHubProvider)

    def test_state_key_exception_falls_through(self, tmp_path):
        """When state raises an exception, factory continues to env var."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"github": {"repo": "owner/repo"}}}')

        with patch.dict(os.environ, {"AGDT_ISSUE_ADAPTER": "github"}):
            with patch(
                "agentic_devtools.state.get_value",
                side_effect=RuntimeError("state unavailable"),
            ):
                with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
                    provider = get_issue_provider(str(tmp_path))
        assert isinstance(provider, GitHubProvider)

    def test_github_missing_repo_coordinates_raises_config_error(self, tmp_path):
        """GitHub adapter config must include repo slug or owner/name parts."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "github", "github": {}}}')

        with pytest.raises(ConfigError) as exc_info:
            get_issue_provider(str(tmp_path))

        assert "platform.github.repo" in str(exc_info.value)

    def test_jira_missing_project_key_raises_config_error(self, tmp_path):
        """Jira adapter config must include a project key."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "jira", "jira": {}}}')

        with pytest.raises(ConfigError) as exc_info:
            get_issue_provider(str(tmp_path))

        assert "platform.jira.project_key" in str(exc_info.value)

    def test_repo_path_accepts_pathlib_path(self, tmp_path):
        """FR-001: Path object works as repo_path."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "github", "github": {"repo": "owner/repo"}}}')

        with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
            provider = get_issue_provider(Path(tmp_path))
        assert isinstance(provider, GitHubProvider)

    def test_provider_arg_overrides_config(self, tmp_path):
        """FR-002: Explicit provider='jira' overrides config 'github'."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text(
            '{"platform": {"issue_adapter": "github", "github": {"repo": "owner/repo"}, '
            '"jira": {"project_key": "PROJ"}}}'
        )

        with patch.dict(os.environ, {"JIRA_BASE_URL": "https://jira.example.com", "JIRA_API_TOKEN": "tok"}, clear=True):
            provider = get_issue_provider(str(tmp_path), provider="jira")
        assert isinstance(provider, JiraProvider)

    def test_provider_arg_with_no_config_issue_adapter(self, tmp_path):
        """FR-002: provider='github' works when config has no issue_adapter."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"github": {"repo": "owner/repo"}}}')

        with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
            provider = get_issue_provider(str(tmp_path), provider="github")
        assert isinstance(provider, GitHubProvider)

    def test_provider_arg_ignores_config_issue_adapter(self, tmp_path):
        """FR-002: provider='github' overrides invalid config issue_adapter."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "gitlab", "github": {"repo": "owner/repo"}}}')

        with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
            provider = get_issue_provider(str(tmp_path), provider="github")
        assert isinstance(provider, GitHubProvider)

    def test_platform_non_dict_raises_immediately_without_provider(self, tmp_path):
        """FR-002 edge: platform non-dict raises even without provider override."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": "github"}')

        with pytest.raises(ConfigError) as exc_info:
            get_issue_provider(str(tmp_path))
        assert "must be a mapping" in str(exc_info.value)

    def test_platform_non_dict_raises_immediately_with_provider(self, tmp_path):
        """FR-002 edge: platform non-dict raises even with provider override."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": "github"}')

        with pytest.raises(ConfigError) as exc_info:
            get_issue_provider(str(tmp_path), provider="github")
        assert "must be a mapping" in str(exc_info.value)

    def test_empty_issue_adapter_falls_through(self, tmp_path):
        """FR-002: Empty-string issue_adapter falls through to next source."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "", "github": {"repo": "owner/repo"}}}')

        with patch.dict(os.environ, {"AGDT_ISSUE_ADAPTER": "github"}):
            with patch("agentic_devtools.state.get_value", return_value=None):
                with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
                    provider = get_issue_provider(str(tmp_path))
        assert isinstance(provider, GitHubProvider)

    def test_non_string_issue_adapter_raises_config_error(self, tmp_path):
        """FR-002 edge: non-string issue_adapter fails fast instead of falling through."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": 123, "github": {"repo": "owner/repo"}}}')

        with patch.dict(os.environ, {"AGDT_ISSUE_ADAPTER": "github"}):
            with patch("agentic_devtools.state.get_value", return_value="jira"):
                with pytest.raises(ConfigError) as exc_info:
                    get_issue_provider(str(tmp_path))
        assert "must be a string" in str(exc_info.value)
        assert "platform.issue_adapter" in str(exc_info.value)

    def test_nonexistent_repo_path_allows_env_var_resolution(self, tmp_path):
        """FR-002 edge: env-var adapter selection still works when repo_path has no config."""
        nonexistent = tmp_path / "nonexistent"

        with patch.dict(os.environ, {"AGDT_ISSUE_ADAPTER": "github"}):
            with patch("agentic_devtools.state.get_value", return_value=None):
                with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
                    with patch(
                        "agentic_devtools.config.load_platform_config",
                        return_value={
                            "github": {"repo": "owner/repo"},
                        },
                    ):
                        provider = get_issue_provider(str(nonexistent))
        assert isinstance(provider, GitHubProvider)

    def test_adapter_name_normalization(self, tmp_path):
        """FR-006: Various casings resolve correctly."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()

        for name in ("GitHub", " github ", "GITHUB"):
            config_file = config_dir / "agdt-config.json"
            config_file.write_text(f'{{"platform": {{"issue_adapter": "{name}", "github": {{"repo": "owner/repo"}}}}}}')

            with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
                provider = get_issue_provider(str(tmp_path))
            assert isinstance(provider, GitHubProvider)

    def test_no_stdout_stderr_output(self, tmp_path, capsys):
        """FR-008: Factory does not write directly to stdout/stderr."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "github", "github": {"repo": "owner/repo"}}}')

        # Suppress logger output from config helpers
        config_logger = logging.getLogger("agentic_devtools.config")
        previous_level = config_logger.level
        config_logger.setLevel(logging.CRITICAL)
        try:
            with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
                get_issue_provider(str(tmp_path))
            captured = capsys.readouterr()
            assert captured.out == ""
            assert captured.err == ""
        finally:
            config_logger.setLevel(previous_level)

    def test_no_network_io_during_construction(self, tmp_path, monkeypatch):
        """SC-007: No network I/O during provider construction."""
        import socket

        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "github", "github": {"repo": "owner/repo"}}}')

        # Mock run_safe to prevent real subprocess
        monkeypatch.setattr(
            "agentic_devtools.adapters.factory.run_safe",
            _mock_gh_auth_success,
        )
        # Monkeypatch socket to detect any Python-level network I/O

        def _no_socket(*args, **kwargs):
            raise AssertionError("Unexpected network I/O during construction")

        monkeypatch.setattr(socket, "socket", _no_socket)

        provider = get_issue_provider(str(tmp_path))
        assert isinstance(provider, GitHubProvider)

    def test_provider_arg_whitespace_only_falls_through(self, tmp_path):
        """provider='  ' is treated as unset and falls through to config."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "github", "github": {"repo": "owner/repo"}}}')

        with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
            provider = get_issue_provider(str(tmp_path), provider="  ")
        assert isinstance(provider, GitHubProvider)

    def test_provider_arg_non_string_raises_config_error(self, tmp_path):
        """Non-string provider argument raises ConfigError, not AttributeError."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text("{}")

        with pytest.raises(ConfigError) as exc_info:
            get_issue_provider(str(tmp_path), provider=123)  # type: ignore[arg-type]
        assert "must be a string" in str(exc_info.value)
        assert "int" in str(exc_info.value)

    def test_github_provider_init_valueerror_wrapped(self, tmp_path):
        """ValueError from GitHubProvider.__init__ is re-raised as ConfigError."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "github", "github": {"repo": "owner/repo"}}}')

        with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
            with patch(
                "agentic_devtools.adapters.github_provider.GitHubProvider.__init__",
                side_effect=ValueError("bad slug"),
            ):
                with pytest.raises(ConfigError) as exc_info:
                    get_issue_provider(str(tmp_path))
        assert "Invalid GitHub repository slug" in str(exc_info.value)


class TestResolutionPriority:
    """SC-005: Verify the full 4-level resolution priority chain."""

    def test_explicit_arg_wins(self, tmp_path):
        """Level 1: provider arg wins over all other sources."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text(
            '{"platform": {"issue_adapter": "jira", "github": {"repo": "owner/repo"}, "jira": {"project_key": "P"}}}'
        )

        env = {
            "AGDT_ISSUE_ADAPTER": "jira",
            "JIRA_BASE_URL": "https://j.example.com",
            "JIRA_API_TOKEN": "t",
        }
        with patch.dict(os.environ, env):
            with patch("agentic_devtools.state.get_value", return_value="jira"):
                with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
                    provider = get_issue_provider(str(tmp_path), provider="github")
        assert isinstance(provider, GitHubProvider)

    def test_config_wins_over_state(self, tmp_path):
        """Level 2: config wins over state when no explicit arg."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text(
            '{"platform": {"issue_adapter": "github", "github": {"repo": "owner/repo"}, "jira": {"project_key": "P"}}}'
        )

        env = {
            "AGDT_ISSUE_ADAPTER": "jira",
            "JIRA_BASE_URL": "https://j.example.com",
            "JIRA_API_TOKEN": "t",
        }
        with patch.dict(os.environ, env):
            with patch("agentic_devtools.state.get_value", return_value="jira"):
                with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
                    provider = get_issue_provider(str(tmp_path))
        assert isinstance(provider, GitHubProvider)

    def test_state_wins_over_env(self, tmp_path):
        """Level 3: state wins over env when no config issue_adapter."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"github": {"repo": "owner/repo"}, "jira": {"project_key": "P"}}}')

        env = {
            "AGDT_ISSUE_ADAPTER": "jira",
            "JIRA_BASE_URL": "https://j.example.com",
            "JIRA_API_TOKEN": "t",
        }
        with patch.dict(os.environ, env):
            with patch("agentic_devtools.state.get_value", return_value="github"):
                with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
                    provider = get_issue_provider(str(tmp_path))
        assert isinstance(provider, GitHubProvider)

    def test_env_var_last_resort(self, tmp_path):
        """Level 4: env var resolves when no other source is set."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"github": {"repo": "owner/repo"}}}')

        with patch.dict(os.environ, {"AGDT_ISSUE_ADAPTER": "github"}):
            with patch("agentic_devtools.state.get_value", return_value=None):
                with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
                    provider = get_issue_provider(str(tmp_path))
        assert isinstance(provider, GitHubProvider)

    def test_no_source_raises_config_error(self, tmp_path):
        """All four source names mentioned in error when none yields a value."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {}}')

        with patch.dict(os.environ, {}, clear=True):
            with patch("agentic_devtools.state.get_value", return_value=None):
                with pytest.raises(ConfigError) as exc_info:
                    get_issue_provider(str(tmp_path))
        msg = str(exc_info.value)
        assert "--provider" in msg
        assert "platform.issue_adapter" in msg
        assert "AGDT_ISSUE_ADAPTER" in msg


class TestSourceAttribution:
    """NFR-002: Verify error messages attribute the correct source."""

    def test_unsupported_value_from_config_names_config_file(self, tmp_path):
        """Config source attribution includes .github/agdt-config.json."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"issue_adapter": "gitlab"}}')

        with pytest.raises(ConfigError) as exc_info:
            get_issue_provider(str(tmp_path))
        assert exc_info.value.config_path == ".github/agdt-config.json"
        assert exc_info.value.field == "platform.issue_adapter"

    def test_unsupported_value_from_state_names_state_source(self, tmp_path):
        """State source attribution includes 'agdt state'."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {}}')

        with patch("agentic_devtools.state.get_value", return_value="gitlab"):
            with pytest.raises(ConfigError) as exc_info:
                get_issue_provider(str(tmp_path))
        assert exc_info.value.config_path == "agdt state"
        assert exc_info.value.field == "platform.issue_adapter"

    def test_non_string_state_value_raises_config_error(self, tmp_path):
        """Non-string platform.issue_adapter state value fails fast instead of coercing."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {}}')

        with patch("agentic_devtools.state.get_value", return_value=123):
            with pytest.raises(ConfigError) as exc_info:
                get_issue_provider(str(tmp_path))
        assert exc_info.value.config_path == "agdt state"
        assert exc_info.value.field == "platform.issue_adapter"
        assert "int" in str(exc_info.value)

    def test_whitespace_only_state_value_falls_through_to_env(self, tmp_path):
        """Whitespace-only state value is treated as unset and falls through to env var."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {"github": {"repo": "owner/repo"}}}')

        with patch.dict(os.environ, {"AGDT_ISSUE_ADAPTER": "github"}):
            with patch("agentic_devtools.state.get_value", return_value="   "):
                with patch("agentic_devtools.adapters.factory.run_safe", side_effect=_mock_gh_auth_success):
                    provider = get_issue_provider(str(tmp_path))
        assert isinstance(provider, GitHubProvider)

    def test_unsupported_value_from_env_names_env_var(self, tmp_path):
        """Env var source attribution includes env var name."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {}}')

        with patch.dict(os.environ, {"AGDT_ISSUE_ADAPTER": "gitlab"}):
            with patch("agentic_devtools.state.get_value", return_value=None):
                with pytest.raises(ConfigError) as exc_info:
                    get_issue_provider(str(tmp_path))
        assert exc_info.value.config_path == "environment variable AGDT_ISSUE_ADAPTER"
        assert exc_info.value.field == "AGDT_ISSUE_ADAPTER"

    def test_unsupported_value_from_provider_arg_names_cli_arg(self, tmp_path):
        """CLI arg source attribution includes --provider."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {}}')

        with pytest.raises(ConfigError) as exc_info:
            get_issue_provider(str(tmp_path), provider="gitlab")
        assert exc_info.value.config_path == "CLI argument --provider"
        assert exc_info.value.field == "--provider"

    def test_markdown_from_provider_arg_distinct_error(self, tmp_path):
        """CLI --provider=markdown gets distinct message with CLI attribution."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text('{"platform": {}}')

        with pytest.raises(ConfigError) as exc_info:
            get_issue_provider(str(tmp_path), provider="markdown")
        assert "get_adapter" in str(exc_info.value)
        assert exc_info.value.config_path == "CLI argument --provider"
        assert exc_info.value.field == "--provider"

    def test_unsupported_adapter_three_distinct_values(self, tmp_path):
        """SC-003: Three different unsupported values all produce ConfigError."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()

        for value in ("gitlab", "bitbucket", "azure"):
            config_file = config_dir / "agdt-config.json"
            config_file.write_text(f'{{"platform": {{"issue_adapter": "{value}"}}}}')

            with pytest.raises(ConfigError) as exc_info:
                get_issue_provider(str(tmp_path))
            assert value in str(exc_info.value)
            assert "github" in str(exc_info.value)
            assert "jira" in str(exc_info.value)

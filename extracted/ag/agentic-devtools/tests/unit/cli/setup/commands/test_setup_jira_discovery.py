"""Tests for Jira discovery integration in setup_cmd (Step 1.5)."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.setup import commands
from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.tools.jira import JiraConfig


def _make_statuses() -> list:
    return [
        DependencyStatus(name="copilot", found=True, version="v1.0.0", path="/bin/copilot", category="Recommended"),
        DependencyStatus(name="gh", found=True, version="v2.65.0", path="/bin/gh", category="Recommended"),
        DependencyStatus(
            name="git",
            found=True,
            path="/usr/bin/git",
            version="2.43.0",
            required=True,
            category="Required",
        ),
        DependencyStatus(name="az", found=False, category="Optional — needed for Azure DevOps"),
        DependencyStatus(name="code", found=False, category="Optional — needed for VS Code integration"),
    ]


_PROBE_CONFIG = JiraConfig(
    base_url="https://jira.example.com",
    headers={"Authorization": "******"},
    ssl_verify=True,
)


class TestSetupJiraDiscoveryIntegration:
    """Tests for the Jira instance discovery step in _run_file_modifying_steps."""

    def _run_setup_with_platform_config(
        self,
        tmp_path,
        platform_config,
        discovery_mock=None,
        cache_mock=None,
        connectivity_result=(True, None),
    ):
        """Helper to run setup_cmd with the given platform_config and discovery mocks."""
        mock_result = MagicMock()
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses()):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=mock_result,
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                            return_value=platform_config,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.cli.jira.discovery.get_instance_metadata",
                                                                        return_value=discovery_mock,
                                                                    ) as mock_get:
                                                                        with patch(
                                                                            "agentic_devtools.cli.jira.discovery.load_cached_instance_metadata",
                                                                            return_value=cache_mock,
                                                                        ):
                                                                            with patch(
                                                                                "agentic_devtools.cli.setup.provider_connectivity.check_provider_connectivity",
                                                                                return_value=connectivity_result,
                                                                            ) as mock_connectivity:
                                                                                with patch(
                                                                                    "agentic_devtools.adapters.resolve_jira_config",
                                                                                    return_value=_PROBE_CONFIG,
                                                                                ):
                                                                                    commands.setup_cmd()
        return mock_get, mock_connectivity

    def test_jira_adapter_calls_discovery(self, tmp_path, capsys) -> None:
        """When issue_adapter is 'jira', get_instance_metadata is called and output is printed."""
        metadata = {
            "version": "10.3.17",
            "versionNumbers": [10, 3, 17],
            "deploymentType": "Server",
            "buildNumber": "1003017",
            "baseUrl": "https://jira.example.com",
            "discoveredUtc": "2024-06-01T12:00:00+00:00",
        }
        mock_get, mock_connectivity = self._run_setup_with_platform_config(
            tmp_path,
            platform_config={"issue_adapter": "jira"},
            discovery_mock=metadata,
            cache_mock=None,
        )

        mock_get.assert_called_once_with(force_refresh=False, config=_PROBE_CONFIG)
        mock_connectivity.assert_called_once_with("jira", tmp_path, timeout=5.0)
        captured = capsys.readouterr()
        assert "Jira v10.3.17" in captured.out
        assert "(Server)" in captured.out
        assert "https://jira.example.com" in captured.out
        assert "(cached)" not in captured.out

    def test_cache_hit_shows_cached_suffix(self, tmp_path, capsys) -> None:
        """When cache is valid, output shows (cached) suffix."""
        metadata = {
            "version": "10.3.17",
            "versionNumbers": [10, 3, 17],
            "deploymentType": "Server",
            "buildNumber": "1003017",
            "baseUrl": "https://jira.example.com",
            "discoveredUtc": "2024-06-01T12:00:00+00:00",
        }
        mock_get, mock_connectivity = self._run_setup_with_platform_config(
            tmp_path,
            platform_config={"issue_adapter": "jira"},
            discovery_mock=metadata,
            cache_mock=metadata,
        )

        mock_connectivity.assert_not_called()
        mock_get.assert_called_once_with(force_refresh=False)
        captured = capsys.readouterr()
        assert "(cached)" in captured.out

    def test_non_jira_adapter_skips_discovery(self, tmp_path, capsys) -> None:
        """When issue_adapter is 'github', no Jira discovery is performed."""
        mock_get, _ = self._run_setup_with_platform_config(
            tmp_path,
            platform_config={"issue_adapter": "github"},
        )

        mock_get.assert_not_called()
        captured = capsys.readouterr()
        assert "Jira v" not in captured.out

    def test_missing_issue_adapter_skips_discovery(self, tmp_path, capsys) -> None:
        """When issue_adapter is not set, no Jira discovery is performed."""
        mock_get, _ = self._run_setup_with_platform_config(
            tmp_path,
            platform_config={},
        )

        mock_get.assert_not_called()
        captured = capsys.readouterr()
        assert "Jira v" not in captured.out

    def test_discovery_returns_none_no_output(self, tmp_path, capsys) -> None:
        """When get_instance_metadata returns None, no Jira version line is printed."""
        self._run_setup_with_platform_config(
            tmp_path,
            platform_config={"issue_adapter": "jira"},
            discovery_mock=None,
            cache_mock=None,
        )

        captured = capsys.readouterr()
        assert "Jira v" not in captured.out

    def test_exception_emits_warning_and_continues(self, tmp_path, capsys) -> None:
        """Unexpected exception prints warning to stderr and does not raise."""
        mock_result = MagicMock()
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        with patch("sys.argv", ["agdt-setup"]):
            with patch("sys.stdin", mock_stdin):
                with patch.object(commands, "_prefetch_certs", return_value=(None, None)):
                    with patch.object(commands, "install_copilot_cli", return_value=True):
                        with patch.object(commands, "install_gh_cli", return_value=True):
                            with patch.object(commands, "check_all_dependencies", return_value=_make_statuses()):
                                with patch.object(commands, "_persist_env_vars_to_profile"):
                                    with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                                        with patch(
                                            "agentic_devtools.agdt_gitignore.ensure_agdt_gitignore",
                                            return_value=True,
                                        ):
                                            with patch.object(commands, "_prompt_project_config"):
                                                with patch.object(commands, "_prompt_copilot_model"):
                                                    with patch(
                                                        "agentic_devtools.cli.setup.platform_detection.detect_platforms",
                                                        return_value=mock_result,
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.cli.setup.platform_detection.confirm_and_override",
                                                            return_value={"issue_adapter": "jira"},
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.config.save_platform_config",
                                                                return_value=True,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.cli.setup.workflow_templates.generate_default_templates",
                                                                    return_value=[],
                                                                ):
                                                                    with patch(
                                                                        "agentic_devtools.cli.jira.discovery.load_cached_instance_metadata",
                                                                        side_effect=RuntimeError("unexpected failure"),
                                                                    ):
                                                                        commands.setup_cmd()

        captured = capsys.readouterr()
        assert "Jira discovery skipped" in captured.err
        assert "unexpected failure" in captured.err

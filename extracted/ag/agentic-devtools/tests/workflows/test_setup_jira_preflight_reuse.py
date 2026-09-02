"""Workflow-level coverage for Jira setup preflight handoff."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.setup import commands
from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.tools.jira import JiraConfig

_PROBE_CONFIG = JiraConfig(
    base_url="https://jira.example.com",
    headers={"Authorization": "******"},
    ssl_verify=True,
)


def _make_statuses() -> list[DependencyStatus]:
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


def test_issue_type_discovery_reuses_jira_preflight_result(tmp_path) -> None:
    """Step 1.6 receives Step 1.5 Jira preflight result to avoid duplicate probing."""
    mock_result = MagicMock()
    mock_stdin = MagicMock()
    mock_stdin.isatty.return_value = True
    with (
        patch("sys.argv", ["agdt-setup"]),
        patch("sys.stdin", mock_stdin),
        patch.object(commands, "_prefetch_certs", return_value=(None, None)),
        patch.object(commands, "install_copilot_cli", return_value=True),
        patch.object(commands, "install_gh_cli", return_value=True),
        patch.object(commands, "check_all_dependencies", return_value=_make_statuses()),
        patch.object(commands, "_persist_env_vars_to_profile"),
        patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path),
        patch("agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True),
        patch.object(commands, "_prompt_project_config"),
        patch.object(commands, "_prompt_copilot_model"),
        patch("agentic_devtools.cli.setup.platform_detection.detect_platforms", return_value=mock_result),
        patch(
            "agentic_devtools.cli.setup.platform_detection.confirm_and_override", return_value={"issue_adapter": "jira"}
        ),
        patch("agentic_devtools.config.save_platform_config", return_value=True),
        patch("agentic_devtools.cli.setup.workflow_templates.generate_default_templates", return_value=[]),
        patch("agentic_devtools.cli.jira.discovery.get_instance_metadata", return_value=None),
        patch("agentic_devtools.cli.jira.discovery.load_cached_instance_metadata", return_value=None),
        patch(
            "agentic_devtools.cli.setup.provider_connectivity.check_provider_connectivity",
            return_value=(False, "offline"),
        ),
        patch("agentic_devtools.adapters.resolve_jira_config", return_value=_PROBE_CONFIG),
        patch("agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types") as mock_discover,
    ):
        commands.setup_cmd()

    mock_discover.assert_called_once()
    kwargs = mock_discover.call_args.kwargs
    assert kwargs["preflight_connectivity"] == (False, "offline")
    assert kwargs["preflight_warning_emitted"] is True


def test_unreachable_jira_skips_server_info_discovery(tmp_path, capsys) -> None:
    """Cache misses skip Jira serverInfo discovery when preflight connectivity fails."""
    mock_result = MagicMock()
    mock_stdin = MagicMock()
    mock_stdin.isatty.return_value = True
    with (
        patch("sys.argv", ["agdt-setup"]),
        patch("sys.stdin", mock_stdin),
        patch.object(commands, "_prefetch_certs", return_value=(None, None)),
        patch.object(commands, "install_copilot_cli", return_value=True),
        patch.object(commands, "install_gh_cli", return_value=True),
        patch.object(commands, "check_all_dependencies", return_value=_make_statuses()),
        patch.object(commands, "_persist_env_vars_to_profile"),
        patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path),
        patch("agentic_devtools.agdt_gitignore.ensure_agdt_gitignore", return_value=True),
        patch.object(commands, "_prompt_project_config"),
        patch.object(commands, "_prompt_copilot_model"),
        patch("agentic_devtools.cli.setup.platform_detection.detect_platforms", return_value=mock_result),
        patch(
            "agentic_devtools.cli.setup.platform_detection.confirm_and_override", return_value={"issue_adapter": "jira"}
        ),
        patch("agentic_devtools.config.save_platform_config", return_value=True),
        patch("agentic_devtools.cli.setup.workflow_templates.generate_default_templates", return_value=[]),
        patch("agentic_devtools.cli.jira.discovery.get_instance_metadata") as mock_get,
        patch("agentic_devtools.cli.jira.discovery.load_cached_instance_metadata", return_value=None),
        patch(
            "agentic_devtools.cli.setup.provider_connectivity.check_provider_connectivity",
            return_value=(False, "offline"),
        ),
        patch("agentic_devtools.adapters.resolve_jira_config", return_value=_PROBE_CONFIG),
    ):
        commands.setup_cmd()

    mock_get.assert_not_called()
    captured = capsys.readouterr()
    assert "Jira discovery skipped" in captured.err
    assert "offline" in captured.err

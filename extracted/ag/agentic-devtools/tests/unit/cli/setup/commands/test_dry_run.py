"""Tests for --dry-run behavior across setup commands."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup import commands
from agentic_devtools.cli.setup.version_guard import VersionGuardResult


@pytest.fixture(autouse=True)
def mock_setup_network():
    """Override the conftest autouse mock to allow dry-run testing."""
    yield


@pytest.fixture(autouse=True)
def isolate_os_environ():
    """Keep test environment variables isolated per test case."""
    original_env = os.environ.copy()
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(original_env)


class TestPrefetchCertsDryRun:
    """Tests for _prefetch_certs with dry_run=True."""

    def test_returns_planned_paths_on_dry_run(self) -> None:
        """dry_run=True returns the planned bundle and npmrc paths immediately."""
        result = commands._prefetch_certs(npm_enabled=True, dry_run=True)
        assert result == (
            Path.home() / ".agdt" / "certs" / "unified-ca-bundle.pem",
            Path.home() / ".agdt" / "npmrc",
        )

    def test_returns_no_npmrc_path_when_npm_disabled_on_dry_run(self) -> None:
        """dry_run=True omits the npmrc path when npm work is disabled."""
        result = commands._prefetch_certs(npm_enabled=False, dry_run=True)
        assert result == (Path.home() / ".agdt" / "certs" / "unified-ca-bundle.pem", None)

    def test_populates_selected_hosts_out_on_dry_run(self) -> None:
        """dry_run=True still reports the planned fixed/npm host set."""
        selected_hosts: list[str] = []

        commands._prefetch_certs(npm_enabled=True, dry_run=True, selected_hosts_out=selected_hosts)

        assert selected_hosts == [
            "api.github.com",
            "github.com",
            "dev.azure.com",
            "release-assets.githubusercontent.com",
            "registry.npmjs.org",
        ]

    def test_no_network_calls_on_dry_run(self) -> None:
        """dry_run=True makes no network calls."""
        with patch("agentic_devtools.cli.cert_utils.ensure_ca_bundle") as mock_cert:
            commands._prefetch_certs(npm_enabled=True, dry_run=True)
        mock_cert.assert_not_called()

    def test_no_environ_mutation_on_dry_run(self) -> None:
        """dry_run=True does not mutate os.environ."""
        original_env = os.environ.copy()
        commands._prefetch_certs(npm_enabled=True, dry_run=True)
        # No new env vars should have been set
        for key in ("REQUESTS_CA_BUNDLE", "NODE_EXTRA_CA_CERTS", "NPM_CONFIG_USERCONFIG"):
            if key not in original_env:
                assert key not in os.environ, f"{key} was unexpectedly set"

    def test_prints_would_message_on_dry_run(self, capsys: pytest.CaptureFixture[str]) -> None:
        """dry_run=True prints 'would ...' message."""
        commands._prefetch_certs(npm_enabled=True, dry_run=True)
        captured = capsys.readouterr()
        assert "would prefetch certificates" in captured.out


class TestPersistEnvVarsDryRun:
    """Tests for _persist_env_vars_to_profile with dry_run=True."""

    def test_no_profile_writes_on_dry_run(self) -> None:
        """dry_run=True does not write to shell profile."""
        with patch.object(commands, "persist_env_var") as mock_persist:
            with patch.object(commands, "persist_path_entry") as mock_path:
                commands._persist_env_vars_to_profile(
                    npmrc_path=Path("/fake/npmrc"),
                    unified_path=Path("/fake/bundle.pem"),
                    persist_env=True,
                    overwrite_env=True,
                    dry_run=True,
                )
        mock_persist.assert_not_called()
        mock_path.assert_not_called()

    def test_prints_would_message_on_dry_run(self, capsys: pytest.CaptureFixture[str]) -> None:
        """dry_run=True prints 'would ...' message."""
        commands._persist_env_vars_to_profile(
            npmrc_path=None,
            unified_path=None,
            persist_env=True,
            overwrite_env=False,
            dry_run=True,
        )
        captured = capsys.readouterr()
        assert "would persist environment variables" in captured.out

    def test_dry_run_with_persist_env_false_prints_manual_instructions(self) -> None:
        """dry_run=True + persist_env=False still previews manual instructions path."""
        with patch.object(commands, "_print_manual_instructions") as mock_manual:
            commands._persist_env_vars_to_profile(
                npmrc_path=Path("/fake/npmrc"),
                unified_path=Path("/fake/bundle.pem"),
                persist_env=False,
                overwrite_env=False,
                dry_run=True,
            )
        mock_manual.assert_called_once()


class TestInstallCopilotCliDryRun:
    """Tests for install_copilot_cli with dry_run=True."""

    def test_no_download_on_dry_run(self) -> None:
        """dry_run=True does not download anything."""
        from agentic_devtools.cli.setup.copilot_cli_installer import install_copilot_cli

        with patch("agentic_devtools.cli.setup.copilot_cli_installer.get_latest_release_info") as mock_release:
            result = install_copilot_cli(dry_run=True)
        mock_release.assert_not_called()
        assert result is True

    def test_prints_would_message_on_dry_run(self, capsys: pytest.CaptureFixture[str]) -> None:
        """dry_run=True prints 'would ...' message."""
        from agentic_devtools.cli.setup.copilot_cli_installer import install_copilot_cli

        install_copilot_cli(dry_run=True)
        captured = capsys.readouterr()
        assert "would install Copilot CLI" in captured.out


class TestInstallGhCliDryRun:
    """Tests for install_gh_cli with dry_run=True."""

    def test_no_download_on_dry_run(self) -> None:
        """dry_run=True does not download anything."""
        from agentic_devtools.cli.setup.gh_cli_installer import install_gh_cli

        with patch("agentic_devtools.cli.setup.gh_cli_installer.get_latest_release_info") as mock_release:
            result = install_gh_cli(dry_run=True)
        mock_release.assert_not_called()
        assert result is True

    def test_prints_would_message_on_dry_run(self, capsys: pytest.CaptureFixture[str]) -> None:
        """dry_run=True prints 'would ...' message."""
        from agentic_devtools.cli.setup.gh_cli_installer import install_gh_cli

        install_gh_cli(dry_run=True)
        captured = capsys.readouterr()
        assert "would install GitHub CLI" in captured.out


def _make_statuses(all_found=True):
    """Helper to create mock dependency statuses."""
    from unittest.mock import MagicMock

    s = MagicMock()
    s.required = True
    s.found = all_found
    return [s]


class TestSetupCmdDryRun:
    """Tests for setup_cmd --dry-run behavior."""

    def test_dry_run_exits_zero(self) -> None:
        """--dry-run exits with code 0."""
        with patch("sys.argv", ["agdt-setup", "--dry-run"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit) as exc_info:
                                    commands.setup_cmd()
        assert exc_info.value.code == 0

    def test_dry_run_report_has_mode_dry_run(self) -> None:
        """--dry-run sets report.mode to 'dry-run'."""
        with patch("sys.argv", ["agdt-setup", "--dry-run"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch(
                                "agentic_devtools.cli.setup.report.write_report", return_value=True
                            ) as mock_write:
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        report = mock_write.call_args[0][0]
        assert report.mode == "dry-run"

    def test_dry_run_mutator_phases_skipped(self) -> None:
        """--dry-run records mutator phases as 'skipped'."""
        with patch("sys.argv", ["agdt-setup", "--dry-run"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch(
                                "agentic_devtools.cli.setup.report.write_report", return_value=True
                            ) as mock_write:
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        report = mock_write.call_args[0][0]
        phase_map = {p.name: p.status for p in report.phases}
        assert phase_map["certificate_prefetch"] == "skipped"
        assert phase_map["cli_installation"] == "skipped"
        assert phase_map["environment_persistence"] == "skipped"
        assert phase_map["file_modifications"] == "skipped"
        assert phase_map["autorun_setup"] == "skipped"

    def test_dry_run_dependency_check_still_runs(self) -> None:
        """--dry-run still executes the read-only dependency check."""
        with patch("sys.argv", ["agdt-setup", "--dry-run"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(
                        commands, "check_all_dependencies", return_value=_make_statuses(True)
                    ) as mock_deps:
                        with patch.object(commands, "print_dependency_report") as mock_print:
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        mock_deps.assert_called_once()
        mock_print.assert_called_once()

    def test_dry_run_bypasses_missing_dep_exit(self) -> None:
        """--dry-run exits 0 even when required deps are missing."""
        with patch("sys.argv", ["agdt-setup", "--dry-run"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(False)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit) as exc_info:
                                    commands.setup_cmd()
        assert exc_info.value.code == 0

    def test_dry_run_no_environ_mutation_for_no_verify_ssl(self) -> None:
        """--dry-run --no-verify-ssl does not mutate os.environ."""
        original_env = os.environ.copy()
        with patch("sys.argv", ["agdt-setup", "--dry-run", "--no-verify-ssl"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        # AGDT_NO_VERIFY_SSL should NOT have been set
        if "AGDT_NO_VERIFY_SSL" not in original_env:
            assert "AGDT_NO_VERIFY_SSL" not in os.environ

    def test_dry_run_version_blocked_still_exits(self) -> None:
        """--dry-run still exits VERSION_BLOCKED when version is blocked."""
        with patch("sys.argv", ["agdt-setup", "--dry-run"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="block", target_version="99.0.0"),
                ):
                    with patch.object(commands, "_cleanup_stale_specialization_artifact") as mock_cleanup:
                        with patch("agentic_devtools.cli.setup.report.write_report", return_value=True) as mock_write:
                            with pytest.raises(SystemExit) as exc_info:
                                commands.setup_cmd()
        assert exc_info.value.code == 3  # VERSION_BLOCKED
        report = mock_write.call_args[0][0]
        assert report.mode == "dry-run"
        mock_cleanup.assert_not_called()

    def test_dry_run_does_not_call_stale_cleanup_helper(self) -> None:
        """Plain dry-run exits without touching specialization cleanup."""
        with patch("sys.argv", ["agdt-setup", "--dry-run"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch.object(commands, "_cleanup_stale_specialization_artifact") as mock_cleanup:
                                with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                    with pytest.raises(SystemExit):
                                        commands.setup_cmd()

        mock_cleanup.assert_not_called()

    def test_dry_run_standalone_refresh_does_not_call_stale_cleanup_helper(self) -> None:
        """Dry-run standalone refresh remains preview-only and skips cleanup."""
        with patch("sys.argv", ["agdt-setup", "--dry-run", "--refresh-issue-types"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "_cleanup_stale_specialization_artifact") as mock_cleanup:
                        with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                            with pytest.raises(SystemExit):
                                commands.setup_cmd()

        mock_cleanup.assert_not_called()

    def test_dry_run_internal_error_before_specialization_skips_stale_cleanup(self) -> None:
        """Dry-run internal errors before specialization do not trigger cleanup."""
        with patch("sys.argv", ["agdt-setup", "--dry-run"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    side_effect=RuntimeError("guard exploded"),
                ):
                    with patch.object(commands, "_cleanup_stale_specialization_artifact") as mock_cleanup:
                        with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                            with pytest.raises(SystemExit) as exc_info:
                                commands.setup_cmd()

        assert exc_info.value.code == 6
        mock_cleanup.assert_not_called()

    def test_dry_run_prints_would_messages_for_file_mods(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run prints 'would ...' messages for file modification sub-operations."""
        with patch("sys.argv", ["agdt-setup", "--dry-run"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        output = capsys.readouterr().out
        assert "would ensure .agdt/.gitignore" in output
        assert "would inject agent/prompt/skill files" in output
        assert "would generate setup scripts" in output

    def test_dry_run_no_git_root_shows_skipped_reason(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run with no git root shows 'skipped (no git root)' messages."""
        with patch("sys.argv", ["agdt-setup", "--dry-run"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=None):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        output = capsys.readouterr().out
        assert "skipped (no git root)" in output

    def test_dry_run_system_only_composability(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run --system-only skips cli installer messages."""
        with patch("sys.argv", ["agdt-setup", "--dry-run", "--system-only"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        output = capsys.readouterr().out
        # system_only means no installer messages
        assert "would install Copilot CLI" not in output
        assert "would install GitHub CLI" not in output
        assert "would persist environment variables" not in output

    def test_dry_run_no_persist_env_previews_manual_instructions(self) -> None:
        """--dry-run --no-persist-env routes through the manual-instructions preview path."""
        with patch("sys.argv", ["agdt-setup", "--dry-run", "--no-persist-env", "--npm"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with patch.object(commands, "_is_managed_bin_on_path", return_value=False):
                                    with patch.object(commands, "detect_shell_type", return_value="bash"):
                                        with patch.object(
                                            commands, "_print_manual_instructions"
                                        ) as mock_manual_instructions:
                                            with pytest.raises(SystemExit):
                                                commands.setup_cmd()
        mock_manual_instructions.assert_called_once()
        assert mock_manual_instructions.call_args.args[0] == Path.home() / ".agdt" / "npmrc"
        assert mock_manual_instructions.call_args.args[1] == Path.home() / ".agdt" / "certs" / "unified-ca-bundle.pem"

    def test_dry_run_upgrade_action_prints_would_upgrade(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run with version upgrade prints 'would upgrade' message."""
        with patch("sys.argv", ["agdt-setup", "--dry-run"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="upgrade", target_version="2.0.0"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        output = capsys.readouterr().out
        assert "would upgrade to version 2.0.0" in output

    def test_dry_run_skip_platform_detection(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run --skip-platform-detection omits platform detection message."""
        with patch("sys.argv", ["agdt-setup", "--dry-run", "--skip-platform-detection"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        output = capsys.readouterr().out
        assert "would detect and save platform configuration" not in output

    def test_dry_run_skip_templates(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run --skip-templates omits template generation messages."""
        with patch("sys.argv", ["agdt-setup", "--dry-run", "--skip-templates"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        output = capsys.readouterr().out
        assert "would generate workflow templates" not in output
        assert "would ensure commit template" not in output

    def test_dry_run_refresh_issue_types_prints_would_message(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run --refresh-issue-types prints 'would ...' without calling discover_issue_types."""
        with patch("sys.argv", ["agdt-setup", "--dry-run", "--refresh-issue-types"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                        with pytest.raises(SystemExit) as exc_info:
                            commands.setup_cmd()
        assert exc_info.value.code == 0
        output = capsys.readouterr().out
        assert "would refresh issue types" in output

    def test_dry_run_refresh_respects_skip_platform(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run --refresh-issue-types --skip-platform-detection previews suppression."""
        with patch(
            "sys.argv",
            ["agdt-setup", "--dry-run", "--refresh-issue-types", "--skip-platform-detection"],
        ):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                        with pytest.raises(SystemExit) as exc_info:
                            commands.setup_cmd()
        assert exc_info.value.code == 0
        output = capsys.readouterr().out
        assert "would refresh issue types — skipped (--skip-platform-detection)" in output

    def test_dry_run_refresh_issue_types_skips_when_no_git_root(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run --refresh-issue-types previews skip when no git root is available."""
        with patch("sys.argv", ["agdt-setup", "--dry-run", "--refresh-issue-types"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=None):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                        with pytest.raises(SystemExit) as exc_info:
                            commands.setup_cmd()
        assert exc_info.value.code == 0
        output = capsys.readouterr().out
        assert "would refresh issue types — skipped (no git root)" in output

    def test_dry_run_refresh_issue_types_skips_in_force_mode(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run --refresh-issue-types previews skip in --force-old-version mode."""
        with patch("sys.argv", ["agdt-setup", "--dry-run", "--refresh-issue-types"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="force"),
                ):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                        with pytest.raises(SystemExit) as exc_info:
                            commands.setup_cmd()
        assert exc_info.value.code == 0
        output = capsys.readouterr().out
        assert "would refresh issue types — skipped (--force-old-version)" in output

    def test_dry_run_refresh_previews_when_possible(self, capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
        """--dry-run --refresh-issue-types previews refresh when config is present."""
        config_file = tmp_path / ".github" / "agdt-config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text('{"platform": {"issue_adapter": "jira"}}', encoding="utf-8")

        with patch("sys.argv", ["agdt-setup", "--dry-run", "--refresh-issue-types"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                        with pytest.raises(SystemExit) as exc_info:
                            commands.setup_cmd()
        assert exc_info.value.code == 0
        output = capsys.readouterr().out
        assert "  ○ would refresh issue types" in output
        assert "skipped" not in output

    def test_dry_run_refresh_issue_types_does_not_call_discover(self) -> None:
        """--dry-run --refresh-issue-types does not call discover_issue_types."""
        with patch("sys.argv", ["agdt-setup", "--dry-run", "--refresh-issue-types"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="ok"),
                ):
                    with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                        with patch(
                            "agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types"
                        ) as mock_discover:
                            with pytest.raises(SystemExit):
                                commands.setup_cmd()
        mock_discover.assert_not_called()

    def test_dry_run_force_old_version_previews_repo_steps_as_skipped(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run + force mode marks repo-mutating previews as skipped."""
        with patch("sys.argv", ["agdt-setup", "--dry-run"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="force"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        output = capsys.readouterr().out
        assert "would ensure .agdt/.gitignore — skipped (--force-old-version)" in output
        assert "would pin agdt_version in project.json — skipped (--force-old-version)" in output

    def test_dry_run_force_old_version_with_system_only_skips_nested_repo_preview(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """--dry-run --system-only in force mode skips nested repo-preview details."""
        with patch("sys.argv", ["agdt-setup", "--dry-run", "--system-only"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="force"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        output = capsys.readouterr().out
        assert "would prompt project configuration — skipped (--force-old-version)" not in output
        assert "would pin agdt_version in project.json — skipped (--force-old-version)" in output

    def test_dry_run_force_old_version_respects_skip_flags_in_preview(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run force mode respects --skip-platform-detection and --skip-templates."""
        with patch("sys.argv", ["agdt-setup", "--dry-run", "--skip-platform-detection", "--skip-templates"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=Path("/fake/repo")):
                with patch(
                    "agentic_devtools.cli.setup.version_guard.check_version_guard",
                    return_value=VersionGuardResult(action="force"),
                ):
                    with patch.object(commands, "check_all_dependencies", return_value=_make_statuses(True)):
                        with patch.object(commands, "print_dependency_report"):
                            with patch("agentic_devtools.cli.setup.report.write_report", return_value=True):
                                with pytest.raises(SystemExit):
                                    commands.setup_cmd()
        output = capsys.readouterr().out
        assert "would detect and save platform configuration — skipped (--force-old-version)" not in output
        assert "would generate workflow templates — skipped (--force-old-version)" not in output


class TestSetupCopilotCliCmdDryRun:
    """Tests for setup_copilot_cli_cmd --dry-run."""

    def test_dry_run_no_mutations(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run prints would messages without mutations."""
        with patch("sys.argv", ["agdt-setup-copilot-cli", "--dry-run"]):
            commands.setup_copilot_cli_cmd()
        output = capsys.readouterr().out
        assert "would prefetch certificates" in output
        assert "would install Copilot CLI" in output
        assert "would persist environment variables" in output

    def test_dry_run_no_verify_ssl_not_set(self) -> None:
        """--dry-run --no-verify-ssl does not set AGDT_NO_VERIFY_SSL."""
        original = os.environ.get("AGDT_NO_VERIFY_SSL")
        with patch("sys.argv", ["agdt-setup-copilot-cli", "--dry-run", "--no-verify-ssl"]):
            commands.setup_copilot_cli_cmd()
        if original is None:
            assert "AGDT_NO_VERIFY_SSL" not in os.environ
        else:
            assert os.environ.get("AGDT_NO_VERIFY_SSL") == original


class TestSetupGhCliCmdDryRun:
    """Tests for setup_gh_cli_cmd --dry-run."""

    def test_dry_run_no_mutations(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run prints would messages without mutations."""
        with patch("sys.argv", ["agdt-setup-gh-cli", "--dry-run"]):
            commands.setup_gh_cli_cmd()
        output = capsys.readouterr().out
        assert "would prefetch certificates" in output
        assert "would install GitHub CLI" in output
        assert "would persist environment variables" in output

    def test_dry_run_no_verify_ssl_not_set(self) -> None:
        """--dry-run --no-verify-ssl does not set AGDT_NO_VERIFY_SSL."""
        original = os.environ.get("AGDT_NO_VERIFY_SSL")
        with patch("sys.argv", ["agdt-setup-gh-cli", "--dry-run", "--no-verify-ssl"]):
            commands.setup_gh_cli_cmd()
        if original is None:
            assert "AGDT_NO_VERIFY_SSL" not in os.environ
        else:
            assert os.environ.get("AGDT_NO_VERIFY_SSL") == original


class TestSetupCertsCmdDryRun:
    """Tests for setup_certs_cmd --dry-run."""

    def test_dry_run_no_mutations(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--dry-run prints would messages without mutations."""
        with patch("sys.argv", ["agdt-setup-certs", "--dry-run", "--no-npm"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=None):
                commands.setup_certs_cmd()
        output = capsys.readouterr().out
        assert "Refreshing CA certificate bundles..." not in output
        assert "Previewing CA certificate bundle refresh..." in output
        assert "would prefetch certificates" in output
        assert "would persist environment variables" in output

    def test_dry_run_no_verify_ssl_not_set(self) -> None:
        """--dry-run --no-verify-ssl does not set AGDT_NO_VERIFY_SSL."""
        original = os.environ.get("AGDT_NO_VERIFY_SSL")
        with patch("sys.argv", ["agdt-setup-certs", "--dry-run", "--no-verify-ssl", "--no-npm"]):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=None):
                commands.setup_certs_cmd()
        if original is None:
            assert "AGDT_NO_VERIFY_SSL" not in os.environ
        else:
            assert os.environ.get("AGDT_NO_VERIFY_SSL") == original

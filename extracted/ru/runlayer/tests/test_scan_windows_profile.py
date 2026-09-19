"""Windows profile scan SID plumbing."""

from __future__ import annotations

from unittest import mock

import pytest
import typer
from typer.testing import CliRunner

from runlayer_cli.commands import scan as scan_command
from runlayer_cli.scan.service import ScanResult

_SID = "S-1-5-21-1-2-3-1001"


def _empty_result() -> ScanResult:
    return ScanResult(
        device_id="device",
        hostname=None,
        os="windows",
        os_version=None,
        username="alice",
        org_device_id=None,
        scan_duration_ms=0,
        collector_version="test",
        configurations=[],
    )


def test_internal_scan_options_are_hidden() -> None:
    result = CliRunner().invoke(scan_command.app, ["--help"])

    assert result.exit_code == 0
    assert "--windows-user-sid" not in result.output
    assert "--windows-system-profile" not in result.output
    assert "--machine-scope" not in result.output
    assert "--no-machine-scope" not in result.output


def test_windows_user_sid_option_reaches_scan_runner(tmp_path) -> None:
    lock = mock.Mock()
    with (
        mock.patch.object(
            scan_command,
            "setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        mock.patch.object(scan_command, "acquire_scan_run_lock", return_value=lock),
        mock.patch.object(
            scan_command,
            "resolve_credentials",
            return_value={"secret": None, "host": None},
        ),
        mock.patch.object(scan_command, "_run_scan") as run_scan,
    ):
        result = CliRunner().invoke(
            scan_command.app,
            ["--dry-run", "--windows-user-sid", _SID],
        )

    assert result.exit_code == 0, result.output
    assert run_scan.call_args.kwargs["windows_user_sid"] == _SID


def test_windows_system_profile_option_reaches_scan_runner(tmp_path) -> None:
    lock = mock.Mock()
    with (
        mock.patch.object(
            scan_command,
            "setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        mock.patch.object(scan_command, "acquire_scan_run_lock", return_value=lock),
        mock.patch.object(
            scan_command,
            "resolve_credentials",
            return_value={"secret": None, "host": None},
        ),
        mock.patch.object(scan_command, "_run_scan") as run_scan,
    ):
        result = CliRunner().invoke(
            scan_command.app,
            [
                "--dry-run",
                "--windows-user-sid",
                _SID,
                "--windows-system-profile",
            ],
        )

    assert result.exit_code == 0, result.output
    assert run_scan.call_args.kwargs["windows_system_profile"] is True


@pytest.mark.parametrize(
    ("args", "expected"),
    [([], True), (["--no-machine-scope"], False)],
)
def test_machine_scope_option_reaches_scan_runner(
    tmp_path, args: list[str], expected: bool
) -> None:
    lock = mock.Mock()
    with (
        mock.patch.object(
            scan_command,
            "setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        mock.patch.object(scan_command, "acquire_scan_run_lock", return_value=lock),
        mock.patch.object(
            scan_command,
            "resolve_credentials",
            return_value={"secret": None, "host": None},
        ),
        mock.patch.object(scan_command, "_run_scan") as run_scan,
    ):
        result = CliRunner().invoke(scan_command.app, ["--dry-run", *args])

    assert result.exit_code == 0, result.output
    assert run_scan.call_args.kwargs["machine_scope"] is expected


def test_scan_runner_forwards_windows_user_sid_to_service() -> None:
    with mock.patch.object(
        scan_command,
        "scan_all_clients",
        return_value=_empty_result(),
    ) as scan_all_clients:
        with pytest.raises(typer.Exit) as exc_info:
            scan_command._run_scan(
                effective_host="",
                effective_secret="",
                device_id=None,
                org_device_id=None,
                dry_run=True,
                verbose=False,
                quiet=True,
                no_projects=True,
                project_depth=7,
                project_timeout=60,
                cpu_cores=2,
                max_cpu_percent=50,
                memory_limit_mb=1024,
                username="alice",
                detect_agents=False,
                detect_agent_frameworks=False,
                detect_processes=False,
                detect_containers=False,
                detect_disguised_skills=False,
                detect_renamed_plugin_caches=False,
                log_file_path="scan.log",
                windows_user_sid=_SID,
                windows_system_profile=True,
            )

    assert exc_info.value.exit_code == 0
    assert scan_all_clients.call_args.kwargs["windows_user_sid"] == _SID
    assert scan_all_clients.call_args.kwargs["windows_system_profile"] is True


def test_scan_runner_forwards_machine_scope_to_service() -> None:
    with mock.patch.object(
        scan_command,
        "scan_all_clients",
        return_value=_empty_result(),
    ) as scan_all_clients:
        with pytest.raises(typer.Exit):
            scan_command._run_scan(
                effective_host="",
                effective_secret="",
                device_id=None,
                org_device_id=None,
                dry_run=True,
                verbose=False,
                quiet=True,
                no_projects=True,
                project_depth=7,
                project_timeout=60,
                cpu_cores=2,
                max_cpu_percent=50,
                memory_limit_mb=1024,
                username="alice",
                detect_agents=False,
                detect_agent_frameworks=False,
                detect_processes=False,
                detect_containers=False,
                detect_disguised_skills=False,
                detect_renamed_plugin_caches=False,
                log_file_path="scan.log",
                machine_scope=False,
            )

    assert scan_all_clients.call_args.kwargs["machine_scope"] is False

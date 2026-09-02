"""Command-layer tests for packaged binary self-update."""

import os
from pathlib import Path
import subprocess
from typing import cast
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from runlayer_cli.commands.update_privilege import elevating_runner
from runlayer_cli.main import app as runlayer_app
from runlayer_cli.updater import InstallTarget, UpdateResult, UpdateStatus


runner = CliRunner()


@pytest.fixture(autouse=True)
def _installed_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("runlayer_cli.commands.update.installed_package", lambda: "cli")


def _updated() -> UpdateResult:
    return UpdateResult(
        status=UpdateStatus.UPDATED,
        from_version="1.0.0",
        to_version="2.0.0",
        artifact_filename="installer.pkg",
    )


def _scheduled() -> UpdateResult:
    return UpdateResult(
        status=UpdateStatus.SCHEDULED,
        from_version="1.0.0",
        to_version="2.0.0",
        artifact_filename="installer.msi",
    )


def test_source_install_fails_before_credential_resolution() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", False, create=True),
        patch("runlayer_cli.commands.update.resolve_credentials") as resolve,
        patch("runlayer_cli.commands.update._perform_update") as perform,
    ):
        result = runner.invoke(runlayer_app, ["update"])

    assert result.exit_code == 1
    assert "available only in the packaged binary" in result.output
    resolve.assert_not_called()
    perform.assert_not_called()


def test_print_result_rejects_unhandled_status() -> None:
    from runlayer_cli.commands.update import _print_result

    result = UpdateResult(
        status=cast(UpdateStatus, "future"),
        from_version="1.0.0",
    )

    with pytest.raises(AssertionError, match="Unhandled update status: future"):
        _print_result(result, product="Runlayer CLI")


def test_runlayer_update_requires_org_key() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch(
            "runlayer_cli.commands.update.resolve_credentials",
            return_value={
                "host": "https://tenant.runlayer.com",
                "secret": "rl_user_secret",
            },
        ),
        patch("runlayer_cli.commands.update._perform_update") as perform,
    ):
        result = runner.invoke(runlayer_app, ["update"])

    assert result.exit_code == 1
    assert "requires an organization API key" in result.output
    perform.assert_not_called()


def test_runlayer_update_applies_backend_target() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch(
            "runlayer_cli.commands.update.resolve_credentials",
            return_value={
                "host": "https://tenant.runlayer.com",
                "secret": "rl_org_secret",
            },
        ),
        patch(
            "runlayer_cli.commands.update._perform_update", return_value=_updated()
        ) as perform,
    ):
        result = runner.invoke(runlayer_app, ["update"])

    assert result.exit_code == 0
    assert "Updated Runlayer CLI from 1.0.0 to 2.0.0" in result.output
    perform.assert_called_once_with(
        package="cli",
        host="https://tenant.runlayer.com",
        org_api_key="rl_org_secret",
        allow_privileged_reexec=True,
        minimum_target_version=None,
    )


def test_runlayer_update_tracks_desktop_package_from_install_marker() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch("runlayer_cli.commands.update.installed_package", return_value="desktop"),
        patch(
            "runlayer_cli.commands.update.resolve_credentials",
            return_value={
                "host": "https://tenant.runlayer.com",
                "secret": "rl_org_secret",
            },
        ),
        patch(
            "runlayer_cli.commands.update._perform_update", return_value=_updated()
        ) as perform,
    ):
        result = runner.invoke(runlayer_app, ["update"])

    assert result.exit_code == 0
    assert "Updated Runlayer from 1.0.0 to 2.0.0" in result.output
    perform.assert_called_once_with(
        package="desktop",
        host="https://tenant.runlayer.com",
        org_api_key="rl_org_secret",
        allow_privileged_reexec=True,
        minimum_target_version=None,
    )


def test_runlayer_update_reports_windows_handoff_as_scheduled() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch(
            "runlayer_cli.commands.update.resolve_credentials",
            return_value={
                "host": "https://tenant.runlayer.com",
                "secret": "rl_org_secret",
            },
        ),
        patch(
            "runlayer_cli.commands.update._perform_update",
            return_value=_scheduled(),
        ),
    ):
        result = runner.invoke(runlayer_app, ["update"])

    assert result.exit_code == 0
    assert "Scheduled Runlayer CLI update from 1.0.0 to 2.0.0" in result.output
    assert "Updated Runlayer CLI" not in result.output


def test_scheduled_cli_update_requires_privileged_scheduler() -> None:
    with (
        patch.dict(os.environ, {"RUNLAYER_API_KEY": "rl_org_secret"}),
        patch(
            "runlayer_cli.commands.cli_update._is_privileged_scheduler",
            return_value=False,
        ),
        patch("runlayer_cli.commands.cli_update._run_or_exit") as run,
    ):
        result = runner.invoke(runlayer_app, ["__scheduled-update"])
        assert "RUNLAYER_API_KEY" not in os.environ

    assert result.exit_code == 1
    assert "privileged system scheduler" in result.output
    run.assert_not_called()


def test_scheduled_cli_update_is_quiet_when_mdm_auto_update_is_disabled() -> None:
    with (
        patch.dict(os.environ, {"RUNLAYER_API_KEY": "rl_org_secret"}),
        patch(
            "runlayer_cli.commands.cli_update._is_privileged_scheduler",
            return_value=True,
        ),
        patch(
            "runlayer_cli.commands.cli_update.platform.system", return_value="Darwin"
        ),
        patch(
            "runlayer_cli.commands.cli_update.read_managed_config",
            return_value={
                "host": "https://tenant.runlayer.com",
                "org_api_key": "rl_org_secret",
                "auto_update": False,
            },
        ),
        patch("runlayer_cli.commands.cli_update._run_or_exit") as run,
    ):
        result = runner.invoke(runlayer_app, ["__scheduled-update"])
        assert "RUNLAYER_API_KEY" not in os.environ

    assert result.exit_code == 0
    assert result.output == ""
    run.assert_not_called()


@pytest.mark.parametrize(
    "managed",
    (
        {},
        {"org_api_key": "rl_org_secret"},
        {"host": "https://tenant.runlayer.com"},
    ),
)
def test_scheduled_cli_update_is_quiet_without_complete_mdm_credentials(
    managed: dict[str, str],
) -> None:
    with (
        patch(
            "runlayer_cli.commands.cli_update._is_privileged_scheduler",
            return_value=True,
        ),
        patch(
            "runlayer_cli.commands.cli_update.platform.system", return_value="Darwin"
        ),
        patch(
            "runlayer_cli.commands.cli_update.read_managed_config",
            return_value=managed,
        ),
        patch("runlayer_cli.commands.cli_update._run_or_exit") as run,
    ):
        result = runner.invoke(runlayer_app, ["__scheduled-update"])

    assert result.exit_code == 0
    assert result.output == ""
    run.assert_not_called()


def test_scheduled_cli_update_applies_mdm_target_quietly() -> None:
    with (
        patch(
            "runlayer_cli.commands.cli_update._is_privileged_scheduler",
            return_value=True,
        ),
        patch(
            "runlayer_cli.commands.cli_update.platform.system", return_value="Darwin"
        ),
        patch(
            "runlayer_cli.commands.cli_update.read_managed_config",
            return_value={
                "host": "https://tenant.runlayer.com",
                "org_api_key": "rl_org_secret",
                "auto_update": True,
            },
        ),
        patch("runlayer_cli.commands.cli_update._run_or_exit") as run,
    ):
        result = runner.invoke(runlayer_app, ["__scheduled-update"])

    assert result.exit_code == 0
    assert result.output == ""
    run.assert_called_once_with(
        package="cli",
        product="Runlayer CLI",
        host="https://tenant.runlayer.com",
        org_api_key="rl_org_secret",
        quiet=True,
        allow_privileged_reexec=False,
        minimum_target_version="0.29.2",
    )


def test_scheduled_cli_update_uses_linux_credentials_env_and_floor() -> None:
    with (
        patch.dict(
            os.environ,
            {
                "RUNLAYER_HOST": "https://tenant.runlayer.com",
                "RUNLAYER_API_KEY": "rl_org_secret",
            },
        ),
        patch(
            "runlayer_cli.commands.cli_update._is_privileged_scheduler",
            return_value=True,
        ),
        patch("runlayer_cli.commands.cli_update.platform.system", return_value="Linux"),
        patch(
            "runlayer_cli.commands.cli_update.read_managed_config",
            return_value={},
        ),
        patch("runlayer_cli.commands.cli_update._run_or_exit") as run,
    ):
        result = runner.invoke(runlayer_app, ["__scheduled-update"])
        assert "RUNLAYER_API_KEY" not in os.environ

    assert result.exit_code == 0
    assert result.output == ""
    run.assert_called_once_with(
        package="cli",
        product="Runlayer CLI",
        host="https://tenant.runlayer.com",
        org_api_key="rl_org_secret",
        quiet=True,
        allow_privileged_reexec=False,
        minimum_target_version="0.30.8",
    )


def test_scheduled_cli_update_is_quiet_without_complete_linux_credentials() -> None:
    with (
        patch.dict(
            os.environ,
            {"RUNLAYER_HOST": "", "RUNLAYER_API_KEY": "rl_org_secret"},
        ),
        patch(
            "runlayer_cli.commands.cli_update._is_privileged_scheduler",
            return_value=True,
        ),
        patch("runlayer_cli.commands.cli_update.platform.system", return_value="Linux"),
        patch(
            "runlayer_cli.commands.cli_update.read_managed_config",
            return_value={},
        ),
        patch("runlayer_cli.commands.cli_update._run_or_exit") as run,
    ):
        result = runner.invoke(runlayer_app, ["__scheduled-update"])
        assert "RUNLAYER_API_KEY" not in os.environ

    assert result.exit_code == 0
    assert result.output == ""
    run.assert_not_called()


def test_scheduled_cli_update_ignores_credentials_env_off_linux() -> None:
    with (
        patch(
            "runlayer_cli.commands.cli_update._is_privileged_scheduler",
            return_value=True,
        ),
        patch(
            "runlayer_cli.commands.cli_update.platform.system", return_value="Darwin"
        ),
        patch(
            "runlayer_cli.commands.cli_update.read_managed_config",
            return_value={},
        ),
        patch("runlayer_cli.commands.cli_update._run_or_exit") as run,
    ):
        result = runner.invoke(
            runlayer_app,
            ["__scheduled-update"],
            env={
                "RUNLAYER_HOST": "https://tenant.runlayer.com",
                "RUNLAYER_API_KEY": "rl_org_secret",
            },
        )

    assert result.exit_code == 0
    assert result.output == ""
    run.assert_not_called()


def test_scheduled_update_tracks_desktop_package_from_install_marker() -> None:
    with (
        patch(
            "runlayer_cli.commands.cli_update._is_privileged_scheduler",
            return_value=True,
        ),
        patch(
            "runlayer_cli.commands.cli_update.platform.system", return_value="Darwin"
        ),
        patch(
            "runlayer_cli.commands.cli_update.read_managed_config",
            return_value={
                "host": "https://tenant.runlayer.com",
                "org_api_key": "rl_org_secret",
                "auto_update": True,
            },
        ),
        patch("runlayer_cli.commands.update.installed_package", return_value="desktop"),
        patch("runlayer_cli.commands.cli_update._run_or_exit") as run,
    ):
        result = runner.invoke(runlayer_app, ["__scheduled-update"])

    assert result.exit_code == 0
    run.assert_called_once_with(
        package="desktop",
        product="Runlayer",
        host="https://tenant.runlayer.com",
        org_api_key="rl_org_secret",
        quiet=True,
        allow_privileged_reexec=False,
        minimum_target_version="0.29.2",
    )


def test_runlayer_update_accepts_command_level_credentials() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch(
            "runlayer_cli.commands.update.resolve_credentials",
            return_value={
                "host": "https://tenant.runlayer.com",
                "secret": "rl_org_secret",
            },
        ) as resolve,
        patch("runlayer_cli.commands.update._perform_update", return_value=_updated()),
    ):
        result = runner.invoke(
            runlayer_app,
            [
                "update",
                "--secret",
                "rl_org_secret",
                "--host",
                "https://tenant.runlayer.com",
                "--org-api-key",
                "release",
            ],
            env={"RUNLAYER_API_KEY": "rl_user_secret"},
        )

    assert result.exit_code == 0
    command_ctx = resolve.call_args.args[0]
    assert command_ctx.obj == {
        "secret": "rl_org_secret",
        "host": "https://tenant.runlayer.com",
        "org_api_key_name": "release",
    }


def test_explicit_org_key_name_overrides_environment_secret() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch(
            "runlayer_cli.commands.update.resolve_credentials",
            return_value={
                "host": "https://tenant.runlayer.com",
                "secret": "rl_org_secret",
            },
        ) as resolve,
        patch("runlayer_cli.commands.update._perform_update", return_value=_updated()),
    ):
        result = runner.invoke(
            runlayer_app,
            ["update", "--org-api-key", "release"],
            env={"RUNLAYER_API_KEY": "rl_user_secret"},
        )

    assert result.exit_code == 0
    command_ctx = resolve.call_args.args[0]
    assert command_ctx.obj["secret"] is None
    assert command_ctx.obj["org_api_key_name"] == "release"


def test_global_explicit_org_key_name_overrides_command_environment_secret() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch(
            "runlayer_cli.commands.update.resolve_credentials",
            return_value={
                "host": "https://tenant.runlayer.com",
                "secret": "rl_org_secret",
            },
        ) as resolve,
        patch("runlayer_cli.commands.update._perform_update", return_value=_updated()),
    ):
        result = runner.invoke(
            runlayer_app,
            ["--org-api-key", "release", "update"],
            env={"RUNLAYER_API_KEY": "rl_user_secret"},
        )

    assert result.exit_code == 0
    command_ctx = resolve.call_args.args[0]
    assert command_ctx.obj["secret"] is None
    assert command_ctx.obj["org_api_key_name"] == "release"


def test_global_explicit_host_overrides_command_environment_host() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch(
            "runlayer_cli.commands.update.resolve_credentials",
            return_value={
                "host": "https://new.runlayer.com",
                "secret": "rl_org_secret",
            },
        ) as resolve,
        patch("runlayer_cli.commands.update._perform_update", return_value=_updated()),
    ):
        result = runner.invoke(
            runlayer_app,
            [
                "--host",
                "https://new.runlayer.com",
                "update",
                "--org-api-key",
                "release",
            ],
            env={"RUNLAYER_HOST": "https://stale.runlayer.com"},
        )

    assert result.exit_code == 0
    command_ctx = resolve.call_args.args[0]
    assert command_ctx.obj["host"] == "https://new.runlayer.com"


def test_environment_host_is_kept_without_an_explicit_host() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch(
            "runlayer_cli.commands.update.resolve_credentials",
            return_value={
                "host": "https://environment.runlayer.com",
                "secret": "rl_org_secret",
            },
        ) as resolve,
        patch("runlayer_cli.commands.update._perform_update", return_value=_updated()),
    ):
        result = runner.invoke(
            runlayer_app,
            ["update", "--org-api-key", "release"],
            env={"RUNLAYER_HOST": "https://environment.runlayer.com"},
        )

    assert result.exit_code == 0
    command_ctx = resolve.call_args.args[0]
    assert command_ctx.obj["host"] == "https://environment.runlayer.com"


def test_environment_org_key_name_does_not_override_environment_secret() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch(
            "runlayer_cli.commands.update.resolve_credentials",
            return_value={
                "host": "https://tenant.runlayer.com",
                "secret": "rl_org_secret",
            },
        ) as resolve,
        patch("runlayer_cli.commands.update._perform_update", return_value=_updated()),
    ):
        result = runner.invoke(
            runlayer_app,
            ["update"],
            env={
                "RUNLAYER_API_KEY": "rl_user_secret",
                "RUNLAYER_ORG_API_KEY_NAME": "release",
            },
        )

    assert result.exit_code == 0
    command_ctx = resolve.call_args.args[0]
    assert command_ctx.obj["secret"] == "rl_user_secret"
    assert command_ctx.obj["org_api_key_name"] == "release"


def test_update_command_reports_failure_without_traceback() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch(
            "runlayer_cli.commands.update.resolve_credentials",
            return_value={
                "host": "https://tenant.runlayer.com",
                "secret": "rl_org_secret",
            },
        ),
        patch(
            "runlayer_cli.commands.update._perform_update",
            side_effect=RuntimeError("signature rejected"),
        ),
    ):
        result = runner.invoke(runlayer_app, ["update"])

    assert result.exit_code == 1
    assert "Update failed: signature rejected" in result.output
    assert "Traceback" not in result.output


def test_update_suppresses_exit_metrics_before_installer_can_replace_bundle() -> None:
    from runlayer_cli.commands.update import _run_or_exit

    call_order: list[str] = []

    def perform(**_: object) -> UpdateResult:
        call_order.append("install")
        return _updated()

    with (
        patch(
            "runlayer_cli.command_metrics.suppress_current_command_metrics",
            side_effect=lambda: call_order.append("suppress"),
        ),
        patch(
            "runlayer_cli.commands.update._perform_update",
            side_effect=perform,
        ),
    ):
        _run_or_exit(
            package="cli",
            product="Runlayer CLI",
            host="https://tenant.runlayer.com",
            org_api_key="rl_org_secret",
            quiet=True,
        )

    assert call_order == ["suppress", "install"]


def test_perform_update_activates_windows_handoff_installer() -> None:
    from runlayer_cli.commands.update import __version__, _perform_update

    target = InstallTarget("windows", "x64", "msi")
    expected = _updated()
    marker_path = Path(
        r"C:\Program Files\Runlayer\UpdateStaging\aiwatch-update-outcome.json"
    )

    with (
        patch(
            "runlayer_cli.commands.update.native_install_target",
            return_value=target,
        ),
        patch(
            "runlayer_cli.commands.update._is_windows_elevated",
            return_value=True,
        ),
        patch(
            "runlayer_cli.commands.update.NativePlatformInstaller"
        ) as installer_class,
        patch(
            "runlayer_cli.commands.update.check_and_update",
            return_value=expected,
        ) as check,
    ):
        installer_class.return_value.outcome_marker_path = marker_path
        result = _perform_update(
            package="ai-watch",
            host="https://tenant.runlayer.com",
            org_api_key="rl_org_secret",
            allow_privileged_reexec=False,
        )

    assert result is expected
    installer_class.assert_called_once_with(
        "ai-watch",
        target=target,
        runner=elevating_runner,
    )
    check.assert_called_once_with(
        package="ai-watch",
        installed_version=__version__,
        host="https://tenant.runlayer.com",
        org_api_key="rl_org_secret",
        installer=installer_class.return_value,
        install_target=target,
        minimum_target_version=None,
        outcome_marker_path=marker_path,
    )


def test_perform_update_requires_elevated_windows_console() -> None:
    from runlayer_cli.commands.update import _perform_update

    with (
        patch(
            "runlayer_cli.commands.update.native_install_target",
            return_value=InstallTarget("windows", "x64", "msi"),
        ),
        patch(
            "runlayer_cli.commands.update._is_windows_elevated",
            return_value=False,
        ),
        patch("runlayer_cli.commands.update.NativePlatformInstaller") as installer,
        pytest.raises(RuntimeError, match="elevated administrator console"),
    ):
        _perform_update(
            package="cli",
            host="https://tenant.runlayer.com",
            org_api_key="rl_org_secret",
        )

    installer.assert_not_called()


def test_perform_update_activates_linux_native_installer() -> None:
    from runlayer_cli.commands.update import __version__, _perform_update

    target = InstallTarget("linux", "x86_64", "deb")
    expected = _updated()

    with (
        patch(
            "runlayer_cli.commands.update.native_install_target",
            return_value=target,
        ),
        patch("runlayer_cli.commands.update.os.geteuid", return_value=0),
        patch(
            "runlayer_cli.commands.update.configure_privileged_temp_root"
        ) as configure_temp,
        patch(
            "runlayer_cli.commands.update.NativePlatformInstaller"
        ) as installer_class,
        patch(
            "runlayer_cli.commands.update.check_and_update",
            return_value=expected,
        ) as check,
    ):
        installer_class.return_value.outcome_marker_path = None
        result = _perform_update(
            package="ai-watch",
            host="https://tenant.runlayer.com",
            org_api_key="rl_org_secret",
        )

    assert result is expected
    configure_temp.assert_called_once_with()
    installer_class.assert_called_once_with(
        "ai-watch",
        target=target,
        runner=elevating_runner,
    )
    check.assert_called_once_with(
        package="ai-watch",
        installed_version=__version__,
        host="https://tenant.runlayer.com",
        org_api_key="rl_org_secret",
        installer=installer_class.return_value,
        install_target=target,
        minimum_target_version=None,
        outcome_marker_path=None,
    )


def test_perform_update_wires_installed_variant_into_target() -> None:
    from runlayer_cli.commands.update import __version__, _perform_update

    expected = _updated()

    with (
        patch(
            "runlayer_cli.commands.update.native_install_target",
            return_value=InstallTarget("linux", "x86_64", "deb"),
        ),
        patch(
            "runlayer_cli.commands.update.installed_variant",
            return_value="glibc2.17",
        ) as read_variant,
        patch("runlayer_cli.commands.update.os.geteuid", return_value=0),
        patch("runlayer_cli.commands.update.configure_privileged_temp_root"),
        patch(
            "runlayer_cli.commands.update.NativePlatformInstaller"
        ) as installer_class,
        patch(
            "runlayer_cli.commands.update.check_and_update",
            return_value=expected,
        ) as check,
    ):
        installer_class.return_value.outcome_marker_path = None
        result = _perform_update(
            package="cli",
            host="https://tenant.runlayer.com",
            org_api_key="rl_org_secret",
        )

    variant_target = InstallTarget("linux", "x86_64", "deb", variant="glibc2.17")
    assert result is expected
    read_variant.assert_called_once_with("cli")
    installer_class.assert_called_once_with(
        "cli",
        target=variant_target,
        runner=elevating_runner,
    )
    check.assert_called_once_with(
        package="cli",
        installed_version=__version__,
        host="https://tenant.runlayer.com",
        org_api_key="rl_org_secret",
        installer=installer_class.return_value,
        install_target=variant_target,
        minimum_target_version=None,
        outcome_marker_path=None,
    )


def test_corrupt_variant_marker_fails_update_without_traceback() -> None:
    with (
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch(
            "runlayer_cli.commands.update.resolve_credentials",
            return_value={
                "host": "https://tenant.runlayer.com",
                "secret": "rl_org_secret",
            },
        ),
        patch(
            "runlayer_cli.commands.update.native_install_target",
            return_value=InstallTarget("linux", "x86_64", "deb"),
        ),
        patch(
            "runlayer_cli.commands.update.installed_variant",
            side_effect=RuntimeError("Installed Runlayer variant marker is invalid"),
        ),
        patch("runlayer_cli.commands.update.run_privileged_update") as reexec,
        patch("runlayer_cli.commands.update.check_and_update") as check,
    ):
        result = runner.invoke(runlayer_app, ["update"])

    assert result.exit_code == 1
    assert "Update failed: Installed Runlayer variant marker is invalid" in (
        result.output
    )
    assert "Traceback" not in result.output
    reexec.assert_not_called()
    check.assert_not_called()


def test_frozen_nonroot_reexecs_whole_update_as_root() -> None:
    from runlayer_cli.commands.update import _perform_update

    completed = subprocess.CompletedProcess([], 0, stdout="", stderr="")
    with (
        patch(
            "runlayer_cli.commands.update.native_install_target",
            return_value=InstallTarget("macos", "arm64", "pkg"),
        ),
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch("runlayer_cli.commands.update.os.geteuid", return_value=501),
        patch(
            "runlayer_cli.commands.update_privilege._trusted_installed_executable",
            return_value=Path("/usr/local/bin/runlayer"),
        ),
        patch(
            "runlayer_cli.commands.update_privilege.subprocess.run",
            return_value=completed,
        ) as run,
        patch("runlayer_cli.commands.update.check_and_update") as check,
        patch.dict(
            os.environ,
            {
                "RUNLAYER_CA_BUNDLE": "",
                "SSL_CERT_FILE": "/tmp/caller-ca.pem",
                "SSL_CERT_DIR": "/tmp/caller-ca-dir",
            },
            clear=False,
        ),
    ):
        result = _perform_update(
            package="cli",
            host="https://tenant.runlayer.com",
            org_api_key="rl_org_secret",
        )

    assert result is None
    argv = run.call_args.args[0]
    assert argv[-2:] == ["__self-update-root", "cli"]
    assert "rl_org_secret" not in argv
    assert argv[:3] == [
        "/usr/bin/sudo",
        (
            "--preserve-env=RUNLAYER_SELF_UPDATE_HOST,"
            "RUNLAYER_SELF_UPDATE_ORG_KEY,RUNLAYER_SELF_UPDATE_CA_BUNDLE,"
            "RUNLAYER_SELF_UPDATE_CA_DIR"
        ),
        "--",
    ]
    env = run.call_args.kwargs["env"]
    assert env["RUNLAYER_SELF_UPDATE_HOST"] == "https://tenant.runlayer.com"
    assert env["RUNLAYER_SELF_UPDATE_ORG_KEY"] == "rl_org_secret"
    assert env["RUNLAYER_SELF_UPDATE_CA_BUNDLE"] == "/tmp/caller-ca.pem"
    assert env["RUNLAYER_SELF_UPDATE_CA_DIR"] == "/tmp/caller-ca-dir"
    check.assert_not_called()


def test_frozen_nonroot_linux_reexecs_whole_update_as_root() -> None:
    from runlayer_cli.commands.update import _perform_update

    with (
        patch(
            "runlayer_cli.commands.update.native_install_target",
            return_value=InstallTarget("linux", "x86_64", "deb"),
        ),
        patch("runlayer_cli.commands.update.sys.frozen", True, create=True),
        patch("runlayer_cli.commands.update.os.geteuid", return_value=501),
        patch(
            "runlayer_cli.commands.update.run_privileged_update"
        ) as privileged_update,
        patch("runlayer_cli.commands.update.check_and_update") as check,
    ):
        result = _perform_update(
            package="cli",
            host="https://tenant.runlayer.com",
            org_api_key="rl_org_secret",
        )

    assert result is None
    privileged_update.assert_called_once_with(
        package="cli",
        platform="linux",
        host="https://tenant.runlayer.com",
        org_api_key="rl_org_secret",
        ca_bundle=None,
        ca_bundle_dir=None,
    )
    check.assert_not_called()


def test_privileged_continuation_scrubs_secret_environment() -> None:
    privileged_env = {
        "RUNLAYER_SELF_UPDATE_HOST": "https://tenant.runlayer.com",
        "RUNLAYER_SELF_UPDATE_ORG_KEY": "rl_org_secret",
        "RUNLAYER_SELF_UPDATE_CA_BUNDLE": "/tmp/caller-ca.pem",
        "RUNLAYER_SELF_UPDATE_CA_DIR": "/tmp/caller-ca-dir",
        "RUNLAYER_API_KEY": "rl_org_standard",
        "RUNLAYER_CA_BUNDLE": "/tmp/stale-ca.pem",
        "SSL_CERT_FILE": "/tmp/stale-ssl-ca.pem",
        "SSL_CERT_DIR": "/tmp/stale-ssl-dir",
        "REQUESTS_CA_BUNDLE": "/tmp/stale-requests-ca.pem",
    }

    def perform_after_scrub(**_: object) -> UpdateResult:
        assert "RUNLAYER_SELF_UPDATE_HOST" not in os.environ
        assert "RUNLAYER_SELF_UPDATE_ORG_KEY" not in os.environ
        assert "RUNLAYER_SELF_UPDATE_CA_BUNDLE" not in os.environ
        assert "RUNLAYER_SELF_UPDATE_CA_DIR" not in os.environ
        assert "RUNLAYER_API_KEY" not in os.environ
        assert os.environ["RUNLAYER_CA_BUNDLE"] == "/tmp/caller-ca.pem"
        assert "SSL_CERT_FILE" not in os.environ
        assert os.environ["SSL_CERT_DIR"] == "/tmp/caller-ca-dir"
        assert "REQUESTS_CA_BUNDLE" not in os.environ
        return _updated()

    with (
        patch.dict(os.environ, privileged_env, clear=False),
        patch("runlayer_cli.commands.update.os.geteuid", return_value=0),
        patch(
            "runlayer_cli.commands.update._perform_update",
            side_effect=perform_after_scrub,
        ) as perform,
    ):
        result = runner.invoke(runlayer_app, ["__self-update-root", "cli"])

    assert result.exit_code == 0
    assert "Updated Runlayer CLI from 1.0.0 to 2.0.0" in result.output
    perform.assert_called_once_with(
        package="cli",
        host="https://tenant.runlayer.com",
        org_api_key="rl_org_secret",
        allow_privileged_reexec=False,
        minimum_target_version=None,
    )


def test_privileged_continuation_rejects_unwired_ai_watch_entrypoint() -> None:
    privileged_env = {
        "RUNLAYER_SELF_UPDATE_HOST": "https://tenant.runlayer.com",
        "RUNLAYER_SELF_UPDATE_ORG_KEY": "rl_org_secret",
    }
    with (
        patch.dict(os.environ, privileged_env, clear=False),
        patch("runlayer_cli.commands.update.os.geteuid", return_value=0),
        patch("runlayer_cli.commands.update._perform_update") as perform,
    ):
        result = runner.invoke(runlayer_app, ["__self-update-root", "ai-watch"])

    assert result.exit_code == 1
    assert "unsupported context" in result.output
    perform.assert_not_called()


def test_privileged_continuation_clears_generic_tls_without_handoff() -> None:
    privileged_env = {
        "RUNLAYER_SELF_UPDATE_HOST": "https://tenant.runlayer.com",
        "RUNLAYER_SELF_UPDATE_ORG_KEY": "rl_org_secret",
        "RUNLAYER_CA_BUNDLE": "/tmp/stale-runlayer-ca.pem",
        "SSL_CERT_FILE": "/tmp/stale-ssl-ca.pem",
        "SSL_CERT_DIR": "/tmp/stale-ssl-dir",
        "REQUESTS_CA_BUNDLE": "/tmp/stale-requests-ca.pem",
    }

    def perform_after_scrub(**_: object) -> UpdateResult:
        for name in (
            "RUNLAYER_CA_BUNDLE",
            "SSL_CERT_FILE",
            "SSL_CERT_DIR",
            "REQUESTS_CA_BUNDLE",
        ):
            assert name not in os.environ
        return _updated()

    with (
        patch.dict(os.environ, privileged_env, clear=False),
        patch("runlayer_cli.commands.update.os.geteuid", return_value=0),
        patch(
            "runlayer_cli.commands.update._perform_update",
            side_effect=perform_after_scrub,
        ) as perform,
    ):
        result = runner.invoke(runlayer_app, ["__self-update-root", "cli"])

    assert result.exit_code == 0
    perform.assert_called_once()

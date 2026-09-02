"""Managed AI Watch self-update command tests."""

from collections.abc import Iterator
import os
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from runlayer_cli.aiwatch import app as aiwatch_app
from runlayer_cli.scan import windows_users
from runlayer_cli.updater import UpdateResult, UpdateStatus


runner = CliRunner()


@pytest.fixture(autouse=True)
def _run_as_root_scheduler(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.delenv("RUNLAYER_API_KEY", raising=False)
    monkeypatch.delenv("RUNLAYER_HOST", raising=False)
    with patch("runlayer_cli.commands.update_scheduler.os.geteuid", return_value=0):
        yield


def _updated() -> UpdateResult:
    return UpdateResult(
        status=UpdateStatus.UPDATED,
        from_version="1.0.0",
        to_version="2.0.0",
        artifact_filename="installer.pkg",
    )


def test_aiwatch_self_update_uses_managed_host_and_org_key() -> None:
    managed = {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
    }
    with (
        patch(
            "runlayer_cli.commands.aiwatch_update.read_managed_config",
            return_value=managed,
        ),
        patch(
            "runlayer_cli.commands.update._perform_update", return_value=_updated()
        ) as perform,
    ):
        result = runner.invoke(aiwatch_app, ["self-update"])

    assert result.exit_code == 0
    assert result.output == ""
    perform.assert_called_once_with(
        package="ai-watch",
        host="https://tenant.runlayer.com",
        org_api_key="rl_org_secret",
        allow_privileged_reexec=False,
        minimum_target_version=None,
    )


def test_aiwatch_self_update_accepts_windows_system_task() -> None:
    managed = {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
    }
    with (
        patch("runlayer_cli.commands.update_scheduler.sys.platform", "win32"),
        patch(
            "runlayer_cli.commands.update_scheduler.os.geteuid",
            None,
        ),
        patch.object(windows_users, "is_running_as_system", return_value=True),
        patch(
            "runlayer_cli.commands.aiwatch_update.read_managed_config",
            return_value=managed,
        ),
        patch(
            "runlayer_cli.commands.update._perform_update",
            return_value=_updated(),
        ) as perform,
    ):
        result = runner.invoke(aiwatch_app, ["self-update"])

    assert result.exit_code == 0
    assert result.output == ""
    perform.assert_called_once_with(
        package="ai-watch",
        host="https://tenant.runlayer.com",
        org_api_key="rl_org_secret",
        allow_privileged_reexec=False,
        minimum_target_version=None,
    )


@pytest.mark.parametrize(
    "status",
    [UpdateStatus.NO_TARGET, UpdateStatus.UP_TO_DATE, UpdateStatus.SCHEDULED],
)
def test_aiwatch_self_update_keeps_non_install_results_quiet(
    status: UpdateStatus,
) -> None:
    managed = {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
    }
    with (
        patch(
            "runlayer_cli.commands.aiwatch_update.read_managed_config",
            return_value=managed,
        ),
        patch(
            "runlayer_cli.commands.update._perform_update",
            return_value=UpdateResult(status=status, from_version="1.0.0"),
        ),
    ):
        result = runner.invoke(aiwatch_app, ["self-update"])

    assert result.exit_code == 0
    assert result.output == ""


def test_aiwatch_self_update_reports_failure_for_launchd_retry() -> None:
    managed = {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
    }
    with (
        patch(
            "runlayer_cli.commands.aiwatch_update.read_managed_config",
            return_value=managed,
        ),
        patch(
            "runlayer_cli.commands.update._perform_update",
            side_effect=RuntimeError("network unavailable"),
        ),
    ):
        result = runner.invoke(aiwatch_app, ["self-update"])

    assert result.exit_code == 1
    assert "Update failed: network unavailable" in result.output


def test_aiwatch_self_update_honors_managed_opt_out() -> None:
    with (
        patch.dict(os.environ, {"RUNLAYER_API_KEY": "rl_org_secret"}),
        patch(
            "runlayer_cli.commands.aiwatch_update.read_managed_config",
            return_value={"auto_update": False},
        ),
        patch("runlayer_cli.commands.update._perform_update") as perform,
    ):
        result = runner.invoke(aiwatch_app, ["self-update"])
        assert "RUNLAYER_API_KEY" not in os.environ

    assert result.exit_code == 0
    assert result.output == ""
    perform.assert_not_called()


def test_aiwatch_self_update_silently_skips_unconfigured_fleet() -> None:
    with (
        patch.dict(os.environ, {"RUNLAYER_API_KEY": "rl_org_secret"}),
        patch(
            "runlayer_cli.commands.aiwatch_update.read_managed_config", return_value={}
        ),
        patch("runlayer_cli.commands.update._perform_update") as perform,
    ):
        result = runner.invoke(aiwatch_app, ["self-update"])
        assert "RUNLAYER_API_KEY" not in os.environ

    assert result.exit_code == 0
    assert result.output == ""
    perform.assert_not_called()


def test_aiwatch_self_update_rejects_non_root_before_reading_credentials() -> None:
    with (
        patch.dict(os.environ, {"RUNLAYER_API_KEY": "rl_org_secret"}),
        patch("runlayer_cli.commands.update_scheduler.os.geteuid", return_value=501),
        patch(
            "runlayer_cli.commands.aiwatch_update.read_managed_config"
        ) as read_config,
        patch("runlayer_cli.commands.update._perform_update") as perform,
    ):
        result = runner.invoke(aiwatch_app, ["self-update"])
    assert "RUNLAYER_API_KEY" not in os.environ

    assert result.exit_code == 1
    assert "privileged system scheduler" in result.output
    read_config.assert_not_called()
    perform.assert_not_called()


def test_aiwatch_self_update_rejects_non_system_windows_task() -> None:
    with (
        patch.dict(os.environ, {"RUNLAYER_API_KEY": "rl_org_secret"}),
        patch("runlayer_cli.commands.update_scheduler.sys.platform", "win32"),
        patch.object(windows_users, "is_running_as_system", return_value=False),
        patch(
            "runlayer_cli.commands.aiwatch_update.read_managed_config"
        ) as read_config,
        patch("runlayer_cli.commands.update._perform_update") as perform,
    ):
        result = runner.invoke(aiwatch_app, ["self-update"])
        assert "RUNLAYER_API_KEY" not in os.environ

    assert result.exit_code == 1
    assert "privileged system scheduler" in result.output
    read_config.assert_not_called()
    perform.assert_not_called()

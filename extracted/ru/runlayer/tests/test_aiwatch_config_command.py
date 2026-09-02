"""AI Watch config and scheduler trigger command tests."""

import builtins
import ctypes
import json
from pathlib import Path
import subprocess
from unittest.mock import MagicMock, patch

from click import Group
import pytest
import typer
from typer.testing import CliRunner

from runlayer_cli import aiwatch_config_cache, mdm_config
from runlayer_cli.aiwatch import app as aiwatch_app
from runlayer_cli.commands.aiwatch_setup import app as aiwatch_setup_app
from runlayer_cli.mdm_config import AIWatchMode


runner = CliRunner()


def test_managed_config_secret_fields_cover_sensitive_names() -> None:
    sensitive_name_parts = ("key", "secret", "token", "password")
    declared_fields = set(mdm_config.ManagedConfig.__annotations__)
    conventionally_sensitive_fields = {
        field
        for field in declared_fields
        if any(part in field.lower() for part in sensitive_name_parts)
    }

    assert conventionally_sensitive_fields <= mdm_config.SECRET_FIELDS
    assert mdm_config.SECRET_FIELDS <= declared_fields


def _listed_commands(app: typer.Typer) -> set[str]:
    command = typer.main.get_command(app)
    assert isinstance(command, Group)
    return {
        name for name, subcommand in command.commands.items() if not subcommand.hidden
    }


def test_aiwatch_help_lists_only_operator_commands() -> None:
    result = runner.invoke(aiwatch_app, ["--help"])

    assert result.exit_code == 0
    assert _listed_commands(aiwatch_app) == {
        "config",
        "scan",
        "setup",
        "update-now",
    }


@pytest.mark.parametrize(
    ("args", "expected_text"),
    [
        ([], "Commands"),
        (["setup"], "hooks"),
        (["config"], "show"),
    ],
)
def test_aiwatch_groups_show_help_by_default(
    args: list[str], expected_text: str
) -> None:
    result = runner.invoke(aiwatch_app, args)

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert expected_text in result.output
    assert "Missing command" not in result.output


def test_aiwatch_root_help_does_not_import_click_directly() -> None:
    original_import = builtins.__import__

    def reject_click_import(
        name: str,
        globals=None,
        locals=None,
        fromlist=(),
        level: int = 0,
    ):
        if (
            name == "click"
            and globals
            and globals.get("__name__") == "runlayer_cli.aiwatch"
        ):
            raise ModuleNotFoundError("No module named 'click'")
        return original_import(name, globals, locals, fromlist, level)

    with patch("builtins.__import__", side_effect=reject_click_import):
        result = runner.invoke(aiwatch_app, [])

    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_aiwatch_setup_help_hides_test_device_config() -> None:
    result = runner.invoke(aiwatch_app, ["setup", "--help"])

    assert result.exit_code == 0
    assert _listed_commands(aiwatch_setup_app) == {"hooks"}


@pytest.mark.parametrize(
    "command",
    [
        ("login",),
        ("logout",),
        ("logs",),
        ("enroll",),
        ("bootstrap",),
        ("self-update",),
        ("org-api-key",),
        ("setup", "config"),
    ],
)
def test_hidden_aiwatch_commands_remain_invocable(command: tuple[str, ...]) -> None:
    result = runner.invoke(aiwatch_app, [*command, "--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_config_show_json_redacts_all_managed_secrets() -> None:
    managed = {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_12345678",
        "enrollment_key": "enroll_abcdefgh",
        "skill_sync_org_api_key": "rl_org_skills_wxyz",
        "mode": AIWatchMode.PROTECT,
        "sessions": True,
    }
    with patch(
        "runlayer_cli.mdm_config.read_managed_config",
        return_value=managed,
    ):
        result = runner.invoke(aiwatch_app, ["config", "show", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["config"] == {
        "enrollment_key": "****efgh",
        "host": "https://tenant.runlayer.com",
        "mode": "protect",
        "org_api_key": "****5678",
        "sessions": True,
        "skill_sync_org_api_key": "****wxyz",
    }
    assert "rl_org_12345678" not in result.output
    assert "enroll_abcdefgh" not in result.output
    assert "rl_org_skills_wxyz" not in result.output


def test_config_show_text_redacts_secrets_and_reports_cache_status() -> None:
    managed = {
        "org_api_key": "rl_org_12345678",
        "enrollment_key": "enroll_abcdefgh",
        "mode": AIWatchMode.PROTECT,
    }
    with (
        patch(
            "runlayer_cli.mdm_config.read_managed_config",
            return_value=managed,
        ),
        patch("platform.system", return_value="FreeBSD"),
    ):
        result = runner.invoke(aiwatch_app, ["config", "show"])

    assert result.exit_code == 0
    assert "org_api_key: ****5678" in result.output
    assert "enrollment_key: ****efgh" in result.output
    assert "mode: protect" in result.output
    assert "status: unsupported" in result.output
    assert "rl_org_12345678" not in result.output
    assert "enroll_abcdefgh" not in result.output


def test_config_show_works_without_managed_config() -> None:
    with (
        patch("runlayer_cli.mdm_config.read_managed_config", return_value={}),
        patch("platform.system", return_value="FreeBSD"),
    ):
        result = runner.invoke(aiwatch_app, ["config", "show", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.output) == {
        "backend_cache": {
            "location": None,
            "modified_at": None,
            "status": "unsupported",
        },
        "config": {},
    }


def test_config_show_reports_missing_linux_backend_cache(tmp_path: Path) -> None:
    cache_path = tmp_path / "backend-config.json"
    with (
        patch("runlayer_cli.mdm_config.read_managed_config", return_value={}),
        patch("platform.system", return_value="Linux"),
        patch.object(aiwatch_config_cache, "LINUX_CACHE_PATH", cache_path),
    ):
        result = runner.invoke(aiwatch_app, ["config", "show", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.output)["backend_cache"] == {
        "location": str(cache_path),
        "modified_at": None,
        "status": "missing",
    }


def test_config_show_reports_valid_macos_backend_cache(
    tmp_path: Path,
) -> None:
    cache_path = tmp_path / "backend-config.json"
    cache_path.write_text("{}", encoding="utf-8")
    with (
        patch(
            "runlayer_cli.mdm_config.read_managed_config",
            return_value={"org_api_key": "rl_org_12345678"},
        ),
        patch("platform.system", return_value="Darwin"),
        patch.object(aiwatch_config_cache, "MACOS_CACHE_PATH", cache_path),
        patch.object(aiwatch_config_cache, "read_backend_config", return_value={}),
    ):
        result = runner.invoke(aiwatch_app, ["config", "show", "--json"])

    assert result.exit_code == 0
    cache_status = json.loads(result.output)["backend_cache"]
    assert cache_status["status"] == "valid"
    assert cache_status["location"] == str(cache_path)
    assert cache_status["modified_at"] is not None


def test_config_show_reports_rejected_macos_backend_cache(tmp_path: Path) -> None:
    cache_path = tmp_path / "backend-config.json"
    cache_path.write_text("{}", encoding="utf-8")
    with (
        patch(
            "runlayer_cli.mdm_config.read_managed_config",
            return_value={"org_api_key": "rl_org_12345678"},
        ),
        patch("platform.system", return_value="Darwin"),
        patch.object(aiwatch_config_cache, "MACOS_CACHE_PATH", cache_path),
        patch.object(aiwatch_config_cache, "read_backend_config", return_value=None),
    ):
        result = runner.invoke(aiwatch_app, ["config", "show", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.output)["backend_cache"]["status"] == "rejected"


def test_config_show_reports_valid_linux_backend_cache_via_env_key(
    tmp_path: Path, monkeypatch
) -> None:
    cache_path = tmp_path / "backend-config.json"
    cache_path.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("RUNLAYER_API_KEY", "rl_org_env")
    seen: list[str] = []

    def fake_read(org_api_key: str):
        seen.append(org_api_key)
        return {}

    with (
        patch("runlayer_cli.mdm_config.read_managed_config", return_value={}),
        patch("platform.system", return_value="Linux"),
        patch.object(aiwatch_config_cache, "LINUX_CACHE_PATH", cache_path),
        patch.object(aiwatch_config_cache, "read_backend_config", fake_read),
    ):
        result = runner.invoke(aiwatch_app, ["config", "show", "--json"])

    assert result.exit_code == 0
    cache_status = json.loads(result.output)["backend_cache"]
    assert cache_status["status"] == "valid"
    assert cache_status["location"] == str(cache_path)
    assert seen == ["rl_org_env"]


def test_config_show_reports_valid_windows_backend_cache() -> None:
    fake_winreg = MagicMock()
    fake_winreg.HKEY_LOCAL_MACHINE = object()
    fake_winreg.KEY_READ = 1
    with (
        patch(
            "runlayer_cli.mdm_config.read_managed_config",
            return_value={"org_api_key": "rl_org_12345678"},
        ),
        patch("platform.system", return_value="Windows"),
        patch.object(aiwatch_config_cache, "winreg", fake_winreg),
        patch.object(aiwatch_config_cache, "read_backend_config", return_value={}),
    ):
        result = runner.invoke(aiwatch_app, ["config", "show", "--json"])

    assert result.exit_code == 0
    cache_status = json.loads(result.output)["backend_cache"]
    assert cache_status == {
        "location": r"HKLM\Software\Runlayer\AIWatch\BackendConfig",
        "modified_at": None,
        "status": "valid",
    }


def test_config_sync_kicks_macos_bootstrap_unit() -> None:
    completed = subprocess.CompletedProcess(args=[], returncode=0)
    with (
        patch("platform.system", return_value="Darwin"),
        patch("os.geteuid", return_value=0),
        patch("subprocess.run", return_value=completed) as run,
    ):
        result = runner.invoke(aiwatch_app, ["config", "sync"])

    assert result.exit_code == 0
    assert "Configuration sync started." in result.output
    assert run.call_args.args == (
        [
            "launchctl",
            "kickstart",
            "system/com.runlayer.aiwatch.bootstrap",
        ],
    )


def test_config_sync_already_running_reports_success() -> None:
    completed = subprocess.CompletedProcess(
        args=[],
        returncode=36,
        stdout="",
        stderr="Operation already in progress",
    )
    with (
        patch("platform.system", return_value="Darwin"),
        patch("os.geteuid", return_value=0),
        patch("subprocess.run", return_value=completed),
    ):
        result = runner.invoke(aiwatch_app, ["config", "sync"])

    assert result.exit_code == 0
    assert "Cycle already running." in result.output


def test_config_sync_runs_windows_hooks_task() -> None:
    completed = subprocess.CompletedProcess(args=[], returncode=0)
    with (
        patch("platform.system", return_value="Windows"),
        patch("sys.platform", "win32"),
        patch.object(ctypes, "windll", create=True) as windll,
        patch("subprocess.run", return_value=completed) as run,
    ):
        windll.shell32.IsUserAnAdmin.return_value = True
        result = runner.invoke(aiwatch_app, ["config", "sync"])

    assert result.exit_code == 0
    assert run.call_args.args == (
        ["schtasks", "/Run", "/TN", r"\Runlayer\AIWatchHooks"],
    )


def test_config_sync_non_admin_windows_runs_hooks_task() -> None:
    completed = subprocess.CompletedProcess(args=[], returncode=0)
    with (
        patch("platform.system", return_value="Windows"),
        patch("sys.platform", "win32"),
        patch.object(ctypes, "windll", create=True) as windll,
        patch("subprocess.run", return_value=completed) as run,
    ):
        windll.shell32.IsUserAnAdmin.return_value = False
        result = runner.invoke(aiwatch_app, ["config", "sync"])

    assert result.exit_code == 0
    assert "Configuration sync started." in result.output
    assert run.call_args.args == (
        ["schtasks", "/Run", "/TN", r"\Runlayer\AIWatchHooks"],
    )


def test_config_sync_windows_access_denied_shows_elevation_hint() -> None:
    completed = subprocess.CompletedProcess(
        args=[],
        returncode=1,
        stdout="",
        stderr="ERROR: Access is denied.",
    )
    with (
        patch("platform.system", return_value="Windows"),
        patch("sys.platform", "win32"),
        patch.object(ctypes, "windll", create=True) as windll,
        patch("subprocess.run", return_value=completed),
    ):
        windll.shell32.IsUserAnAdmin.return_value = True
        result = runner.invoke(aiwatch_app, ["config", "sync"])

    assert result.exit_code == 1
    assert "Administrator privileges required" in result.output
    assert "aiwatch config sync" in result.output
    assert "elevated prompt" in result.output


def test_config_sync_non_root_macos_shows_sudo_hint() -> None:
    with (
        patch("platform.system", return_value="Darwin"),
        patch("os.geteuid", return_value=501),
        patch("subprocess.run") as run,
    ):
        result = runner.invoke(aiwatch_app, ["config", "sync"])

    assert result.exit_code == 1
    assert "sudo aiwatch config sync" in result.output
    run.assert_not_called()


def test_config_sync_missing_unit_reports_package_not_installed() -> None:
    completed = subprocess.CompletedProcess(
        args=[],
        returncode=113,
        stdout="",
        stderr="Could not find service in domain for system",
    )
    with (
        patch("platform.system", return_value="Darwin"),
        patch("os.geteuid", return_value=0),
        patch("subprocess.run", return_value=completed),
    ):
        result = runner.invoke(aiwatch_app, ["config", "sync"])

    assert result.exit_code == 1
    assert "AI Watch package not installed" in result.output


def test_config_sync_runs_linux_scan_wrapper() -> None:
    completed = subprocess.CompletedProcess(args=[], returncode=0)
    with (
        patch("platform.system", return_value="Linux"),
        patch("os.geteuid", return_value=0),
        patch.object(Path, "is_file", return_value=True),
        patch("subprocess.run", return_value=completed) as run,
    ):
        result = runner.invoke(aiwatch_app, ["config", "sync"])

    assert result.exit_code == 0
    assert "Configuration sync started." in result.output
    assert run.call_args.args == (["/usr/lib/runlayer/run-aiwatch-scan.sh"],)


def test_config_sync_linux_lock_contention_reports_skip_not_success() -> None:
    """A wrapper lock skip (EX_TEMPFAIL) ran nothing: sync must not claim the
    cycle started."""
    completed = subprocess.CompletedProcess(
        args=[],
        returncode=75,
        stdout="",
        stderr="",
    )
    with (
        patch("platform.system", return_value="Linux"),
        patch("os.geteuid", return_value=0),
        patch.object(Path, "is_file", return_value=True),
        patch("subprocess.run", return_value=completed),
    ):
        result = runner.invoke(aiwatch_app, ["config", "sync"])

    assert result.exit_code == 1
    assert "already running" in result.output
    assert "Configuration sync started." not in result.output


def test_config_sync_non_root_linux_shows_sudo_hint() -> None:
    with (
        patch("platform.system", return_value="Linux"),
        patch("os.geteuid", return_value=1000),
        patch("subprocess.run") as run,
    ):
        result = runner.invoke(aiwatch_app, ["config", "sync"])

    assert result.exit_code == 1
    assert "sudo aiwatch config sync" in result.output
    run.assert_not_called()


def test_config_refresh_quiet_noop_when_unconfigured(monkeypatch) -> None:
    monkeypatch.delenv("RUNLAYER_HOST", raising=False)
    monkeypatch.delenv("RUNLAYER_API_KEY", raising=False)
    with (
        patch("runlayer_cli.mdm_config.read_managed_config", return_value={}),
        patch("runlayer_cli.commands.aiwatch_config.sync_backend_config") as sync,
    ):
        result = runner.invoke(aiwatch_app, ["config", "refresh"])

    assert result.exit_code == 0
    assert result.output == ""
    sync.assert_not_called()


def test_config_refresh_uses_env_credentials(monkeypatch) -> None:
    monkeypatch.setenv("RUNLAYER_HOST", "https://env.runlayer.com")
    monkeypatch.setenv("RUNLAYER_API_KEY", "rl_org_env")
    with (
        patch("runlayer_cli.mdm_config.read_managed_config", return_value={}),
        patch(
            "runlayer_cli.commands.aiwatch_config.sync_backend_config",
            return_value=True,
        ) as sync,
    ):
        result = runner.invoke(aiwatch_app, ["config", "refresh"])

    assert result.exit_code == 0
    assert "refreshed" in result.output
    sync.assert_called_once_with(
        host="https://env.runlayer.com",
        org_api_key="rl_org_env",
    )


def test_config_refresh_fetch_failure_keeps_last_known_good(monkeypatch) -> None:
    monkeypatch.delenv("RUNLAYER_HOST", raising=False)
    monkeypatch.setenv("RUNLAYER_API_KEY", "rl_org_env")
    with (
        patch(
            "runlayer_cli.mdm_config.read_managed_config",
            return_value={"host": "https://managed.runlayer.com"},
        ),
        patch(
            "runlayer_cli.commands.aiwatch_config.sync_backend_config",
            return_value=False,
        ) as sync,
    ):
        result = runner.invoke(aiwatch_app, ["config", "refresh"])

    assert result.exit_code == 0
    assert "last-known-good" in result.output
    sync.assert_called_once_with(
        host="https://managed.runlayer.com",
        org_api_key="rl_org_env",
    )


def test_update_now_kicks_macos_update_unit() -> None:
    completed = subprocess.CompletedProcess(args=[], returncode=0)
    with (
        patch("platform.system", return_value="Darwin"),
        patch("os.geteuid", return_value=0),
        patch("subprocess.run", return_value=completed) as run,
    ):
        result = runner.invoke(aiwatch_app, ["update-now"])

    assert result.exit_code == 0
    assert "Update cycle started." in result.output
    assert run.call_args.args == (
        [
            "launchctl",
            "kickstart",
            "system/com.runlayer.aiwatch.update",
        ],
    )


def test_update_now_runs_windows_update_task() -> None:
    completed = subprocess.CompletedProcess(args=[], returncode=0)
    with (
        patch("platform.system", return_value="Windows"),
        patch("sys.platform", "win32"),
        patch.object(ctypes, "windll", create=True) as windll,
        patch("subprocess.run", return_value=completed) as run,
    ):
        windll.shell32.IsUserAnAdmin.return_value = True
        result = runner.invoke(aiwatch_app, ["update-now"])

    assert result.exit_code == 0
    assert run.call_args.args == (
        ["schtasks", "/Run", "/TN", r"\Runlayer\AIWatchUpdate"],
    )


def test_update_now_non_admin_windows_shows_elevation_hint() -> None:
    with (
        patch("platform.system", return_value="Windows"),
        patch("sys.platform", "win32"),
        patch.object(ctypes, "windll", create=True) as windll,
        patch("subprocess.run") as run,
    ):
        windll.shell32.IsUserAnAdmin.return_value = False
        result = runner.invoke(aiwatch_app, ["update-now"])

    assert result.exit_code == 1
    assert "Administrator privileges required" in result.output
    assert "aiwatch update-now" in result.output
    assert "elevated prompt" in result.output
    run.assert_not_called()


def test_update_now_runs_linux_update_script() -> None:
    completed = subprocess.CompletedProcess(args=[], returncode=0)
    with (
        patch("platform.system", return_value="Linux"),
        patch("os.geteuid", return_value=0),
        patch.object(Path, "is_file", return_value=True),
        patch("subprocess.run", return_value=completed) as run,
    ):
        result = runner.invoke(aiwatch_app, ["update-now"])

    assert result.exit_code == 0
    assert run.call_args.args == (["/usr/lib/runlayer/run-aiwatch-update.sh"],)


def test_update_now_missing_linux_script_reports_package_not_installed() -> None:
    with (
        patch("platform.system", return_value="Linux"),
        patch("os.geteuid", return_value=0),
        patch.object(Path, "is_file", return_value=False),
        patch("subprocess.run") as run,
    ):
        result = runner.invoke(aiwatch_app, ["update-now"])

    assert result.exit_code == 1
    assert "AI Watch package not installed" in result.output
    run.assert_not_called()


def test_update_now_non_root_linux_shows_sudo_hint() -> None:
    with (
        patch("platform.system", return_value="Linux"),
        patch("os.geteuid", return_value=1000),
        patch("subprocess.run") as run,
    ):
        result = runner.invoke(aiwatch_app, ["update-now"])

    assert result.exit_code == 1
    assert "sudo aiwatch update-now" in result.output
    run.assert_not_called()

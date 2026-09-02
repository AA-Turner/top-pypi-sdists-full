"""Tests for package-only Test Device configuration."""

from __future__ import annotations

import json
import os
import plistlib
import subprocess
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from typer.testing import CliRunner

from runlayer_cli import macos_test_device_config, mdm_config
from runlayer_cli.aiwatch import app as aiwatch_app
from runlayer_cli.aiwatch_config_cache import SyncedAIWatchConfig
from runlayer_cli.commands.setup import app as setup_app

test_device_config = macos_test_device_config

runner = CliRunner()


@pytest.fixture
def macos_root(monkeypatch) -> dict[str, MagicMock]:
    def run_defaults(command, **kwargs):
        path = Path(f"{command[2]}.plist")
        if command[1] == "export":
            if path.exists():
                return subprocess.CompletedProcess(
                    command,
                    0,
                    stdout=path.read_bytes(),
                    stderr=b"",
                )
            return subprocess.CompletedProcess(command, 1, stdout=b"", stderr=b"")
        path.write_bytes(kwargs["input"])
        return subprocess.CompletedProcess(command, 0, stdout=b"", stderr=b"")

    defaults = MagicMock(side_effect=run_defaults)
    monkeypatch.setattr(test_device_config.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(test_device_config.os, "geteuid", lambda: 0, raising=False)
    monkeypatch.setattr(test_device_config.subprocess, "run", defaults)
    return {"defaults": defaults}


@pytest.fixture
def linux_root(monkeypatch) -> None:
    monkeypatch.setattr(test_device_config.platform, "system", lambda: "Linux")
    monkeypatch.setattr(test_device_config.os, "geteuid", lambda: 0, raising=False)


def _defaults_call(defaults: MagicMock, action: str):
    return next(call for call in defaults.call_args_list if call.args[0][1] == action)


def _imported_plist(defaults: MagicMock) -> dict[str, object]:
    content = _defaults_call(defaults, "import").kwargs["input"]
    return plistlib.loads(content)


def test_aiwatch_config_publishes_local_preferences_through_cfprefsd(
    tmp_path: Path,
    macos_root,
) -> None:
    path = tmp_path / "com.runlayer.aiwatch.plist"

    result = test_device_config.configure_aiwatch_test_device(
        "https://tenant.runlayer.com/",
        "rl_org_secret",
        path=path,
    )

    assert result == {
        "host": "https://tenant.runlayer.com",
        "flushed": True,
    }
    import_call = _defaults_call(macos_root["defaults"], "import")
    assert import_call.args[0] == [
        "/usr/bin/defaults",
        "import",
        str(path.with_suffix("")),
        "-",
    ]
    assert import_call.kwargs == {
        "input": import_call.kwargs["input"],
        "check": True,
        "capture_output": True,
    }
    assert _imported_plist(macos_root["defaults"]) == {
        "Host": "https://tenant.runlayer.com",
        "OrgApiKey": "rl_org_secret",
    }
    export_call = _defaults_call(macos_root["defaults"], "export")
    assert export_call.args[0] == [
        "/usr/bin/defaults",
        "export",
        str(path.with_suffix("")),
        "-",
    ]
    assert export_call.kwargs == {
        "check": False,
        "capture_output": True,
    }


def test_aiwatch_config_removes_stale_policy_keys(
    tmp_path: Path,
    macos_root,
) -> None:
    path = tmp_path / "com.runlayer.aiwatch.plist"
    with path.open("wb") as file:
        plistlib.dump(
            {
                "Host": "https://old.example",
                "OrgApiKey": "rl_org_old",
                "Mode": "enforce",
                "Enforcement": True,
                "Sessions": True,
                "DetectProcesses": True,
                "DetectContainers": True,
                "ProjectDepth": 3,
                "ProjectTimeout": 15,
                "Username": "test-user",
                "DeviceName": "test-device",
                "AutoUpdate": False,
                "CpuCores": 2,
                "MaxCpuPercent": 25,
                "MemoryLimitMb": 768,
                "UnknownSetting": "preserved",
            },
            file,
        )

    test_device_config.configure_aiwatch_test_device(
        "https://tenant.runlayer.com",
        "rl_org_secret",
        path=path,
    )

    assert _imported_plist(macos_root["defaults"]) == {
        "Host": "https://tenant.runlayer.com",
        "OrgApiKey": "rl_org_secret",
        "Username": "test-user",
        "DeviceName": "test-device",
        "AutoUpdate": False,
        "CpuCores": 2,
        "MaxCpuPercent": 25,
        "MemoryLimitMb": 768,
        "UnknownSetting": "preserved",
    }


def test_backend_sync_owned_local_keys_match_synced_capabilities() -> None:
    # hook_wire_encodings is a backend capability advertisement with no
    # plist counterpart — admins never hand-set what codecs a backend
    # accepts, so it has no local key for the writer to strip.
    non_local_fields = {
        "version",
        "daemon_enabled",
        "remove_uv_tool",
        "hook_wire_encodings",
    }
    synced_capability_fields = {
        field
        for field in SyncedAIWatchConfig.__annotations__
        if field not in non_local_fields
        and not field.startswith(("browser_", "firefox_"))
    }
    acronyms = {"mcp": "MCP"}
    expected_keys = {
        "".join(acronyms.get(part, part.title()) for part in field.split("_"))
        for field in synced_capability_fields
    }
    expected_keys.add("Enforcement")

    assert set(mdm_config.BACKEND_SYNC_OWNED_KEYS) == expected_keys


def test_config_reports_when_cfprefsd_has_not_flushed_plist(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    path = tmp_path / "com.runlayer.aiwatch.plist"
    monkeypatch.setattr(test_device_config.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(test_device_config.os, "geteuid", lambda: 0, raising=False)
    monkeypatch.setattr(test_device_config.subprocess, "run", MagicMock())
    monkeypatch.setattr(test_device_config, "LOCAL_CONFIG_FLUSH_TIMEOUT_SECONDS", 0)

    result = test_device_config.configure_aiwatch_test_device(
        "https://tenant.runlayer.com/",
        "rl_org_secret",
        path=path,
    )

    assert result == {
        "host": "https://tenant.runlayer.com",
        "flushed": False,
    }
    warning = capsys.readouterr().err
    assert "local preferences are still flushing" in warning
    assert "rl_org_secret" not in warning


def test_config_reports_unflushed_when_disk_still_has_stale_policy_keys(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    """Same credentials on disk must not satisfy the wait while stripped
    BACKEND_SYNC_OWNED_KEYS (e.g. Sessions) linger in the stale disk copy."""
    path = tmp_path / "com.runlayer.aiwatch.plist"
    stale = {
        "Host": "https://tenant.runlayer.com",
        "OrgApiKey": "rl_org_secret",
        "Sessions": True,
    }
    with path.open("wb") as file:
        plistlib.dump(stale, file)

    def run_defaults(command, **kwargs):
        if command[1] == "export":
            return subprocess.CompletedProcess(
                command,
                0,
                stdout=path.read_bytes(),
                stderr=b"",
            )
        # Simulate cfprefsd accepting the import without flushing to disk.
        return subprocess.CompletedProcess(command, 0, stdout=b"", stderr=b"")

    monkeypatch.setattr(test_device_config.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(test_device_config.os, "geteuid", lambda: 0, raising=False)
    monkeypatch.setattr(test_device_config.subprocess, "run", run_defaults)
    monkeypatch.setattr(test_device_config, "LOCAL_CONFIG_FLUSH_TIMEOUT_SECONDS", 0)

    result = test_device_config.configure_aiwatch_test_device(
        "https://tenant.runlayer.com",
        "rl_org_secret",
        path=path,
    )

    assert result == {
        "host": "https://tenant.runlayer.com",
        "flushed": False,
    }
    assert "local preferences are still flushing" in capsys.readouterr().err


def test_config_waits_for_stale_policy_keys_to_flush_off_disk(
    tmp_path: Path,
    monkeypatch,
) -> None:
    path = tmp_path / "com.runlayer.aiwatch.plist"
    stale = {
        "Host": "https://tenant.runlayer.com",
        "OrgApiKey": "rl_org_secret",
        "Sessions": True,
    }
    with path.open("wb") as file:
        plistlib.dump(stale, file)
    imported = b""

    def run_defaults(command, **kwargs):
        nonlocal imported
        if command[1] == "export":
            return subprocess.CompletedProcess(
                command,
                0,
                stdout=path.read_bytes(),
                stderr=b"",
            )
        imported = kwargs["input"]
        return subprocess.CompletedProcess(command, 0, stdout=b"", stderr=b"")

    def flush_plist(_seconds: float) -> None:
        path.write_bytes(imported)

    monkeypatch.setattr(test_device_config.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(test_device_config.os, "geteuid", lambda: 0, raising=False)
    monkeypatch.setattr(test_device_config.subprocess, "run", run_defaults)
    monkeypatch.setattr(time, "sleep", flush_plist)

    result = test_device_config.configure_aiwatch_test_device(
        "https://tenant.runlayer.com",
        "rl_org_secret",
        path=path,
    )

    assert result == {
        "host": "https://tenant.runlayer.com",
        "flushed": True,
    }
    with path.open("rb") as file:
        assert plistlib.load(file) == {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_secret",
        }


def test_config_waits_for_cfprefsd_to_flush_credentials(
    tmp_path: Path,
    monkeypatch,
) -> None:
    path = tmp_path / "com.runlayer.aiwatch.plist"
    imported = b""

    def run_defaults(command, **kwargs):
        nonlocal imported
        if command[1] == "import":
            imported = kwargs["input"]
            return subprocess.CompletedProcess(command, 0, stdout=b"", stderr=b"")
        return subprocess.CompletedProcess(command, 1, stdout=b"", stderr=b"")

    def flush_plist(_seconds: float) -> None:
        path.write_bytes(imported)

    monkeypatch.setattr(test_device_config.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(test_device_config.os, "geteuid", lambda: 0, raising=False)
    monkeypatch.setattr(test_device_config.subprocess, "run", run_defaults)
    monkeypatch.setattr(time, "sleep", flush_plist)

    test_device_config.configure_aiwatch_test_device(
        "https://tenant.runlayer.com/",
        "rl_org_secret",
        path=path,
    )

    with path.open("rb") as file:
        assert plistlib.load(file) == {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_secret",
        }


def test_cli_config_preserves_existing_local_preferences(
    tmp_path: Path,
    macos_root,
) -> None:
    path = tmp_path / "com.runlayer.cli.plist"
    with path.open("wb") as file:
        plistlib.dump({"SyncSkills": False, "Host": "https://old.example"}, file)

    test_device_config.configure_cli_test_device(
        "https://tenant.runlayer.com",
        "rl_org_secret",
        path=path,
    )

    assert _imported_plist(macos_root["defaults"]) == {
        "Host": "https://tenant.runlayer.com",
        "OrgApiKey": "rl_org_secret",
        "SyncSkills": False,
    }


def test_cli_config_preserves_cached_preferences_before_disk_flush(
    tmp_path: Path,
    monkeypatch,
) -> None:
    path = tmp_path / "com.runlayer.cli.plist"
    cached = plistlib.dumps({"SyncSkills": False, "Host": "https://old.example"})

    def run_defaults(command, **kwargs):
        if command[1] == "export":
            return subprocess.CompletedProcess(command, 0, stdout=cached, stderr=b"")
        path.write_bytes(kwargs["input"])
        return subprocess.CompletedProcess(command, 0, stdout=b"", stderr=b"")

    defaults = MagicMock(side_effect=run_defaults)
    monkeypatch.setattr(test_device_config.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(test_device_config.os, "geteuid", lambda: 0, raising=False)
    monkeypatch.setattr(test_device_config.subprocess, "run", defaults)

    test_device_config.configure_cli_test_device(
        "https://tenant.runlayer.com",
        "rl_org_secret",
        path=path,
    )

    import_call = next(
        call for call in defaults.call_args_list if call.args[0][1] == "import"
    )
    assert plistlib.loads(import_call.kwargs["input"]) == {
        "Host": "https://tenant.runlayer.com",
        "OrgApiKey": "rl_org_secret",
        "SyncSkills": False,
    }


def test_linux_cli_config_writes_shared_config_and_credentials(
    tmp_path: Path,
    linux_root,
) -> None:
    config_path = tmp_path / "aiwatch" / "config.json"
    credentials_path = tmp_path / "aiwatch" / "credentials"
    config_path.parent.mkdir()
    config_path.write_text(
        json.dumps(
            {
                "Host": "https://old.example",
                "OrgApiKey": "rl_org_old",
                "Mode": "enforce",
                "Sessions": True,
                "AutoUpdate": False,
                "Username": "test-user",
                "UnknownSetting": "preserved",
            }
        )
    )
    credentials_path.write_text("RUNLAYER_API_KEY=rl_org_old\n")
    credentials_path.chmod(0o644)

    result = test_device_config.configure_cli_test_device(
        "https://tenant.runlayer.com/",
        "rl_org_secret",
        path=config_path,
        credentials_path=credentials_path,
    )

    assert result == {
        "host": "https://tenant.runlayer.com",
        "flushed": True,
    }
    assert json.loads(config_path.read_text()) == {
        "AutoUpdate": False,
        "Host": "https://tenant.runlayer.com",
        "UnknownSetting": "preserved",
        "Username": "test-user",
    }
    assert config_path.stat().st_mode & 0o777 == 0o644
    assert credentials_path.read_text() == "RUNLAYER_API_KEY=rl_org_secret\n"
    assert credentials_path.stat().st_mode & 0o777 == 0o600


def test_linux_cli_config_creates_public_directories_under_hardened_umask(
    tmp_path: Path,
    linux_root,
) -> None:
    config_root = tmp_path / "etc"
    config_path = config_root / "runlayer" / "aiwatch" / "config.json"
    credentials_path = config_path.with_name("credentials")
    previous_umask = os.umask(0o077)
    try:
        test_device_config.configure_cli_test_device(
            "https://tenant.runlayer.com",
            "rl_org_secret",
            path=config_path,
            credentials_path=credentials_path,
        )
    finally:
        os.umask(previous_umask)

    assert config_root.stat().st_mode & 0o777 == 0o755
    assert config_root.joinpath("runlayer").stat().st_mode & 0o777 == 0o755
    assert config_path.parent.stat().st_mode & 0o777 == 0o755


@pytest.mark.skipif(os.name == "nt", reason="POSIX credentials file")
def test_linux_cli_config_shell_quotes_credentials(
    tmp_path: Path,
    linux_root,
) -> None:
    config_path = tmp_path / "config.json"
    credentials_path = tmp_path / "credentials"
    marker = tmp_path / "injected"
    org_api_key = f"rl_org_$(touch${{IFS}}{marker})"

    test_device_config.configure_cli_test_device(
        "https://tenant.runlayer.com",
        org_api_key,
        path=config_path,
        credentials_path=credentials_path,
    )
    result = subprocess.run(
        [
            "/bin/sh",
            "-c",
            '. "$CREDENTIALS"; printf "%s" "$RUNLAYER_API_KEY"',
        ],
        env={**os.environ, "CREDENTIALS": str(credentials_path)},
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout == org_api_key
    assert not marker.exists()


def test_linux_cli_config_requires_root(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(test_device_config.platform, "system", lambda: "Linux")
    monkeypatch.setattr(test_device_config.os, "geteuid", lambda: 501, raising=False)

    with pytest.raises(test_device_config.TestDeviceConfigError, match="requires root"):
        test_device_config.configure_cli_test_device(
            "https://tenant.runlayer.com",
            "rl_org_secret",
            path=tmp_path / "config.json",
            credentials_path=tmp_path / "credentials",
        )


def test_cli_config_rejects_windows(monkeypatch) -> None:
    monkeypatch.setattr(test_device_config.platform, "system", lambda: "Windows")

    with pytest.raises(
        test_device_config.TestDeviceConfigError,
        match="supported only on macOS and Linux",
    ):
        test_device_config.configure_cli_test_device(
            "https://tenant.runlayer.com",
            "rl_org_secret",
        )


@pytest.mark.parametrize(
    ("host", "key", "message"),
    [
        ("tenant.runlayer.com", "rl_org_secret", "absolute HTTP"),
        ("https://tenant.runlayer.com", "not-an-org-key", "rl_org_"),
        ("https://tenant.runlayer.com", "rl_org_bad key", "without whitespace"),
    ],
)
def test_linux_cli_config_validates_credentials(
    tmp_path: Path,
    linux_root,
    host: str,
    key: str,
    message: str,
) -> None:
    with pytest.raises(test_device_config.TestDeviceConfigError, match=message):
        test_device_config.configure_cli_test_device(
            host,
            key,
            path=tmp_path / "config.json",
            credentials_path=tmp_path / "credentials",
        )


def test_linux_cli_config_rejects_invalid_existing_json(
    tmp_path: Path,
    linux_root,
) -> None:
    config_path = tmp_path / "config.json"
    credentials_path = tmp_path / "credentials"
    config_path.write_text("not-json")
    credentials_path.write_text("RUNLAYER_API_KEY=rl_org_old\n")

    with pytest.raises(
        test_device_config.TestDeviceConfigError,
        match="existing Linux configuration is unreadable",
    ):
        test_device_config.configure_cli_test_device(
            "https://tenant.runlayer.com",
            "rl_org_secret",
            path=config_path,
            credentials_path=credentials_path,
        )

    assert credentials_path.read_text() == "RUNLAYER_API_KEY=rl_org_old\n"


def test_config_paths_are_below_managed_preferences() -> None:
    assert test_device_config.AIWATCH_LOCAL_CONFIG_PATH == Path(
        "/Library/Preferences/com.runlayer.aiwatch.plist"
    )
    assert test_device_config.CLI_LOCAL_CONFIG_PATH == Path(
        "/Library/Preferences/com.runlayer.cli.plist"
    )
    assert "Managed Preferences" not in str(
        test_device_config.AIWATCH_LOCAL_CONFIG_PATH
    )
    assert "Managed Preferences" not in str(test_device_config.CLI_LOCAL_CONFIG_PATH)


@pytest.mark.parametrize(
    ("system", "euid", "message"),
    [
        ("Linux", 0, "supported only on macOS"),
        ("Darwin", 501, "requires root"),
    ],
)
def test_config_rejects_unsupported_context(
    tmp_path: Path,
    monkeypatch,
    system: str,
    euid: int,
    message: str,
) -> None:
    monkeypatch.setattr(test_device_config.platform, "system", lambda: system)
    monkeypatch.setattr(
        test_device_config.os,
        "geteuid",
        lambda: euid,
        raising=False,
    )

    with pytest.raises(test_device_config.TestDeviceConfigError, match=message):
        test_device_config.configure_aiwatch_test_device(
            "https://tenant.runlayer.com",
            "rl_org_secret",
            path=tmp_path / "config.plist",
        )


@pytest.mark.parametrize(
    ("host", "key", "message"),
    [
        ("tenant.runlayer.com", "rl_org_secret", "absolute HTTP"),
        ("https://tenant.runlayer.com", "not-an-org-key", "rl_org_"),
        ("https://tenant.runlayer.com", "rl_org_bad key", "without whitespace"),
    ],
)
def test_config_validates_credentials(
    tmp_path: Path,
    macos_root,
    host: str,
    key: str,
    message: str,
) -> None:
    with pytest.raises(test_device_config.TestDeviceConfigError, match=message):
        test_device_config.configure_aiwatch_test_device(
            host,
            key,
            path=tmp_path / "config.plist",
        )


def test_aiwatch_setup_config_writes_then_reconciles(monkeypatch) -> None:
    write = MagicMock(
        return_value={
            "host": "https://tenant.runlayer.com",
            "flushed": True,
        }
    )
    reconcile = MagicMock(return_value=0)
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup.configure_aiwatch_test_device",
        write,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup._reconcile_hooks",
        reconcile,
    )

    result = runner.invoke(
        aiwatch_app,
        [
            "setup",
            "config",
            "--host",
            "https://tenant.runlayer.com",
            "--org-api-key",
            "rl_org_secret",
        ],
    )

    assert result.exit_code == 0, result.output
    write.assert_called_once_with(
        "https://tenant.runlayer.com",
        "rl_org_secret",
    )
    reconcile.assert_called_once_with(
        client=None,
        host="https://tenant.runlayer.com",
        mdm=True,
        all_events=False,
    )
    assert "AI Watch configured" in result.output
    assert "rl_org_secret" not in result.output


def test_aiwatch_setup_config_warns_when_reconcile_fails(monkeypatch) -> None:
    write = MagicMock(
        return_value={
            "host": "https://tenant.runlayer.com",
            "flushed": True,
        }
    )
    reconcile = MagicMock(return_value=1)
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup.configure_aiwatch_test_device",
        write,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup._reconcile_hooks",
        reconcile,
    )

    result = runner.invoke(
        aiwatch_app,
        [
            "setup",
            "config",
            "--host",
            "https://tenant.runlayer.com",
            "--org-api-key",
            "rl_org_secret",
        ],
    )

    assert result.exit_code == 1, result.output
    reconcile.assert_called_once_with(
        client=None,
        host="https://tenant.runlayer.com",
        mdm=True,
        all_events=False,
    )
    assert "AI Watch configured" in result.output
    assert "hook reconciliation is incomplete" in result.output
    assert "hourly bootstrap daemon will retry" in result.output
    assert "rl_org_secret" not in result.output


def test_cli_setup_config_writes_then_kickstarts_schedule(monkeypatch) -> None:
    write = MagicMock(
        return_value={
            "host": "https://tenant.runlayer.com",
            "flushed": True,
        }
    )
    kickstart = MagicMock(return_value=True)
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.configure_cli_test_device",
        write,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.kickstart_cli_schedule",
        kickstart,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.plat.system",
        lambda: "Darwin",
    )

    result = runner.invoke(
        setup_app,
        [
            "config",
            "--host",
            "https://tenant.runlayer.com",
            "--org-api-key",
            "rl_org_secret",
        ],
    )

    assert result.exit_code == 0, result.output
    write.assert_called_once_with(
        "https://tenant.runlayer.com",
        "rl_org_secret",
    )
    kickstart.assert_called_once_with()
    assert "Runlayer CLI configured" in result.output
    assert "rl_org_secret" not in result.output


def test_cli_setup_config_warns_when_preferences_have_not_flushed(
    monkeypatch,
) -> None:
    write = MagicMock(
        return_value={
            "host": "https://tenant.runlayer.com",
            "flushed": False,
        }
    )
    kickstart = MagicMock(return_value=True)
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.configure_cli_test_device",
        write,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.kickstart_cli_schedule",
        kickstart,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.plat.system",
        lambda: "Darwin",
    )

    result = runner.invoke(
        setup_app,
        [
            "config",
            "--host",
            "https://tenant.runlayer.com",
            "--org-api-key",
            "rl_org_secret",
        ],
    )

    assert result.exit_code == 0, result.output
    kickstart.assert_called_once_with()
    assert "local preferences are still flushing" in result.output
    assert "hourly schedule agent will retry" in result.output
    assert "rl_org_secret" not in result.output


def test_linux_cli_setup_config_reports_paths_without_macos_kick(
    monkeypatch,
) -> None:
    write = MagicMock(
        return_value={
            "host": "https://tenant.runlayer.com",
            "flushed": True,
        }
    )
    kickstart = MagicMock(return_value=True)
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.configure_cli_test_device",
        write,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.kickstart_cli_schedule",
        kickstart,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.plat.system",
        lambda: "Linux",
    )

    result = runner.invoke(
        setup_app,
        [
            "config",
            "--host",
            "https://tenant.runlayer.com",
            "--org-api-key",
            "rl_org_secret",
        ],
    )

    assert result.exit_code == 0, result.output
    kickstart.assert_not_called()
    assert "/etc/runlayer/aiwatch/config.json" in result.output
    assert "/etc/runlayer/aiwatch/credentials" in result.output
    assert "rl_org_secret" not in result.output

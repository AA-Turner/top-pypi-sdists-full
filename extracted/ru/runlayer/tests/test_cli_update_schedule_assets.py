"""Static contracts for packaged Runlayer CLI update and skill-sync schedules."""

from __future__ import annotations

import os
import plistlib
from pathlib import Path
import shlex
import subprocess
import time
import xml.etree.ElementTree as ET

import pytest
import yaml

from runlayer_cli import regex_safe


_CLI_ROOT = Path(__file__).parent.parent
_MACOS = _CLI_ROOT / "packaging" / "macos"
_WINDOWS = _CLI_ROOT / "packaging" / "windows"
_LINUX = _CLI_ROOT / "packaging" / "linux"
_MACOS_PLIST = _MACOS / "com.runlayer.cli.update.plist"
_WINDOWS_REGISTER = _WINDOWS / "cli-update-task" / "register-tasks.ps1"
_WINDOWS_UNREGISTER = _WINDOWS / "cli-update-task" / "unregister-tasks.ps1"
_WINDOWS_SCHEDULE_REGISTER = _WINDOWS / "cli-schedule-task" / "register-tasks.ps1"
_WINDOWS_SCHEDULE_UNREGISTER = _WINDOWS / "cli-schedule-task" / "unregister-tasks.ps1"
_WINDOWS_WXS = _WINDOWS / "runlayer.wxs"
_LINUX_CRON = _LINUX / "cron.d-runlayer-cli"
_LINUX_UPDATE_WRAPPER = _LINUX / "run-cli-update.sh"
_LINUX_NFPM = _LINUX / "nfpm.yaml"


def _windows_package() -> tuple[str, ET.Element]:
    root = ET.fromstring(_WINDOWS_WXS.read_text())
    ns = root.tag[root.tag.index("{") : root.tag.index("}") + 1]
    package = root.find(f"{ns}Package")
    assert package is not None
    return ns, package


def test_macos_cli_package_ships_plain_hourly_update_daemon() -> None:
    with _MACOS_PLIST.open("rb") as f:
        data = plistlib.load(f)

    assert data == {
        "Label": "com.runlayer.cli.update",
        "ProgramArguments": [
            "/usr/local/bin/runlayer",
            "__scheduled-update",
        ],
        "StartInterval": 3600,
    }

    build = (_MACOS / "build_pkg_runlayer.sh").read_text()
    postinstall = (_MACOS / "scripts" / "postinstall-runlayer").read_text()
    assert _MACOS_PLIST.name in build
    assert "postinstall-runlayer" in build
    assert _MACOS_PLIST.name in postinstall
    assert 'launchctl bootstrap system "$UPDATE_DAEMON_PLIST"' in postinstall
    # The updater may be the parent of this very install transaction, so the
    # postinstall must never boot it (or anything system-domain) out. The
    # skill-sync LaunchAgent bootout is gui-domain only and exempt.
    assert "launchctl bootout system" not in postinstall
    assert 'bootout "system' not in postinstall


def test_windows_cli_package_registers_locked_hourly_update_task() -> None:
    register = _WINDOWS_REGISTER.read_text()

    assert (
        '$script:ExePath = Join-Path (Split-Path -Parent $PSScriptRoot) "runlayer.exe"'
    ) in register
    assert "C:\\Program Files" not in register
    assert '"CLIUpdate"' in register
    assert '"__scheduled-update"' in register
    assert "New-RunlayerRepeatingTrigger -IntervalMinutes 60" in register
    assert "-InitialDelayMinutes 2" in register
    assert "-InitialDelayMinutes 73" not in register
    assert "New-RunlayerUpdateTaskSettings" in register
    assert "Get-RunlayerUpdateTaskSddl" in register
    assert "WindowsIdentity]::GetCurrent()" in register
    assert ".IsSystem" in register
    assert "Start-ScheduledTask" not in register


def test_windows_cli_uninstall_removes_only_cli_update_tasks() -> None:
    unregister = _WINDOWS_UNREGISTER.read_text()

    assert '"CLIUpdate"' in unregister
    assert '"CLIUpdateHandoff"' in unregister
    assert "AIWatchUpdate" not in unregister
    assert "GetTasks(1)" in unregister
    assert "preserved shared \\Runlayer task folder" in unregister


def test_windows_cli_package_registers_all_users_skill_sync_task() -> None:
    register = _WINDOWS_SCHEDULE_REGISTER.read_text()

    assert (
        '$script:ExePath = Join-Path (Split-Path -Parent $PSScriptRoot) "runlayer.exe"'
    ) in register
    assert '"CLISchedule"' in register
    assert '"schedule --all-users"' in register
    assert "New-ScheduledTaskTrigger -AtLogOn" in register
    assert "New-RunlayerRepeatingTrigger -IntervalMinutes 60" in register
    assert "New-RunlayerTaskSettings" in register
    assert "Set-RunlayerTaskSecurity" in register
    assert "WindowsIdentity]::GetCurrent()" in register
    assert ".IsSystem" in register


def test_windows_cli_uninstall_removes_only_cli_schedule_task() -> None:
    unregister = _WINDOWS_SCHEDULE_UNREGISTER.read_text()

    assert '$script:CliScheduleTaskNames = @("CLISchedule")' in unregister
    assert '"CLIUpdate"' not in unregister
    assert '"AIWatchUpdate"' not in unregister
    assert "GetTasks(1)" in unregister
    assert "preserved shared \\Runlayer task folder" in unregister


def test_windows_cli_msi_bundles_and_sequences_update_task_scripts() -> None:
    ns, package = _windows_package()

    component_refs = {
        ref.get("Id")
        for feature in package.findall(f"{ns}Feature")
        for ref in feature.findall(f"{ns}ComponentRef")
    }
    assert "CliUpdateTaskScripts" in component_refs
    assert "CliScheduleTaskScripts" in component_refs

    custom_actions = {
        action.get("Id"): action for action in package.findall(f"{ns}CustomAction")
    }
    for action_id in (
        "RegisterCliUpdateTask",
        "UnregisterCliUpdateTask",
        "RegisterCliScheduleTask",
        "UnregisterCliScheduleTask",
    ):
        action = custom_actions[action_id]
        assert action.get("BinaryRef") == "Wix4UtilCA_X64"
        assert action.get("DllEntry") == "WixQuietExec64"
        assert action.get("Execute") == "deferred"
        assert action.get("Impersonate") == "no"
    assert custom_actions["RegisterCliUpdateTask"].get("Return") == "check"
    assert custom_actions["UnregisterCliUpdateTask"].get("Return") == "ignore"
    assert custom_actions["RegisterCliScheduleTask"].get("Return") == "check"
    assert custom_actions["UnregisterCliScheduleTask"].get("Return") == "ignore"

    sequence = package.find(f"{ns}InstallExecuteSequence")
    assert sequence is not None
    scheduled = {
        action.get("Action"): action for action in sequence.findall(f"{ns}Custom")
    }
    register = scheduled["RegisterCliUpdateTask"]
    assert register.get("After") == "InstallFiles"
    assert register.get("Condition") == "NOT REMOVE"
    unregister = scheduled["UnregisterCliUpdateTask"]
    assert unregister.get("Before") == "RemoveFiles"
    assert unregister.get("Condition") == 'REMOVE="ALL" AND NOT UPGRADINGPRODUCTCODE'
    schedule_register = scheduled["RegisterCliScheduleTask"]
    assert schedule_register.get("After") == "InstallFiles"
    assert schedule_register.get("Condition") == "NOT REMOVE"
    schedule_unregister = scheduled["UnregisterCliScheduleTask"]
    assert schedule_unregister.get("Before") == "RemoveFiles"
    assert schedule_unregister.get("Condition") == (
        'REMOVE="ALL" AND NOT UPGRADINGPRODUCTCODE'
    )


def test_windows_cli_build_pins_and_loads_wix_util_extension() -> None:
    build = (_WINDOWS / "build_msi_runlayer.ps1").read_text()

    assert "WixToolset.Util.wixext/5.0.2" in build
    assert "-ext WixToolset.Util.wixext" in build


def test_windows_desktop_msi_conditionally_registers_native_tray() -> None:
    ns, package = _windows_package()
    wxs = _WINDOWS_WXS.read_text()
    components = {
        component.get("Id"): component for component in package.iter(f"{ns}Component")
    }
    tray = components["TrayRegistration"]

    registry_keys = {key.get("Key"): key for key in tray.findall(f"{ns}RegistryKey")}
    protocol = registry_keys["runlayer"]
    assert protocol.get("Root") == "HKCR"
    protocol_values = {
        value.get("Name", ""): value for value in protocol.findall(f"{ns}RegistryValue")
    }
    assert protocol_values[""].get("Value") == "URL:Runlayer Protocol"
    assert protocol_values["URL Protocol"].get("Value") == ""

    command = registry_keys[r"runlayer\shell\open\command"].find(f"{ns}RegistryValue")
    assert command is not None
    assert command.get("Value") == ('"[INSTALLDIR]tray\\RunlayerTray.exe" "%1"')

    run_value = tray.find(f"{ns}RegistryValue")
    assert run_value is not None
    assert run_value.attrib == {
        "Root": "HKLM",
        "Key": r"Software\Microsoft\Windows\CurrentVersion\Run",
        "Name": "Runlayer",
        "Type": "string",
        "Value": '"[INSTALLDIR]tray\\RunlayerTray.exe"',
    }

    component_refs = {
        ref.get("Id")
        for feature in package.findall(f"{ns}Feature")
        for ref in feature.findall(f"{ns}ComponentRef")
    }
    assert "TrayRegistration" in component_refs

    desktop_condition = "<?if $(var.IncludeDesktop) = 1 ?>"
    tray_component = wxs.index('Id="TrayRegistration"')
    assert wxs.rfind(desktop_condition, 0, tray_component) >= 0
    assert wxs.index("<?endif?>", tray_component) > tray_component
    tray_ref = wxs.index('<ComponentRef Id="TrayRegistration"/>')
    assert wxs.rfind(desktop_condition, 0, tray_ref) >= 0
    assert wxs.index("<?endif?>", tray_ref) > tray_ref

    build = (_WINDOWS / "build_msi_runlayer.ps1").read_text()
    assert r'$TrayExePath = "$TrayDir\RunlayerTray.exe"' in build
    assert "$IncludeDesktop -and" in build
    assert "-d IncludeDesktop=$IncludeDesktopValue" in build


def test_cli_installer_variants_default_to_tray_free_and_write_product_marker() -> None:
    macos_build = (_MACOS / "build_pkg_runlayer.sh").read_text()
    windows_build = (_WINDOWS / "build_msi_runlayer.ps1").read_text()
    wxs = _WINDOWS_WXS.read_text()

    assert 'INCLUDE_DESKTOP="${INCLUDE_DESKTOP:-0}"' in macos_build
    assert 'PACKAGE_SLUG="cli"' in macos_build
    assert 'PACKAGE_SLUG="desktop"' in macos_build
    assert 'payload/usr/local/lib/runlayer/product"' in macos_build
    # WiX 5.0.2 cannot Exclude in Files harvesting; the build script keeps the
    # CLI-only bundle tray-free instead.
    assert "Exclude=" not in wxs
    assert 'Include="..\\..\\dist\\runlayer\\**"' in wxs
    assert r"-not $IncludeDesktop -and (Test-Path $TrayDir)" in windows_build
    assert r"Remove-Item -Recurse -Force $TrayDir" in windows_build
    assert 'Id="ProductMarker"' in wxs
    assert 'Name="product"' in wxs
    assert '$PackageSlug = if ($IncludeDesktop) { "desktop" } else { "cli" }' in (
        windows_build
    )


def test_linux_cli_package_ships_hourly_update_schedule() -> None:
    destination_name = _LINUX_CRON.name.removeprefix("cron.d-")
    cron = _LINUX_CRON.read_text()

    assert destination_name == "runlayer-cli"
    assert regex_safe.fullmatch(r"[A-Za-z0-9_-]+", destination_name)
    assert "41 * * * * root /usr/lib/runlayer/run-cli-update.sh" in cron


def test_linux_cli_update_wrapper_locks_schedule_and_gates_credentials() -> None:
    text = _LINUX_UPDATE_WRAPPER.read_text()
    source = '. "$CREDENTIALS_FILE"'
    key_gate = '[ -z "${RUNLAYER_API_KEY:-}" ]'
    invocation = "/usr/bin/runlayer __scheduled-update"

    assert text.startswith("#!/bin/sh")
    assert "sudo" not in text
    assert "runuser" not in text
    assert "EX_TEMPFAIL=75" in text
    assert "LOCK_DIR=/run/runlayer-cli" in text
    assert 'exec 9>"$LOCK_DIR/update.lock"' in text
    assert 'chmod 0600 "$LOCK_DIR/update.lock"' in text
    assert "flock -n 9 || exit $EX_TEMPFAIL" in text
    assert 'exec 8>"$LOCK_DIR/schedule.lock"' in text
    assert 'chmod 0600 "$LOCK_DIR/schedule.lock"' in text
    assert "flock 8 || exit 1" in text
    assert "flock -n 8" not in text
    assert "CREDENTIALS_FILE=/etc/runlayer/aiwatch/credentials" in text
    assert source in text
    assert key_gate in text
    assert "export RUNLAYER_API_KEY" in text
    assert "export RUNLAYER_HOST" in text
    assert text.find("flock -n 9") < text.find("flock 8") < text.find(source)
    assert text.find(source) < text.find(key_gate) < text.find(invocation)
    assert "AutoUpdate" not in text
    assert "config.json" not in text
    assert "logger -t runlayer-cli" in text
    assert '"update failed (rc=$update_rc)"' in text
    assert "exit $update_rc" in text


def _test_linux_wrapper(
    tmp_path: Path,
    *,
    credentials: str | None = None,
) -> tuple[Path, Path, Path]:
    lock_dir = tmp_path / "locks"
    credentials_path = tmp_path / "credentials"
    update_marker = tmp_path / "updated"
    if credentials is not None:
        credentials_path.write_text(credentials)

    wrapper = tmp_path / "run-cli-update.sh"
    wrapper.write_text(
        _LINUX_UPDATE_WRAPPER.read_text()
        .replace(
            "LOCK_DIR=/run/runlayer-cli",
            f"LOCK_DIR={shlex.quote(str(lock_dir))}",
        )
        .replace(
            "CREDENTIALS_FILE=/etc/runlayer/aiwatch/credentials",
            f"CREDENTIALS_FILE={shlex.quote(str(credentials_path))}",
        )
        .replace(
            "/usr/bin/runlayer __scheduled-update",
            f"touch {shlex.quote(str(update_marker))}",
        )
    )
    wrapper.chmod(0o755)
    return wrapper, update_marker, lock_dir


@pytest.mark.skipif(os.name == "nt", reason="Linux wrapper requires a POSIX shell")
def test_linux_cli_update_lock_contention_exits_tempfail(tmp_path: Path) -> None:
    wrapper, update_marker, _lock_dir = _test_linux_wrapper(tmp_path)
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_flock = fake_bin / "flock"
    fake_flock.write_text("#!/bin/sh\nexit 1\n")
    fake_flock.chmod(0o755)

    result = subprocess.run(
        [str(wrapper)],
        env={
            **os.environ,
            "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
            "RUNLAYER_API_KEY": "",
            "RUNLAYER_HOST": "",
        },
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 75
    assert result.stdout == ""
    assert result.stderr == ""
    assert not update_marker.exists()


@pytest.mark.skipif(os.name == "nt", reason="Linux wrapper requires a POSIX shell")
def test_linux_cli_update_is_quiet_when_unconfigured(tmp_path: Path) -> None:
    wrapper, update_marker, _lock_dir = _test_linux_wrapper(tmp_path)
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_flock = fake_bin / "flock"
    fake_flock.write_text("#!/bin/sh\nexit 0\n")
    fake_flock.chmod(0o755)

    result = subprocess.run(
        [str(wrapper)],
        env={
            **os.environ,
            "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
            "RUNLAYER_API_KEY": "",
            "RUNLAYER_HOST": "",
        },
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert not update_marker.exists()


@pytest.mark.skipif(os.name == "nt", reason="Linux wrapper requires a POSIX shell")
def test_linux_cli_update_waits_for_schedule_lock(tmp_path: Path) -> None:
    wrapper, update_marker, _lock_dir = _test_linux_wrapper(
        tmp_path,
        credentials="RUNLAYER_API_KEY=rl_org_test\n",
    )
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_flock = fake_bin / "flock"
    fake_flock.write_text(
        """#!/bin/sh
if [ "${1:-}" = "-n" ]; then
    exit 0
fi
while [ -e "$TEST_SCHEDULE_LOCK" ]; do
    sleep 0.01
done
"""
    )
    fake_flock.chmod(0o755)
    held_schedule_lock = tmp_path / "schedule-lock-held"
    held_schedule_lock.touch()
    env = {
        **os.environ,
        "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
        "TEST_SCHEDULE_LOCK": str(held_schedule_lock),
    }

    update = subprocess.Popen(
        [str(wrapper)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        time.sleep(0.25)
        assert update.poll() is None
    finally:
        held_schedule_lock.unlink(missing_ok=True)

    stdout, stderr = update.communicate(timeout=2)
    assert update.returncode == 0, (stdout, stderr)
    assert update_marker.exists()


def test_linux_nfpm_ships_root_owned_cli_update_wrapper() -> None:
    data = yaml.safe_load(_LINUX_NFPM.read_text())
    contents = {entry["dst"]: entry for entry in data["contents"]}

    assert contents["/usr/lib/runlayer/run-cli-update.sh"] == {
        "src": "./packaging/linux/run-cli-update.sh",
        "dst": "/usr/lib/runlayer/run-cli-update.sh",
        "file_info": {"mode": 0o755, "owner": "root", "group": "root"},
    }

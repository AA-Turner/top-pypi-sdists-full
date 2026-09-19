"""Regression evidence for bounded AI-client launcher inspection."""

from __future__ import annotations

import os
from pathlib import Path
import struct
from types import SimpleNamespace

import pytest

from runlayer_cli.scan import (
    cli_binaries as cli_binaries_module,
    client_presence as presence_module,
    hidden_space_sweep as hidden_module,
    launcher_inspection as launcher_module,
    symlink_identity as symlink_identity_module,
)
from runlayer_cli.scan.client_presence import (
    DetectedClient,
    detect_client_presence,
)
from runlayer_cli.scan.clients import (
    InstallProbe,
    MCPClientDefinition,
    get_client_by_name,
)
from runlayer_cli.scan.completeness import ScanCompletionStatus
from runlayer_cli.scan.hidden_space_sweep import (
    HiddenLauncherDirectory,
    HiddenSpaceScanResult,
    scan_hidden_spaces,
)
from runlayer_cli.scan.launcher_inspection import inspect_launcher_identities


_SHELL_LINK_CLSID = bytes.fromhex("0114020000000000c000000000000046")
_SHELL_LINK_HAS_RELATIVE_PATH = 0x00000008
_SHELL_LINK_IS_UNICODE = 0x00000080


def _aider_client() -> MCPClientDefinition:
    client = get_client_by_name("aider")
    assert client is not None
    return client


def _isolate_launcher_signals(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )
    monkeypatch.setattr(
        presence_module,
        "scan_pip_global_packages",
        lambda *_args, **_kwargs: {},
    )
    monkeypatch.setattr(
        presence_module,
        "_wsl_homes",
        lambda _scan_status=None: (),
    )
    monkeypatch.setattr(
        presence_module,
        "_windows_uninstall_entries",
        lambda *args, **kwargs: [],
    )


def _expected_aider(target: Path | None = None) -> list[DetectedClient]:
    return [
        DetectedClient(
            client="aider",
            display_name="Aider",
            detected_via=["cli"],
            config_paths=[str(target.resolve())] if target is not None else [],
        )
    ]


def _write_relative_shell_link(path: Path, relative_target: str) -> None:
    """Write a minimal MS-SHLLINK file with Unicode RelativePath StringData."""
    flags = _SHELL_LINK_HAS_RELATIVE_PATH | _SHELL_LINK_IS_UNICODE
    header = struct.pack(
        "<I16sIIQQQIiIHHII",
        0x4C,
        _SHELL_LINK_CLSID,
        flags,
        0x20,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
    )
    encoded_target = relative_target.encode("utf-16le")
    code_units = len(encoded_target) // 2
    string_data = struct.pack("<H", code_units) + encoded_target
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(header + string_data + struct.pack("<I", 0))


@pytest.mark.skipif(os.name != "posix", reason="requires a real POSIX symlink")
def test_aider_detected_through_local_bin_netcheck_symlink(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    target = tmp_path / "vendor" / "aider"
    target.parent.mkdir()
    target.write_text("#!/bin/sh\n")
    target.chmod(0o755)
    launcher = tmp_path / ".local" / "bin" / "netcheck"
    launcher.parent.mkdir(parents=True)
    launcher.symlink_to(target)

    assert launcher.is_symlink()
    assert launcher.resolve().name == "aider"
    assert detect_client_presence(
        [_aider_client()],
        home=tmp_path,
        system="Linux",
        environment={},
        hidden_space_result=HiddenSpaceScanResult(),
    ) == _expected_aider(target)


@pytest.mark.skipif(os.name != "posix", reason="requires a real POSIX symlink")
def test_aider_detected_through_hidden_space_renamed_symlink(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    home = tmp_path / "home"
    target = home / "vendor" / "aider"
    target.parent.mkdir(parents=True)
    target.write_text("#!/bin/sh\n")
    target.chmod(0o755)
    launcher = home / ".cache" / ".updater-state" / "bin" / "netcheck"
    launcher.parent.mkdir(parents=True)
    launcher.symlink_to(target)
    hidden_result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=False,
        temp_roots=(),
    )

    assert hidden_result.files == []
    assert len(hidden_result.launcher_directories) == 1
    assert (
        detect_client_presence(
            [_aider_client()],
            home=home,
            system="Linux",
            environment={},
            hidden_space_result=hidden_result,
        )
        == _expected_aider()
    )


def test_aider_detected_through_renamed_windows_cmd_wrapper(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    target = tmp_path / "aider-bin" / "aider.exe"
    target.parent.mkdir()
    target.write_bytes(b"MZ")
    launcher = tmp_path / "AppData" / "Roaming" / "npm" / "netcheck.cmd"
    launcher.parent.mkdir(parents=True)
    launcher.write_bytes(
        b'@echo off\r\n@"%~dp0..\\..\\..\\aider-bin\\aider.exe" %*\r\n'
    )

    assert (
        detect_client_presence(
            [_aider_client()],
            home=tmp_path,
            system="Windows",
            environment={},
            hidden_space_result=HiddenSpaceScanResult(),
            include_current_user_registry=False,
            wsl_distros=[],
        )
        == _expected_aider()
    )


@pytest.mark.parametrize(
    "version_root",
    [
        Path("AppData/Roaming/nvm/v20.0.0"),
        Path("AppData/Roaming/fnm/node-versions/v20.0.0/installation"),
    ],
    ids=["nvm", "fnm"],
)
def test_aider_detected_through_version_manager_cmd_wrapper(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    version_root: Path,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    root = tmp_path / version_root
    root.mkdir(parents=True)
    (root / "aider.exe").write_bytes(b"MZ")
    (root / "netcheck.cmd").write_bytes(b'@"%~dp0aider.exe" %*\r\n')

    assert (
        detect_client_presence(
            [_aider_client()],
            home=tmp_path,
            system="Windows",
            environment={},
            hidden_space_result=HiddenSpaceScanResult(),
            include_current_user_registry=False,
            wsl_distros=[],
        )
        == _expected_aider()
    )


def test_version_manager_root_cap_marks_client_presence_incomplete(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    versions = tmp_path / "AppData" / "Roaming" / "nvm"
    (versions / "v1").mkdir(parents=True)
    (versions / "v2").mkdir()
    monkeypatch.setattr(cli_binaries_module, "_MAX_VERSION_MANAGER_ROOTS", 1)
    status = ScanCompletionStatus()

    detect_client_presence(
        [_aider_client()],
        home=tmp_path,
        system="Windows",
        environment={},
        hidden_space_result=HiddenSpaceScanResult(),
        include_current_user_registry=False,
        wsl_distros=[],
        scan_status=status,
    )

    assert status.complete is False
    assert "client_launcher_probe_truncated" in status.reasons


def test_version_manager_checkpoint_deadline_marks_client_presence_incomplete(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    (tmp_path / "AppData" / "Roaming" / "nvm" / "v1").mkdir(parents=True)
    monotonic_values = iter((0.0, 6.0))
    monkeypatch.setattr(
        launcher_module.time,
        "monotonic",
        lambda: next(monotonic_values, 6.0),
    )
    status = ScanCompletionStatus()

    detect_client_presence(
        [_aider_client()],
        home=tmp_path,
        system="Windows",
        environment={},
        hidden_space_result=HiddenSpaceScanResult(),
        include_current_user_registry=False,
        wsl_distros=[],
        scan_status=status,
    )

    assert status.complete is False
    assert "client_launcher_probe_truncated" in status.reasons


def test_aider_detected_through_renamed_windows_shell_link(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    target = tmp_path / "aider-bin" / "aider.exe"
    target.parent.mkdir()
    target.write_bytes(b"MZ")
    launcher = (
        tmp_path
        / "AppData"
        / "Local"
        / "Microsoft"
        / "WinGet"
        / "Links"
        / "netcheck.lnk"
    )
    _write_relative_shell_link(
        launcher,
        r"..\..\..\..\..\aider-bin\aider.exe",
    )

    assert (
        detect_client_presence(
            [_aider_client()],
            home=tmp_path,
            system="Windows",
            environment={},
            hidden_space_result=HiddenSpaceScanResult(),
            include_current_user_registry=False,
            wsl_distros=[],
        )
        == _expected_aider()
    )


@pytest.mark.parametrize("suffix", [".cmd", ".lnk"])
def test_windows_user_token_with_profile_sid_inspects_safe_launchers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    suffix: str,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    target = tmp_path / "aider-bin" / "aider.exe"
    target.parent.mkdir()
    target.write_bytes(b"MZ")
    launcher = tmp_path / "AppData" / "Roaming" / "npm" / f"netcheck{suffix}"
    launcher.parent.mkdir(parents=True)
    if suffix == ".cmd":
        launcher.write_bytes(
            b'@echo off\r\n@"%~dp0..\\..\\..\\aider-bin\\aider.exe" %*\r\n'
        )
    else:
        _write_relative_shell_link(
            launcher,
            r"..\..\..\aider-bin\aider.exe",
        )

    assert (
        detect_client_presence(
            [_aider_client()],
            home=tmp_path,
            system="Windows",
            environment={},
            hidden_space_result=HiddenSpaceScanResult(),
            windows_user_sid="S-1-5-21-1-2-3-1001",
            include_current_user_registry=False,
            wsl_distros=[],
        )
        == _expected_aider()
    )


@pytest.mark.parametrize("suffix", [".cmd", ".lnk"])
def test_windows_system_profile_skips_launcher_inspection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    suffix: str,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    target = tmp_path / "aider-bin" / "aider.exe"
    target.parent.mkdir()
    target.write_bytes(b"MZ")
    launcher = tmp_path / "AppData" / "Roaming" / "npm" / f"netcheck{suffix}"
    launcher.parent.mkdir(parents=True)
    if suffix == ".cmd":
        launcher.write_bytes(
            b'@echo off\r\n@"%~dp0..\\..\\..\\aider-bin\\aider.exe" %*\r\n'
        )
    else:
        _write_relative_shell_link(
            launcher,
            r"..\..\..\aider-bin\aider.exe",
        )
    status = ScanCompletionStatus()

    detected = detect_client_presence(
        [_aider_client()],
        home=tmp_path,
        system="Windows",
        environment={},
        hidden_space_result=HiddenSpaceScanResult(),
        windows_user_sid="S-1-5-21-1-2-3-1001",
        windows_system_profile=True,
        include_current_user_registry=False,
        wsl_distros=[],
        scan_status=status,
    )

    assert detected == []
    assert status.reasons == ["client_launcher_profile_safety_skip"]


def test_windows_interactive_user_still_inspects_safe_launcher_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    target = tmp_path / "aider-bin" / "aider.exe"
    target.parent.mkdir()
    target.write_bytes(b"MZ")
    launcher = tmp_path / "AppData" / "Roaming" / "npm" / "netcheck.cmd"
    launcher.parent.mkdir(parents=True)
    launcher.write_bytes(
        b'@echo off\r\n@"%~dp0..\\..\\..\\aider-bin\\aider.exe" %*\r\n'
    )

    detected = detect_client_presence(
        [_aider_client()],
        home=tmp_path,
        system="Windows",
        environment={},
        hidden_space_result=HiddenSpaceScanResult(),
        include_current_user_registry=True,
        wsl_distros=[],
    )

    assert detected == _expected_aider()


def test_parsed_launcher_never_probes_version_or_executes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    target = tmp_path / "aider-bin" / "aider.exe"
    target.parent.mkdir()
    target.write_bytes(b"MZ")
    launcher = tmp_path / "AppData" / "Roaming" / "npm" / "netcheck.cmd"
    launcher.parent.mkdir(parents=True)
    launcher.write_bytes(
        b'@echo off\r\n@"%~dp0..\\..\\..\\aider-bin\\aider.exe" %*\r\n'
    )
    monkeypatch.setattr(
        presence_module,
        "get_cli_version",
        lambda *_args, **_kwargs: pytest.fail("derived launcher executed"),
    )
    client = MCPClientDefinition(
        name="probe",
        display_name="Probe",
        paths=[],
        install_probe=InstallProbe(
            cli_binaries=["aider"],
            probe_cli_version=True,
        ),
    )

    assert detect_client_presence(
        [client],
        home=tmp_path,
        system="Windows",
        environment={},
        hidden_space_result=HiddenSpaceScanResult(),
        include_current_user_registry=False,
        wsl_distros=[],
    ) == [
        DetectedClient(
            client="probe",
            display_name="Probe",
            detected_via=["cli"],
        )
    ]


def test_hidden_launcher_directory_cap_marks_discovery_incomplete(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "home"
    for index in range(2):
        (home / ".cache" / f".hidden-{index}" / "bin").mkdir(parents=True)
    monkeypatch.setattr(hidden_module, "MAX_LAUNCHER_DIRECTORIES", 1)

    result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=False,
        temp_roots=(),
    )

    assert len(result.launcher_directories) == 1
    assert result.launcher_directories_truncated is True
    assert result.truncated is True


def test_hidden_truncation_marks_client_presence_incomplete(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    status = ScanCompletionStatus()

    assert (
        detect_client_presence(
            [_aider_client()],
            home=tmp_path,
            system="Linux",
            environment={},
            hidden_space_result=HiddenSpaceScanResult(truncated=True),
            scan_status=status,
        )
        == []
    )
    assert status.complete is False


@pytest.mark.skipif(os.name != "posix", reason="requires a real POSIX symlink")
def test_windows_user_launcher_root_reparse_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    target = tmp_path / "target" / "aider.exe"
    target.parent.mkdir()
    target.write_bytes(b"MZ")
    actual_root = tmp_path / "actual-npm"
    actual_root.mkdir()
    (actual_root / "alias.cmd").write_bytes(
        b'@echo off\r\n@"%~dp0..\\target\\aider.exe" %*\r\n'
    )
    launcher_root = tmp_path / "AppData" / "Roaming" / "npm"
    launcher_root.parent.mkdir(parents=True)
    launcher_root.symlink_to(actual_root, target_is_directory=True)

    assert (
        detect_client_presence(
            [_aider_client()],
            home=tmp_path,
            system="Windows",
            environment={},
            hidden_space_result=HiddenSpaceScanResult(),
            include_current_user_registry=False,
            wsl_distros=[],
        )
        == []
    )


@pytest.mark.skipif(os.name != "posix", reason="requires real POSIX symlinks")
def test_hidden_launcher_chain_resolves_to_known_executable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    home = tmp_path / "home"
    final_target = home / "target" / "aider"
    final_target.parent.mkdir(parents=True)
    final_target.write_bytes(b"binary")
    final_target.chmod(0o755)
    intermediate = home / "target" / "intermediate"
    intermediate.symlink_to(final_target)
    launcher = home / ".cache" / ".hidden" / "bin" / "alias"
    launcher.parent.mkdir(parents=True)
    launcher.symlink_to(intermediate)
    hidden_result = scan_hidden_spaces(
        home=home,
        system="Linux",
        include_files=False,
        temp_roots=(),
    )

    assert (
        detect_client_presence(
            [_aider_client()],
            home=home,
            system="Linux",
            environment={},
            hidden_space_result=hidden_result,
        )
        == _expected_aider()
    )


@pytest.mark.skipif(os.name != "posix", reason="requires real POSIX symlinks")
def test_posix_launcher_rejects_long_component_link_chain_without_realpath(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    final_dir = tmp_path / "target"
    final_dir.mkdir()
    target = final_dir / "aider"
    target.write_bytes(b"binary")
    target.chmod(0o755)
    next_target = final_dir
    for index in reversed(range(128)):
        link = tmp_path / f"chain-{index}"
        link.symlink_to(next_target, target_is_directory=True)
        next_target = link
    launcher_dir = tmp_path / "bin"
    launcher_dir.mkdir()
    (launcher_dir / "alias").symlink_to(next_target / "aider")
    monkeypatch.setattr(
        symlink_identity_module,
        "os",
        SimpleNamespace(
            access=os.access,
            curdir=os.curdir,
            pardir=os.pardir,
            path=SimpleNamespace(
                abspath=os.path.abspath,
                normcase=os.path.normcase,
                realpath=lambda *_a, **_k: pytest.fail("unbounded realpath traversal"),
            ),
            X_OK=os.X_OK,
        ),
    )
    checkpoints = 0

    def checkpoint() -> None:
        nonlocal checkpoints
        checkpoints += 1

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Linux",
        hidden_directories=[HiddenLauncherDirectory(path=launcher_dir)],
        checkpoint=checkpoint,
    )

    assert result.findings == []
    assert result.malformed_or_unsafe == 1
    assert checkpoints <= (2 * symlink_identity_module.MAX_PATH_COMPONENTS) + 1


@pytest.mark.skipif(os.name != "posix", reason="POSIX launcher non-goal")
def test_posix_copied_binary_and_shell_wrapper_remain_non_goals(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_launcher_signals(monkeypatch)
    shell_target = tmp_path / "vendor" / "shell" / "aider"
    shell_target.parent.mkdir(parents=True)
    shell_target.write_text("#!/bin/sh\n")
    shell_target.chmod(0o755)
    binary_target = tmp_path / "vendor" / "binary" / "aider"
    binary_target.parent.mkdir(parents=True)
    binary_target.write_bytes(b"\x7fELFopaque")
    binary_target.chmod(0o755)

    launcher_dir = tmp_path / ".local" / "bin"
    launcher_dir.mkdir(parents=True)
    shell_wrapper = launcher_dir / "netcheck"
    shell_wrapper.write_text(f'#!/bin/sh\nexec "{shell_target}" "$@"\n')
    shell_wrapper.chmod(0o755)
    copied_binary = launcher_dir / "telemetryd"
    copied_binary.write_bytes(binary_target.read_bytes())
    copied_binary.chmod(0o755)

    assert (
        detect_client_presence(
            [_aider_client()],
            home=tmp_path,
            system="Linux",
            environment={},
            hidden_space_result=HiddenSpaceScanResult(),
        )
        == []
    )

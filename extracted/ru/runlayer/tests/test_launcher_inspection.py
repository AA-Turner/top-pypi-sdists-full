"""Safety and parser boundaries for local launcher inspection."""

from __future__ import annotations

import os
from pathlib import Path, PureWindowsPath
import struct
from types import SimpleNamespace

import pytest

from runlayer_cli.scan import launcher_inspection as inspection_module, symlink_identity
from runlayer_cli.scan.bin_shims import sweep_shim_identities
from runlayer_cli.scan.hidden_space_sweep import HiddenLauncherDirectory
from runlayer_cli.scan.launcher_inspection import (
    SHELL_LINK_MAX_PATH_CODE_UNITS,
    inspect_launcher_identities,
    parse_windows_cmd_target,
    parse_windows_shell_link_target,
)


_SHELL_LINK_CLSID = bytes.fromhex("0114020000000000c000000000000046")
_HAS_LINK_TARGET_ID_LIST = 0x00000001
_HAS_RELATIVE_PATH = 0x00000008
_HAS_ARGUMENTS = 0x00000020
_IS_UNICODE = 0x00000080


def _shell_link(relative_target: str, *, extra_flags: int = 0) -> bytes:
    flags = _HAS_RELATIVE_PATH | _IS_UNICODE | extra_flags
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
    encoded = relative_target.encode("utf-16le")
    return header + struct.pack("<H", len(encoded) // 2) + encoded + b"\0\0\0\0"


def test_strict_cmd_parser_accepts_only_static_dp0_forwarder() -> None:
    raw = b'@echo off\r\n@"%~dp0..\\tools\\aider.exe" %*\r\n'

    assert parse_windows_cmd_target(raw) == PureWindowsPath(r"..\tools\aider.exe")
    assert parse_windows_cmd_target(
        b'@echo off\n@"%~dp0..\\tools\\aider.exe" %*\n'
    ) == PureWindowsPath(r"..\tools\aider.exe")
    assert parse_windows_cmd_target(b"\xef\xbb\xbf" + raw) == PureWindowsPath(
        r"..\tools\aider.exe"
    )


@pytest.mark.parametrize(
    "raw",
    [
        b'call "%~dp0..\\tools\\aider.exe" %*\r\n',
        b'"%~dp0..\\tools\\aider.exe" %*\r\n',
        b'@"C:\\tools\\aider.exe" %*\r\n',
        b'@"\\\\server\\share\\aider.exe" %*\r\n',
        b'@"\\tools\\aider.exe" %*\r\n',
        b'@"%~dp0..\\tools\\aider.exe:stream" %*\r\n',
        b'@"%~dp0..\\tools\\aider.exe.exe" %*\r\n',
        b'@"%~dp0..\\tools\\aider.exe. " %*\r\n',
        b'@"%~dp0..\\tools\\aider.exe\\" %*\r\n',
        b'@"%~dp0..\\tools\\aider.exe\\." %*\r\n',
        b'@"%~dp0%OTHER%\\aider.exe" %*\r\n',
        b'@"%~dp0..\\tools\\aider.cmd" %*\r\n',
        b'@"%~dp0..\\tools\\aider.exe" %* & whoami\r\n',
        b'@echo off\r\n@"%~dp0..\\tools\\aider.exe" %*\r\nexit /b\r\n',
        b'\xc3\xa9@"%~dp0..\\tools\\aider.exe" %*\r\n',
        b"\xef\xbb\xbf\xff",
        b"",
    ],
)
def test_strict_cmd_parser_rejects_unsafe_or_dynamic_forms(raw: bytes) -> None:
    assert parse_windows_cmd_target(raw) is None


@pytest.mark.parametrize("target", ["CON.exe", "NUL.exe", "tools\\COM1.exe"])
def test_windows_launcher_parsers_reject_reserved_device_names(target: str) -> None:
    cmd = f'@"%~dp0{target}" %*\r\n'.encode()

    assert parse_windows_cmd_target(cmd) is None
    assert parse_windows_shell_link_target(_shell_link(target)) is None


@pytest.mark.parametrize("separator", [b"\r", b"\v", b"\f", b"\x1c", b"\x1d", b"\x1e"])
def test_strict_cmd_parser_rejects_non_lf_line_separators(separator: bytes) -> None:
    raw = b"@echo off" + separator + b'@"%~dp0..\\tools\\aider.exe" %*' + separator

    assert parse_windows_cmd_target(raw) is None


def test_shell_link_parser_accepts_unicode_relative_path_by_code_units() -> None:
    target = "tools\\\U0001f680\\aider.exe"

    assert parse_windows_shell_link_target(_shell_link(target)) == PureWindowsPath(
        target
    )


def test_shell_link_parser_enforces_max_path_code_units() -> None:
    suffix = "\\aider.exe"
    accepted = "a" * (SHELL_LINK_MAX_PATH_CODE_UNITS - len(suffix)) + suffix
    rejected = "a" + accepted

    assert parse_windows_shell_link_target(_shell_link(accepted)) == PureWindowsPath(
        accepted
    )
    assert parse_windows_shell_link_target(_shell_link(rejected)) is None


@pytest.mark.parametrize(
    "raw",
    [
        b"",
        b"\0" * 75,
        _shell_link(r"tools\aider.exe")[:-1],
        _shell_link(r"tools\aider.exe") + b"\0",
        _shell_link(r"tools\aider.exe", extra_flags=_HAS_LINK_TARGET_ID_LIST),
        _shell_link(r"tools\aider.exe", extra_flags=_HAS_ARGUMENTS),
        _shell_link(r"\\server\share\aider.exe"),
        _shell_link(r"C:\tools\aider.exe"),
        _shell_link(r"\tools\aider.exe"),
        _shell_link(r"tools\aider.exe:stream"),
        _shell_link(r"tools\aider.exe.exe"),
        _shell_link("tools\\aider.exe. "),
        _shell_link("tools\\aider.exe\\"),
        _shell_link("tools\\aider.exe\\."),
    ],
)
def test_shell_link_parser_rejects_unsupported_or_unsafe_forms(raw: bytes) -> None:
    assert parse_windows_shell_link_target(raw) is None


def test_shell_link_parser_rejects_invalid_lengths_and_utf16() -> None:
    valid = bytearray(_shell_link(r"tools\aider.exe"))
    valid[76:78] = struct.pack("<H", 260)
    invalid_utf16 = bytearray(_shell_link(r"tools\aider.exe"))
    invalid_utf16[76:80] = struct.pack("<H", 1) + b"\x00\xd8"
    del invalid_utf16[80:-4]

    assert parse_windows_shell_link_target(bytes(valid)) is None
    assert parse_windows_shell_link_target(bytes(invalid_utf16)) is None


def test_shell_link_parser_never_raises_for_arbitrary_bytes() -> None:
    corpus = [bytes(range(length)) for length in range(0, 256, 7)]
    corpus.extend(
        bytes([value]) * length
        for value in (0, 1, 0x4C, 0x80, 0xFF)
        for length in (1, 4, 75, 76, 77, 256)
    )

    assert all(parse_windows_shell_link_target(raw) is None for raw in corpus)


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
def test_inspection_directory_entry_and_launcher_caps(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directories = []
    for index in range(2):
        directory = tmp_path / f"hidden-{index}" / "bin"
        directory.mkdir(parents=True)
        target = tmp_path / f"target-{index}" / "aider"
        target.parent.mkdir()
        target.write_bytes(b"binary")
        target.chmod(0o755)
        (directory / f"alias-{index}").symlink_to(target)
        directories.append(HiddenLauncherDirectory(path=directory))
    monkeypatch.setattr(symlink_identity, "MAX_IDENTITY_DIRECTORIES", 1)

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Linux",
        hidden_directories=directories,
    )

    assert result.directories == 1
    assert result.entries == 1
    assert result.launchers == 1
    assert result.truncated is True
    assert result.truncation_reason == "directories"


def test_windows_primary_bin_roots_are_inspected_before_hidden_bins(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "tools" / "aider.exe"
    target.parent.mkdir()
    target.write_bytes(b"MZ")
    primary = tmp_path / "AppData" / "Roaming" / "npm"
    primary.mkdir(parents=True)
    (primary / "aider.cmd").write_bytes(
        b'@echo off\r\n@"%~dp0..\\..\\..\\tools\\aider.exe" %*\r\n'
    )
    hidden = tmp_path / ".hidden" / "bin"
    hidden.mkdir(parents=True)
    monkeypatch.setattr(symlink_identity, "MAX_IDENTITY_DIRECTORIES", 1)
    monkeypatch.setattr(
        inspection_module,
        "windows_bin_roots",
        lambda **_kwargs: [primary],
    )

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Windows",
        hidden_directories=[HiddenLauncherDirectory(path=hidden)],
    )

    assert [finding.basename for finding in result.findings] == ["aider"]
    assert result.findings[0].kind == "windows_cmd"


def test_windows_hidden_directories_outside_home_are_counted_as_skipped(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    outside = tmp_path / "wsl-home" / ".hidden" / "bin"
    outside.mkdir(parents=True)
    missing = home / ".gone" / "bin"
    monkeypatch.setattr(inspection_module, "windows_bin_roots", lambda **_kwargs: [])

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=home,
        system="Windows",
        hidden_directories=[
            HiddenLauncherDirectory(path=outside),
            HiddenLauncherDirectory(path=missing),
        ],
    )

    assert result.findings == []
    assert result.hidden_directories_skipped == 2
    assert result.truncated is False


def test_windows_shell_link_inspection_reports_target_identity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "tools" / "aider.exe"
    target.parent.mkdir()
    target.write_bytes(b"MZ")
    primary = tmp_path / "AppData" / "Roaming" / "npm"
    primary.mkdir(parents=True)
    (primary / "renamed.lnk").write_bytes(_shell_link(r"..\..\..\tools\aider.exe"))
    monkeypatch.setattr(
        inspection_module,
        "windows_bin_roots",
        lambda **_kwargs: [primary],
    )

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Windows",
    )

    assert [(finding.basename, finding.kind) for finding in result.findings] == [
        ("aider", "windows_lnk")
    ]


def _counters(result: inspection_module.LauncherInspectionResult) -> dict[str, int]:
    return {
        "unreadable": result.unreadable,
        "unsafe_path": result.unsafe_path,
        "unparsed_grammar": result.unparsed_grammar,
        "unknown_target": result.unknown_target,
    }


def test_windows_npm_cmd_shim_counts_as_unparsed_grammar(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    primary = tmp_path / "AppData" / "Roaming" / "npm"
    primary.mkdir(parents=True)
    (primary / "aider.cmd").write_bytes(
        b"@ECHO off\r\n"
        b"GOTO start\r\n"
        b":find_dp0\r\n"
        b"SET dp0=%~dp0\r\n"
        b"EXIT /b\r\n"
        b":start\r\n"
        b"SETLOCAL\r\n"
        b"CALL :find_dp0\r\n"
        b'IF EXIST "%dp0%\\node.exe" (\r\n'
        b'  SET "_prog=%dp0%\\node.exe"\r\n'
        b") ELSE (\r\n"
        b'  SET "_prog=node"\r\n'
        b"  SET PATHEXT=%PATHEXT:;.JS;=;%\r\n"
        b")\r\n"
        b'endLocal & goto #_undefined_# 2>NUL || title %COMSPEC% & "%_prog%"  '
        b'"%dp0%\\node_modules\\aider\\bin\\aider.js" %*\r\n'
    )
    monkeypatch.setattr(
        inspection_module,
        "windows_bin_roots",
        lambda **_kwargs: [primary],
    )

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Windows",
    )

    assert result.findings == []
    assert result.launchers == 1
    assert _counters(result) == {
        "unreadable": 0,
        "unsafe_path": 0,
        "unparsed_grammar": 1,
        "unknown_target": 0,
    }


def test_windows_forwarder_to_unknown_exe_counts_as_unknown_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "tools" / "other.exe"
    target.parent.mkdir()
    target.write_bytes(b"MZ")
    primary = tmp_path / "AppData" / "Roaming" / "npm"
    primary.mkdir(parents=True)
    (primary / "other.cmd").write_bytes(
        b'@echo off\r\n@"%~dp0..\\..\\..\\tools\\other.exe" %*\r\n'
    )
    monkeypatch.setattr(
        inspection_module,
        "windows_bin_roots",
        lambda **_kwargs: [primary],
    )

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Windows",
    )

    assert result.findings == []
    assert _counters(result) == {
        "unreadable": 0,
        "unsafe_path": 0,
        "unparsed_grammar": 0,
        "unknown_target": 1,
    }


def test_windows_forwarder_escaping_home_counts_as_unsafe_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "home"
    primary = home / "AppData" / "Roaming" / "npm"
    primary.mkdir(parents=True)
    (primary / "aider.cmd").write_bytes(
        b'@echo off\r\n@"%~dp0..\\..\\..\\..\\aider.exe" %*\r\n'
    )
    monkeypatch.setattr(
        inspection_module,
        "windows_bin_roots",
        lambda **_kwargs: [primary],
    )

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=home,
        system="Windows",
    )

    assert result.findings == []
    assert _counters(result) == {
        "unreadable": 0,
        "unsafe_path": 1,
        "unparsed_grammar": 0,
        "unknown_target": 0,
    }


def test_windows_static_roots_are_inspected_before_version_root_listing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "tools" / "aider.exe"
    target.parent.mkdir()
    target.write_bytes(b"MZ")
    primary = tmp_path / "AppData" / "Roaming" / "npm"
    primary.mkdir(parents=True)
    (primary / "aider.cmd").write_bytes(
        b'@echo off\r\n@"%~dp0..\\..\\..\\tools\\aider.exe" %*\r\n'
    )
    clock = [0.0]

    def windows_roots(*, include_versioned, checkpoint=None, **_kwargs):
        if include_versioned:
            clock[0] = inspection_module.MAX_INSPECTION_SECONDS + 1
            assert checkpoint is not None
            checkpoint()
        return [primary]

    monkeypatch.setattr(inspection_module.time, "monotonic", lambda: clock[0])
    monkeypatch.setattr(inspection_module, "windows_bin_roots", windows_roots)

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Windows",
    )

    assert [finding.basename for finding in result.findings] == ["aider"]
    assert result.truncated is True
    assert result.truncation_reason == "deadline"


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
def test_posix_launcher_under_symlinked_home_resolves_target(
    tmp_path: Path,
) -> None:
    actual_home = tmp_path / "actual-home"
    directory = actual_home / ".hidden" / "bin"
    directory.mkdir(parents=True)
    target = actual_home / "tools" / "aider"
    target.parent.mkdir()
    target.write_bytes(b"binary")
    target.chmod(0o755)
    (directory / "alias").symlink_to(Path("../../tools/aider"))
    home = tmp_path / "home"
    home.symlink_to(actual_home, target_is_directory=True)

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=home,
        system="Linux",
        hidden_directories=[HiddenLauncherDirectory(path=home / ".hidden" / "bin")],
    )

    assert [finding.basename for finding in result.findings] == ["aider"]


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
def test_posix_entry_metadata_error_skips_entry_and_keeps_inspecting(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "home"
    directory = home / ".hidden" / "bin"
    directory.mkdir(parents=True)
    target = home / "tools" / "aider"
    target.parent.mkdir()
    target.write_bytes(b"binary")
    target.chmod(0o755)
    (directory / "aaa-unreadable").symlink_to(Path("../../tools/aider"))
    (directory / "zzz-alias").symlink_to(Path("../../tools/aider"))
    original_is_symlink = inspection_module.Path.is_symlink

    def unreadable_is_symlink(self: Path) -> bool:
        if self.name == "aaa-unreadable":
            raise PermissionError(13, "Permission denied", str(self))
        return original_is_symlink(self)

    monkeypatch.setattr(inspection_module.Path, "is_symlink", unreadable_is_symlink)

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=home,
        system="Linux",
        hidden_directories=[HiddenLauncherDirectory(path=directory)],
    )

    assert [finding.basename for finding in result.findings] == ["aider"]
    assert result.unreadable == 1
    assert result.unsafe_path == 0
    assert result.truncated is False
    assert result.truncation_reason is None


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
@pytest.mark.parametrize(
    ("case", "expected"),
    [
        ("chain", True),
        ("cycle", False),
        ("relative", True),
        ("non_executable", False),
    ],
)
def test_posix_launcher_and_shim_sweep_identity_parity(
    tmp_path: Path,
    case: str,
    expected: bool,
) -> None:
    target = tmp_path / "tools" / "aider"
    target.parent.mkdir()
    target.write_bytes(b"binary")
    target.chmod(0o755)
    directory = tmp_path / ".local" / "bin"
    directory.mkdir(parents=True)
    alias = directory / "alias"
    if case == "chain":
        intermediate = tmp_path / "links" / "intermediate"
        intermediate.parent.mkdir()
        intermediate.symlink_to(target)
        alias.symlink_to(intermediate)
    elif case == "cycle":
        intermediate = tmp_path / "links" / "intermediate"
        intermediate.parent.mkdir()
        alias.symlink_to(intermediate)
        intermediate.symlink_to(alias)
    elif case == "relative":
        alias.symlink_to(Path("../../tools/aider"))
    else:
        target.chmod(0o644)
        alias.symlink_to(target)

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Linux",
        hidden_directories=[HiddenLauncherDirectory(path=directory)],
    )
    by_basename, _ = sweep_shim_identities(
        cli_basenames=["aider"],
        npm_packages={},
        home=tmp_path,
        system="Linux",
        environment={},
        include_host_dirs=False,
    )

    assert bool(result.findings) is expected
    assert bool(by_basename.get("aider")) is expected


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
def test_posix_launcher_resolution_is_bounded(
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
    directory = tmp_path / "bin"
    directory.mkdir()
    (directory / "alias").symlink_to(next_target / "aider")
    monkeypatch.setattr(
        inspection_module.os.path,
        "realpath",
        lambda *_args, **_kwargs: pytest.fail("unbounded realpath traversal"),
    )

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Linux",
        hidden_directories=[HiddenLauncherDirectory(path=directory)],
    )

    assert result.findings == []
    assert result.unsafe_path == 1
    assert result.unreadable == 0


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
def test_posix_launcher_and_shim_sweep_share_candidate_budget(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / ".local" / "bin"
    directory.mkdir(parents=True)
    target = tmp_path / "tools" / "aider"
    target.parent.mkdir()
    target.write_bytes(b"binary")
    target.chmod(0o755)
    for name in ("alias-one", "alias-two"):
        (directory / name).symlink_to(target)
    monkeypatch.setattr(symlink_identity, "MAX_IDENTITY_CANDIDATES", 1)

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Linux",
        hidden_directories=[HiddenLauncherDirectory(path=directory)],
    )
    by_basename, _ = sweep_shim_identities(
        cli_basenames=["aider"],
        npm_packages={},
        home=tmp_path,
        system="Linux",
        environment={},
        include_host_dirs=False,
    )

    assert len(result.findings) == 1
    assert len(by_basename["aider"]) == 1
    assert result.truncated is True
    assert result.truncation_reason == "launchers"


@pytest.mark.skipif(os.name != "posix", reason="requires symlinked home")
def test_windows_launcher_under_symlinked_home_is_admitted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actual_home = tmp_path / "actual-home"
    target = actual_home / "tools" / "aider.exe"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"MZ")
    primary = actual_home / "AppData" / "Roaming" / "npm"
    primary.mkdir(parents=True)
    (primary / "aider.cmd").write_bytes(
        b'@echo off\r\n@"%~dp0..\\..\\..\\tools\\aider.exe" %*\r\n'
    )
    home = tmp_path / "home"
    home.symlink_to(actual_home, target_is_directory=True)
    monkeypatch.setattr(
        inspection_module,
        "windows_bin_roots",
        lambda **_kwargs: [home / "AppData" / "Roaming" / "npm"],
    )

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=home,
        system="Windows",
    )

    assert [finding.basename for finding in result.findings] == ["aider"]


def test_inspection_entry_cap_marks_result_incomplete(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / "hidden" / "bin"
    directory.mkdir(parents=True)
    (directory / "one").write_bytes(b"1")
    (directory / "two").write_bytes(b"2")
    monkeypatch.setattr(inspection_module, "MAX_INSPECTION_ENTRIES", 1)

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Linux",
        hidden_directories=[HiddenLauncherDirectory(path=directory)],
    )

    assert result.entries == 1
    assert result.truncated is True
    assert result.truncation_reason == "entries"


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
def test_partial_scandir_error_marks_result_incomplete_and_keeps_findings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / "hidden" / "bin"
    directory.mkdir(parents=True)
    target = tmp_path / "targets" / "aider"
    target.parent.mkdir()
    target.write_bytes(b"binary")
    target.chmod(0o755)
    alias = directory / "alias"
    alias.symlink_to(target)

    class PartialScandir:
        yielded = False

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def __iter__(self):
            return self

        def __next__(self):
            if not self.yielded:
                self.yielded = True
                return SimpleNamespace(path=str(alias), name=alias.name)
            raise OSError("directory changed during iteration")

    monkeypatch.setattr(
        inspection_module.os,
        "scandir",
        lambda _directory: PartialScandir(),
    )

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Linux",
        hidden_directories=[HiddenLauncherDirectory(path=directory)],
    )

    assert [finding.basename for finding in result.findings] == ["aider"]
    assert result.unreadable == 1
    assert result.truncated is True
    assert result.truncation_reason == "directory_error"


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
def test_inspection_launcher_and_finding_caps(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / "hidden" / "bin"
    directory.mkdir(parents=True)
    for basename in ("aider", "codex"):
        target = tmp_path / "targets" / basename
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(b"binary")
        target.chmod(0o755)
        (directory / f"{basename}-alias").symlink_to(target)
    monkeypatch.setattr(inspection_module, "MAX_RETAINED_FINDINGS", 1)

    result = inspect_launcher_identities(
        known_basenames=["aider", "codex"],
        home=tmp_path,
        system="Linux",
        hidden_directories=[HiddenLauncherDirectory(path=directory)],
    )

    assert len(result.findings) == 1
    assert result.launchers == 2
    assert result.truncated is True
    assert result.truncation_reason == "findings"

    monkeypatch.setattr(symlink_identity, "MAX_IDENTITY_CANDIDATES", 1)
    launcher_limited = inspect_launcher_identities(
        known_basenames=["aider", "codex"],
        home=tmp_path,
        system="Linux",
        hidden_directories=[HiddenLauncherDirectory(path=directory)],
    )

    assert launcher_limited.launchers == 1
    assert launcher_limited.truncated is True
    assert launcher_limited.truncation_reason == "launchers"


def test_inspection_aggregate_byte_cap_and_checkpoint(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "target" / "aider.exe"
    target.parent.mkdir()
    target.write_bytes(b"MZ")
    launcher = tmp_path / "AppData" / "Roaming" / "npm" / "alias.cmd"
    launcher.parent.mkdir(parents=True)
    launcher.write_bytes(b'@echo off\r\n@"%~dp0..\\..\\..\\target\\aider.exe" %*\r\n')
    monkeypatch.setattr(inspection_module, "MAX_AGGREGATE_BYTES", 0)
    checkpoints = 0

    def checkpoint() -> None:
        nonlocal checkpoints
        checkpoints += 1

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Windows",
        checkpoint=checkpoint,
    )

    assert result.findings == []
    assert result.bytes_read == 0
    assert result.truncated is True
    assert result.truncation_reason == "aggregate_bytes"
    assert checkpoints > 0


def test_inspection_deadline_stops_before_filesystem_access(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / "hidden" / "bin"
    directory.mkdir(parents=True)
    monotonic_values = iter((0.0, 6.0))
    monkeypatch.setattr(
        inspection_module.time,
        "monotonic",
        lambda: next(monotonic_values, 6.0),
    )

    result = inspect_launcher_identities(
        known_basenames=["aider"],
        home=tmp_path,
        system="Linux",
        hidden_directories=[HiddenLauncherDirectory(path=directory)],
    )

    assert result.directories == 0
    assert result.truncated is True
    assert result.truncation_reason == "deadline"


def test_windows_candidate_deadline_is_not_counted_as_malformed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result = inspection_module.LauncherInspectionResult()
    budget = inspection_module._InspectionBudget(
        result=result,
        checkpoint_callback=None,
        deadline=1.0,
    )
    readings = iter((0.0, 2.0))
    monkeypatch.setattr(
        inspection_module.time,
        "monotonic",
        lambda: next(readings, 2.0),
    )
    monkeypatch.setattr(inspection_module, "_safe_user_path", lambda *_args: True)
    monkeypatch.setattr(
        inspection_module,
        "is_link_or_reparse",
        lambda *_args: False,
    )
    monkeypatch.setattr(inspection_module, "is_regular_file", lambda *_args: True)

    inspection_module._inspect_windows_candidate(
        tmp_path / "aider.cmd",
        kind="cmd",
        home=tmp_path,
        known_basenames={"aider": "aider"},
        budget=budget,
    )

    assert result.truncated is True
    assert result.truncation_reason == "deadline"
    assert _counters(result) == {
        "unreadable": 0,
        "unsafe_path": 0,
        "unparsed_grammar": 0,
        "unknown_target": 0,
    }


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
def test_posix_candidate_deadline_is_not_counted_as_malformed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "aider"
    target.write_text("#!/bin/sh\n")
    launcher = tmp_path / "renamed"
    launcher.symlink_to(target)
    result = inspection_module.LauncherInspectionResult()
    budget = inspection_module._InspectionBudget(
        result=result,
        checkpoint_callback=None,
        deadline=1.0,
    )
    readings = iter((0.0, 2.0))
    monkeypatch.setattr(
        inspection_module.time,
        "monotonic",
        lambda: next(readings, 2.0),
    )

    def _resolve_at_deadline(
        _path: Path,
        *,
        known_basenames: frozenset[str],
        checkpoint,
    ):
        assert known_basenames == frozenset({"aider"})
        assert checkpoint() is False
        return None

    monkeypatch.setattr(
        inspection_module.symlink_identity,
        "resolve_posix_symlink_identity",
        _resolve_at_deadline,
    )

    inspection_module._inspect_posix_symlink(
        launcher,
        known_posix_basenames=frozenset({"aider"}),
        budget=budget,
    )

    assert result.truncated is True
    assert result.truncation_reason == "deadline"
    assert _counters(result) == {
        "unreadable": 0,
        "unsafe_path": 0,
        "unparsed_grammar": 0,
        "unknown_target": 0,
    }

"""Tests for locating CLI binaries and reading their versions."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest

from runlayer_cli.scan.cli_binaries import (
    _nvm_bin_roots,
    _resolved_from_path,
    get_cli_version,
    locate_cli_binary,
)

posix_only = pytest.mark.skipif(os.name != "posix", reason="POSIX ownership gate")


def _make_binary(tmp_path: Path) -> Path:
    binary = tmp_path / "test-cli"
    binary.write_text("#!/bin/sh\necho test-cli 3.0\n")
    binary.chmod(0o755)
    return binary


def test_locate_cli_binary_prefers_path(monkeypatch):
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: "/usr/bin/test-cli",
    )

    assert locate_cli_binary("test-cli") == Path("/usr/bin/test-cli")


def test_locate_cli_binary_falls_back_to_common_bin_dirs(tmp_path, monkeypatch):
    binary = tmp_path / ".local" / "bin" / "test-cli"
    binary.parent.mkdir(parents=True)
    binary.write_text("#!/bin/sh\n")
    binary.chmod(0o755)
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )

    assert locate_cli_binary("test-cli", home=tmp_path, system="Linux") == binary


def test_locate_cli_binary_finds_claude_native_install(tmp_path, monkeypatch):
    binary = tmp_path / ".claude" / "local" / "claude"
    binary.parent.mkdir(parents=True)
    binary.write_text("#!/bin/sh\n")
    binary.chmod(0o755)
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )

    assert locate_cli_binary("claude", home=tmp_path, system="Darwin") == binary


def test_locate_cli_binary_finds_nvm_version_install(tmp_path, monkeypatch):
    binary = tmp_path / ".nvm" / "versions" / "node" / "v22.14.0" / "bin" / "claude"
    binary.parent.mkdir(parents=True)
    binary.write_text("#!/bin/sh\n")
    binary.chmod(0o755)
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )

    assert locate_cli_binary("claude", home=tmp_path, system="Darwin") == binary


def test_nvm_version_roots_are_bounded_at_enumeration(tmp_path, monkeypatch):
    versions = tmp_path / ".nvm" / "versions" / "node"
    for index in range(128):
        (versions / f"v{index}" / "bin").mkdir(parents=True)

    listed = 0
    real_scandir = os.scandir

    class CountingScandir:
        def __init__(self, path: Path | str) -> None:
            self._iterator = real_scandir(path)

        def __enter__(self):
            self._iterator.__enter__()
            return self

        def __exit__(self, *exc):
            return self._iterator.__exit__(*exc)

        def __iter__(self):
            for entry in self._iterator:
                nonlocal listed
                listed += 1
                yield entry

    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.os.scandir",
        CountingScandir,
    )

    roots = _nvm_bin_roots(tmp_path)

    assert listed == 64
    assert len(roots) == 64
    assert all(root.name == "bin" for root in roots)


def test_nvm_version_roots_sort_the_bounded_listing(tmp_path, monkeypatch):
    versions = tmp_path / ".nvm" / "versions" / "node"
    entries = []
    for index in range(65):
        version = versions / f"v{index:03d}"
        (version / "bin").mkdir(parents=True)
        entries.append(mock.Mock(path=str(version)))
    listed: list[str] = []

    def listing():
        for entry in reversed(entries):
            listed.append(entry.path)
            yield entry

    scandir = mock.MagicMock()
    scandir.return_value.__enter__.return_value = listing()
    monkeypatch.setattr("runlayer_cli.scan.cli_binaries.os.scandir", scandir)

    roots = _nvm_bin_roots(tmp_path)

    assert len(listed) == 64
    assert roots == sorted(Path(path) / "bin" for path in listed)


def test_locate_cli_binary_finds_windows_npm_global_install(tmp_path, monkeypatch):
    binary = tmp_path / "AppData" / "Roaming" / "npm" / "copilot.cmd"
    binary.parent.mkdir(parents=True)
    binary.write_text("@echo off\n")
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )

    assert locate_cli_binary("copilot", home=tmp_path, system="Windows") == binary


def test_locate_cli_binary_finds_windows_nvm_version_install(tmp_path, monkeypatch):
    binary = tmp_path / "AppData" / "Roaming" / "nvm" / "v22.14.0" / "copilot.cmd"
    binary.parent.mkdir(parents=True)
    binary.write_text("@echo off\n")
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )

    assert locate_cli_binary("copilot", home=tmp_path, system="Windows") == binary


def test_locate_cli_binary_ignores_windows_non_executable_suffix(tmp_path, monkeypatch):
    binary = tmp_path / "AppData" / "Roaming" / "npm" / "copilot.ps1"
    binary.parent.mkdir(parents=True)
    binary.write_text("# powershell shim\n")
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )

    assert locate_cli_binary("copilot", home=tmp_path, system="Windows") is None


def test_locate_cli_binary_returns_none_when_absent(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )

    assert locate_cli_binary("test-cli", home=tmp_path, system="Linux") is None


def test_cli_version_subprocess_has_five_second_timeout(tmp_path):
    binary = _make_binary(tmp_path)
    completed = subprocess.CompletedProcess(
        args=["test-cli", "--version"],
        returncode=0,
        stdout="test-cli 3.0\n",
        stderr="",
    )
    with mock.patch(
        "runlayer_cli.scan.cli_binaries.subprocess.run",
        return_value=completed,
    ) as run:
        assert get_cli_version(binary) == "test-cli 3.0"

    run.assert_called_once_with(
        [str(binary), "--version"],
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )


@posix_only
def test_cli_version_skips_world_writable_binary(tmp_path):
    binary = _make_binary(tmp_path)
    binary.chmod(0o757)

    with mock.patch("runlayer_cli.scan.cli_binaries.subprocess.run") as run:
        assert get_cli_version(binary) is None

    run.assert_not_called()


@posix_only
def test_cli_version_skips_binary_owned_by_another_user(tmp_path, monkeypatch):
    binary = _make_binary(tmp_path)
    foreign_euid = os.geteuid() + 12345
    monkeypatch.setattr(os, "geteuid", lambda: foreign_euid, raising=False)

    with mock.patch("runlayer_cli.scan.cli_binaries.subprocess.run") as run:
        assert get_cli_version(binary) is None

    run.assert_not_called()


def test_resolved_from_path_accepts_path_resolution(tmp_path, monkeypatch):
    binary = tmp_path / "copilot.cmd"
    binary.write_text("@echo off\n")
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: str(binary),
    )

    assert _resolved_from_path(binary)


def test_resolved_from_path_rejects_user_writable_fallback(tmp_path, monkeypatch):
    """%APPDATA%\\npm is writable by the user, so SYSTEM must not execute it."""
    binary = tmp_path / "AppData" / "Roaming" / "npm" / "copilot.cmd"
    binary.parent.mkdir(parents=True)
    binary.write_text("@echo off\n")
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: None,
    )

    assert not _resolved_from_path(binary)


def test_resolved_from_path_rejects_shadowed_name(tmp_path, monkeypatch):
    binary = tmp_path / "npm" / "copilot.cmd"
    binary.parent.mkdir(parents=True)
    binary.write_text("@echo off\n")
    other = tmp_path / "copilot.cmd"
    other.write_text("@echo off\n")
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries.shutil.which",
        lambda _binary: str(other),
    )

    assert not _resolved_from_path(binary)


@pytest.mark.parametrize("resolves", [True, False])
def test_cli_version_gates_non_posix_execution_on_path(tmp_path, monkeypatch, resolves):
    binary = _make_binary(tmp_path)
    monkeypatch.setattr("runlayer_cli.scan.cli_binaries.os", SimpleNamespace(name="nt"))
    monkeypatch.setattr(
        "runlayer_cli.scan.cli_binaries._resolved_from_path",
        lambda _path: resolves,
    )
    completed = subprocess.CompletedProcess(
        args=[str(binary), "--version"],
        returncode=0,
        stdout="test-cli 3.0\n",
        stderr="",
    )

    with mock.patch(
        "runlayer_cli.scan.cli_binaries.subprocess.run",
        return_value=completed,
    ) as run:
        version = get_cli_version(binary)

    assert version == ("test-cli 3.0" if resolves else None)
    assert run.called is resolves


def test_cli_version_skips_missing_binary():
    with mock.patch("runlayer_cli.scan.cli_binaries.subprocess.run") as run:
        assert get_cli_version(Path("/nonexistent/test-cli")) is None

    if os.name == "posix":
        run.assert_not_called()

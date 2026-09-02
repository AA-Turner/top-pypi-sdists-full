from __future__ import annotations

import os
import stat
from pathlib import Path

import pytest

from runlayer_cli.uv_tool_cleanup import (
    cleanup_uv_tool,
    uv_tool_cleanup_completed,
    uv_tool_removed_marker_path,
    write_uv_tool_removed_marker,
)


def _write(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


class _ReparseStat:
    st_file_attributes = stat.FILE_ATTRIBUTE_REPARSE_POINT

    def __init__(self, result: os.stat_result) -> None:
        self._result = result

    def __getattr__(self, name: str) -> object:
        return getattr(self._result, name)


def _mark_as_reparse_point(
    monkeypatch: pytest.MonkeyPatch,
    reparse_path: Path,
) -> None:
    original_lstat = os.lstat

    def reparse_lstat(path: os.PathLike[str] | str, *args: object, **kwargs: object):
        result = original_lstat(path, *args, **kwargs)
        return _ReparseStat(result) if Path(path) == reparse_path else result

    monkeypatch.setattr(os, "lstat", reparse_lstat)


def test_posix_removes_verified_shim_and_custom_uv_tool_dir(tmp_path: Path) -> None:
    home = tmp_path / "home"
    tool_dir = tmp_path / "xdg" / "uv" / "tools" / "runlayer"
    target = tool_dir / "bin" / "runlayer"
    shim = home / ".local" / "bin" / "runlayer"
    _write(target, "#!/bin/sh\n")
    shim.parent.mkdir(parents=True)
    shim.symlink_to(target)

    assert cleanup_uv_tool(home=home, system="Darwin") is True

    assert not shim.exists()
    assert not shim.is_symlink()
    assert not tool_dir.exists()


def test_posix_leaves_non_uv_symlink_untouched(tmp_path: Path) -> None:
    home = tmp_path / "home"
    target = tmp_path / "other" / "bin" / "runlayer"
    shim = home / ".local" / "bin" / "runlayer"
    _write(target)
    shim.parent.mkdir(parents=True)
    shim.symlink_to(target)

    assert cleanup_uv_tool(home=home, system="Linux") is False

    assert shim.is_symlink()
    assert target.exists()


def test_posix_leaves_regular_runlayer_file_untouched(tmp_path: Path) -> None:
    home = tmp_path / "home"
    shim = home / ".local" / "bin" / "runlayer"
    _write(shim, "not uv")

    assert cleanup_uv_tool(home=home, system="Linux") is False
    assert shim.read_text() == "not uv"


def test_posix_removes_default_tool_dir_without_shim(tmp_path: Path) -> None:
    home = tmp_path / "home"
    tool_dir = home / ".local" / "share" / "uv" / "tools" / "runlayer"
    _write(tool_dir / "bin" / "runlayer")

    assert cleanup_uv_tool(home=home, system="Linux") is True
    assert not tool_dir.exists()
    assert cleanup_uv_tool(home=home, system="Linux") is False


def test_windows_requires_uv_tool_dir_before_removing_trampoline(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    appdata = home / "AppData" / "Roaming"
    shim = home / ".local" / "bin" / "runlayer.exe"
    _write(shim, "trampoline")

    assert cleanup_uv_tool(home=home, system="Windows", appdata=appdata) is False
    assert shim.exists()

    tool_dir = appdata / "uv" / "tools" / "runlayer"
    _write(tool_dir / "Scripts" / "runlayer.exe")

    assert cleanup_uv_tool(home=home, system="Windows", appdata=appdata) is True
    assert not shim.exists()
    assert not tool_dir.exists()


def test_windows_leaves_reparse_tool_dir_untouched(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "home"
    appdata = home / "AppData" / "Roaming"
    tool_dir = appdata / "uv" / "tools" / "runlayer"
    shim = home / ".local" / "bin" / "runlayer.exe"
    _write(tool_dir / "Scripts" / "runlayer.exe")
    _write(shim, "trampoline")
    _mark_as_reparse_point(monkeypatch, tool_dir)

    assert cleanup_uv_tool(home=home, system="Windows", appdata=appdata) is False
    assert shim.exists()
    assert tool_dir.exists()


def test_windows_leaves_tool_dir_untouched_when_parent_is_reparse(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "home"
    appdata = home / "AppData" / "Roaming"
    uv_dir = appdata / "uv"
    tool_dir = uv_dir / "tools" / "runlayer"
    shim = home / ".local" / "bin" / "runlayer.exe"
    _write(tool_dir / "Scripts" / "runlayer.exe")
    _write(shim, "trampoline")
    _mark_as_reparse_point(monkeypatch, uv_dir)

    assert cleanup_uv_tool(home=home, system="Windows", appdata=appdata) is False
    assert shim.exists()
    assert tool_dir.exists()


def test_windows_rechecks_reparse_points_before_deletion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    home = tmp_path / "home"
    appdata = home / "AppData" / "Roaming"
    tool_dir = appdata / "uv" / "tools" / "runlayer"
    shim = home / ".local" / "bin" / "runlayer.exe"
    _write(tool_dir / "Scripts" / "runlayer.exe")
    _write(shim, "trampoline")
    original_lstat = os.lstat
    tool_dir_checks = 0

    def changing_lstat(
        path: os.PathLike[str] | str,
        *args: object,
        **kwargs: object,
    ):
        nonlocal tool_dir_checks
        result = original_lstat(path, *args, **kwargs)
        if Path(path) == tool_dir:
            tool_dir_checks += 1
            if tool_dir_checks > 1:
                return _ReparseStat(result)
        return result

    monkeypatch.setattr(os, "lstat", changing_lstat)

    assert cleanup_uv_tool(home=home, system="Windows", appdata=appdata) is True
    assert not shim.exists()
    assert tool_dir.exists()


def test_marker_is_best_effort_and_per_user(tmp_path: Path) -> None:
    home = tmp_path / "home"

    assert uv_tool_cleanup_completed(home=home) is False
    write_uv_tool_removed_marker(home=home)

    assert uv_tool_cleanup_completed(home=home) is True
    assert uv_tool_removed_marker_path(home=home).is_file()

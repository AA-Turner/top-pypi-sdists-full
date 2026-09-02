"""Best-effort removal of a legacy uv-tool-installed Runlayer CLI."""

from __future__ import annotations

import os
import platform
import shutil
import stat
from pathlib import Path

UV_TOOL_REMOVED_MARKER = ".uv-tool-removed"


def cleanup_uv_tool(
    *,
    home: Path | None = None,
    system: str | None = None,
    appdata: Path | None = None,
) -> bool:
    """Remove the current user's uv tool install when its origin is verified."""
    user_home = home if home is not None else Path.home()
    current_system = system if system is not None else platform.system()
    if current_system == "Windows":
        return _cleanup_windows(user_home, appdata=appdata)
    return _cleanup_posix(user_home)


def uv_tool_removed_marker_path(*, home: Path | None = None) -> Path:
    user_home = home if home is not None else Path.home()
    return user_home / ".runlayer" / UV_TOOL_REMOVED_MARKER


def uv_tool_cleanup_completed(*, home: Path | None = None) -> bool:
    try:
        return uv_tool_removed_marker_path(home=home).is_file()
    except OSError:
        return False


def write_uv_tool_removed_marker(*, home: Path | None = None) -> None:
    """Record a completed cleanup attempt without surfacing filesystem errors."""
    marker = uv_tool_removed_marker_path(home=home)
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch(exist_ok=True)
        os.utime(marker, None)
    except OSError:
        pass


def _cleanup_posix(home: Path) -> bool:
    """Run as the owning user; packaging scripts harden privileged cleanup."""
    shim = home / ".local" / "bin" / "runlayer"
    resolved_tool_dir: Path | None = None
    try:
        if shim.is_symlink():
            resolved_tool_dir = _uv_tool_dir_for_target(shim.resolve(strict=False))
    except (OSError, RuntimeError):
        resolved_tool_dir = None

    removed = False
    if resolved_tool_dir is not None:
        removed = _remove_tree(resolved_tool_dir) or removed
        removed = _unlink(shim) or removed

    default_tool_dir = home / ".local" / "share" / "uv" / "tools" / "runlayer"
    removed = _remove_tree(default_tool_dir) or removed
    return removed


def _cleanup_windows(home: Path, *, appdata: Path | None) -> bool:
    roaming = appdata
    if roaming is None:
        configured_appdata = os.environ.get("APPDATA")
        roaming = (
            Path(configured_appdata)
            if configured_appdata
            else home / "AppData" / "Roaming"
        )

    tool_dir = roaming / "uv" / "tools" / "runlayer"
    try:
        uv_origin_verified = (
            not _has_windows_reparse_component(roaming, tool_dir) and tool_dir.is_dir()
        )
    except OSError:
        uv_origin_verified = False
    if not uv_origin_verified:
        return False

    removed = False
    shim = home / ".local" / "bin" / "runlayer.exe"
    try:
        if shim.is_file() or shim.is_symlink():
            removed = _unlink(shim) or removed
    except OSError:
        pass
    removed = _remove_tree(tool_dir, reparse_boundary=roaming) or removed
    return removed


def _has_windows_reparse_component(boundary: Path, target: Path) -> bool:
    candidates = [boundary]
    candidate = boundary
    for part in target.relative_to(boundary).parts:
        candidate /= part
        candidates.append(candidate)

    for candidate in candidates:
        try:
            attributes = getattr(os.lstat(candidate), "st_file_attributes", 0)
        except FileNotFoundError:
            continue
        if attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            return True
    return False


def _uv_tool_dir_for_target(target: Path) -> Path | None:
    for candidate in (target, *target.parents):
        if (
            candidate.name == "runlayer"
            and candidate.parent.name == "tools"
            and candidate.parent.parent.name == "uv"
        ):
            return candidate
    return None


def _remove_tree(path: Path, *, reparse_boundary: Path | None = None) -> bool:
    try:
        if reparse_boundary is not None and _has_windows_reparse_component(
            reparse_boundary, path
        ):
            return False
        if path.is_symlink():
            path.unlink()
            return True
        if path.is_dir():
            shutil.rmtree(path)
            return True
    except OSError:
        pass
    return False


def _unlink(path: Path) -> bool:
    try:
        path.unlink()
        return True
    except OSError:
        return False

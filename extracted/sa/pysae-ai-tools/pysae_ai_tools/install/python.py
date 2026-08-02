"""Install Python (3.14, the version Pysae projects target) via uv.

uv manages the Python interpreter download. The runtime itself lands under
``~/.local/share/uv/python/cpython-3.14.X-...`` (Linux/macOS) or
``%APPDATA%\\uv\\python\\cpython-3.14-...`` (Windows) and stays invokable
through ``uv run --python 3.14`` regardless of the shim state.

This tool is OPTIONAL but ``default_selected=True`` — the package targets
3.14 (see CLAUDE.md), so most users want it pinned locally.

Install passes ``--default --preview-features python-install-default`` so
uv writes the ``python`` / ``python3`` / ``python3.14`` shims itself —
no custom .cmd wrapper, uv stays the single source of truth for which
interpreter the shims resolve to (a patch-level upgrade just keeps
working).

On Windows the install also removes the Microsoft Store App Execution
Alias stubs at ``%LOCALAPPDATA%\\Microsoft\\WindowsApps\\python.exe`` so
they cannot hijack ``python`` calls to open the Store dialog ahead of
uv's shim on PATH. ``get_state`` reports ``needs_update=True`` whenever
those stubs are still present, so re-running ``tools install`` is enough
to repair the Windows side-car cleanup.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import typer

from .common.base import BaseTool, InstallReport, ToolState

PYTHON_TARGET = "3.14"

_MS_STORE_PYTHON_STUBS = ("python.exe", "python3.exe")

# Match every uv-managed cpython 3.14.x build, regardless of platform suffix.
_VERSION_RE = re.compile(r"cpython-(3\.14\.\d+)")


def _uv_path() -> str:
    return shutil.which("uv") or ""


def _uv_python_list_installed() -> list[str]:
    """Return non-empty lines from ``uv python list --only-installed``."""
    uv = _uv_path()
    if not uv:
        return []
    try:
        r = subprocess.run(
            [uv, "python", "list", "--only-installed"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if r.returncode != 0:
        return []
    return [line for line in r.stdout.splitlines() if line.strip()]


def _installed_target_version() -> str:
    """Return the highest installed 3.14.x version, or '' when none."""
    versions: list[str] = []
    for line in _uv_python_list_installed():
        match = _VERSION_RE.search(line)
        if match:
            versions.append(match.group(1))
    if not versions:
        return ""
    return max(versions, key=lambda v: tuple(int(x) for x in v.split(".")))


def _ms_store_python_stub_dir() -> Path | None:
    """Directory holding the Microsoft Store App Execution Alias stubs."""
    if sys.platform != "win32":
        return None
    local_app = os.environ.get("LOCALAPPDATA")
    if not local_app:
        return None
    apps_dir = Path(local_app) / "Microsoft" / "WindowsApps"
    return apps_dir if apps_dir.exists() else None


def _detect_ms_store_python_stubs() -> list[Path]:
    """Return any present 0-byte python alias stubs in WindowsApps.

    Uses :func:`os.lstat` (not ``Path.stat``) so the call doesn't follow
    the reparse point — App Execution Aliases on Windows reliably report
    ``st_size == 0`` for the link itself but ``stat`` may return the
    target launcher's size on newer Pythons, breaking the heuristic.
    """
    apps_dir = _ms_store_python_stub_dir()
    if apps_dir is None:
        return []
    stubs: list[Path] = []
    for name in _MS_STORE_PYTHON_STUBS:
        stub = apps_dir / name
        try:
            info = os.lstat(stub)
        except (FileNotFoundError, OSError):
            continue
        if info.st_size == 0:
            stubs.append(stub)
    return stubs


def _remove_ms_store_python_stubs() -> list[str]:
    """Delete every detected ``python.exe`` / ``python3.exe`` alias stub.

    Idempotent and best-effort: permission errors are swallowed — the
    caller can tell from the returned list how many were actually
    cleared.
    """
    removed: list[str] = []
    for stub in _detect_ms_store_python_stubs():
        try:
            stub.unlink()
        except OSError:
            continue
        removed.append(str(stub))
    return removed


def _uv_python_path(version_hint: str) -> str:
    """Best-effort: return the path uv resolves for ``version_hint``."""
    uv = _uv_path()
    if not uv:
        return ""
    try:
        r = subprocess.run(
            [uv, "python", "find", version_hint],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if r.returncode != 0:
        return ""
    return r.stdout.strip()


class PythonTool(BaseTool):
    name = "python"
    cli_help = f"Install Python {PYTHON_TARGET} via uv"

    def get_state(self) -> ToolState:
        uv = _uv_path()
        version = _installed_target_version() if uv else ""
        installed = bool(version)
        path = _uv_python_path(PYTHON_TARGET) if installed else ""

        stubs = [str(s) for s in _detect_ms_store_python_stubs()]

        # Trigger a re-run whenever Windows stubs are still in place even
        # though the interpreter is already installed — `do_install` is
        # what removes them.
        post_install_dirty = installed and bool(stubs)

        return ToolState(
            needs_install=not installed,
            needs_update=post_install_dirty,
            extra={
                "binary": {
                    "name": f"python{PYTHON_TARGET}",
                    "installed": installed,
                    "path": path,
                    "version": version,
                },
                "uv_available": bool(uv),
                "target": PYTHON_TARGET,
                "ms_store_stubs": stubs,
            },
        )

    def do_install(self) -> InstallReport:
        uv = _uv_path()
        if not uv:
            return InstallReport(
                error="uv not found on PATH — re-run install.sh / install.ps1 to bootstrap uv first",
            )

        # Skip the uv install entirely when the interpreter is already at
        # the target version — re-running it is a no-op for the bytes on
        # disk, but ``get_state`` may have triggered us only to repair the
        # Microsoft Store stub side-car. Avoid the 30-60 s no-op cost.
        already_installed = bool(_installed_target_version())

        if not already_installed:
            # ``--default --preview-features python-install-default`` makes
            # uv create the ``python`` / ``python3`` / ``python3.14`` shims
            # itself under its bin dir (which install.cmd has already added
            # to PATH ahead of WindowsApps).
            try:
                r = subprocess.run(
                    [
                        uv,
                        "python",
                        "install",
                        PYTHON_TARGET,
                        "--default",
                        "--preview-features",
                        "python-install-default",
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    check=False,
                    timeout=600,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                return InstallReport(error=f"uv python install: {exc}")
            if r.returncode != 0:
                return InstallReport(error=(r.stderr or r.stdout).strip()[:500])

        version = _installed_target_version() or PYTHON_TARGET
        path = _uv_python_path(PYTHON_TARGET)
        report = InstallReport(
            version=version,
            path=path,
            method="uv (already up-to-date)" if already_installed else "uv",
        )

        removed_stubs = _remove_ms_store_python_stubs()
        if removed_stubs:
            report.extra["ms_store_stubs_removed"] = removed_stubs
        return report

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        if not state.get("uv_available", True):
            return [("✗ uv not on PATH", typer.colors.RED)]
        target = state.get("target", PYTHON_TARGET)
        return [(f"target: {target}", typer.colors.BRIGHT_BLACK)]

    def format_check(self, state: ToolState) -> None:
        d = state.to_dict()
        bin_info = d.get("binary", {})
        if isinstance(bin_info, dict) and bin_info.get("installed"):
            typer.echo(f"python {PYTHON_TARGET}: {bin_info.get('version')} (managed by uv)")
        else:
            typer.echo(f"python {PYTHON_TARGET}: NOT installed")

    def format_install(self, report: InstallReport) -> None:
        if report.error:
            typer.echo(f"FAILED: {report.error}", err=True)
            return
        line = f"python {PYTHON_TARGET} installed"
        if report.version:
            line += f" ({report.version})"
        if report.method:
            line += f" via {report.method}"
        typer.echo(line)
        if report.path:
            typer.echo(f"  path: {report.path}")
        removed = report.extra.get("ms_store_stubs_removed")
        if isinstance(removed, list) and removed:
            count = len(removed)
            typer.echo(f"  removed {count} Microsoft Store python stub{'s' if count > 1 else ''}")


tool = PythonTool()

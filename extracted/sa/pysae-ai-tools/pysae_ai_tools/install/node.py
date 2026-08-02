"""Install Node.js (LTS).

Behavior:

- If a ``node`` binary is already on PATH (any source — apt, brew, manual,
  fnm, …) the tool reports up-to-date and leaves it alone.
- Otherwise, it ensures fnm is present (delegating to the ``fnm`` install
  module if needed), then runs ``fnm install --lts && fnm default lts-latest``.

This is REQUIRED — most Pysae JS tooling assumes a Node runtime is reachable.
"""

import subprocess
from typing import Any

import httpx
import typer

from . import fnm as fnm_module
from .common import binary, platform
from .common.base import BinaryTool, InstallReport, ToolState

NODE_DIST_INDEX = "https://nodejs.org/dist/index.json"


def _latest_lts_version() -> str:
    """Return the latest Node.js LTS version (without leading ``v``)."""
    try:
        r = httpx.get(NODE_DIST_INDEX, timeout=10.0, follow_redirects=True)
        r.raise_for_status()
        data = r.json()
    except (httpx.HTTPError, ValueError):
        return ""
    if not isinstance(data, list):
        return ""
    for entry in data:
        if isinstance(entry, dict) and entry.get("lts"):
            version = entry.get("version", "")
            if isinstance(version, str):
                return version.lstrip("v")
    return ""


def _ensure_fnm() -> tuple[str, InstallReport]:
    """Make sure fnm is present, installing it transparently if not.

    Returns ``(fnm_path, report)`` — ``fnm_path`` is empty when fnm couldn't
    be installed, in which case ``report.error`` is set.
    """
    located = fnm_module.find_fnm()
    if located:
        return located, InstallReport(method="already installed")

    report = fnm_module.tool.do_install()
    if report.error:
        return "", report

    fnm_module.augment_path()
    located = fnm_module.find_fnm()
    if not located:
        return "", InstallReport(error="fnm not found after install")
    return located, report


def _fnm_install_lts(fnm: str) -> tuple[str, str]:
    """Run ``fnm install --lts`` then pin ``fnm default`` to the resolved version.

    The default alias is set to the concrete version that ``fnm install --lts``
    just installed (e.g. ``v22.11.0``) — not the floating ``lts-latest``
    label — so the user's default Node only moves when they explicitly
    re-run the install.

    Returns ``(node_version, error_message)`` — empty error on success.
    """
    try:
        r = subprocess.run(
            [fnm, "install", "--lts"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=300,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "", f"fnm install --lts: {exc}"
    if r.returncode != 0:
        return "", (r.stderr or r.stdout).strip()[:500] or "fnm install --lts failed"

    try:
        check = subprocess.run(
            [fnm, "exec", "--using=lts-latest", "--", "node", "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "", f"node version check failed: {exc}"
    version = binary.extract_version(check.stdout) or check.stdout.strip().lstrip("v")
    if not version:
        return "", "could not determine installed Node version"

    try:
        r = subprocess.run(
            [fnm, "default", f"v{version}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "", f"fnm default v{version}: {exc}"
    if r.returncode != 0:
        return "", (r.stderr or r.stdout).strip()[:500] or f"fnm default v{version} failed"

    return version, ""


class NodeTool(BinaryTool):
    name = "node"
    binary_name = "node"
    cli_help = "Install Node.js (LTS) — uses fnm when node is missing"

    def fetch_latest_version(self) -> str:
        return _latest_lts_version()

    def get_state(self) -> ToolState:
        # Surface fnm-managed binaries even when the current shell hasn't
        # sourced the fnm init yet, otherwise fresh fnm-installed Node looks
        # missing.
        fnm_module.augment_path()
        state = super().get_state()
        state.extra["fnm_path"] = fnm_module.find_fnm()
        return state

    def install_linux(self, plat: platform.Platform) -> InstallReport:
        return self._do(plat)

    def install_macos(self, plat: platform.Platform) -> InstallReport:
        return self._do(plat)

    def install_windows(self, plat: platform.Platform) -> InstallReport:
        return self._do(plat)

    def _do(self, plat: platform.Platform) -> InstallReport:
        # The framework only calls install when ``get_state`` flagged
        # ``needs_install`` or ``needs_update`` — so we always go through fnm
        # to install (or bump) the LTS line and re-pin the default. Existing
        # ``node`` binaries from other channels (apt, brew) get superseded
        # in new shells via the fnm shell init wired by the ``fnm`` tool.
        fnm_path, fnm_report = _ensure_fnm()
        if fnm_report.error:
            return InstallReport(error=f"could not install fnm: {fnm_report.error}")

        version, err = _fnm_install_lts(fnm_path)
        if err:
            return InstallReport(error=err)

        return InstallReport(
            version=version,
            method="fnm",
            extra={"fnm": fnm_report.method or "installed"},
        )

    def do_install(self) -> InstallReport:
        # Override BinaryTool.do_install to skip its pre/post version-equality
        # guard — when node is already installed (any source) we deliberately
        # report the same version pre and post, which the guard would flag.
        return self.install_binary()

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        fnm_path = state.get("fnm_path", "")
        if not fnm_path:
            return []
        return [(f"via fnm ({fnm_path})", typer.colors.BRIGHT_BLACK)]

    def format_install(self, report: InstallReport) -> None:
        if report.error:
            typer.echo(f"FAILED: {report.error}", err=True)
            return
        line = "node ready"
        if report.version:
            line += f" ({report.version})"
        if report.method:
            line += f" via {report.method}"
        typer.echo(line)
        fnm = report.extra.get("fnm")
        if fnm:
            typer.echo(f"  fnm: {fnm}")


tool = NodeTool()

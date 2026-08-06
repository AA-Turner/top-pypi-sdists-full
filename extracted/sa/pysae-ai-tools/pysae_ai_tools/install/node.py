"""Install Node.js (LTS).

Behavior:

- If a ``node`` binary is already on PATH (any source — apt, brew, manual,
  fnm, …) the tool reports up-to-date and leaves it alone.
- Otherwise, it ensures fnm is present (delegating to the ``fnm`` install
  module if needed), then runs ``fnm install --lts && fnm default lts-latest``.

This is REQUIRED — most Pysae JS tooling assumes a Node runtime is reachable.

Bumping the LTS line carries the **globally installed npm packages** over to the
new version. Under fnm those live inside each Node installation, so pinning a new
default silently takes every global CLI out of PATH — a statusline, a linter, and
tools this very installer manages (``codex``, ``codex-flow``). fnm offers no
equivalent of ``nvm --reinstall-packages-from`` (requested since 2019, see
Schniz/fnm#703 and #620), so the packages are listed before the bump and
reinstalled after, and anything that fails to reinstall is named rather than lost
without a word.

Configuration carries the private npm registry credential into the user's own
``~/.npmrc`` and ``~/.yarnrc.yml``, so npm, pnpm, Yarn and bun install scoped
private packages in a project that declares no registry of its own.
"""

import json
import subprocess
from typing import Any

import httpx
import typer

from . import fnm as fnm_module
from . import registry_credential
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


# Shipped with Node itself — never carried over, the new version brings its own.
_BUNDLED_WITH_NODE = frozenset({"npm", "corepack"})


def _default_node_version(fnm: str) -> str:
    """The version ``fnm default`` currently points at (``v24.18.0``), or empty."""
    try:
        r = subprocess.run(
            [fnm, "default"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    candidate = (r.stdout or "").strip()
    return candidate if r.returncode == 0 and candidate.startswith("v") else ""


def _global_package_names(fnm: str, version: str) -> tuple[str, ...]:
    """Globally installed npm package names for ``version``, Node's own excluded.

    Parsed even on a non-zero exit: ``npm ls -g`` reports unmet peer dependencies
    as an error while still emitting a perfectly usable tree, and refusing to read
    it would silently drop the packages we are trying to carry over.
    """
    try:
        r = subprocess.run(
            [fnm, "exec", f"--using={version}", "--", "npm", "ls", "-g", "--depth=0", "--json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ()
    try:
        data = json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        return ()
    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict):
        return ()
    return tuple(sorted(name for name in dependencies if name not in _BUNDLED_WITH_NODE))


def _reinstall_global_packages(fnm: str, version: str, packages: tuple[str, ...]) -> tuple[list[str], list[str]]:
    """Install ``packages`` globally on ``version``. Returns ``(carried, lost)``.

    One package per call rather than a single batch: a batch fails as a whole, so
    one unpublished or renamed package would take every other one down with it.
    Whatever cannot be reinstalled is returned so the caller can name it — losing
    a tool silently is what made this worth fixing.
    """
    carried: list[str] = []
    lost: list[str] = []
    for package in packages:
        try:
            r = subprocess.run(
                [fnm, "exec", f"--using={version}", "--", "npm", "install", "-g", package],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=300,
            )
        except (OSError, subprocess.TimeoutExpired):
            lost.append(package)
            continue
        (carried if r.returncode == 0 else lost).append(package)
    return carried, lost


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
    cli_help = "Install Node.js (LTS) — uses fnm when node is missing; configures the private npm registry"
    # Optional, never pre-configure: node is REQUIRED, so a developer without a
    # registry PAT must still get node installed rather than skipped.
    env_optional = (registry_credential.TOKEN_VAR,)

    def fetch_latest_version(self) -> str:
        return _latest_lts_version()

    def get_state(self) -> ToolState:
        # Surface fnm-managed binaries even when the current shell hasn't
        # sourced the fnm init yet, otherwise fresh fnm-installed Node looks
        # missing.
        fnm_module.augment_path()
        state = super().get_state()
        state.extra["fnm_path"] = fnm_module.find_fnm()
        return registry_credential.augment_state(self.name, state)

    def do_configure(self) -> InstallReport:
        return registry_credential.configure_report(self.name)

    def do_uninstall(self, *, dry_run: bool = False) -> InstallReport:
        return registry_credential.uninstall_report(self.name, dry_run=dry_run)

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

        # Read the outgoing version's global packages *before* the bump: under fnm
        # they live inside the Node installation, so pinning a new default takes
        # them out of PATH. fnm has no equivalent of `nvm
        # --reinstall-packages-from` (asked for since 2019, see Schniz/fnm#703),
        # so carrying them over is on us — otherwise a bump silently removes the
        # user's CLIs, including ones this installer manages (codex, codex-flow).
        outgoing = _default_node_version(fnm_path)
        to_carry = _global_package_names(fnm_path, outgoing) if outgoing else ()

        version, err = _fnm_install_lts(fnm_path)
        if err:
            return InstallReport(error=err)

        extra: dict[str, Any] = {"fnm": fnm_report.method or "installed"}
        if to_carry and outgoing.lstrip("v") != version:
            carried, lost = _reinstall_global_packages(fnm_path, f"v{version}", to_carry)
            extra["global_packages"] = {"from": outgoing, "carried": carried, "lost": lost}

        return InstallReport(version=version, method="fnm", extra=extra)

    def do_install(self) -> InstallReport:
        # Override BinaryTool.do_install to skip its pre/post version-equality
        # guard — when node is already installed (any source) we deliberately
        # report the same version pre and post, which the guard would flag.
        return self.install_binary()

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        lines: list[tuple[str, str | None]] = []
        fnm_path = state.get("fnm_path", "")
        if fnm_path:
            lines.append((f"via fnm ({fnm_path})", typer.colors.BRIGHT_BLACK))
        lines.extend(registry_credential.identity_lines(state))
        return lines

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

        migration = report.extra.get("global_packages")
        if isinstance(migration, dict):
            carried = migration.get("carried") or []
            lost = migration.get("lost") or []
            if carried:
                typer.echo(f"  paquets globaux repris de {migration.get('from')} : {', '.join(carried)}")
            if lost:
                # Named, never dropped in silence: these CLIs left the PATH with
                # the old Node and could not be reinstalled.
                typer.secho(
                    f"  ⚠ non réinstallés : {', '.join(lost)} — relance `npm install -g <paquet>`",
                    fg=typer.colors.YELLOW,
                )


tool = NodeTool()

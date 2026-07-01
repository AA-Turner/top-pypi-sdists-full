"""Install capability dependencies into the SDK runtime.

Runs only in sandbox runtimes, after the project capability sync completes
and before ``Capability.discover`` registers components — so any preflight
``checks:`` see installed binaries.

Pipeline (per-boot):

1. ``packages`` — apt-get per capability. Skipped when the install marker
   is already present in the capability's cache directory.
2. ``python`` — combined ``uv pip install`` (or ``python -m pip install``)
   across every capability's pins. Runs every boot so the venv re-resolves
   when the binding set changes; pip is fast on already-satisfied specs.
3. ``scripts`` — bash scripts per capability, in declaration order. Skipped
   when the install marker is already present.

A successful packages+scripts pass writes ``.dreadnode-installed`` into the
capability's cache directory. ``CapabilitySyncClient`` atomically replaces
that directory whenever the capability's runtime_digest changes, so the
marker disappears with the directory and a fresh install runs automatically
on the next boot — no extra cache bookkeeping required.

See specs/capabilities/runtime.md (CAP-INST-*) and
packages/docs/src/content/docs/capabilities/dependencies-and-checks.mdx.
"""

import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

from dreadnode.capabilities.types import DependencySpec

# Per-step subprocess timeout. Heavy installs (Caido, Burp, large pip
# resolutions) need a generous budget; ``checks:`` is the 5s fast surface.
_INSTALL_TIMEOUT_SECONDS = 600

# Marker written into each capability's cache directory after a successful
# packages+scripts pass. Wiped automatically when the sync replaces the
# directory on a runtime_digest change.
_INSTALLED_MARKER = ".dreadnode-installed"


@dataclass
class InstallReport:
    """Outcome of one install pass over a set of capabilities.

    Mutually exclusive: a capability appears in exactly one of ``installed``,
    ``cached``, or ``failed``.
    """

    installed: list[str] = field(default_factory=list)
    cached: list[str] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)


def install_dependencies(
    specs: list[tuple[str, Path, DependencySpec]],
) -> InstallReport:
    """Run the three-step install pipeline across the supplied capabilities.

    ``specs`` is the list returned by
    :func:`dreadnode.capabilities.loader.preload_dependency_specs` — tuples of
    ``(capability_name, capability_dir, DependencySpec)``.
    """
    report = InstallReport()
    if not specs:
        return report

    to_install: list[tuple[str, Path, DependencySpec]] = []
    for name, path, dep in specs:
        if (path / _INSTALLED_MARKER).exists():
            report.cached.append(name)
        else:
            to_install.append((name, path, dep))

    _install_packages(to_install, report)
    _install_python_combined(specs, report)
    _install_scripts(to_install, report)

    for name, path, _dep in to_install:
        if name in report.failed:
            continue
        try:
            (path / _INSTALLED_MARKER).touch()
        except OSError:
            logger.warning(
                "Failed to write install marker for capability '{}' at {}",
                name,
                path,
            )
        report.installed.append(name)

    return report


def _install_packages(
    specs: list[tuple[str, Path, DependencySpec]],
    report: InstallReport,
) -> None:
    """Run privileged apt installs per capability that declares packages."""
    apt = shutil.which("apt-get")
    sudo = shutil.which("sudo")
    for name, _path, dep in specs:
        pkgs = [pkg for pkg in dep.packages if isinstance(pkg, str)]
        if not pkgs:
            continue
        if apt is None:
            logger.warning(
                "Capability '{}' declares packages but apt-get is unavailable; skipping",
                name,
            )
            continue
        command_prefix = _privileged_command_prefix(sudo)
        if command_prefix is None:
            report.failed[name] = (
                "packages: apt-get requires root privileges but sudo is unavailable"
            )
            continue
        logger.info("Installing apt packages for '{}': {}", name, pkgs)
        err = _run([*command_prefix, apt, "update"])
        if err:
            report.failed[name] = f"packages: {err}"
            continue
        err = _run([*command_prefix, apt, "install", "-y", *pkgs])
        if err:
            report.failed[name] = f"packages: {err}"


def _privileged_command_prefix(sudo: str | None) -> list[str] | None:
    """Return the prefix needed to run an apt command with root privileges."""
    if os.geteuid() == 0:
        return []
    if sudo:
        return [sudo]
    return None


def _install_python_combined(
    specs: list[tuple[str, Path, DependencySpec]],
    report: InstallReport,
) -> None:
    """Union pip specs across every capability and install in one call.

    A failure blames every capability that contributed pins; a marker-cached
    capability is moved out of ``cached`` into ``failed`` because the boot
    is broken even though its prior packages+scripts pass remains valid.
    """
    union = sorted({pkg for _name, _path, dep in specs for pkg in dep.python})
    if not union:
        return

    cmd = _python_install_cmd(union)
    logger.info("Installing python deps (combined across {} caps): {}", len(specs), union)
    err = _run(cmd)
    if err is None:
        return

    for name, _path, dep in specs:
        if not dep.python:
            continue
        report.failed[name] = f"python: {err}"
        if name in report.cached:
            report.cached.remove(name)


def _install_scripts(
    specs: list[tuple[str, Path, DependencySpec]],
    report: InstallReport,
) -> None:
    """Run each capability's install scripts sequentially with cwd = cap dir."""
    for name, path, dep in specs:
        if name in report.failed:
            continue
        for script in dep.scripts:
            script_path = path / script
            logger.info("Running install script for '{}': {}", name, script)
            err = _run(["bash", str(script_path)], cwd=path)
            if err:
                report.failed[name] = f"scripts/{script}: {err}"
                break


def _python_install_cmd(packages: list[str]) -> list[str]:
    """Prefer ``uv pip install`` when available; fall back to ``python -m pip``."""
    if shutil.which("uv"):
        return ["uv", "pip", "install", *packages]
    return [sys.executable, "-m", "pip", "install", *packages]


def _run(cmd: list[str], cwd: Path | None = None) -> str | None:
    """Run a subprocess, returning ``None`` on success or a short error tail.

    The returned string is the last few lines of stderr (or a generic
    "exit code N" / "timed out" message) — enough to land in logs without
    flooding them.
    """
    try:
        result = subprocess.run(  # noqa: S603
            cmd,
            cwd=cwd,
            capture_output=True,
            timeout=_INSTALL_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return f"timed out after {_INSTALL_TIMEOUT_SECONDS}s"
    except FileNotFoundError as exc:
        return f"command not found: {exc.filename or cmd[0]}"
    except Exception as exc:
        return str(exc)

    if result.returncode == 0:
        return None

    stderr = result.stderr.decode("utf-8", errors="replace").strip()
    if stderr:
        return "\n".join(stderr.splitlines()[-5:])
    return f"exit code {result.returncode}"


__all__ = ["InstallReport", "install_dependencies"]

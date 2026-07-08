"""Version check and upgrade detection for the Dreadnode CLI.

Pure async + HTTP module with no TUI dependencies.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import httpx
from loguru import logger
from packaging.version import InvalidVersion, Version

from dreadnode.version import VERSION

_PACKAGE_NAME = "dreadnode"
_TIMEOUT = 3.0
_DIAGNOSTIC_EXCERPT_CHARS = 600


@dataclass(frozen=True, slots=True)
class UpdateInfo:
    """Holds version comparison result."""

    current: str
    latest: str


async def check_for_update(
    pypi_url: str = "https://pypi.org",
    *,
    suppress_errors: bool = True,
) -> UpdateInfo | None:
    """Check PyPI for a newer version of dreadnode.

    Returns UpdateInfo if a newer version exists, None otherwise.
    By default, swallows all exceptions to avoid degrading the TUI
    experience. Pass ``suppress_errors=False`` for explicit CLI commands
    where check failures should be visible to automation.

    This function is pure async (no blocking subprocess calls) so it is
    safe to run from a Textual worker without blocking the event loop.
    Installer detection (detect_upgrade_command) is deferred to /update
    time because it shells out to ``uv tool list`` / ``pipx list``.
    """
    if VERSION == "0.0.0+local":
        logger.debug("Skipping update check for dev build")
        return None

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.get(f"{pypi_url}/pypi/{_PACKAGE_NAME}/json")
            resp.raise_for_status()

        data = resp.json()
        latest_str = data["info"]["version"]
        current = Version(VERSION)
        latest = Version(latest_str)

        if latest > current:
            logger.debug("Update available: {} -> {}", VERSION, latest_str)
            return UpdateInfo(current=VERSION, latest=latest_str)
    except Exception as exc:
        logger.opt(exception=True).debug("Update check failed")
        if not suppress_errors:
            raise RuntimeError(f"Update check failed: {exc}") from exc
        return None
    else:
        logger.debug("Up to date: {} (pypi={})", VERSION, latest_str)
        return None


def _running_exe_dir() -> Path | None:
    """Return the directory containing the running ``dn`` executable."""
    dn_path = shutil.which("dn")
    if dn_path:
        # Preserve the launcher directory (for example ~/.local/bin) instead of
        # resolving the symlink target into uv's tool environment.
        return Path(dn_path).parent.resolve()
    return Path(sys.executable).resolve().parent


def _is_managed_by_uv_tool() -> bool:
    """Check if the running dn binary lives inside uv's tool bin directory."""
    exe_dir = _running_exe_dir()
    if exe_dir is None:
        return False

    # uv tool bin is typically ~/.local/bin or $UV_TOOL_BIN_DIR
    uv_bin_dir = os.environ.get("UV_TOOL_BIN_DIR")
    if uv_bin_dir:
        if exe_dir == Path(uv_bin_dir).resolve():
            return True

    try:
        result = subprocess.run(
            ["uv", "tool", "dir", "--bin"],  # noqa: S607
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            uv_tool_bin = Path(result.stdout.strip()).resolve()
            if exe_dir == uv_tool_bin:
                return True
    except Exception:
        logger.opt(exception=True).debug("uv tool dir --bin failed")

    return False


def _is_managed_by_pipx() -> bool:
    """Check if the running dn binary lives inside pipx's bin directory."""
    exe_dir = _running_exe_dir()
    if exe_dir is None:
        return False

    pipx_bin_dir = os.environ.get("PIPX_BIN_DIR")
    if pipx_bin_dir:
        if exe_dir == Path(pipx_bin_dir).resolve():
            return True

    try:
        result = subprocess.run(
            ["pipx", "environment", "--value", "PIPX_BIN_DIR"],  # noqa: S607
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            pipx_bin = Path(result.stdout.strip()).resolve()
            if exe_dir == pipx_bin:
                return True
    except Exception:
        logger.opt(exception=True).debug("pipx environment failed")

    return False


def detect_upgrade_command() -> list[str] | str:
    """Detect which package manager owns the running dn install.

    Matches the running executable's location against each tool manager's
    bin directory, rather than just checking if the package name appears
    in the manager's list.  This avoids upgrading a stale copy in one
    manager while a different installation is actually on PATH.

    Returns a list of args for create_subprocess_exec (uv/pipx),
    or a shell string for create_subprocess_shell (install script fallback).
    """
    if shutil.which("uv") and _is_managed_by_uv_tool():
        logger.debug("Installer detected: uv tool (binary in uv tool bin dir)")
        return ["uv", "tool", "upgrade", _PACKAGE_NAME]

    if shutil.which("pipx") and _is_managed_by_pipx():
        logger.debug("Installer detected: pipx (binary in pipx bin dir)")
        return ["pipx", "upgrade", _PACKAGE_NAME]

    # Fallback to install script
    logger.debug("Installer detected: falling back to install script")
    if shutil.which("curl"):
        return "curl -fsSL https://dreadnode.io/install.sh | bash"
    if shutil.which("wget"):
        return "wget -qO- https://dreadnode.io/install.sh | bash"
    return "curl -fsSL https://dreadnode.io/install.sh | bash"


def build_noop_upgrade_diagnostic(expected_version: str, stdout: str, stderr: str) -> list[str]:
    """Build a diagnostic for upgrade commands that exit 0 without changing version."""
    output = f"{stdout}\n{stderr}".lower()
    if any(
        phrase in output
        for phrase in (
            "resolutionimpossible",
            "no matching distribution",
            "could not find a version",
            "no solution found",
        )
    ):
        reason = "Installer output suggests no valid upgrade could be resolved."
    elif any(
        phrase in output
        for phrase in (
            "already installed",
            "already up-to-date",
            "already up to date",
            "nothing to do",
            "no changes",
        )
    ):
        reason = "Installer output suggests it decided nothing needed to be upgraded."
    else:
        reason = "Installer output did not clearly explain why no version changed."

    lines = [
        f"Upgrade command exited 0, but dn --version did not report v{expected_version}.",
        reason,
        "Multiple installations are also possible; check which dn is on your PATH "
        "if the installer output looks correct.",
    ]
    lines.extend(_output_excerpt("stdout", stdout))
    lines.extend(_output_excerpt("stderr", stderr))
    return lines


def _output_excerpt(label: str, text: str) -> list[str]:
    """Return a capped, indented output excerpt."""
    text = text.strip()
    if not text:
        return []

    truncated = len(text) > _DIAGNOSTIC_EXCERPT_CHARS
    excerpt = text[:_DIAGNOSTIC_EXCERPT_CHARS].rstrip()
    lines = [f"{label}:"]
    lines.extend(f"  {line}" for line in excerpt.splitlines())
    if truncated:
        lines.append("  … output truncated …")
    return lines


def verify_upgrade(expected_version: str) -> str | None:
    """Check the installed version after upgrade.

    Returns the newly installed version string if it matches or exceeds
    ``expected_version``, or None if verification failed.

    Uses the same detection logic as detect_upgrade_command to find the
    correct binary path, ensuring we verify the same installation that
    was just upgraded.
    """
    # Try to find the correct dn binary using the same logic as detect_upgrade_command
    dn_path = _get_managed_dn_path()
    if not dn_path:
        # Fallback to PATH lookup
        dn_path = shutil.which("dn")
        if not dn_path:
            return None

    try:
        result = subprocess.run(  # noqa: S603
            [dn_path, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if result.returncode != 0:
            logger.debug("verify_upgrade: dn --version failed (rc={})", result.returncode)
            return None

        installed = result.stdout.strip().split()[-1]
        if Version(installed) >= Version(expected_version):
            return installed
        logger.debug(
            "verify_upgrade: version mismatch, expected>={} got={}",
            expected_version,
            installed,
        )
    except (InvalidVersion, Exception):
        logger.opt(exception=True).debug("verify_upgrade failed")

    return None


def _get_managed_dn_path() -> str | None:
    """Get the path to the dn binary that is managed by uv tool or pipx.

    Returns the path to the specific dn binary that would be upgraded,
    or None if not managed by uv tool or pipx.
    """
    # Check if managed by uv tool
    if shutil.which("uv") and _is_managed_by_uv_tool():
        try:
            # Get the uv tool bin directory
            result = subprocess.run(
                ["uv", "tool", "dir", "--bin"],  # noqa: S607
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                uv_bin_dir = Path(result.stdout.strip()).resolve()
                dn_path = uv_bin_dir / "dn"
                if dn_path.exists():
                    return str(dn_path)
        except Exception:
            logger.opt(exception=True).debug("Failed to get uv tool dn path")

    # Check if managed by pipx
    if shutil.which("pipx") and _is_managed_by_pipx():
        try:
            # Get the pipx bin directory
            result = subprocess.run(
                ["pipx", "environment", "--value", "PIPX_BIN_DIR"],  # noqa: S607
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                pipx_bin_dir = Path(result.stdout.strip()).resolve()
                dn_path = pipx_bin_dir / "dn"
                if dn_path.exists():
                    return str(dn_path)
        except Exception:
            logger.opt(exception=True).debug("Failed to get pipx dn path")

    return None

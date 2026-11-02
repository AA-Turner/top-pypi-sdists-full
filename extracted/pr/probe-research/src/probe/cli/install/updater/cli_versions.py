"""read the CLI version an upgrade really left (fresh subprocess) and judge the result."""

from __future__ import annotations
import shutil
import subprocess
import sys
from dataclasses import dataclass


# -- upgrade actions --------------------------------------------------------
@dataclass
class CliResult:
    ran: bool
    ok: bool  # the CLI is at (or past) the target after the attempt — VERIFIED
    changed: bool  # the installed version actually moved
    before: str | None
    after: str | None
    message: str
    #: The package manager this install needs (`uv`, `pipx`) is not on this
    #: process's PATH. An observation for the server's update report only.
    missing_binary: bool = False


def _run(cmd: list[str], timeout: float) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(cmd, timeout=timeout)  # inherit stdio: show progress
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, returncode=124)


def _installed_cli_version() -> str | None:
    """The CLI version after an upgrade, read FRESH -- the running process keeps
    its own stale __version__.

    The upgraded environment's own version first. The `probe` on PATH can be a
    different install entirely (a conda or pipx copy ahead of the uv tool), and
    grading that one reported "CLI upgraded" for an install nobody touched, or
    a failure for one that did move. PATH is the fallback for the one upgrade
    that deletes this environment: the legacy probe-agent reinstall.
    """
    return env_cli_version() or _path_cli_version()


def _path_cli_version() -> str | None:
    """Version of the `probe` on PATH, read via a fresh subprocess."""
    probe_bin = shutil.which("probe") or "probe"
    try:
        r = subprocess.run([probe_bin, "--version"], capture_output=True, text=True, timeout=15)
        if r.returncode == 0 and (r.stdout or "").strip():
            return r.stdout.strip().split()[-1]  # "probe 0.8.2" -> "0.8.2"
    except Exception:
        return None
    return None


def env_cli_version() -> str | None:
    """The CLI version now installed in THIS interpreter's own environment.

    Read by a fresh interpreter from the dist metadata on disk, because this
    process's own `__version__` is whatever it imported before the upgrade.
    None when that environment is gone (the legacy reinstall deletes it) or
    unreadable.
    """
    try:
        r = subprocess.run(  # noqa: S603 - our own interpreter, no shell
            [
                sys.executable,
                "-c",
                f"from importlib.metadata import version; print(version({DIST!r}))",
            ],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    out = (r.stdout or "").strip()
    return out if r.returncode == 0 and out else None


def _finalize(before: str | None, target: str | None, tool: str) -> CliResult:
    """Post-condition — the CLI's H1: trust the observed version, not the upgrade's
    exit code. A no-op upgrade (e.g. a ``uv tool install ==X`` version pin) exits 0
    while changing nothing; only re-reading the version catches that."""
    after = _installed_cli_version()
    if is_newer(after, before):
        return CliResult(True, True, True, before, after, f"CLI upgraded {before} → {after}")
    if target and after and not is_newer(target, after):
        return CliResult(True, True, False, before, after, f"CLI already at the latest ({after})")
    return CliResult(
        True,
        False,
        False,
        before,
        after,
        f"`{tool}` reported success but the CLI is still {after or before} "
        "(it may be version-pinned, or that release was yanked)",
    )
from probe.cli.install.updater.updater import DIST  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.plugin_update import is_newer  # noqa: E402 -- pieces need each other; the front door loads this one first

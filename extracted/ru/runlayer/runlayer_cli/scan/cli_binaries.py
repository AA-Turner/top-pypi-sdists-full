"""Locate CLI binaries and read their versions.

Neutral, dependency-free helpers shared by scan features (client-presence
probes and agent detectors) that need to find a CLI on ``PATH`` or in common
install locations and read its ``--version``. Kept free of any
client-presence or agent concepts so both layers can depend on it.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from itertools import islice
from pathlib import Path


_MAX_NVM_VERSION_ROOTS = 64
_WINDOWS_EXECUTABLE_SUFFIXES = (".cmd", ".exe", ".bat")


def _nvm_bin_roots(home: Path) -> list[Path]:
    """Return deterministic bin roots from nvm's versioned installs.

    Cap scandir itself. Sorting the full tree first would list every dirent
    over WSL UNC homes before the 64-root limit takes effect.
    """
    roots: list[Path] = []
    versions_root = home / ".nvm" / "versions" / "node"
    try:
        with os.scandir(versions_root) as entries:
            for entry in islice(entries, _MAX_NVM_VERSION_ROOTS):
                try:
                    bin_root = Path(entry.path) / "bin"
                    if bin_root.is_dir():
                        roots.append(bin_root)
                except OSError:
                    continue
    except OSError:
        return roots
    return sorted(roots)


def _windows_versioned_node_roots(home: Path) -> list[Path]:
    """Return per-version bin roots from Windows Node version managers."""
    app_data = home / "AppData" / "Roaming"
    roots: list[Path] = []
    for root, pattern in (
        (app_data / "nvm", "v*"),
        (app_data / "fnm" / "node-versions", "*/installation"),
    ):
        try:
            roots.extend(sorted(root.glob(pattern)))
        except OSError:
            continue
    return roots


def _windows_cli_candidates(binary: str, *, home: Path) -> list[Path]:
    """Return per-user Windows install locations for a CLI binary.

    ``shutil.which`` resolves against the calling process' ``PATH``, which for
    the SYSTEM-context scan and MDM hook probes is the machine ``PATH`` — it
    never contains a user's npm/volta/scoop shim directory. Clients that ship
    only as a per-user package (GitHub Copilot CLI is npm-only, so it has no
    installer directory or uninstall registry entry either) would otherwise
    have no executable-class evidence at all.
    """
    app_data = home / "AppData" / "Roaming"
    local_app_data = home / "AppData" / "Local"
    roots = [
        app_data / "npm",
        local_app_data / "pnpm",
        local_app_data / "Volta" / "bin",
        local_app_data / "Yarn" / "bin",
        local_app_data / "Microsoft" / "WinGet" / "Links",
        home / ".bun" / "bin",
        home / ".local" / "bin",
        home / ".cargo" / "bin",
        home / "scoop" / "shims",
        *_windows_versioned_node_roots(home),
    ]
    return [
        root / f"{binary}{suffix}"
        for root in roots
        for suffix in _WINDOWS_EXECUTABLE_SUFFIXES
    ]


def posix_bin_roots(*, home: Path, system: str) -> list[Path]:
    """Return the common POSIX bin directories probed for CLI installs.

    Shared by the name-keyed candidate probe below and the shim-identity
    sweep (``bin_shims``), so both layers cover the same directory set.
    """
    roots = [
        home / ".volta" / "bin",
        home / ".local" / "bin",
        home / ".claude" / "local",
        home / ".nvm" / "current" / "bin",
        *_nvm_bin_roots(home),
        home / "bin",
        home / ".cargo" / "bin",
        home / ".asdf" / "shims",
        home / ".mise" / "shims",
        home / ".nix-profile" / "bin",
        Path("/usr/local/bin"),
        Path("/usr/bin"),
    ]
    if system == "Darwin":
        roots.append(Path("/opt/homebrew/bin"))
    elif system == "Linux":
        roots.extend(
            [
                Path("/snap/bin"),
                Path("/nix/var/nix/profiles/default/bin"),
            ]
        )
    return roots


def _common_cli_candidates(binary: str, *, home: Path, system: str) -> list[Path]:
    """Return common fallback install locations for a CLI binary."""
    if system == "Windows":
        return _windows_cli_candidates(binary, home=home)

    return [
        *(root / binary for root in posix_bin_roots(home=home, system=system)),
        Path("/opt") / binary / "bin" / binary,
    ]


def _is_executable_file(path: Path) -> bool:
    """Return whether ``path`` is a file the current user can execute."""
    try:
        return path.is_file() and os.access(path, os.X_OK)
    except OSError:
        return False


def _is_windows_executable_file(path: Path) -> bool:
    """Return whether ``path`` is a file Windows can execute.

    Windows has no execute bit — ``os.access(X_OK)`` reduces to an existence
    check — so the suffix is what makes a file runnable.
    """
    try:
        return path.suffix.lower() in _WINDOWS_EXECUTABLE_SUFFIXES and path.is_file()
    except OSError:
        return False


def locate_cli_binary(
    binary: str,
    *,
    home: Path | None = None,
    system: str | None = None,
) -> Path | None:
    """Locate a CLI on PATH or in common user/system binary directories."""
    located = shutil.which(binary)
    if located:
        return Path(located)

    actual_home = home or Path.home()
    actual_system = system or platform.system()
    is_executable = (
        _is_windows_executable_file
        if actual_system == "Windows"
        else _is_executable_file
    )
    for candidate in _common_cli_candidates(
        binary, home=actual_home, system=actual_system
    ):
        if is_executable(candidate):
            return candidate
    return None


def _resolved_from_path(path: Path) -> bool:
    """Whether ``PATH`` resolution for ``path``'s own name yields ``path``."""
    located = shutil.which(path.name)
    if not located:
        return False
    try:
        return os.path.normcase(os.path.realpath(located)) == os.path.normcase(
            os.path.realpath(path)
        )
    except OSError:
        return False


def _safe_to_execute(path: Path) -> bool:
    """Refuse to execute binaries another user could have planted (POSIX).

    Version probes run on a schedule (launchd/cron/Task Scheduler), so a binary
    planted by a *different* user in a shared or world-writable PATH dir must
    not be executed. Executing the scanning user's own binaries is not an
    escalation.

    Windows has no cheap ownership check, so execution is limited to what
    ``PATH`` resolves: SYSTEM's machine ``PATH`` holds only admin-writable dirs,
    and a probe running under the user's own token resolves their own ``PATH``.
    The per-user fallback dirs (``%APPDATA%\\npm`` and friends) are writable by
    that user, so they stay presence-only evidence and are never executed.
    """
    if os.name != "posix":
        return _resolved_from_path(path)
    try:
        info = os.stat(path)
    except OSError:
        return False
    if info.st_mode & 0o002:
        return False
    return info.st_uid in (0, os.geteuid())


def get_cli_version(cli_path: str | Path) -> str | None:
    """Read a CLI's ``--version`` under a bounded (5s) subprocess policy.

    Skips execution entirely when the binary fails the POSIX ownership gate
    (owned by neither root nor the scanning user, or world-writable).
    """
    if not _safe_to_execute(Path(cli_path)):
        return None
    try:
        result = subprocess.run(
            [str(cli_path), "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except Exception:
        return None
    output = result.stdout.strip() or result.stderr.strip()
    if result.returncode != 0 or not output:
        return None
    return output.splitlines()[0][:200]

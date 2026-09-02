"""Generator for ``agentic-devtools-required-setup.py``.

The generated script uses **only** the Python standard library.  It
detects and removes corrupted installation artefacts, then installs the
latest PyPI release of ``agentic-devtools``.
"""

from __future__ import annotations

import os
import re
import site
import subprocess
import sys
import threading
from pathlib import Path
from typing import TextIO

from ..git_hooks_policy import (
    HOOKS_DISABLED_MESSAGE,
    format_preserved_message,
    is_git_hooks_management_enabled,
)

#: Warning printed when pip cannot replace the console scripts of the running
#: agentic-devtools install (Windows locks a running ``.exe``).
SELF_UPGRADE_LOCK_MESSAGE = (
    "  ⚠ Skipped self-upgrade: Windows is holding a lock on the agentic-devtools "
    "console script that started this run (WinError 32)."
)

#: Actionable remediation printed alongside :data:`SELF_UPGRADE_LOCK_MESSAGE`.
#: The ``<sys.executable>`` placeholder stands for the Python interpreter path;
#: the generated script substitutes the real path via an f-string at runtime,
#: formats it for PowerShell with ``&`` and surrounds the executable with
#: double quotes so paths with spaces remain runnable.
SELF_UPGRADE_LOCK_REMEDY_TEMPLATE = (
    "    Continuing with the installed version. To upgrade, close every running "
    'agdt-* process and run: & "<sys.executable>" -m pip install --upgrade agentic-devtools'
)

_SELF_UPGRADE_LOCK_EXECUTABLE = "agdt-setup.exe"


# ---------------------------------------------------------------------------
# Corruption detection helpers (used by the generator to embed logic)
# ---------------------------------------------------------------------------


def is_self_upgrade_lock(output: str) -> bool:
    """Return ``True`` when pip failed because a running console script is locked.

    On Windows a running ``.exe`` cannot be deleted or replaced, so pip's
    uninstall of the currently-installed wheel fails with
    ``[WinError 32] The process cannot access the file because it is being used
    by another process`` when the setup run itself was started from one of the
    package's console scripts (``agdt-setup.exe``).  That failure is recoverable:
    the already-installed version remains fully functional.

    *output* is the combined stdout + stderr from pip.
    """
    lowered = output.lower()
    locked = "winerror 32" in lowered or "used by another process" in lowered
    return locked and _SELF_UPGRADE_LOCK_EXECUTABLE in lowered


def _is_agentic_devtools_tilde_backup(name: str) -> bool:
    """Return ``True`` for pip's ``~``-mangled agentic-devtools backups."""
    name_lower = name.lower()
    for candidate in ("agentic-devtools", "agentic_devtools"):
        prefix = f"~{candidate[1:]}"
        if name_lower == prefix:
            return True
        if not name_lower.startswith(prefix):
            continue
        remainder = name_lower[len(prefix) :]
        return _has_distribution_suffix(remainder)
    return False


def _is_agentic_devtools_distribution_name(name: str) -> bool:
    """Return ``True`` for agentic-devtools distribution names and pip backups."""
    name_lower = name.lower()
    if _is_agentic_devtools_tilde_backup(name_lower):
        return True

    for candidate in ("agentic-devtools", "agentic_devtools"):
        if name_lower == candidate:
            return True
        if not name_lower.startswith(candidate):
            continue
        remainder = name_lower[len(candidate) :]
        if _has_distribution_suffix(remainder):
            return True
    return False


def _has_distribution_suffix(remainder: str) -> bool:
    """Return ``True`` when *remainder* is a valid dist-info/version suffix."""
    if remainder == ".dist-info":
        return True
    if not remainder.startswith("-"):
        return False
    version = remainder[1:]
    if version.endswith(".dist-info"):
        version = version[: -len(".dist-info")]
    return bool(version) and version[0].isdigit() and re.fullmatch(r"[A-Za-z0-9.+!]+", version) is not None


def detect_corrupted_artifacts() -> list[Path]:
    """Scan site-packages for known corrupted agentic-devtools artefacts.

    Returns a list of filesystem paths that should be removed before a
    clean install can succeed.

    Detected artefact patterns:
    * Tilde-prefixed leftover directories created by pip when uninstalling the
      currently running console script (for example ``~gentic-devtools`` or
      ``~gentic_devtools-0.2.380.dist-info``).
    * ``.dist-info`` directories for ``agentic-devtools`` / ``agentic_devtools``
      that lack a ``RECORD`` file.
    * ``_editable_impl_agentic_devtools.pth`` files (leftovers from
      editable installs).
    """
    artifacts: list[Path] = []

    for sp_dir in _site_packages_dirs():
        sp = Path(sp_dir)
        if not sp.is_dir():
            continue

        try:
            children = list(sp.iterdir())
        except (PermissionError, OSError):
            continue

        for child in children:
            name = child.name

            # Tilde-prefixed leftover directories
            if child.is_dir() and _is_agentic_devtools_tilde_backup(name):
                artifacts.append(child)
                continue

            # dist-info without RECORD
            if child.is_dir() and name.endswith(".dist-info") and _is_agentic_devtools_distribution_name(name):
                record = child / "RECORD"
                if not record.exists():
                    artifacts.append(child)
                continue

            # Editable-install .pth files
            if child.is_file() and name == "_editable_impl_agentic_devtools.pth":
                artifacts.append(child)

    return artifacts


def cleanup_artifacts(artifacts: list[Path]) -> list[str]:
    """Remove the artefacts returned by :func:`detect_corrupted_artifacts`.

    Returns a list of human-readable messages describing each removal
    attempt (success or failure).
    """
    import shutil

    messages: list[str] = []
    for artifact in artifacts:
        try:
            if artifact.is_symlink():
                artifact.unlink()
            elif artifact.is_dir():
                shutil.rmtree(artifact)
            else:
                artifact.unlink()
            messages.append(f"  Removed: {artifact}")
        except PermissionError:
            messages.append(f"  ⚠ Permission denied (read-only site-packages?): {artifact}")
        except OSError as exc:
            messages.append(f"  ⚠ Failed to remove {artifact}: {exc}")
    return messages


def install_package() -> tuple[bool, str]:
    """Install/upgrade ``agentic-devtools`` from PyPI.

    Returns ``(success, output)`` where *output* is the combined
    stdout + stderr from pip, or a synthetic lock message when the
    Windows autorun short-circuit fires (see below).

    On Windows when spawned by ``agdt-setup.exe`` (``AGDT_SETUP_AUTORUN``
    is set), pip is **not** invoked — the function returns
    ``(False, <lock message>)`` immediately to prevent WinError 32 from
    corrupting package metadata.  Callers should treat that pair the same
    as a real pip WinError 32 failure.
    """
    if sys.platform == "win32" and os.environ.get("AGDT_SETUP_AUTORUN"):
        # Proactively skip pip install when spawned by agdt-setup.exe to avoid WinError 32
        return (
            False,
            "[WinError 32] The process cannot access the file because "
            "it is being used by another process: agdt-setup.exe",
        )

    stdout_chunks: list[str] = []
    stderr_chunks: list[str] = []
    process = subprocess.Popen(
        [sys.executable, "-m", "pip", "install", "--upgrade", "agentic-devtools"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    stdout_thread = threading.Thread(
        target=_stream_subprocess_output,
        args=(process.stdout, sys.stdout, stdout_chunks),
    )
    stderr_thread = threading.Thread(
        target=_stream_subprocess_output,
        args=(process.stderr, sys.stderr, stderr_chunks),
    )
    stdout_thread.start()
    stderr_thread.start()
    stdout_thread.join()
    stderr_thread.join()
    output = "".join(stdout_chunks + stderr_chunks)
    return process.wait() == 0, output


def setup_git_hooks() -> str | None:
    """Configure ``core.hooksPath`` to ``.githooks`` if inside a git repo.

    Non-destructive: an existing ``core.hooksPath`` pointing anywhere other than
    ``.githooks`` is preserved, and no directory is created.  Management can be
    disabled entirely with ``"manage_git_hooks": false`` in
    ``.agdt/config/project.json``; when the repository root cannot be resolved
    that file is unreachable and management is treated as enabled.

    Returns a status message, or ``None`` when not in a git context.
    """
    # Check if we're in a git repo
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    # Resolve the repo root up front: it locates both the project config and the
    # .githooks directory.
    repo_root: Path | None
    try:
        toplevel = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        repo_root = Path(toplevel.stdout.strip())
    except (subprocess.CalledProcessError, OSError):
        repo_root = None

    if repo_root is not None and not is_git_hooks_management_enabled(repo_root):
        return HOOKS_DISABLED_MESSAGE

    # Check current hooksPath
    try:
        result = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            capture_output=True,
            text=True,
        )
        hooks_path_set = result.returncode == 0
        current = result.stdout.strip() if hooks_path_set else ""
    except FileNotFoundError:
        return None

    if hooks_path_set and current != ".githooks":
        return format_preserved_message(current)

    try:
        subprocess.run(
            ["git", "config", "core.hooksPath", ".githooks"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        return f"  ⚠ Failed to set core.hooksPath: {exc}"

    # Ensure .githooks directory exists
    if repo_root is not None:
        try:
            (repo_root / ".githooks").mkdir(parents=True, exist_ok=True)
        except OSError:
            pass

    return "  ✓ core.hooksPath set to '.githooks'"


# ---------------------------------------------------------------------------
# Script content generator
# ---------------------------------------------------------------------------


def generate_required_setup_script() -> str:
    """Return the full content of ``agentic-devtools-required-setup.py``.

    The generated script is stdlib-only and supports a ``--foreground``
    flag (currently a no-op for forward compatibility).
    """
    return _REQUIRED_SETUP_TEMPLATE


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _site_packages_dirs() -> list[str]:
    """Return a list of site-packages directories for the current interpreter."""
    dirs: list[str] = []
    for attr in ("getsitepackages", "getusersitepackages"):
        fn = getattr(site, attr, None)
        if fn is None:
            continue
        result = fn()
        if isinstance(result, str):
            dirs.append(result)
        elif isinstance(result, list):
            dirs.extend(result)
    return dirs


def _stream_subprocess_output(stream: TextIO | None, sink: TextIO, chunks: list[str]) -> None:
    """Mirror a subprocess text stream to *sink* while accumulating it."""
    if stream is None:
        return
    try:
        while True:
            line = stream.readline()
            if line == "":
                break
            sink.write(line)
            sink.flush()
            chunks.append(line)
    finally:
        stream.close()


# ---------------------------------------------------------------------------
# Template — the generated script that goes into .agdt/
# ---------------------------------------------------------------------------

_REQUIRED_SETUP_TEMPLATE = '''\
#!/usr/bin/env python3
"""agentic-devtools required setup — self-repair & install.

This script is managed by agentic-devtools and regenerated on every
``agdt-setup`` run.  DO NOT EDIT — your changes will be overwritten.

Supports: ``--foreground`` (default, forward-compatible no-op).
"""

import argparse
import json
import re
import shutil
import site
import subprocess
import sys
import threading
from pathlib import Path

_HOOKS_DISABLED_MESSAGE = (
    "  ℹ Git hooks management is disabled by project config "
    "(manage_git_hooks: false in .agdt/config/project.json) — leaving core.hooksPath unchanged."
)

_PRESERVED_MESSAGE_PREFIX = "  ⚠ core.hooksPath is already set to "

_PRESERVED_MESSAGE_SUFFIX = (
    "    agentic-devtools did not overwrite it. "
    'Set "manage_git_hooks": false in .agdt/config/project.json to silence this notice.'
)

_NON_BOOLEAN_WARNING_PREFIX = "  ⚠ manage_git_hooks in .agdt/config/project.json must be a boolean, got "

_SELF_UPGRADE_LOCK_MESSAGE = (
    "  ⚠ Skipped self-upgrade: Windows is holding a lock on the agentic-devtools "
    "console script that started this run (WinError 32)."
)

_SELF_UPGRADE_LOCK_REMEDY = (
    "    Continuing with the installed version. To upgrade, close every running "
    f'agdt-* process and run: & "{sys.executable}" -m pip install --upgrade agentic-devtools'
)

_SELF_UPGRADE_LOCK_EXECUTABLE = "agdt-setup.exe"


def _site_packages_dirs():
    """Return site-packages directories."""
    dirs = []
    for attr in ("getsitepackages", "getusersitepackages"):
        fn = getattr(site, attr, None)
        if fn is None:
            continue
        result = fn()
        if isinstance(result, str):
            dirs.append(result)
        elif isinstance(result, list):
            dirs.extend(result)
    return dirs


def _is_agentic_devtools_tilde_backup(name):
    """Return True for pip's ~-mangled agentic-devtools backups."""
    name_lower = name.lower()
    for candidate in ("agentic-devtools", "agentic_devtools"):
        prefix = f"~{candidate[1:]}"
        if name_lower == prefix:
            return True
        if not name_lower.startswith(prefix):
            continue
        remainder = name_lower[len(prefix) :]
        return _has_distribution_suffix(remainder)
    return False


def _is_agentic_devtools_distribution_name(name):
    """Return True for agentic-devtools distribution names and pip backups."""
    name_lower = name.lower()
    if _is_agentic_devtools_tilde_backup(name_lower):
        return True

    for candidate in ("agentic-devtools", "agentic_devtools"):
        if name_lower == candidate:
            return True
        if not name_lower.startswith(candidate):
            continue
        remainder = name_lower[len(candidate) :]
        if _has_distribution_suffix(remainder):
            return True
    return False


def _has_distribution_suffix(remainder):
    """Return True when remainder is a valid dist-info/version suffix."""
    if remainder == ".dist-info":
        return True
    if not remainder.startswith("-"):
        return False
    version = remainder[1:]
    if version.endswith(".dist-info"):
        version = version[: -len(".dist-info")]
    return bool(version) and version[0].isdigit() and re.fullmatch(r"[A-Za-z0-9.+!]+", version) is not None


def _detect_corrupted_artifacts():
    """Scan site-packages for corrupted agentic-devtools artefacts."""
    artifacts = []
    for sp_dir in _site_packages_dirs():
        sp = Path(sp_dir)
        if not sp.is_dir():
            continue
        try:
            children = list(sp.iterdir())
        except (PermissionError, OSError):
            continue
        for child in children:
            name = child.name
            if child.is_dir() and _is_agentic_devtools_tilde_backup(name):
                artifacts.append(child)
                continue
            if child.is_dir() and name.endswith(".dist-info") and _is_agentic_devtools_distribution_name(name):
                if not (child / "RECORD").exists():
                    artifacts.append(child)
                continue
            if child.is_file() and name == "_editable_impl_agentic_devtools.pth":
                artifacts.append(child)
    return artifacts


def _cleanup_artifacts(artifacts):
    """Remove corrupted artefacts with permission error handling."""
    for artifact in artifacts:
        try:
            if artifact.is_symlink():
                artifact.unlink()
            elif artifact.is_dir():
                shutil.rmtree(artifact)
            else:
                artifact.unlink()
            print(f"  Removed: {artifact}")
        except PermissionError:
            print(f"  ⚠ Permission denied (read-only site-packages?): {artifact}")
        except OSError as exc:
            print(f"  ⚠ Failed to remove {artifact}: {exc}")


def _install_package():
    """Install/upgrade agentic-devtools from PyPI.

    Returns ``(success, self_upgrade_lock)``.  ``self_upgrade_lock`` is True
    in two cases:
    1. **Proactive skip** — running on Windows as the ``agdt-setup.exe``
       autorun executable (``AGDT_SETUP_AUTORUN`` is set).  pip is not
       invoked; the return is immediate to prevent WinError 32 from
       corrupting package metadata.
    2. **Reactive detection** — pip was invoked but failed with WinError 32
       (Windows refused to replace the locked console-script executable).
    In both cases ``success`` is False.  Only the proactive skip guarantees
    the installed version remains intact; the reactive path runs after pip
    has already attempted the uninstall.
    """
    import os
    import sys
    if sys.platform == "win32" and os.environ.get("AGDT_SETUP_AUTORUN"):
        # Proactively skip pip install when spawned by agdt-setup.exe to avoid WinError 32
        # which corrupts metadata before failing.
        return False, True

    stdout_chunks = []
    stderr_chunks = []
    process = subprocess.Popen(
        [sys.executable, "-m", "pip", "install", "--upgrade", "agentic-devtools"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    stdout_thread = threading.Thread(
        target=_stream_subprocess_output,
        args=(process.stdout, sys.stdout, stdout_chunks),
    )
    stderr_thread = threading.Thread(
        target=_stream_subprocess_output,
        args=(process.stderr, sys.stderr, stderr_chunks),
    )
    stdout_thread.start()
    stderr_thread.start()
    stdout_thread.join()
    stderr_thread.join()
    output = "".join(stdout_chunks + stderr_chunks)
    if process.wait() == 0:
        return True, False
    return False, _is_self_upgrade_lock(output)


def _is_self_upgrade_lock(output):
    """Return True when pip failed because a running console script is locked."""
    lowered = output.lower()
    locked = "winerror 32" in lowered or "used by another process" in lowered
    return locked and _SELF_UPGRADE_LOCK_EXECUTABLE in lowered


def _stream_subprocess_output(stream, sink, chunks):
    """Mirror a subprocess text stream to its original sink while accumulating it."""
    if stream is None:
        return
    try:
        while True:
            line = stream.readline()
            if line == "":
                break
            sink.write(line)
            sink.flush()
            chunks.append(line)
    finally:
        stream.close()


def _git_hooks_management_enabled(repo_root):
    """Return False only when project config explicitly disables hooks management.

    Any read failure defaults to True so a broken config never blocks setup.
    """
    config_path = repo_root / ".agdt" / "config" / "project.json"
    try:
        parsed = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return True
    if not isinstance(parsed, dict):
        return True
    value = parsed.get("manage_git_hooks")
    if value is None:
        return True
    if isinstance(value, bool):
        return value
    print(f"{_NON_BOOLEAN_WARNING_PREFIX}{value!r}. Treating it as enabled.", file=sys.stderr)
    return True


def _setup_git_hooks():
    """Configure core.hooksPath to .githooks if in a git repo.

    Non-destructive: an existing core.hooksPath pointing anywhere other than
    .githooks is preserved and no directory is created.
    """
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("  ℹ Not a git repository — skipping git hooks setup.")
        return

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        repo_root = Path(result.stdout.strip())
    except (subprocess.CalledProcessError, OSError):
        repo_root = None

    if repo_root is not None and not _git_hooks_management_enabled(repo_root):
        print(_HOOKS_DISABLED_MESSAGE)
        return

    try:
        result = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            capture_output=True,
            text=True,
        )
        hooks_path_set = result.returncode == 0
        current = result.stdout.strip() if hooks_path_set else ""
    except FileNotFoundError:
        return

    if hooks_path_set and current != ".githooks":
        print(f"{_PRESERVED_MESSAGE_PREFIX}'{current}' — leaving it unchanged.")
        print(_PRESERVED_MESSAGE_SUFFIX)
        return

    try:
        subprocess.run(
            ["git", "config", "core.hooksPath", ".githooks"],
            capture_output=True,
            text=True,
            check=True,
        )
        print("  ✓ core.hooksPath set to '.githooks'")
    except subprocess.CalledProcessError as exc:
        print(f"  ⚠ Failed to set core.hooksPath: {exc}")
        return

    if repo_root is not None:
        try:
            (repo_root / ".githooks").mkdir(parents=True, exist_ok=True)
        except OSError:
            pass


def main():
    parser = argparse.ArgumentParser(
        description="agentic-devtools required setup — self-repair & install.",
    )
    parser.add_argument(
        "--foreground",
        action="store_true",
        default=True,
        help="Run in foreground (default, forward-compatible).",
    )
    parser.parse_args()

    print("─── agentic-devtools Required Setup ─────────────────────────")
    print()

    # Step 1: Detect corrupted artefacts
    print("Scanning for corrupted installation artefacts...")
    artifacts = _detect_corrupted_artifacts()
    if artifacts:
        print(f"  Found {len(artifacts)} corrupted artefact(s):")
        for a in artifacts:
            print(f"    - {a}")
        print()
        print("Cleaning up...")
        _cleanup_artifacts(artifacts)
        print()
    else:
        print("  ✓ No corrupted artefacts detected.")
        print()

    # Step 2: Install/upgrade
    print("Installing/upgrading agentic-devtools from PyPI...")
    installed, self_upgrade_lock = _install_package()
    if installed:
        print("  ✓ agentic-devtools installed/upgraded successfully.")
    elif self_upgrade_lock:
        print(_SELF_UPGRADE_LOCK_MESSAGE, file=sys.stderr)
        print(_SELF_UPGRADE_LOCK_REMEDY, file=sys.stderr)
    else:
        print("  ✗ Failed to install agentic-devtools.", file=sys.stderr)
        sys.exit(1)
    print()

    # Step 3: Git hooks
    print("Configuring git hooks...")
    _setup_git_hooks()
    print()

    print("─── Required Setup Complete ─────────────────────────────────")


if __name__ == "__main__":
    main()
'''

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
    "agdt-* process and run: python -m pip install --upgrade agentic-devtools"
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
    for candidate in ("agentic-devtools", "agentic_devtools"):
        prefix = f"~{candidate[1:]}"
        if name == prefix:
            return True
        if not name.startswith(prefix):
            continue
        remainder = name[len(prefix) :]
        return _has_distribution_suffix(remainder)
    return False


def _is_agentic_devtools_distribution_name(name):
    """Return True for agentic-devtools distribution names and pip backups."""
    if _is_agentic_devtools_tilde_backup(name):
        return True

    for candidate in ("agentic-devtools", "agentic_devtools"):
        if name == candidate:
            return True
        if not name.startswith(candidate):
            continue
        remainder = name[len(candidate) :]
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
    when the failure was Windows refusing to replace the console script of the
    running installation, which is recoverable.
    """
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

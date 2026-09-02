"""Ruff lint, format, mypy type, and markdownlint checks.

All functions capture subprocess output and return ``(passed, output)``
so they can be called from a thread pool without interleaving stdout.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

# Version pin used by .github/workflows/copilot-setup-steps.yml.
MARKDOWNLINT_VERSION = "0.17.2"
MARKDOWNLINT_INSTALL_HINT = f"npm install -g markdownlint-cli2@{MARKDOWNLINT_VERSION}"


def lint_files(files: list[str], *, cwd: str | None = None) -> tuple[bool, str]:
    """Run ruff check on the given files. Returns (passed, output)."""
    if not files:
        return True, ""
    result = subprocess.run(
        ["ruff", "check"] + files,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, (result.stdout + result.stderr).rstrip()


def format_fix_files(files: list[str], *, cwd: str | None = None) -> tuple[bool, str]:
    """Run ruff format (auto-fix) on the given files.

    Returns ``(no_changes_made, format_output)``.
    *True* means all files were already formatted (no changes).
    *False* means files were reformatted (caller should abort push).
    """
    if not files:
        return True, ""
    proc = subprocess.run(
        ["ruff", "format"] + files,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    output = (proc.stdout + proc.stderr).rstrip()
    if proc.returncode != 0:
        return False, f"ERROR: ruff format failed\n{output}".rstrip()

    # Check if any files were modified by the format
    diff = subprocess.run(
        ["git", "diff", "--name-only", "--"] + files,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if diff.stdout.strip():
        return False, output
    return True, output


def format_check_files(files: list[str], *, cwd: str | None = None) -> tuple[bool, str]:
    """Run ruff format --check on the given files. Returns (passed, output)."""
    if not files:
        return True, ""
    result = subprocess.run(
        ["ruff", "format", "--check"] + files,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, (result.stdout + result.stderr).rstrip()


def mypy_check_files(files: list[str], *, cwd: str | None = None) -> tuple[bool, str]:
    """Run mypy on the given files. Returns (passed, output)."""
    if not files:
        return True, ""
    result = subprocess.run(
        ["mypy", "--ignore-missing-imports", "--follow-imports=silent"] + files,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, (result.stdout + result.stderr).rstrip()


def markdownlint_files(files: list[str], *, cwd: str | None = None) -> tuple[bool, str]:
    """Run markdownlint-cli2 on the given markdown files. Returns (passed, output).

    Files deleted in the current change set are skipped (they are resolved
    against ``cwd``), so a delete-only markdown change is a pass. Configuration
    is picked up automatically from ``.markdownlint-cli2.jsonc`` /
    ``.markdownlint.json`` at the repository root.

    When ``markdownlint-cli2`` cannot be executed the check *fails* with an
    actionable message naming the install command — silently skipping would
    recreate the local/CI validation gap this check exists to close.

    ``node`` and ``npm`` are resolved via :func:`shutil.which`. The
    markdownlint-cli2 JavaScript entry point is located by running
    ``npm root -g`` to obtain the global node_modules directory, then
    constructing the path directly. The adjacent ``package.json`` is read to
    enforce the pinned ``markdownlint-cli2`` version used in CI. This avoids
    ``require.resolve``, which does **not** search global node_modules and
    therefore fails when markdownlint-cli2 is installed globally. It also
    bypasses the ``markdownlint-cli2.cmd`` batch shim on Windows: launching a
    ``.cmd`` file routes all arguments through ``cmd.exe``, which expands
    ``%ENV_VAR%`` patterns in PR-supplied file names. Invoking
    ``node <entry-point>`` directly never touches ``cmd.exe``, so untrusted
    filenames are safe.
    """
    if not files:
        return True, ""
    root = Path(cwd) if cwd else Path.cwd()
    existing = [f for f in files if (root / f).is_file()]
    if not existing:
        return True, ""
    node = shutil.which("node")
    if node is None:
        return (
            False,
            f"ERROR: 'node' was not found on PATH.\nInstall Node.js, then run: {MARKDOWNLINT_INSTALL_HINT}",
        )
    npm = shutil.which("npm")
    if npm is None:
        return (
            False,
            f"ERROR: 'npm' was not found on PATH.\nInstall Node.js, then run: {MARKDOWNLINT_INSTALL_HINT}",
        )
    # Resolve the markdownlint-cli2 JS entry point via npm root -g so that
    # globally installed packages are found, the pinned package version can be
    # verified, and file-path arguments are never passed through a .cmd batch
    # shim on Windows.
    try:
        root_result = subprocess.run(
            [npm, "root", "-g"],
            capture_output=True,
            text=True,
            shell=False,  # nosec B603 - args are fixed literals; never user-controlled
        )
    except OSError as exc:
        return False, f"ERROR: could not run npm ({exc}).\nInstall Node.js, then run: {MARKDOWNLINT_INSTALL_HINT}"
    if root_result.returncode != 0:
        return (
            False,
            f"ERROR: could not determine npm global root.\nInstall Node.js, then run: {MARKDOWNLINT_INSTALL_HINT}",
        )
    package_dir = Path(root_result.stdout.strip()) / "markdownlint-cli2"
    entry_point = package_dir / "markdownlint-cli2-bin.mjs"
    if not entry_point.is_file():
        return (
            False,
            f"ERROR: 'markdownlint-cli2' was not found.\nInstall it with: {MARKDOWNLINT_INSTALL_HINT}",
        )
    package_json = package_dir / "package.json"
    try:
        package_data = json.loads(package_json.read_text(encoding="utf-8"))
    except OSError:
        return (
            False,
            "ERROR: could not verify installed markdownlint-cli2 version.\n"
            f"Install it with: {MARKDOWNLINT_INSTALL_HINT}",
        )
    except json.JSONDecodeError:
        return (
            False,
            "ERROR: installed markdownlint-cli2 package metadata is invalid.\n"
            f"Install it with: {MARKDOWNLINT_INSTALL_HINT}",
        )
    if not isinstance(package_data, dict):
        return (
            False,
            "ERROR: installed markdownlint-cli2 package metadata is not a JSON object.\n"
            f"Install it with: {MARKDOWNLINT_INSTALL_HINT}",
        )
    installed_version = package_data.get("version")
    if not isinstance(installed_version, str):
        return (
            False,
            "ERROR: installed markdownlint-cli2 package metadata is missing a string version.\n"
            f"Install it with: {MARKDOWNLINT_INSTALL_HINT}",
        )
    if installed_version != MARKDOWNLINT_VERSION:
        return (
            False,
            "ERROR: installed markdownlint-cli2 version "
            f"{installed_version} does not match required version {MARKDOWNLINT_VERSION}.\n"
            f"Install it with: {MARKDOWNLINT_INSTALL_HINT}",
        )
    try:
        result = subprocess.run(
            [node, str(entry_point), "--no-globs"] + [f":{f}" for f in existing],
            cwd=cwd,
            capture_output=True,
            text=True,
            shell=False,  # nosec B603 - node is a proper binary; file paths are not shell-expanded
        )
    except OSError as exc:
        return False, f"ERROR: could not run markdownlint-cli2 ({exc}).\nInstall it with: {MARKDOWNLINT_INSTALL_HINT}"
    return result.returncode == 0, (result.stdout + result.stderr).rstrip()

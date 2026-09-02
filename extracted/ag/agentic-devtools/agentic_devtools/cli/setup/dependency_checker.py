"""
Unified dependency checker for agentic-devtools.

Checks all external CLI tools that ``agentic-devtools`` depends on and
reports their availability, version, and install path in a formatted table.
"""

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..subprocess_utils import run_safe
from .git_hooks_policy import is_git_hooks_management_enabled

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_MANAGED_BIN_DIR = Path.home() / ".agdt" / "bin"
_GIT_HOOKS_OPTIONAL_CATEGORY = "Optional — only inside a git repository"
_GIT_HOOKS_EXTERNAL_CATEGORY = "Optional — core.hooksPath is managed outside agentic-devtools"
_GIT_HOOKS_DISABLED_CATEGORY = "Optional — hooks management disabled by manage_git_hooks"


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------


@dataclass
class DependencyStatus:
    """Status of a single external CLI dependency.

    Attributes:
        name: The binary name (e.g. ``"git"``, ``"gh"``).
        found: Whether the binary was located.
        path: Absolute path to the binary when *found* is ``True``.
        version: Version string extracted from the binary, or ``None``.
        required: Whether the tool is strictly required for core functionality.
        install_hint: Short hint shown in the report when the tool is missing.
        category: Human-readable category label (``"Required"``, ``"Recommended"``,
            or ``"Optional — ..."``) used for display.
    """

    name: str
    found: bool
    path: str | None = field(default=None)
    version: str | None = field(default=None)
    required: bool = field(default=False)
    install_hint: str = field(default="")
    category: str = field(default="Optional")
    repair_details: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Version extractors
# ---------------------------------------------------------------------------


def _run_version(args: list[str]) -> str | None:
    """Run *args* and return the first non-empty line of stdout.

    Uses ``shell=None`` so that :func:`run_safe` applies its default
    Windows behaviour (``shell=True`` for list args), which is needed for
    tools like ``az`` and ``code`` that are ``.cmd`` shims on Windows.
    The args here are never user-controlled, so this is safe.

    Returns ``None`` on any error or non-zero exit code.
    """
    try:
        result = run_safe(args, capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().splitlines()[0]
    except (OSError, subprocess.TimeoutExpired):
        pass
    return None


def _get_version(name: str, path: str) -> str | None:
    """Return a version string for *name* at *path*, or ``None``."""
    if name == "git":
        raw = _run_version([path, "--version"])
        # "git version 2.43.0" → "2.43.0"
        if raw and raw.startswith("git version "):
            return raw[len("git version ") :].strip()
        return raw
    if name in ("gh", "copilot"):
        raw = _run_version([path, "--version"])
        if raw:
            # "gh version 2.65.0 (2025-01-01)" → "2.65.0"
            parts = raw.split()
            for i, part in enumerate(parts):
                if part == "version" and i + 1 < len(parts):
                    return parts[i + 1]
            # Fallback: return first token that looks like a version
            for part in parts:
                if part and (part[0].isdigit() or part.startswith("v")):
                    return part
        return raw
    if name == "az":
        raw = _run_version([path, "--version"])
        if raw:
            # "azure-cli  2.57.0" → "2.57.0"
            parts = raw.split()
            for part in parts:
                if part and (part[0].isdigit() or part.startswith("v")):
                    return part
        return raw
    if name == "code":
        return _run_version([path, "--version"])
    return _run_version([path, "--version"])


# ---------------------------------------------------------------------------
# Dependency definitions
# ---------------------------------------------------------------------------


def _find_binary(name: str) -> str | None:
    """Locate *name* in the managed bin dir first, then on ``PATH``."""
    managed = _MANAGED_BIN_DIR / (name + (".exe" if sys.platform == "win32" else ""))
    if managed.is_file():
        return str(managed)
    return shutil.which(name)


def _check_dependency(
    name: str,
    *,
    required: bool,
    install_hint: str,
    category: str,
) -> DependencyStatus:
    """Check a single dependency and return its :class:`DependencyStatus`."""
    path = _find_binary(name)
    if not path:
        return DependencyStatus(
            name=name,
            found=False,
            required=required,
            install_hint=install_hint,
            category=category,
        )
    version = _get_version(name, path)
    return DependencyStatus(
        name=name,
        found=True,
        path=path,
        version=version,
        required=required,
        install_hint=install_hint,
        category=category,
    )


# ---------------------------------------------------------------------------
# Configuration checks (PATH profile, git hooks)
# ---------------------------------------------------------------------------


def _check_path_profile() -> DependencyStatus:
    """Check whether ``~/.agdt/bin`` is present as a PATH component.

    Reads the user's shell profile (bash/zsh/PowerShell) and searches for
    a PATH-assignment line containing the managed bin directory as an exact
    PATH component.

    When the shell type is unknown (e.g. fish), no profile path can be
    determined; the check is non-blocking (``required=False``) because the
    auto-repair cannot run in this scenario either.

    Returns:
        ``DependencyStatus(name="path-profile", ...)`` with ``found=True``
        if the entry is present, ``found=False`` otherwise.  ``required=True``
        for supported shells; ``required=False`` for unknown shells.
    """
    from .shell_profile import (
        _path_assignment_contains_entry,
        detect_shell_profile,
        detect_shell_type,
    )

    shell_type = detect_shell_type()
    profile_path = detect_shell_profile()
    path_entry = str(_MANAGED_BIN_DIR)

    if profile_path is None:
        if shell_type == "unknown":
            # Unknown shell — cannot detect profile; non-blocking
            return DependencyStatus(
                name="path-profile",
                found=False,
                required=False,
                install_hint="Manually add ~/.agdt/bin to PATH in your shell profile",
                category="Optional — unknown shell",
            )
        return DependencyStatus(
            name="path-profile",
            found=False,
            required=True,
            install_hint="run: agdt-setup (or agdt-setup-check --fix)",
            category="Required",
        )

    if not profile_path.exists():
        return DependencyStatus(
            name="path-profile",
            found=False,
            required=True,
            install_hint="run: agdt-setup (or agdt-setup-check --fix)",
            category="Required",
        )

    try:
        content = profile_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return DependencyStatus(
            name="path-profile",
            found=False,
            required=True,
            install_hint="run: agdt-setup (or agdt-setup-check --fix)",
            category="Required",
        )

    if shell_type in ("bash", "zsh"):
        path_line_re = re.compile(r"^\s*(?:export\s+)?PATH\s*=")
    else:  # powershell
        path_line_re = re.compile(r"^\s*\$env:PATH\s*=", re.IGNORECASE)

    for line in content.splitlines():
        if path_line_re.match(line) and _path_assignment_contains_entry(line, path_entry, shell_type):
            return DependencyStatus(
                name="path-profile",
                found=True,
                path=str(profile_path),
                required=True,
                category="Required",
            )

    return DependencyStatus(
        name="path-profile",
        found=False,
        required=True,
        install_hint="run: agdt-setup (or agdt-setup-check --fix)",
        category="Required",
    )


def _check_git_hooks_config() -> DependencyStatus:
    """Check whether ``core.hooksPath`` is set to ``.githooks``.

    When not inside a git repository or git is not available, the check
    returns ``found=False, required=False`` (non-blocking).  It is also
    non-blocking when ``manage_git_hooks`` is ``false`` in
    ``.agdt/config/project.json``, or when ``core.hooksPath`` points at a
    path owned by another hooks manager (Husky, pre-commit, …) — that value
    is preserved rather than reported as a missing dependency.

    Returns:
        ``DependencyStatus(name="git-hooks", ...)``
    """
    # Check if we're in a git repo
    try:
        in_repo = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except FileNotFoundError:
        # git not available — non-blocking
        return DependencyStatus(
            name="git-hooks",
            found=False,
            required=False,
            install_hint="Install git first",
            category=_GIT_HOOKS_OPTIONAL_CATEGORY,
        )
    except subprocess.TimeoutExpired:
        return DependencyStatus(
            name="git-hooks",
            found=False,
            required=False,
            category=_GIT_HOOKS_OPTIONAL_CATEGORY,
        )

    if in_repo.returncode != 0:
        # Not in a git repo — non-blocking
        return DependencyStatus(
            name="git-hooks",
            found=False,
            required=False,
            install_hint="Run from inside a git repository",
            category=_GIT_HOOKS_OPTIONAL_CATEGORY,
        )

    # Get repo root for .githooks dir check
    try:
        toplevel = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # git disappeared or timed out — treat as non-blocking (same as git-missing)
        return DependencyStatus(
            name="git-hooks",
            found=False,
            required=False,
            category=_GIT_HOOKS_OPTIONAL_CATEGORY,
        )

    if toplevel.returncode != 0:
        # show-toplevel failed (e.g. detached HEAD, bare repo, or unexpected error)
        # — cannot validate .githooks dir; treat as non-blocking
        return DependencyStatus(
            name="git-hooks",
            found=False,
            required=False,
            category=_GIT_HOOKS_OPTIONAL_CATEGORY,
        )

    repo_root = Path(toplevel.stdout.strip())

    # Check current hooksPath config
    try:
        config_result = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # git disappeared or timed out — treat as non-blocking
        return DependencyStatus(
            name="git-hooks",
            found=False,
            required=False,
            category=_GIT_HOOKS_OPTIONAL_CATEGORY,
        )

    hooks_path_set = config_result.returncode == 0
    current = config_result.stdout.strip() if hooks_path_set else ""

    if not is_git_hooks_management_enabled(repo_root):
        return DependencyStatus(
            name="git-hooks",
            found=True,
            path=current or "(not configured)",
            required=False,
            category=_GIT_HOOKS_DISABLED_CATEGORY,
        )

    if current == ".githooks" and (repo_root / ".githooks").is_dir():
        return DependencyStatus(
            name="git-hooks",
            found=True,
            path=str(repo_root / ".githooks"),
            required=True,
            category="Required",
        )

    if hooks_path_set and current != ".githooks":
        return DependencyStatus(
            name="git-hooks",
            found=True,
            path=current or "(empty)",
            required=False,
            category=_GIT_HOOKS_EXTERNAL_CATEGORY,
        )

    return DependencyStatus(
        name="git-hooks",
        found=False,
        required=True,
        install_hint="run: agdt-setup-check --fix",
        category="Required",
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def check_all_dependencies() -> list[DependencyStatus]:
    """Check all external CLI dependencies.

    Returns:
        A list of :class:`DependencyStatus` objects, one per tool.
    """
    results = [
        _check_dependency(
            "copilot",
            required=False,
            install_hint="run: agdt-setup-copilot-cli",
            category="Recommended",
        ),
        _check_dependency(
            "gh",
            required=False,
            install_hint="run: agdt-setup-gh-cli  (or https://cli.github.com/)",
            category="Recommended",
        ),
        _check_dependency(
            "git",
            required=True,
            install_hint="https://git-scm.com/downloads",
            category="Required",
        ),
        _check_dependency(
            "az",
            required=False,
            install_hint="https://docs.microsoft.com/cli/azure/install-azure-cli",
            category="Optional — needed for Azure DevOps",
        ),
        _check_dependency(
            "code",
            required=False,
            install_hint="https://code.visualstudio.com/",
            category="Optional — needed for VS Code integration",
        ),
    ]
    results.append(_check_path_profile())
    results.append(_check_git_hooks_config())
    return results


def print_dependency_report(statuses: list[DependencyStatus]) -> None:
    """Pretty-print a dependency status table to stdout.

    Args:
        statuses: List of :class:`DependencyStatus` objects to display.
    """
    print("\nDependency Check:")

    name_width = max(len(s.name) for s in statuses) + 2
    version_width = 10

    for s in statuses:
        icon = "✅" if s.found else "❌"
        name = s.name.ljust(name_width)
        version = (s.version or "—").ljust(version_width)
        location = s.path if s.path else "not found"
        category = s.category
        line = f"  {icon} {name}{version}  {location:<40}  ({category})"
        print(line)
        if not s.found and s.install_hint:
            print(f"       Install: {s.install_hint}")

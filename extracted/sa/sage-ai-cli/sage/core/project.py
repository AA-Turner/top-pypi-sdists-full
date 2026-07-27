"""Project discovery and test command utilities for SAGE.

This module contains functions for:
- Detecting project roots in workspaces and monorepos
- Finding test commands for different languages (Python, JS, Go, Rust)
- Identifying test files and runnable files

Extracted from main.py for better code organization (P3-74).
"""

from __future__ import annotations

import json
import os
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Iterator

__all__ = [
    "detect_test_files",
    "detect_runnable_files",
    "discover_workspace_project_roots",
    "project_root_score",
    "default_project_root",
    "discover_npm_script",
    "discover_python_test_command",
    "discover_project_test_command",
    "discover_project_full_test_command",
    "discover_project_root_for_file",
    "command_from_project_root",
    "validation_command_for_written_files",
    "safe_walk",
    "is_git_repo",
    # Constants
    "PROJECT_MARKERS",
    "SKIP_DIRS",
]


# Project root markers - files that indicate a project root
PROJECT_MARKERS: tuple[str, ...] = (
    "pyproject.toml",
    "package.json",
    "Cargo.toml",
    "go.mod",
)

def is_git_repo(path: Path) -> bool:
    """Check if a directory is a git repository efficiently."""
    try:
        if (path / ".git").exists():
            return True
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=2,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception:
        return False


def safe_walk(
    cwd: Path,
    *,
    skip_dirs: set[str] | None = None,
    max_files: int = 10000,
    include_hidden: bool = False,
) -> Iterator[Path]:
    """Efficiently walk a directory, skipping common ignored paths.
    
    Uses os.walk for better performance and early directory pruning.
    """
    if skip_dirs is None:
        skip_dirs = SKIP_DIRS

    count = 0
    for root, dirs, files in os.walk(cwd):
        # Prune directories in-place
        dirs[:] = [
            d for d in dirs 
            if (include_hidden or not d.startswith(".")) and d not in skip_dirs
        ]
        
        root_path = Path(root)
        for f in files:
            if not include_hidden and f.startswith("."):
                continue
            
            yield root_path / f
            count += 1
            if count >= max_files:
                return


# Directories to skip during project discovery
SKIP_DIRS: set[str] = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
}


def detect_test_files(written: list[str]) -> list[str]:
    """Return test file paths from a list of written files.

    Args:
        written: List of file paths

    Returns:
        List of paths that are Python test files
    """
    return [f for f in written if Path(f).name.startswith("test_") and f.endswith(".py")]


def detect_runnable_files(written: list[str]) -> list[str]:
    """Return Python files that can be syntax-checked.

    Args:
        written: List of file paths

    Returns:
        List of Python file paths
    """
    return [f for f in written if f.endswith(".py")]


def discover_workspace_project_roots(cwd: Path, max_depth: int = 3) -> list[Path]:
    """Find likely project roots under the current workspace.

    Searches for directories containing project markers like pyproject.toml,
    package.json, Cargo.toml, or go.mod.

    Args:
        cwd: Current working directory to search from
        max_depth: Maximum directory depth to search

    Returns:
        List of paths to discovered project roots
    """
    roots: list[Path] = []
    seen: set[Path] = set()

    def _is_project_root(path: Path) -> bool:
        return any((path / marker).exists() for marker in PROJECT_MARKERS)

    def _walk(path: Path, depth: int) -> None:
        resolved = path.resolve()
        if resolved in seen:
            return
        seen.add(resolved)

        if _is_project_root(path):
            roots.append(resolved)

        if depth >= max_depth:
            return

        try:
            children = list(path.iterdir())
        except OSError:
            return

        for child in children:
            if not child.is_dir():
                continue
            if child.name in SKIP_DIRS or child.name.startswith("."):
                continue
            _walk(child, depth + 1)

    _walk(cwd.resolve(), 0)
    return roots


def project_root_score(project_root: Path, cwd: Path) -> tuple[int, int, int]:
    """Score a project root so the most relevant nested app wins.

    Higher scores indicate more relevant project roots.

    Args:
        project_root: Path to the project root
        cwd: Current working directory

    Returns:
        Tuple of (relevance_score, relative_depth, absolute_depth)
    """
    score = 0
    if (project_root / "sage").is_dir():
        score += 12
    if (project_root / "tests" / "sage").is_dir():
        score += 10
    if (project_root / "backend").is_dir():
        score += 4
    if (project_root / "frontend").is_dir():
        score += 4
    if (project_root / "tests").is_dir():
        score += 3
    if (project_root / "pyproject.toml").exists():
        score += 4
    if (project_root / "package.json").exists():
        score += 2
    rel_depth = len(project_root.relative_to(cwd.resolve()).parts)
    return (score, rel_depth, len(project_root.parts))


def default_project_root(cwd: Path) -> Path:
    """Pick the most relevant project root in the workspace.

    Args:
        cwd: Current working directory

    Returns:
        Path to the most relevant project root, or cwd if none found
    """
    roots = discover_workspace_project_roots(cwd)
    if not roots:
        return cwd.resolve()
    return max(roots, key=lambda root: project_root_score(root, cwd))


def discover_npm_script(project_root: Path, script_name: str) -> str | None:
    """Return an npm script definition when package.json declares it.

    Args:
        project_root: Path to the project root
        script_name: Name of the npm script to find

    Returns:
        The script command if found, None otherwise
    """
    package_json = project_root / "package.json"
    if not package_json.exists():
        return None
    try:
        data = json.loads(package_json.read_text("utf-8"))
    except (ValueError, OSError):
        return None

    scripts = data.get("scripts")
    if not isinstance(scripts, dict):
        return None
    value = scripts.get(script_name)
    if not isinstance(value, str):
        return None
    value = value.strip()
    if not value or "no test specified" in value.lower():
        return None
    return value


def discover_python_test_command(
    project_root: Path,
    prefer_sage_subset: bool = False,
    full_suite: bool = False,
) -> str | None:
    """Return the best Python test command for a project root.

    Args:
        project_root: Path to the project root
        prefer_sage_subset: If True, prefer running sage-specific tests
        full_suite: If True, return full test suite command

    Returns:
        Test command string if pytest is available, None otherwise
    """
    has_pytest_suite = any(
        (project_root / marker).exists()
        for marker in ("tests", "pytest.ini", "tox.ini", Path("sage") / "tests")
    )
    if not has_pytest_suite:
        return None

    if full_suite:
        return "python -m pytest -v --tb=short"

    if (
        prefer_sage_subset
        and (project_root / "sage").exists()
        and (project_root / "tests" / "sage").exists()
    ):
        return "python -m pytest tests/sage -v --tb=short"
    return "python -m pytest -v --tb=short"


def discover_project_test_command(project_root: Path) -> str | None:
    """Return a project-aware test command for Python, JS, Go, or Rust.

    Args:
        project_root: Path to the project root

    Returns:
        Appropriate test command for the project type
    """
    js_test = discover_npm_script(project_root, "test")
    if js_test:
        lower = js_test.lower()
        if "vitest" in lower:
            return "npm test -- --run"
        if "jest" in lower:
            return "npm test -- --runInBand"
        if "react-scripts test" in lower:
            return "CI=1 npm test -- --watch=false"
        return "npm test"

    python_cmd = discover_python_test_command(project_root, prefer_sage_subset=True)
    if python_cmd:
        return python_cmd

    if (project_root / "Cargo.toml").exists():
        return "cargo test"
    if (project_root / "go.mod").exists():
        return "go test ./..."
    return None


def discover_project_full_test_command(project_root: Path) -> str | None:
    """Return the best full-project validation command for a project root.

    Args:
        project_root: Path to the project root

    Returns:
        Full test suite command for the project type
    """
    js_test = discover_npm_script(project_root, "test")
    if js_test:
        lower = js_test.lower()
        if "vitest" in lower:
            return "npm test -- --run"
        if "jest" in lower:
            return "npm test -- --runInBand"
        if "react-scripts test" in lower:
            return "CI=1 npm test -- --watch=false"
        return "npm test"

    python_cmd = discover_python_test_command(project_root, full_suite=True)
    if python_cmd:
        return python_cmd

    if (project_root / "Cargo.toml").exists():
        return "cargo test"
    if (project_root / "go.mod").exists():
        return "go test ./..."
    return None


def discover_project_root_for_file(filepath: str, cwd: Path) -> Path:
    """Find the nearest project root that owns a written file.

    Args:
        filepath: Relative path to the file
        cwd: Current working directory

    Returns:
        Path to the nearest project root
    """
    try:
        target = (cwd / filepath).resolve()
    except (OSError, ValueError):
        return cwd.resolve()

    workspace_root = cwd.resolve()
    if not str(target).startswith(str(workspace_root)):
        return workspace_root

    current = target if target.is_dir() else target.parent
    markers = ("pyproject.toml", "package.json", "Cargo.toml", "go.mod", "tests")
    while True:
        if any((current / marker).exists() for marker in markers):
            return current
        if current == workspace_root:
            return workspace_root
        parent = current.parent
        if not str(parent).startswith(str(workspace_root)):
            return workspace_root
        current = parent


def command_from_project_root(project_root: Path, command: str, cwd: Path) -> str:
    """Prefix a command with directory context when validation belongs to a nested project.

    Args:
        project_root: Path to the project root
        command: Command to execute
        cwd: Current working directory

    Returns:
        Command with [cwd=...] prefix if needed
    """
    root = project_root.resolve()
    base = cwd.resolve()
    if root == base:
        return command
    rel = root.relative_to(base)
    return f"[cwd={rel.as_posix()}] {command}"


def validation_command_for_written_files(
    written: list[str], cwd: Path, shell_quote_func=None
) -> str | None:
    """Return the best validation command for changed files in a workspace.

    Args:
        written: List of written file paths
        cwd: Current working directory
        shell_quote_func: Optional function to quote shell arguments

    Returns:
        Appropriate validation command for the written files
    """
    if not written:
        project_root = default_project_root(cwd)
        inner = discover_project_test_command(project_root)
        if inner:
            return command_from_project_root(project_root, inner, cwd)
        return None

    roots = Counter(discover_project_root_for_file(fp, cwd) for fp in written)
    project_root = max(roots.items(), key=lambda item: (item[1], len(item[0].resolve().parts)))[0]

    normalized: list[str] = []
    for fp in written:
        try:
            target = (cwd / fp).resolve()
            if str(target).startswith(str(project_root.resolve())):
                normalized.append(target.relative_to(project_root).as_posix())
        except (OSError, ValueError):
            continue

    test_files = detect_test_files(normalized)
    if test_files:
        if shell_quote_func:
            quoted = " ".join(shell_quote_func(path) for path in test_files)
        else:
            # Simple quoting fallback
            quoted = " ".join(f"'{path}'" for path in test_files)
        inner = f"python -m pytest {quoted} -v --tb=short"
        return command_from_project_root(project_root, inner, cwd)

    if any(path.endswith(".py") for path in normalized):
        prefer_sage_subset = any(
            Path(path).parts and Path(path).parts[0] == "sage" for path in normalized
        )
        inner = discover_python_test_command(project_root, prefer_sage_subset=prefer_sage_subset)
        if inner:
            return command_from_project_root(project_root, inner, cwd)

    if any(
        path.endswith((".js", ".jsx", ".ts", ".tsx")) or path == "package.json"
        for path in normalized
    ):
        inner = discover_project_test_command(project_root)
        if inner:
            return command_from_project_root(project_root, inner, cwd)

    inner = discover_project_test_command(project_root)
    if inner:
        return command_from_project_root(project_root, inner, cwd)
    return None


# Backward compatibility aliases (prefixed versions for main.py)
_detect_test_files = detect_test_files
_detect_runnable_files = detect_runnable_files
_discover_workspace_project_roots = discover_workspace_project_roots
_project_root_score = project_root_score
_default_project_root = default_project_root
_discover_npm_script = discover_npm_script
_discover_python_test_command = discover_python_test_command
_discover_project_test_command = discover_project_test_command
_discover_project_full_test_command = discover_project_full_test_command
_discover_project_root_for_file = discover_project_root_for_file
_command_from_project_root = command_from_project_root
_validation_command_for_written_files = validation_command_for_written_files

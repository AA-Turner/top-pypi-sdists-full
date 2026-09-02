"""Related test file discovery for source context enrichment.

Identifies test files related to a given source file using both the 1:1:1
convention (``tests/unit/<module_path>/<stem>/test_*.py``) and the legacy
flat convention (``tests/test_<module>.py``). When no verified local checkout
is available, the module can still infer remote candidate paths from the source
path and source content so the ADO fetcher can try them directly.
"""

from __future__ import annotations

import ast
import logging
import subprocess
from pathlib import Path
from typing import Any, cast

logger = logging.getLogger(__name__)

# Preferred in-repo package root prefix (stripped when present).
_PACKAGE_PREFIX = "agentic_devtools/"

# Source files that never have dedicated test files under the 1:1:1 policy, so
# they must not be flagged as ``missing_tests``.
_NON_TESTABLE_FILENAMES = frozenset({"__init__.py", "_version.py"})

# Module-level cache for the detected repo root, so repeated calls within
# the same process only invoke `git rev-parse` once.
_cached_repo_root: Path | None | bool = False  # False = not yet resolved


def _normalize_module_path(source_path: str) -> str:
    """Normalize a source path to a repo-relative Python module path."""
    if source_path.startswith(_PACKAGE_PREFIX):
        return source_path[len(_PACKAGE_PREFIX) :]
    if source_path.startswith(f"/{_PACKAGE_PREFIX}"):
        return source_path[len(f"/{_PACKAGE_PREFIX}") :]
    return source_path.lstrip("/")


def _discover_1to1_tests(source_path: str, repo_root: Path) -> list[str]:
    """Discover tests using 1:1:1 convention.

    Maps ``agentic_devtools/cli/git/core.py`` to
    ``tests/unit/cli/git/core/test_*.py``.

    Args:
        source_path: Source file path relative to repo root.
        repo_root: Repository root directory.

    Returns:
        List of test file paths (relative to repo root) that exist.
    """
    # Strip known package prefix when present; otherwise use generic repo-relative path.
    module_path = _normalize_module_path(source_path)

    # Remove .py extension and build test directory path
    if not module_path.endswith(".py"):
        return []

    module_path_no_ext = module_path[:-3]
    parts = module_path_no_ext.split("/")
    # The stem is the filename without extension
    stem = parts[-1]
    # Build test directory: tests/unit/<parent_dirs>/<stem>/
    parent_dirs = "/".join(parts[:-1])
    if parent_dirs:
        test_dir = repo_root / "tests" / "unit" / parent_dirs / stem
    else:
        test_dir = repo_root / "tests" / "unit" / stem

    if not test_dir.is_dir():
        return []

    results = []
    for test_file in sorted(test_dir.glob("test_*.py")):
        results.append(test_file.relative_to(repo_root).as_posix())

    return results


def _discover_legacy_flat_tests(source_path: str, repo_root: Path) -> list[str]:
    """Discover tests using legacy flat convention.

    Maps ``agentic_devtools/cli/release/commands.py`` to
    ``tests/test_release_commands.py``.

    Args:
        source_path: Source file path relative to repo root.
        repo_root: Repository root directory.

    Returns:
        List of test file paths (relative to repo root) that exist.
    """
    candidate = _build_legacy_flat_test_candidate(source_path)
    if candidate is None:
        return []

    results = []
    candidate_path = repo_root / candidate
    if candidate_path.is_file():
        results.append(candidate)

    return results


def _build_legacy_flat_test_candidate(source_path: str) -> str | None:
    """Build the legacy flat test candidate path without checking the filesystem."""
    module_path = _normalize_module_path(source_path)
    if not module_path.endswith(".py"):
        return None

    module_path_no_ext = module_path[:-3]
    parts = module_path_no_ext.split("/")
    base_name = parts[-1]

    if parts[-3:] == ["cli", "release", "commands"]:
        flat_test_name = f"test_release_{base_name}.py"
    else:
        flat_test_name = f"test_{base_name}.py"
    return f"tests/{flat_test_name}"


def _infer_remote_test_candidates(source_path: str, source_content: str | None) -> list[str]:
    """Infer test file candidates without a verified local checkout."""
    module_path = _normalize_module_path(source_path)
    if not module_path.endswith(".py"):
        return []

    module_path_no_ext = module_path[:-3]
    parts = module_path_no_ext.split("/")
    stem = parts[-1]
    parent_dirs = "/".join(parts[:-1])
    test_dir = f"tests/unit/{parent_dirs}/{stem}" if parent_dirs else f"tests/unit/{stem}"

    inferred: list[str] = []
    if isinstance(source_content, str) and source_content.strip():
        try:
            tree = ast.parse(source_content)
        except SyntaxError:
            tree = None
        if tree is not None:
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    inferred.append(f"{test_dir}/test_{node.name}.py")
                elif isinstance(node, ast.ClassDef):
                    inferred.append(f"{test_dir}/test_{node.name.lower()}.py")

    inferred.append(_build_legacy_flat_test_candidate(source_path) or "")
    inferred = [candidate for candidate in inferred if candidate]
    return sorted(set(inferred))


def discover_related_tests(
    source_path: str,
    repo_root: Path | str | None = None,
    *,
    source_content: str | None = None,
    auto_detect_repo_root: bool = True,
) -> dict[str, Any]:
    """Discover related test files for a source file.

    Combines results from both 1:1:1 and legacy flat conventions.

    Args:
        source_path: Source file path (repo-relative, may have leading slash).
        repo_root: Repository root directory. If None, attempts to detect unless
            ``auto_detect_repo_root`` is false.
        source_content: Optional source content used to infer test candidates
            when no verified local checkout is available.
        auto_detect_repo_root: Whether to auto-detect a local repo root when
            ``repo_root`` is not provided.

    Returns:
        Dict with ``related_tests`` (list of paths) and ``missing_tests`` (bool).
    """
    # Normalize path
    clean_path = source_path.lstrip("/")

    # Non-Python paths cannot have related Python tests.
    if not clean_path.endswith(".py"):
        return {"related_tests": [], "missing_tests": False}

    # Package scaffolding files (``__init__.py``, ``_version.py``) never have dedicated
    # test files under the 1:1:1 policy, so they must not be reported as missing tests.
    if clean_path.rsplit("/", 1)[-1] in _NON_TESTABLE_FILENAMES:
        return {"related_tests": [], "missing_tests": False}

    if repo_root is None:
        if not auto_detect_repo_root:
            inferred_tests = _infer_remote_test_candidates(clean_path, source_content)
            return {"related_tests": inferred_tests, "missing_tests": False}
        global _cached_repo_root
        if _cached_repo_root is False:
            try:
                result = subprocess.run(
                    ["git", "rev-parse", "--show-toplevel"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    shell=False,
                )
                _cached_repo_root = (
                    Path(result.stdout.strip()) if result.returncode == 0 and result.stdout.strip() else None
                )
            except Exception:
                _cached_repo_root = None
        if _cached_repo_root is None:
            return {"related_tests": [], "missing_tests": True}
        repo_root = cast(Path, _cached_repo_root)
    else:
        repo_root = Path(repo_root)

    # Combine both conventions
    tests_1to1 = _discover_1to1_tests(clean_path, repo_root)
    tests_flat = _discover_legacy_flat_tests(clean_path, repo_root)

    # Merge and deduplicate, maintaining sorted order
    all_tests = sorted(set(tests_1to1 + tests_flat))

    return {
        "related_tests": all_tests,
        "missing_tests": len(all_tests) == 0,
    }

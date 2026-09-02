"""Git diff helpers for identifying changed files."""

from __future__ import annotations

import ast
import subprocess
from pathlib import Path

EXCLUDE_PATTERNS = {"__pycache__", "_version.py"}
COVERAGE_EXCLUDE_PATTERNS = {"__init__.py", "__main__.py", "templates/"}


class DiffUnavailableError(RuntimeError):
    """Raised when git diff cannot determine changed files."""


def _is_shared_test_support(name: str) -> bool:
    """Return True for non-runnable shared test-support modules.

    These are modules other test files depend on but that must not be executed
    directly: ``conftest.py`` and underscore-prefixed helper modules such as
    ``_contract_scenarios.py``. ``__init__.py`` is a package marker, not a
    support module, so it is excluded.
    """
    if name == "__init__.py":
        return False
    return name == "conftest.py" or name.startswith("_")


def get_changed_files(
    base_ref: str = "origin/main",
    *,
    pattern: str = "*.py",
    source_only: bool = False,
    tests_only: bool = False,
    tests_support_only: bool = False,
    cwd: str | Path | None = None,
) -> list[str]:
    """Return changed files between base_ref and HEAD.

    Uses merge-base diff (``...``) for accurate results. If the primary
    diff fails (e.g. ``origin/main`` not available), tries local fallbacks
    suitable for shallow repositories. Raises :class:`DiffUnavailableError`
    when all strategies fail.

    Args:
        base_ref: Git ref to diff against.
        pattern: Glob pattern for git diff (e.g. '*.py').
        source_only: Only return files under agentic_devtools/.
        tests_only: Only return runnable files under tests/ (excludes
            ``__init__.py``, ``conftest.py``, and underscore-prefixed helpers).
        tests_support_only: Only return changed shared test-support modules
            under tests/ (``conftest.py`` and underscore-prefixed helpers).
            These are not runnable directly; use :func:`find_consumer_test_paths`
            to map them to their consumer suites.
        cwd: Working directory for git commands.

    Returns:
        List of relative file paths.

    Raises:
        DiffUnavailableError: When both diff strategies fail.
    """
    cwd_str = str(cwd) if cwd else None
    pathspecs = []
    if source_only:
        pathspecs = ["agentic_devtools/*.py", "agentic_devtools/**/*.py"]
    elif tests_only or tests_support_only:
        pathspecs = ["tests/**/*.py"]
    else:
        if "/" not in pattern and "\\" not in pattern:
            pathspecs = [pattern, f"**/{pattern}"]
        else:
            pathspecs = [pattern]

    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=d", f"{base_ref}...HEAD", "--"] + pathspecs,
            capture_output=True,
            text=True,
            cwd=cwd_str,
        )
    except (FileNotFoundError, OSError) as exc:
        raise DiffUnavailableError(f"git diff unavailable (could not execute git): {exc}") from exc
    if result.returncode != 0:
        # Fallbacks for local-only and shallow repositories.
        fallback_cmds = [
            ["git", "diff", "--name-only", "--diff-filter=d", "HEAD~10..HEAD", "--"] + pathspecs,
            ["git", "diff", "--name-only", "--diff-filter=d", "HEAD~1..HEAD", "--"] + pathspecs,
            [
                "git",
                "diff-tree",
                "--no-commit-id",
                "--name-only",
                "-r",
                "--diff-filter=d",
                "HEAD",
                "--",
            ]
            + pathspecs,
        ]
        for cmd in fallback_cmds:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd_str)
            except (FileNotFoundError, OSError) as exc:
                raise DiffUnavailableError(f"git diff unavailable (could not execute git): {exc}") from exc
            if result.returncode == 0:
                break
        else:
            raise DiffUnavailableError(
                f"git diff failed for '{base_ref}...HEAD' and local fallbacks. Cannot determine changed files."
            )
    files = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if any(pat in line for pat in EXCLUDE_PATTERNS):
            continue
        if source_only and any(pat in line for pat in COVERAGE_EXCLUDE_PATTERNS):
            continue
        name = Path(line).name
        if tests_only and (name == "__init__.py" or _is_shared_test_support(name)):
            continue
        if tests_support_only and not _is_shared_test_support(name):
            continue
        files.append(line)
    return files


def find_consumer_test_paths(support_file: str, *, cwd: str | Path | None = None) -> list[str]:
    """Map a shared test-support file to the test paths that must run for it.

    Shared support modules are not runnable directly, so a change to one would
    otherwise select no tests. This resolves each to its consumers:

    * ``conftest.py`` applies to its whole directory subtree, so its containing
      directory is returned (running it exercises every affected test).
    * An underscore-prefixed helper module (e.g. ``_contract_scenarios.py``) is
      mapped to every runnable ``test_*.py`` file that imports it by module stem.

    Args:
        support_file: Repo-relative path to the changed support module.
        cwd: Repository root used to resolve and scan the ``tests/`` tree.

    Returns:
        A de-duplicated, sorted list of repo-relative consumer paths (test
        files or a directory). Empty when no consumers are found.
    """
    base = Path(cwd) if cwd else Path.cwd()
    rel = Path(support_file)
    if rel.name == "conftest.py":
        parent = rel.parent
        return [str(parent)] if str(parent) not in ("", ".") else ["tests"]

    stem = rel.stem
    tests_root = base / "tests"
    if not tests_root.is_dir():
        return []
    consumers: set[str] = set()
    for path in tests_root.rglob("test_*.py"):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if _file_imports_stem(text, stem):
            consumers.add(str(path.relative_to(base)))
    return sorted(consumers)


def _file_imports_stem(text: str, stem: str) -> bool:
    """Return True if *text* contains any import that references *stem*.

    Uses AST parsing to handle multiline imports correctly; falls back to
    line-based heuristic when the source cannot be parsed.
    """
    try:
        tree = ast.parse(text)
    except SyntaxError:
        # Fall back to simple substring check for unparseable files
        return any("import" in line and stem in line for line in text.splitlines())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(stem in alias.name for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if stem in module:
                return True
            if any(stem in alias.name for alias in node.names):
                return True
    return False

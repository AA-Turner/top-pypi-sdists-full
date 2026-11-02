"""Git diff helpers for identifying changed files."""

from __future__ import annotations

import ast
import os
import re
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


def get_strict_committed_changed_files(cwd: str | Path | None = None) -> list[str]:
    """Return surviving repository-relative paths committed in ``origin/main...HEAD``.

    Use ``cwd`` as Git's working directory, or the current directory when omitted.
    Staged, unstaged, and untracked-only changes are not included. No path
    exclusions or fallback revisions are applied.

    Raises:
        DiffUnavailableError: If the exact committed diff cannot be obtained.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "-z", "--diff-filter=d", "origin/main...HEAD", "--"],
            capture_output=True,
            check=True,
            cwd=str(cwd) if cwd is not None else None,
            shell=False,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise DiffUnavailableError(
            f"git diff origin/main...HEAD unavailable: {exc}. Run `git fetch origin main` and retry."
        ) from exc
    return [os.fsdecode(path) for path in result.stdout.split(b"\0") if path]


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
        A de-duplicated, sorted list of POSIX-form repo-relative consumer paths (test
        files or a directory). Empty when no consumers are found.
    """
    base = Path(cwd) if cwd else Path.cwd()
    rel = Path(support_file)
    if rel.name == "conftest.py":
        parent = rel.parent
        return [parent.as_posix()] if str(parent) not in ("", ".") else ["tests"]

    stem = rel.stem
    tests_root = base / "tests"
    if not tests_root.is_dir():
        return []
    consumers: set[str] = set()
    for path in tests_root.rglob("test_*.py"):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError, UnicodeDecodeError:
            continue
        if _file_imports_stem(text, stem):
            consumers.add(path.relative_to(base).as_posix())
    return sorted(consumers)


def _get_parent_package_initializers(module: str, module_paths: dict[str, Path]) -> set[str]:
    """Return indexed package initializers executed before an imported module."""
    parts = module.split(".")
    parents = set()
    for index in range(1, len(parts)):
        parent = ".".join(parts[:index])
        if parent in module_paths and module_paths[parent].name == "__init__.py":
            parents.add(parent)
    return parents


def _get_imported_module_names(module: str, path: Path, module_paths: dict[str, Path]) -> set[str]:
    """Return local module names statically imported by one Python file."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except OSError, UnicodeDecodeError, SyntaxError:
        return set()

    imports: set[str] = set()
    module_parts = module.split(".")
    package_parts = module_parts if path.name == "__init__.py" else module_parts[:-1]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_names = {alias.name for alias in node.names}
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                if node.level > len(package_parts):
                    continue
                imported_parts = package_parts[: len(package_parts) - node.level + 1]
            else:
                imported_parts = []
            if node.module:
                imported_parts.extend(node.module.split("."))
            imported_names = {".".join(imported_parts)}
            imported_names.update(".".join([*imported_parts, *alias.name.split(".")]) for alias in node.names)
        else:
            continue

        for name in imported_names:
            imports.update(_get_parent_package_initializers(name, module_paths))
        imports.update(name for name in imported_names if name in module_paths)
    return imports


def _build_static_import_graph(base: Path) -> tuple[dict[str, Path], dict[str, str], dict[str, set[str]]]:
    """Index repository modules and map each imported module to its importers."""
    module_paths: dict[str, Path] = {}
    path_modules: dict[str, str] = {}
    for root_name in ("agentic_devtools", "tests"):
        root = base / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*.py"):
            relative = path.relative_to(base)
            parts = list(relative.parts)
            if parts[-1] == "__init__.py":
                parts.pop()
            else:
                parts[-1] = Path(parts[-1]).stem
            module = ".".join(parts)
            module_paths[module] = path
            path_modules[relative.as_posix()] = module

    reverse_imports: dict[str, set[str]] = {}
    for importer, path in module_paths.items():
        imported_modules = _get_imported_module_names(importer, path, module_paths)
        imported_modules.update(_get_parent_package_initializers(importer, module_paths))
        for imported in imported_modules:
            reverse_imports.setdefault(imported, set()).add(importer)
    return module_paths, path_modules, reverse_imports


def _find_reverse_dependent_test_paths(changed_source: list[str], *, cwd: str | Path | None = None) -> list[str]:
    """Return statically dependent test targets, including scoped fixture consumers.

    Reachable conftests select explicit runnable tests in their scope.
    """
    if not changed_source:
        return []

    base = Path(cwd) if cwd else Path.cwd()
    module_paths, path_modules, reverse_imports = _build_static_import_graph(base)
    changed_modules = {
        path_modules[path.replace("\\", "/")] for path in changed_source if path.replace("\\", "/") in path_modules
    }
    if not changed_modules:
        return []

    pending = list(changed_modules)
    visited = set(changed_modules)
    test_paths: set[str] = set()
    while pending:
        imported = pending.pop()
        for importer in reverse_imports.get(imported, ()):
            if importer in visited:
                continue
            visited.add(importer)
            path = module_paths[importer]
            if path.name == "conftest.py" and path.is_relative_to(base / "tests"):
                if path.parent == base / "tests":
                    test_paths.update(test.relative_to(base).as_posix() for test in (base / "tests").rglob("test_*.py"))
                else:
                    test_paths.update(find_consumer_test_paths(path.relative_to(base).as_posix(), cwd=base))
            elif path.name.startswith("test_") and path.is_relative_to(base / "tests"):
                test_paths.add(path.relative_to(base).as_posix())
            pending.append(importer)
    return sorted(test_paths)


def _filter_test_targets(
    targets: list[str],
    *,
    cwd: Path,
    covered_dirs: set[Path],
    covered_files: set[Path],
) -> list[str]:
    """Remove covered and nested targets while preserving their input order."""
    expanded_targets: list[str] = []
    covered_paths = covered_dirs | covered_files
    for target in dict.fromkeys(targets):
        candidate = (cwd / target).resolve(strict=False)
        if candidate.is_dir() and any(candidate in path.parents for path in covered_paths):
            expanded_targets.extend(path.relative_to(cwd).as_posix() for path in sorted(candidate.rglob("test_*.py")))
        else:
            expanded_targets.append(target)

    candidates = []
    for target in dict.fromkeys(expanded_targets):
        candidate = (cwd / target).resolve(strict=False)
        if candidate in covered_files or any(
            candidate == directory or directory in candidate.parents for directory in covered_dirs
        ):
            continue
        candidates.append((target, candidate))

    selected_dirs = {candidate for _, candidate in candidates if candidate.suffix != ".py"}
    return [
        target
        for target, candidate in candidates
        if not any(directory in candidate.parents for directory in selected_dirs)
    ]


def get_python_module_moves(base_ref: str = "origin/main", *, cwd: str | Path | None = None) -> list[tuple[str, str]]:
    """Return old/new source paths for renames and content-backed extractions.

    Use the same revision fallback order as ``get_changed_files``. Missing move
    metadata is best-effort and never causes selection of a broad test suite.
    """
    base = Path(cwd) if cwd else Path.cwd()
    strategies = [
        (["git", "diff"], f"{base_ref}...HEAD"),
        (["git", "diff"], "HEAD~10..HEAD"),
        (["git", "diff"], "HEAD~1..HEAD"),
        (["git", "diff-tree", "--no-commit-id", "-r"], "HEAD"),
    ]
    for command, revision in strategies:
        try:
            result = subprocess.run(
                [*command, "--name-status", "-z", "--find-renames", revision, "--", "agentic_devtools"],
                capture_output=True,
                text=True,
                cwd=str(base),
                shell=False,
            )
        except OSError:
            return []
        if result.returncode == 0:
            return _parse_python_module_moves(result.stdout, command, revision, base)
    return []


def _parse_python_module_moves(output: str, command: list[str], revision: str, cwd: Path) -> list[tuple[str, str]]:
    """Parse NUL-separated statuses, checking content for delete/add or extraction pairs."""
    records = iter(output.rstrip("\0").split("\0"))
    moves: set[tuple[str, str]] = set()
    origins: list[str] = []
    additions: list[str] = []
    for status in records:
        path = next(records, "")
        if status.startswith("R"):
            new = next(records, "")
            if path.endswith(".py") and new.endswith(".py"):
                moves.add((path, new))
        elif path.endswith(".py"):
            if status in {"D", "M"}:
                origins.append(path)
            elif status == "A":
                additions.append(path)
    moves.update(_pair_python_module_moves(origins, additions, command, revision, cwd))
    return sorted(moves)


def _pair_python_module_moves(
    origins: list[str], additions: list[str], command: list[str], revision: str, cwd: Path
) -> set[tuple[str, str]]:
    """Pair removed source content with added modules, without relying on filenames."""
    moves: set[tuple[str, str]] = set()
    if not additions:
        return moves
    definition_pattern = re.compile(r"^(?:async\s+)?(?:def|class)\s+\w+")
    for old in origins:
        removed = _removed_python_lines(command, revision, old, cwd)
        for new in additions:
            try:
                added = _python_content_lines((cwd / new).read_text(encoding="utf-8"))
            except OSError, UnicodeDecodeError:
                continue
            # Require substantive overlap, not just common imports or blank lines.
            shared = removed & added
            has_moved_definition = any(definition_pattern.match(line) for line in shared)
            if has_moved_definition and len(shared) >= 3 and len(shared) >= len(added) / 2:
                moves.add((old, new))
    return moves


def _python_content_lines(text: str) -> set[str]:
    """Return substantive Python lines used to recognize moved source content."""
    return {
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith(("#", "import ", "from "))
    }


def _removed_python_lines(command: list[str], revision: str, path: str, cwd: Path) -> set[str]:
    """Read removed lines from the same revision range as the move metadata."""
    try:
        result = subprocess.run(
            [*command, "--no-ext-diff", "--no-renames", "-p", "--unified=0", revision, "--", path],
            capture_output=True,
            text=True,
            cwd=str(cwd),
            shell=False,
        )
    except OSError:
        return set()
    if result.returncode != 0:
        return set()
    return _python_content_lines(
        "\n".join(
            line[1:] for line in result.stdout.splitlines() if line.startswith("-") and not line.startswith("---")
        )
    )


def find_workflow_contract_tests(moves: list[tuple[str, str]], *, cwd: str | Path | None = None) -> list[str]:
    """Find only workflow test files naming either side of a detected module move."""
    if not moves:
        return []
    base = Path(cwd) if cwd else Path.cwd()
    path_references: set[str] = set()
    module_references: set[str] = set()
    for move in moves:
        for path in move:
            normalized = path.replace("\\", "/")
            path_references.add(normalized)
            module_references.add(normalized.removesuffix(".py").replace("/", "."))
    paths = "|".join(re.escape(ref) for ref in sorted(path_references))
    modules = "|".join(re.escape(ref) for ref in sorted(module_references))
    pattern = re.compile(r"(?<![\w./])(?:" + paths + r")(?![\w./])|(?<![\w.])(?:" + modules + r")(?!\w)")
    consumers = []
    for test_path in sorted((base / "tests" / "workflows").rglob("test_*.py")):
        try:
            text = test_path.read_text(encoding="utf-8").replace("\\\\", "/").replace("\\", "/")
        except OSError, UnicodeDecodeError:
            continue
        if pattern.search(text):
            consumers.append(test_path.relative_to(base).as_posix())
    return consumers


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

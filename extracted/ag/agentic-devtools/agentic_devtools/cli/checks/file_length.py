"""Guard physical Python file length using the shared quality baseline."""

from __future__ import annotations

import fnmatch
import os
import time
from collections.abc import Iterator
from pathlib import Path

from agentic_devtools.cli.checks.check_result import _CheckResult
from agentic_devtools.cli.checks.quality_baseline import read_quality_baseline

_WARNING_LINES = 200
_HARD_LIMIT_LINES = 500
_SOURCE_ROOTS = ("agentic_devtools", "scripts", "tests", ".github", ".agents", ".agdt")
_IGNORED_RUNTIME_ROOTS = frozenset({".agdt/workflows/", ".agdt/cache/"})


def _iter_source_python_files(root: Path, directory: Path) -> Iterator[tuple[str, Path]]:
    """Yield Python files under a source root, excluding generated agent state."""
    for current_directory, directory_names, file_names in os.walk(directory):
        current_path = Path(current_directory)
        relative_directory = current_path.relative_to(root).as_posix()
        directory_names[:] = [
            name for name in directory_names if f"{relative_directory}/{name}/" not in _IGNORED_RUNTIME_ROOTS
        ]
        for file_name in file_names:
            path = current_path / file_name
            if fnmatch.fnmatch(file_name, "*.py"):
                yield path.relative_to(root).as_posix(), path


def _check_file_lengths(repo_root: str | Path) -> _CheckResult:
    """Wrap the file-length guard in the result type used by the checks runner."""
    started = time.monotonic()
    passed, output = check_file_lengths(repo_root)
    return _CheckResult("File length", passed, output, time.monotonic() - started)


def check_file_lengths(repo_root: str | Path) -> tuple[bool, str]:
    """Check Python source and test lengths against ``quality-baseline.json``.

    The baseline records a grow-only ceiling for existing oversized files.
    Files above the warning threshold are reported, while new files above the
    hard limit and growth beyond an existing baseline fail the check.
    """
    root = Path(repo_root)
    file_lengths, _, error = read_quality_baseline(root)
    if error is not None:
        return False, error

    python_files = {path.relative_to(root).as_posix(): path for path in root.glob("*.py")}
    for directory_name in _SOURCE_ROOTS:
        directory = root / directory_name
        if directory.is_dir():
            for relative_path, path in _iter_source_python_files(root, directory):
                python_files[relative_path] = path

    errors: list[str] = []
    warnings: list[str] = []
    current_paths: set[str] = set()
    for relative_path, path in sorted(python_files.items()):
        current_paths.add(relative_path)
        try:
            with path.open(encoding="utf-8") as source_file:
                line_count = sum(1 for _ in source_file)
        except (OSError, UnicodeError) as exc:
            return False, f"ERROR: Could not read {relative_path}: {exc}"

        baseline_lines = file_lengths.get(relative_path)
        has_error = False
        if baseline_lines is None:
            if line_count > _HARD_LIMIT_LINES:
                errors.append(f"FAIL: {relative_path}: {line_count} lines exceeds the 500-line hard limit.")
                has_error = True
        elif line_count > baseline_lines:
            errors.append(f"FAIL: {relative_path}: {line_count} lines exceeds its baseline of {baseline_lines} lines.")
            has_error = True

        if not has_error and line_count > _WARNING_LINES:
            warnings.append(f"WARNING: {relative_path}: {line_count} lines exceeds the 200-line warning threshold.")
        elif not has_error and baseline_lines is not None:
            warnings.append(f"WARNING: {relative_path} is now compliant at {line_count} lines; retain its baseline.")

    for relative_path in sorted(file_lengths):
        if relative_path not in current_paths:
            warnings.append(f"WARNING: Baseline entry {relative_path} is missing; retain the grow-only entry.")

    messages = [*errors, *warnings]
    if not messages:
        return True, "OK — no Python files exceed the configured thresholds."
    return not errors, "\n".join(messages)

"""pytest-xdist selection for large per-file coverage runs."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

_XDIST_TEST_FILE_THRESHOLD = 30
_MAX_XDIST_WORKERS = 4
_MAX_CONCURRENT_CHECK_WORKERS = 8


def count_runnable_test_files(test_targets: list[str], cwd: str | Path | None) -> int:
    """Count unique existing ``test_*.py`` files represented by pytest targets."""
    base = Path(cwd) if cwd is not None else Path.cwd()
    test_files: set[Path] = set()
    for target in test_targets:
        path = (base / target.split("::", 1)[0]).resolve(strict=False)
        if path.is_file() and path.name.startswith("test_") and path.suffix == ".py":
            test_files.add(path)
        elif path.is_dir():
            test_files.update(
                candidate.resolve(strict=False) for candidate in path.rglob("test_*.py") if candidate.is_file()
            )
    return len(test_files)


def get_changed_test_xdist_args(
    test_targets: list[str],
    cwd: str | Path | None,
    *,
    cpu_count: int | None,
    xdist_available: bool,
) -> list[str]:
    """Return bounded xdist arguments for a large, safe changed-test batch."""
    if count_runnable_test_files(test_targets, cwd) <= _XDIST_TEST_FILE_THRESHOLD:
        return []
    if not xdist_available or cpu_count is None or cpu_count <= 0:
        return []

    base = Path(cwd) if cwd is not None else Path.cwd()
    target_parts = [
        Path(os.path.normcase(os.fspath((base / target.split("::", 1)[0]).resolve(strict=False)))).parts
        for target in test_targets
    ]
    for index, parts in enumerate(target_parts):
        for other in target_parts[index + 1 :]:
            if (
                len(parts) < len(other)
                and other[: len(parts)] == parts
                or len(other) < len(parts)
                and parts[: len(other)] == other
            ):
                return []

    worker_count = min(
        _MAX_XDIST_WORKERS,
        max(0, cpu_count - _MAX_CONCURRENT_CHECK_WORKERS - 1),
    )
    if worker_count < 2:
        return []
    return ["-n", str(worker_count), "--dist", "loadfile"]


def get_xdist_args(
    test_path: Path,
    *,
    coverage_workers: int,
    cpu_count: int | None = None,
    distribution: Literal["loadfile", "worksteal"] = "loadfile",
) -> list[str]:
    """Return xdist arguments for a large test directory within the CPU budget."""
    if coverage_workers <= 0:
        raise ValueError("coverage_workers must be a positive integer")
    if not test_path.is_dir():
        return []

    test_file_count = sum(1 for _ in test_path.rglob("test_*.py"))
    if test_file_count <= _XDIST_TEST_FILE_THRESHOLD:
        return []

    available_cpus = cpu_count if cpu_count is not None else os.cpu_count()
    # Each coverage job reserves one CPU for its pytest controller; xdist gets the remainder.
    worker_count = min(_MAX_XDIST_WORKERS, max(available_cpus or 1, 1) // coverage_workers - 1)
    if worker_count <= 1:
        return []
    return ["-n", str(worker_count), "--dist", distribution]

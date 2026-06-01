"""Shared file-walk logic for collecting text files from artifact directories."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

import structlog

logger = structlog.get_logger(__name__)

MAX_SINGLE_FILE_BYTES = 1_048_576  # 1 MB
MAX_TOTAL_BYTES = 5_242_880  # 5 MB

SKIP_DIRS = {"node_modules", ".venv", "venv", "vendor", "dist", ".tox", ".git"}


@dataclass
class CollectedFile:
    """A single text file collected from an artifact directory."""

    title: str
    content: str


def collect_files(
    root: Path,
    supported_extensions: set[str],
    *,
    max_single: int | None = None,
    max_total: int | None = None,
    skip_dirs: set[str] | None = None,
) -> tuple[list[CollectedFile], list[str], bool]:
    """Walk *root* and collect text files matching *supported_extensions*.

    Returns:
        (files, symlinks_found, oversized)
    """
    if max_single is None:
        max_single = MAX_SINGLE_FILE_BYTES
    if max_total is None:
        max_total = MAX_TOTAL_BYTES
    if skip_dirs is None:
        skip_dirs = SKIP_DIRS
    files: list[CollectedFile] = []
    symlinks: list[str] = []
    oversized = False
    budget_exceeded = False
    total_bytes = 0
    resolved_root = root.resolve()

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        dp = Path(dirpath)
        for fname in sorted(filenames):
            fpath = dp / fname
            if fpath.suffix not in supported_extensions:
                continue

            if fpath.is_symlink():
                try:
                    target = fpath.resolve()
                except OSError:
                    symlinks.append(str(fpath))
                    continue
                if not target.is_relative_to(resolved_root):
                    symlinks.append(str(fpath))
                    continue

            try:
                size = fpath.stat().st_size
            except OSError:
                continue

            if size > max_single:
                oversized = True
                continue

            if total_bytes + size > max_total:
                oversized = True
                budget_exceeded = True
                break

            try:
                content = fpath.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            total_bytes += size
            rel = fpath.relative_to(root)
            title = PurePosixPath(rel).as_posix()
            files.append(CollectedFile(title=title, content=content))

        if budget_exceeded:
            break

    return files, symlinks, oversized

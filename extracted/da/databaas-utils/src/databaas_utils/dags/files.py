"""Which files under the DAG directory a deploy ships."""

from __future__ import annotations

import fnmatch
import os
from collections.abc import Iterable
from pathlib import Path

from databaas_utils.errors import ConfigurationError

# Matched against every path component, so `.venv` also drops `pkg/.venv/...`.
DEFAULT_EXCLUDES: tuple[str, ...] = (
    "__pycache__",
    "*.pyc",
    ".git",
    ".venv",
    ".DS_Store",
)


def _excluded(relative: str, patterns: tuple[str, ...]) -> bool:
    return any(
        fnmatch.fnmatchcase(part, pattern)
        for part in relative.split("/")
        for pattern in patterns
    )


def collect_files(root: Path, excludes: Iterable[str] = ()) -> dict[str, Path]:
    """Relative posix path -> file, for every regular file under `root`.

    Symlinks are refused rather than followed or skipped: either would make the
    deployed tree differ from what the deployer sees.

    Raises:
        ConfigurationError: If `root` is not a directory or holds a symlink.
    """
    root = Path(root)
    if not root.is_dir():
        raise ConfigurationError(f"DAG directory {root} does not exist")
    patterns = (*DEFAULT_EXCLUDES, *excludes)
    found: dict[str, Path] = {}
    for current, dirs, names in os.walk(root):
        base = Path(current)
        rel_base = base.relative_to(root).as_posix()
        prefix = "" if rel_base == "." else f"{rel_base}/"
        kept = []
        for name in sorted(dirs):
            relative = f"{prefix}{name}"
            if _excluded(relative, patterns):
                continue
            if (base / name).is_symlink():
                raise ConfigurationError(f"symlinks cannot be deployed: {relative}")
            kept.append(name)
        dirs[:] = kept
        for name in sorted(names):
            relative = f"{prefix}{name}"
            if _excluded(relative, patterns):
                continue
            path = base / name
            if path.is_symlink():
                raise ConfigurationError(f"symlinks cannot be deployed: {relative}")
            if path.is_file():
                found[relative] = path
    return found

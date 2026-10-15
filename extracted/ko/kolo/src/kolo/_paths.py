"""
Lightweight path utilities for kolo.

This module is designed to be imported with minimal overhead - it only uses
stdlib imports. Heavy modules like cerberus and toolz are NOT imported here.

Used by db.py and _emit_auto.py to avoid importing the full config module.
"""

from __future__ import annotations

import logging
import os
import shutil
import stat
from pathlib import Path
from typing import Tuple

logger = logging.getLogger("kolo")


class KoloWriteError(Exception):
    """Raised when kolo cannot write to the filesystem."""

    pass


INTERNAL_DIR = ".internal"


# Every trace session resolves the store; remember the on-disk state from the last full pass
# to skip the mkdirs/rewrites, and redo the pass when any of it no longer matches.
_GITIGNORE_CONTENT = ".internal/\nkolo.txt\n.gitignore\n.ignore\ntraces/*\n"
_IGNORE_CONTENT = (
    "# ripgrep .ignore file - makes traces/ searchable despite being gitignored\n"
    "# ripgrep reads .gitignore (to respect git) but .ignore takes precedence\n"
    "# The ! prefix negates the pattern, un-ignoring traces/* for search\n"
    "!traces/*\n"
)
_KoloDirectoryState = Tuple[Tuple[int, ...], ...]
_KoloDirectoryPaths = Tuple[str, ...]
_kolo_directories: dict[
    Tuple[str, str], Tuple[Path, _KoloDirectoryPaths, _KoloDirectoryState]
] = {}


def _kolo_directory_paths(kolo_directory: Path) -> _KoloDirectoryPaths:
    """Directories, then ignore files, then the legacy and current databases."""
    root = os.fspath(kolo_directory)
    internal = os.path.join(root, INTERNAL_DIR)
    return (
        root,
        internal,
        os.path.join(internal, "raw"),
        os.path.join(root, "traces"),
        os.path.join(root, ".gitignore"),
        os.path.join(root, ".ignore"),
        os.path.join(root, "db.sqlite3"),
        os.path.join(internal, "db.sqlite3"),
    )


def _kolo_directory_state(paths: _KoloDirectoryPaths) -> _KoloDirectoryState | None:
    """Identify everything the full pass creates, or None if any is missing.

    Directories are identified by device and inode only: their mtimes change
    whenever a trace is written. The two ignore files also include mode, size,
    mtime and ctime, so an edit, rewrite or permission change triggers a full
    pass (Windows reports a read-only file through its mode, not its ctime).
    """
    state: list[Tuple[int, ...]] = []
    try:
        for directory in paths[:4]:
            result = os.stat(directory)
            if not stat.S_ISDIR(result.st_mode):
                return None
            state.append((result.st_dev, result.st_ino))
        for ignore_file in paths[4:6]:
            result = os.stat(ignore_file)
            if not stat.S_ISREG(result.st_mode):
                return None
            state.append(
                (
                    result.st_dev,
                    result.st_ino,
                    result.st_mode,
                    result.st_size,
                    result.st_mtime_ns,
                    result.st_ctime_ns,
                )
            )
    except OSError:
        return None
    # A pre-.internal database still waiting to be migrated needs a full pass.
    if os.path.exists(paths[6]) and not os.path.exists(paths[7]):
        return None
    return tuple(state)


def _same_directory(path: str, identity: Tuple[int, ...]) -> bool:
    """Whether path (following symlinks) is still the cached directory.

    The cache holds the resolved path, so a symlink in KOLO_PATH or the
    working directory that now points elsewhere must not reuse it.
    """
    try:
        result = os.stat(path)
    except OSError:
        return False
    return (result.st_dev, result.st_ino) == identity


def create_kolo_directory() -> Path:
    """
    Create the kolo directory and contents if they do not exist.

    Returns the path to the .kolo directory for convenience.
    """
    kolo_path = os.environ.get("KOLO_PATH", ".")
    key = (kolo_path, "" if os.path.isabs(kolo_path) else os.getcwd())
    cached = _kolo_directories.get(key)
    if (
        cached is not None
        and _same_directory(os.path.join(kolo_path, ".kolo"), cached[2][0])
        and _kolo_directory_state(cached[1]) == cached[2]
    ):
        return cached[0]

    kolo_directory = _create_kolo_directory(kolo_path)
    paths = _kolo_directory_paths(kolo_directory)
    state = _kolo_directory_state(paths)
    if state is not None:
        _kolo_directories[key] = (kolo_directory, paths, state)
    return kolo_directory


def _create_kolo_directory(kolo_path: str) -> Path:
    kolo_directory = (Path(kolo_path) / ".kolo").resolve()
    try:
        kolo_directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        message = f"Could not create .kolo directory at {kolo_directory}."
        raise KoloWriteError(message) from e

    internal_directory = kolo_directory / INTERNAL_DIR
    try:
        internal_directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        message = f"Could not create .internal directory at {internal_directory}."
        raise KoloWriteError(message) from e

    raw_traces_directory = internal_directory / "raw"
    try:
        raw_traces_directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        message = f"Could not create raw directory at {raw_traces_directory}."
        raise KoloWriteError(message) from e

    _migrate_old_structure(kolo_directory, internal_directory, raw_traces_directory)

    traces_directory = kolo_directory / "traces"
    try:
        traces_directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        message = f"Could not create traces directory at {traces_directory}."
        raise KoloWriteError(message) from e

    gitignore_path = kolo_directory / ".gitignore"
    try:
        with open(gitignore_path, "w") as gitignore:
            gitignore.write(_GITIGNORE_CONTENT)
    except Exception as e:
        message = f"Could not write to {gitignore_path}."
        raise KoloWriteError(message) from e

    # ripgrep's .ignore takes precedence over .gitignore, exposing traces to search.
    ignore_path = kolo_directory / ".ignore"
    try:
        with open(ignore_path, "w") as f:
            f.write(_IGNORE_CONTENT)
    except Exception as e:  # pragma: no cover
        message = f"Could not write to {ignore_path}."
        raise KoloWriteError(message) from e

    return kolo_directory.resolve()


def _migrate_old_structure(
    kolo_directory: Path, internal_directory: Path, raw_traces_directory: Path
) -> None:
    """
    Migrate old directory structure to new .internal/ structure.

    Old structure:
        .kolo/db.sqlite3

    New structure:
        .kolo/.internal/db.sqlite3, .kolo/.internal/raw/
    """
    old_db = kolo_directory / "db.sqlite3"
    new_db = internal_directory / "db.sqlite3"
    if old_db.exists() and not new_db.exists():
        try:
            shutil.move(str(old_db), str(new_db))
        except OSError as e:
            logger.warning(f"Failed to migrate database from {old_db} to {new_db}: {e}")
            return

        for wal_file in ["db.sqlite3-shm", "db.sqlite3-wal"]:
            old_wal = kolo_directory / wal_file
            if old_wal.exists():
                try:
                    shutil.move(str(old_wal), str(internal_directory / wal_file))
                except OSError as e:  # pragma: no cover
                    logger.warning(f"Failed to migrate WAL file {old_wal}: {e}")

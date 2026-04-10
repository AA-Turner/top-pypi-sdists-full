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
from pathlib import Path

logger = logging.getLogger("kolo")


class KoloWriteError(Exception):
    """Raised when kolo cannot write to the filesystem."""

    pass


# Internal directory name for plumbing (db, raw traces)
# Hidden with . prefix, keeps user-facing files at top level
INTERNAL_DIR = ".internal"


def create_kolo_directory() -> Path:
    """
    Create the kolo directory and contents if they do not exist.

    Returns the path to the .kolo directory for convenience.
    """
    kolo_directory = (Path(os.environ.get("KOLO_PATH", ".")) / ".kolo").resolve()
    try:
        kolo_directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        message = f"Could not create .kolo directory at {kolo_directory}."
        raise KoloWriteError(message) from e

    # Create .internal directory for plumbing (db, raw traces)
    internal_directory = kolo_directory / INTERNAL_DIR
    try:
        internal_directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        message = f"Could not create .internal directory at {internal_directory}."
        raise KoloWriteError(message) from e

    # Create raw directory inside .internal for file-based trace storage
    raw_traces_directory = internal_directory / "raw"
    try:
        raw_traces_directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        message = f"Could not create raw directory at {raw_traces_directory}."
        raise KoloWriteError(message) from e

    # Migrate old structure to new structure
    _migrate_old_structure(kolo_directory, internal_directory, raw_traces_directory)

    # Create traces directory for emitted traces
    traces_directory = kolo_directory / "traces"
    try:
        traces_directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        message = f"Could not create traces directory at {traces_directory}."
        raise KoloWriteError(message) from e

    # Write .gitignore to exclude generated files from git
    gitignore_path = kolo_directory / ".gitignore"
    try:
        with open(gitignore_path, "w") as gitignore:
            gitignore.write(".internal/\n")
            gitignore.write("kolo.txt\n")
            gitignore.write(".gitignore\n")
            gitignore.write(".ignore\n")
            gitignore.write("traces/*\n")
    except Exception as e:
        message = f"Could not write to {gitignore_path}."
        raise KoloWriteError(message) from e

    # Write .ignore to make traces/ searchable by ripgrep despite being gitignored
    # ripgrep reads both .gitignore and .ignore, but .ignore takes precedence
    # The !traces/* pattern negates the gitignore, making traces visible to rg
    # See: https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md#automatic-filtering
    ignore_path = kolo_directory / ".ignore"
    try:
        with open(ignore_path, "w") as f:
            f.write(
                "# ripgrep .ignore file - makes traces/ searchable despite being gitignored\n"
            )
            f.write(
                "# ripgrep reads .gitignore (to respect git) but .ignore takes precedence\n"
            )
            f.write(
                "# The ! prefix negates the pattern, un-ignoring traces/* for search\n"
            )
            f.write("!traces/*\n")
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
    # Migrate db.sqlite3 and WAL files
    old_db = kolo_directory / "db.sqlite3"
    new_db = internal_directory / "db.sqlite3"
    if old_db.exists() and not new_db.exists():
        try:
            shutil.move(str(old_db), str(new_db))
        except OSError as e:
            logger.warning(f"Failed to migrate database from {old_db} to {new_db}: {e}")
            return  # Don't try to move WAL files if main DB failed

        # Also move WAL files if they exist
        for wal_file in ["db.sqlite3-shm", "db.sqlite3-wal"]:
            old_wal = kolo_directory / wal_file
            if old_wal.exists():
                try:
                    shutil.move(str(old_wal), str(internal_directory / wal_file))
                except OSError as e:  # pragma: no cover
                    logger.warning(f"Failed to migrate WAL file {old_wal}: {e}")

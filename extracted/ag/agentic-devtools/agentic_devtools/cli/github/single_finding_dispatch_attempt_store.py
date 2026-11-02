"""Durable storage for single-finding dispatch attempt records."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from agentic_devtools.cli.github.single_finding_dispatch import AcceptancePersistenceError
from agentic_devtools.file_locking import FileLockError, locked_file

_SKIP_DIRECTORY_FSYNC = os.name == "nt" and not hasattr(os, "O_DIRECTORY")


def write_attempt_record(path: Path, record: dict[str, Any], timeout_seconds: int) -> None:
    """Atomically write and durably sync one dispatch attempt record."""
    lock_path = path.with_suffix(f"{path.suffix}.lock")
    temporary_path: Path | None = None
    try:
        with locked_file(lock_path, mode="a+", timeout=timeout_seconds):
            try:
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    encoding="utf-8",
                    dir=path.parent,
                    prefix=f".{path.name}.",
                    suffix=".tmp",
                    delete=False,
                ) as output:
                    temporary_path = Path(output.name)
                    output.write(json.dumps(record, sort_keys=True))
                    output.flush()
                    os.fsync(output.fileno())
                os.replace(temporary_path, path)
                if not _SKIP_DIRECTORY_FSYNC:
                    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                    directory_fd = os.open(path.parent, flags)
                    try:
                        os.fsync(directory_fd)
                    finally:
                        os.close(directory_fd)
                temporary_path = None
            finally:
                if temporary_path is not None:
                    temporary_path.unlink(missing_ok=True)
    except (FileLockError, OSError, TypeError, ValueError) as error:
        raise AcceptancePersistenceError(f"could not durably persist dispatch acceptance: {error}") from error

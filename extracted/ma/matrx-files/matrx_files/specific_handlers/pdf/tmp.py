"""Temporary file management for the PDF subsystem.

The handler historically wrote PDFs to `tempfile.NamedTemporaryFile(delete=False)`
and relied on best-effort cleanup in `finally`. A crash between write and unlink
leaks a file in the temp directory; in a long-running worker those add up.

This module provides:

- ``pdf_temp_dir()`` — a single namespaced directory under the system temp root
  (``<system-tmp>/matrx_pdf/``) so we can sweep our own files without touching
  others.
- ``write_pdf_bytes_to_temp()`` — returns the absolute path of the newly written
  PDF and never falls through to a deletion check (caller deletes via ``finally``
  or the startup sweep eventually catches it).
- ``cleanup_tmp_older_than(seconds)`` — sweep helper, intended to be invoked at
  process startup to clean up orphans from prior runs.
- ``pdf_temp_file(...)`` — context-manager wrapper for the common
  "write bytes, get a path, clean up on exit" pattern.
"""

from __future__ import annotations

import os
import tempfile
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


_NAMESPACE = "matrx_pdf"


def pdf_temp_dir() -> Path:
    base = Path(tempfile.gettempdir()) / _NAMESPACE
    base.mkdir(parents=True, exist_ok=True)
    return base


def write_pdf_bytes_to_temp(pdf_bytes: bytes, suffix: str = ".pdf") -> Path:
    name = f"{uuid.uuid4().hex}{suffix}"
    path = pdf_temp_dir() / name
    path.write_bytes(pdf_bytes)
    return path


@contextmanager
def pdf_temp_file(pdf_bytes: bytes, suffix: str = ".pdf") -> Iterator[Path]:
    """Write *pdf_bytes* to a namespaced temp file; unlink on exit."""
    path = write_pdf_bytes_to_temp(pdf_bytes, suffix=suffix)
    try:
        yield path
    finally:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass


def cleanup_tmp_older_than(seconds: int = 3600) -> int:
    """Remove namespaced temp files older than *seconds*. Returns count removed.

    Safe to call repeatedly; missing dir is a no-op. Errors per-file are logged
    to stdout (no exception is raised — sweep is best-effort).
    """
    base = pdf_temp_dir()
    if not base.exists():
        return 0
    now = time.time()
    removed = 0
    for entry in base.iterdir():
        try:
            if not entry.is_file():
                continue
            age = now - entry.stat().st_mtime
            if age < seconds:
                continue
            entry.unlink(missing_ok=True)
            removed += 1
        except OSError as exc:
            print(f"[matrx-pdf-tmp] cleanup failed for {entry}: {exc}")
    return removed


def install_startup_cleanup_hook(seconds: int = 3600) -> int:
    """Convenience entry point for host apps to wire into FastAPI startup."""
    return cleanup_tmp_older_than(seconds=seconds)


__all__ = [
    "pdf_temp_dir",
    "write_pdf_bytes_to_temp",
    "pdf_temp_file",
    "cleanup_tmp_older_than",
    "install_startup_cleanup_hook",
]

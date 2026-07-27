"""Item #14 — Distributed RAG sync (push/pull project index to GCS)."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

__all__ = ["push_index", "pull_index"]


def _have_gsutil() -> bool:
    return shutil.which("gsutil") is not None


def _gcs_uri(db_path: Path, bucket: str) -> str:
    return f"{bucket}/rag/{db_path.name}"


def push_index(db_path: Path, *, bucket: str) -> bool:
    if not _have_gsutil():
        return False
    if not db_path.is_file():
        return False
    try:
        r = subprocess.run(
            ["gsutil", "-q", "cp", str(db_path), _gcs_uri(db_path, bucket)],
            capture_output=True, text=True, timeout=300,
        )
        return r.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def pull_index(db_path: Path, *, bucket: str) -> bool:
    if not _have_gsutil():
        return False
    db_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(
            ["gsutil", "-q", "cp", _gcs_uri(db_path, bucket), str(db_path)],
            capture_output=True, text=True, timeout=300,
        )
        return r.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

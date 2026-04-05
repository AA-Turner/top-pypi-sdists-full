"""Durable output storage and inspection for background tasks.

Provides file-based stdout/stderr capture, retrieval with tailing,
and size-capped file management. Extends BackgroundTaskManager from #1311.
"""

from __future__ import annotations

import logging
import re
import shutil
from collections import deque
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection

logger = logging.getLogger(__name__)

MAX_OUTPUT_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
_UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)


def task_output_dir(data_dir: Path, conversation_id: str) -> Path:
    """Return the output directory for a conversation's background tasks."""
    return data_dir / "task_output" / conversation_id


def ensure_task_output_dir(data_dir: Path, conversation_id: str) -> Path:
    """Create and return the output directory for a conversation's tasks."""
    out_dir = task_output_dir(data_dir, conversation_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def stdout_path(data_dir: Path, conversation_id: str, task_id: str) -> Path:
    return task_output_dir(data_dir, conversation_id) / f"{task_id}.stdout"


def stderr_path(data_dir: Path, conversation_id: str, task_id: str) -> Path:
    return task_output_dir(data_dir, conversation_id) / f"{task_id}.stderr"


def read_task_output(
    file_path: Path,
    *,
    tail_lines: int | None = None,
) -> str:
    """Read task output file content, optionally tailing the last N lines.

    Returns empty string if file does not exist.
    """
    if not file_path.exists():
        return ""

    if tail_lines is not None and tail_lines > 0:
        return _tail_file(file_path, tail_lines)

    return file_path.read_text(encoding="utf-8", errors="replace")


def _tail_file(file_path: Path, n: int) -> str:
    """Read the last *n* lines from a file efficiently."""
    lines: deque[str] = deque(maxlen=n)
    with open(file_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            lines.append(line)
    return "".join(lines)


def truncate_output_file(file_path: Path, max_size: int = MAX_OUTPUT_FILE_SIZE) -> None:
    """Truncate an output file from the beginning if it exceeds *max_size*.

    Keeps the last *max_size* bytes.
    """
    if not file_path.exists():
        return
    size = file_path.stat().st_size
    if size <= max_size:
        return

    with open(file_path, "rb") as f:
        f.seek(size - max_size)
        # Advance to the next newline to avoid cutting mid-line
        f.readline()
        kept = f.read()

    with open(file_path, "wb") as f:
        f.write(kept)


def update_task_output_paths(
    db: ThreadSafeConnection,
    task_id: str,
    stdout_file: str,
    stderr_file: str,
) -> None:
    """Store output file paths in the background_tasks DB row."""
    db.execute(
        "UPDATE background_tasks SET stdout_path = ?, stderr_path = ? WHERE id = ?",
        (stdout_file, stderr_file, task_id),
    )
    db.commit()


def get_task_output_paths(db: ThreadSafeConnection, task_id: str) -> tuple[str | None, str | None]:
    """Retrieve stored output file paths for a task."""
    row = db.execute(
        "SELECT stdout_path, stderr_path FROM background_tasks WHERE id = ?",
        (task_id,),
    ).fetchone()
    if row is None:
        return None, None
    if hasattr(row, "keys"):
        return row["stdout_path"], row["stderr_path"]
    return row[0], row[1]


def preview_from_file(file_path: Path, lines: int = 5) -> str:
    """Extract the last few lines from a file as a preview string."""
    if not file_path.exists():
        return ""
    return _tail_file(file_path, lines).strip()


def purge_orphaned_task_output(
    data_dir: Path,
    db: ThreadSafeConnection,
    *,
    dry_run: bool = False,
) -> int:
    """Remove task_output directories whose conversation_id has no DB row.

    Returns the count of orphaned directories removed.
    """
    task_output_root = data_dir / "task_output"
    if not task_output_root.exists():
        return 0

    count = 0
    for entry in task_output_root.iterdir():
        if not entry.is_dir():
            continue
        if not _UUID_RE.match(entry.name):
            continue
        row = db.execute("SELECT 1 FROM conversations WHERE id = ?", (entry.name,)).fetchone()
        if row is None:
            if not dry_run:
                shutil.rmtree(entry)
            count += 1

    return count


def cleanup_conversation_task_output(data_dir: Path, conversation_id: str) -> None:
    """Remove all task output files for a conversation."""
    if not _UUID_RE.match(conversation_id):
        return
    out_dir = task_output_dir(data_dir, conversation_id)
    if out_dir.exists():
        shutil.rmtree(out_dir, ignore_errors=True)

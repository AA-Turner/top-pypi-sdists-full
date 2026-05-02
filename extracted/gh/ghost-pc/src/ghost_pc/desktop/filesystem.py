"""Safe filesystem operations for the GhostPC agent.

Provides directory listing, file search, and file reading with
configurable allowed directories to prevent unauthorized access.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Maximum file size to read (10 MB)
MAX_READ_SIZE = 10 * 1024 * 1024

# Default allowed directories (user's common folders)
DEFAULT_ALLOWED_DIRS: list[str] = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Pictures"),
    os.path.expanduser("~/Videos"),
    os.path.expanduser("~/Music"),
]


def _is_path_allowed(path: str, allowed_dirs: list[str] | None = None) -> bool:
    """Check if a path falls within allowed directories."""
    dirs = allowed_dirs or DEFAULT_ALLOWED_DIRS
    if not dirs:
        return True  # No restrictions

    resolved = os.path.realpath(path)
    return any(resolved.startswith(os.path.realpath(d)) for d in dirs)


def list_directory(
    path: str,
    allowed_dirs: list[str] | None = None,
) -> dict[str, object]:
    """List contents of a directory.

    Returns a dict with status, items list (name, type, size).
    """
    if not _is_path_allowed(path, allowed_dirs):
        return {"status": "error", "message": f"Access denied: {path}"}

    if not os.path.isdir(path):
        return {"status": "error", "message": f"Not a directory: {path}"}

    try:
        items = []
        for entry in sorted(os.scandir(path), key=lambda e: e.name.lower()):
            try:
                stat = entry.stat()
                items.append(
                    {
                        "name": entry.name,
                        "type": "dir" if entry.is_dir() else "file",
                        "size": stat.st_size if entry.is_file() else None,
                    }
                )
            except OSError:
                items.append({"name": entry.name, "type": "unknown", "size": None})

        return {"status": "ok", "path": path, "items": items, "count": len(items)}
    except PermissionError:
        return {"status": "error", "message": f"Permission denied: {path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def search_files(
    directory: str,
    pattern: str,
    allowed_dirs: list[str] | None = None,
    max_results: int = 50,
) -> dict[str, object]:
    """Search for files matching a glob pattern.

    Args:
        directory: Root directory to search.
        pattern: Glob pattern (e.g., "*.pdf", "report*").
        max_results: Maximum number of results to return.
    """
    if not _is_path_allowed(directory, allowed_dirs):
        return {"status": "error", "message": f"Access denied: {directory}"}

    if not os.path.isdir(directory):
        return {"status": "error", "message": f"Not a directory: {directory}"}

    try:
        results = []
        for match in Path(directory).rglob(pattern):
            if not _is_path_allowed(str(match), allowed_dirs):
                continue
            results.append(str(match))
            if len(results) >= max_results:
                break

        return {"status": "ok", "pattern": pattern, "results": results, "count": len(results)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def read_file(
    path: str,
    allowed_dirs: list[str] | None = None,
    max_size: int = MAX_READ_SIZE,
) -> dict[str, object]:
    """Read a text file's contents.

    Args:
        path: Path to the file.
        max_size: Maximum file size to read.
    """
    if not _is_path_allowed(path, allowed_dirs):
        return {"status": "error", "message": f"Access denied: {path}"}

    if not os.path.isfile(path):
        return {"status": "error", "message": f"File not found: {path}"}

    try:
        size = os.path.getsize(path)
        if size > max_size:
            return {
                "status": "error",
                "message": f"File too large: {size} bytes (max {max_size})",
            }

        with open(path, encoding="utf-8", errors="replace") as f:
            content = f.read()

        return {"status": "ok", "path": path, "size": size, "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_file_info(
    path: str,
    allowed_dirs: list[str] | None = None,
) -> dict[str, object]:
    """Get metadata about a file."""
    if not _is_path_allowed(path, allowed_dirs):
        return {"status": "error", "message": f"Access denied: {path}"}

    if not os.path.exists(path):
        return {"status": "error", "message": f"Not found: {path}"}

    try:
        stat = os.stat(path)
        return {
            "status": "ok",
            "path": path,
            "type": "dir" if os.path.isdir(path) else "file",
            "size": stat.st_size,
            "modified": stat.st_mtime,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

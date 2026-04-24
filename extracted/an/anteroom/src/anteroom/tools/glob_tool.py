"""File pattern matching tool using glob."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

from .path_utils import safe_resolve_pathlib
from .security import validate_path

_MAX_RESULTS = 500

_working_dir: str = os.getcwd()

DEFINITION: dict[str, Any] = {
    "name": "glob_files",
    "description": (
        "Find files and directories matching a glob pattern. "
        "Returns matching paths sorted by modification time (newest first)."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "pattern": {"type": "string", "description": 'Glob pattern (e.g. "**/*.py", "src/**/*.ts")'},
            "path": {
                "type": "string",
                "description": "Directory to search in. Defaults to working directory.",
            },
        },
        "required": ["pattern"],
    },
}


def set_working_dir(d: str) -> None:
    global _working_dir
    _working_dir = d


def _glob_matches(base: Path, pattern: str) -> tuple[list[str], bool]:
    matches = sorted(base.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    resolved_base = safe_resolve_pathlib(base)
    results: list[str] = []
    for match in matches[:_MAX_RESULTS]:
        if not match.is_file() and not match.is_dir():
            continue
        try:
            if not safe_resolve_pathlib(match).is_relative_to(resolved_base):
                continue
        except (OSError, ValueError):
            continue
        rel_path = str(match.relative_to(base))
        if match.is_dir():
            rel_path += "/"
        results.append(rel_path)
    return results, len(matches) > _MAX_RESULTS


async def handle(pattern: str, path: str | None = None, **_: Any) -> dict[str, Any]:
    if "\x00" in pattern:
        return {"error": "Pattern contains null bytes"}

    base_path = path or _working_dir
    resolved, error = validate_path(base_path, _working_dir)
    if error:
        return {"error": error}

    base = Path(resolved)
    if not base.is_dir():
        return {"error": "Directory not found"}

    try:
        results, truncated = await asyncio.to_thread(_glob_matches, base, pattern)
    except OSError:
        return {"error": "Search failed: unable to list directory contents"}

    return {"files": results, "count": len(results), "truncated": truncated}

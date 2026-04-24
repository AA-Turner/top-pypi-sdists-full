"""Read file contents tool."""

from __future__ import annotations

import asyncio
import os
from typing import Any

from .security import validate_path

_MAX_OUTPUT = 100_000

_working_dir: str = os.getcwd()

DEFINITION: dict[str, Any] = {
    "name": "read_file",
    "description": "Read the contents of a file. Returns numbered lines.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "File path (relative to working directory or absolute)"},
            "offset": {"type": "integer", "description": "Line number to start reading from (1-based). Optional."},
            "limit": {"type": "integer", "description": "Maximum number of lines to read. Optional."},
        },
        "required": ["path"],
    },
}


def set_working_dir(d: str) -> None:
    global _working_dir
    _working_dir = d


def _read_numbered_content(resolved: str, offset: int, limit: int | None) -> tuple[str, int, int]:
    with open(resolved, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    start = max(0, offset - 1)
    end = start + limit if limit else len(lines)
    selected = lines[start:end]

    numbered = []
    for i, line in enumerate(selected, start=start + 1):
        numbered.append(f"{i:>6}\t{line.rstrip()}")

    content = "\n".join(numbered)
    if len(content) > _MAX_OUTPUT:
        content = content[:_MAX_OUTPUT] + "\n... (truncated)"

    return content, len(lines), len(selected)


async def handle(path: str, offset: int = 1, limit: int | None = None, **_: Any) -> dict[str, Any]:
    resolved, error = validate_path(path, _working_dir)
    if error:
        return {"error": error}
    if not os.path.isfile(resolved):
        return {"error": f"File not found: {path}"}
    try:
        content, total_lines, lines_shown = await asyncio.to_thread(_read_numbered_content, resolved, offset, limit)
    except OSError:
        return {"error": "Unable to read file"}

    return {"content": content, "total_lines": total_lines, "lines_shown": lines_shown}

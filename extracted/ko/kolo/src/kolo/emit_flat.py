"""
Emit a trace into a single flat markdown file for easy preview.

This module uses the same emit logic as emit.py by emitting to a temp
directory, then walking the tree and assembling into a flat file.
This guarantees the output matches the normal emit exactly.
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from .emit import emit_trace
from .trace import Trace


def _header(level: int, text: str) -> str:
    """Generate a markdown header at the given level (1-6, clamped)."""
    level = max(1, min(6, level))
    return "#" * level + " " + text


def _walk_directory_depth_first(
    directory: Path,
    base_path: str,
    depth: int,
    lines: list[str],
) -> None:
    """
    Walk a directory depth-first and append content to lines.

    Args:
        directory: The directory to walk
        base_path: Path prefix for display (e.g., "0000_method/")
        depth: Current header depth (starting at 3)
        lines: Output lines to append to
    """
    entries = sorted(directory.iterdir(), key=lambda p: p.name)

    files = [e for e in entries if e.is_file()]
    dirs = [e for e in entries if e.is_dir()]

    for file_path in files:
        if depth == 3 and file_path.name == "README.txt":
            continue

        display_path = f"{base_path}{file_path.name}" if base_path else file_path.name
        lines.append(_header(depth, f"📄 {display_path}"))
        content = file_path.read_text()
        lines.append(content)
        lines.append("")

    for dir_path in dirs:
        display_path = (
            f"{base_path}{dir_path.name}/" if base_path else f"{dir_path.name}/"
        )
        lines.append(_header(depth, f"📁 {display_path}"))
        lines.append("")
        _walk_directory_depth_first(
            dir_path,
            display_path,
            depth + 1,
            lines,
        )


def emit_trace_flat(trace: Trace) -> str:
    """
    Emit a trace as a single flat markdown file.

    This uses the same emit logic as emit.py by:
    1. Emitting to a temp directory using emit_trace()
    2. Walking the directory tree depth-first
    3. Assembling everything into a flat markdown file

    Args:
        trace: The Trace object to emit

    Returns:
        The markdown content as a string
    """
    temp_dir = Path(tempfile.mkdtemp(prefix="kolo_emit_flat_"))
    try:
        trace_dir = emit_trace(trace, temp_dir)

        folder_name = trace_dir.name

        lines = []

        lines.append(_header(1, f"🔍 Kolo Trace: {folder_name}"))
        lines.append("")
        lines.append(f"**Trace ID:** `{trace.id}`")
        lines.append("")
        lines.append("---")
        lines.append("")

        overview_file = trace_dir / f"{trace.id}.txt"
        if overview_file.exists():
            lines.append(_header(2, f"📄 {trace.id}.txt"))
            lines.append(overview_file.read_text())
            lines.append("")
            lines.append("---")
            lines.append("")

        lines.append(_header(2, "📂 Trace Contents"))
        lines.append("")

        entries = sorted(trace_dir.iterdir(), key=lambda p: p.name)
        for entry in entries:
            if entry.name == f"{trace.id}.txt" or entry.name == "README.txt":
                continue

            if entry.is_dir():
                lines.append(_header(3, f"📁 {entry.name}/"))
                lines.append("")
                _walk_directory_depth_first(entry, f"{entry.name}/", 4, lines)
            elif entry.is_file():
                lines.append(_header(3, f"📄 {entry.name}"))
                lines.append(entry.read_text())
                lines.append("")

        content = "\n".join(lines)

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    return content

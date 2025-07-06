"""Provide utilities for regenerating Python code from flowchart nodes."""

from typing import List, Dict

def mesh_to_python(nodes: List[Dict]) -> str:
    """Regenerates code from flowchart nodes."""
    lines: List[str] = []
    for n in nodes:
        if n["type"] == "def":
            lines.append(n["raw"])
        elif n["type"] == "return":
            lines.append("    " + n["raw"])
    return "\n".join(lines)

"""Item #19 — Constitution prompt per project."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["Constitution", "load_constitution", "format_constitution_for_prompt"]


@dataclass
class Constitution:
    invariants: list[str] = field(default_factory=list)
    test_requirements: list[str] = field(default_factory=list)
    naming_rules: list[str] = field(default_factory=list)


_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_BULLET_RE = re.compile(r"^\s*[-*]\s+(.+?)\s*$", re.MULTILINE)


def _extract_section(text: str, heading_keyword: str) -> list[str]:
    """Extract bullet items under a heading whose name contains heading_keyword."""
    headings = list(_HEADING_RE.finditer(text))
    for i, h in enumerate(headings):
        if heading_keyword.lower() in h.group(1).lower():
            section_start = h.end()
            section_end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
            section = text[section_start:section_end]
            return [m.group(1) for m in _BULLET_RE.finditer(section)]
    return []


def load_constitution(project_root: Path) -> Constitution:
    p = project_root / "SAGE.md"
    if not p.exists():
        return Constitution()
    try:
        text = p.read_text("utf-8", errors="replace")
    except OSError:
        return Constitution()
    return Constitution(
        invariants=_extract_section(text, "invariants"),
        test_requirements=_extract_section(text, "test"),
        naming_rules=_extract_section(text, "naming"),
    )


def format_constitution_for_prompt(c: Constitution) -> str:
    if not (c.invariants or c.test_requirements or c.naming_rules):
        return ""
    parts: list[str] = ["## PROJECT CONSTITUTION (must follow)"]
    if c.invariants:
        parts.append("\n### Invariants")
        for inv in c.invariants:
            parts.append(f"  - {inv}")
    if c.test_requirements:
        parts.append("\n### Test requirements")
        for req in c.test_requirements:
            parts.append(f"  - {req}")
    if c.naming_rules:
        parts.append("\n### Naming rules")
        for rule in c.naming_rules:
            parts.append(f"  - {rule}")
    return "\n".join(parts)

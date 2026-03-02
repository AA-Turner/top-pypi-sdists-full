"""Specification schema - free-form markdown."""

from __future__ import annotations

from typing import Optional
from dataclasses import dataclass


@dataclass
class Spec:
    """A feature specification in markdown format."""

    title: str
    content: str  # Free-form markdown

    def to_markdown(self) -> str:
        """Return the spec as markdown."""
        return f"# {self.title}\n\n{self.content}"

    @classmethod
    def from_markdown(cls, markdown: str) -> "Spec":
        """Parse a markdown spec.

        Extracts title from first # heading, rest is content.
        """
        lines = markdown.strip().split("\n")
        title = "Untitled Spec"
        content_start = 0

        for i, line in enumerate(lines):
            if line.startswith("# "):
                title = line[2:].strip()
                content_start = i + 1
                break

        content = "\n".join(lines[content_start:]).strip()
        return cls(title=title, content=content)


# Template for suggested spec structure (shown in system prompt)
SPEC_TEMPLATE = """# Feature Title

> One-sentence summary

## Problem
What is broken or missing?

## Solution
What are we building?

## Implementation
- Step 1
- Step 2
- Step 3

## Related Files
- `path/to/file.py` - reason
- `path/to/other.py` - reason

## Edge Cases
- Case 1: expected behavior
- Case 2: expected behavior

## Open Questions
- Any unresolved questions?
"""

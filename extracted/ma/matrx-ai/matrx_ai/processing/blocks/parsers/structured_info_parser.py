"""Parser for the legacy ``structured_info`` markdown vocabulary.

This mirrors the frontend's legacy-text parser so server envelopes and the
client fallback parser agree during migration.
"""

from __future__ import annotations

import re

from matrx_ai.processing.blocks.models.structured_info import (
    StructuredInfoBlockData,
    StructuredInfoItem,
    StructuredInfoSection,
)

_HEADING = re.compile(r"^\*\*(.+?)\*\*$")
_BULLET = re.compile(r"^[*-]\s+(.+)$")
_BOLD_LABEL = re.compile(r"^\*\*(.+?):\*\*\s*(.*)$")
_PLAIN_LABEL = re.compile(r"^([^:]+):\s+(.+)$")


def _item(text: str) -> StructuredInfoItem:
    match = _BOLD_LABEL.match(text) or _PLAIN_LABEL.match(text)
    if match:
        return StructuredInfoItem(label=match.group(1).strip(), text=match.group(2).strip())
    return StructuredInfoItem(text=text.strip())


def parse_structured_info(content: str) -> StructuredInfoBlockData | None:
    lines = [line.strip() for line in content.splitlines()]
    if not any(_HEADING.match(line) for line in lines):
        return None

    title = "Structured Information"
    description: list[str] = []
    sections: list[StructuredInfoSection] = []
    current: StructuredInfoSection | None = None
    saw_title = False

    for line in lines:
        if not line:
            continue
        heading = _HEADING.match(line)
        if heading:
            text = heading.group(1).strip()
            if not saw_title:
                title = text
                saw_title = True
            else:
                current = StructuredInfoSection(heading=text)
                sections.append(current)
            continue

        bullet = _BULLET.match(line)
        if bullet and current is not None:
            current.items.append(_item(bullet.group(1)))
            continue

        if current is None:
            description.append(line)
        else:
            current.body = "\n".join(filter(None, [current.body, line])) or None

    return StructuredInfoBlockData(
        title=title,
        description="\n".join(description) or None,
        sections=sections,
    )

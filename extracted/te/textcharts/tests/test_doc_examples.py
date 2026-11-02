"""Validate that all JSON examples in docs/input-formats.md render without errors.

Extracts fenced JSON blocks from the doc and runs each through execute_command()
to verify they produce non-empty output.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from textcharts.commands import execute_command

DOCS_PATH = Path(__file__).resolve().parent.parent / "docs" / "input-formats.md"

# Chart types in document order — each JSON block maps to its preceding ## heading
_HEADING_RE = re.compile(r"^## (\w+)", re.MULTILINE)
_JSON_BLOCK_RE = re.compile(r"```json\n(.*?)```", re.DOTALL)


def _extract_examples() -> list[tuple[str, str]]:
    """Parse input-formats.md, returning (chart_type, json_string) pairs.

    Each ```json block is associated with the most recent ## heading above it.
    Skips blocks that appear after ## Common Options (not chart-specific).
    """
    text = DOCS_PATH.read_text()
    # Split into sections by ## headings
    sections: list[tuple[str, str]] = []
    headings = list(_HEADING_RE.finditer(text))

    for i, match in enumerate(headings):
        name = match.group(1).lower()
        start = match.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        section_text = text[start:end]
        sections.append((name, section_text))

    examples = []
    skip_sections = {"common"}
    for name, section_text in sections:
        if name in skip_sections:
            continue
        for block in _JSON_BLOCK_RE.finditer(section_text):
            examples.append((name, block.group(1).strip()))

    return examples


EXAMPLES = _extract_examples()


@pytest.mark.parametrize(
    "chart_type,json_str",
    EXAMPLES,
    ids=[f"{ct}" for ct, _ in EXAMPLES],
)
def test_doc_example_renders(chart_type: str, json_str: str) -> None:
    """Each JSON example from the docs should render a non-empty chart."""
    data = json.loads(json_str)
    result = execute_command(chart_type, data, options={"use_color": False})
    assert isinstance(result, str)
    assert len(result) > 0, f"{chart_type} example produced empty output"

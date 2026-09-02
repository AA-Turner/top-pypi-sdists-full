"""Decision block parser.

Parses the inner content of a <decision> block into structured data.

Mirrors the TypeScript parseDecisionFromContent() in:
    components/mardown-display/blocks/inline-decision/parseDecisionXml.ts

Expected LLM XML shape:
    <decision prompt="Select the project direction:">
      <option label="Aggressive">move forward aggressively.</option>
      <option label="Conservative">proceed carefully.</option>
    </decision>

The full opening tag is parsed separately by the detector; this parser
receives the inner content (between opening and closing tags) plus the
pre-parsed attributes dict.
"""

from __future__ import annotations

import re

from matrx_ai.processing.blocks.models.decision import DecisionBlockData, DecisionOption

_OPTION_RE = re.compile(r'<option\s+label="([^"]*)">([\s\S]*?)</option>', re.DOTALL)


def parse_decision(
    inner_content: str,
    attributes: dict[str, str],
    block_index: int = 0,
) -> DecisionBlockData | None:
    """
    Parse a decision block's inner content into structured data.

    Args:
        inner_content: Raw text between <decision ...> and </decision> tags.
        attributes: Pre-parsed tag attributes, e.g. {"prompt": "Select..."}.
        block_index: Line index used to produce a stable block id.

    Returns:
        DecisionBlockData if at least one option was found, else None.
    """
    options: list[DecisionOption] = []
    for idx, match in enumerate(_OPTION_RE.finditer(inner_content)):
        options.append(
            DecisionOption(
                id=f"opt-{idx}",
                label=match.group(1),
                text=match.group(2).strip(),
            )
        )

    if not options:
        return None

    return DecisionBlockData(
        id=f"decision-{block_index}",
        prompt=attributes.get("prompt", "Make a selection"),
        options=options,
    )


def parse_decision_from_raw_xml(full_xml: str, block_index: int = 0) -> DecisionBlockData | None:
    """
    Convenience wrapper that parses a complete <decision ...>...</decision> string.

    Handles both the opening tag attributes and inner content in one call.
    Mirrors parseDecisionXml() from parseDecisionXml.ts.
    """
    open_tag_match = re.match(r"^<decision\s+([^>]*)>", full_xml.lstrip())
    if not open_tag_match:
        return None

    attributes = _parse_xml_attributes(open_tag_match.group(1))
    closing_idx = full_xml.rfind("</decision>")
    if closing_idx == -1:
        return None

    open_end = full_xml.index(">") + 1
    inner_content = full_xml[open_end:closing_idx]
    return parse_decision(inner_content, attributes, block_index)


def _parse_xml_attributes(attr_string: str) -> dict[str, str]:
    """Extract key="value" pairs from an attribute string."""
    attrs: dict[str, str] = {}
    for match in re.finditer(r'(\w+)\s*=\s*"([^"]*)"', attr_string):
        attrs[match.group(1)] = match.group(2)
    return attrs

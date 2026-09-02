"""Decision tree parser.

Accepts both snake_case and camelCase field names from the LLM.

Expected LLM JSON shape:
    {
        "decision_tree": {
            "title": str,
            "description": str,       # optional
            "root": <Node>
        }
    }

Node shape:
    {
        "question": str,              # decision node (has yes/no)
        "action": str,                # leaf node
        "yes": <Node>,
        "no": <Node>,
        "priority": str,              # optional
        "category": str,              # optional
        "estimatedTime" | "estimated_time": str  # optional
    }
"""

from __future__ import annotations

import json
import re

from matrx_ai.processing.blocks.models.decision_tree import DecisionNode, DecisionTreeBlockData
from matrx_ai.processing.blocks.parsers._llm_json import loads_block_json

_CODE_BLOCK_RE = re.compile(r'```(?:json)?\s*([\s\S]*?)\s*```')


def _get(d: dict, *keys: str, default=None):
    """Return the first value found for any of the given key names."""
    for k in keys:
        if k in d:
            return d[k]
    return default


def parse_decision_tree(content: str) -> DecisionTreeBlockData | None:
    """Parse decision tree JSON into structured data."""
    try:
        json_content = content.strip()
        m = _CODE_BLOCK_RE.search(json_content)
        if m:
            json_content = m.group(1).strip()

        parsed = loads_block_json(json_content)
    except (json.JSONDecodeError, ValueError):
        return None

    if not isinstance(parsed, dict):
        return None

    # Accept both {"decision_tree": {...}} and the inner dict directly
    tree = parsed.get("decision_tree") or parsed

    if not isinstance(tree, dict):
        return None
    if not tree.get("title") or not tree.get("root"):
        return None

    try:
        root = _process_node(tree["root"], "root")
    except Exception:
        return None

    return DecisionTreeBlockData(
        title=tree["title"],
        description=tree.get("description"),
        root=root,
    )


def _process_node(data: dict, node_id: str) -> DecisionNode:
    """Recursively process a decision tree node."""
    if not isinstance(data, dict):
        raise ValueError(f"Node {node_id!r} is not a dict")

    node_type = "decision" if data.get("question") else "action"

    yes_node = None
    no_node = None
    if data.get("yes"):
        yes_node = _process_node(data["yes"], f"{node_id}-yes")
    if data.get("no"):
        no_node = _process_node(data["no"], f"{node_id}-no")

    return DecisionNode(
        id=node_id,
        question=data.get("question"),
        action=data.get("action"),
        type=node_type,
        yes=yes_node,
        no=no_node,
        priority=data.get("priority"),
        category=data.get("category"),
        estimated_time=_get(data, "estimatedTime", "estimated_time"),
    )

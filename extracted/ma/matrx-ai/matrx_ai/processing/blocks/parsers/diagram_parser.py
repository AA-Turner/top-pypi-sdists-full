"""Diagram parser.

Accepts both snake_case and camelCase field names from the LLM.

Expected LLM JSON shape:
    {
        "diagram": {
            "title": str,
            "description": str,                                # optional
            "type": "flowchart"|"mindmap"|"orgchart"|...,     # optional, default "flowchart"
            "nodes": [
                {
                    "id": str,
                    "label": str,
                    "type": str,                              # optional
                    "nodeType" | "node_type": str,           # optional
                    "description": str,                       # optional
                    "details": str,                           # optional
                    "position": {"x": float, "y": float}     # optional
                }
            ],
            "edges": [
                {
                    "id": str,                               # optional (auto-generated)
                    "source" | "from": str,
                    "target" | "to": str,
                    "label": str,                            # optional
                    "type": str,                             # optional
                    "color": str,                            # optional
                    "dashed": bool,                          # optional
                    "strokeWidth" | "stroke_width": float   # optional
                }
            ],
            "layout": {
                "direction": "TB"|"LR"|"BT"|"RL",           # optional
                "spacing": float                             # optional
            }
        }
    }
"""

from __future__ import annotations

import json
import logging
import math
import re

from matrx_ai.processing.blocks.models.diagram import (
    DiagramBlockData,
    DiagramEdge,
    DiagramLayout,
    DiagramNode,
    Position,
)

_CODE_BLOCK_RE = re.compile(r'```(?:json)?\s*([\s\S]*?)\s*```')

logger = logging.getLogger(__name__)
_logged_causes: set[str] = set()


def _log_once(cause: str, message: str) -> None:
    """Warn once per cause per process — loud, never spammy (envelope.py posture)."""
    if cause not in _logged_causes:
        _logged_causes.add(cause)
        logger.warning(message)


# Must mirror DiagramBlockData.type's Literal members exactly.
_KNOWN_DIAGRAM_TYPES = frozenset(
    {"flowchart", "mindmap", "orgchart", "network", "system", "process"}
)
from matrx_ai.processing.blocks.parsers._llm_json import loads_block_json


def _get(d: dict, *keys: str, default=None):
    """Return the first value found for any of the given key names."""
    for k in keys:
        if k in d:
            return d[k]
    return default


def parse_diagram(content: str) -> DiagramBlockData | None:
    """Parse diagram JSON into structured data."""
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

    # Accept both {"diagram": {...}} and the inner dict directly
    diagram = parsed.get("diagram") or parsed

    if not isinstance(diagram, dict):
        return None
    if not diagram.get("title") or not isinstance(diagram.get("nodes"), list):
        return None

    diagram_type = diagram.get("type", "flowchart")
    requested_type: str | None = None
    if diagram_type not in _KNOWN_DIAGRAM_TYPES:
        # LLMs emit free-form type strings ("architecture", "sequence", ...).
        # DiagramBlockData.type is a Literal, so an unknown string used to
        # raise ValidationError and silently finalize the block with
        # data=None. Degrade LOUDLY to the default renderer instead of losing
        # the whole diagram; the original string is preserved on
        # `requested_type` (envelope residue channel — zero data loss).
        _log_once(
            f"unknown-type:{diagram_type}",
            f"diagram parser: unknown diagram type '{diagram_type}' — not in "
            f"{sorted(_KNOWN_DIAGRAM_TYPES)}. Degrading to 'flowchart'; the "
            f"original type is preserved on requested_type. If this type is "
            f"legitimate, add it to DiagramBlockData.type and "
            f"_KNOWN_DIAGRAM_TYPES.",
        )
        requested_type = str(diagram_type)
        diagram_type = "flowchart"

    nodes: list[DiagramNode] = []
    for i, node in enumerate(diagram["nodes"]):
        if not isinstance(node, dict):
            continue
        if not node.get("id") or not node.get("label"):
            continue
        pos = node.get("position")
        position = (
            Position(x=pos["x"], y=pos["y"])
            if isinstance(pos, dict) and "x" in pos and "y" in pos
            else _default_position(i, diagram_type)
        )
        nodes.append(DiagramNode(
            id=node["id"],
            label=node["label"],
            type=node.get("type"),
            node_type=_get(node, "nodeType", "node_type") or node.get("type") or "default",
            description=node.get("description"),
            details=node.get("details"),
            position=position,
        ))

    edges: list[DiagramEdge] = []
    for i, edge in enumerate(diagram.get("edges", [])):
        if not isinstance(edge, dict):
            continue
        source = _get(edge, "source", "from")
        target = _get(edge, "target", "to")
        if not source or not target:
            continue
        edge_id = edge.get("id") or f"edge_{source}_to_{target}_{i}"
        edges.append(DiagramEdge(
            id=edge_id,
            source=source,
            target=target,
            label=edge.get("label"),
            type=edge.get("type", "default"),
            color=edge.get("color"),
            dashed=edge.get("dashed", False),
            stroke_width=_get(edge, "strokeWidth", "stroke_width") or 2,
        ))

    layout_data = diagram.get("layout") or {}
    layout = DiagramLayout(
        direction=layout_data.get("direction", "TB"),
        spacing=layout_data.get("spacing", 100),
    )

    return DiagramBlockData(
        title=diagram["title"],
        description=diagram.get("description"),
        type=diagram_type,
        requested_type=requested_type,
        nodes=nodes,
        edges=edges,
        layout=layout,
    )


def _default_position(index: int, diagram_type: str) -> Position:
    if diagram_type in ("flowchart", "process"):
        return Position(x=250, y=index * 120 + 50)
    elif diagram_type == "orgchart":
        level = index // 3
        pos = index % 3
        return Position(x=pos * 200 + 100, y=level * 150 + 50)
    elif diagram_type == "mindmap":
        angle = (index * 2 * math.pi) / 8
        radius = 200 + (index // 8) * 100
        return Position(x=300 + radius * math.cos(angle), y=300 + radius * math.sin(angle))
    elif diagram_type == "network":
        cols = 4
        row = index // cols
        col = index % cols
        return Position(x=col * 180 + 100 + (row % 2) * 90, y=row * 140 + 80)
    else:
        return Position(x=(index % 3) * 200 + 100, y=(index // 3) * 150 + 100)

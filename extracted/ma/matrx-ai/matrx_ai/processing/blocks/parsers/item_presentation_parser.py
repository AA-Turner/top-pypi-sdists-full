"""Parser for the ``item_presentation`` JSON block.

The detector promotes a ``{"item_presentation": {...}}`` object (fenced or
bare) to its own block type; this lifts the inner object into the registered
``item_presentation`` kind shape. Keys the kind does not declare are carried
under ``additional_details`` rather than dropped.
"""

from __future__ import annotations

import json
from typing import Any

from matrx_ai.processing.blocks.models.item_presentation import ItemPresentationBlockData
from matrx_ai.processing.blocks.parsers._llm_json import loads_block_json

_DECLARED = ("type", "id", "name", "about")


def parse_item_presentation(content: str) -> ItemPresentationBlockData | None:
    try:
        parsed = loads_block_json(content)
    except (json.JSONDecodeError, ValueError):
        return None

    if not isinstance(parsed, dict):
        return None
    inner = parsed.get("item_presentation")
    if not isinstance(inner, dict) or not isinstance(inner.get("type"), str):
        return None

    extra_source = inner.get("additionalDetails") or inner.get("additional_details")
    extra: dict[str, Any] = dict(extra_source) if isinstance(extra_source, dict) else {}
    for key, value in inner.items():
        if key in _DECLARED or key in ("additionalDetails", "additional_details"):
            continue
        extra[key] = value

    return ItemPresentationBlockData(
        type=inner["type"],
        id=inner.get("id"),
        name=inner.get("name"),
        about=inner.get("about"),
        additional_details=extra or None,
    )

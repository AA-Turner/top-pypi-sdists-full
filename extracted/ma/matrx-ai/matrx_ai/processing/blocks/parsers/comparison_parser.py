"""Comparison table parser.

Accepts both snake_case and camelCase field names from the LLM.

Expected LLM JSON shape:
    {
        "comparison": {
            "title": str,
            "description": str,        # optional
            "items": [str, ...],
            "criteria": [
                {
                    "name": str,
                    "values": [...],
                    "type": "cost"|"rating"|"text"|"boolean",   # optional
                    "weight": float,                             # optional
                    "higherIsBetter" | "higher_is_better": bool # optional
                }
            ]
        }
    }
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from matrx_ai.processing.blocks.models.comparison import ComparisonBlockData, ComparisonCriterion
from matrx_ai.processing.blocks.parsers._llm_json import loads_block_json

_CODE_BLOCK_RE = re.compile(r'```(?:json)?\s*([\s\S]*?)\s*```')

logger = logging.getLogger(__name__)
_logged_causes: set[str] = set()


def _log_once(cause: str, message: str) -> None:
    """Warn once per cause per process — loud, never spammy (envelope.py posture)."""
    if cause not in _logged_causes:
        _logged_causes.add(cause)
        logger.warning(message)


def _get(d: dict, *keys: str, default=None):
    """Return the first value found for any of the given key names."""
    for k in keys:
        if k in d:
            return d[k]
    return default


def parse_comparison(content: str) -> ComparisonBlockData | None:
    """Parse comparison JSON into structured data."""
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

    # Accept both {"comparison": {...}} and the inner dict directly
    comp = parsed.get("comparison") or parsed

    if not isinstance(comp, dict) or not comp.get("title"):
        return None

    items = comp.get("items", [])
    if not isinstance(items, list):
        return None

    criteria: list[ComparisonCriterion] = []
    for crit in comp.get("criteria", []):
        if not isinstance(crit, dict):
            continue
        values = crit.get("values", [])
        if isinstance(values, dict):
            # LLMs frequently emit values keyed by item name instead of an
            # ordered list. Normalize to the canonical ordered list (one value
            # per `items` entry) — this shape used to CRASH the parser and
            # silently finalize the block with data=None.
            #
            # Keys must match `items` exactly; a mismatch means empty cells
            # (missing keys) and/or dropped values (extra keys). Non-fatal —
            # exact-match traffic keeps working — but LOUD, never a silent
            # hollow block.
            item_keys = [str(item) for item in items]
            missing = [k for k in item_keys if k not in values]
            extra = [k for k in values if k not in item_keys]
            if missing or extra:
                _log_once(
                    f"values-key-mismatch:{comp.get('title')}:{crit.get('name')}",
                    f"comparison parser: criterion '{crit.get('name')}' has "
                    f"dict values whose keys do not match items exactly — "
                    f"missing={missing[:5]} (empty cells), extra={extra[:5]} "
                    f"(dropped). The block still renders; fix the emitting "
                    f"prompt/agent if this recurs.",
                )
            values = [values.get(key, "") for key in item_keys]
        if not isinstance(values, list):
            values = [values]
        crit_type = crit.get("type") or _infer_type(values)
        higher = _get(crit, "higherIsBetter", "higher_is_better")
        if higher is None:
            higher = _default_higher_is_better(crit_type)

        criteria.append(ComparisonCriterion(
            name=crit.get("name", ""),
            values=values,
            type=crit_type,
            weight=crit.get("weight"),
            higher_is_better=higher,
        ))

    return ComparisonBlockData(
        title=comp["title"],
        description=comp.get("description"),
        items=[str(i) for i in items],
        criteria=criteria,
    )


def _infer_type(values: list[Any]) -> str:
    if not isinstance(values, list) or not values:
        return "text"
    sample = values[0]
    if isinstance(sample, bool):
        return "boolean"
    if isinstance(sample, (int, float)):
        return "rating"
    if isinstance(sample, str):
        if re.match(r'^\$+$', sample):
            return "cost"
        try:
            float(sample.replace("$", "").replace(",", ""))
            return "cost"
        except ValueError:
            pass
    return "text"


def _default_higher_is_better(crit_type: str) -> bool:
    return crit_type != "cost"

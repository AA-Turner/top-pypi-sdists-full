"""The v1 variant condition grammar (the whole grammar).

``{"provider": [...], "model": [...], "latest": true, "reasoning": [...]}`` — every key present
must match (AND); a list matches any member (OR); ``{}`` never matches.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.prompt_blocks.models import ModelFacts

KEYS = ("provider", "model", "latest", "reasoning")


def _as_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)):
        return [str(v) for v in value]
    return []


def matches(condition: dict[str, Any] | None, facts: ModelFacts | None, reasoning: str | None) -> bool:
    if not isinstance(condition, dict):
        return False
    keys = [k for k in KEYS if k in condition]
    if not keys:
        return False
    for key in keys:
        value = condition[key]
        if key == "provider":
            wanted = {v.lower() for v in _as_list(value)}
            if not facts or not facts.provider or facts.provider.lower() not in wanted:
                return False
        elif key == "model":
            wanted = {v.lower() for v in _as_list(value)}
            have = {n.lower() for n in (facts.names if facts else frozenset())}
            if not wanted & have:
                return False
        elif key == "latest":
            if bool(value) != bool(facts and facts.latest):
                return False
        elif key == "reasoning":
            effort = (reasoning or "unset").lower()
            if effort not in {v.lower() for v in _as_list(value)}:
                return False
    return True

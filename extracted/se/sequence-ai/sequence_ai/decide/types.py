"""The decide (`/v1/decide`) wire type, as a plain dataclass. Field names are the wire names verbatim."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DecideResult:
    """
    One `/v1/decide` response. Field names are the wire names (schema.py DecideResponse).

    `answers` is keyed exactly as your questions were. Each value carries `["type"]` — noul,
    choice, or score — and the shape that goes with it: noul a `noul` probability; choice a
    `choice` plus a `probabilities` map and `confidence`; score a `score` plus a `legend`,
    `probabilities` and `confidence`. Branch on `answers[key]["type"]`, as the examples in
    `decide()` show; this layer passes them through rather than typing each.

    """

    id: str
    model: str
    answers: dict[str, Any]
    usage: dict[str, Any] = field(default_factory=dict)
    perf: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    cost_usd: float = 0.0

    def __repr__(self) -> str:
        return f"DecideResult({len(self.answers)} answer(s), {self.usage.get('input_tokens', '?')} in-tok)"

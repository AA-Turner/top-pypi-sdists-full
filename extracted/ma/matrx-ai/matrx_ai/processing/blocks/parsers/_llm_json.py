"""``loads_block_json`` — THE parse for a JSON-bodied block's content.

🚨 THE DEFECT THIS CLOSES (2026-08-22). Every JSON-bodied block parser called
bare ``json.loads``, so a model's answer had to be byte-perfect JSON to render
as its kind. It routinely is not: a live agent closed a 10-question quiz with a
TRAILING COMMA, ``json.loads`` refused it, the block was stamped ``parseError``
with no data, no ``__ir`` envelope could be built, and the reader — who had just
watched that quiz fill in question by question through the partial channel —
got a wall of raw JSON in the final frame instead of the quiz component
(run a488390e).

The partial channel survived the same document because ``close_partial_json``
truncates to a safe point before closing, which drops the dangling comma. So
the STREAM was more tolerant than the SETTLE, and the render collapsed at the
exact moment it should have locked in. One law, one tolerance: the final parse
now goes through the platform's canonical LLM-JSON funnel
(``matrx_ai.agents.response_parser.extract_json``, which already repairs
trailing commas and is pinned by its own tests) — the same funnel every other
LLM-output consumer uses. Never a tenth hand-rolled repair.

Tolerance is not laxity: ``extract_json`` returns a real value or nothing, and
each parser still applies its own structural validation on top. A document that
is genuinely wrong still fails, loudly, exactly as before.
"""

from __future__ import annotations

from typing import Any

__all__ = ["loads_block_json"]


def loads_block_json(content: str) -> Any:
    """Parse a block body written by a model. Returns None — never raises."""
    if not content or not content.strip():
        return None
    from matrx_ai.agents.response_parser import extract_json

    return extract_json(content)

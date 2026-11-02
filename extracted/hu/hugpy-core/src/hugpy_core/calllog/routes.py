"""calllog route registration: the central-pulls call surface.

The box-pull handlers (``pull_start`` / ``pull_finish``) live with the call-row
domain in ``call_record.py``; here they are grouped into a nested category tree
and registered with ``register_categories`` — the dict nesting encodes the path
(``llm`` -> ``central`` -> ``pulls`` -> handler)."""
from __future__ import annotations

from abstract_flask import get_bp, register_categories
from .call_record import pull_start, pull_finish

calllog_bp, logger = get_bp("calllog_bp", __name__)

ALL_CATEGORIES = {
    "llm": {
        "central": {
            "pulls": {
                "pull_start":  pull_start,   # -> /llm/central/pulls/pull_start
                "pull_finish": pull_finish,  # -> /llm/central/pulls/pull_finish
            },
        },
    },
}
register_categories(calllog_bp, ALL_CATEGORIES)

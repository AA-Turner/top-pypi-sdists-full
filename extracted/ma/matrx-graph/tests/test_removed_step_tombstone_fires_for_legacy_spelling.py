"""A deleted step's tombstone fires for the stored legacy ``action.`` spelling too.

Stored definitions keep the old ``action.<type>`` spelling and are never rewritten. The tombstone lookup
used the raw spelling, so ``action.ai.extract`` / ``action.ai.agent.tool_calling`` fell through to the
generic "unknown node type" message instead of naming the replacement.
"""

from __future__ import annotations

import pytest

from matrx_graph.validation import REMOVED_NODE_TYPES, validate_definition


def _definition(spec_type: str) -> dict:
    return {
        "nodes": [{"id": "n1", "type": "custom", "position": {"x": 0, "y": 0}, "data": {"spec_type": spec_type}}],
        "edges": [],
    }


@pytest.mark.parametrize("removed", ["ai.extract", "ai.agent.tool_calling", "ai.agent.react"])
@pytest.mark.parametrize("prefix", ["", "action."])
def test_tombstone_message_fires_for_both_spellings(removed: str, prefix: str) -> None:
    result = validate_definition(_definition(prefix + removed))
    messages = [i.message for i in result.issues if i.node_id == "n1"]
    assert REMOVED_NODE_TYPES[removed] in messages, messages

"""A failed tool call that a later call of the same turn recovers is a self-corrected slip.

Rule (agreed with the chat lane): superseded = a LATER successful call with the same tool name and
the same ``action`` and DIFFERENT arguments. The ledger decides (`claim_superseded`); the completion
event carries `supersedes`; the failed row carries `metadata.superseded_by`.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools.streaming import ToolStreamManager
from matrx_ai.tools.turn_ledger import (
    claim_superseded,
    get_turn_ledger,
    record_tool_outcome,
    record_tool_started,
    reset_turn_ledger,
    start_turn_ledger,
)


@pytest.fixture
def ledger():
    token = start_turn_ledger()
    yield
    reset_turn_ledger(token)


def _call(key: str, tool: str, args: dict, status: str) -> None:
    record_tool_started(key=key, tool_name=tool, arguments=args)
    record_tool_outcome(key=key, tool_name=tool, status=status, error_text="bad" if status == "error" else None)


def test_fail_then_corrected_success_is_marked(ledger):
    _call("c1", "table_rows", {"action": "update", "id": 1}, "error")
    record_tool_started(key="c2", tool_name="table_rows", arguments={"action": "update", "id": "1"})
    claimed = claim_superseded("c2")
    assert [e.key for e in claimed] == ["c1"]
    assert claimed[0].superseded_by == "c2"
    # claimed once only
    record_tool_started(key="c3", tool_name="table_rows", arguments={"action": "update", "id": "2"})
    assert claim_superseded("c3") == []


def test_success_of_a_different_tool_or_action_is_not_marked(ledger):
    _call("c1", "table_rows", {"action": "update", "id": 1}, "error")
    record_tool_started(key="c2", tool_name="other_tool", arguments={"action": "update", "id": 2})
    assert claim_superseded("c2") == []
    record_tool_started(key="c3", tool_name="table_rows", arguments={"action": "list"})
    assert claim_superseded("c3") == []
    record_tool_started(key="c4", tool_name="table_rows", arguments={"action": "update", "id": 1})
    assert claim_superseded("c4") == []  # identical arguments is a retry, not a correction


def test_fail_with_no_later_success_is_not_marked(ledger):
    _call("c1", "table_rows", {"action": "update", "id": 1}, "error")
    _call("c2", "table_rows", {"action": "update", "id": 2}, "error")
    # claim_superseded runs only as a call SUCCEEDS; a lone failure with no later success is never marked
    assert claim_superseded("c1") == []  # nothing earlier
    assert get_turn_ledger() is not None
    assert all(e.superseded_by is None for e in get_turn_ledger().entries)


class _Emitter:
    def __init__(self):
        self.sent = []

    async def send_tool_event(self, payload):
        self.sent.append(payload)


@pytest.mark.asyncio
async def test_completion_event_names_what_it_supersedes():
    emitter = _Emitter()
    stream = ToolStreamManager(emitter, "c2", "table_rows")
    await stream.completed("Done", result=None, supersedes=["c1"])
    assert emitter.sent[-1]["data"]["supersedes"] == ["c1"]
    await stream.completed("Done", result=None)
    assert emitter.sent[-1]["data"]["supersedes"] == []

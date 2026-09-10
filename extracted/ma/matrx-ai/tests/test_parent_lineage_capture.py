from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.db import conversation_gate as gate


@pytest.mark.asyncio
@pytest.mark.parametrize("lookup_fails", [False, True])
async def test_missing_lineage_is_captured_before_child_continues(monkeypatch, lookup_fails):
    captures = []

    async def lookup(**kwargs):
        if lookup_fails:
            raise RuntimeError("lookup unavailable")
        return []

    async def capture(exc, **kwargs):
        captures.append(kwargs)

    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(conversation=SimpleNamespace(filter_conversations=lookup)))
    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", capture)
    parent, child = str(uuid4()), str(uuid4())
    assert await gate.resolve_parent_conversation_lineage(parent, child) is None
    assert len(captures) == 1
    assert captures[0]["kind"] == "conversation_parent_lineage_unavailable"
    assert captures[0]["context"] == {
        "parent_conversation_id": parent,
        "child_conversation_id": child,
        "reason": "lookup_failed" if lookup_fails else "parent_missing",
    }

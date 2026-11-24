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


@pytest.mark.asyncio
async def test_a_workflow_steps_minted_invocation_parent_is_expected_not_an_incident(monkeypatch):
    """A system run inside a workflow step names the step's minted invocation id as
    parent; no row backs it, so the drop is expected and files nothing (2026-11-01:
    1,028 such rows each took a pool slot during the pool-saturation spike)."""
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    captures = []

    async def lookup(**kwargs):
        return []

    async def capture(exc, **kwargs):
        captures.append(kwargs)

    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(conversation=SimpleNamespace(filter_conversations=lookup)))
    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", capture)
    invocation_id = str(uuid4())
    step_ctx = AppContext(emitter=None, user_id=str(uuid4())).fork_for_workflow_step(invocation_id)
    token = set_app_context(step_ctx)
    try:
        assert await gate.resolve_parent_conversation_lineage(invocation_id, str(uuid4())) is None
        assert captures == []
        # Any OTHER missing parent inside the same step is still an incident.
        assert await gate.resolve_parent_conversation_lineage(str(uuid4()), str(uuid4())) is None
        assert len(captures) == 1
    finally:
        clear_app_context(token)

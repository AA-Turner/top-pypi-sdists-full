"""The content-gate verdict reaches its chat.tool_call row without bypassing the Coordinator.

Live 2026-11-03 (13:22Z-21:24Z): every verdict was a direct ``update_item_fields`` from a
detached task, filed by the ownership guard as COORDINATOR OWNERSHIP BYPASS, and it rewrote the
whole metadata object it had read earlier. A still-queued row now takes the verdict on its own
INSERT; a stored row gets one declared, atomic jsonb path write.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any

import pytest

from matrx_ai.tools import logger as tool_logger


def test_a_queued_row_carries_the_verdict_on_its_insert(monkeypatch: pytest.MonkeyPatch) -> None:
    key = tool_logger._call_row_key("conv-1", "call-1")
    assert key
    tool_logger._TOOL_CALL_ROW_BY_CALL_ID.set(key, "row-1")
    merged: list[tuple[str, str, Any]] = []

    def fake_merge(row_id: str, k: str, value: Any) -> bool:
        merged.append((row_id, k, value))
        return True

    def never(*_a: Any, **_k: Any) -> None:
        raise AssertionError("a queued row must not take a detached write")

    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.merge_into_queued_tool_call_metadata", fake_merge
    )
    monkeypatch.setattr("matrx_utils.detached_task", never)

    tool_logger.record_gate_verdict_on_row(
        call_id="call-1", conversation_id="conv-1", verdict={"action": "refused"}
    )

    assert merged == [("row-1", tool_logger.GATE_VERDICT_METADATA_KEY, {"action": "refused"})]


@pytest.mark.asyncio
async def test_a_stored_row_gets_one_declared_path_write(monkeypatch: pytest.MonkeyPatch) -> None:
    key = tool_logger._call_row_key("conv-2", "call-2")
    assert key
    tool_logger._TOOL_CALL_ROW_BY_CALL_ID.set(key, "row-2")
    declared: list[str] = []
    patched: list[tuple[Any, ...]] = []
    model = object()

    @contextmanager
    def fake_allow(m: Any, *, reason: str, acknowledgement: str):
        assert m is model
        declared.append(reason)
        yield

    class FakeToolCallManager:
        async def patch_jsonb_path(
            self, row_id: str, field: str, path: list[str], value: Any
        ) -> int:
            assert declared, "the write must run inside the declared bypass"
            patched.append((row_id, field, path, value))
            return 1

    class FakeCxm:
        tool_call = FakeToolCallManager()

    monkeypatch.setattr("matrx_orm.allow_direct_coordinator_write", fake_allow)
    monkeypatch.setattr("matrx_ai.persistence.queue_helpers._ensure_cx_registered", lambda: None)
    monkeypatch.setattr("matrx_ai.persistence.queue_helpers.get_model", lambda _t: model)
    monkeypatch.setattr(tool_logger, "_cxm", lambda: FakeCxm())

    await tool_logger._write_gate_verdict(
        call_id="call-2", conversation_id="conv-2", verdict={"action": "trimmed"}
    )

    assert patched == [
        ("row-2", "metadata", [tool_logger.GATE_VERDICT_METADATA_KEY], {"action": "trimmed"})
    ]
    assert len(declared) == 1

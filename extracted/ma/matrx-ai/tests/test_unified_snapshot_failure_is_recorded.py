"""A send's canonical snapshot (``unified_payload``) is never dropped silently.

Every send of conversation 5ae00046 from 2026-11-14 20:04 stored ``unified_payload`` NULL: the
executor caught a ``to_dict`` failure and set None with no record, so the cause was invisible and
the live typed-text guard lost the ledger it reads. The failure now goes through the durable
snapshot-capture seam, naming the error and the send.
"""

from __future__ import annotations

import asyncio
from typing import Any

from matrx_utils.source_guard import stable_source

from matrx_ai.orchestrator import executor


class _Broken:
    conversation_id = "conv-1"
    request_id = "req-1"

    def to_dict(self) -> dict[str, Any]:
        raise AttributeError("'dict' object has no attribute 'to_dict'")


class _Fine:
    def to_dict(self) -> dict[str, Any]:
        return {"config": {"messages": []}}


def test_a_to_dict_failure_is_recorded_and_the_send_goes_on(monkeypatch) -> None:
    seen: list[tuple[BaseException, dict[str, Any]]] = []

    async def record(exc: BaseException, context: dict[str, Any]) -> None:
        seen.append((exc, context))

    monkeypatch.setattr(executor, "_record_snapshot_capture_failure", record)
    out = asyncio.run(executor._unified_snapshot(_Broken(), iteration=5, path="success"))
    assert out is None
    assert len(seen) == 1
    exc, context = seen[0]
    assert isinstance(exc, AttributeError)
    assert context["path_kind"] == "unified_payload"
    assert context["conversation_id"] == "conv-1" and context["iteration"] == 5


def test_a_good_request_is_captured_without_a_record(monkeypatch) -> None:
    seen: list[Any] = []

    async def record(exc: BaseException, context: dict[str, Any]) -> None:
        seen.append(exc)

    monkeypatch.setattr(executor, "_record_snapshot_capture_failure", record)
    assert asyncio.run(executor._unified_snapshot(_Fine(), iteration=1, path="success")) == {"config": {"messages": []}}
    assert seen == []


def test_no_snapshot_site_swallows_to_dict_silently() -> None:

    source = stable_source(executor)
    assert "unified_snap = current_request.to_dict()" not in source

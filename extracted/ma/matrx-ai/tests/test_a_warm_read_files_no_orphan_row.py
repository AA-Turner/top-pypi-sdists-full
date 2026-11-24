"""A CACHE WARM IS NOT A SEND (live 2026-11-03/04, 9 orphan_tool_use_repaired rows from warm_fanout and /ai/warm).

A warm reads a conversation to fill a cache and can land mid-turn, while that turn's own tool call
(``records``) is still running: its tool_use is stored, its result is not. The sanitizer still repairs the
copy, but an in-flight call is not one the platform failed to answer, so nothing is screamed or filed.
Outside a warm the same repair stays loud.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.config import tool_result_guard as guard

REPAIRED = [{"tool_use_id": "toolu_1", "name": "records"}]


def _spy(monkeypatch: Any) -> list[dict[str, Any]]:
    captured: list[dict[str, Any]] = []
    monkeypatch.setattr(guard, "_schedule_orphan_capture", lambda **kw: captured.append(kw))
    return captured


def test_a_repair_during_a_warm_read_files_nothing(monkeypatch: Any) -> None:
    captured = _spy(monkeypatch)
    with guard.reading_for_warm():
        guard.report_orphan_tool_uses_repaired(layer="MessageList.sanitize", repaired=REPAIRED)
    assert captured == []


def test_the_same_repair_outside_a_warm_is_still_filed(monkeypatch: Any) -> None:
    captured = _spy(monkeypatch)
    with guard.reading_for_warm():
        pass
    guard.report_orphan_tool_uses_repaired(layer="MessageList.sanitize", repaired=REPAIRED)
    assert len(captured) == 1 and captured[0]["repaired"] == REPAIRED

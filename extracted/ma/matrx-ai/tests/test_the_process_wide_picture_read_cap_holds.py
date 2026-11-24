"""THE PROCESS-WIDE PICTURE READ CAP HOLDS ACROSS TURNS (CGU-10 AND-V IMG18, live guard for AND-IMG18 N4).

``ai.vision.media_pass_process_concurrency`` caps picture reads across every turn the process runs at once
(the per-turn knob alone lets N turns x 8 reads hit storage). The builder shipped it with no test: removing
``_process_media_pass_limit()`` from ``_bounded`` left every suite green. Three turns of six pictures at a
process cap of 2 must never have more than 2 reads in flight.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.providers import unified_client as uc


class _Messages:
    def __init__(self, messages: list[UnifiedMessage]) -> None:
        self._messages = messages

    def to_list(self) -> list[UnifiedMessage]:
        return self._messages


@pytest.mark.asyncio
async def test_reads_across_turns_never_pass_the_process_cap(monkeypatch) -> None:
    state = {"now": 0, "peak": 0}

    class _SlowFileManager:
        async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
            state["now"] += 1
            state["peak"] = max(state["peak"], state["now"])
            await asyncio.sleep(0.01)
            state["now"] -= 1
            ref.base64_data, ref.is_resolved = "QUJD", True
            return ref

    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _SlowFileManager())
    monkeypatch.setattr(uc, "MEDIA_PASS_PROCESS_CONCURRENCY_MIRROR", 2)
    monkeypatch.setattr(uc, "_PROCESS_LIMIT", None)

    def _turn(n: int) -> _Messages:
        pictures = [ImageContent(file_id=f"t{n}-p{i}", mime_type="image/jpeg", is_resolved=True) for i in range(6)]
        return _Messages([UnifiedMessage(role="user", content=pictures)])

    client = uc.UnifiedAIClient()
    await asyncio.gather(*(
        client._annotate_and_resolve_image_refs(
            _turn(n), model_name="claude-sonnet-5-5", wire_format="anthropic_chat", supports_vision=True,
        )
        for n in range(3)
    ))
    assert 1 <= state["peak"] <= 2, f"{state['peak']} picture reads in flight at a process cap of 2"


# ── CGU-10 AND-IMG19 F5: one turn never holds every server slot, and a throttled read never sleeps on a slot.


@pytest.mark.asyncio
async def test_one_turn_holds_at_most_its_share_of_the_server_cap(monkeypatch) -> None:
    state = {"now": 0, "peak": 0}

    class _SlowFileManager:
        async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
            state["now"] += 1
            state["peak"] = max(state["peak"], state["now"])
            await asyncio.sleep(0.01)
            state["now"] -= 1
            ref.base64_data, ref.is_resolved = "QUJD", True
            return ref

    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _SlowFileManager())
    monkeypatch.setattr(uc, "MEDIA_PASS_PROCESS_CONCURRENCY_MIRROR", 8)
    monkeypatch.setattr(uc, "MEDIA_PASS_CONCURRENCY_MIRROR", 8)  # the per-turn knob at the server cap
    monkeypatch.setattr(uc, "MEDIA_PASS_TURN_SHARE_MIRROR", 25)
    monkeypatch.setattr(uc, "_PROCESS_LIMIT", None)
    pictures = [ImageContent(file_id=f"p{i}", mime_type="image/jpeg", is_resolved=True) for i in range(8)]
    await uc.UnifiedAIClient()._annotate_and_resolve_image_refs(
        _Messages([UnifiedMessage(role="user", content=pictures)]),
        model_name="claude-sonnet-5-5", wire_format="anthropic_chat", supports_vision=True,
    )
    assert state["peak"] == 2, f"one turn held {state['peak']} of the server's 8 read slots (its share is 25%)"


@pytest.mark.asyncio
async def test_a_retry_backoff_does_not_hold_a_slot(monkeypatch) -> None:
    order: list[str] = []
    tries: dict[str, int] = {}

    class _FirstThrottled:
        async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
            fid = ref.file_id
            tries[fid] = tries.get(fid, 0) + 1
            order.append(f"{fid}#{tries[fid]}")
            if fid == "a" and tries[fid] == 1:
                ref.resolver_error = "storage_read_failed: SlowDown"
                return ref
            ref.base64_data, ref.is_resolved = "QUJD", True
            return ref

    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _FirstThrottled())
    monkeypatch.setattr(uc, "MEDIA_PASS_PROCESS_CONCURRENCY_MIRROR", 1)
    monkeypatch.setattr(uc, "_PROCESS_LIMIT", None)
    monkeypatch.setattr(uc, "_MEDIA_PASS_RETRY_BACKOFF_S", 0.05)
    pictures = [ImageContent(file_id=f, mime_type="image/jpeg", is_resolved=True) for f in ("a", "b")]
    await uc.UnifiedAIClient()._annotate_and_resolve_image_refs(
        _Messages([UnifiedMessage(role="user", content=pictures)]),
        model_name="claude-sonnet-5-5", wire_format="anthropic_chat", supports_vision=True,
    )
    assert order == ["a#1", "b#1", "a#2"], f"the only slot was held through a's retry sleep: {order}"

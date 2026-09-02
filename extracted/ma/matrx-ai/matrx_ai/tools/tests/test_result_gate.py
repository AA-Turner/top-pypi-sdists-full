"""Phase 1 — Layer-1 soft cap, canary, and the secure overflow cache."""

from __future__ import annotations

import pytest

from matrx_ai.tools import output_overflow
from matrx_ai.tools.output_caps import (
    TOOL_RESULT_CANARY_CHARS,
    TOOL_RESULT_SOFT_CAP_CHARS,
)
from matrx_ai.tools.result_gate import (
    ToolResultGateEvent,
    _SINKS,
    apply_size_gate,
    register_tool_result_gate_sink,
    tool_kind_label,
)


@pytest.fixture
def captured_events(monkeypatch):
    events: list[ToolResultGateEvent] = []
    register_tool_result_gate_sink(events.append)
    yield events
    # Remove our test sink so it doesn't leak into other tests.
    if events.append in _SINKS:
        _SINKS.remove(events.append)


def _content_dict(content, call_id="call-1", preview=None):
    return {
        "tool_use_id": call_id,
        "call_id": call_id,
        "name": "data",
        "content": content,
        "is_error": False,
        "output_chars": len(content) if isinstance(content, str) else 0,
        "output_preview": preview,
    }


def test_small_result_untouched_no_event(captured_events):
    cd = _content_dict("small result")
    out, truncated = apply_size_gate(
        cd,
        output_self_capped=False,
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
    )
    assert out["content"] == "small result"
    assert truncated is False
    assert captured_events == []


def test_canary_band_records_but_does_not_truncate(captured_events):
    body = "x" * (TOOL_RESULT_CANARY_CHARS + 100)
    cd = _content_dict(body)
    out, truncated = apply_size_gate(
        cd,
        output_self_capped=False,
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
    )
    assert out["content"] == body  # NOT truncated
    assert truncated is False
    assert len(captured_events) == 1
    assert captured_events[0].tier == "canary"
    assert captured_events[0].output_chars == len(body)


def test_over_soft_cap_truncates_stashes_and_alarms(captured_events):
    body = "y" * (TOOL_RESULT_SOFT_CAP_CHARS + 50_000)
    cd = _content_dict(body, call_id="call-big", preview={"chars": len(body)})
    out, truncated = apply_size_gate(
        cd,
        output_self_capped=False,
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-9",
        user_id="user-9",
    )
    # Truncated to head + notice; far smaller than the original.
    assert truncated is True
    assert len(out["content"]) < len(body)
    assert out["content"].startswith("y" * TOOL_RESULT_SOFT_CAP_CHARS)
    assert "fetch_tool_result" in out["content"]
    assert out["output_preview"]["size_gated"] is True
    # output_chars (what the model now sees) is lowered to the truncated size, while
    # the true pre-truncation size is preserved for display.
    assert out["output_chars"] == len(out["content"])
    assert out["output_preview"]["true_output_chars"] == len(body)
    assert len(captured_events) == 1
    assert captured_events[0].tier == "soft_fired"

    # The full payload was stashed and is retrievable by the same owner.
    sl = output_overflow.fetch_overflow(
        call_id="call-big",
        user_id="user-9",
        conversation_id="conv-9",
        offset=0,
        max_chars=10,
    )
    assert sl is not None
    assert sl.total_chars == len(body)
    assert sl.content == "y" * 10
    assert sl.has_more is True


def test_self_capped_is_trusted_even_when_huge(captured_events):
    body = "z" * (TOOL_RESULT_SOFT_CAP_CHARS + 100_000)
    cd = _content_dict(body)
    out, truncated = apply_size_gate(
        cd,
        output_self_capped=True,  # tool declared it managed itself
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
    )
    assert out["content"] == body  # untouched
    assert truncated is False
    assert captured_events == []  # no canary, no alarm


def test_media_block_list_never_truncated(captured_events):
    # Non-string content (typed image/audio blocks) must pass through untouched.
    blocks = [{"type": "image", "file_id": "f1"}]
    cd = _content_dict("placeholder")
    cd["content"] = blocks
    out, truncated = apply_size_gate(
        cd,
        output_self_capped=False,
        tool_name="screenshot",
        tool_kind="native",
        conversation_id="c",
        user_id="u",
    )
    assert out["content"] is blocks
    assert truncated is False
    assert captured_events == []


def test_overflow_fails_closed_on_owner_mismatch():
    output_overflow.stash_overflow(
        call_id="c-secure",
        content="secret-data" * 5000,
        total_chars=55_000,
        user_id="owner-A",
        conversation_id="conv-x",
        tool_name="data",
    )
    # Same call_id + conversation, DIFFERENT user → must not serve.
    leaked = output_overflow.fetch_overflow(
        call_id="c-secure",
        user_id="attacker-B",
        conversation_id="conv-x",
        offset=0,
        max_chars=100,
    )
    assert leaked is None
    # Correct owner still works.
    ok = output_overflow.fetch_overflow(
        call_id="c-secure",
        user_id="owner-A",
        conversation_id="conv-x",
        offset=0,
        max_chars=100,
    )
    assert ok is not None


def test_overflow_paging_offset_and_has_more():
    output_overflow.stash_overflow(
        call_id="c-page",
        content="abcdefghij",  # 10 chars
        total_chars=10,
        user_id="u",
        conversation_id="cv",
        tool_name="data",
    )
    first = output_overflow.fetch_overflow(
        call_id="c-page", user_id="u", conversation_id="cv", offset=0, max_chars=4
    )
    assert first.content == "abcd"
    assert first.next_offset == 4
    assert first.has_more is True
    last = output_overflow.fetch_overflow(
        call_id="c-page", user_id="u", conversation_id="cv", offset=8, max_chars=100
    )
    assert last.content == "ij"
    assert last.has_more is False
    assert last.next_offset is None


def test_tool_kind_label_mapping():
    from matrx_ai.tools.models import ToolType

    assert tool_kind_label(ToolType.LOCAL) == "native"
    assert tool_kind_label(ToolType.AGENT) == "agent"
    assert tool_kind_label(ToolType.EXTERNAL_MCP) == "external"
    assert tool_kind_label(ToolType.EXTERNAL_HANDLER) == "external"

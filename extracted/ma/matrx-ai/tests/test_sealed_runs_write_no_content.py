"""A confidential (sealed) run writes structure, never content — at the one write funnel."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.persistence import queue_helpers
from matrx_ai.persistence.sealed import (
    blanks_content,
    seal_payload,
    writes_sealed_structure,
)

CANARY = "CANARY-7f3a-never-on-our-server"
CONV = "11111111-1111-4111-8111-111111111111"


def _ctx(**kw: Any) -> SimpleNamespace:
    base = {"sealed_conversation_id": CONV, "sealed_keeps_content": False, "conversation_id": CONV}
    base.update(kw)
    return SimpleNamespace(**base)


def _contains_canary(value: Any) -> bool:
    return CANARY in repr(value)


@pytest.mark.parametrize(
    ("table", "payload"),
    [
        ("chat.conversation", {"id": CONV, "title": CANARY, "system_instruction": CANARY,
                               "description": CANARY, "keywords": [CANARY], "variables": {"v": CANARY},
                               "overrides": {"o": CANARY}, "config": {"model": "m", "messages": CANARY},
                               "metadata": {"run_configuration": CANARY}, "custom_fields": {"x": CANARY}}),
        ("chat.message", {"id": "m", "conversation_id": CONV, "role": "user", "position": 3,
                          "content": [{"type": "text", "text": CANARY}], "content_chars": 41,
                          "user_content": [CANARY], "model_context": {"c": CANARY},
                          "tools_on_call": [CANARY], "error": {"message": CANARY}, "voice": {"t": CANARY},
                          "metadata": {"editor_state": CANARY, "provider_iteration": 1},
                          "content_history": [CANARY]}),
        ("chat.tool_call", {"id": "t", "conversation_id": CONV, "tool_name": "web_search", "status": "completed",
                            "arguments": {"q": CANARY}, "output": CANARY, "output_preview": {"p": CANARY},
                            "execution_events": [CANARY], "file_path": f"/x/{CANARY}",
                            "error_message": CANARY, "metadata": {"content_ir": CANARY}, "duration_ms": 5}),
        ("chat.request", {"id": "r", "conversation_id": CONV, "cost": 0.1, "input_tokens": 9,
                          "tool_calls_details": [{"arguments": CANARY}], "trim_summary": {"s": CANARY},
                          "error": {"message": CANARY}, "metadata": {"pricing_snapshot": {"p": 1}, "x": CANARY}}),
        ("chat.user_request", {"id": "u", "error": CANARY, "total_cost": 0.1,
                               "metadata": {"turn_user_words": CANARY, "first_turn_results": CANARY,
                                            "usage_by_model": {"m": 1}}}),
    ],
)
@pytest.mark.parametrize("op_type", ["insert", "update"])
def test_no_content_column_survives_the_seal(table: str, payload: dict[str, Any], op_type: str) -> None:
    out = seal_payload(table, dict(payload), op_type=op_type, ctx=_ctx())
    assert out is not None
    assert not _contains_canary(out), f"{table} {op_type} kept content: {out}"


def test_structure_survives_the_seal() -> None:
    msg = seal_payload("chat.message", {"id": "m", "conversation_id": CONV, "role": "assistant", "position": 4,
                                        "status": "completed", "content": [{"text": "x"}], "content_chars": 1,
                                        "metadata": {"provider_iteration": 2}},
                       op_type="insert", ctx=_ctx())
    assert msg["role"] == "assistant" and msg["position"] == 4 and msg["content_chars"] == 1
    assert msg["content"] == [] and msg["metadata"] == {"provider_iteration": 2, "sealed": True}
    conv = seal_payload("chat.conversation", {"id": CONV, "config": {"model": "claude", "tools": ["a"]}},
                        op_type="insert", ctx=_ctx())
    assert conv["config"] == {"model": "claude"}
    assert conv["metadata"] == {"confidential": True}
    assert conv["is_ephemeral"] is False and conv["exclude_from_kg"] is True


@pytest.mark.parametrize("table", ["chat.request_snapshot", "chat.tool_trace", "chat.observational_memory"])
def test_content_derived_tables_are_dropped_whole(table: str) -> None:
    assert seal_payload(table, {"id": "x", "request_payload": CANARY}, op_type="insert", ctx=_ctx()) is None


def test_the_org_knob_keeps_content_but_still_marks_confidential() -> None:
    ctx = _ctx(sealed_keeps_content=True)
    assert not blanks_content(ctx)
    msg = seal_payload("chat.message", {"id": "m", "content": [CANARY]}, op_type="insert", ctx=ctx)
    assert _contains_canary(msg)
    conv = seal_payload("chat.conversation", {"id": CONV, "title": "t", "metadata": {"k": 1}},
                        op_type="insert", ctx=ctx)
    assert conv["metadata"] == {"k": 1, "confidential": True}


def test_an_unsealed_context_is_untouched() -> None:
    payload = {"id": "m", "content": [CANARY]}
    assert seal_payload("chat.message", payload, op_type="insert", ctx=SimpleNamespace()) is payload
    assert seal_payload("chat.message", payload, op_type="insert", ctx=None) is payload


def test_structure_writes_only_for_the_sealed_conversation() -> None:
    assert writes_sealed_structure(_ctx())
    assert not writes_sealed_structure(_ctx(conversation_id="22222222-2222-4222-8222-222222222222"))
    assert not writes_sealed_structure(SimpleNamespace(conversation_id=CONV))


def test_the_write_funnel_applies_the_seal(monkeypatch: pytest.MonkeyPatch) -> None:
    """The funnel (``_queue_or_drop``) — not each caller — empties the row."""
    queued: list[tuple[str, dict[str, Any]]] = []

    class _Coord:
        _owner_lane = None
        _late_boundary_captured = False

        def queue(self, table: str, payload: dict[str, Any], **_: Any) -> str:
            queued.append((table, payload))
            return "queued"

    monkeypatch.setattr(queue_helpers, "_resolve_app_context", lambda: _ctx(organization_id=None))
    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: _Coord())
    monkeypatch.setattr(queue_helpers, "conversation_organization", lambda _cid: "o")
    queue_helpers.queue_message_create(
        id="m", conversation_id=CONV, role="user", position=0, content=[{"type": "text", "text": CANARY}]
    )
    assert queued and not _contains_canary(queued[-1][1])
    assert queue_helpers.queue_request_snapshot_create(
        id="s", user_request_id="u", conversation_id=CONV, request_payload={"m": CANARY}
    ) == ""
    assert len(queued) == 1


def test_a_nested_metadata_object_keeps_only_its_named_structure() -> None:
    """mandate_run / run_configuration are never kept whole (review N1, 2026-10-22)."""
    conv = seal_payload(
        "chat.conversation",
        {"id": CONV, "metadata": {
            "mandate_run": {"door": "chat_start", "mandate_key": "k", "user_input": CANARY,
                            "result": {"envelope": {"a": CANARY}}, "placement": {"variables": [CANARY]},
                            "resolution": {"holder_id": "h", "note": CANARY}},
            "run_configuration": {"outputKinds": ["x"], "prompt": CANARY},
        }},
        op_type="update", ctx=_ctx(),
    )
    assert not _contains_canary(conv)
    assert conv["metadata"]["mandate_run"] == {"door": "chat_start", "mandate_key": "k",
                                               "resolution": {"holder_id": "h"}}
    assert conv["metadata"]["run_configuration"] == {"outputKinds": ["x"]}


@pytest.mark.parametrize(
    ("table", "metadata", "kept"),
    [
        ("chat.request", {"builtin_tool_use": {"web_search": {"count": 1, "queries": [CANARY]}},
                          "provider_attempts": [{"attempt": 1, "prompt": CANARY}]},
         {"builtin_tool_use": {"web_search": {"count": 1}}, "provider_attempts": [{"attempt": 1}], "sealed": True}),
        ("chat.user_request", {"usage_by_model": {"m": {"cost": 1, "note": CANARY}},
                               "mandate_attribution": {"why": CANARY}},
         {"usage_by_model": {"m": {"cost": 1}}, "sealed": True}),
        ("chat.message", {"prefill": {"mode": "x", "text": CANARY}}, {"prefill": {"mode": "x"}, "sealed": True}),
    ],
)
def test_no_object_is_ever_kept_whole(table: str, metadata: dict, kept: dict) -> None:
    """Every nested key is a NAMED structure subkey or dropped; a leaf holds no object."""
    out = seal_payload(table, {"id": "x", "conversation_id": CONV, "metadata": metadata}, op_type="update", ctx=_ctx())
    assert out["metadata"] == kept and not _contains_canary(out)

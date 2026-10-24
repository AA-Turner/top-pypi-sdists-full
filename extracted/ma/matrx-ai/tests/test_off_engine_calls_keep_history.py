"""Law — an AI call made OUTSIDE the engine loop keeps its history the one way.

Owner ruling (Arman, 2026-10-05): conversation + messages + cost row + exact
request snapshot, through the canonical funnel, for EVERY AI call. Three kinds
of call spend money without ``execute_ai_request``: a direct ``send_once`` (a
settings probe, a fix replay, a Hindsight wire replay), a provider batch result,
and a realtime socket session (Gemini Live / Lyria). They all record through
``matrx_ai.agents.run_history``.

These tests drive the REAL ``persist_completed_request`` (sections 1-4) with
only its queue sinks, the conversation gate and the snapshot writer doubled,
and assert what each kind of call leaves behind: the conversation is opened,
the person's input AND the model's answer become message rows, the request row
carries the provider usage, and the snapshot carries the exact wire body — with
audio as a blob block for the snapshot writer to save as a file, never inside a
message.
"""

from __future__ import annotations

import base64
from typing import Any

import pytest

from matrx_ai.config import TextContent, TokenUsage, UnifiedConfig, UnifiedMessage
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.orchestrator.requests import AIMatrixRequest

USER_ID = "22222222-2222-2222-2222-222222222222"
ORG_ID = "66666666-6666-6666-6666-666666666666"


class _StubModelManager:
    async def load_model_get_string_uuid(self, name):
        return "44444444-4444-4444-4444-444444444444"


class _StubCoordinator:
    def queue(self, *a, **k):
        return ""


class _AsyncAnything:
    def __getattr__(self, name):
        return _AsyncAnything()

    async def __call__(self, *a, **k):
        return []


@pytest.fixture()
def funnel(monkeypatch):
    """The real persist funnel; sinks, gate and snapshot writer captured."""
    from contextlib import asynccontextmanager

    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import (
        AppContext,
        clear_app_context,
        set_app_context,
    )

    import matrx_ai.db.conversation_gate as gate_mod
    import matrx_ai.db.persistence as persistence_mod
    import matrx_ai.orchestrator.executor as executor_mod
    import matrx_ai.persistence as persistence_pkg

    token = set_app_context(
        AppContext(
            emitter=ConsoleEmitter(),
            user_id=USER_ID,
            organization_id=ORG_ID,
            request_id="77777777-7777-7777-7777-777777777777",
            source_app="aidream",
            source_feature="ambient",
        )
    )
    calls: dict[str, list[Any]] = {
        "conversation_created": [],
        "user_request": [],
        "message_create": [],
        "message_update": [],
        "conversation_update": [],
        "request_create": [],
        "snapshot": [],
        "ctx": [],
    }

    async def _create_conv(conversation_id, user_id, *a, **k):
        from matrx_connect.context.app_context import get_app_context

        ctx = get_app_context()
        calls["ctx"].append(
            {"system_run": ctx.system_run, "source_feature": ctx.source_feature,
             "store": ctx.store, "organization_id": ctx.organization_id}
        )
        calls["conversation_created"].append(conversation_id)

    async def _ensure_ur(*, request_id, user_id, **k):
        calls["user_request"].append(request_id)

    async def _snapshot(**kw):
        calls["snapshot"].append(kw)

    @asynccontextmanager
    async def _coord(**_k):
        yield None

    monkeypatch.setattr(gate_mod, "create_new_conversation", _create_conv)
    monkeypatch.setattr(gate_mod, "ensure_user_request_exists", _ensure_ur)
    monkeypatch.setattr(executor_mod, "_write_request_snapshot", _snapshot)
    monkeypatch.setattr(persistence_pkg, "standalone_coordinator", _coord)
    monkeypatch.setattr(persistence_mod, "ai_model_manager_instance", _StubModelManager())
    monkeypatch.setattr(persistence_mod, "_get_coordinator", lambda: _StubCoordinator())
    monkeypatch.setattr(persistence_mod, "_get_live_coordinator", lambda: _StubCoordinator())

    def _msg_create(**kw):
        calls["message_create"].append(kw)

    monkeypatch.setattr(persistence_mod, "_queue_message_create", _msg_create)
    monkeypatch.setattr(
        persistence_mod, "_queue_message_update",
        lambda mid, **kw: calls["message_update"].append((mid, kw)),
    )
    monkeypatch.setattr(
        persistence_mod, "_queue_conversation_update",
        lambda cid, **kw: calls["conversation_update"].append((cid, kw)),
    )
    monkeypatch.setattr(
        persistence_mod, "_queue_request_create", lambda **kw: calls["request_create"].append(kw)
    )
    monkeypatch.setattr(persistence_mod, "_queue_user_request_update", lambda rid, **kw: None)

    async def _zero(*a, **k):
        return 0

    async def _none(*a, **k):
        return None

    monkeypatch.setattr(persistence_mod, "_hide_superseded_failed_turns", _zero)
    monkeypatch.setattr(persistence_mod, "_refresh_cache_state", _none)
    monkeypatch.setattr(persistence_mod, "_emit_context_state", _none)
    monkeypatch.setattr(persistence_mod, "cxm", _AsyncAnything())
    monkeypatch.setattr(persistence_mod, "try_get_tracker", lambda: None)
    monkeypatch.setattr(persistence_mod, "pinned_version_agent_id", _none)
    try:
        yield calls
    finally:
        clear_app_context(token)


def _text_of(row: dict[str, Any]) -> str:
    return "".join(
        str(block.get("text") or "") for block in row["content"] if isinstance(block, dict)
    )


@pytest.mark.asyncio
async def test_a_direct_send_once_call_keeps_conversation_messages_cost_and_snapshot(funnel):
    from matrx_ai.agents.run_history import record_sent_call

    request = AIMatrixRequest(
        conversation_id="11111111-1111-1111-1111-111111111111",
        config=UnifiedConfig(
            model="probe-model",
            messages=[UnifiedMessage(role="user", content=[TextContent(text="Reply OK.")])],
        ),
        request_id="33333333-3333-3333-3333-333333333333",
    )
    response = UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=[TextContent(text="OK")])],
        usage=TokenUsage(
            input_tokens=12, output_tokens=2, matrx_model_name="probe-model", api="openai"
        ),
        finish_reason="stop",
    )
    record = await record_sent_call(
        request,
        source_feature="ai_catalog.probe",
        response=response,
        wire_payload={"model": "probe-model", "max_tokens": 16},
    )

    assert record is not None, "the call's history was not kept"
    assert funnel["conversation_created"] == ["11111111-1111-1111-1111-111111111111"]
    assert funnel["ctx"][0]["system_run"] is True
    assert funnel["ctx"][0]["source_feature"] == "ai_catalog.probe"
    assert funnel["ctx"][0]["store"] is True
    roles = [m["role"] for m in funnel["message_create"]]
    assert roles == ["user", "assistant"], f"messages written: {roles}"
    assert _text_of(funnel["message_create"][1]) == "OK"
    assert len(funnel["request_create"]) == 1
    req_row = funnel["request_create"][0]
    assert req_row["input_tokens"] == 12 and req_row["output_tokens"] == 2
    snap = funnel["snapshot"][0]
    assert snap["request_payload"] == {"model": "probe-model", "max_tokens": 16}
    assert snap["unified_payload"]["config"]["model"] == "probe-model"
    assert snap["provider"] == "openai"


@pytest.mark.asyncio
async def test_a_refused_send_once_call_still_keeps_its_history(funnel):
    from matrx_ai.agents.run_history import record_sent_call

    request = AIMatrixRequest(
        conversation_id="11111111-1111-1111-1111-111111111112",
        config=UnifiedConfig(
            model="probe-model",
            messages=[UnifiedMessage(role="user", content=[TextContent(text="Reply OK.")])],
        ),
        request_id="33333333-3333-3333-3333-333333333334",
    )
    record = await record_sent_call(
        request,
        source_feature="hindsight/wire_replay",
        error=ValueError("temperature is not supported"),
        wire_payload={"temperature": 2},
    )
    assert record is not None
    # The refusal is a visible error turn after the person's turn (owner ruling 2026-10-23).
    assert [m["role"] for m in funnel["message_create"]] == ["user", "assistant"]
    assert funnel["message_create"][1]["status"] == "failed"
    assert funnel["message_create"][1]["is_visible_to_model"] is False
    assert funnel["snapshot"][0]["error_payload"]["outcome"] == "error"
    assert funnel["snapshot"][0]["request_payload"] == {"temperature": 2}


@pytest.mark.asyncio
async def test_a_failed_record_is_reported_never_silent(monkeypatch):
    """No actor on the context: the call cannot be kept — and says so."""
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import (
        AppContext,
        clear_app_context,
        set_app_context,
    )

    import matrx_ai.db.persistence as persistence_mod
    from matrx_ai.agents.run_history import record_sent_call

    token = set_app_context(AppContext(emitter=ConsoleEmitter(), user_id=""))
    reported: list[dict[str, Any]] = []

    async def _report(exc, **kw):
        reported.append({"exc": exc, **kw})

    monkeypatch.setattr(persistence_mod, "record_run_history_write_failure", _report)
    request = AIMatrixRequest(
        conversation_id="11111111-1111-1111-1111-111111111113",
        config=UnifiedConfig(
            model="m", messages=[UnifiedMessage(role="user", content=[TextContent(text="x")])]
        ),
        request_id="33333333-3333-3333-3333-333333333335",
    )
    try:
        result = await record_sent_call(
            request, source_feature="ai_catalog.probe", error=ValueError()
        )
    finally:
        clear_app_context(token)
    assert result is None
    assert len(reported) == 1
    assert reported[0]["stage"] == "record:sent_call:ai_catalog.probe"


@pytest.mark.asyncio
async def test_a_live_session_is_one_conversation_with_one_row_pair_per_turn(funnel):
    from matrx_ai.agents.run_history import RunConversation
    from matrx_ai.providers.google.live_history import LiveTurnCollector, live_usage

    collector = LiveTurnCollector()
    pcm = base64.b64encode(b"\x01\x02" * 400).decode()
    collector.observe_client({"type": "audio", "data": pcm, "mime_type": "audio/pcm;rate=16000"})
    turns = []
    for event in (
        {"server_content": {"input_transcription": {"text": "What's the weather"}}},
        {"server_content": {"model_turn": {"parts": [
            {"inline_data": {"data": pcm, "mime_type": "audio/pcm;rate=24000"}}]}}},
        {"server_content": {"output_transcription": {"text": "It is sunny."}}},
        {"server_content": {"turn_complete": True}},
        # Google reports the turn's usage just AFTER turn_complete.
        {"usage_metadata": {"prompt_token_count": 120, "response_token_count": 40,
                            "total_token_count": 160}},
        {"server_content": {"input_transcription": {"text": "Thanks"}}},
        {"server_content": {"output_transcription": {"text": "Any time."}},
         "usage_metadata": {"prompt_token_count": 170, "response_token_count": 8}},
        {"server_content": {"turn_complete": True}},
    ):
        turns.extend(collector.observe_provider(event))
    turns.extend(collector.drain())
    assert [t.user_text for t in turns] == ["What's the weather", "Thanks"]
    assert [t.output_text for t in turns] == ["It is sunny.", "Any time."]
    assert turns[0].usage_metadata["response_token_count"] == 40
    assert turns[0].input_audio and turns[0].output_audio, "the turn's audio was not kept"

    session = RunConversation(
        provider="google",
        model="gemini-live-test",
        source_feature="mandate:voice.gemini_live",
        system_instruction="You are a voice assistant.",
        session_config={"options": {"response_modalities": ["AUDIO"]}},
        conversation_id="11111111-1111-1111-1111-111111111199",
    )
    for turn in turns:
        await session.record(
            user_messages=[UnifiedMessage(role="user", content=[TextContent(text=turn.user_text)])],
            output_text=turn.output_text,
            usage=live_usage(turn.usage_metadata, model="gemini-live-test",
                             provider_model="gemini-live-test"),
            request_payload=turn.request_payload(session.session_config),
            response_payload=turn.response_payload(),
        )

    # ONE conversation, opened once; a person's session is not a system run.
    assert funnel["conversation_created"] == ["11111111-1111-1111-1111-111111111199"]
    assert funnel["ctx"][0]["system_run"] is False
    # Each turn writes ONLY its own two rows — the earlier turn is never re-INSERTed.
    texts = [(m["role"], _text_of(m)) for m in funnel["message_create"]]
    assert texts == [
        ("user", "What's the weather"), ("assistant", "It is sunny."),
        ("user", "Thanks"), ("assistant", "Any time."),
    ]
    # Audio never rides a message row.
    assert all(pcm not in str(m["content"]) for m in funnel["message_create"])
    # One cost row per turn, carrying the Live usage.
    assert [(r["input_tokens"], r["output_tokens"]) for r in funnel["request_create"]] == [
        (120, 40), (170, 8)
    ]
    # One snapshot per turn; the audio rides it as a blob block the snapshot
    # writer's redactor saves as a file.
    assert len(funnel["snapshot"]) == 2
    first = funnel["snapshot"][0]
    assert first["request_payload"]["input_audio"]["mime_type"] == "audio/pcm;rate=16000"
    assert first["error_payload"]["output_audio"]["data"]
    assert first["unified_payload"]["config"]["system_instruction"]


@pytest.mark.asyncio
async def test_a_stored_conversation_resumes_and_only_appends(funnel):
    """One HTTP request per exchange (a browser-held realtime session): the
    conversation is rebuilt from storage, never re-opened, and only the new
    exchange is written."""
    from matrx_ai.agents.run_history import RunConversation

    conv = "11111111-1111-1111-1111-111111111177"
    stored = [
        UnifiedMessage(role="user", content=[TextContent(text="Hello")]),
        UnifiedMessage(role="assistant", content=[TextContent(text="Hi there.")]),
    ]

    async def load(cid):
        assert cid == conv
        return stored

    session = await RunConversation.resume(
        conv, provider="xai", model="grok-voice-test",
        source_feature="voice-agent", load=load,
    )
    assert session.opened is True
    await session.record(
        user_messages=[UnifiedMessage(role="user", content=[TextContent(text="And now?")])],
        output_text="Now this.",
    )
    assert funnel["conversation_created"] == [], "a stored conversation was opened again"
    texts = [(m["role"], _text_of(m)) for m in funnel["message_create"]]
    assert texts == [("user", "And now?"), ("assistant", "Now this.")]

    async def empty(cid):
        return []

    fresh = await RunConversation.resume(
        "11111111-1111-1111-1111-111111111178", provider="xai",
        model="grok-voice-test", source_feature="voice-agent", load=empty,
    )
    assert fresh.opened is False
    await fresh.record(
        user_messages=[UnifiedMessage(role="user", content=[TextContent(text="First")])],
        output_text="Reply",
    )
    assert funnel["conversation_created"] == ["11111111-1111-1111-1111-111111111178"]


@pytest.mark.asyncio
async def test_realtime_audio_leaves_as_a_file_reference_never_inline(monkeypatch):
    import matrx_ai.providers.snapshot_redactors as redactors
    from matrx_ai.providers.google.live_history import LiveTurn, store_turn_audio

    saved: list[tuple[bytes, str]] = []

    async def _store(raw, mime, sha, **_k):
        saved.append((raw, mime))
        return "file-123"

    pcm = base64.b64encode(b"\x05\x06" * 64).decode()  # far below the redactor's size floor
    turn = LiveTurn(
        user_text="hi", output_text="hello", usage_metadata=None,
        input_audio={"data": pcm, "mime_type": "audio/pcm;rate=16000", "bytes": 128},
        output_audio=None,
    )
    monkeypatch.setattr(redactors, "_blob_store", _store)
    await store_turn_audio(turn, user_id=USER_ID, organization_id=ORG_ID)
    assert "data" not in turn.input_audio
    assert turn.input_audio["file_id"] == "file-123" and turn.input_audio["stored"] is True
    assert saved == [(b"\x05\x06" * 64, "audio/pcm;rate=16000")]

    turn.input_audio = {"data": pcm, "mime_type": "audio/pcm"}
    monkeypatch.setattr(redactors, "_blob_store", None)
    await store_turn_audio(turn, user_id=USER_ID, organization_id=ORG_ID)
    assert "data" not in turn.input_audio and turn.input_audio["stored"] is False

"""THE STATIC SEAL LINE — P0 guards (report only).

Plan: ``common-docs/systems/agents/agent-harness/projects/prompt-blocks-static-seal/PLAN.md`` §5.6 / §9 P0. The final outbound
snapshot fingerprints what actually left for the provider; a change ABOVE the line between two sends
of one conversation is reported once, a change below it never, and nothing here may ever touch,
delay or fail the send.
"""

from __future__ import annotations

import asyncio
import importlib
import json
import logging
import time
from typing import Any

import httpx
import pytest
from xai_sdk.proto import chat_pb2

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.send_boundary import order_for_wire, remember_cache_state, reset_loop_state
from matrx_ai.orchestrator.execution_state import (
    ExecutionState,
    clear_execution_state,
    set_execution_state,
)
from matrx_ai.providers import final_outbound_snapshot as fos
from matrx_ai.providers.outbound_capture import CallMeta, make_capture_http_client, set_call_meta
from matrx_ai.testing.profile_factory import make_profile


@pytest.fixture(autouse=True)
def _call_meta_never_leaks() -> Any:
    """Sync sends here stamp the provider call metadata (a ContextVar) on the test's own context;
    without this a later test in the same process inherits it (test_outbound_capture's fallback
    test read "anthropic" instead of "unknown")."""
    from matrx_ai.providers import outbound_capture

    token = outbound_capture._call_meta_var.set(None)
    yield
    outbound_capture._call_meta_var.reset(token)


@pytest.fixture(autouse=True)
def _seal_check_switched_on(monkeypatch):
    """These tests prove the check itself; production starts it off (knob seal_check_on = 0)."""
    from matrx_ai.providers import final_outbound_snapshot as _fos

    monkeypatch.setattr(_fos, "seal_check_on", lambda: True)


TYPED = "What should I post on Friday?"
MARK = "<live_date>It is now 09:00.</live_date>"
TEMPLATE = "Write the brief for this request:\n"
SYSTEM = "You are a careful assistant."
CONV = "11111111-2222-3333-4444-555555555555"

TRANSLATORS = [
    ("matrx_ai.providers.anthropic.translator", "AnthropicTranslator", "anthropic_chat"),
    ("matrx_ai.providers.openai.translator", "OpenAITranslator", "openai_responses"),
    ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
    ("matrx_ai.providers.cerebras.translator", "CerebrasTranslator", "cerebras_chat"),
    ("matrx_ai.providers.together.translator", "TogetherTranslator", "together_chat"),
    ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator", "openai_chat"),
    ("matrx_ai.providers.google.translator", "GoogleTranslator", "google_chat"),
    ("matrx_ai.providers.xai.translator", "XAITranslator", "xai_chat"),
]


@pytest.fixture(autouse=True)
def _clean() -> Any:
    fos.reset_for_tests()
    reset_loop_state(CONV)
    yield
    fos.reset_for_tests()
    reset_loop_state(CONV)


# ---------------------------------------------------------------------------
# The stamp: each translator marks the line in its own wire list
# ---------------------------------------------------------------------------


def _authored(role: str, text: str) -> UnifiedMessage:
    """A template message as the fill leaves it: stamped ``cache_template`` (``config/cache_marks.py``)."""
    message = UnifiedMessage(role=role, content=[TextContent(text=text)])
    message.metadata = {"cache_template": "stable"}
    return message


def _config(history: list[UnifiedMessage], *, typed: str | None) -> UnifiedConfig:
    config = UnifiedConfig(model="m", messages=MessageList(_messages=list(history)))
    config.system_instruction = SYSTEM
    if typed is not None:
        config.messages.append_or_extend_user_input(typed)
    config.messages.attach_turn_context(MARK, slot="live_date")
    return config


def _build(module: str, cls: str, wire_format: str, config: UnifiedConfig) -> Any:
    profile = make_profile(model_name="m", wire_format=wire_format)
    prep = order_for_wire(config, profile)
    translator = getattr(importlib.import_module(module), cls)()
    return translator.build_request(prep.wire_config if prep.wire_config is not None else config, profile)


def _texts(item: Any) -> list[str]:
    if hasattr(item, "SerializeToString"):
        return [c.text for c in getattr(item, "content", [])]
    content = item.get("content", item.get("parts"))
    if isinstance(content, str):
        return [content]
    return [p.get("text") or "" for p in content or [] if isinstance(p, dict)]


def _above_text(cls: str, request: Any, stamp: fos.SealStamp) -> str:
    key = {"OpenAITranslator": "input", "GoogleTranslator": "contents"}.get(cls, "messages")
    items = list(request[key])
    out: list[str] = []
    for item in items[: stamp.message_index]:
        out.extend(_texts(item))
    if stamp.block_index:
        out.extend(_texts(items[stamp.message_index])[: stamp.block_index])
    return "\n".join(out)


@pytest.mark.parametrize(("module", "cls", "wire_format"), TRANSLATORS)
def test_typed_text_the_template_text_is_above_the_line(module: str, cls: str, wire_format: str) -> None:
    template = _authored("user", TEMPLATE)
    request = _build(module, cls, wire_format, _config([template], typed=TYPED))
    stamp = fos.current_seal_stamp()
    assert stamp is not None, f"{cls}: no seal stamped"
    above = _above_text(cls, request, stamp)
    assert TEMPLATE.strip() in above, f"{cls}: authored template text is not above the line ({stamp})"
    assert MARK not in above and TYPED not in above, f"{cls}: per-turn block or typed text above the line"


@pytest.mark.parametrize(("module", "cls", "wire_format"), TRANSLATORS)
def test_nothing_typed_the_final_template_message_is_below_the_line(module: str, cls: str, wire_format: str) -> None:
    template = _authored("user", TEMPLATE)
    request = _build(module, cls, wire_format, _config([template], typed=None))
    stamp = fos.current_seal_stamp()
    assert stamp is not None
    above = _above_text(cls, request, stamp)
    assert TEMPLATE.strip() not in above and MARK not in above, f"{cls}: {stamp} {above!r}"


def test_anthropic_merged_turn_stamps_a_block_index() -> None:
    """Anthropic merges template + per-turn block + typed text into ONE wire message: the line is
    INSIDE it, (message index, content-block index)."""
    template = _authored("user", TEMPLATE)
    request = _build(*TRANSLATORS[0], _config([template], typed=TYPED))
    stamp = fos.current_seal_stamp()
    assert stamp is not None and stamp.block_index == 1 and stamp.message_index == len(request["messages"]) - 1


# ---------------------------------------------------------------------------
# One segment parser per wire shape
# ---------------------------------------------------------------------------


def test_parser_anthropic_messages() -> None:
    body = {
        "tools": [{"name": "t", "cache_control": {"type": "ephemeral", "ttl": "5m"}}],
        "system": [{"type": "text", "text": "S", "cache_control": {"type": "ephemeral"}}],
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": "a"}]},
            {"role": "user", "content": [{"type": "text", "text": "head"}, {"type": "text", "text": "ctx"}]},
        ],
    }
    labels = [s.label for s in fos.segments_anthropic(body, fos.SealStamp(fos.SHAPE_ANTHROPIC, 1, 1))]
    assert labels == ["tools", "system", "message 0", "message 1 blocks 0..0"]


def test_parser_openai_responses() -> None:
    body = {"instructions": "S", "tools": [], "input": [{"role": "developer", "content": "S"}, {"role": "user"}], "prompt_cache_key": "k"}
    labels = [s.label for s in fos.segments_responses(body, fos.SealStamp(fos.SHAPE_RESPONSES, 1))]
    assert labels == ["tools", "system", "message 0"]


def test_parser_chat_completions() -> None:
    body = {"messages": [{"role": "system", "content": "S"}, {"role": "user", "content": "x"}], "stream": True}
    labels = [s.label for s in fos.segments_chat(body, fos.SealStamp(fos.SHAPE_CHAT, 1))]
    assert labels == ["message 0"]


def test_parser_google_generate_content() -> None:
    body = {"systemInstruction": {"parts": [{"text": "S"}]}, "contents": [{"role": "user", "parts": [{"text": "a"}, {"text": "b"}]}]}
    labels = [s.label for s in fos.segments_google(body, fos.SealStamp(fos.SHAPE_GOOGLE, 0, 1))]
    assert labels == ["system", "message 0 blocks 0..0"]


def test_parser_xai_proto() -> None:
    request = chat_pb2.GetCompletionsRequest(model="m")
    request.messages.add(role=chat_pb2.MessageRole.ROLE_SYSTEM).content.add(text="S")
    user = request.messages.add(role=chat_pb2.MessageRole.ROLE_USER)
    user.content.add(text="head")
    user.content.add(text="ctx")
    segs = fos.segments_xai(request, fos.SealStamp(fos.SHAPE_XAI, 1, 1))
    assert [s.label for s in segs] == ["message 0", "message 1 blocks 0..0"]
    request.messages[1].content[1].text = "changed below"
    assert [s.sha for s in fos.segments_xai(request, fos.SealStamp(fos.SHAPE_XAI, 1, 1))] == [s.sha for s in segs]


def test_non_chat_urls_are_never_parsed() -> None:
    assert fos.shape_of_url("https://api.openai.com/v1/files") is None
    assert fos.shape_of_url("https://api.anthropic.com/v1/messages/batches") is None
    assert fos.shape_of_url("https://api.anthropic.com/v1/messages/count_tokens") is None
    assert fos.shape_of_url("https://api.anthropic.com/v1/messages") == fos.SHAPE_ANTHROPIC


# ---------------------------------------------------------------------------
# The check — on real serialized bodies, through the observer
# ---------------------------------------------------------------------------


def _body(*, system: str = SYSTEM, template: str = TEMPLATE, below: str = MARK, ttl: str = "5m") -> bytes:
    return json.dumps(
        {
            "model": "m",
            "tools": [{"name": "lookup", "input_schema": {"type": "object"}}],
            "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral", "ttl": ttl}}],
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": template}, {"type": "text", "text": below}, {"type": "text", "text": TYPED}]}
            ],
            "stream": True,
        }
    ).encode()


class _Ctx:
    conversation_id = CONV
    request_id = "req-1"
    agent_id = "agent-1"
    ai_watch = False
    emitter = None
    store = True
    system_run = False

    def __init__(self) -> None:
        self.metadata: dict[str, Any] = {}


@pytest.fixture
def send(monkeypatch: pytest.MonkeyPatch) -> Any:
    """One observed send: the stamp a translator leaves, the call meta, the loop's state."""
    ctx = _Ctx()
    monkeypatch.setattr("matrx_connect.context.app_context.try_get_app_context", lambda: ctx)
    token = set_execution_state(ExecutionState())

    def _send(
        body: bytes, *, request_id: str = "req-1", model: str = "m", stamp: tuple[int, int | None] = (0, 1)
    ) -> fos.FinalOutboundSnapshot | None:
        ctx.request_id = request_id
        set_call_meta(CallMeta(provider="anthropic", model=model))
        fos.stamp_seal(fos.SealStamp(fos.SHAPE_ANTHROPIC, *stamp))
        return fos.observe_wire_body(url="https://api.anthropic.com/v1/messages", body=body)

    _send.ctx = ctx  # type: ignore[attr-defined]
    yield _send
    clear_execution_state(token)


def _breaks(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [r.getMessage() for r in caplog.records if "static_seal_broken" in r.getMessage()]


def test_identical_sends_report_nothing(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING)
    send(_body())
    send(_body(), request_id="req-2")
    assert _breaks(caplog) == []


def test_change_above_the_line_is_reported_once_naming_the_segment(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING)
    send(_body())
    send(_body(system=SYSTEM + " Today is Tuesday."), request_id="req-2")
    send(_body(system=SYSTEM + " Today is Wednesday."), request_id="req-3")  # same segment, same window
    breaks = _breaks(caplog)
    assert len(breaks) == 1, breaks
    assert "'system'" in breaks[0] and "req-1" in breaks[0] and "req-2" in breaks[0]


def test_change_in_the_seal_message_head_names_its_blocks(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING)
    send(_body())
    send(_body(template="Write the plan for this request:\n"), request_id="req-2")
    breaks = _breaks(caplog)
    assert len(breaks) == 1 and "'message 0 blocks 0..0'" in breaks[0]


def test_change_below_the_line_is_never_reported(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING)
    send(_body())
    send(_body(below="<live_date>It is now 09:05.</live_date>"), request_id="req-2")
    assert _breaks(caplog) == []


def test_no_prior_record_no_check(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING)
    send(_body(system="anything"))
    assert _breaks(caplog) == []


def test_cache_mark_ttl_only_change_is_not_a_break(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING)
    send(_body(ttl="5m"))
    send(_body(ttl="1h"), request_id="req-2")
    assert _breaks(caplog) == []


def test_previous_send_older_than_the_window_is_not_compared(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING)
    send(_body())
    for entries in fos._LATEST.values():
        for record in entries.values():
            record["at"] = time.time() - fos.seal_window_seconds() - 5
    send(_body(system="changed"), request_id="req-2")
    assert _breaks(caplog) == []


def test_a_model_switch_is_a_new_baseline(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING)
    send(_body())
    send(_body(system="changed"), request_id="req-2", model="other")
    assert _breaks(caplog) == []


def test_turn_two_reads_the_record_back_from_cache_state(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    """Cache-miss reload: another process (no memory) gets the record through ``cache_state`` —
    hashes, lengths and a bounded few chunk digests from each end (never the text) — and still
    reports the break, located."""
    caplog.set_level(logging.WARNING)
    send(_body())
    persisted = {fos.SEAL_STATE_KEY: fos.merged_seal_state(None, fos.take_seal_records(CONV))}
    entry = next(v for k, v in persisted[fos.SEAL_STATE_KEY].items() if k != fos.POSITION_KEY)
    assert entry["seal"] == [0, 1] and all(len(s) == 5 for s in entry["segments"])
    assert all(
        len(s[3]) <= fos._PERSISTED_HEAD_CHUNKS and len(s[4]) <= fos._PERSISTED_TAIL_CHUNKS for s in entry["segments"]
    )  # bounded chunk digests
    assert "text" not in json.dumps(persisted).lower().replace("type", "")  # hashes only, never the prompt
    with fos._LOCK:
        fos._LATEST.clear()
    remember_cache_state(CONV, persisted)
    send(_body(system="changed"), request_id="req-2")
    breaks = _breaks(caplog)
    assert len(breaks) == 1 and "'system'" in breaks[0] and "first difference at byte 0" in breaks[0]
    taken = fos.take_seal_records(CONV)
    assert taken and next(iter(taken.values()))["breaks"][0]["divergence_offset"] == 0


def test_turn_two_cache_hit_in_process_memory(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING)
    send(_body())
    send(_body(below="next turn's block"), request_id="req-2")
    assert _breaks(caplog) == []
    send(_body(template="edited template", below="third"), request_id="req-3")
    assert len(_breaks(caplog)) == 1


# ---------------------------------------------------------------------------
# Never breaks a send
# ---------------------------------------------------------------------------


def test_an_exception_in_the_check_does_not_fail_the_send(send: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_a: Any, **_k: Any) -> Any:
        raise RuntimeError("seal check exploded")

    monkeypatch.setattr(fos, "check_and_remember", boom)
    assert send(_body()) is None  # said once, swallowed


def test_hook_raises_send_proceeds(monkeypatch: pytest.MonkeyPatch) -> None:
    """The observer itself raising inside httpx's request hook: the request still goes out."""

    def boom(**_k: Any) -> Any:
        raise RuntimeError("observer exploded")

    monkeypatch.setattr(fos, "observe_wire_body", boom)
    fos.stamp_seal(fos.SealStamp(fos.SHAPE_ANTHROPIC, 0, None))
    seen: list[bytes] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.content)
        return httpx.Response(200, json={"ok": True})

    async def run() -> int:
        client = make_capture_http_client(transport=httpx.MockTransport(handler))
        async with client:
            response = await client.post("https://api.anthropic.com/v1/messages", content=_body())
            return response.status_code

    assert asyncio.run(run()) == 200
    assert seen == [_body()]  # not a byte changed


def test_bodies_above_the_parse_limit_are_hashed_not_parsed(send: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fos, "seal_parse_max_bytes", lambda: 10)
    snapshot = send(_body())
    assert snapshot is not None and snapshot.parsed is False and snapshot.segments == () and snapshot.body_sha256


def test_xai_proto_send_is_checked(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    """xAI chat (gRPC): the observer reads the request proto the stub sends (``chat._proto``)."""
    caplog.set_level(logging.WARNING)

    class _Chat:
        def __init__(self, system_text: str) -> None:
            self._proto = chat_pb2.GetCompletionsRequest(model="m")
            self._proto.messages.add(role=chat_pb2.MessageRole.ROLE_SYSTEM).content.add(text=system_text)
            self._proto.messages.add(role=chat_pb2.MessageRole.ROLE_USER).content.add(text=TYPED)

    def _xai(system_text: str, request_id: str) -> fos.FinalOutboundSnapshot | None:
        set_call_meta(CallMeta(provider="xai", model="m"))
        fos.stamp_seal(fos.SealStamp(fos.SHAPE_XAI, 1, None))
        _Ctx.request_id = request_id
        return fos.observe_xai_request(_Chat(system_text))

    send(_body())  # binds the context and loop state
    first = _xai(SYSTEM, "x-1")
    assert first is not None and first.fidelity == "proto"
    _xai(SYSTEM, "x-2")
    assert _breaks(caplog) == []
    _xai(SYSTEM + " now", "x-3")
    breaks = _breaks(caplog)
    assert len(breaks) == 1 and "'message 0'" in breaks[0]



# ---------------------------------------------------------------------------
# Real translators across turns: the line is the conversation's, fixed at assembly
# ---------------------------------------------------------------------------

URLS = {
    "anthropic_chat": ("anthropic", "https://api.anthropic.com/v1/messages"),
    "openai_responses": ("openai", "https://api.openai.com/v1/responses"),
}
REAL = [TRANSLATORS[0], TRANSLATORS[1]]


def _turn(history: list[UnifiedMessage], typed: str, *, template: str = TEMPLATE) -> UnifiedConfig:
    head = [_authored("user", template), _authored("assistant", "Understood.")]
    return _config([*head, *history], typed=typed)


def _translated_send(send: Any, module: str, cls: str, wire_format: str, config: UnifiedConfig, **kw: Any) -> Any:
    provider, url = URLS[wire_format]
    request = _build(module, cls, wire_format, config)
    stamp = fos.current_seal_stamp()
    set_call_meta(CallMeta(provider=provider, model=kw.get("model", "m")))
    send.ctx.request_id = kw.get("request_id", "req-1")
    snapshot = fos.observe_wire_body(url=url, body=json.dumps(request, default=str).encode())
    return stamp, snapshot


def _t1_history() -> list[UnifiedMessage]:
    return [
        UnifiedMessage(role="user", content=[TextContent(text="first question")]),
        UnifiedMessage(role="assistant", content=[TextContent(text="first answer")]),
    ]


@pytest.mark.parametrize(("module", "cls", "wire_format"), REAL)
def test_turn_two_through_the_translator_keeps_the_assembly_line(
    send: Any, caplog: pytest.LogCaptureFixture, module: str, cls: str, wire_format: str
) -> None:
    caplog.set_level(logging.WARNING)
    t1_stamp, _ = _translated_send(send, module, cls, wire_format, _turn([], "first question"))
    assert t1_stamp.position == 2 and not t1_stamp.under_sealed  # after the template pair
    t2_stamp, _ = _translated_send(send, module, cls, wire_format, _turn(_t1_history(), TYPED), request_id="req-2")
    assert t2_stamp.position == 2 and t2_stamp.message_index == t1_stamp.message_index
    assert _breaks(caplog) == []
    _translated_send(
        send, module, cls, wire_format, _turn(_t1_history(), TYPED, template="Edited template"), request_id="req-3"
    )
    breaks = _breaks(caplog)
    template_item = "'message 1'" if cls == "OpenAITranslator" else "'message 0'"  # Responses: system item first
    assert len(breaks) == 1 and template_item in breaks[0], breaks


@pytest.mark.parametrize(("module", "cls", "wire_format"), REAL)
def test_a_chat_with_no_record_seals_tools_and_system_only(
    send: Any, caplog: pytest.LogCaptureFixture, module: str, cls: str, wire_format: str
) -> None:
    """A chat that predates the record: never over-seal its history."""
    caplog.set_level(logging.WARNING)
    remember_cache_state(CONV, {"last_response_at": "2026-11-01T00:00:00+00:00"})  # an earlier turn finished
    stamp, snapshot = _translated_send(send, module, cls, wire_format, _turn(_t1_history(), TYPED))
    assert stamp.under_sealed and stamp.position == 0
    assert all(not s.label.startswith("message") or s.label == "message 0" and cls == "OpenAITranslator"
               for s in snapshot.segments)  # Responses: the leading developer item IS the system
    # A history change (an allowed trim, an edited old turn) is below the line: nothing reported.
    _translated_send(send, module, cls, wire_format, _turn(_t1_history()[:1], TYPED), request_id="req-2")
    assert _breaks(caplog) == []


@pytest.mark.parametrize(("module", "cls", "wire_format"), REAL)
def test_a_model_switch_reuses_the_conversation_line(
    send: Any, caplog: pytest.LogCaptureFixture, module: str, cls: str, wire_format: str
) -> None:
    caplog.set_level(logging.WARNING)
    _translated_send(send, module, cls, wire_format, _turn([], "first question"))
    stamp, _ = _translated_send(send, module, cls, wire_format, _turn(_t1_history(), TYPED), model="other")
    assert stamp.position == 2 and not stamp.under_sealed
    assert _breaks(caplog) == []  # a new baseline under the new model, not a break


def test_a_restart_reads_the_line_from_cache_state(send: Any) -> None:
    module, cls, wire_format = REAL[0]
    _translated_send(send, module, cls, wire_format, _turn([], "first question"))
    persisted = {fos.SEAL_STATE_KEY: fos.merged_seal_state(None, fos.take_seal_records(CONV))}
    assert persisted[fos.SEAL_STATE_KEY][fos.POSITION_KEY]["index"] == 2
    fos.reset_for_tests()
    remember_cache_state(CONV, persisted)
    stamp, _ = _translated_send(send, module, cls, wire_format, _turn(_t1_history(), TYPED))
    assert stamp.position == 2 and not stamp.under_sealed


def test_side_runs_in_the_same_conversation_never_cross_the_baseline(
    send: Any, caplog: pytest.LogCaptureFixture
) -> None:
    """The labeler runs inside the conversation it names, on the same model: interleaved with the
    person's turns it must neither break nor replace the conversation's baseline or line."""
    caplog.set_level(logging.WARNING)
    module, cls, wire_format = REAL[0]
    _translated_send(send, module, cls, wire_format, _turn([], "first question"))
    labeler = UnifiedConfig(model="m", messages=MessageList(_messages=[]))
    labeler.system_instruction = "Name this conversation."
    labeler.messages.append_or_extend_user_input("first question / first answer")
    send.ctx.metadata = {"system_process": "system_process"}
    send.ctx.agent_id = None
    side_stamp, _ = _translated_send(send, module, cls, wire_format, labeler, request_id="lab-1")
    assert side_stamp.side
    send.ctx.metadata = {}
    send.ctx.agent_id = "agent-1"
    _translated_send(send, module, cls, wire_format, _turn(_t1_history(), TYPED), request_id="req-2")
    send.ctx.metadata = {"system_process": "system_process"}
    send.ctx.agent_id = None
    _translated_send(send, module, cls, wire_format, labeler, request_id="lab-2")
    assert _breaks(caplog) == []
    assert fos.conversation_position(CONV)["index"] == 2
    taken = fos.take_seal_records(CONV) or {}
    assert not any(k.startswith("side:") for k in taken)  # side runs are never persisted


def test_two_agents_in_one_conversation_on_one_model_keep_separate_baselines(
    send: Any, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.WARNING)
    send(_body())
    send.ctx.agent_id = "agent-2"
    send(_body(system="another agent's prompt"), request_id="req-2")
    send.ctx.agent_id = "agent-1"
    send(_body(), request_id="req-3")
    assert _breaks(caplog) == []


# ---------------------------------------------------------------------------
# Cost on the send path
# ---------------------------------------------------------------------------


def test_outside_an_agent_loop_nothing_is_serialized_or_parsed(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    class _CountingJson:
        @staticmethod
        def dumps(*a: Any, **k: Any) -> Any:
            calls.append("dumps")
            return json.dumps(*a, **k)

        @staticmethod
        def loads(*a: Any, **k: Any) -> Any:
            calls.append("loads")
            return json.loads(*a, **k)

    ctx = _Ctx()
    monkeypatch.setattr("matrx_connect.context.app_context.try_get_app_context", lambda: ctx)
    monkeypatch.setattr(fos, "json", _CountingJson)
    set_call_meta(CallMeta(provider="google", model="m"))
    fos.stamp_seal(fos.SealStamp(fos.SHAPE_GOOGLE, 0, None))
    url = "https://generativelanguage.googleapis.com/v1beta/models/m:generateContent"
    assert fos.observe_wire_body(url=url, body_obj={"contents": [{"role": "user", "parts": [{"text": "x"}]}]}) is None
    assert calls == []  # no ExecutionState: nothing reads the record, so nothing is serialized
    assert fos.current_seal_stamp() is None  # cleared with its send


def test_large_bodies_are_fingerprinted_off_the_send_path(send: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    async def run() -> Any:
        returned = send(_body())
        await fos.wait_for_pending()
        return returned

    assert asyncio.run(run()) is None  # the hook returned at once
    assert fos.take_seal_records(CONV)  # the record landed from the worker process


def test_the_genai_patch_passes_every_keyword_through(monkeypatch: pytest.MonkeyPatch) -> None:
    """genai's retry path calls ``_async_request_once(..., implicit_retry=False)``."""
    from google.genai import _api_client

    from matrx_ai.providers import request_capture

    seen: dict[str, Any] = {}

    async def original(self: Any, http_request: Any, stream: bool = False, *, implicit_retry: bool = True) -> str:
        seen["implicit_retry"] = implicit_retry
        return "sent"

    monkeypatch.setattr(_api_client.BaseApiClient, "_async_request_once", original)
    monkeypatch.setattr(request_capture, "_GENAI_INSTALLED", False)
    request_capture.install_genai_capture()

    class _Req:
        data = b"{}"
        url = "https://generativelanguage.googleapis.com/v1beta/models/m:generateContent"
        method = "POST"
        headers: dict[str, str] = {}

    result = asyncio.run(_api_client.BaseApiClient._async_request_once(None, _Req(), False, implicit_retry=False))
    assert result == "sent" and seen == {"implicit_retry": False}


# ---------------------------------------------------------------------------
# Hardening: backpressure, ordering, over-seal edges
# ---------------------------------------------------------------------------


def test_a_flood_past_the_cap_is_dropped_and_never_blocks(send: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    import threading

    gate = threading.Event()
    started: list[int] = []
    real = fos._run_in_worker

    def slow(payload: Any) -> Any:
        started.append(1)
        gate.wait(5)
        return real(payload)

    monkeypatch.setattr(fos, "_run_in_worker", slow)
    monkeypatch.setattr(fos, "seal_pending_max", lambda: 3)

    async def run() -> tuple[float, int]:
        began = time.perf_counter()
        for index in range(20):
            send(_body(), request_id=f"req-{index}")
        elapsed = time.perf_counter() - began
        pending = len(fos._PENDING)
        gate.set()
        await fos.wait_for_pending()
        return elapsed, pending

    elapsed, pending = asyncio.run(run())
    assert pending == 3 and elapsed < 1.0  # capped, and no send waited


def test_an_older_send_finishing_later_never_overwrites_a_newer_one(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING)
    send(_body())  # the baseline
    newer = send(_body(), request_id="req-new")
    assert newer is not None
    older = fos.FinalOutboundSnapshot(
        provider="anthropic", model="m", conversation_id=CONV, request_id="req-old", loop_round=None,
        fidelity="bytes", body_sha256="x", body_bytes=0, seal=newer.seal,
        segments=tuple(fos.segment_of(s.label, b"different") for s in newer.segments),
        agent_id="agent-1", at=newer.at - 1.0,
    )
    assert fos.check_and_remember(older) == []  # completed out of order: not compared, not stored
    send(_body(), request_id="req-next")
    assert _breaks(caplog) == []  # the newer record stayed the baseline


def test_an_unreadable_conversation_row_is_never_an_assembly_send(send: Any) -> None:
    fos.note_conversation_row_read(CONV, known=False)
    stamp, _ = _translated_send(send, *REAL[0], _turn([], "first question"))
    assert stamp.under_sealed and fos.conversation_position(CONV) is None  # no position stored
    fos.note_conversation_row_read(CONV, known=True)
    stamp, _ = _translated_send(send, *REAL[0], _turn([], "first question"), request_id="req-2")
    assert not stamp.under_sealed and fos.conversation_position(CONV)["index"] == 2


def test_a_fork_seeded_with_copied_history_is_never_an_assembly_send(send: Any) -> None:
    """No completed turn of its own, but earlier person turns above the line (copied history)."""
    copied = [
        UnifiedMessage(role="user", content=[TextContent(text="an earlier question")], id="c1", position=2),
        UnifiedMessage(role="assistant", content=[TextContent(text="an earlier answer")], id="c2", position=3),
    ]
    stamp, snapshot = _translated_send(send, *REAL[0], _turn(copied, TYPED))
    assert stamp.under_sealed and fos.conversation_position(CONV) is None
    assert not any(s.label.startswith("message") for s in snapshot.segments)


# ---------------------------------------------------------------------------
# Live findings (2026-11-12): the split-then-merged first turn, the report wording
# ---------------------------------------------------------------------------


def _anthropic(messages: list[dict[str, Any]]) -> bytes:
    return json.dumps({"model": "m", "system": [{"type": "text", "text": SYSTEM}], "messages": messages}).encode()


def test_turn_one_split_then_turn_two_merged_is_not_a_break(send: Any, caplog: pytest.LogCaptureFixture) -> None:
    """Turn 1: the line sits INSIDE message 0 at block 1 (template, then the merged per-turn block,
    then her words). Turn 2: the stored turn is merged (B8), the line sits after the whole of message 0,
    and the template block only lost its cache mark. Its head is unchanged: no break."""
    caplog.set_level(logging.WARNING)
    marked = {"type": "text", "text": TEMPLATE, "cache_control": {"type": "ephemeral"}}
    plain = {"type": "text", "text": TEMPLATE}
    send(_anthropic([{"role": "user", "content": [marked, {"type": "text", "text": MARK}, {"type": "text", "text": "q1"}]}]),
         stamp=(0, 1))
    turn_two = [
        {"role": "user", "content": [plain, {"type": "text", "text": "q1"}]},
        {"role": "assistant", "content": [{"type": "text", "text": "a1"}]},
        {"role": "user", "content": [{"type": "text", "text": MARK}, {"type": "text", "text": TYPED}]},
    ]
    send(_anthropic(turn_two), request_id="req-2", stamp=(1, None))
    assert _breaks(caplog) == []
    turn_two[0]["content"][0] = {"type": "text", "text": "Edited template"}
    send(_anthropic(turn_two), request_id="req-3", stamp=(1, None))
    breaks = _breaks(caplog)
    assert len(breaks) == 1 and "'message 0'" in breaks[0]  # one change, one report


def test_the_warning_names_the_provider_call_and_where_the_baseline_came_from(
    send: Any, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.WARNING)
    send(_body())
    send(_body(system="changed"), request_id="req-2")
    breaks = _breaks(caplog)
    assert len(breaks) == 1 and "provider call" in breaks[0] and "baseline from this process" in breaks[0]
    assert "round" not in breaks[0]


def test_a_record_says_whether_it_was_compared(send: Any) -> None:
    """The screen calls a segment stable only after a comparison: the first send is not compared."""
    send(_body())
    first = next(v for k, v in fos.take_seal_records(CONV).items() if k != fos.POSITION_KEY)
    assert first["compared"] is False
    send(_body(), request_id="req-2")
    second = next(v for k, v in fos.take_seal_records(CONV).items() if k != fos.POSITION_KEY)
    assert second["compared"] is True


def test_the_check_is_off_unless_switched_on(monkeypatch):
    """Off by default (knob seal_check_on = 0): a send is never parsed, hashed or queued."""
    import types

    from matrx_ai.providers import final_outbound_snapshot as _fos

    monkeypatch.setattr(_fos, "seal_check_on", lambda: False)
    calls: list[str] = []
    monkeypatch.setattr(_fos, "_fingerprint_safely", lambda *a, **k: calls.append("fp"))
    monkeypatch.setattr(_fos, "_off_loop", lambda *a, **k: calls.append("queued") or True)
    monkeypatch.setattr(_fos, "_in_agent_loop", lambda: True)
    monkeypatch.setattr(_fos, "_send_identity", lambda: types.SimpleNamespace(conversation_id="c-1"))
    monkeypatch.setattr(_fos, "shape_of_url", lambda url: "anthropic")
    stamp = types.SimpleNamespace(shape="anthropic")
    token = _fos._stamp_var.set(stamp)
    try:
        assert _fos.SEAL_CHECK_ON_MIRROR == 0
        assert _fos.observe_wire_body(url="https://api.anthropic.com/v1/messages", body=b'{"messages": []}') is None
    finally:
        _fos._stamp_var.reset(token)
    assert calls == []

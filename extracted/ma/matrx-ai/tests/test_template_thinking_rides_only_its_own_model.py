"""A thinking part saved into an agent's template rides only to the model that wrote it.

The feature (2026-11-13): an authored template may carry an assistant turn with a THINKING part
from a real run — Anthropic signed thinking, OpenAI reasoning (encrypted_content + id), Gemini
thought signatures, including the signature on a Gemini TEXT part. The model that produced it is
stamped at intake (``metadata.produced_by``); at the send boundary a template part from another
model is removed from the wire (never turned into visible text), and a same-model part goes
verbatim — so turn 1 (from the agent definition) and turn 2 (from the stored rows) send the same
bytes. Live conversation history is never touched. ``matrx_ai/config/template_thinking.py``.
"""

from __future__ import annotations

import base64
import json
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import MessageList, TextContent, ThinkingContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.cache_marks import TEMPLATE_METADATA_KEY, TEMPLATE_STABLE
from matrx_ai.config.send_boundary import SendPrep
from matrx_ai.config.template_thinking import (
    PRODUCED_BY_KEY,
    STEP_NAME,
    STORED_GOOGLE_TEXT_SIGNATURE_KEY,
    drop_foreign_template_thinking,
    stamp_produced_by,
)
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.config.unified_content import reconstruct_content
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.providers.openai.translator import OpenAITranslator
from matrx_ai.providers.unified_client import UnifiedAIClient, _build_provider_wire_config
from matrx_ai.testing.profile_factory import make_profile

CLAUDE = make_profile(model_name="claude-sonnet-4-5", wire_format="anthropic_chat")
OPUS = make_profile(model_name="claude-opus-4-5", wire_format="anthropic_chat")
GPT = make_profile(model_name="gpt-5", wire_format="openai_chat")
GEMINI = make_profile(model_name="gemini-3-pro", wire_format="google_chat")
GEMINI_FLASH = make_profile(model_name="gemini-3-flash", wire_format="google_chat")


def _stamp(profile: Any) -> dict[str, str]:
    return {
        "model": profile.model_name,
        "model_id": profile.model_id,
        "provider_model_id": profile.provider_model_id,
        "provider": profile.vendor,
        "offering_id": profile.offering_id,
    }


def _thinking_parts(profile: Any) -> list[Any]:
    """The thinking (and signed text) parts each provider really returns, stamped by ``profile``."""
    stamp = {PRODUCED_BY_KEY: _stamp(profile)}
    if profile.wire_format == "anthropic_chat":
        return [
            ThinkingContent(text="weigh the two drafts", provider="anthropic", signature="sig-ant-1", metadata=dict(stamp)),
            TextContent(text="Draft B is stronger."),
        ]
    if profile.wire_format == "openai_chat":
        return [
            ThinkingContent(
                id="rs_123",
                provider="openai",
                signature="enc-blob-1",
                summary=[{"type": "summary_text", "text": "compared drafts"}],
                metadata=dict(stamp),
            ),
            TextContent(text="Draft B is stronger."),
        ]
    return [
        ThinkingContent(text="compare drafts", provider="google", signature=b"\x01gsig", metadata=dict(stamp)),
        TextContent(
            text="Draft B is stronger.",
            metadata={"google_thought_signature": b"\x02tsig", **{PRODUCED_BY_KEY: _stamp(profile)}},
        ),
    ]


def _template_config(producer: Any, outgoing: Any) -> UnifiedConfig:
    messages = MessageList()
    messages.append(UnifiedMessage(role="user", content=[TextContent(text="Compare these drafts.")]))
    messages.append(UnifiedMessage(role="assistant", content=_thinking_parts(producer)))
    messages.append(UnifiedMessage(role="user", content=[TextContent(text="Now this pair.")]))
    for message in list(messages)[:2]:
        message.metadata[TEMPLATE_METADATA_KEY] = TEMPLATE_STABLE
    return UnifiedConfig(model=outgoing.model_name, messages=messages, max_output_tokens=2000)


def _rebuilt_from_rows(config: UnifiedConfig) -> UnifiedConfig:
    """Turn 2: the conversation's stored cx_message rows, read back through the one decoder."""
    rows = json.loads(json.dumps(config.to_storage_dict()["messages"]))  # through JSONB
    messages = MessageList()
    for position, row in enumerate(rows):
        stored = SimpleNamespace(
            id=f"m{position}", role=row["role"], content=row["content"], user_content=None,
            created_at=None, status="active", metadata=row.get("metadata") or {}, position=position,
        )
        messages.append(UnifiedMessage.from_cx_message(stored))
    return UnifiedConfig(model=config.model, messages=messages, max_output_tokens=config.max_output_tokens)


def _bytes_safe(value: Any) -> Any:
    if isinstance(value, (bytes, bytearray)):
        return {"__bytes__": base64.b64encode(bytes(value)).decode()}
    raise TypeError(type(value).__name__)


def _wire(config: UnifiedConfig, profile: Any) -> str:
    prep = SendPrep(stage="loop")
    drop_foreign_template_thinking(prep, config, profile)
    sent = prep.wire_config if prep.wire_config is not None else config
    wire_config = _build_provider_wire_config(sent, profile)
    if profile.wire_format == "anthropic_chat":
        payload = AnthropicTranslator().to_anthropic(wire_config, profile)
        body = payload["messages"]
    elif profile.wire_format == "openai_chat":
        payload = OpenAITranslator().to_openai(wire_config, profile)
        body = payload["input"]
    else:
        payload = GoogleTranslator().to_google(wire_config, profile)
        body = [c.model_dump(exclude_none=True) if hasattr(c, "model_dump") else c for c in payload["contents"]]
    return json.dumps(body, default=_bytes_safe, sort_keys=True)


# --------------------------------------------------------------------------- decoder + storage


def test_the_decoder_keeps_a_thinking_parts_metadata() -> None:
    stored = ThinkingContent(
        id="rs_9", provider="openai", signature="enc", metadata={PRODUCED_BY_KEY: _stamp(GPT), "id": "rs_9"}
    ).to_storage_dict()
    part = reconstruct_content(json.loads(json.dumps(stored)))
    assert isinstance(part, ThinkingContent)
    assert part.metadata[PRODUCED_BY_KEY] == _stamp(GPT)
    assert part.id == "rs_9"
    # The wire never carries metadata.
    assert "metadata" not in json.dumps(part.to_openai())
    assert PRODUCED_BY_KEY not in json.dumps(part.to_anthropic() or {})


def test_a_gemini_signed_text_part_keeps_its_signature_and_stamp_through_storage() -> None:
    text = TextContent(
        text="Draft B.", metadata={"google_thought_signature": b"\x02tsig", PRODUCED_BY_KEY: _stamp(GEMINI)}
    )
    part = reconstruct_content(json.loads(json.dumps(text.to_storage_dict())))
    # Kept under a key no translator reads: the stored part alone sends what it always did.
    assert part.metadata[STORED_GOOGLE_TEXT_SIGNATURE_KEY] == b"\x02tsig"
    assert "google_thought_signature" not in part.metadata
    assert part.metadata[PRODUCED_BY_KEY] == _stamp(GEMINI)
    assert part.to_google() == {"text": "Draft B."}


def test_a_plain_text_parts_storage_is_unchanged() -> None:
    assert TextContent(text="hi").to_storage_dict() == {"type": "text", "text": "hi"}


# --------------------------------------------------------------------------- intake stamp


def test_intake_stamps_the_producing_model_on_thinking_and_signed_text_only() -> None:
    thinking = ThinkingContent(text="t", provider="google", signature=b"s")
    signed = TextContent(text="a", metadata={"google_thought_signature": b"x"})
    plain = TextContent(text="b")
    response = UnifiedResponse(messages=[UnifiedMessage(role="assistant", content=[thinking, signed, plain])])
    UnifiedAIClient._stamp_offering_usage(response, GEMINI, UnifiedConfig(model="gemini-3-pro", messages=MessageList()))
    assert thinking.metadata[PRODUCED_BY_KEY] == _stamp(GEMINI)
    assert signed.metadata[PRODUCED_BY_KEY] == _stamp(GEMINI)
    assert PRODUCED_BY_KEY not in plain.metadata


def test_intake_never_overwrites_an_existing_stamp() -> None:
    thinking = ThinkingContent(text="t", provider="anthropic", signature="s", metadata={PRODUCED_BY_KEY: {"model": "x"}})
    response = UnifiedResponse(messages=[UnifiedMessage(role="assistant", content=[thinking])])
    assert stamp_produced_by(response, CLAUDE) == 0
    assert thinking.metadata[PRODUCED_BY_KEY] == {"model": "x"}


# --------------------------------------------------------------------------- same model: verbatim, byte-stable


@pytest.mark.parametrize("profile", [CLAUDE, GPT, GEMINI], ids=["anthropic", "openai", "google"])
def test_same_model_template_thinking_sends_the_same_bytes_on_turn_1_and_turn_2(profile: Any) -> None:
    turn_1 = _template_config(profile, profile)
    turn_2 = _rebuilt_from_rows(turn_1)
    wire_1, wire_2 = _wire(turn_1, profile), _wire(turn_2, profile)
    assert wire_1 == wire_2
    signature = {"anthropic_chat": "sig-ant-1", "openai_chat": "enc-blob-1"}.get(profile.wire_format)
    if signature:
        assert signature in wire_1
    else:
        assert base64.b64encode(b"\x01gsig").decode() in wire_1  # thinking signature
        assert base64.b64encode(b"\x02tsig").decode() in wire_1  # signed text part


# --------------------------------------------------------------------------- different model: removed, noted


@pytest.mark.parametrize(
    ("producer", "outgoing", "secret"),
    [
        (CLAUDE, OPUS, "weigh the two drafts"),
        (CLAUDE, GEMINI, "weigh the two drafts"),
        (GPT, CLAUDE, "compared drafts"),
        (GEMINI, CLAUDE, "compare drafts"),
        (GEMINI, GPT, "compare drafts"),
    ],
)
def test_a_different_model_never_receives_the_thinking_not_even_as_text(producer: Any, outgoing: Any, secret: str) -> None:
    config = _template_config(producer, outgoing)
    stored_before = json.dumps(config.to_storage_dict(), sort_keys=True, default=str)
    prep = SendPrep(stage="loop")
    notes = drop_foreign_template_thinking(prep, config, outgoing)
    assert prep.wire_config is not None and STEP_NAME in prep.steps
    assert any(producer.model_name in n and "static seal break expected" in n for n in notes)
    wire = _wire(config, outgoing)
    assert secret not in wire
    assert "Draft B is stronger." in wire
    # The canonical config (what the chat stores) still holds the part.
    assert json.dumps(config.to_storage_dict(), sort_keys=True, default=str) == stored_before


def test_a_gemini_signed_text_part_loses_only_its_signature_for_another_gemini_model() -> None:
    config = _template_config(GEMINI, GEMINI_FLASH)
    wire = _wire(config, GEMINI_FLASH)
    assert "Draft B is stronger." in wire
    assert base64.b64encode(b"\x02tsig").decode() not in wire
    assert base64.b64encode(b"\x01gsig").decode() not in wire


# --------------------------------------------------------------------------- no stamp, and live history


def test_unstamped_template_thinking_is_kept_only_on_its_own_provider() -> None:
    def config_for(outgoing: Any) -> UnifiedConfig:
        config = _template_config(CLAUDE, outgoing)
        list(config.messages)[1].content[0].metadata.clear()
        return config

    same = SendPrep(stage="loop")
    notes = drop_foreign_template_thinking(same, config_for(OPUS), OPUS)
    assert same.wire_config is None and any("kept (same provider anthropic)" in n for n in notes)

    other = config_for(GPT)
    assert "weigh the two drafts" not in _wire(other, GPT)
    assert "weigh the two drafts" not in _wire(config_for(GEMINI), GEMINI)


def test_live_history_thinking_is_never_touched() -> None:
    config = _template_config(CLAUDE, GEMINI)
    for message in config.messages:
        message.metadata.pop(TEMPLATE_METADATA_KEY, None)
    prep = SendPrep(stage="loop")
    assert drop_foreign_template_thinking(prep, config, GEMINI) == []
    assert prep.wire_config is None and STEP_NAME not in prep.steps


# --------------------------------------------------------------------------- the real boundary


@pytest.mark.asyncio
async def test_prepare_for_send_runs_the_step_on_the_wire_only(monkeypatch) -> None:
    from matrx_ai.catalog import resolve as catalog_resolve
    from matrx_ai.config import context_preflight
    from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state
    from matrx_ai.knobs import configure_package_knobs

    configure_package_knobs(None)
    monkeypatch.setattr(context_preflight, "_declared_window", lambda _ref: None)

    async def _profile(model: str, **_kw: Any) -> Any:
        return {p.model_name: p for p in (CLAUDE, OPUS, GPT, GEMINI)}[model]

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", _profile)
    conversation, request = "conv-template-thinking", "req-template-thinking"
    reset_loop_state(conversation, request)
    try:
        config = _template_config(CLAUDE, GPT)
        before = json.dumps(config.to_storage_dict(), sort_keys=True, default=str)
        prep = await prepare_for_send(
            config, stage=STAGE_LOOP, conversation_id=conversation, request_id=request, iteration=1
        )
        assert STEP_NAME in prep.steps
        wire_parts = [p for m in prep.wire_config.messages for p in m.content]
        assert not any(isinstance(p, ThinkingContent) for p in wire_parts)
        assert json.dumps(config.to_storage_dict(), sort_keys=True, default=str) == before

        same = _template_config(CLAUDE, CLAUDE)
        prep_same = await prepare_for_send(
            same, stage=STAGE_LOOP, conversation_id=conversation, request_id=request, iteration=2
        )
        assert STEP_NAME not in prep_same.steps
        sent = prep_same.wire_config if prep_same.wire_config is not None else same
        assert any(isinstance(p, ThinkingContent) for m in sent.messages for p in m.content)
    finally:
        reset_loop_state(conversation, request)


# --------------------------------------------------------------------------- live Gemini wire: unchanged


def _live_gemini_config(text_metadata: dict[str, Any]) -> UnifiedConfig:
    messages = MessageList()
    messages.append(UnifiedMessage(role="user", content=[TextContent(text="Compare these drafts.")]))
    messages.append(
        UnifiedMessage(
            role="assistant",
            content=[
                ThinkingContent(text="compare drafts", provider="google", signature=b"\x01gsig"),
                TextContent(text="Draft B is stronger.", metadata=dict(text_metadata)),
            ],
        )
    )
    messages.append(UnifiedMessage(role="user", content=[TextContent(text="Now this pair.")]))
    return UnifiedConfig(model=GEMINI.model_name, messages=messages, max_output_tokens=2000)


def test_a_live_gemini_later_turn_sends_exactly_what_it_sent_before_this_change() -> None:
    """Before: storage dropped the text signature, so a later turn sent the text without one. The
    stored (stamped) part must render the same wire as a part that never had a signature."""
    signed = _live_gemini_config({"google_thought_signature": b"\x02tsig", PRODUCED_BY_KEY: _stamp(GEMINI)})
    later_turn = _wire(_rebuilt_from_rows(signed), GEMINI)
    before_change = _wire(_rebuilt_from_rows(_live_gemini_config({})), GEMINI)
    assert later_turn == before_change
    assert base64.b64encode(b"\x02tsig").decode() not in later_turn


def test_an_in_request_tool_loop_still_sends_the_in_memory_text_signature() -> None:
    """Within one request the parts are the provider's own objects (never stored): unchanged."""
    live = _live_gemini_config({"google_thought_signature": b"\x02tsig", PRODUCED_BY_KEY: _stamp(GEMINI)})
    wire = _wire(live, GEMINI)
    assert base64.b64encode(b"\x02tsig").decode() in wire
    assert wire == _wire(_live_gemini_config({"google_thought_signature": b"\x02tsig"}), GEMINI)


def test_a_stored_text_signature_is_restored_only_for_its_own_model() -> None:
    stored = _rebuilt_from_rows(_template_config(GEMINI, GEMINI))
    assert base64.b64encode(b"\x02tsig").decode() in _wire(stored, GEMINI)
    other = _rebuilt_from_rows(_template_config(GEMINI, GEMINI_FLASH))
    assert base64.b64encode(b"\x02tsig").decode() not in _wire(other, GEMINI_FLASH)


# --------------------------------------------------------------------------- no send profile, and the step failing


def _unstamped(producer: Any, outgoing: Any) -> UnifiedConfig:
    config = _template_config(producer, outgoing)
    list(config.messages)[1].content[0].metadata.clear()
    return config


def _wire_parts(prep: SendPrep, config: UnifiedConfig) -> list[Any]:
    sent = prep.wire_config if prep.wire_config is not None else config
    return [p for m in sent.messages for p in m.content]


def _resolver(monkeypatch, known: dict[str, Any]) -> None:
    from matrx_ai.catalog import resolve as catalog_resolve

    async def _profile(model: str, **_kw: Any) -> Any:
        if model not in known:
            raise RuntimeError(f"unknown model {model!r}")
        return known[model]

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", _profile)


@pytest.mark.asyncio
async def test_with_no_send_profile_the_provider_of_config_model_decides(monkeypatch) -> None:
    from matrx_ai.config.template_thinking import apply_template_thinking

    _resolver(monkeypatch, {GPT.model_name: GPT, OPUS.model_name: OPUS})
    foreign = _unstamped(CLAUDE, GPT)
    prep = SendPrep(stage="loop")
    await apply_template_thinking(prep, foreign, None)
    assert not any(isinstance(p, ThinkingContent) for p in _wire_parts(prep, foreign))

    own = _unstamped(CLAUDE, OPUS)
    prep_own = SendPrep(stage="loop")
    await apply_template_thinking(prep_own, own, None)
    assert any(isinstance(p, ThinkingContent) for p in _wire_parts(prep_own, own))


@pytest.mark.asyncio
async def test_an_unresolvable_model_drops_unstamped_template_thinking(monkeypatch) -> None:
    from matrx_ai.config.template_thinking import apply_template_thinking

    _resolver(monkeypatch, {})
    config = _unstamped(CLAUDE, GEMINI)
    prep = SendPrep(stage="loop")
    notes = await apply_template_thinking(prep, config, None)
    assert not any(isinstance(p, ThinkingContent) for p in _wire_parts(prep, config))
    assert any("could not be resolved" in n for n in notes)


@pytest.mark.asyncio
async def test_the_step_failing_fails_closed_for_template_thinking_only(monkeypatch) -> None:
    from matrx_ai.config import template_thinking

    def _boom(*_a: Any, **_k: Any) -> Any:
        raise RuntimeError("step broke")

    monkeypatch.setattr(template_thinking, "drop_foreign_template_thinking", _boom)
    config = _template_config(GEMINI, CLAUDE)
    live = UnifiedMessage(role="assistant", content=[ThinkingContent(text="live thought", provider="anthropic", signature="s")])
    config.messages.append(live)
    stored_before = json.dumps(config.to_storage_dict(), sort_keys=True, default=str)
    prep = SendPrep(stage="loop")
    notes = await template_thinking.apply_template_thinking(prep, config, CLAUDE)
    parts = _wire_parts(prep, config)
    template_parts = [p for m in list(prep.wire_config.messages)[:2] for p in m.content]
    assert not any(isinstance(p, ThinkingContent) for p in template_parts)
    assert not any("google_thought_signature" in (getattr(p, "metadata", None) or {}) for p in template_parts)
    assert any(getattr(p, "text", "") == "live thought" for p in parts)  # live history untouched
    assert f"{template_thinking.STEP_NAME}:fail_closed" in prep.steps and notes
    assert json.dumps(config.to_storage_dict(), sort_keys=True, default=str) == stored_before


# --------------------------------------------------------------------------- a template turn left empty


@pytest.mark.parametrize("outgoing", [CLAUDE, GPT, GEMINI], ids=["anthropic", "openai", "google"])
def test_a_template_turn_holding_only_foreign_thinking_leaves_a_valid_wire(outgoing: Any) -> None:
    """The emptied assistant turn is left off: two person turns in a row. Anthropic's translator
    merges them into one user turn; OpenAI Responses and Gemini take consecutive user turns."""
    producer = GEMINI if outgoing is not GEMINI else CLAUDE
    config = _template_config(producer, outgoing)
    turn = list(config.messages)[1]
    turn.content = [p for p in turn.content if isinstance(p, ThinkingContent)]
    body = json.loads(_wire(config, outgoing))
    if outgoing is CLAUDE:
        assert [m["role"] for m in body] == ["user"]
        assert [b["text"] for b in body[0]["content"]] == ["Compare these drafts.", "Now this pair."]
    elif outgoing is GPT:
        assert [(m["role"], m["content"][0]["text"]) for m in body] == [
            ("user", "Compare these drafts."),
            ("user", "Now this pair."),
        ]
    else:
        assert [(m["role"], m["parts"][0]["text"]) for m in body] == [
            ("user", "Compare these drafts."),
            ("user", "Now this pair."),
        ]



@pytest.mark.asyncio
async def test_a_double_failure_never_fails_the_send(monkeypatch) -> None:
    """Both the step and its fail-closed path throw: logged, noted, the send continues."""
    from matrx_ai.config import template_thinking

    def _boom(*_a: Any, **_k: Any) -> Any:
        raise RuntimeError("broke")

    monkeypatch.setattr(template_thinking, "drop_foreign_template_thinking", _boom)
    monkeypatch.setattr(template_thinking, "_fail_closed", _boom)
    config = _template_config(GEMINI, CLAUDE)
    prep = SendPrep(stage="loop")
    notes = await template_thinking.apply_template_thinking(prep, config, CLAUDE)
    assert f"{template_thinking.STEP_NAME}:failed_open" in prep.steps
    assert notes and "both failed" in notes[0]
    assert prep.wire_config is None  # the send goes out exactly as before the step existed

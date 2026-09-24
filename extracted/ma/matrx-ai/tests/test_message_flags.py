"""Message FLAGS — prefill, cache boundary, example (typed-messages FEATURE.md, Flag row).

Each test names the real use: a support-reply drafter whose system prompt is
cached, whose two example exchanges are few-shot turns, and whose reply must
start "Dear". The translators decide the wire; a flag a model cannot honour is
refused, converted or dropped by the org's mode — never silently lost.
"""

from __future__ import annotations

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.message_config import MessageSanitizationError
from matrx_ai.config.message_flags import (
    FLAGS_METADATA_KEY,
    InvalidMessageFlags,
    MessageFlagRefusal,
    apply_prefill_to_reply,
    flags_of,
    parse_flags,
    plan_message_flags,
    validate_message_flags,
)
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile

CUSTOMER = "My order #4417 arrived with a cracked screen protector. Can you send a new one?"


def _msg(role: str, text: str, **flags: bool) -> UnifiedMessage:
    data: dict = {"role": role, "content": [{"type": "text", "text": text}]}
    if flags:
        data["flags"] = flags
    return UnifiedMessage.from_dict(data)


def _drafter(prefill: bool = True) -> list[UnifiedMessage]:
    msgs = [
        _msg("user", "Order arrived two days late and the box was crushed.", example=True),
        _msg("assistant", "Dear Priya, I'm sorry your order arrived late and damaged...", example=True, cache_boundary=True),
        _msg("user", CUSTOMER),
    ]
    if prefill:
        msgs.append(_msg("assistant", "Dear ", prefill=True))
    return msgs


# ── storage + validation ────────────────────────────────────────────────────


def test_from_dict_keeps_flags_in_metadata_for_persistence() -> None:
    msg = _msg("assistant", "Dear", prefill=True)
    assert msg.metadata[FLAGS_METADATA_KEY] == {"prefill": True}
    assert flags_of(msg) == {"prefill": True}
    assert msg.to_storage_dict()["metadata"][FLAGS_METADATA_KEY] == {"prefill": True}


def test_unknown_flag_is_refused_not_carried() -> None:
    with pytest.raises(InvalidMessageFlags):
        parse_flags({"prefil": True})
    with pytest.raises(InvalidMessageFlags):
        UnifiedMessage.from_dict({"role": "user", "content": "hi", "flags": {"pin": True}})


def test_false_flag_means_absent() -> None:
    assert parse_flags({"example": False, "cache_boundary": True}) == {"cache_boundary": True}


def test_placement_rules() -> None:
    system = {"role": "system", "content": [{"type": "text", "text": "You draft support replies."}], "flags": {"cache_boundary": True}}
    user = {"role": "user", "content": [{"type": "text", "text": CUSTOMER}]}
    prefill = {"role": "assistant", "content": [{"type": "text", "text": "Dear"}], "flags": {"prefill": True}}
    validate_message_flags([system, user, prefill])  # cache boundary on system is fine

    with pytest.raises(InvalidMessageFlags, match="not the last message"):
        validate_message_flags([system, prefill, user])
    with pytest.raises(InvalidMessageFlags, match="only an assistant"):
        validate_message_flags([system, {**user, "flags": {"prefill": True}}])
    with pytest.raises(InvalidMessageFlags, match="only user and assistant"):
        validate_message_flags([{**system, "flags": {"example": True}}, user])
    with pytest.raises(InvalidMessageFlags, match="no text"):
        validate_message_flags([user, {**prefill, "content": [{"type": "text", "text": "  "}]}])


def test_execution_definition_refuses_a_misplaced_prefill() -> None:
    from matrx_ai.client_host.agent_source import ExecutionAgentDefinition

    with pytest.raises(Exception, match="prefill"):
        ExecutionAgentDefinition(
            definition_id="d",
            agent_id="a",
            model_id="m",
            messages=[
                {"role": "assistant", "content": [{"type": "text", "text": "Dear"}], "flags": {"prefill": True}},
                {"role": "user", "content": [{"type": "text", "text": CUSTOMER}]},
            ],
        )


def test_user_input_lands_before_a_trailing_prefill() -> None:
    messages = MessageList(_messages=[_msg("user", "{{customer_message}}"), _msg("assistant", "Dear", prefill=True)])
    messages.append_or_extend_user_input("Please be brief.")
    assert [m.role for m in messages] == ["user", "assistant"]
    assert "Please be brief." in messages[0].content[0].text
    assert flags_of(messages[-1]) == {"prefill": True}


# ── the plan (provider-agnostic gate) ───────────────────────────────────────


def test_native_prefill_is_kept_on_the_wire() -> None:
    plan = plan_message_flags(_drafter(), supports_prefill=True, cache_boundary_support="breakpoint", model_label="claude-haiku-4-5")
    assert plan.prefill_mode == "native" and plan.prefill_text == "Dear"
    assert len(plan.wire_messages) == 4
    assert plan.examples == 2 and plan.cache_boundaries == 1 and plan.notes == []


def test_refuse_names_the_model_before_any_spend() -> None:
    with pytest.raises(MessageFlagRefusal, match="claude-sonnet-5 cannot continue a reply from a prefill"):
        plan_message_flags(_drafter(), supports_prefill=False, cache_boundary_support="breakpoint", model_label="claude-sonnet-5")


def test_convert_asks_for_the_start_and_says_so() -> None:
    plan = plan_message_flags(_drafter(), supports_prefill=False, cache_boundary_support="automatic", model_label="gpt-5", mode="convert")
    assert plan.prefill_mode == "convert"
    assert len(plan.wire_messages) == 3 and plan.wire_messages[-1].role == "user"
    assert "Begin your reply with exactly" in (plan.convert_instruction or "")
    assert any("asked for, not forced" in n for n in plan.notes)
    assert any("caches repeated prompt prefixes automatically" in n for n in plan.notes)


def test_drop_mode_announces_it() -> None:
    plan = plan_message_flags(_drafter(), supports_prefill=False, cache_boundary_support="implicit", model_label="gemini-3-pro", mode="drop")
    assert plan.prefill_mode == "drop" and len(plan.wire_messages) == 3
    assert any("was not sent" in n for n in plan.notes)
    assert any("implicitly" in n for n in plan.notes)


def test_a_consumed_prefill_never_reaches_a_wire_again() -> None:
    history = _drafter() + [_msg("assistant", "Dear Sam, a replacement is on its way."), _msg("user", "Thanks! Can it ship express?")]
    plan = plan_message_flags(history, supports_prefill=False, cache_boundary_support="breakpoint", model_label="claude-sonnet-5")
    assert plan.prefill_mode is None
    assert all(not flags_of(m).get("prefill") for m in plan.wire_messages)


def test_native_reply_is_stored_whole() -> None:
    plan = plan_message_flags(_drafter(), supports_prefill=True, cache_boundary_support="breakpoint", model_label="claude-haiku-4-5")
    reply = UnifiedMessage(role="assistant", content=[TextContent(text=" Sam, I'm sorry about the cracked protector.")])
    record = apply_prefill_to_reply([reply], plan)
    assert reply.content[0].text.startswith("Dear Sam")
    assert record == {"mode": "native", "text": "Dear", "forced": True, "starts_with_prefill": True}
    assert reply.metadata["prefill"]["mode"] == "native"


def test_converted_reply_records_whether_it_complied() -> None:
    plan = plan_message_flags(_drafter(), supports_prefill=False, cache_boundary_support="breakpoint", model_label="claude-sonnet-5", mode="convert")
    ok = UnifiedMessage(role="assistant", content=[TextContent(text="Dear Sam, sorry about that.")])
    assert apply_prefill_to_reply([ok], plan)["starts_with_prefill"] is True
    off = UnifiedMessage(role="assistant", content=[TextContent(text="Hi Sam, sorry about that.")])
    rec = apply_prefill_to_reply([off], plan)
    assert rec["forced"] is False and rec["starts_with_prefill"] is False


# ── Anthropic translator ────────────────────────────────────────────────────


def _anthropic(messages: list[UnifiedMessage], system: str | None = "You draft support replies for Northwind Outfitters.") -> dict:
    config = UnifiedConfig(model="claude-haiku-4-5", system_instruction=system, messages=MessageList(_messages=messages))
    return AnthropicTranslator().to_anthropic(config, make_profile(model_name="claude-haiku-4-5", wire_format="anthropic_chat"))


def _breakpoints(request: dict) -> int:
    n = sum(1 for b in request.get("system") or [] if isinstance(b, dict) and "cache_control" in b)
    for m in request["messages"]:
        n += sum(1 for b in m["content"] if isinstance(b, dict) and "cache_control" in b)
    return n


def test_cache_boundary_puts_a_breakpoint_on_that_messages_last_block() -> None:
    request = _anthropic(_drafter(prefill=False))
    example_answer = request["messages"][1]
    assert example_answer["role"] == "assistant"
    assert example_answer["content"][-1]["cache_control"] == {"type": "ephemeral"}
    # the unflagged first example carries none
    assert "cache_control" not in request["messages"][0]["content"][-1]


def test_trailing_prefill_is_sent_as_the_prefill_without_trailing_space() -> None:
    request = _anthropic(_drafter(prefill=True))
    last = request["messages"][-1]
    assert last["role"] == "assistant" and last["content"][-1]["text"] == "Dear"
    # rolling breakpoint sits on the user turn before the prefill
    assert request["messages"][-2]["content"][-1].get("cache_control") == {"type": "ephemeral"}
    assert "cache_control" not in last["content"][-1]


def test_unflagged_terminal_assistant_is_still_refused() -> None:
    with pytest.raises(MessageSanitizationError):
        _anthropic([_msg("user", CUSTOMER), _msg("assistant", "Dear")])


def test_breakpoints_never_exceed_four() -> None:
    msgs = []
    for i in range(5):
        msgs.append(_msg("user", f"Example complaint {i}", example=True, cache_boundary=True))
        msgs.append(_msg("assistant", f"Dear customer {i}, ...", example=True))
    msgs.append(_msg("user", CUSTOMER))
    request = _anthropic(msgs)
    assert _breakpoints(request) == 4
    # the LATEST boundary survives
    assert request["messages"][8]["content"][-1].get("cache_control") == {"type": "ephemeral"}


def test_refusal_is_not_retried_and_keeps_its_sentence() -> None:
    from matrx_ai.providers.errors import classify_internal_error

    try:
        plan_message_flags(_drafter(), supports_prefill=False, cache_boundary_support="breakpoint", model_label="claude-sonnet-5")
    except MessageFlagRefusal as exc:
        classified = classify_internal_error(exc, "anthropic")
    assert classified is not None and classified.is_retryable is False
    assert classified.error_type == "prefill_unsupported"
    assert "claude-sonnet-5 cannot continue a reply from a prefill" in (classified.user_message or "")

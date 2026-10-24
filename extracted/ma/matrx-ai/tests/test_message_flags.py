"""Message FLAGS — prefill, example (typed-messages FEATURE.md, Flag row).

Each test names the real use: a support-reply drafter whose system prompt is
cached, whose two example exchanges are few-shot turns, and whose reply must
start "Dear". The translators decide the wire; a flag a model cannot honor is
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
        _msg("assistant", "Dear Priya, I'm sorry your order arrived late and damaged...", example=True),
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
    assert parse_flags({"example": False, "prefill": True}) == {"prefill": True}


def test_retired_cache_boundary_flag_is_refused() -> None:
    # Retired 2026-10-16: the platform places every cache mark (config/cache_marks.py).
    with pytest.raises(InvalidMessageFlags):
        parse_flags({"cache_boundary": True})


def test_placement_rules() -> None:
    system = {"role": "system", "content": [{"type": "text", "text": "You draft support replies."}]}
    user = {"role": "user", "content": [{"type": "text", "text": CUSTOMER}]}
    prefill = {"role": "assistant", "content": [{"type": "text", "text": "Dear"}], "flags": {"prefill": True}}
    validate_message_flags([system, user, prefill])

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
    plan = plan_message_flags(_drafter(), supports_prefill=True, model_label="claude-haiku-4-5")
    assert plan.prefill_mode == "native" and plan.prefill_text == "Dear"
    assert len(plan.wire_messages) == 4
    assert plan.examples == 2 and plan.notes == []


def test_refuse_names_the_model_before_any_spend() -> None:
    with pytest.raises(MessageFlagRefusal, match="claude-sonnet-5 cannot continue a reply from a prefill"):
        plan_message_flags(_drafter(), supports_prefill=False, model_label="claude-sonnet-5", mode="refuse")


def test_default_is_convert_so_a_prefill_never_fails_every_run() -> None:
    # 2026-10-17: "Support reply drafter" (claude-haiku-5-5, authored prefill) failed
    # EVERY run with prefill_unsupported. With no org mode set the run must go ahead:
    # the prefill rides as an instruction and the plan carries the announcement.
    plan = plan_message_flags(_drafter(), supports_prefill=False, model_label="claude-haiku-5-5")
    assert plan.prefill_mode == "convert"
    assert plan.wire_messages[-1].role == "user"
    assert any("claude-haiku-5-5 cannot take a prefill" in n for n in plan.notes)
    # an unreadable / unknown org value also lands on convert, not a failed run
    assert plan_message_flags(
        _drafter(), supports_prefill=False, model_label="m", mode="garbage"
    ).prefill_mode == "convert"


def test_a_model_that_ignores_the_instruction_is_recorded_not_hidden() -> None:
    plan = plan_message_flags(_drafter(), supports_prefill=False, model_label="claude-haiku-5-5")
    reply = _msg("assistant", "Hello Priya, sorry about the screen protector.")
    record = apply_prefill_to_reply([reply], plan)
    assert record and record["forced"] is False and record["starts_with_prefill"] is False
    assert plan.prefill_model_label == "claude-haiku-5-5"
    ok = _msg("assistant", "Dear Priya, sorry about the screen protector.")
    plan2 = plan_message_flags(_drafter(), supports_prefill=False, model_label="m")
    assert apply_prefill_to_reply([ok], plan2)["starts_with_prefill"] is True  # type: ignore[index]


def test_finish_announces_a_non_compliant_convert() -> None:
    import asyncio
    from types import SimpleNamespace
    from unittest.mock import AsyncMock, patch

    from matrx_ai.providers import unified_client as uc

    plan = plan_message_flags(_drafter(), supports_prefill=False, model_label="claude-haiku-5-5")
    response = SimpleNamespace(messages=[_msg("assistant", "Hi Priya, sorry.")])

    async def run() -> AsyncMock:
        with patch.object(uc, "_announce_flag_notes", new=AsyncMock()) as announce:
            uc._finish_message_flags(response, plan)
            await asyncio.sleep(0)
            return announce

    announce = asyncio.run(run())
    announce.assert_awaited_once()
    assert "did not begin its reply" in announce.await_args.args[0][0]


@pytest.mark.parametrize("caller", ["awaited_prepare", "detached_finish"])
def test_flag_notice_failure_is_captured_without_failing_the_call(caller: str) -> None:
    import asyncio
    from types import SimpleNamespace

    from matrx_connect.context import AppContext, clear_app_context, set_app_context
    from matrx_utils import configure_error_capture
    import matrx_utils.error_capture as error_capture_module
    from matrx_ai.providers import unified_client as uc

    class _FailingEmitter:
        async def send_info(self, _payload) -> None:
            raise RuntimeError("notice transport unavailable")

    captured: list[tuple[BaseException, dict]] = []
    old_sink = error_capture_module._sink
    old_allow = error_capture_module._allow_in_tests

    async def _sink(exc: BaseException, **kwargs) -> None:
        captured.append((exc, kwargs))

    async def _run() -> None:
        app_context_token = set_app_context(AppContext(emitter=_FailingEmitter()))
        configure_error_capture(_sink, allow_in_tests=True)
        try:
            if caller == "awaited_prepare":
                messages = MessageList(_drafter())
                config = SimpleNamespace(messages=messages, metadata={}, stream=False)
                wire_config = SimpleNamespace(messages=MessageList(_drafter()))
                plan = await uc._apply_message_flags(
                    wire_config,
                    config,
                    make_profile(model_name="claude-haiku-5-5"),
                    "anthropic_chat",
                )
                assert plan is not None
            else:
                plan = plan_message_flags(
                    _drafter(), supports_prefill=False, model_label="claude-haiku-5-5"
                )
                response = SimpleNamespace(messages=[_msg("assistant", "Hi Priya, sorry.")])
                uc._finish_message_flags(response, plan)
                await asyncio.sleep(0.02)
        finally:
            configure_error_capture(old_sink, allow_in_tests=old_allow)
            clear_app_context(app_context_token)

    asyncio.run(_run())
    assert len(captured) == 1
    exc, fields = captured[0]
    assert str(exc) == "notice transport unavailable"
    assert fields["kind"] == "provider_flag_note_emit_failed"
    assert fields["context"] == {
        "source_app": "matrx-ai",
        "source_feature": "providers.unified_client",
        "code": "message_flag_adjusted",
    }


def test_convert_asks_for_the_start_and_says_so() -> None:
    plan = plan_message_flags(_drafter(), supports_prefill=False, model_label="gpt-5", mode="convert")
    assert plan.prefill_mode == "convert"
    assert len(plan.wire_messages) == 3 and plan.wire_messages[-1].role == "user"
    assert "Begin your reply with exactly" in (plan.convert_instruction or "")
    assert any("asked for, not forced" in n for n in plan.notes)


def test_drop_mode_announces_it() -> None:
    plan = plan_message_flags(_drafter(), supports_prefill=False, model_label="gemini-3-pro", mode="drop")
    assert plan.prefill_mode == "drop" and len(plan.wire_messages) == 3
    assert any("was not sent" in n for n in plan.notes)


def test_a_consumed_prefill_never_reaches_a_wire_again() -> None:
    history = _drafter() + [_msg("assistant", "Dear Sam, a replacement is on its way."), _msg("user", "Thanks! Can it ship express?")]
    plan = plan_message_flags(history, supports_prefill=False, model_label="claude-sonnet-5")
    assert plan.prefill_mode is None
    assert all(not flags_of(m).get("prefill") for m in plan.wire_messages)


def test_native_reply_is_stored_whole() -> None:
    plan = plan_message_flags(_drafter(), supports_prefill=True, model_label="claude-haiku-4-5")
    reply = UnifiedMessage(role="assistant", content=[TextContent(text=" Sam, I'm sorry about the cracked protector.")])
    record = apply_prefill_to_reply([reply], plan)
    assert reply.content[0].text.startswith("Dear Sam")
    assert record == {"mode": "native", "text": "Dear", "forced": True, "starts_with_prefill": True}
    assert reply.metadata["prefill"]["mode"] == "native"


def test_converted_reply_records_whether_it_complied() -> None:
    plan = plan_message_flags(_drafter(), supports_prefill=False, model_label="claude-sonnet-5", mode="convert")
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


def test_refusal_is_not_retried_and_keeps_its_sentence() -> None:
    from matrx_ai.providers.errors import classify_internal_error

    try:
        plan_message_flags(_drafter(), supports_prefill=False, model_label="claude-sonnet-5", mode="refuse")
    except MessageFlagRefusal as exc:
        classified = classify_internal_error(exc, "anthropic")
    assert classified is not None and classified.is_retryable is False
    assert classified.error_type == "prefill_unsupported"
    assert "claude-sonnet-5 cannot continue a reply from a prefill" in (classified.user_message or "")

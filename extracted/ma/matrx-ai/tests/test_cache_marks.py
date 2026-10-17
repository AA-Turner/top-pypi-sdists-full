"""Prompt cache marks — the platform's own (config/cache_marks.py).

The real use: a support-reply drafter whose system prompt and two authored example
exchanges never change, followed by an authored request that carries the customer's
name as a variable, then whatever the person types. Repeat runs should read the
system + examples from cache; only the filled and typed tail is new.
"""

from __future__ import annotations

from matrx_ai.config import MessageList, UnifiedConfig, UnifiedMessage
TEMPLATE_METADATA_KEY = "cache_template"  # config/cache_marks.py; a literal so a pre-change tree fails per test
from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.providers.anthropic import translator as anthropic_translator
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile

SYSTEM = "You draft support replies for Northwind Outfitters. Warm, short, specific."
ONE_HOUR = {"type": "ephemeral", "ttl": "1h"}
FIVE_MIN = {"type": "ephemeral"}


def _msg(role: str, text: str) -> UnifiedMessage:
    return UnifiedMessage.from_dict({"role": role, "content": [{"type": "text", "text": text}]})


def _drafter_config(*, long_cache: bool) -> UnifiedConfig:
    messages = [
        _msg("user", "Order arrived two days late and the box was crushed."),
        _msg("assistant", "Dear Priya, I'm sorry your order arrived late and damaged..."),
        _msg("user", "Write the reply for {{customer_name}}."),
    ]
    return UnifiedConfig(
        model="claude-haiku-4-5",
        system_instruction=SYSTEM,
        messages=MessageList(_messages=messages),
        extended_prompt_cache=long_cache,
    )


def _run(config: UnifiedConfig, *, typed: str | None = None) -> dict:
    """First turn exactly as a door runs it: fill the authored template, then the typed turn joins."""
    config.replace_variables({"customer_name": "Tomas Okafor"})
    if typed is not None:
        config.messages.append(_msg("user", typed))
    return AnthropicTranslator().to_anthropic(
        config, make_profile(model_name="claude-haiku-4-5", wire_format="anthropic_chat")
    )


def _marks(request: dict) -> list[tuple[str, int, dict]]:
    out: list[tuple[str, int, dict]] = []
    for i, b in enumerate(request.get("system") or []):
        if isinstance(b, dict) and "cache_control" in b:
            out.append(("system", i, b["cache_control"]))
    for i, m in enumerate(request["messages"]):
        for b in m["content"]:
            if isinstance(b, dict) and "cache_control" in b:
                out.append(("message", i, b["cache_control"]))
    return out


# ── the long cache reaches the Anthropic wire ───────────────────────────────


def test_long_cache_puts_the_one_hour_ttl_on_the_system_and_template_marks() -> None:
    request = _run(_drafter_config(long_cache=True), typed="Please mention the free return label.")
    assert request["system"][0]["cache_control"] == ONE_HOUR
    marks = _marks(request)
    # system (1h), template on the authored example answer (1h), rolling on the last turn (5m)
    assert marks == [("system", 0, ONE_HOUR), ("message", 1, ONE_HOUR), ("message", 2, FIVE_MIN)]


def test_without_long_cache_every_mark_is_the_five_minute_default() -> None:
    request = _run(_drafter_config(long_cache=False), typed="Please mention the free return label.")
    assert all(cc == FIVE_MIN for _, _, cc in _marks(request))


# ── the automatic template mark ─────────────────────────────────────────────


def test_template_mark_sits_after_the_last_authored_message_the_fill_left_unchanged() -> None:
    config = _drafter_config(long_cache=False)
    request = _run(config, typed="Please mention the free return label.")
    stamps = [m.metadata.get(TEMPLATE_METADATA_KEY) for m in config.messages]
    assert stamps == ["stable", "stable", "filled", None]
    # wire: [user example, assistant example, filled request + typed turn merged into one user turn]
    assert request["messages"][1]["role"] == "assistant"
    assert "cache_control" in request["messages"][1]["content"][-1]
    assert "cache_control" not in request["messages"][0]["content"][-1]


def test_with_no_variables_the_template_mark_is_the_end_of_the_authored_messages() -> None:
    config = UnifiedConfig(
        model="claude-haiku-4-5",
        system_instruction=SYSTEM,
        messages=MessageList(
            _messages=[
                _msg("user", "Order arrived two days late and the box was crushed."),
                _msg("assistant", "Dear Priya, I'm sorry your order arrived late and damaged..."),
            ]
        ),
    )
    config.replace_variables({})
    config.messages.append(_msg("user", "My jacket zipper broke after a week."))
    request = AnthropicTranslator().to_anthropic(
        config, make_profile(model_name="claude-haiku-4-5", wire_format="anthropic_chat")
    )
    assert [(kind, i) for kind, i, _ in _marks(request)] == [("system", 0), ("message", 1), ("message", 2)]


def test_a_conversation_with_no_authored_template_gets_no_template_mark() -> None:
    config = UnifiedConfig(
        model="claude-haiku-4-5",
        system_instruction=SYSTEM,
        messages=MessageList(_messages=[_msg("user", "hi"), _msg("assistant", "Hello!"), _msg("user", "Help")]),
    )
    request = AnthropicTranslator().to_anthropic(
        config, make_profile(model_name="claude-haiku-4-5", wire_format="anthropic_chat")
    )
    assert [(kind, i) for kind, i, _ in _marks(request)] == [("system", 0), ("message", 2)]


# ── the 4-mark ceiling is announced, never silent ───────────────────────────


def test_marks_past_four_are_dropped_earliest_first_and_said(monkeypatch) -> None:
    said: list[str] = []
    monkeypatch.setattr(anthropic_translator, "note_capture", said.append)
    cc = {"type": "ephemeral"}
    request = {"system": [{"type": "text", "text": SYSTEM, "cache_control": cc}]}
    messages = [
        {"role": "user", "content": [{"type": "text", "text": f"turn {i}", "cache_control": cc}]}
        for i in range(4)
    ]
    dropped = AnthropicTranslator._enforce_breakpoint_ceiling(request, messages, None)
    assert dropped == 1
    assert "cache_control" not in messages[0]["content"][0]
    assert all("cache_control" in m["content"][0] for m in messages[1:])
    assert said and "at most 4" in said[0]


# ── cache writes are recorded ───────────────────────────────────────────────


def test_cache_writes_are_read_from_each_providers_usage() -> None:
    anthropic = TokenUsage(
        input_tokens=200,
        output_tokens=50,
        cached_input_tokens=1800,
        matrx_model_name="claude-haiku-4-5",
        api="anthropic",
        raw_usage={
            "input_tokens": 200,
            "cache_read_input_tokens": 1800,
            "cache_creation_input_tokens": 2400,
            "cache_creation": {"ephemeral_5m_input_tokens": 400, "ephemeral_1h_input_tokens": 2000},
        },
    )
    openai = TokenUsage(
        input_tokens=900,
        output_tokens=10,
        matrx_model_name="gpt-5",
        api="openai",
        raw_usage={"input_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 1536}},
    )
    assert anthropic.cache_write_tokens == 2400
    assert openai.cache_write_tokens == 1536


def test_the_request_row_carries_cache_write_tokens() -> None:
    from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
    from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

    usage = TokenUsage(
        input_tokens=200,
        output_tokens=50,
        cached_input_tokens=1800,
        matrx_model_name="claude-haiku-4-5",
        api="anthropic",
        raw_usage={"input_tokens": 200, "cache_read_input_tokens": 1800, "cache_creation_input_tokens": 2400},
    )
    token = set_app_context(AppContext(emitter=None, user_id="u1"))
    try:
        config = UnifiedConfig(model="claude-haiku-4-5", messages=[{"role": "user", "content": "hi"}])
        req = AIMatrixRequest(conversation_id="c1", config=config, usage_history=[usage])
        row = CompletedRequest(request=req, iterations=1, final_response=None).to_storage_dict()["requests"][0]
    finally:
        clear_app_context(token)
    assert row["cache_write_tokens"] == 2400
    assert row["cached_tokens"] == 1800

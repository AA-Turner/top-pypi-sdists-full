"""Always-warm prompt cache: the Anthropic layout for an enrolled agent (providers/prompt_warm.py).

The prefix every conversation of an enrolled agent shares must be byte-identical across
conversations, days and users: block A (the agent's own authored text) leads the system
channel with a 1-hour mark; the date line and skills preamble move behind it (block B).
"""

from __future__ import annotations

import re
from typing import Any

import pytest

from matrx_ai.config import UnifiedConfig
from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_ai.providers import prompt_warm
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.unified_client import _build_provider_wire_config
from matrx_ai.testing.profile_factory import make_profile

AGENT = "6b6b4e45-4699-4860-8dea-d8a60e07d69a"
ONE_HOUR = {"type": "ephemeral", "ttl": "1h"}
AUTHORED = "You are General Chat. " + "Be precise and kind. " * 40


def _system(date: str, skills: int) -> str:
    return (
        f"<!--matrx:current_date-->Current date: {date}\n\n"
        f"<available_skills>{'s' * skills}</available_skills>\n\n" + AUTHORED
    )


@pytest.fixture(autouse=True)
def _enrolled():
    profiles = {AGENT: prompt_warm.WarmProfile(shared_text=AUTHORED.rstrip(), prompt_chars=len(AUTHORED))}
    seen: list[prompt_warm.WarmObservation] = []
    prompt_warm.configure_prompt_warm(profiles.get, seen.append)
    token = set_app_context(AppContext(emitter=None, user_id="u1", agent_id=AGENT, conversation_id="c1"))
    yield seen
    clear_app_context(token)
    prompt_warm.configure_prompt_warm(None, None)
    prompt_warm.take_layout()


def _wire(
    system: str,
    *,
    tools: list[dict[str, Any]] | None = None,
    dynamic: list[str] | None = None,
    authored: list[str] | None = None,
) -> dict:
    config = UnifiedConfig.from_dict(
        {
            "model": "claude-opus-5-5",
            "system_instruction": system,
            "messages": [{"role": "user", "content": [{"type": "text", "text": "Hello there."}]}],
            "dynamic_tools": dynamic or [],
            "authored_tools": authored or [],
        }
    )
    profile = make_profile(model_name="claude-opus-5-5", wire_format="anthropic_chat")
    translator = AnthropicTranslator()
    if tools is not None:
        translator.build_provider_tools = lambda _config, _provider: [dict(t) for t in tools]  # type: ignore[method-assign]
    return translator.to_anthropic(_build_provider_wire_config(config, profile), profile)


def _marks(request: dict) -> list[tuple[str, dict]]:
    out: list[tuple[str, dict]] = []
    for t in request.get("tools") or []:
        if "cache_control" in t:
            out.append(("tool", t["cache_control"]))
    for b in request.get("system") if isinstance(request.get("system"), list) else []:
        if "cache_control" in b:
            out.append(("system", b["cache_control"]))
    for m in request["messages"]:
        for b in m["content"] if isinstance(m["content"], list) else []:
            if isinstance(b, dict) and "cache_control" in b:
                out.append(("message", b["cache_control"]))
    return out


def _date_blocks(request: dict) -> list[str]:
    text = "".join(b["text"] for b in request["system"])
    return re.findall(r"<!--matrx:current_date-->Current date: (\d{4}-\d{2}-\d{2})", text)


def test_the_agents_own_text_leads_the_system_channel_with_a_one_hour_mark() -> None:
    request = _wire(_system("2026-11-15", 1721))
    system = request["system"]
    assert system[0]["text"] == AUTHORED.rstrip()
    assert system[0]["cache_control"] == ONE_HOUR
    # The date block leads block B; its digits are the send's pinned date (any day this runs).
    assert re.match(r"<!--matrx:current_date-->Current date: \d{4}-\d{2}-\d{2}", system[1]["text"])
    assert AUTHORED.rstrip() not in system[1]["text"]


@pytest.mark.parametrize("own_date", ["2026-11-15", "2031-01-02"])
def test_an_agents_own_date_block_is_replaced_never_doubled(own_date: str) -> None:
    """Live 2026-11-17: text that already opened its own date block (no closing marker) reached the
    provider with a SECOND, freshly rendered date block in front of it. One date block, always."""
    request = _wire(_system(own_date, 1721))
    assert len(_date_blocks(request)) == 1, _date_blocks(request)


def test_the_prefix_key_is_the_same_across_days_and_users() -> None:
    _wire(_system("2026-11-15", 1721))
    first = prompt_warm.take_layout()
    _wire(_system("2026-11-16", 1775))
    second = prompt_warm.take_layout()
    assert first is not None and second is not None and first.applied and second.applied
    assert first.variant_key == second.variant_key
    assert first.prefix_text == second.prefix_text
    assert '"ttl":"1h"' in first.prefix_text


def test_a_system_prompt_without_the_agents_text_is_left_alone_as_a_layout_miss() -> None:
    request = _wire("<!--matrx:current_date-->Current date: 2026-11-15\n\nSomething else entirely.")
    layout = prompt_warm.take_layout()
    assert layout is not None and layout.applied is False and layout.variant_key == ""
    assert len(request["system"]) == 1


def test_authored_tools_get_a_one_hour_mark_when_dynamic_tools_follow() -> None:
    tools = [{"name": n, "input_schema": {"type": "object"}} for n in ("memory", "web", "bundle__list_google")]
    request = _wire(_system("2026-11-15", 10), tools=tools, dynamic=["bundle:list_google"], authored=["memory", "web"])
    assert request["tools"][1]["cache_control"] == ONE_HOUR
    assert "cache_control" not in request["tools"][0]
    assert "cache_control" not in request["tools"][2]


def test_a_surface_tool_that_is_not_dynamic_still_ends_the_authored_run() -> None:
    """A platform tool that arrives with the request (an app surface's tools) is not ``dynamic`` but
    is not the agent's own either: the 1h mark closes the authored run before it."""
    tools = [{"name": n, "input_schema": {"type": "object"}} for n in ("memory", "web", "apply_surface_write")]
    request = _wire(_system("2026-11-15", 10), tools=tools, authored=["memory", "web"])
    assert request["tools"][1]["cache_control"] == ONE_HOUR
    assert "cache_control" not in request["tools"][2]


def test_no_tool_mark_when_every_tool_is_authored() -> None:
    tools = [{"name": n, "input_schema": {"type": "object"}} for n in ("memory", "web")]
    request = _wire(_system("2026-11-15", 10), tools=tools, authored=["memory", "web"])
    assert not any("cache_control" in t for t in request["tools"])


def test_the_ceiling_is_four_and_every_one_hour_mark_precedes_every_five_minute_mark() -> None:
    tools = [{"name": n, "input_schema": {"type": "object"}} for n in ("memory", "web", "bundle__list_google")]
    request = _wire(_system("2026-11-15", 10), tools=tools, dynamic=["bundle:list_google"], authored=["memory", "web"])
    marks = _marks(request)
    assert len(marks) <= 4
    ttls = [m[1].get("ttl", "5m") for m in marks]
    assert ttls == sorted(ttls, key=lambda t: 0 if t == "1h" else 1), marks


def test_the_ceiling_drops_block_bs_mark_first_then_the_tool_mark() -> None:
    request = {
        "model": "m",
        "tools": [{"name": "a"}, {"name": "b"}, {"name": "dyn"}],
        "system": [],
    }
    messages = [
        {"role": "user", "content": [{"type": "text", "text": "x", "cache_control": ONE_HOUR}]},
        {"role": "user", "content": [{"type": "text", "text": "y", "cache_control": {"type": "ephemeral"}}]},
    ]
    profile = prompt_warm.WarmProfile(shared_text="SHARED")
    layout = prompt_warm.apply_warm_layout(
        request, messages, agent_id=AGENT, profile=profile, system_text="date\nSHARED\ntail", authored_run=2
    )
    assert layout.marks_dropped == ["system_rest"]
    assert "cache_control" not in request["system"][1]
    assert request["tools"][1]["cache_control"] == ONE_HOUR
    messages[0]["content"].append({"type": "text", "text": "z", "cache_control": ONE_HOUR})
    request2 = {"model": "m", "tools": [{"name": "a"}, {"name": "dyn"}], "system": []}
    layout2 = prompt_warm.apply_warm_layout(
        request2, messages, agent_id=AGENT, profile=profile, system_text="SHARED tail", authored_run=1
    )
    assert layout2.marks_dropped == ["system_rest", "authored_tools"]
    assert request2["system"][0]["cache_control"] == ONE_HOUR


def test_an_unenrolled_agent_is_untouched() -> None:
    prompt_warm.configure_prompt_warm(lambda _id: None, None)
    request = _wire(_system("2026-11-15", 10))
    assert len(request["system"]) == 1
    assert prompt_warm.take_layout() is None


def test_shared_text_is_cut_at_the_first_variable() -> None:
    assert prompt_warm.shared_text_from_authored("Lead text.\n\nUse {{name}} here.", ["name"]) == "Lead text.\n\nUse"
    assert prompt_warm.shared_text_from_authored("No variables.") == "No variables."


def test_only_a_declared_slot_cuts_and_escapes_are_shared_as_sent() -> None:
    """THE VARIABLE RULE: an undeclared {{x}} is left as written and an escape {{!x}} is sent as {{x}}, so both
    belong to the shared text; only a DECLARED slot (or its section / block) varies per run."""
    teaching = "Reference variables with {{!variable_name}}. Keep {{undeclared}} as is.\n\nPurpose: {{purpose}} end."
    shared = prompt_warm.shared_text_from_authored(teaching, ["purpose"])
    assert shared == "Reference variables with {{variable_name}}. Keep {{undeclared}} as is.\n\nPurpose:"
    assert prompt_warm.shared_text_from_authored("A {{#purpose}}x{{/purpose}}", ["purpose"]) == "A"
    assert prompt_warm.shared_text_from_authored("All {{!x}} shared.", []) == "All {{x}} shared."


def test_the_keepalive_replays_the_prefix_with_zero_output() -> None:
    _wire(_system("2026-11-15", 10))
    layout = prompt_warm.take_layout()
    assert layout is not None
    payload = prompt_warm.keepalive_payload(layout.prefix_text)
    assert payload["max_tokens"] == 0
    assert payload["messages"] == [{"role": "user", "content": prompt_warm.KEEPALIVE_TEXT}]
    assert payload["system"][0]["text"] == AUTHORED.rstrip()
    assert "stream" not in payload and "format" not in (payload.get("output_config") or {})


def test_usage_numbers_split_the_write_tiers() -> None:
    numbers = prompt_warm.usage_numbers(
        {
            "input_tokens": 12,
            "cache_read_input_tokens": 30000,
            "cache_creation_input_tokens": 500,
            "cache_creation": {"ephemeral_5m_input_tokens": 200, "ephemeral_1h_input_tokens": 300},
        }
    )
    assert numbers == {
        "input_tokens": 12,
        "output_tokens": 0,
        "cache_read_tokens": 30000,
        "cache_write_5m_tokens": 200,
        "cache_write_1h_tokens": 300,
    }


def test_a_failing_profile_reader_never_breaks_the_send() -> None:
    def boom(_agent_id: str) -> prompt_warm.WarmProfile:
        raise RuntimeError("db down")

    prompt_warm.configure_prompt_warm(boom, None)
    request = _wire(_system("2026-11-15", 10))
    assert len(request["system"]) == 1


def test_a_send_while_the_prompt_is_still_loading_is_recorded_with_its_reason(_enrolled) -> None:
    """An enrolled agent whose prompt this process has not loaded yet must still leave a trace:
    the send goes out unwarmed (no 1h marks) and is observed as a layout miss naming why."""
    reason = "still loading"
    prompt_warm.configure_prompt_warm(
        lambda _id: prompt_warm.WarmProfile(shared_text="", pending_reason=reason), _enrolled.append
    )
    request = _wire(_system("2026-11-15", 10))
    assert len(request["system"]) == 1
    assert request["system"][0]["cache_control"] == {"type": "ephemeral"}
    layout = prompt_warm.take_layout()
    assert layout is not None and not layout.applied and layout.miss_reason == reason
    prompt_warm.observe(layout, kind=prompt_warm.KIND_LIVE, usage={"input_tokens": 5})
    assert _enrolled[-1].applied is False and _enrolled[-1].miss_reason == reason


@pytest.mark.asyncio
async def test_the_keepalive_prepares_the_provider_client_before_touching_it(monkeypatch) -> None:
    """Live 2026-11-15: touching the SDK client cold on the event loop raised on every keep-alive. The send must
    run the same preflight every unified dispatch runs before it reads ``.client``."""
    order: list[str] = []

    class _Usage:
        def model_dump(self) -> dict:
            return {"cache_read_input_tokens": 7}

    class _Messages:
        async def create(self, **_payload: Any) -> Any:
            order.append("create")
            return type("R", (), {"usage": _Usage()})()

    class _Chat:
        @property
        def client(self) -> Any:
            assert "prepare" in order, "client touched before prepare_provider_clients"
            return type("C", (), {"messages": _Messages()})()

    async def _prepare(_instance: Any) -> None:
        order.append("prepare")

    monkeypatch.setattr(prompt_warm, "_KEEPALIVE_CHAT", _Chat())
    monkeypatch.setattr("matrx_ai.providers.keys.prepare_provider_clients", _prepare)
    monkeypatch.setattr("matrx_ai.providers.guardrail_gate.admit_call_spend_cap", lambda *_a: None)
    _wire(_system("2026-11-15", 10))
    layout = prompt_warm.take_layout()
    numbers = await prompt_warm.send_keepalive(layout.prefix_text)
    assert order == ["prepare", "create"] and numbers["cache_read_tokens"] == 7

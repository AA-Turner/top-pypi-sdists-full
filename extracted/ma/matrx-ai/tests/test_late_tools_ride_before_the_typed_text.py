"""LATE TOOLS never ride AFTER the person's typed text (THE REQUEST ENDS WITH WHAT THE PERSON TYPED).

Live guard ``scripts/check_request_ends_with_typed_text.py`` (2026-11-18): 10 anthropic sends in 24 h
ended with a ``<late_tools>`` user turn after her words (conversation 3af9e95c): the translator's
trailing channel appended the block even when the send boundary had placed this turn's platform
block before her typed text. Now the boundary stages the late tools in that block
(``late_tools.LATE_TOOLS_SLOT``, ``send_boundary._stage_late_tools``): frozen with the turn, so the
next send of the loop replays it byte for byte (the cache line holds), and a tool that turns late
mid-loop rides the tail after the tool result as the slot's current copy.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.cache_plan import configure_prompt_cache_knobs
from matrx_ai.config.message_config import ToolCallContent, ToolResultContent
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_ai.providers import late_tools
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.testing.profile_factory import make_profile
from matrx_ai.tools import declaration_ledger
from matrx_ai.tools import registry as registry_module
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType
from matrx_ai.tools.registry import ToolRegistry

TYPED = "And my three most recent documents — what are they called?"
MARK = "<live_date>It is now 09:00.</live_date>"
AUTHORED = ["memory", "use_tool"]


async def _probe(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    return ToolResult(success=True, output={"ok": True}, tool_name=ctx.tool_name, call_id=ctx.call_id)


def _definition(name: str) -> ToolDefinition:
    return ToolDefinition(
        name=name,
        description=f"The {name} tool.",
        parameters={"q": {"type": "string", "description": "A query.", "required": True}},
        tool_type=ToolType.LOCAL,
        function_path=f"{__name__}._probe",
    )


@pytest.fixture(autouse=True)
def registry(monkeypatch: pytest.MonkeyPatch) -> Any:
    reg = ToolRegistry()
    reg.load_from_definitions([_definition(n) for n in (*AUTHORED, "late_calendar_probe", "late_notes_probe")])
    reg._loaded = True
    monkeypatch.setattr(registry_module.ToolRegistry, "_instance", reg)
    late_tools.reset_for_tests()
    declaration_ledger.reset_for_tests()
    configure_prompt_cache_knobs(
        lambda key: {"late_tools_enabled": True, "late_tools_scope": "all"}[key]
    )
    token = set_app_context(AppContext(emitter=None, user_id="u1"))
    yield reg
    clear_app_context(token)
    declaration_ledger.reset_for_tests()
    late_tools.reset_for_tests()
    configure_prompt_cache_knobs(None)


def _config(dynamic: list[str]) -> UnifiedConfig:
    history = [
        UnifiedMessage(role="user", content=[TextContent(text="What is on tomorrow?")], id="m1", position=0),
        UnifiedMessage(role="assistant", content=[TextContent(text="Nothing is on tomorrow.")], id="m2", position=1),
    ]
    config = UnifiedConfig(model="m", messages=MessageList(_messages=history))
    config.system_instruction = "You are a careful assistant. " * 40
    config.tools = [*AUTHORED, *dynamic]
    config.authored_tools = list(AUTHORED)
    config.dynamic_tools = list(dynamic)
    config.messages.append_or_extend_user_input(TYPED)
    config.messages.attach_turn_context(MARK, slot="live_date")
    return config


def _send(config: UnifiedConfig) -> dict[str, Any]:
    profile = make_profile(model_name="claude-opus-5-5", wire_format="anthropic_chat")
    prep = order_for_wire(config, profile)
    return AnthropicTranslator().build_request(prep.wire_config if prep.wire_config is not None else config, profile)


def _texts(message: dict[str, Any]) -> list[str]:
    content = message["content"]
    return [content] if isinstance(content, str) else [b.get("text") or "" for b in content if isinstance(b, dict)]


def _strip_marks(messages: list[dict[str, Any]]) -> list[Any]:
    return [
        {**m, "content": [{k: v for k, v in b.items() if k != "cache_control"} for b in m["content"]]}
        if isinstance(m["content"], list)
        else m
        for m in messages
    ]


def test_the_person_turn_send_ends_with_her_typed_text_and_carries_the_late_tools_before_it() -> None:
    request = _send(_config(["late_calendar_probe"]))
    last = request["messages"][-1]
    assert last["role"] == "user"
    texts = _texts(last)
    assert texts[-1].rstrip().endswith(TYPED), f"the request does not end with her words: {texts[-1][-200:]!r}"
    before = "\n".join(texts[:-1])
    assert "<late_tools>" in before and "### late_calendar_probe" in before and MARK in before
    wire = repr(request["messages"])
    assert wire.count("<late_tools>") == 1, "the late tools rode twice"
    assert "late_calendar_probe" not in [t.get("name") for t in request["tools"]]


def test_the_next_send_of_the_loop_replays_the_same_prefix_and_trails_only_a_newly_late_tool() -> None:
    config = _config(["late_calendar_probe"])
    first = _send(config)
    turn_len = len(first["messages"])
    # The model calls a tool; the result lands; a second tool joins mid-loop.
    config.messages.append(
        UnifiedMessage(role="assistant", content=[ToolCallContent(id="c1", name="memory", arguments={"q": "x"})])
    )
    config.messages.append(
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="c1", call_id="c1", name="memory", content="done")])
    )
    config.tools = [*config.tools, "late_notes_probe"]
    config.dynamic_tools = [*config.dynamic_tools, "late_notes_probe"]
    second = _send(config)
    # Byte-identical through her turn (cache marks aside): the late block placed on her turn did not move.
    assert _strip_marks(second["messages"][:turn_len]) == _strip_marks(first["messages"])
    tail = "\n".join(t for m in second["messages"][turn_len:] for t in _texts(m))
    assert "late_notes_probe" in tail, "a tool that turned late mid-loop must ride after the tool result"
    assert repr(second["messages"]).count("### late_calendar_probe") == 1, "an already-placed late tool rode twice"


def test_a_send_with_no_person_turn_keeps_the_late_tools_in_the_trailing_channel() -> None:
    config = UnifiedConfig(
        model="m",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="Summarize the record.")])]
        ),
    )
    config.tools = [*AUTHORED, "late_calendar_probe"]
    config.authored_tools = list(AUTHORED)
    config.dynamic_tools = ["late_calendar_probe"]
    request = _send(config)
    assert "<late_tools>" in repr(request["messages"]), "late tools were lost on a system job"


def test_the_boundary_and_the_translators_agree_on_who_delivers_late_tools() -> None:
    modules = {
        "anthropic": ("matrx_ai.providers.anthropic.translator", "AnthropicTranslator"),
        "google": ("matrx_ai.providers.google.translator", "GoogleTranslator"),
        "openai": ("matrx_ai.providers.openai.translator", "OpenAITranslator"),
        "groq": ("matrx_ai.providers.groq.translator", "GroqTranslator"),
        "cerebras": ("matrx_ai.providers.cerebras.translator", "CerebrasTranslator"),
        "together": ("matrx_ai.providers.together.translator", "TogetherTranslator"),
        "generic_openai": ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator"),
        "xai": ("matrx_ai.providers.xai.translator", "XAITranslator"),
    }
    flagged = {
        provider
        for provider, (module, cls) in modules.items()
        if getattr(getattr(importlib.import_module(module), cls), "SUPPORTS_LATE_TOOLS", BaseTranslator.SUPPORTS_LATE_TOOLS)
    }
    assert flagged == set(late_tools.LATE_TOOLS_PROVIDERS)

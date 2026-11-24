"""LATE TOOLS (providers/late_tools.py): a tool added mid-conversation leaves the wire ``tools`` list
and rides AFTER the cache line as text, behind knob ``agents.prompt_cache.late_tools_enabled``.

Knob off (or its row missing): the request is exactly what it was before the feature. Knob on: the
dynamic tools are absent from ``tools``, present in the trailing block after the last cache mark,
``use_tool`` stays declared, the authored order is unchanged, and the cached prefix (tools + system)
is identical between two configs that differ only in their dynamic tools. A late tool stays callable
by its own name (the executor's allowlist is built from ``config.tools``).
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config import UnifiedConfig
from matrx_ai.config.cache_plan import configure_prompt_cache_knobs
from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_ai.providers import late_tools, prompt_warm
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.providers.groq.translator import GroqTranslator
from matrx_ai.providers.openai.translator import OpenAITranslator
from matrx_ai.providers.unified_client import _build_provider_wire_config
from matrx_ai.testing.profile_factory import make_profile
from matrx_ai.tools import declaration_ledger
from matrx_ai.tools import registry as registry_module
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType
from matrx_ai.tools.registry import ToolRegistry

SYSTEM = "You are a careful assistant. " * 60
AUTHORED = ["memory", "use_tool", "web"]
AGENT = "1f6d1a8e-7a43-4c9a-9a4e-0d1a3b6f2c11"


async def late_probe_tool(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    return ToolResult(success=True, output={"echo": args.get("city")}, tool_name=ctx.tool_name, call_id=ctx.call_id)


def _definition(name: str) -> ToolDefinition:
    return ToolDefinition(
        name=name,
        description=f"The {name} tool.",
        parameters={"city": {"type": "string", "description": "A city.", "required": True}},
        tool_type=ToolType.LOCAL,
        function_path=f"{__name__}.late_probe_tool",
    )


@pytest.fixture
def registry(monkeypatch: pytest.MonkeyPatch) -> ToolRegistry:
    reg = ToolRegistry()
    reg.load_from_definitions(
        [_definition(n) for n in (*AUTHORED, "latebundle:probe_list", "late_weather_probe", "late_zeta_probe", "late_third_probe")]
    )
    reg._loaded = True
    monkeypatch.setattr(registry_module.ToolRegistry, "_instance", reg)
    late_tools.reset_for_tests()
    declaration_ledger.reset_for_tests()
    # No conversation: the tool-declaration ledger (which keeps a declared tool for the life of a
    # conversation) must not carry another test's declarations into this one.
    token = set_app_context(AppContext(emitter=None, user_id="u1"))
    yield reg
    clear_app_context(token)
    declaration_ledger.reset_for_tests()
    late_tools.reset_for_tests()
    configure_prompt_cache_knobs(None)


def _knobs(values: dict[str, Any] | None) -> None:
    def reader(key: str) -> Any:
        if values is None or key not in values:
            raise KeyError(f"agents.prompt_cache.{key} has no row")
        return values[key]

    configure_prompt_cache_knobs(reader)


def _config(dynamic: list[str], *, tools: list[str] | None = None) -> UnifiedConfig:
    offered = tools if tools is not None else [*AUTHORED, *dynamic]
    return UnifiedConfig.from_dict(
        {
            "model": "m",
            "system_instruction": SYSTEM,
            "messages": [{"role": "user", "content": [{"type": "text", "text": "Plan my trip."}]}],
            "tools": offered,
            "authored_tools": [t for t in AUTHORED if t in offered],
            "dynamic_tools": dynamic,
        }
    )


def _anthropic(config: UnifiedConfig) -> dict[str, Any]:
    profile = make_profile(model_name="claude-opus-5-5", wire_format="anthropic_chat")
    return AnthropicTranslator().to_anthropic(_build_provider_wire_config(config, profile), profile)


def _openai(config: UnifiedConfig) -> dict[str, Any]:
    profile = make_profile(model_name="gpt-5.5", wire_format="openai_chat")
    return OpenAITranslator().to_openai(_build_provider_wire_config(config, profile), profile)


def _google(config: UnifiedConfig) -> Any:
    profile = make_profile(model_name="gemini-3.5-flash", wire_format="google_chat")
    return GoogleTranslator().to_google(_build_provider_wire_config(config, profile), profile)


def _names(tools: list[dict[str, Any]] | None) -> list[str]:
    return [t.get("name") for t in tools or [] if isinstance(t, dict) and t.get("name")]


def _last_mark_position(request: dict[str, Any]) -> int:
    last = -1
    for i, message in enumerate(request["messages"]):
        for block in message["content"] if isinstance(message["content"], list) else []:
            if isinstance(block, dict) and "cache_control" in block:
                last = i
    return last


DYNAMIC = ["latebundle:probe_list", "late_weather_probe"]


@pytest.mark.parametrize("knobs", [None, {"late_tools_enabled": False, "late_tools_scope": "all"}])
def test_knob_off_or_missing_leaves_the_request_exactly_as_before(registry: ToolRegistry, knobs: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    _knobs(knobs)
    request = _anthropic(_config(DYNAMIC))
    # The pre-feature path: the split code is skipped entirely.
    monkeypatch.setattr(BaseTranslator, "_late_tool_names", lambda self, config: [])
    before = _anthropic(_config(DYNAMIC))
    assert request == before
    assert {"latebundle__probe_list", "late_weather_probe"} <= set(_names(request["tools"]))
    assert "<late_tools>" not in repr(request)
    assert late_tools.take_late_tools() is None


def test_knob_on_moves_dynamic_tools_after_the_rolling_mark_on_anthropic(registry: ToolRegistry) -> None:
    _knobs({"late_tools_enabled": True, "late_tools_scope": "all"})
    request = _anthropic(_config(DYNAMIC))
    assert _names(request["tools"]) == AUTHORED  # authored order unchanged, use_tool declared
    host_turn = request["messages"][-1]
    text = host_turn["content"][-1]["text"]
    assert "<late_tools>" in text and "### latebundle__probe_list" in text and "### late_weather_probe" in text
    assert "call use_tool with job_key=<name> and inputs=<object>" in text
    assert '"city"' in text  # the input JSON schema rides with it
    assert _last_mark_position(request) < len(request["messages"]) - 1  # after the rolling mark
    assert not any("cache_control" in b for b in host_turn["content"])
    split = late_tools.take_late_tools()
    assert split is not None and split.names == ("latebundle__probe_list", "late_weather_probe")


def test_the_cached_prefix_is_identical_whatever_tools_joined_later(registry: ToolRegistry) -> None:
    _knobs({"late_tools_enabled": True, "late_tools_scope": "all"})
    first = _anthropic(_config(["late_weather_probe"]))
    second = _anthropic(_config(["late_weather_probe", "late_zeta_probe", "latebundle:probe_list"]))
    assert first["tools"] == second["tools"]
    assert first["system"] == second["system"]
    assert first["messages"][:-1] == second["messages"][:-1]
    assert first["messages"][-1] != second["messages"][-1]


def test_knob_on_moves_dynamic_tools_after_the_cache_line_on_openai(registry: ToolRegistry) -> None:
    _knobs({"late_tools_enabled": True, "late_tools_scope": "all"})
    request = _openai(_config(DYNAMIC))
    assert _names(request["tools"]) == AUTHORED
    last = request["input"][-1]
    assert last["role"] == "developer" and "<late_tools>" in last["content"][0]["text"]
    assert "### late_weather_probe" in last["content"][0]["text"]


def test_knob_on_moves_dynamic_tools_after_the_cache_line_on_google(registry: ToolRegistry) -> None:
    _knobs({"late_tools_enabled": True, "late_tools_scope": "all"})
    built = _google(_config(DYNAMIC))
    declared = [d.name for tool in built["config"].tools or [] for d in (tool.function_declarations or [])]
    assert declared == AUTHORED
    last = built["contents"][-1]
    assert last["role"] == "user" and "<late_tools>" in last["parts"][-1]["text"]
    assert "### latebundle__probe_list" in last["parts"][-1]["text"]


def test_scope_enrolled_skips_an_agent_outside_the_warm_cache(registry: ToolRegistry) -> None:
    _knobs({"late_tools_enabled": True, "late_tools_scope": "enrolled"})
    request = _anthropic(_config(DYNAMIC))
    assert {"latebundle__probe_list", "late_weather_probe"} <= set(_names(request["tools"]))

    profiles = {AGENT: prompt_warm.WarmProfile(shared_text="Other text entirely.", prompt_chars=20)}
    prompt_warm.configure_prompt_warm(profiles.get, None)
    token = set_app_context(AppContext(emitter=None, user_id="u1", agent_id=AGENT, conversation_id="c-late"))
    try:
        enrolled = _anthropic(_config(DYNAMIC))
    finally:
        clear_app_context(token)
        prompt_warm.configure_prompt_warm(None, None)
        prompt_warm.take_layout()
    assert _names(enrolled["tools"]) == AUTHORED


def test_no_gateway_means_no_split_and_it_is_said(registry: ToolRegistry, capsys: pytest.CaptureFixture[str]) -> None:
    _knobs({"late_tools_enabled": True, "late_tools_scope": "all"})
    request = _anthropic(_config(DYNAMIC, tools=["memory", "web", *DYNAMIC]))
    assert {"latebundle__probe_list", "late_weather_probe"} <= set(_names(request["tools"]))
    assert "<late_tools>" not in repr(request)
    assert "'use_tool' is not offered" in capsys.readouterr().out


def test_a_translator_without_the_channel_keeps_its_tools_and_says_so(registry: ToolRegistry, capsys: pytest.CaptureFixture[str]) -> None:
    _knobs({"late_tools_enabled": True, "late_tools_scope": "all"})
    profile = make_profile(model_name="openai/gpt-oss-120b", wire_format="groq_chat")
    config = _config(DYNAMIC)
    request = GroqTranslator().to_groq(_build_provider_wire_config(config, profile), profile)
    names = [t["function"]["name"] for t in request["tools"]]
    assert {"latebundle__probe_list", "late_weather_probe"} <= set(names)
    assert "<late_tools>" not in repr(request)
    assert "translator does not place late tools" in capsys.readouterr().out


@pytest.mark.asyncio
async def test_a_native_call_to_a_late_tool_runs_like_a_declared_one(registry: ToolRegistry, monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.orchestrator.executor import _resolve_allowed_tools
    from matrx_ai.persistence import queue_helpers
    from matrx_ai.tools.executor import ToolExecutor

    class _Silent:
        def prepare_metadata(self, *_a: Any, **_k: Any) -> None:
            return None

        def __getattr__(self, _name: str) -> Any:
            async def _noop(*_a: Any, **_k: Any) -> None:
                return None

            return _noop

    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    _knobs({"late_tools_enabled": True, "late_tools_scope": "all"})
    config = _config(DYNAMIC)
    request = _anthropic(config)
    assert "latebundle__probe_list" not in _names(request["tools"])
    allowed = _resolve_allowed_tools(config)
    executor = ToolExecutor(registry=registry, execution_logger=_Silent())
    seen: list[ToolContext] = []

    async def _dispatch(tool_def: Any, args: dict[str, Any], ctx: ToolContext, *a: Any, **k: Any) -> ToolResult:
        seen.append(ctx)
        return await late_probe_tool(args, ctx)

    monkeypatch.setattr(executor, "_dispatch", _dispatch)
    try:
        _, result = await executor.execute(
            "latebundle__probe_list", {"city": "Lisbon"}, ToolContext(call_id="late-1", tool_name="latebundle__probe_list"),
            allowed_tools=allowed,
        )
        _, refused = await executor.execute(
            "late_zeta_probe", {"city": "Lisbon"}, ToolContext(call_id="late-2", tool_name="late_zeta_probe"),
            allowed_tools=allowed,
        )
    finally:
        pass
    assert result.success, result.error
    assert result.output == {"echo": "Lisbon"}
    assert seen and seen[0].tool_name == "latebundle:probe_list"
    assert seen[0].allowed_tools == allowed  # the gateway reads the run's allowed set from here
    assert not refused.success and refused.error.error_type == "not_allowed"


def test_a_tool_the_conversation_already_sent_in_its_tools_list_is_never_also_a_late_tool(registry: ToolRegistry) -> None:
    """Review finding 2026-11-15: the declaration ledger keeps a sent tool in the list for the conversation's
    life (e.g. the knob was turned on mid-conversation). Such a tool must not ALSO appear in the late block."""
    token = set_app_context(AppContext(emitter=None, user_id="u1", conversation_id="c-held"))
    try:
        _knobs({"late_tools_enabled": False, "late_tools_scope": "all"})
        first = _anthropic(_config(DYNAMIC))  # knob off: dynamic tools go out in the tools list
        assert "late_weather_probe" in _names(first["tools"])
        _knobs({"late_tools_enabled": True, "late_tools_scope": "all"})
        second = _anthropic(_config(DYNAMIC))
        assert "late_weather_probe" in _names(second["tools"])  # the ledger keeps it declared
        assert "<late_tools>" not in repr(second)  # and it is not delivered a second time
        new = _anthropic(_config([*DYNAMIC, "late_third_probe"]))
        assert "late_third_probe" not in _names(new["tools"])  # a tool joining now does ride late
        assert "late_third_probe" in repr(new) and "<late_tools>" in repr(new)
    finally:
        clear_app_context(token)

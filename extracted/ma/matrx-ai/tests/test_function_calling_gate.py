"""Function-calling capability — the single source of truth + its gates.

Covers the axis that gates ALL tool / context injection:
  • ``capabilities.features`` declares ``function_calling`` on chat models and on
    no media/tts/image/video/extraction model. That is the ONLY source.
  • config.supports_tools carries the resolved flag (default permissive).
  • CANONICAL gate: merge_request_tools adds nothing when supports_tools is False
    (silent — it's doing its job).
  • FALLBACK gate: unified_client._warn_and_strip_leaked_tools strips + screams
    when a tool reaches the provider boundary for a non-function-calling model
    (a leak that should never happen).
  • The SystemInstruction decoration mechanism the non-chat path relies on.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities


def _caps(
    name: str = "m",
    *,
    input_: list[str] | None = None,
    output: list[str] | None = None,
    features: list[str] | None = None,
    interaction: str = "turn",
    multilingual: bool = False,
):
    return resolve_model_capabilities(
        SimpleNamespace(
            name=name,
            model_class=name,
            capabilities={
                "input": input_ if input_ is not None else ["text"],
                "output": output if output is not None else ["text"],
                "features": features if features is not None else [],
                "interaction": interaction,
                "multilingual": multilingual,
            },
        )
    )


_CHAT = ["function_calling", "structured_output", "json_mode"]


# ── Source of truth ─────────────────────────────────────────────────────────


def test_function_calling_is_declared_data_not_inferred():
    assert _caps("gpt-4o", features=_CHAT).supports_function_calling is True
    # A media model declares no features → no tools, ever.
    assert _caps("tts-1", output=["audio"]).supports_function_calling is False
    assert _caps("imagen", output=["image"]).supports_function_calling is False
    assert _caps("veo", output=["video"]).supports_function_calling is False
    assert (
        _caps(
            "gliner2-base", output=["entities"], interaction="extraction"
        ).supports_function_calling
        is False
    )


def test_unknown_or_missing_capabilities_has_no_function_calling():
    bare = resolve_model_capabilities(SimpleNamespace(name="mystery", capabilities=None))
    assert bare.supports_function_calling is False
    assert resolve_model_capabilities(None).supports_function_calling is False


def test_non_chat_groq_models_declare_no_function_calling():
    """STT / safety-classifier models served on the Groq chat route declare no
    function calling in their own capability data — there is no api_class default
    left to override (root cause C in the capability-reconciliation ledger)."""
    for name in (
        "whisper-large-v3",
        "distil-whisper-large-v3-en",
        "meta-llama/llama-prompt-guard-2-22m",
        "openai/gpt-oss-safeguard-20b",
    ):
        assert _caps(name).supports_function_calling is False


def test_groq_compound_systems_have_no_user_function_calling():
    """Groq compound/compound-mini ride the Groq chat route but accept no
    user-defined tools (they run built-in tools internally) — root cause F."""
    assert _caps("groq/compound").supports_function_calling is False
    assert _caps("groq/compound-mini").supports_function_calling is False


def test_gemini_image_models_carry_search_but_no_function_calling():
    """The Gemini-3 image models host Google Search grounding; they expose no user
    function calling. Both facts are per-model data, so a shared route can't blur
    them (the older gemini-2.5-flash-image sibling has neither)."""
    pro = _caps(
        "gemini-3-pro-image-preview",
        input_=["text", "image"],
        output=["image", "text"],
        features=["web_search"],
    )
    assert pro.supports_web_search is True
    assert pro.supports_function_calling is False

    sibling = _caps("gemini-2.5-flash-image", input_=["text", "image"], output=["image", "text"])
    assert sibling.supports_web_search is False


def test_gemini_omni_video_produces_video_and_audio_and_accepts_audio_input():
    """Gemini Omni Flash generates video WITH native audio and accepts audio input,
    and exposes no user function calling."""
    caps = _caps(
        "gemini-omni-flash-preview",
        input_=["text", "image", "audio", "video"],
        output=["video", "audio"],
    )
    assert caps.produces_video is True
    assert caps.produces_audio is True
    assert caps.supports_audio_input is True
    assert caps.supports_function_calling is False


def test_gemma_4_31b_is_the_one_vision_capable_cerebras_model():
    """Cerebras added native image input exclusively for gemma-4-31b. Vision is now
    capability DATA (``image`` in input), and the vision CLASS only decides how to
    re-encode the bytes: gemma-4-31b pins the OpenAI profile because Cerebras is
    OpenAI-compatible."""
    from matrx_ai.processing.vision import resolve_vision_class

    assert _caps("gemma-4-31b", input_=["text", "image"]).supports_vision is True
    assert _caps("zai-glm-4.7").supports_vision is False
    assert resolve_vision_class("gemma-4-31b", "cerebras_chat").name == "openai_high"


def test_grok_build_has_function_calling_but_no_web_search():
    """grok-build-0.1: xAI's coding model supports function calling but its model
    page lists no hosted web search."""
    m = _caps("grok-build-0.1", features=_CHAT)
    assert m.supports_function_calling is True
    assert m.supports_web_search is False


def test_realtime_voice_vs_transcription_only_capabilities():
    """A full voice realtime model (audio OUT) hosts tools + search; a
    transcription-only realtime model (text OUT) never speaks or exposes tools
    (root cause D). Both are pure declarations now."""
    voice = _caps(
        "realtime-api",
        input_=["audio", "text"],
        output=["audio", "text"],
        features=["function_calling", "web_search", "x_search"],
        interaction="realtime",
    )
    assert voice.produces_audio is True and voice.supports_function_calling is True
    assert voice.native_capabilities == frozenset({"web_search", "x_search"})

    stt = _caps("scribe_v2_realtime", input_=["audio"], output=["text"], interaction="realtime")
    assert stt.supports_audio_input is True
    assert stt.produces_audio is False and stt.supports_function_calling is False
    assert stt.native_capabilities == frozenset()


def test_unified_config_supports_tools_defaults_permissive():
    from matrx_ai.config import UnifiedConfig

    cfg = UnifiedConfig(model="x", messages=[])
    assert cfg.supports_tools is True  # unknown/unresolved → permissive


# ── CANONICAL gate: the merge primitive ─────────────────────────────────────


def test_merge_primitive_adds_nothing_when_no_function_calling():
    from matrx_ai.tools.merge import merge_request_tools
    from matrx_ai.tools.specs import RegisteredToolSpec

    cfg = SimpleNamespace(supports_tools=False, tools=[], custom_tools=[])
    sentinel_ctx = object()
    specs = [RegisteredToolSpec(name="ctx_get"), RegisteredToolSpec(name="ctx_batch")]

    out = merge_request_tools(cfg, sentinel_ctx, specs)

    assert cfg.tools == []  # the gate added nothing
    assert cfg.custom_tools == []
    assert out is sentinel_ctx  # ctx returned unchanged, no client_tools touched


def test_no_function_calling_clears_stale_routing_state_with_missing_metadata():
    from matrx_connect import AppContext

    from matrx_ai.tools.merge import merge_request_tools

    cfg = SimpleNamespace(
        supports_tools=False,
        tools=["ctx_get"],
        custom_tools=[{"name": "inline"}],
        mcp_servers=["stale-mcp"],
    )
    ctx = AppContext(emitter=None, client_tools=["ctx_get"], metadata=None)

    out = merge_request_tools(cfg, ctx, [])

    assert cfg.tools == []
    assert cfg.custom_tools == []
    assert cfg.mcp_servers == []
    assert out.client_tools == []
    assert out.metadata == {}


def test_no_function_calling_clears_capability_and_authority_metadata():
    from matrx_connect import AppContext

    from matrx_ai.tools.merge import merge_request_tools

    cfg = SimpleNamespace(
        supports_tools=False,
        tools=[],
        custom_tools=[],
        mcp_servers=[],
    )
    stale = {
        "client_capabilities_payloads": {"desktop-native": {}},
        "filesystem_authority": {"namespace": "local-machine"},
        "desktop_target_instance_id": "desktop-1",
        "active_ui_surface": "matrx-local/desktop",
        "active_tool_executors": ["matrx-local"],
        "hard_excluded_tools": ["cloud_file"],
        "unrelated": "keep",
    }
    ctx = AppContext(emitter=None, client_tools=["stale"], metadata=stale)

    out = merge_request_tools(cfg, ctx, [])

    assert out.client_tools == []
    assert out.metadata == {"unrelated": "keep"}


def test_no_function_calling_round_trip_restores_authored_tools_and_mcp():
    from matrx_connect import AppContext

    from matrx_ai.config import UnifiedConfig
    from matrx_ai.tools.merge import merge_request_tools

    cfg = UnifiedConfig(
        model="audio-model",
        messages=[],
        tools=["registered_tool"],
        custom_tools=[
            {
                "name": "inline_tool",
                "description": "fixture",
                "input_schema": {"type": "object", "properties": {}},
            }
        ],
        mcp_servers=["agent-mcp"],
        supports_tools=False,
    )

    merge_request_tools(cfg, AppContext(emitter=None), [])
    assert cfg.tools == [] and cfg.custom_tools == [] and cfg.mcp_servers == []
    assert cfg.tool_capability_filtered is True

    stored = cfg.to_storage_dict()
    restored = UnifiedConfig.from_dict(
        {
            "model": "chat-model",
            "system_instruction": stored["system_instruction"],
            "messages": stored["messages"],
            **stored["config"],
        }
    )
    assert restored.tools == []
    assert restored.mcp_servers == []
    assert restored.authored_tools == ["registered_tool"]
    assert restored.authored_mcp_servers == ["agent-mcp"]

    restored.supports_tools = True
    merge_request_tools(restored, AppContext(emitter=None), [])

    assert restored.tools == ["registered_tool"]
    assert [tool.name for tool in restored.custom_tools] == ["inline_tool"]
    assert restored.mcp_servers == ["agent-mcp"]
    assert restored.tool_capability_filtered is False

    # Request-effective MCP additions remain session-only; only the authored
    # declaration crosses the conversation storage boundary.
    restored.mcp_servers.append("request-mcp")
    stored_again = restored.to_storage_dict()
    reloaded_again = UnifiedConfig.from_dict(
        {
            "model": stored_again["model"],
            "system_instruction": stored_again["system_instruction"],
            "messages": stored_again["messages"],
            **stored_again["config"],
        }
    )
    assert reloaded_again.mcp_servers == ["agent-mcp"]


def test_unfiltered_round_trip_rehydrates_only_authored_inline_tools():
    from matrx_ai.config import UnifiedConfig

    cfg = UnifiedConfig(
        model="chat-model",
        messages=[],
        custom_tools=[
            {
                "name": "authored_inline",
                "description": "fixture",
                "input_schema": {"type": "object", "properties": {}},
            }
        ],
    )
    # A request-effective addition must not become authored persistence.
    cfg.custom_tools.append(
        type(cfg.custom_tools[0])(
            name="request_inline",
            description="request fixture",
            input_schema={"type": "object", "properties": {}},
        )
    )

    stored = cfg.to_storage_dict()
    restored = UnifiedConfig.from_dict(
        {
            "model": stored["model"],
            "system_instruction": stored["system_instruction"],
            "messages": stored["messages"],
            **stored["config"],
        }
    )

    assert [tool.name for tool in restored.custom_tools] == ["authored_inline"]


# ── FALLBACK gate: the provider boundary ────────────────────────────────────


def test_provider_fallback_strips_full_tool_surface_for_non_fc_model():
    from matrx_ai.providers.unified_client import _warn_and_strip_leaked_tools

    cfg = SimpleNamespace(
        tools=["ctx_get"],
        custom_tools=[{"name": "x"}],
        mcp_servers=["some-mcp"],
        internal_url_context=True,
        model="some-tts",
    )
    _warn_and_strip_leaked_tools(cfg, _caps("some-tts", output=["audio"]))
    # The ENTIRE tool surface is stripped, not just config.tools.
    assert cfg.tools == [] and cfg.custom_tools == []
    assert cfg.mcp_servers == [] and cfg.internal_url_context is None


def test_provider_fallback_is_noop_for_chat_model():
    from matrx_ai.providers.unified_client import _warn_and_strip_leaked_tools

    cfg = SimpleNamespace(
        tools=["ctx_get"],
        custom_tools=[{"name": "x"}],
        mcp_servers=["m"],
        internal_url_context=True,
        model="gpt",
    )
    _warn_and_strip_leaked_tools(cfg, _caps("gpt", features=_CHAT))
    # A function-calling model keeps its whole surface — the fallback only guards leaks.
    assert cfg.tools == ["ctx_get"] and cfg.custom_tools == [{"name": "x"}]
    assert cfg.mcp_servers == ["m"] and cfg.internal_url_context is True


# ── Decorations: the SINGLE dispatch gate that covers every path ────────────


def test_strip_chat_decorations_method():
    from matrx_ai.instructions.core import SystemInstruction

    si = SystemInstruction(
        base_instruction="Read this aloud:",
        include_date=True,
        tools_list=["ctx_get"],
        include_code_guidelines=True,
        include_context_block=True,
    )
    assert "Current date:" in str(si)
    si.strip_chat_decorations()
    assert si.include_date is False and si.tools_list == []
    assert si.include_code_guidelines is False and si.include_context_block is False
    rendered = str(si)
    assert "Current date:" not in rendered
    assert "Read this aloud:" in rendered  # the agent's own directive survives


def test_system_instruction_round_trips_include_context_block():
    """The agent-builder toggle persists: from_value reads include_context_block
    (default True), so a creator can turn the context-awareness block off."""
    from matrx_ai.instructions.core import SystemInstruction

    assert SystemInstruction.from_value({"base_instruction": "hi"}).include_context_block is True
    off = SystemInstruction.from_value({"base_instruction": "hi", "include_context_block": False})
    assert off.include_context_block is False


def test_dispatch_decoration_gate_covers_non_fc_only():
    """_strip_chat_decorations_if_non_fc is the single render-point gate — it must
    clean a non-chat model's instruction on ANY path (incl. NamedAgent.run) and
    leave a chat model's alone."""
    from matrx_ai.instructions.core import SystemInstruction
    from matrx_ai.providers.unified_client import _strip_chat_decorations_if_non_fc

    tts_cfg = SimpleNamespace(
        system_instruction=SystemInstruction(base_instruction="Read aloud:", include_date=True)
    )
    _strip_chat_decorations_if_non_fc(
        tts_cfg, _caps("gemini-2.5-flash-preview-tts", output=["audio"])
    )
    assert tts_cfg.system_instruction.include_date is False
    assert "Current date:" not in str(tts_cfg.system_instruction)

    chat_cfg = SimpleNamespace(
        system_instruction=SystemInstruction(base_instruction="Help:", include_date=True)
    )
    _strip_chat_decorations_if_non_fc(chat_cfg, _caps("gemini-2.5-flash", features=_CHAT))
    assert chat_cfg.system_instruction.include_date is True  # untouched for chat

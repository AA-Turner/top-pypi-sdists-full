"""
Unified AI API System for OpenAI, Anthropic, and Google Gemini
Preserves ALL content types and metadata from all providers
"""

from __future__ import annotations

import asyncio
import threading
from copy import copy
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

from matrx_ai.config import UnifiedResponse

# IMPORT SAFETY — do NOT import ai_model_manager (or anything else that resolves
# host-injected DB models) at module scope. ``matrx_ai.db.ai_models`` resolves
# ``get_model("AiModel")`` when its impl loads, which raises DBNotConfiguredError
# in a CLIENT host (matrx-local). The manager is resolved lazily at CALL time
# (see ``UnifiedAIClient.__getattr__``), mirroring the lazy pattern in
# ``orchestrator/executor.py``. Config errors surface at call time, never import.
#
# AIMatrixRequest is an ANNOTATION-ONLY dependency here. Importing it at
# runtime puts matrx_ai.orchestrator into the providers import closure — the
# structural edge behind the providers ↔ orchestrator circular-import class
# matrx-local hit cold-importing matrx_ai.providers. TYPE_CHECKING only.
if TYPE_CHECKING:
    from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.providers.resolved_capabilities import (
    ResolvedModelCapabilities,
    StructuredOutputMode,
)

# ============================================================================
# UNIFIED CLIENT
# ============================================================================

# The wire_format of the ONE service whose provider rejects hosted web search
# paired with legacy JSON mode. OpenAI 400s the pairing; Structured Outputs
# (json_schema) does not have the limitation.
_WEB_SEARCH_JSON_MODE_CONFLICT_WIRE_FORMAT = "openai_chat"

# These OpenAI-compatible Chat endpoints advertise BOTH function calling and
# structured output as individual capabilities, but reject the pair in one
# request. This is a wire-level cross-field constraint, not a model-capability
# lie: either feature works on its own. Keep the machine-consumed output
# contract and drop the lower-priority enrichment tools when the two collide.
_TOOL_STRUCTURED_OUTPUT_CONFLICT_WIRE_FORMATS = frozenset({"cerebras_chat", "groq_chat"})


def _build_provider_wire_config(config: Any, profile: Any) -> Any:
    # ``UnifiedConfig.model`` is durable conversation state and must retain the
    # canonical reference. Provider ids are per-call transport details.
    wire_config = copy(config)
    wire_config.model = profile.provider_model_id
    wire_config.matrx_model_name = profile.model_name
    return wire_config


def _downgrade_response_format(
    config: Any, caps: ResolvedModelCapabilities, wire_format: str
) -> None:
    """Downgrade ``config.response_format`` to the best mode the model supports.

    json_schema → json_object → text, driven by the model's declared
    ``structured_output_mode``. Mutates ``config.response_format`` in place when a
    downgrade is needed and logs it loudly — a runtime ADJUSTMENT to keep
    limited/older models working, never a persisted setting. No-op when the model
    already supports the requested mode.
    """
    rf = getattr(config, "response_format", None)
    if not isinstance(rf, dict):
        return
    rf_type = rf.get("type")
    if rf_type not in ("json_schema", "json_object"):
        return

    mode = caps.structured_output_mode
    target: str | None = None
    if rf_type == "json_schema" and mode is not StructuredOutputMode.SCHEMA:
        target = "json_object" if mode is StructuredOutputMode.JSON else "text"
    elif rf_type == "json_object" and mode is StructuredOutputMode.TEXT:
        target = "text"
    if target is None:
        return

    vcprint(
        data={
            "model": caps.model_name,
            "wire_format": wire_format,
            "structured_output_mode": mode.value,
            "requested": rf,
            "downgraded_to": target,
        },
        title=(
            f"⚠️  CAPABILITY ADJUSTMENT [{caps.model_name}]: response_format "
            f"{rf_type} → {target} — this model does not support {rf_type}. Output "
            "is downgraded to the best supported mode; the schema is NOT enforced "
            "at the provider. Do NOT persist this as a saved config — pick a model "
            "whose capabilities declare structured_output."
        ),
        color="yellow",
        verbose=True,
    )
    config.response_format = {"type": target}


def _warn_and_strip_unsupported_search(
    config: Any, caps: ResolvedModelCapabilities, wire_format: str
) -> None:
    """Drop provider-native search flags a model can't honour, loudly.

    Both flags map 1:1 onto a member of the model's declared
    ``native_capabilities`` (the SET of provider-hosted tools):

    - ``internal_x_search`` → ``x_search``. Native X/Twitter search is an xAI Grok
      feature; on every other model the flag is meaningless.
    - ``internal_web_search`` → ``web_search`` (OpenAI web_search_preview, xAI live
      search, Google googleSearch). Sending the tool to a model that doesn't host it
      400s the whole request (e.g. "Tool 'web_search_preview' is not supported with
      gpt-4.1-nano-2025-04-14"), so it is dropped here rather than left for the API.

    Both strip in place and emit a loud yellow banner so a caller knows their
    request was adjusted, never silently ignored. Mirrors the response_format
    downgrade pattern above.
    """
    if getattr(config, "internal_x_search", None) and "x_search" not in caps.native_capabilities:
        vcprint(
            data={
                "model": caps.model_name,
                "wire_format": wire_format,
                "dropped": "internal_x_search",
            },
            title=(
                f"⚠️  CAPABILITY ADJUSTMENT [{caps.model_name}]: internal_x_search "
                "dropped — native X (Twitter) search is an xAI-Grok-only hosted tool "
                "and this model does not declare it. The flag is ignored."
            ),
            color="yellow",
            verbose=True,
        )
        config.internal_x_search = None

    if getattr(config, "internal_web_search", None) and not caps.supports_web_search:
        vcprint(
            data={
                "model": caps.model_name,
                "wire_format": wire_format,
                "dropped": "internal_web_search",
            },
            title=(
                f"⚠️  CAPABILITY ADJUSTMENT [{caps.model_name}]: internal_web_search "
                "dropped — this model does not host the web-search tool. The flag is "
                "ignored so the request doesn't 400. Use a web-search-capable model "
                "(e.g. gpt-4o / gpt-4.1 / gpt-5.x, a Grok model, or a Gemini model)."
            ),
            color="yellow",
            verbose=True,
        )
        config.internal_web_search = None


def _resolve_web_search_json_mode_conflict(
    config: Any, caps: ResolvedModelCapabilities, wire_format: str
) -> None:
    """Drop hosted web search when it collides with OpenAI JSON mode, loudly.

    OpenAI rejects a request that pairs the hosted web-search tool with legacy
    JSON mode (``response_format={"type": "json_object"}``) — "Web Search cannot
    be used with JSON mode." Structured Outputs (``json_schema``) does NOT have
    this limitation. The caller explicitly asked for JSON, so we keep the JSON
    contract and drop web search (the lower-priority enrichment) rather than let
    the whole turn 400 and discard the response.

    Must run AFTER ``_downgrade_response_format`` so it sees the FINAL
    response_format — a ``json_schema`` request downgraded to ``json_object`` for a
    JSON-mode-only model collides too. Strips in place + emits a loud banner so the
    adjustment is never silent. Mirrors the patterns above.
    """
    if wire_format != _WEB_SEARCH_JSON_MODE_CONFLICT_WIRE_FORMAT:
        return
    if not getattr(config, "internal_web_search", None):
        return
    rf = getattr(config, "response_format", None)
    if not isinstance(rf, dict) or rf.get("type") != "json_object":
        return

    vcprint(
        data={
            "model": caps.model_name,
            "wire_format": wire_format,
            "dropped": "internal_web_search",
            "response_format": rf,
        },
        title=(
            f"⚠️  CAPABILITY ADJUSTMENT [{caps.model_name}]: internal_web_search dropped "
            "— OpenAI does not allow the hosted web-search tool together with JSON "
            "mode (response_format json_object). The JSON output contract is kept "
            "and web search is dropped so the request doesn't 400. To combine web "
            "search with JSON, use Structured Outputs (json_schema) instead of JSON "
            "mode."
        ),
        color="yellow",
        verbose=True,
    )
    config.internal_web_search = None


def _resolve_tool_structured_output_conflict(
    config: Any, caps: ResolvedModelCapabilities, wire_format: str
) -> None:
    if wire_format not in _TOOL_STRUCTURED_OUTPUT_CONFLICT_WIRE_FORMATS:
        return
    rf = getattr(config, "response_format", None)
    if not isinstance(rf, dict) or rf.get("type") not in ("json_object", "json_schema"):
        return

    registered = list(getattr(config, "tools", None) or [])
    inline = list(getattr(config, "custom_tools", None) or [])
    mcp_servers = list(getattr(config, "mcp_servers", None) or [])
    if not (registered or inline or mcp_servers):
        return

    from matrx_ai.tools.merge import filter_tool_surface_for_unsupported_model

    filter_tool_surface_for_unsupported_model(config)
    vcprint(
        data={
            "model": caps.model_name,
            "wire_format": wire_format,
            "dropped_registered_tools": registered,
            "dropped_inline_tools": [getattr(tool, "name", "?") for tool in inline],
            "dropped_mcp_servers": mcp_servers,
            "kept_response_format": rf,
        },
        title=(
            f"⚠️  CAPABILITY ADJUSTMENT [{caps.model_name}]: tools dropped to "
            f"honour {rf['type']} — {wire_format} rejects tools combined with "
            "structured output. The output contract is kept so the request does "
            "not fail. If this run requires tools, bind it to an offering that "
            "supports the combination."
        ),
        color="yellow",
        verbose=True,
    )


def _warn_and_strip_leaked_tools(config: Any, caps: ResolvedModelCapabilities) -> None:
    """FALLBACK guard — tools must NEVER reach a non-function-calling model.

    This is NOT the canonical place tools are gated. Tools are gated canonically
    at request-prep: ``config.supports_tools`` (resolved from the capability seam)
    drives ``apply_unified_tools`` / ``merge_request_tools`` /
    ``apply_context_objects``, which simply never add tools for a model with no
    function calling. That is those gates doing their job, silently.

    This function is the final structural check at the provider boundary. If tools
    are STILL on the config here for a model that declares no function calling, a
    canonical gate was bypassed — a regression. So unlike the canonical "CAPABILITY
    ADJUSTMENT" notices above, this one screams "LEAK": it must be impossible to
    miss so the regression is caught instantly, before it 400s production. We strip
    (so the in-flight request survives) AND shout.
    """
    if caps.supports_function_calling:
        return  # canonical case — this model supports tools; nothing to guard

    # The full tool surface a non-function-calling model must never carry. Tools
    # 400 a chat-style request; mcp_servers + internal_url_context are latent
    # (un-wired today) but would leak the same way the moment they're consumed.
    stripped: list[str] = []
    if getattr(config, "tools", None):
        stripped.append(f"{len(config.tools)} registered")
    if getattr(config, "custom_tools", None):
        stripped.append(f"{len(config.custom_tools)} inline")
    if getattr(config, "mcp_servers", None):
        stripped.append(f"{len(config.mcp_servers)} mcp_server(s)")
    if getattr(config, "internal_url_context", None):
        stripped.append("internal_url_context")
    if not stripped:
        return  # the canonical gates did their job — no leak, no noise
    vcprint(
        data={
            "model": caps.model_name,
            "stripped": stripped,
        },
        title=(
            f"🚨 CAPABILITY LEAK [{caps.model_name}]: tool surface ({', '.join(stripped)}) "
            "reached the provider boundary for a model with NO function calling. A "
            "canonical injection gate (config.supports_tools → apply_unified_tools / "
            "merge_request_tools / apply_context_objects) was BYPASSED — this is a "
            "regression that should never happen. Stripping now so the request does "
            "not 400, but the upstream gate must be fixed."
        ),
        color="yellow",
        verbose=True,
    )
    from matrx_ai.tools.merge import filter_tool_surface_for_unsupported_model

    filter_tool_surface_for_unsupported_model(config)
    config.internal_url_context = None


def _strip_chat_decorations_if_non_fc(config: Any, caps: ResolvedModelCapabilities) -> None:
    """CANONICAL (silent) — a non-chat model gets a clean system instruction.

    The chat-only auto-decorations (the "Current date: …" line, tools-available
    list, code/safety guidelines, context-awareness block) render HERE, at
    dispatch (get_system_text → SystemInstruction.__str__). For a TTS model they'd
    be SPOKEN; for image/video they'd be baked into the generation prompt. This is
    the single, model-agnostic place they are gated, so it covers EVERY dispatch
    path — the HTTP routes AND the internal NamedAgent.run / scheduled-runner
    family that never touches apply_unified_tools. The agent's own directive
    survives. Silent: the render point deciding what to render is its job, not a
    leak.
    """
    from matrx_ai.instructions.core import SystemInstruction

    if caps.supports_function_calling:
        return
    si = getattr(config, "system_instruction", None)
    if isinstance(si, SystemInstruction):
        si.strip_chat_decorations()


# The one TTS wire route whose provider ships a NATIVE pronunciation dictionary
# (pronunciation_dictionary_locators) — higher quality than rewriting the text.
_NATIVE_DICTIONARY_WIRE_FORMAT = "elevenlabs_chat"


def _apply_tts_aliases_for_non_native(
    config: Any, caps: ResolvedModelCapabilities, wire_format: str
) -> None:
    """Universal cross-provider pronunciation for TTS providers WITHOUT a native
    dictionary feature (Google, xAI, OpenAI, Groq). ElevenLabs is skipped — it
    gets the dictionary natively via pronunciation_dictionary_locators, which is
    higher quality than rewriting the text. CANONICAL chokepoint: covers every
    dispatch path (HTTP routes AND internal NamedAgent.run / scheduled runners).

    Rewrites each spoken text segment in place via DictionaryConfig.apply_aliases
    (word-bounded, case-insensitive). No-op when there's no dictionary or it
    carries no spoken forms.

    "A TTS model" is audio as the ONLY output — a model that also emits video or
    images (Gemini Omni Flash) is a media generator whose prompt must not be
    rewritten for pronunciation.
    """
    is_tts = caps.produces_audio and not caps.produces_video and not caps.produces_image
    if not is_tts or wire_format == _NATIVE_DICTIONARY_WIRE_FORMAT:
        return
    raw = getattr(config, "dictionary", None)
    if not raw:
        return
    from matrx_ai.config.dictionary_config import DictionaryConfig

    cfg = DictionaryConfig.coerce(raw)
    if cfg is None or cfg.is_empty:
        return
    for msg in getattr(config, "messages", None) or []:
        for c in getattr(msg, "content", None) or []:
            text = getattr(c, "text", None)
            if isinstance(text, str) and text:
                new_text = cfg.apply_aliases(text)
                if new_text != text:
                    c.text = new_text


# ---------------------------------------------------------------------------
# Generic-OpenAI instance registry (Phase 3a)
# ---------------------------------------------------------------------------
#
# Hosts that need to plug in local OpenAI-compatible servers (llama-server,
# Ollama, vLLM, LocalAI, etc.) register their pre-configured
# ``GenericOpenAIChat`` instances by canonical model name. The
# ``UnifiedAIClient.execute()`` dispatch branch for the
# ``generic_openai_chat`` endpoint looks them up at call time.
#
# Pattern:
#
#     from matrx_ai.providers import GenericOpenAIChat
#     from matrx_ai.providers.unified_client import register_generic_openai_instance
#
#     local = GenericOpenAIChat(base_url="http://127.0.0.1:8088/v1", api_key="not-needed")
#     register_generic_openai_instance("llama_cpp/qwen2.5-vl-7b", local)
#     register_generic_openai_instance("default", local)  # optional fallback
#
# Lookup order in ``execute()``:
#   1. Exact model_name match in ``_generic_openai_instances``
#   2. "default" entry in ``_generic_openai_instances``
#   3. ``self.huggingface_chat`` (the legacy singleton path)
#
# matrx-local uses this to make local llama-server / Ollama models work
# transparently through ``UnifiedAIClient.execute()`` without forking.

_generic_openai_instances: dict[str, Any] = {}


def register_generic_openai_instance(
    name: str,
    instance: Any,
) -> None:
    """Register a ``GenericOpenAIChat`` instance by name.

    Args:
        name: Canonical model name (e.g. ``"llama_cpp/qwen2.5-vl-7b"``)
            OR the literal string ``"default"`` to register a fallback
            used when no exact-name match is found.
        instance: Pre-configured ``GenericOpenAIChat`` (or subclass)
            with ``base_url`` + ``api_key`` already wired.

    The dispatch routes purely by ``name``. Idempotent: calling twice with the
    same ``name`` replaces the instance silently.
    """
    _generic_openai_instances[name] = instance


def unregister_generic_openai_instance(name: str) -> None:
    """Remove a previously-registered instance. No-op when absent."""
    _generic_openai_instances.pop(name, None)


def get_generic_openai_instance(name: str) -> Any | None:
    """Return the registered instance for ``name`` or ``None`` if absent.

    Hosts can use this to inspect the registry (e.g. status routes that
    show which local models are currently mounted)."""
    return _generic_openai_instances.get(name)


# Process-wide cache of provider sub-clients, keyed by attribute name. Provider
# SDK clients are explicitly designed to be constructed ONCE and reused — they
# hold an httpx connection pool whose whole purpose is keep-alive / low TTFT,
# and several SDKs warn that repeatedly reconstructing them degrades
# performance (Cerebras README: "If you are repeatedly reconstructing the SDK
# instance it will lead to poor performance. It is recommended that you
# construct the SDK once and reuse the instance"). UnifiedAIClient is otherwise
# built per request, so without this cache every request rebuilt all of them.
# The aidream process runs a single event loop for its lifetime, so a shared
# pool is safe; a test that needs an isolated stub assigns it on its own
# UnifiedAIClient instance (instance attribute shadows __getattr__).
_provider_client_cache: dict[str, Any] = {}
_provider_client_cache_lock = threading.Lock()


def reset_provider_client_cache() -> None:
    """Drop all cached provider clients (test isolation / forced rebuild)."""
    _provider_client_cache.clear()


class UnifiedAIClient:
    """Unified client for all AI providers.

    Provider sub-clients are constructed LAZILY, cached PROCESS-WIDE, and reused
    across requests. Async dispatch resolves a cold client through
    ``_get_provider_client`` so SDK import and construction run off the event loop.

    Two failure modes this design eliminates:

    1. **Event-loop stalls from blocking constructors.** Some provider SDKs do
       BLOCKING network I/O in their constructor (``AsyncCerebras.__init__``
       issues a synchronous ``GET /v1/tcp_warming``). Eager construction made an
       OpenAI-only request pay that ~2s synchronous freeze just to build a
       Cerebras client it never used. Lazy construction means a request only
       ever builds the provider it actually dispatches to; thread isolation means
       that first build does not freeze unrelated requests.
    2. **Per-request reconstruction.** Rebuilding the SDK client every request
       throws away the warm httpx connection pool and inflates TTFT. The shared
       cache keeps each provider's pool alive for the process lifetime.
    """

    # attribute name -> factory symbol exported from ``matrx_ai.providers``
    _PROVIDER_FACTORIES: dict[str, str] = {
        "google_chat": "GoogleChat",
        "google_image": "GoogleImageGeneration",
        "google_interactions": "GoogleInteractionsVideoGeneration",
        "google_video": "GoogleVideoGeneration",
        "openai_chat": "OpenAIChat",
        "openai_image": "OpenAIImageGeneration",
        "openai_video": "OpenAIVideoGeneration",
        "anthropic_chat": "AnthropicChat",
        "cerebras_chat": "CerebrasChat",
        "together_chat": "TogetherChat",
        "together_image": "TogetherImageGeneration",
        "together_video": "TogetherVideoGeneration",
        "replicate_image": "ReplicateImageGeneration",
        "replicate_video": "ReplicateVideoGeneration",
        "groq_chat": "GroqChat",
        "groq_stt": "GroqSTT",
        "xai_chat": "XAIChat",
        "xai_image": "XAIImageGeneration",
        "xai_video": "XAIVideoGeneration",
        "huggingface_chat": "HuggingFaceChat",
        "elevenlabs_chat": "ElevenLabsChat",
        "mock_chat": "MockChat",
        "moonshot_chat": "MoonshotChat",
    }

    # The dispatch attr for OpenAI-compatible endpoints resolved from the
    # host-populated ``_generic_openai_instances`` registry (keyed by MODEL NAME,
    # not by wire route), so it has no entry in _PROVIDER_FACTORIES.
    _GENERIC_OPENAI_CLIENT_ATTR = "generic_openai_chat"

    def __init__(self):
        # ``model_manager`` is intentionally NOT bound here — resolving it
        # imports ``matrx_ai.db.ai_models`` which requires host DB config.
        # It is materialised lazily via ``__getattr__`` on first access.
        pass

    def __getattr__(self, name: str) -> Any:
        # Only invoked when ``name`` is not already set on the instance, so a
        # client cached on the instance is returned by normal lookup without
        # re-entry here.
        if name == "model_manager":
            from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance

            object.__setattr__(self, "model_manager", ai_model_manager_instance)
            return ai_model_manager_instance
        factory_name = type(self)._PROVIDER_FACTORIES.get(name)
        if factory_name is None:
            raise AttributeError(f"{type(self).__name__!r} object has no attribute {name!r}")
        instance = self._build_provider_client(name, factory_name)
        # Also bind on the instance so repeat access skips __getattr__ entirely.
        object.__setattr__(self, name, instance)
        return instance

    @staticmethod
    def _build_provider_client(name: str, factory_name: str) -> Any:
        instance = _provider_client_cache.get(name)
        if instance is not None:
            return instance
        with _provider_client_cache_lock:
            instance = _provider_client_cache.get(name)
            if instance is not None:
                return instance
            if factory_name == "GroqSTT":
                from matrx_ai.processing.audio.groq_transcription import GroqSTT

                instance = GroqSTT()
            else:
                import matrx_ai.providers as providers_mod

                instance = getattr(providers_mod, factory_name)()
            _provider_client_cache[name] = instance
            return instance

    async def _get_provider_client(self, name: str) -> Any:
        instance = self.__dict__.get(name)
        if instance is not None:
            return instance
        instance = _provider_client_cache.get(name)
        if instance is None:
            factory_name = type(self)._PROVIDER_FACTORIES[name]
            instance = await asyncio.to_thread(
                self._build_provider_client,
                name,
                factory_name,
            )
        object.__setattr__(self, name, instance)
        return instance

    async def execute(
        self,
        request: AIMatrixRequest,
    ) -> dict[str, Any]:
        from matrx_ai.catalog.resolve import resolve_tts_call_profile
        from matrx_ai.processing.audio.audio_preprocessing import (
            preprocess_audio_in_messages,
            should_preprocess_audio,
        )

        config = request.config
        debug = request.debug

        # The catalog resolves EVERYTHING about this call in one shot: which client
        # to dispatch to (client_attr), what model id goes on the wire
        # (provider_model_id), what the model can do (capabilities), how its controls
        # translate, and what it costs. A model with no available ai.offering raises
        # here — loudly, never a silent legacy fallback. The offering pin
        # (config.offering_id, or the runtime sibling-fallback pin when the
        # overload reroute set one) resolves EXACTLY that offering or raises.
        profile = await resolve_tts_call_profile(
            config.model,
            getattr(config, "tts_quality", None),
            offering_id=getattr(config, "routing_offering_id", None),
        )

        model_name = profile.model_name
        caps = profile.capabilities
        wire_format = profile.wire_format

        # Some callers (page extraction) require the physical PDF/document
        # rather than a best-effort text conversion. Enforce that policy as
        # soon as the actual route is known: both the extraction early-return
        # and media fallback below otherwise bypass the document resolver's
        # later guard, especially after a sibling-offering overload reroute.
        _enforce_required_native_document_input(
            config.messages,
            config=config,
            model_name=model_name,
            wire_format=wire_format,
            supports_vision=caps.supports_vision,
        )

        # Information-extraction models (GLiNER2 / Fastino) are not chat models,
        # but an agent CAN be assigned one (e.g. the GLiNER NER A/B agents). When
        # that happens we don't ride the chat dispatch — we run the span
        # extractor and synthesize a normal assistant turn (entities-as-JSON) so
        # the rest of the orchestrator (persistence, usage, STRUCTURED_OUTPUT
        # emission, completion, UI streaming) works identically to any chat
        # agent. The labels/threshold the extractor needs ride on
        # ``config.metadata['extraction']`` (baked into the agent's settings).
        #
        # INVARIANT (defends the capability gates below): this early-return runs
        # BEFORE the non-FC decoration/tool gates. That is safe ONLY because
        # _execute_extraction forwards NOTHING from config.tools / custom_tools /
        # mcp_servers / system_instruction to the provider — it passes only the
        # last user text + the extraction labels/threshold. If you ever extend it
        # to forward the config, move this return to AFTER the two gate calls
        # below (or call them here) so an extraction model can't leak either.
        if caps.interaction == "extraction" or profile.client_attr == "extraction":
            return self._stamp_offering_usage(
                await self._dispatch_with_billing_net(
                    lambda: self._execute_extraction(config, wire_format, model_name, debug),
                    profile=profile,
                ),
                profile,
                config,
            )

        # Realtime sessions and embeddings resolve through the same catalog but
        # have dedicated execution runtimes. Reject them before chat-specific
        # preprocessing so a misplaced model selection cannot mutate the request
        # and fail later as an opaque missing-provider dispatch.
        specialized_channel = profile.client_attr
        if caps.interaction in ("realtime", "embedding") or specialized_channel in (
            "realtime",
            "embedding",
            "stt",
        ):
            channel = (
                caps.interaction
                if caps.interaction in ("realtime", "embedding")
                else specialized_channel
            )
            destination = (
                "the realtime session/token-broker path"
                if channel == "realtime"
                else (
                    "the embedding provider path"
                    if channel == "embedding"
                    else "the transcription provider path"
                )
            )
            raise ValueError(
                f"Model {model_name!r} uses the {channel!r} execution channel "
                f"(wire_format={wire_format!r}) and cannot run through "
                f"UnifiedAIClient.execute(); route it through {destination}."
            )

        # Media fallback: convert any media this provider/model can't accept
        # (e.g. extract a PDF to text) BEFORE dispatch, emitting an inline stream
        # notice + a loud log for each. Conversion failure is terminal: continuing
        # would let provider serializers silently omit media while answering as if
        # they had seen it.
        from matrx_ai.processing.media_fallback import preprocess_unsupported_media

        config.messages, _media_usage = await preprocess_unsupported_media(
            config.messages,
            wire_format,
            model_name=model_name,
            model_supports_vision=caps.supports_vision,
            debug=debug,
        )
        for _u in _media_usage:
            request.add_usage(_u)

        # Check if audio needs transcription (either explicitly requested or the
        # model doesn't accept audio input)
        if should_preprocess_audio(config.messages, supports_audio_input=caps.supports_audio_input):
            if debug:
                if caps.supports_audio_input:
                    vcprint(
                        "Audio auto-transcription explicitly enabled - preprocessing messages",
                        "Unified Client",
                        color="cyan",
                    )
                else:
                    vcprint(
                        f"Model '{model_name}' doesn't accept audio - auto-transcribing as fallback",
                        "Unified Client",
                        color="yellow",
                    )

            config.messages, transcription_usage_list = await preprocess_audio_in_messages(
                config.messages,
                debug=debug,
                supports_audio_input=caps.supports_audio_input,
            )

            # Add transcription usage to request history
            for usage in transcription_usage_list:
                request.add_usage(usage)
                if debug:
                    vcprint(
                        f"Tracked catalog transcription: {usage.metadata.get('duration_seconds', 0):.1f}s "
                        f"({usage.metadata.get('billed_duration', 0):.1f}s billed)",
                        "Usage Tracking",
                        color="blue",
                    )

        # Structured-output capability gate — downgrade response_format to the best
        # mode this model actually declares (json_schema → json_object → text). A
        # runtime ADJUSTMENT, logged loudly, never persisted. Fixes e.g. small Groq
        # models that 400 on json_schema.
        _downgrade_response_format(config, caps, wire_format)

        # Strip provider-native search flags this model can't honour
        # (internal_x_search / internal_web_search vs the model's hosted-tool set).
        # Loud, never silent.
        _warn_and_strip_unsupported_search(config, caps, wire_format)

        # OpenAI rejects hosted web search + legacy JSON mode (json_object).
        # Runs AFTER the response_format downgrade so it sees the final mode;
        # keeps the JSON contract and drops web search rather than 400.
        _resolve_web_search_json_mode_conflict(config, caps, wire_format)

        # Cerebras/Groq each support tools and structured output independently,
        # but reject the pair in one Chat request. Resolve that cross-field
        # endpoint constraint here, after output-mode negotiation and before
        # translator assembly. Keep the machine-consumed output contract.
        _resolve_tool_structured_output_conflict(config, caps, wire_format)

        # Non-chat model → clean system instruction (no date / tools-list /
        # guidelines / context block). CANONICAL + silent: decorations render at
        # dispatch, so this single check covers EVERY path — including the internal
        # NamedAgent.run / scheduled runners that never hit apply_unified_tools.
        _strip_chat_decorations_if_non_fc(config, caps)

        # Cross-provider pronunciation: for non-ElevenLabs TTS, rewrite the spoken
        # text via the dictionary's alias substitution (ElevenLabs uses native
        # locators instead). Single canonical chokepoint for every dispatch path.
        _apply_tts_aliases_for_non_native(config, caps, wire_format)

        # FALLBACK guard (not the canonical gate): tools are gated at request-prep
        # via config.supports_tools. If any reached here on a non-function-calling
        # model, a canonical gate was bypassed — scream + strip so it can't 400
        # production and the regression is caught instantly.
        _warn_and_strip_leaked_tools(config, caps)

        # Resolve server-generated media refs added by tool results mid-loop.
        # Images additionally receive the target model's vision variant;
        # documents are resolved as their original bytes.
        await self._annotate_and_resolve_image_refs(
            config.messages,
            model_name=model_name,
            wire_format=wire_format,
            supports_vision=caps.supports_vision,
            require_native_document_input=bool(
                getattr(config, "metadata", {}).get("require_native_document_input", False)
                if isinstance(getattr(config, "metadata", None), dict)
                else False
            ),
            debug=debug,
        )

        # Media URL resolution does NOT happen here for client-supplied
        # media. It happens at AI Dream's boundary via
        # ``normalize_request_body``
        # (aidream/services/media_resolvers/request_normalizer.py).
        # By the time messages reach the
        # provider, every client-side MediaRef has is_resolved=True and
        # either base64_data or a fetchable URL set. Server-generated
        # refs (tool results) hit the annotate+resolve pass above.
        # Defense-in-depth: any downstream code that constructs a
        # MediaRef internally calls ``await fm.resolve_media_async(ref)``
        # — idempotent + cache-first.

        # A provider id belongs exclusively to this outbound call.  Keep the
        # canonical model on the request so retry, persistence, and a later
        # conversation turn re-enter the catalog with a resolvable reference.
        wire_config = _build_provider_wire_config(config, profile)
        client_attr = profile.client_attr
        if client_attr == self._GENERIC_OPENAI_CLIENT_ATTR:
            # Look up a registered local GenericOpenAIChat by CANONICAL model name
            # (the registry is model-keyed, not route-keyed), then fall back to
            # "default", then to the HuggingFaceChat singleton so cloud usage of the
            # generic-openai route keeps working unchanged.
            instance = _generic_openai_instances.get(model_name) or _generic_openai_instances.get(
                "default"
            )
            if instance is None:
                instance = await self._get_provider_client("huggingface_chat")
            return self._stamp_offering_usage(
                await self._dispatch_with_billing_net(
                    lambda: instance.execute(wire_config, profile, debug),
                    profile=profile,
                    provider_client=instance,
                ),
                profile,
                config,
            )

        if client_attr not in self._PROVIDER_FACTORIES:
            raise ValueError(
                f"UnifiedAIClient has no dispatch for wire_format {wire_format!r} "
                f"(client_attr={client_attr!r}, model={model_name!r}, "
                f"endpoint={profile.endpoint_id!r}, api={profile.api_id!r}). Chat dispatch covers "
                f"{sorted(self._PROVIDER_FACTORIES)} + {self._GENERIC_OPENAI_CLIENT_ATTR}; "
                "'extraction' runs through _execute_extraction; 'realtime' and "
                "'embedding' use specialized runtimes."
            )
        # Every provider client — chat AND media — takes the full
        # ResolvedCallProfile: param shaping is DB-driven (profile.controls),
        # structural branches read profile.capabilities / provider_model_id.
        provider_client = await self._get_provider_client(client_attr)
        return self._stamp_offering_usage(
            await self._dispatch_with_billing_net(
                lambda: provider_client.execute(wire_config, profile, debug),
                profile=profile,
                provider_client=provider_client,
            ),
            profile,
            config,
        )

    @staticmethod
    async def _dispatch_with_billing_net(
        dispatch: Any,
        *,
        profile: Any,
        provider_client: Any | None = None,
    ) -> Any:
        """Run one provider dispatch under the LAYER 2 billing net.

        Layer 1 is each adapter attaching billed usage to its terminal-failure /
        cancel exception; the orchestrator harvests it so a failed turn records
        real cost instead of $0. Nine providers implement it — nothing forces the
        tenth. This wraps the CHAT/MEDIA dispatch, so it can tell a forgetful
        adapter from an honest $0: if the wire was engaged and NOTHING ran billing
        capture, it screams. It never swallows or alters the exception.

        Extraction, chat, and media catalog routes all pass through this wrapper.
        STT, embedding, and realtime use dedicated runtimes and remain outside
        this chat/media billing net.
        """
        from matrx_ai.providers.admission import admit_provider_call
        from matrx_ai.providers.errors import report_unbilled_provider_failure
        from matrx_ai.providers.keys import prepare_provider_clients

        if provider_client is not None:
            await prepare_provider_clients(provider_client)

        async with admit_provider_call(profile):
            try:
                return await dispatch()
            except BaseException as exc:  # noqa: BLE001 — re-raised untouched below
                billing_gap = report_unbilled_provider_failure(
                    exc,
                    provider=str(getattr(profile, "vendor", "unknown")),
                    model=getattr(profile, "model_name", None),
                )
                if billing_gap:
                    try:
                        from matrx_connect.streaming.error_capture import capture_error

                        await capture_error(
                            exc,
                            kind="provider_billing_capture_missing",
                            route="providers/dispatch",
                            error_type=f"{type(exc).__module__}.{type(exc).__qualname__}",
                            payload={
                                "provider": str(getattr(profile, "vendor", "unknown")),
                                "model": getattr(profile, "model_name", None),
                            },
                        )
                    except Exception:
                        # Accounting alarms and their persistence must never
                        # swallow or replace the provider exception.
                        pass
                raise

    @staticmethod
    def _stamp_offering_usage(response: Any, profile: Any, config: Any) -> Any:
        """Stamp WHICH exact call served this response onto its TokenUsage.

        The ONE central seam: every catalog-routed dispatch passes through here,
        so the per-iteration cx_request row (via CompletedRequest.to_storage_dict)
        always records the ai.offering uuid + how it was chosen — pinned /
        preferred / sibling_fallback. Best-effort by design: a response without a
        usage object (some media paths) is returned untouched.
        """
        usage = getattr(response, "usage", None)
        if usage is not None and hasattr(usage, "offering_id"):
            usage.offering_id = profile.offering_id
            usage.offering_route = (
                "sibling_fallback"
                if getattr(config, "runtime_offering_id", None)
                else profile.resolution_route
            )
        # CITATIONS — settle-time identity enrichment. This is the one seam
        # where the request (config.messages, wire-ordered documents) and the
        # response meet, so document citations get their `document_index`
        # mapped back to OUR file_id/title here. Best-effort, never raises.
        from matrx_ai.config.citations import (
            collect_request_document_identities,
            enrich_document_citations_with_request_documents,
        )

        request_documents = collect_request_document_identities(
            getattr(getattr(config, "messages", None), "messages", None)
            or getattr(config, "messages", None)
        )
        if request_documents:
            enrich_document_citations_with_request_documents(request_documents, response)
        return response

    async def _execute_extraction(
        self,
        config: Any,
        wire_format: str,
        model_name: str,
        debug: bool | None = False,
    ) -> UnifiedResponse:
        """Run an information-extraction (GLiNER2 / Fastino) model as an agent turn.

        Mirrors a chat provider's ``execute`` contract: returns a ``UnifiedResponse``
        carrying a single assistant message whose text is the entities JSON. The
        extractor is fed the last user message text plus the labels/threshold the
        agent declared in ``config.metadata['extraction']`` (a label list is
        required — an extraction agent with no labels is a misconfiguration and
        raises loudly). Usage is zero (GLiNER pricing is a placeholder); when real
        Pioneer/Fastino rates land, populate ``input_tokens`` from the char count
        here.
        """
        import json as _json

        from matrx_ai.config import TextContent, TokenUsage, UnifiedMessage
        from matrx_ai.extraction import extract_spans

        spec = config.metadata.get("extraction") if isinstance(config.metadata, dict) else None
        if not isinstance(spec, dict):
            spec = {}
        labels = spec.get("labels")
        if not isinstance(labels, list) or not labels:
            raise ValueError(
                f"Extraction agent for model {model_name!r} has no labels. An "
                "information-extraction agent MUST declare the entity labels to "
                "extract in settings.metadata.extraction.labels (e.g. "
                '["person", "organization", "email address"]).'
            )
        labels = [str(label) for label in labels]
        try:
            threshold = float(spec.get("threshold", 0.3))
        except (TypeError, ValueError):
            threshold = 0.3

        text = self._last_user_text(config)

        result = await extract_spans(model_name, text, labels, threshold=threshold)

        entities: dict[str, list[dict[str, Any]]] = {}
        for span in result.spans:
            surface = (span.text or "").strip()
            if not surface:
                continue
            entities.setdefault(span.label, []).append(
                {
                    "text": surface,
                    "confidence": span.score if span.score is not None else None,
                    "start": span.start,
                    "end": span.end,
                }
            )

        payload = _json.dumps({"entities": entities}, ensure_ascii=False)
        if debug:
            vcprint(
                data={
                    "model": model_name,
                    "labels": labels,
                    "threshold": threshold,
                    "spans": len(result.spans),
                },
                title=f"[UnifiedClient] extraction run ({model_name})",
                color="cyan",
                verbose=True,
            )

        message = UnifiedMessage(role="assistant", content=[TextContent(text=payload)])
        usage = TokenUsage(
            input_tokens=0,
            output_tokens=0,
            matrx_model_name=model_name,
            api=wire_format,
        )
        return UnifiedResponse(
            messages=[message],
            usage=usage,
            stop_reason="stop",
            finish_reason="stop",
            metadata={"extraction": True, "model": result.model, "span_count": len(result.spans)},
        )

    @staticmethod
    def _last_user_text(config: Any) -> str:
        """Concatenate the text content of the last user message — the chunk the
        extraction model runs over. Falls back to the empty string (the extractor
        returns no spans, never crashes)."""
        from matrx_ai.config import TextContent

        for msg in reversed(config.messages.to_list()):
            if getattr(msg, "role", None) not in ("user", "User"):
                continue
            parts = [
                content.text
                for content in (getattr(msg, "content", None) or [])
                if isinstance(content, TextContent) and content.text
            ]
            if parts:
                return "\n".join(parts)
        return ""

    async def translate_request(
        self,
        request: AIMatrixRequest,
    ) -> dict[str, Any]:
        """Translate unified request to provider-specific format"""
        from matrx_ai.catalog.resolve import resolve_call_profile
        from matrx_ai.providers import (
            AnthropicTranslator,
            CerebrasTranslator,
            GenericOpenAITranslator,
            GoogleTranslator,
            GroqTranslator,
            OpenAITranslator,
            TogetherTranslator,
            XAITranslator,
        )

        config = request.config
        profile = await resolve_call_profile(
            config.model, offering_id=getattr(config, "routing_offering_id", None)
        )
        wire_config = _build_provider_wire_config(config, profile)

        # One translator per wire route. Route through build_request (the validated
        # chokepoint) for every provider, so this path gets the same
        # provider-agnostic sanitize as the live *_api.py path.
        translators = {
            "openai_chat": OpenAITranslator,
            "anthropic_chat": AnthropicTranslator,
            "google_chat": GoogleTranslator,
            "cerebras_chat": CerebrasTranslator,
            "together_chat": TogetherTranslator,
            "together_image": TogetherTranslator,
            "together_video": TogetherTranslator,
            "groq_chat": GroqTranslator,
            "xai_chat": XAITranslator,
            "huggingface_chat": GenericOpenAITranslator,
            "generic_openai_chat": GenericOpenAITranslator,
        }
        # A speech model shares its vendor's CHAT wire route (groq_tts and groq_standard are
        # both `groq_chat`; likewise openai_tts, google_tts, xai_tts, elevenlabs_tts). The
        # wire_format alone therefore cannot separate a chat model from a TTS model — that
        # is the distinction the retired api_class used to carry, and this call used to
        # RAISE because no translator was registered for `groq_tts`. Recover it from the
        # CAPABILITY data, never from a name or a route: a model that emits audio and no
        # text cannot be driven by a chat-completions request, and quietly building one
        # produces a nonsense payload instead of speech.
        #
        # `produces_audio and not produces_text` is the precise predicate, not
        # `produces_audio` alone: xai_realtime emits BOTH (a real conversational model),
        # and `distil-whisper-large-v3-en` carries api_class='groq_tts' while actually being
        # speech-to-TEXT (input audio -> output text). The capability data is strictly more
        # correct than the api_class it replaces — an api_class check would block whisper.
        caps = profile.capabilities
        if caps.produces_audio and not caps.produces_text:
            raise ValueError(
                f"translate_request cannot build a chat request for speech model "
                f"{profile.model_name!r} (wire_format={profile.wire_format!r}): it emits "
                f"audio and no text. Route it through the TTS path, not a chat translator."
            )

        translator_cls = translators.get(profile.wire_format)
        if translator_cls is None:
            raise ValueError(
                f"No request translator for wire_format {profile.wire_format!r} "
                f"(model={profile.model_name!r})"
            )
        # Every chat translator is DB-driven (B4): build_request takes the
        # resolved profile — params from profile.controls, structural branches
        # from profile.capabilities.
        return translator_cls().build_request(wire_config, profile)

    # ------------------------------------------------------------------
    # Image-ref annotate + resolve pass (runs once per ``execute()``)
    # ------------------------------------------------------------------

    async def _annotate_and_resolve_image_refs(
        self,
        messages,
        *,
        model_name: str | None,
        wire_format: str | None,
        supports_vision: bool,
        require_native_document_input: bool = False,
        debug: bool = False,
    ) -> None:
        """Resolve tool-result image/document refs before provider translation.

        Walk every image-shaped content item in ``messages`` and:

          1. Stamp ``vision_class`` based on the target model when not set.
          2. Run it through ``FileManager.resolve_media_async`` so the
             variant render fires (idempotent, cache-first).

        Image content blocks come from two places:
          - Client-supplied images, already resolved at the AI Dream
            boundary. ``is_resolved=True`` short-circuits the resolver
            in the variant pivot below.
          - Tool-result image blocks (e.g. screenshots) created mid-loop.
            These have ``file_id`` but no ``vision_class`` until this pass.

        Wrapped in best-effort try/except — failure to resolve an image
        falls back to whatever the boundary already produced (master
        bytes, a direct URL, etc.) and logs a warning.
        """
        from matrx_ai._ext import get_ext, has_ext
        from matrx_ai.processing.vision import resolve_vision_class

        documents: list[Any] = []
        seen_documents: set[int] = set()
        for message in messages.to_list():
            for content in message.content or []:
                _collect_document_shaped(content, documents, seen_documents)

        from matrx_ai.providers.provider_io_capabilities import (
            MediaContainer,
            is_input_natively_supported,
        )

        document_supported = supports_vision and is_input_natively_supported(
            MediaContainer.DOCUMENT, wire_format
        )
        if documents and not document_supported:
            if require_native_document_input:
                raise ValueError(
                    "This request requires native PDF/document input, but model/provider "
                    f"route '{model_name or 'unknown'}' ({wire_format or 'unknown'}) "
                    "cannot accept document input. Choose a document-capable model; "
                    "the requested pages will not be replaced with a text placeholder."
                )
            stripped_documents = _strip_document_content_for_unsupported_model(
                messages,
                model_name=model_name,
                wire_format=wire_format,
            )
            if stripped_documents:
                vcprint(
                    f"[unified_client] Model/provider route '{model_name}' "
                    f"({wire_format}) cannot accept document input; stripped "
                    f"{stripped_documents} document block(s) and substituted "
                    "text placeholders.",
                    color="yellow",
                )

        if not has_ext("get_cloud_file_manager"):
            return  # Standalone install — no cloud, nothing to resolve.

        try:
            fm = get_ext("get_cloud_file_manager")()
        except Exception as exc:
            vcprint(
                f"[unified_client] get_cloud_file_manager() raised: {exc}",
                color="yellow",
            )
            from matrx_connect.streaming.error_capture import capture_error

            await capture_error(
                exc,
                kind="media_reference_resolution_failed",
                route="unified_client/cloud_file_manager",
                error_type=type(exc).__name__,
            )
            return
        if documents:
            for document in documents:
                try:
                    await _resolve_media_ref_item(fm, document)
                except Exception as exc:
                    if debug:
                        vcprint(
                            f"[unified_client] document resolve failed: {exc}",
                            color="yellow",
                        )
                    from matrx_connect.streaming.error_capture import capture_error

                    await capture_error(
                        exc,
                        kind="media_reference_resolution_failed",
                        route="unified_client/document",
                        error_type=type(exc).__name__,
                        payload={"document_type": type(document).__name__},
                    )

        # "Can this model see?" is capability DATA (supports_vision, passed in).
        # ``resolve_vision_class`` answers a different question — the re-encoding
        # params (long_edge / quality / max_bytes) this model family wants.
        cls = resolve_vision_class(model_name, wire_format)
        target_class = cls.name

        # Text-only models (supports_vision=False): the provider will reject
        # any ``image_url`` / ``input_image`` content with HTTP 400. Strip
        # every image-shaped block from the messages and substitute a text
        # placeholder so the model still gets a typed signal that an image
        # existed. This is the only way to keep the conversation alive when
        # a vision-emitting tool (take_screenshot, read_page) runs against
        # an agent backed by a text-only model.
        if not supports_vision:
            stripped = _strip_image_content_for_text_only_model(
                messages,
                model_name=model_name,
                vision_class_name=target_class,
            )
            if stripped:
                vcprint(
                    f"[unified_client] Model '{model_name}' is text-only "
                    f"(vision_class={target_class}); stripped {stripped} "
                    "image block(s) and substituted text placeholders so the "
                    "provider call won't 400.",
                    color="yellow",
                )
            return  # No bytes will be sent; nothing left to resolve.

        try:
            from matrx_files.cloud_sync.media_ref import MediaRef
        except Exception:
            return

        seen: set[int] = set()
        items: list[Any] = []
        for message in messages.to_list():
            for content in message.content or []:
                _collect_image_shaped(content, items, seen)

        for item in items:
            current = getattr(item, "vision_class", None)
            if not current:
                try:
                    setattr(item, "vision_class", target_class)
                except Exception:
                    continue
            # If the item is already resolved with bytes for this class,
            # nothing more to do.
            if getattr(item, "is_resolved", False) and (
                getattr(item, "base64_data", None) or getattr(item, "resolved_url", None)
            ):
                # The boundary normaliser resolves with ``vision_class=None``
                # (no class set when client uploads). Re-resolve with the
                # newly-stamped class so the variant fires.
                if current is None and getattr(item, "file_id", None):
                    item.is_resolved = False  # type: ignore[attr-defined]
                    item.base64_data = None  # type: ignore[attr-defined]
                else:
                    continue
            try:
                if isinstance(item, MediaRef):
                    await fm.resolve_media_async(item, needs_bytes=True)
                else:
                    proxy = _media_ref_proxy(MediaRef, item)
                    await fm.resolve_media_async(proxy, needs_bytes=True)
                    for fname in (
                        "base64_data",
                        "resolved_url",
                        "mime_type",
                        "file_size",
                        "owner_id",
                        "is_ours",
                        "is_resolved",
                        "resolver_error",
                        "file_id",
                    ):
                        new_val = getattr(proxy, fname, None)
                        if new_val is None:
                            continue
                        try:
                            setattr(item, fname, new_val)
                        except Exception:
                            pass
            except Exception as exc:
                if debug:
                    vcprint(
                        f"[unified_client] image resolve failed (class={target_class}): {exc}",
                        color="yellow",
                    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


_IMAGE_REF_ATTRS = ("url", "file_id", "file_uri", "mime_type", "base64_data", "is_resolved")


def _is_image_ref_shaped(item: Any) -> bool:
    """Image-content items (and any future media-shaped type) carry these
    canonical attributes. We narrow to images only by mime_type prefix."""
    if not all(hasattr(item, a) for a in _IMAGE_REF_ATTRS):
        return False
    mime = getattr(item, "mime_type", "") or ""
    if isinstance(mime, str) and mime.lower().startswith("image/"):
        return True
    # Items typed explicitly as "image" / "input_image" still count.
    type_attr = getattr(item, "type", None)
    return isinstance(type_attr, str) and type_attr in ("image", "input_image")


def _collect_image_shaped(item: Any, out: list, seen: set) -> None:
    if id(item) in seen or item is None:
        return
    seen.add(id(item))
    if _is_image_ref_shaped(item):
        out.append(item)
        return
    # Tool-result content lists (ToolResultContent.content) — walk into the
    # list to surface the ImageContent blocks built by ``ToolResult.to_tool_result_content``.
    inner = getattr(item, "content", None)
    if isinstance(inner, list):
        for child in inner:
            _collect_image_shaped(child, out, seen)


def _is_document_ref_shaped(item: Any) -> bool:
    if not all(hasattr(item, attr) for attr in _IMAGE_REF_ATTRS):
        return False
    mime = getattr(item, "mime_type", "") or ""
    if isinstance(mime, str) and mime.lower().split(";", 1)[0] == "application/pdf":
        return True
    return getattr(item, "type", None) in ("document", "input_document")


def _enforce_required_native_document_input(
    messages: Any,
    *,
    config: Any,
    model_name: str | None,
    wire_format: str | None,
    supports_vision: bool,
) -> None:
    """Fail closed when a caller requires physical document input.

    This must run immediately after catalog routing — before an extraction
    model's text-only early return or the media-fallback conversion can turn a
    PDF into text (or remove it). It intentionally re-runs for every executor
    dispatch attempt, so a sibling-offering overload reroute is checked too.
    """
    metadata = getattr(config, "metadata", None)
    if not isinstance(metadata, dict) or not metadata.get("require_native_document_input", False):
        return

    documents: list[Any] = []
    seen_documents: set[int] = set()
    for message in messages.to_list():
        for content in message.content or []:
            _collect_document_shaped(content, documents, seen_documents)

    if not documents:
        raise ValueError(
            "This request requires native PDF/document input, but no document "
            "attachment reached the routed request. Refusing to run without the "
            "requested page context."
        )

    from matrx_ai.providers.provider_io_capabilities import (
        MediaContainer,
        is_input_natively_supported,
    )

    if supports_vision and is_input_natively_supported(MediaContainer.DOCUMENT, wire_format):
        return

    raise ValueError(
        "This request requires native PDF/document input, but model/provider "
        f"route '{model_name or 'unknown'}' ({wire_format or 'unknown'}) "
        "cannot accept document input. Choose a document-capable model; the "
        "requested pages will not be replaced with text or omitted."
    )


def _collect_document_shaped(item: Any, out: list, seen: set) -> None:
    if id(item) in seen or item is None:
        return
    seen.add(id(item))
    if _is_document_ref_shaped(item):
        out.append(item)
        return
    inner = getattr(item, "content", None)
    if isinstance(inner, list):
        for child in inner:
            _collect_document_shaped(child, out, seen)


def _media_ref_proxy(media_ref_cls: Any, item: Any) -> Any:
    """Build the MediaRef we hand the resolver — with EXACTLY ONE identifier.

    ``MediaRef`` accepts exactly one of ``file_id`` / ``url`` / ``file_uri``, and the
    media dataclasses (``ImageContent`` / ``AudioContent`` / …) can legitimately be
    carrying more than one: a persisted block keeps the id AND the URL that was
    visible when it was written. Forwarding all three raised at construction and
    killed the turn.

    Identity wins, always. ``file_id`` re-resolves forever through the access gate,
    with a URL minted at the moment of use if one is needed at all; a stored URL is a
    snapshot of a moment that has passed. Only a reference with no id of ours — a
    genuinely external asset — travels as a URL.
    """
    file_id = getattr(item, "file_id", None) or None
    url = getattr(item, "url", None) or None
    file_uri = getattr(item, "file_uri", None) or None
    if file_id:
        url = file_uri = None
    elif url:
        file_uri = None
    return media_ref_cls(
        file_id=file_id,
        url=url,
        file_uri=file_uri,
        mime_type=getattr(item, "mime_type", None),
        metadata=getattr(item, "metadata", {}) or {},
        vision_class=getattr(item, "vision_class", None),
    )


async def _resolve_media_ref_item(fm: Any, item: Any) -> None:
    from matrx_files.cloud_sync.media_ref import MediaRef

    if getattr(item, "is_resolved", False) and (
        getattr(item, "base64_data", None) or getattr(item, "resolved_url", None)
    ):
        return
    if isinstance(item, MediaRef):
        await fm.resolve_media_async(item, needs_bytes=True)
        return
    proxy = _media_ref_proxy(MediaRef, item)
    await fm.resolve_media_async(proxy, needs_bytes=True)
    for field_name in (
        "base64_data",
        "resolved_url",
        "mime_type",
        "file_size",
        "owner_id",
        "is_ours",
        "is_resolved",
        "resolver_error",
        "file_id",
    ):
        value = getattr(proxy, field_name, None)
        if value is not None:
            setattr(item, field_name, value)


def _build_text_placeholder_for_stripped_image(item: Any, model_name: str | None) -> Any:
    """Build a ``TextContent`` replacement describing an image that was
    stripped because the target model can't see images. Best-effort metadata
    extraction — we never fail the request over this."""
    from matrx_ai.config import TextContent

    parts: list[str] = ["[image attached"]
    mime = getattr(item, "mime_type", None)
    if isinstance(mime, str) and mime:
        parts.append(f" {mime}")
    fid = getattr(item, "file_id", None)
    if fid:
        parts.append(f" file_id={fid}")
    parts.append(
        f" — model '{model_name or 'unknown'}' does not support vision, "
        "image content was omitted from this turn]"
    )
    return TextContent(text="".join(parts))


def _strip_image_content_for_text_only_model(
    messages: Any, *, model_name: str | None, vision_class_name: str
) -> int:
    """Replace every image-shaped content block in ``messages`` with a text
    placeholder. Walks both top-level message content and nested
    ``ToolResultContent.content`` typed-block lists. Returns the count of
    replacements made.

    The replacement gives the model a typed signal that an image existed
    (with mime/file_id when available) so it can pivot — better than silently
    dropping the block and leaving the model wondering what happened to its
    tool call's output.
    """
    replaced = 0
    for message in messages.to_list():
        content_list = message.content or []
        for i, item in enumerate(content_list):
            if _is_image_ref_shaped(item):
                content_list[i] = _build_text_placeholder_for_stripped_image(item, model_name)
                replaced += 1
                continue
            # ToolResultContent.content can be a list of typed blocks
            # (TextContent / ImageContent) — walk it.
            inner = getattr(item, "content", None)
            if isinstance(inner, list):
                for j, child in enumerate(inner):
                    if _is_image_ref_shaped(child):
                        inner[j] = _build_text_placeholder_for_stripped_image(child, model_name)
                        replaced += 1
    return replaced


def _build_text_placeholder_for_stripped_document(
    item: Any,
    *,
    model_name: str | None,
    wire_format: str | None,
) -> Any:
    from matrx_ai.config import TextContent

    file_id = getattr(item, "file_id", None)
    identity = f" file_id={file_id}" if file_id else ""
    return TextContent(
        text=(
            f"[PDF document attached{identity} — model/provider route "
            f"'{model_name or 'unknown'}' ({wire_format or 'unknown'}) does not "
            "support document input, so physical-page content was omitted from this turn]"
        )
    )


def _strip_document_content_for_unsupported_model(
    messages: Any,
    *,
    model_name: str | None,
    wire_format: str | None,
) -> int:
    replaced = 0
    for message in messages.to_list():
        content_list = message.content or []
        for index, item in enumerate(content_list):
            if _is_document_ref_shaped(item):
                content_list[index] = _build_text_placeholder_for_stripped_document(
                    item,
                    model_name=model_name,
                    wire_format=wire_format,
                )
                replaced += 1
                continue
            inner = getattr(item, "content", None)
            if isinstance(inner, list):
                for child_index, child in enumerate(inner):
                    if _is_document_ref_shaped(child):
                        inner[child_index] = _build_text_placeholder_for_stripped_document(
                            child,
                            model_name=model_name,
                            wire_format=wire_format,
                        )
                        replaced += 1
    return replaced

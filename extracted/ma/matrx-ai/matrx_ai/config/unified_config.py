"""
Unified AI API Configuration System for OpenAI, Anthropic, and Google Gemini
Preserves ALL content types and metadata from all providers
"""

from collections.abc import Callable
from dataclasses import dataclass, field, fields
from typing import Any, Literal

from matrx_utils import vcprint
from pydantic import BaseModel, TypeAdapter

from matrx_ai.instructions.core import SystemInstruction
from matrx_ai.instructions.pattern_parser import resolve_matrx_patterns

from .dictionary_config import DictionaryConfig
from .enums import Role
from .llm_params import LLMParams, normalize_max_output_tokens
from .llm_wire_types import CompactionSettings, ImageLora
from .message_config import MessageList, UnifiedMessage
from .response_format import ResponseFormat
from .tts_config import TTSVoiceConfig
from .unified_content import (
    TextContent,
)
from .usage_config import TokenUsage

# Keys that arrive in a config dict and are intentionally not UnifiedConfig
# fields — feature-specific / passthrough values consumed by callers
# downstream (podcast generator, templating, request envelope). They are
# still surfaced on ``UnifiedConfig._unrecognized_keys`` for any consumer that
# wants them, but must never trigger the "unrecognized keys" warning. Add a
# key here once you've confirmed it is legitimately handled elsewhere.
_KNOWN_PASSTHROUGH_KEYS: frozenset[str] = frozenset(
    {
        "variables",  # template variable map (resolved before/after config build)
        "multi_speaker",  # podcast generator: multi-voice TTS toggle
        "model_name",  # human-readable model label (model_id is canonical)
        "voice_id",  # realtime/voice: TTS voice selection (consumed by the voice path)
        "realtime_tools",  # realtime/voice: client-declared realtime tool set
    }
)


def _parse_custom_tools(raw: list) -> list:
    """Deserialize custom tool overrides into runtime ``CustomTool`` instances.

    Accepts:
      - Already-constructed runtime ``CustomTool`` objects (pass-through).
      - Wire ``CustomTool`` instances from ``LLMParams`` validation.
      - Plain dicts from agents.custom_tools JSONB or request bodies.
    """
    from matrx_ai.config.custom_tool import CustomTool as WireCustomTool
    from matrx_ai.tools.models import CustomTool

    result = []
    for item in raw:
        if hasattr(item, "get_provider_format"):
            result.append(item)
        elif isinstance(item, WireCustomTool):
            result.append(CustomTool.model_validate(item.model_dump()))
        elif isinstance(item, dict):
            try:
                result.append(CustomTool.from_dict(item))
            except Exception as exc:
                vcprint(
                    f"[UnifiedConfig] Skipping invalid custom_tool entry: {exc}", color="yellow"
                )
    return result


def _normalize_response_format(value: object) -> dict[str, Any] | None:
    """Store response_format as a plain dict — translators require dict access."""
    if value is None:
        return None
    if isinstance(value, BaseModel):
        return value.model_dump(by_alias=True, exclude_none=True)
    if isinstance(value, dict):
        validated = TypeAdapter(ResponseFormat).validate_python(value)
        return validated.model_dump(by_alias=True, exclude_none=True)
    return None


def _normalize_compaction_settings(value: object) -> dict[str, Any] | None:
    if value is None:
        return None
    if isinstance(value, CompactionSettings):
        return value.model_dump(exclude_none=True)
    if isinstance(value, dict):
        return CompactionSettings.model_validate(value).model_dump(exclude_none=True)
    return None


def _normalize_tts_voice(value: object) -> str | list[dict[str, str]] | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        out: list[dict[str, str]] = []
        for item in value:
            if isinstance(item, BaseModel):
                out.append(item.model_dump())
            elif isinstance(item, dict):
                out.append(item)
        return out
    return None


def _normalize_image_loras(value: object) -> list[dict[str, Any]] | None:
    if value is None:
        return None
    out: list[dict[str, Any]] = []
    for item in value:
        if isinstance(item, ImageLora):
            out.append(item.model_dump())
        elif isinstance(item, dict):
            out.append(ImageLora.model_validate(item).model_dump())
        else:
            out.append(item)
    return out


_OVERRIDE_NORMALIZERS: dict[str, Callable[[object], object]] = {
    "custom_tools": _parse_custom_tools,
    "response_format": _normalize_response_format,
    "dictionary": DictionaryConfig.coerce,
    "compaction_settings": _normalize_compaction_settings,
    "tts_voice": _normalize_tts_voice,
    "image_loras": _normalize_image_loras,
}


@dataclass
class UnifiedConfig:
    """
    Pure LLM request - no AI Matrix specifics

    Core Principle:
    - system_instruction is stored ONLY in the system_instruction field
    - messages NEVER contain system/developer roles in UnifiedConfig
    - System messages are only created during API conversion (translator methods)
    """

    # On the way IN this is whatever the caller had (canonical name or uuid). At
    # dispatch UnifiedAIClient.execute rewrites it to the routing offering's
    # ``provider_model_id`` — the id that actually goes on the wire.
    model: str
    messages: MessageList | list[UnifiedMessage] | list[dict[str, Any]]
    system_instruction: str | dict | SystemInstruction | None = None
    # A conversation's system prompt is a write-once cache prefix.  The host
    # marks this true as soon as its first completed turn persists; every later
    # per-turn addition must use a user message instead.
    system_prompt_frozen: bool = False
    stream: bool = False

    # The CANONICAL matrx model name (ai.model_definition.name), stamped by
    # UnifiedAIClient.execute alongside the provider_model_id rewrite above. This
    # is the key for usage attribution + pricing lookup — never ``model``, which
    # is the provider's id.
    matrx_model_name: str | None = None

    # OFFERING PIN — "we're not listing the model, we're listing the exact call."
    # When set (an ai.offering uuid), resolve_call_profile routes THIS exact
    # offering (model × endpoint × api) and RAISES if it's unavailable or belongs
    # to another model — never a silent fall-back to the preferred offering.
    # Unset = preferred-by-priority (the classic behavior). Persisted in the
    # conversation config JSONB so the pin survives across turns.
    offering_id: str | None = None

    # RUNTIME routing pin — set ONLY by the overload-class sibling-offering
    # fallback (orchestrator/overload_reroute.py + executor), the one sanctioned
    # deviation from ``offering_id``. When set it wins over ``offering_id`` for
    # THIS request's dispatches, but it is NEVER persisted (to_storage_dict skips
    # it) — the user's pin stays intact for future turns; the deviation is
    # per-error, not permanent. Recorded on the call record via
    # TokenUsage.offering_route="sibling_fallback" + the RerouteNote trail.
    runtime_offering_id: str | None = None

    # Transient OpenAI Responses cache-routing key, derived per provider loop.
    # It is deliberately omitted from ``to_storage_dict``.
    prompt_cache_key: str | None = None

    @property
    def routing_offering_id(self) -> str | None:
        """The offering pin dispatch actually uses: runtime fallback pin first,
        then the user's persisted pin, else None (preferred-by-priority)."""
        return self.runtime_offering_id or self.offering_id

    max_output_tokens: int | None = None
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None

    tools: list = field(default_factory=list)
    # Durable pre-policy declaration. ``tools`` is the effective request set
    # and may be filtered by host authority (for example, a bound sandbox
    # suppresses duplicate cloud-file tools). Keeping the authored set separate
    # prevents a filtered turn from permanently deleting tools when its config
    # is persisted and later reloaded after the target detaches.
    authored_tools: list | None = None
    # Registered tools selected dynamically during the conversation (for
    # example, desktop/browser discovery categories).  Unlike the effective
    # ``tools`` list these are conversation state, not one request's policy
    # output: a continuation must restore them, then re-run authority and
    # executor viability against the current client.  ``None`` is accepted as
    # a legacy-deserialization sentinel so pre-field rows can recover dynamic
    # additions from their persisted effective-vs-authored delta.
    dynamic_tools: list[str] | None = None
    # Durable transition marker for authored-vs-effective restoration. It is
    # true only while host hard exclusions are applied to ``tools``; persisting
    # it lets a later reload with no bound target restore ``authored_tools``.
    tool_authority_filtered: bool = False
    # Exact hard-exclusion policy that produced the effective set. Reapplying
    # the same policy must preserve same-request dynamic mutations; switching
    # directly to a different non-empty policy must restart from authored.
    tool_authority_exclusions: list[str] = field(default_factory=list)
    # In-memory-only companion to ``tool_authority_exclusions``. A persisted
    # filtered config must restore once after reload (effective inline tools are
    # not stored), while repeated merges in one request preserve mutations.
    tool_authority_filter_applied_runtime: bool = False
    # Other request-time gates also mutate the effective declaration. Persist
    # their transition markers so the next compatible request can restore the
    # canonical authored declaration instead of inheriting a filtered turn.
    tool_capability_filtered: bool = False
    tool_delegation_filtered: bool = False
    tool_delegation_executors: list[str] | None = None
    tool_delegation_disabled_policy: bool = False
    tool_delegation_registry_fingerprint: str | None = None
    # In-memory only. False after deserialization, allowing a persisted
    # request-effective filter to restore once even when executor names are
    # unchanged; True prevents same-request merges from resurrecting dynamic
    # removals. Deliberately omitted from storage.
    tool_delegation_filter_applied_runtime: bool = False
    # Literal["none", "auto", "required"]
    tool_choice: Literal["none", "auto", "required"] | None = None
    parallel_tool_calls: bool = True

    # Tool UUIDs currently in ``tools`` that were contributed by SKILLS (not the
    # agent's own tool config). Tracked so that when a per-run skill is removed on
    # a later turn, its tools can be reconciled out of the PERSISTED tool set
    # instead of lingering forever. Written by the host skill-merge layer
    # (aidream skill_merge._reconcile_skill_injected_tools); round-trips through
    # the config blob like detected_contexts, and is never sent to a provider.
    skill_injected_tool_ids: list[str] = field(default_factory=list)

    # Function-calling capability of THIS request's model, resolved ONCE from the
    # capability source of truth (providers/capabilities.py) when the model is
    # bound at request-prep. It is the single flag that gates every tool /
    # context auto-injection site: when False (a TTS / image / video / audio /
    # extraction model), injectors skip their work instead of adding tools the
    # provider would only reject. Defaults True (permissive) so an unresolved
    # config never silently loses tools — the provider-boundary fallback in
    # unified_client is the loud backstop if anything slips through anyway.
    supports_tools: bool = True

    # Inline tool definitions not stored in the tool registry.
    # Populated from agents.custom_tools (agent definition) and/or the
    # custom_tools field in AgentStartRequest / ConversationContinueRequest.
    # All names are automatically added to client_tools — calls are always
    # delegated back to the caller; there is no server-side implementation.
    custom_tools: list = field(default_factory=list)  # list[CustomTool]
    authored_custom_tools: list | None = None

    # OpenAI thinking format
    reasoning_effort: (
        Literal["auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"] | None
    ) = None
    reasoning_summary: Literal["concise", "detailed", "never", "auto", "always"] | None = None

    # Google Gemini 3 thinking format
    thinking_level: Literal["minimal", "low", "medium", "high"] | None = None
    include_thoughts: bool | None = None

    # Anthropic thinking & legacy Google Gemini 2 thinking format
    thinking_budget: int | None = None

    # Cerebras-specific thinking controls
    # clear_thinking: strip <thinking> blocks from the final Cerebras response
    # disable_reasoning: when True, suppress reasoning entirely; maps to reasoning_effort="none" cross-provider
    clear_thinking: bool | None = None
    disable_reasoning: bool | None = None

    response_format: dict[str, Any] | None = None
    stop_sequences: list = field(default_factory=list)

    store: bool | None = None
    previous_interaction_id: str | None = None
    task: Literal["text_to_video", "image_to_video", "reference_to_video", "edit"] | None = None
    verbosity: str | None = None

    # Media/attachment settings
    internal_web_search: bool | None = None
    internal_url_context: bool | None = None
    # xAI Grok native X (Twitter) search — modeled on internal_url_context.
    # Honoured by the xAI translator; dropped (yellow warning) for other providers.
    internal_x_search: bool | None = None

    # =====================================================================
    # Media generation: dimensions
    # =====================================================================
    # aspect_ratio: intent ("16:9" / "1:1" / "9:16" / "4:3" / "3:4" / etc).
    # width + height: explicit pixel dimensions. Translators accept either.
    # When both forms set, explicit (width+height) wins.
    aspect_ratio: str | None = None
    width: int | None = None
    height: int | None = None
    count: int = 1

    # =====================================================================
    # Media generation: image-specific
    # =====================================================================
    # render_quality: OpenAI gpt-image-* compute-effort knob.
    # Maps to provider-native "quality" on OpenAI; ignored on most others.
    render_quality: Literal["low", "medium", "high", "auto"] | None = None
    # OpenAI gpt-image-1.5 only — not accepted by gpt-image-2.
    background: Literal["auto", "opaque", "transparent"] | None = None
    # OpenAI gpt-image-2 only — jpeg/webp compression 0..100.
    output_compression: int | None = None
    # OpenAI moderation level.
    moderation: Literal["auto", "low"] | None = None
    # OpenAI gpt-image-1.5 only — controls how strictly the model adheres to input image.
    input_fidelity: Literal["high", "low"] | None = None
    # OpenAI gpt-image-* — number of partial images during streaming (0..3,
    # +100 image-output tokens each). Setting >0 implicitly enables stream.
    partial_images: int | None = None
    # Recraft v4 / DALL-E-3 — preset style.
    style: str | None = None
    # Image-to-image / video-to-video strength (0..1) where supported.
    reference_strength: float | None = None

    # =====================================================================
    # Audio / TTS settings
    # =====================================================================
    # tts_voice: str → single-speaker voice name (e.g. "Orus")
    # tts_voice: list[dict] → multi-speaker [{"name": "Alex", "voice": "Orus"}, ...]
    tts_voice: str | list[dict[str, str]] | None = None
    audio_format: str | None = None  # desired output format: "wav", "mp3", "ogg"

    # =====================================================================
    # Media generation: video-specific
    # =====================================================================
    # duration_seconds: canonical int. Translators stringify for providers
    # (Sora, Veo) that take strings.
    duration_seconds: int | None = None
    # resolution: tier label ("480p" / "720p" / "1080p" / "4k" / "1K" / "2K" / "4K").
    resolution: str | None = None
    fps: int | None = None
    steps: int | None = None
    seed: int | None = None
    guidance_scale: int | None = None
    # encode_quality: video file quality/size tradeoff (1..100, Together video).
    encode_quality: int | None = None
    negative_prompt: str | None = None
    output_format: str | None = None
    frame_images: list | None = None
    reference_images: list | None = None
    image_loras: list | None = None
    disable_safety_checker: bool | None = None
    # generate_audio: video audio toggle. Native name for Google Veo, Together
    # Veo, Replicate Veo, Together Kling. Provider-native.
    generate_audio: bool | None = None
    # Veo 3.1 + several Together models — server-side prompt enhancement.
    enhance_prompt: bool | None = None

    # MediaRef-shaped inputs for image/video generation. All resolved at the
    # AI Dream API boundary via FileManager.resolve_media_async — provider
    # translators consume already-resolved data (base64_data / resolved_url).
    # See aidream/services/media_resolvers/request_normalizer.py.
    image_input: Any | None = None  # MediaRef — single image (i2i, edit, i2v)
    image_inputs: list[Any] | None = None  # list[MediaRef] — multi-reference
    mask: Any | None = None  # MediaRef — alpha-channel inpaint mask
    last_frame_image: Any | None = None  # MediaRef — Veo 3.1 interpolation target
    video_input: Any | None = None  # MediaRef — video edit / extend source

    # For providers (xAI, OpenAI Sora) where one model id handles multiple ops
    # via different endpoints. Provider translator picks the endpoint.
    video_action: Literal["generate", "edit", "extend"] | None = None

    # MCP server UUIDs attached to this agent. Resolution TBD — for now we
    # carry them through so downstream layers can use them when ready.
    mcp_servers: list[str] = field(default_factory=list)
    authored_mcp_servers: list[str] | None = None

    # Context Compaction Settings (5-Tier Architecture)
    # Tier 1: Auto-stripping (always-on) | Tier 2: Minimal prune | Tier 3: Content-to-retrieval
    # Tier 4: Threshold trimming (cost/quality) | Tier 5: Hard lossy compression
    compaction_settings: dict[str, Any] | None = None

    # Discovered Contexts (Surfaced for Cloud UI Review)
    # Object holding parsed repository configurations (.cursorrules, AGENTS.md, etc.)
    # populated by the environment sniffer.
    detected_contexts: dict[str, str] | None = None

    custom_configs: dict[str, Any] | None = None

    # Custom Dictionary (terminology + pronunciation). Set by server-side
    # auto-injection on transcription/TTS surfaces, or via config_overrides.
    # May arrive as a DictionaryConfig or a dict; translators normalize via
    # DictionaryConfig.coerce(). See config/dictionary_config.py.
    dictionary: "DictionaryConfig | dict[str, Any] | None" = None

    # ElevenLabs native pronunciation-dictionary locators — at most 3
    # {pronunciation_dictionary_id, version_id} dicts, applied in order. Resolved
    # host-side (aidream) from published tiers and passed straight to the
    # ElevenLabs TTS call. Empty for every other provider (they use alias
    # substitution instead). See aidream/services/dictionary/locators.py.
    pronunciation_dictionary_locators: list[dict[str, str]] = field(default_factory=list)

    # TTS quality mode — "high_quality" | "fast". The catalog resolver selects
    # an offering whose metadata.tts.quality_tiers contains the requested tier.
    tts_quality: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """
        Normalize messages and system_instruction.

        System instruction normalization:
        - str: Wrapped in SystemInstruction (date auto-injected by default).
        - dict: Converted to SystemInstruction via from_value().
        - SystemInstruction: Kept as-is.
        - None: Left as None.

        After __post_init__, system_instruction is always SystemInstruction | None.
        Providers must use resolved_system_instruction (str | None) when sending to APIs.
        """
        # ``from_dict`` replaces this after construction with the exact unknown
        # input keys. Direct construction has no unknown input mapping, but must
        # still satisfy the same runtime accessor contract.
        self._unrecognized_keys: list[str] = []

        # Provider APIs require an integer token limit. Normalize persisted
        # agent/conversation JSONB and direct UnifiedConfig construction at the
        # runtime boundary, not only request-time LLMParams overrides.
        self.max_output_tokens = normalize_max_output_tokens(self.max_output_tokens)

        # Convert messages to MessageList if needed
        if not isinstance(self.messages, MessageList):
            if isinstance(self.messages, list):
                self.messages = MessageList(_messages=self.messages)
            else:
                raise TypeError(f"messages must be MessageList or list, got {type(self.messages)}")

        self.custom_tools = _parse_custom_tools(self.custom_tools)
        if self.authored_tools is None:
            self.authored_tools = list(self.tools)
        else:
            self.authored_tools = list(self.authored_tools)
        if self.dynamic_tools is None:
            if self.tool_authority_filtered or self.tool_delegation_filtered:
                authored = {entry for entry in self.authored_tools if isinstance(entry, str)}
                self.dynamic_tools = [
                    entry
                    for entry in self.tools
                    if isinstance(entry, str) and entry not in authored
                ]
            else:
                self.dynamic_tools = []
        else:
            self.dynamic_tools = list(dict.fromkeys(self.dynamic_tools))
        if self.authored_custom_tools is None:
            self.authored_custom_tools = list(self.custom_tools)
        else:
            self.authored_custom_tools = _parse_custom_tools(self.authored_custom_tools)
            if (
                not self.custom_tools
                and not self.tool_authority_filtered
                and not self.tool_capability_filtered
                and not self.tool_delegation_filtered
            ):
                # Effective request inline tools are not persisted. Rehydrate
                # only the canonical agent-authored definitions on a normal,
                # unfiltered reload.
                self.custom_tools = list(self.authored_custom_tools)
        if self.authored_mcp_servers is None:
            self.authored_mcp_servers = list(self.mcp_servers)
        else:
            self.authored_mcp_servers = list(self.authored_mcp_servers)
            if not self.mcp_servers and not self.tool_capability_filtered:
                # Effective request MCPs are intentionally not persisted
                # (client.mcp is session-only). Rehydrate only the canonical
                # agent-authored slugs on an unfiltered reload.
                self.mcp_servers = list(self.authored_mcp_servers)

        self.tool_choice = self._normalize_tool_choice(self.tool_choice)
        self.system_instruction = self._normalize_system_instruction(self.system_instruction)
        self._resolve_message_patterns()
        # Agent definitions are hydrated before request input is composed. An
        # authored definition may therefore contain only an empty user
        # placeholder at this phase. Normalize it now but defer the empty-list
        # failure; BaseTranslator.build_request performs the strict pass after
        # runtime input has been added and still fails closed if none was added.
        self.messages.sanitize(allow_empty=True)

    @property
    def unexpected_keys(self) -> list[str]:
        """Caller keys this config neither declares NOR knowingly passes through.

        ``_unrecognized_keys`` deliberately holds BOTH populations — every key that
        is not a ``UnifiedConfig`` field, including the ones in
        ``_KNOWN_PASSTHROUGH_KEYS`` that downstream code consumes on purpose. That
        is correct for a consumer that wants to forward them, and wrong for any
        consumer that wants to tell a user something was ignored: a podcast run
        sends ``multi_speaker`` by design, and warning on it says the platform
        dropped a feature it in fact honoured.

        Use this for anything user-facing; use ``_unrecognized_keys`` only when you
        genuinely want the passthrough keys too.
        """
        # ``getattr`` is the second isolation layer for objects restored by old
        # pickles/copies that predate the constructor invariant.
        return sorted(set(getattr(self, "_unrecognized_keys", ())) - _KNOWN_PASSTHROUGH_KEYS)

    @property
    def tts_voice_config(self) -> TTSVoiceConfig | None:
        """Return a fully-typed TTSVoiceConfig built from tts_voice.

        Returns None when no TTS voice is configured.
        Providers should use this property instead of reading tts_voice directly.
        """
        return TTSVoiceConfig.from_config(self)

    def _resolve_message_patterns(self) -> None:
        """Resolve <<MATRX>> data-fetch patterns in all TextContent across messages."""
        for message in self.messages:
            for content in message.content:
                if isinstance(content, TextContent) and content.text:
                    content.text = resolve_matrx_patterns(content.text)

    @staticmethod
    def _normalize_system_instruction(
        raw: str | dict | SystemInstruction | None,
    ) -> SystemInstruction | None:
        """Normalize to SystemInstruction object. Never resolves to string here."""
        if raw is None:
            return None
        if isinstance(raw, SystemInstruction):
            return raw
        return SystemInstruction.from_value(raw)

    @property
    def resolved_system_instruction(self) -> str | None:
        """Resolve system_instruction to string on demand.

        This is the single point of resolution for all provider translators.
        Never call str(config.system_instruction) directly in a translator —
        always use this property so the resolution logic lives in one place.
        """
        if self.system_instruction is None:
            return None
        # `action_types` (Matrx Directives guidance) is populated upstream by the
        # assembly layer from the agent's `matrx_actions.actions` — see
        # apply_matrx_directives_guidance(). __str__ renders the section when set.
        return str(self.system_instruction)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UnifiedConfig":
        """
        Create UnifiedConfig from dictionary (e.g., from API).

        Extracts system/developer messages from messages list and places them
        in system_instruction field.
        """
        # Provider-native field aliases. Each model's controls JSONB declares
        # control names verbatim from the provider's API — so the agent's
        # settings dict can carry e.g. `seconds: "8"` (Sora native) or
        # `num_outputs: 4` (Replicate native). Normalize to the canonical
        # UnifiedConfig field names here so translators only ever read one
        # form. Mirrors LLMParams._FIELD_ALIASES exactly.
        _FIELD_ALIASES = {
            "max_tokens": "max_output_tokens",
            "n": "count",
            "num_outputs": "count",
            "number_of_images": "count",
            "quality": "render_quality",
            "output_quality": "encode_quality",
            "seconds": "duration_seconds",
            "duration": "duration_seconds",
        }
        _COERCE_INT = {"seconds", "duration"}
        for old_key, new_key in _FIELD_ALIASES.items():
            if old_key not in data:
                continue
            value = data.pop(old_key)
            if value is None:
                continue
            if old_key in _COERCE_INT:
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    continue
            if data.get(new_key) is None:
                data[new_key] = value

        valid_fields = {f.name for f in fields(cls)}
        valid_fields.add("model_id")
        unrecognized_keys = set(data.keys()) - valid_fields

        # Keys the platform knowingly accepts as passthrough/feature-specific
        # config (consumed by callers downstream, not by UnifiedConfig itself).
        # They are still recorded on ``_unrecognized_keys`` but never warned —
        # warning on them was pure log noise on every podcast / templated run.
        _unrecognized = list(unrecognized_keys) if unrecognized_keys else []
        unexpected_keys = unrecognized_keys - _KNOWN_PASSTHROUGH_KEYS
        if unexpected_keys:
            vcprint(
                unexpected_keys,
                "Unrecognized keys in UnifiedConfig (likely expected, but confirm if update is needed on client side or our server side code)",
                color="yellow",
            )

        # Parse messages and extract system instruction
        messages_data = data.get("messages", [])
        parsed_messages = []
        extracted_system_text = ""

        for msg_data in messages_data:
            # Convert to UnifiedMessage if needed
            if isinstance(msg_data, dict):
                msg = UnifiedMessage.from_dict(msg_data)
            elif hasattr(msg_data, "__dict__"):  # Already a UnifiedMessage object
                msg = msg_data
            else:
                vcprint(
                    {"msg_data_type": type(msg_data).__name__, "msg_data_repr": repr(msg_data)},
                    "UnifiedConfig.from_dict: unrecognized message type — Temporarily not raising an error, but dropping the message",
                    color="red",
                )
                continue

            # Extract system/developer messages to system_instruction
            if msg.role in (Role.SYSTEM, Role.DEVELOPER, "system", "developer"):
                # Extract text content from first system/developer message
                if not extracted_system_text and msg.content:
                    for content in msg.content:
                        if isinstance(content, TextContent):
                            extracted_system_text += content.text
                # Don't add to parsed_messages - system goes to system_instruction
            else:
                # Regular message - add to list
                parsed_messages.append(msg)

        # Priority: explicit system_instruction > extracted from messages
        # Use 'is not None' check so dict values (including potentially empty ones)
        # are preserved rather than being swallowed by falsy coalescing.
        explicit_si = data.get("system_instruction")
        if explicit_si is not None:
            system_instruction = explicit_si
        elif extracted_system_text:
            system_instruction = extracted_system_text
        else:
            system_instruction = None

        config = cls(
            model=data.get("model", ""),
            offering_id=data.get("offering_id"),
            messages=parsed_messages,
            system_instruction=system_instruction,
            system_prompt_frozen=bool(data.get("system_prompt_frozen", False)),
            stream=data.get("stream", False),
            max_output_tokens=data.get("max_output_tokens"),
            temperature=data.get("temperature"),
            top_p=data.get("top_p"),
            top_k=data.get("top_k"),
            tools=data.get("tools", []),
            authored_tools=data.get("authored_tools"),
            dynamic_tools=data.get("dynamic_tools"),
            tool_authority_filtered=bool(data.get("tool_authority_filtered", False)),
            tool_authority_exclusions=data.get("tool_authority_exclusions", []),
            tool_capability_filtered=bool(data.get("tool_capability_filtered", False)),
            tool_delegation_filtered=bool(data.get("tool_delegation_filtered", False)),
            tool_delegation_executors=data.get("tool_delegation_executors"),
            tool_delegation_disabled_policy=bool(
                data.get("tool_delegation_disabled_policy", False)
            ),
            tool_delegation_registry_fingerprint=data.get("tool_delegation_registry_fingerprint"),
            skill_injected_tool_ids=data.get("skill_injected_tool_ids", []),
            tool_choice=data.get("tool_choice"),
            parallel_tool_calls=data.get("parallel_tool_calls", True),
            custom_tools=_parse_custom_tools(data.get("custom_tools", [])),
            authored_custom_tools=data.get("authored_custom_tools"),
            reasoning_effort=data.get("reasoning_effort"),
            reasoning_summary=data.get("reasoning_summary"),
            thinking_level=data.get("thinking_level"),
            include_thoughts=data.get("include_thoughts"),
            thinking_budget=data.get("thinking_budget"),
            clear_thinking=data.get("clear_thinking"),
            disable_reasoning=data.get("disable_reasoning"),
            response_format=data.get("response_format"),
            stop_sequences=data.get("stop_sequences", []),
            store=data.get("store"),
            previous_interaction_id=data.get("previous_interaction_id"),
            task=data.get("task"),
            verbosity=data.get("verbosity"),
            internal_web_search=data.get("internal_web_search"),
            internal_url_context=data.get("internal_url_context"),
            internal_x_search=data.get("internal_x_search"),
            # Media: dimensions
            aspect_ratio=data.get("aspect_ratio"),
            width=data.get("width"),
            height=data.get("height"),
            count=data.get("count", 1),
            # Media: image-specific
            render_quality=data.get("render_quality"),
            background=data.get("background"),
            output_compression=data.get("output_compression"),
            moderation=data.get("moderation"),
            input_fidelity=data.get("input_fidelity"),
            partial_images=data.get("partial_images"),
            style=data.get("style"),
            reference_strength=data.get("reference_strength"),
            # TTS / audio
            tts_voice=data.get("tts_voice"),
            audio_format=data.get("audio_format"),
            # Media: video-specific
            duration_seconds=data.get("duration_seconds"),
            resolution=data.get("resolution"),
            fps=data.get("fps"),
            steps=data.get("steps"),
            seed=data.get("seed"),
            guidance_scale=data.get("guidance_scale"),
            encode_quality=data.get("encode_quality"),
            negative_prompt=data.get("negative_prompt"),
            output_format=data.get("output_format"),
            frame_images=data.get("frame_images"),
            reference_images=data.get("reference_images"),
            image_loras=data.get("image_loras"),
            disable_safety_checker=data.get("disable_safety_checker"),
            generate_audio=data.get("generate_audio"),
            enhance_prompt=data.get("enhance_prompt"),
            # MediaRef inputs
            image_input=data.get("image_input"),
            image_inputs=data.get("image_inputs"),
            mask=data.get("mask"),
            last_frame_image=data.get("last_frame_image"),
            video_input=data.get("video_input"),
            video_action=data.get("video_action"),
            mcp_servers=data.get("mcp_servers", []),
            authored_mcp_servers=data.get("authored_mcp_servers"),
            compaction_settings=data.get("compaction_settings"),
            detected_contexts=data.get("detected_contexts"),
            custom_configs=data.get("custom_configs"),
            dictionary=DictionaryConfig.coerce(data.get("dictionary")),
            pronunciation_dictionary_locators=data.get("pronunciation_dictionary_locators") or [],
            tts_quality=data.get("tts_quality"),
            metadata=data.get("metadata", {}),
        )
        config._unrecognized_keys = _unrecognized
        return config

    def _normalize_tool_choice(
        self, tool_choice: Any
    ) -> Literal["none", "auto", "required"] | None:
        if tool_choice in ["none", "auto", "required"]:
            return tool_choice
        elif tool_choice == "any":
            return "required"
        elif tool_choice == "ANY":
            return "required"
        elif tool_choice == "NONE":
            return "none"
        elif tool_choice == "AUTO":
            return "auto"
        elif isinstance(tool_choice, dict):
            return tool_choice["type"]
        elif isinstance(tool_choice, str):
            if tool_choice == "auto":
                return "auto"
            elif tool_choice == "required":
                return "required"
            elif tool_choice == "any":
                return "required"
            elif tool_choice == "none":
                return "none"
            else:
                return None
        elif tool_choice is None:
            return None
        else:
            vcprint(tool_choice, "WARNING: Unknown tool choice type", color="red")
            return None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        result = {}

        for key, value in self.__dict__.items():
            if key == "_unrecognized_keys" and not value:
                continue
            if value is None:
                continue

            # Handle MessageList specially
            if isinstance(value, MessageList):
                result[key] = value.to_dict_list()
            elif isinstance(value, SystemInstruction):
                result[key] = str(value)
            elif isinstance(value, list) and value and hasattr(value[0], "to_dict"):
                result[key] = [item.to_dict() for item in value]
            elif hasattr(value, "to_dict"):
                result[key] = value.to_dict()
            else:
                result[key] = value

        return result

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to storage format matching the cx_conversation + cx_message schema.

        Returns dict with:
            - model: str (cx_conversation.model column)
            - system_instruction: str | None (cx_conversation.system_instruction column)
            - config: dict (cx_conversation.config JSONB)
            - messages: list[dict] (each dict is a cx_message row via UnifiedMessage.to_storage_dict)
        """

        message_storage_dicts = [
            msg.to_storage_dict() for msg in self.messages if not msg.is_ephemeral_only()
        ]
        # vcprint(message_storage_dicts, "[UnifiedConfig] Message Storage Dicts", color="yellow")

        # Top-level columns.
        #
        # The first completed turn freezes the SYSTEM prefix. Persist the exact
        # rendered text, including first-turn runtime additions, so a reload can
        # never reconstruct a different prefix and silently kill prompt caching.
        system_instruction_storage: str | None = (
            self.system_instruction.to_storage_text()
            if isinstance(self.system_instruction, SystemInstruction)
            else self.resolved_system_instruction
        )
        result: dict[str, Any] = {
            "model": self.model,
            "system_instruction": system_instruction_storage,
            "messages": message_storage_dicts,
        }

        # Config JSONB -- only include non-default/non-None values
        config: dict[str, Any] = {}
        if self.offering_id is not None:
            config["offering_id"] = self.offering_id
        if self.temperature is not None:
            config["temperature"] = self.temperature
        if self.max_output_tokens is not None:
            config["max_output_tokens"] = self.max_output_tokens
        if self.top_p is not None:
            config["top_p"] = self.top_p
        if self.top_k is not None:
            config["top_k"] = self.top_k
        if self.tools:
            config["tools"] = self.tools
        if self.authored_tools:
            config["authored_tools"] = self.authored_tools
        if self.dynamic_tools:
            config["dynamic_tools"] = self.dynamic_tools
        if self.authored_custom_tools:
            config["authored_custom_tools"] = [
                tool.model_dump(mode="json") if hasattr(tool, "model_dump") else tool
                for tool in self.authored_custom_tools
            ]
        if self.authored_mcp_servers:
            config["authored_mcp_servers"] = self.authored_mcp_servers
        if self.tool_authority_filtered:
            config["tool_authority_filtered"] = True
        if self.tool_authority_exclusions:
            config["tool_authority_exclusions"] = self.tool_authority_exclusions
        if self.tool_capability_filtered:
            config["tool_capability_filtered"] = True
        if self.tool_delegation_filtered:
            config["tool_delegation_filtered"] = True
        if self.tool_delegation_executors is not None:
            config["tool_delegation_executors"] = self.tool_delegation_executors
        if self.tool_delegation_disabled_policy:
            config["tool_delegation_disabled_policy"] = True
        if self.tool_delegation_registry_fingerprint is not None:
            config["tool_delegation_registry_fingerprint"] = (
                self.tool_delegation_registry_fingerprint
            )
        if self.skill_injected_tool_ids:
            config["skill_injected_tool_ids"] = self.skill_injected_tool_ids
        if self.system_prompt_frozen:
            config["system_prompt_frozen"] = True
        if self.tool_choice is not None:
            config["tool_choice"] = self.tool_choice
        if not self.parallel_tool_calls:
            config["parallel_tool_calls"] = False
        if self.reasoning_effort is not None:
            config["reasoning_effort"] = self.reasoning_effort
        if self.reasoning_summary is not None:
            config["reasoning_summary"] = self.reasoning_summary
        if self.thinking_level is not None:
            config["thinking_level"] = self.thinking_level
        if self.include_thoughts is not None:
            config["include_thoughts"] = self.include_thoughts
        if self.thinking_budget is not None:
            config["thinking_budget"] = self.thinking_budget
        if self.clear_thinking is not None:
            config["clear_thinking"] = self.clear_thinking
        if self.disable_reasoning is not None:
            config["disable_reasoning"] = self.disable_reasoning
        if self.response_format is not None:
            config["response_format"] = self.response_format
        if self.stop_sequences:
            config["stop_sequences"] = self.stop_sequences
        if self.stream:
            config["stream"] = True
        if self.internal_web_search is not None:
            config["internal_web_search"] = self.internal_web_search
        if self.internal_url_context is not None:
            config["internal_url_context"] = self.internal_url_context
        if self.internal_x_search is not None:
            config["internal_x_search"] = self.internal_x_search
        if self.store is not None:
            config["store"] = self.store
        if self.previous_interaction_id is not None:
            config["previous_interaction_id"] = self.previous_interaction_id
        if self.task is not None:
            config["task"] = self.task
        if self.verbosity is not None:
            config["verbosity"] = self.verbosity
        if self.tts_voice is not None:
            config["tts_voice"] = self.tts_voice
        if self.audio_format is not None:
            config["audio_format"] = self.audio_format
        if self.compaction_settings is not None:
            config["compaction_settings"] = self.compaction_settings
        if self.detected_contexts is not None:
            config["detected_contexts"] = self.detected_contexts
        if self.pronunciation_dictionary_locators:
            config["pronunciation_dictionary_locators"] = self.pronunciation_dictionary_locators
        if self.dictionary is not None:
            _dict = DictionaryConfig.coerce(self.dictionary)
            if _dict is not None:
                config["dictionary"] = _dict.model_dump(exclude_none=True)

        result["config"] = config
        return result

    def append_user_message(self, text: str, **kwargs) -> None:
        """
        Append a user message to the conversation.

        Args:
            text: The message text
            **kwargs: Additional UnifiedMessage fields (id, name, timestamp, metadata)
        """
        self.messages.append_user_text(text, **kwargs)

    def append_or_extend_user_text(self, text: str, **kwargs) -> None:
        """
        Add user text to the message list.
        """
        self.messages.append_or_extend_user_text(text, **kwargs)

    def append_or_extend_user_input(self, user_input: str | list[dict[str, Any]]) -> None:
        """
        Add user input items to the message list.
        """
        self.messages.append_or_extend_user_input(user_input)

    def replace_variables(self, variables: dict[str, Any]) -> None:
        """
        Replace variables throughout the config.
        Handles both system_instruction and all messages.

        Args:
            variables: dict mapping variable names to their values
        """
        # Tripwire: a picklist reference envelope must have been resolved to text by
        # resolve_picklist_references() upstream. If one reaches here, a code path skipped
        # resolution — substitute a safe placeholder (never str(dict)) and record the gap.
        from matrx_ai.config.picklist_runtime import guard_unresolved_refs

        variables = guard_unresolved_refs(variables)
        if self.system_instruction is not None:
            for var_name, var_value in variables.items():
                self.system_instruction.base_instruction = (
                    self.system_instruction.base_instruction.replace(
                        f"{{{{{var_name}}}}}", str(var_value)
                    )
                )

        # Replace in all messages
        self.messages.replace_variables(variables)

    def apply_overrides(self, overrides: LLMParams) -> None:
        """Apply typed config overrides from the API layer.

        Only fields explicitly set (non-None) in `overrides` are applied.
        Unknown fields are impossible because LLMParams uses extra="forbid".

        Complex fields are re-normalized into the runtime shapes ``UnifiedConfig``
        and downstream translators expect (dict response_format, ``CustomTool``
        instances, ``DictionaryConfig``, etc.).
        """
        for key in LLMParams.model_fields:
            value = getattr(overrides, key)
            if value is None:
                continue
            if not hasattr(self, key):
                continue
            normalizer = _OVERRIDE_NORMALIZERS.get(key)
            if normalizer is not None:
                value = normalizer(value)
            setattr(self, key, value)

    def get_last_output(self) -> str:
        """Get the output of the last assistant message."""
        return self.messages.get_last_output()


@dataclass
class UnifiedResponse:
    """Pure LLM response - no AI Matrix specifics"""

    messages: list[UnifiedMessage]
    usage: TokenUsage | None = None
    stop_reason: str | None = None
    finish_reason: str | None = None
    raw_response: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate that usage data is present"""
        if self.usage is None:
            vcprint(
                "⚠️  WARNING: UnifiedResponse missing usage data. This means costs cannot be calculated.",
                color="red",
                log_level="warning",
            )

    def to_dict(self) -> dict[str, Any]:
        result = {}

        for key, value in self.__dict__.items():
            if value is None:
                continue

            if isinstance(value, list) and value and hasattr(value[0], "to_dict"):
                result[key] = [item.to_dict() for item in value]
            elif hasattr(value, "to_dict"):
                result[key] = value.to_dict()
            else:
                result[key] = value

        return result

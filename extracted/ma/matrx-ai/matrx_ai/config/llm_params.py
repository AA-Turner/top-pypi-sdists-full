"""Single source of truth for all LLM configuration parameters.

Every overridable LLM parameter is declared here exactly once. This model is
used by:
  - API request models (config_overrides, ChatRequest inheritance)
  - UnifiedConfig.apply_overrides() for runtime application
  - TypeScript type generation (auto-generated via OpenAPI → openapi-typescript)

When you add a new provider parameter, add it HERE and it propagates
everywhere — Python API validation, TypeScript types, and drift-detection
tests.
"""

from __future__ import annotations

from typing import Any, Literal

from matrx_files.cloud_sync.media_ref import MediaRef
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from matrx_ai.config.custom_tool import CustomTool
from matrx_ai.config.dictionary_config import DictionaryConfig
from matrx_ai.config.llm_wire_types import (
    AspectRatio,
    AudioFormat,
    CompactionSettings,
    ImageLora,
    ImageStyle,
    MediaOutputFormat,
    MediaResolution,
    TtsQuality,
    TtsVoice,
    Verbosity,
)
from matrx_ai.config.response_format import ResponseFormat
from matrx_ai.config.validators import ModelReference, UuidString

# Field aliases — provider-native control names that map to canonical
# UnifiedConfig fields. The agent's settings dict may carry any of these
# names because each model declares its controls using the provider's exact
# field names (per the controls JSONB design). Python normalizes them to
# canonical at construction time so translators only ever read canonical
# UnifiedConfig fields.
#
# Coercion: callers should not have to think about types. `seconds` (string)
# maps to `duration_seconds` (int) with parsing; `n`/`num_outputs`/
# `number_of_images` (int) map to `count` directly.
_FIELD_ALIASES: dict[str, str] = {
    # text-gen
    "max_tokens": "max_output_tokens",
    # image / video count
    "n": "count",
    "num_outputs": "count",
    "number_of_images": "count",
    # OpenAI gpt-image-2 quality knob → canonical render_quality
    "quality": "render_quality",
    # Together video bitrate / quality score → canonical encode_quality
    "output_quality": "encode_quality",
    # video duration: any of these → duration_seconds (int)
    "seconds": "duration_seconds",
    "duration": "duration_seconds",
}

# Aliases whose value needs type coercion (string/etc → int) when remapping.
_FIELD_ALIAS_COERCE_INT: frozenset[str] = frozenset({"seconds", "duration"})


# Truly deprecated aliases — fire a user-facing deprecation warning + log to
# api_field_warnings when present in a request body. Distinct from
# `_FIELD_ALIASES` above, which are canonical provider-native names treated
# silently. Keep this empty unless a name is actually being retired.
#
# Consumed by aidream/api/utils/field_warnings.py and
# aidream/api/routers/chat.py. The host imports it as a public-ish hook so
# new deprecations land in one place.
_DEPRECATED_ALIASES: dict[str, str] = {}


_OPENAPI_DEPRECATED_ALIASES: tuple[str, ...] = (
    "max_tokens",
    "n",
    "num_outputs",
    "number_of_images",
    "quality",
    "output_quality",
    "seconds",
    "duration",
)


def _expose_accepted_aliases_in_json_schema(schema: dict[str, Any]) -> None:
    """Describe already-accepted input aliases without changing model fields.

    Alias normalization happens in ``_remap_aliases`` before Pydantic field
    validation. Keeping these names out of ``model_fields`` is intentional:
    runtime application still sees exactly one canonical field, while OpenAPI
    clients can accurately type legacy/provider-native request payloads.
    """
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return
    for alias in _OPENAPI_DEPRECATED_ALIASES:
        canonical = _FIELD_ALIASES[alias]
        canonical_schema = properties.get(canonical)
        if not isinstance(canonical_schema, dict):
            continue
        alias_schema = dict(canonical_schema)
        alias_schema["title"] = alias.replace("_", " ").title()
        alias_schema["deprecated"] = True
        alias_schema["description"] = (
            f"Deprecated input alias for `{canonical}`. The server normalizes "
            "this name before validation and dispatch; new callers should send "
            f"`{canonical}`."
        )
        alias_schema["x-canonical-name"] = canonical
        properties[alias] = alias_schema


def normalize_max_output_tokens(value: Any) -> Any:
    """Truncate numeric token limits to the integer providers require.

    The frontend and persisted JSONB can supply a JSON number with a fractional
    part. Keep invalid/non-numeric values unchanged so Pydantic still reports
    its normal validation error instead of silently accepting bad input.
    """
    if value is None or isinstance(value, bool | int):
        return value
    if isinstance(value, float | str):
        try:
            return int(float(value))
        except (OverflowError, TypeError, ValueError):
            return value
    return value


class LLMParams(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra=_expose_accepted_aliases_in_json_schema,
    )

    def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault("by_alias", True)
        return super().model_dump(*args, **kwargs)

    @model_validator(mode="before")
    @classmethod
    def _remap_aliases(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        for old_name, new_name in _FIELD_ALIASES.items():
            if old_name not in data:
                continue
            value = data.pop(old_name)
            if value is None:
                continue
            if old_name in _FIELD_ALIAS_COERCE_INT:
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    continue
            if data.get(new_name) is None:
                data[new_name] = value
        return data

    model: ModelReference | None = None

    # OFFERING PIN — an ai.offering uuid pinning the EXACT call (model ×
    # endpoint × api). Resolved exactly or raised loudly; unset = preferred
    # offering by priority. See UnifiedConfig.offering_id.
    offering_id: UuidString | None = None

    max_output_tokens: int | None = None

    @field_validator("max_output_tokens", mode="before")
    @classmethod
    def _normalize_max_output_tokens(cls, value: Any) -> Any:
        return normalize_max_output_tokens(value)

    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None

    tool_choice: Literal["none", "auto", "required"] | None = None
    parallel_tool_calls: bool | None = None

    reasoning_effort: (
        Literal["auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"] | None
    ) = None
    reasoning_summary: Literal["concise", "detailed", "never", "auto", "always"] | None = None

    thinking_level: Literal["minimal", "low", "medium", "high"] | None = None
    include_thoughts: bool | None = None

    thinking_budget: int | None = None

    clear_thinking: bool | None = None
    disable_reasoning: bool | None = None

    response_format: ResponseFormat | None = None
    stop_sequences: list[str] | None = None
    stream: bool | None = None
    store: bool | None = None
    previous_interaction_id: str | None = None
    task: Literal["text_to_video", "image_to_video", "reference_to_video", "edit"] | None = None
    verbosity: Verbosity | None = None

    internal_web_search: bool | None = None
    internal_url_context: bool | None = None
    internal_x_search: bool | None = None

    aspect_ratio: AspectRatio | None = None
    width: int | None = None
    height: int | None = None
    count: int | None = None
    render_quality: Literal["low", "medium", "high", "auto"] | None = None
    background: Literal["auto", "opaque", "transparent"] | None = None
    output_compression: int | None = None
    moderation: Literal["auto", "low"] | None = None
    input_fidelity: Literal["high", "low"] | None = None
    partial_images: int | None = None
    style: ImageStyle | None = None
    reference_strength: float | None = None

    tts_voice: TtsVoice | None = None
    audio_format: AudioFormat | None = None

    duration_seconds: int | None = None
    resolution: MediaResolution | None = None
    fps: int | None = None
    steps: int | None = None
    seed: int | None = None
    guidance_scale: float | None = None
    encode_quality: int | None = None
    negative_prompt: str | None = None
    output_format: MediaOutputFormat | None = None
    frame_images: list[MediaRef] | None = None
    reference_images: list[MediaRef] | None = None
    image_loras: list[ImageLora] | None = None
    disable_safety_checker: bool | None = None
    generate_audio: bool | None = None
    enhance_prompt: bool | None = None

    image_input: MediaRef | None = None
    image_inputs: list[MediaRef] | None = None
    mask: MediaRef | None = None
    last_frame_image: MediaRef | None = None
    video_input: MediaRef | None = None

    video_action: Literal["generate", "edit", "extend"] | None = None

    custom_tools: list[CustomTool] | None = None
    mcp_servers: list[UuidString] | None = None
    compaction_settings: CompactionSettings | None = None
    detected_contexts: dict[str, str] | None = None

    dictionary: DictionaryConfig | None = None
    tts_quality: TtsQuality | None = None

"""Pydantic twin for `UnifiedConfig` (Phase 1b.2). Retirement Ledger row 9.

Shadowed, not swapped. The last and largest contract type: 90 fields, 99
construction sites, 35 `replace`/`fields`/`asdict` call sites.

GENERATED FROM THE DATACLASS, ON PURPOSE. Every other twin in this migration was
written by hand because the corpus disagreed with the annotations and each field
needed a judgement. Here it does not: **56 of 57 observed keys agree with their
declared type** (FIELD_TRUTH §4d, measured across 6,485 stored configs). With
the annotations verified, hand-typing 90 fields adds transcription risk and no
information, so these were emitted from `dataclasses.fields()` and are guarded
by an annotation-equality test rather than by care.

🚨 THE ONE THING THE GENERATOR COULD NOT CARRY — `_unrecognized_keys`.
It is stored in **4,178 of 6,485** config payloads and is NOT a declared field:
`from_dict` sets it by post-construction `setattr`, a dataclass permits that, the
value lands in `__dict__`, and `to_dict()` walks `__dict__`. A pydantic model's
`__dict__` holds only declared fields and a `PrivateAttr` is excluded from
`model_dump()`, so the obvious port SILENTLY stops persisting a key that 4,178
production rows carry, with nothing raising. It is a `PrivateAttr` here and
`to_dict()` below re-includes it explicitly. Preconditions:
`tests/pydantic_migration/test_unified_config_preconditions.py`.

STAGED `Any` FIELDS, all for the same stated reason — the type they hold is not
migrated (or, for `MessageList`, may never be a contract type at all; see
PLAN.md § The last three siblings):
  * `messages` — holds a `MessageList` today, `list[UnifiedMessageModel]` after
    that decision;
  * `system_instruction` — holds a `SystemInstruction` builder, and whether the
    contract is its fields or its rendered output is undecided.

Zero explicit nulls at config level, so every optional field is `X | None = None`
without a permissive wrapper. 33 of the 90 have never been populated — marked
inline, because that is the difference between a field the contract needs and a
field nobody has ever sent.
"""

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from matrx_ai.config.dictionary_config import DictionaryConfig


class UnifiedConfigModel(BaseModel):
    # extra="allow", NOT "forbid" — FIELD_TRUTH §5/§6. Callers send 14
    # undeclared keys on 4.24% of live requests across 23 models; forbidding on
    # day one breaks them. The correct order is allow → record → triage → then
    # forbid behind its own S0→S4. `_unrecognized_keys` already records them.
    model_config = ConfigDict(
        extra="allow",
        validate_assignment=False,
        arbitrary_types_allowed=True,
    )

    model: str
    messages: Any | list[Any] | list[dict[str, Any]]
    system_instruction: str | dict | Any | None = None
    system_prompt_frozen: bool = False
    stream: bool = False
    matrx_model_name: str | None = None
    offering_id: str | None = None  # never populated in 6,485 stored configs
    runtime_offering_id: str | None = None
    prompt_cache_key: str | None = None
    max_output_tokens: int | None = None
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None  # never populated in 6,485 stored configs
    tools: list = Field(default_factory=list)
    authored_tools: list | None = None
    dynamic_tools: list[str] | None = None
    tool_authority_filtered: bool = False
    tool_authority_exclusions: list[str] = Field(default_factory=list)
    tool_authority_filter_applied_runtime: bool = False
    tool_capability_filtered: bool = False
    tool_delegation_filtered: bool = False
    tool_delegation_executors: list[str] | None = None
    tool_delegation_disabled_policy: bool = False
    tool_delegation_registry_fingerprint: str | None = None
    tool_delegation_filter_applied_runtime: bool = False
    tool_choice: Optional[Literal['none', 'auto', 'required']] = None  # never populated in 6,485 stored configs
    parallel_tool_calls: bool = True
    skill_injected_tool_ids: list[str] = Field(default_factory=list)
    supports_tools: bool = True
    custom_tools: list = Field(default_factory=list)
    authored_custom_tools: list | None = None
    reasoning_effort: Optional[Literal['auto', 'none', 'minimal', 'low', 'medium', 'high', 'xhigh', 'max']] = None
    reasoning_summary: Optional[Literal['concise', 'detailed', 'never', 'auto', 'always']] = None
    thinking_level: Optional[Literal['minimal', 'low', 'medium', 'high']] = None
    include_thoughts: bool | None = None
    thinking_budget: int | None = None
    clear_thinking: bool | None = None
    disable_reasoning: bool | None = None
    response_format: dict[str, Any] | None = None
    stop_sequences: list = Field(default_factory=list)
    store: bool | None = None
    previous_interaction_id: str | None = None  # never populated in 6,485 stored configs
    task: Optional[Literal['text_to_video', 'image_to_video', 'reference_to_video', 'edit']] = None  # never populated in 6,485 stored configs
    verbosity: str | None = None
    internal_web_search: bool | None = None
    internal_url_context: bool | None = None
    internal_x_search: bool | None = None  # never populated in 6,485 stored configs
    aspect_ratio: str | None = None
    width: int | None = None  # never populated in 6,485 stored configs
    height: int | None = None  # never populated in 6,485 stored configs
    count: int = 1
    render_quality: Optional[Literal['low', 'medium', 'high', 'auto']] = None  # never populated in 6,485 stored configs
    background: Optional[Literal['auto', 'opaque', 'transparent']] = None
    output_compression: int | None = None  # never populated in 6,485 stored configs
    moderation: Optional[Literal['auto', 'low']] = None
    input_fidelity: Optional[Literal['high', 'low']] = None  # never populated in 6,485 stored configs
    partial_images: int | None = None
    style: str | None = None  # never populated in 6,485 stored configs
    reference_strength: float | None = None  # never populated in 6,485 stored configs
    tts_voice: str | list[dict[str, str]] | None = None
    audio_format: str | None = None
    duration_seconds: int | None = None  # never populated in 6,485 stored configs
    resolution: str | None = None
    fps: int | None = None  # never populated in 6,485 stored configs
    steps: int | None = None  # never populated in 6,485 stored configs
    seed: int | None = None
    guidance_scale: int | None = None  # never populated in 6,485 stored configs
    encode_quality: int | None = None  # never populated in 6,485 stored configs
    negative_prompt: str | None = None  # never populated in 6,485 stored configs
    output_format: str | None = None
    frame_images: list | None = None  # never populated in 6,485 stored configs
    reference_images: list | None = None  # never populated in 6,485 stored configs
    image_loras: list | None = None  # never populated in 6,485 stored configs
    disable_safety_checker: bool | None = None  # never populated in 6,485 stored configs
    generate_audio: bool | None = None  # never populated in 6,485 stored configs
    enhance_prompt: bool | None = None  # never populated in 6,485 stored configs
    image_input: Any | None = None  # never populated in 6,485 stored configs
    image_inputs: list[Any] | None = None  # never populated in 6,485 stored configs
    mask: Any | None = None  # never populated in 6,485 stored configs
    last_frame_image: Any | None = None  # never populated in 6,485 stored configs
    video_input: Any | None = None  # never populated in 6,485 stored configs
    video_action: Optional[Literal['generate', 'edit', 'extend']] = None  # never populated in 6,485 stored configs
    mcp_servers: list[str] = Field(default_factory=list)
    authored_mcp_servers: list[str] | None = None
    compaction_settings: dict[str, Any] | None = None  # never populated in 6,485 stored configs
    detected_contexts: dict[str, str] | None = None  # never populated in 6,485 stored configs
    custom_configs: dict[str, Any] | None = None  # never populated in 6,485 stored configs
    dictionary: DictionaryConfig | dict[str, Any] | None = None
    pronunciation_dictionary_locators: list[dict[str, str]] = Field(default_factory=list)
    tts_quality: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    # Not a field on the dataclass either — set by post-construction setattr in
    # from_dict. Here it must be a PrivateAttr AND re-included by to_dict().
    _unrecognized_keys: list[str] = PrivateAttr(default_factory=list)

    @property
    def unexpected_keys(self) -> list[str]:
        """Twin of `UnifiedConfig.unexpected_keys` — the caller keys this config
        neither declares NOR knowingly passes through.

        Kept in parity with the dataclass on purpose: `_unrecognized_keys` holds
        both populations, so any user-facing consumer must subtract the
        deliberate passthrough set or it reports honoured features as ignored.
        """
        from matrx_ai.config.unified_config import _KNOWN_PASSTHROUGH_KEYS

        return sorted(set(self._unrecognized_keys) - _KNOWN_PASSTHROUGH_KEYS)

    def to_dict(self) -> dict[str, Any]:
        """`UnifiedConfig.to_dict`, reproduced — including the two things that
        would otherwise change the persisted shape:

        1. None is DROPPED, an empty dict is KEPT (same encoding as every other
           shape in this contract, and why the corpus shows zero explicit nulls);
        2. `_unrecognized_keys` is re-included, because a pydantic `__dict__`
           would not carry it and 4,178 stored rows do.
        """
        result: dict[str, Any] = {}

        for key, value in self.__dict__.items():
            if value is None:
                continue
            if isinstance(value, list) and value and hasattr(value[0], "to_dict"):
                result[key] = [item.to_dict() for item in value]
            elif hasattr(value, "to_dict"):
                result[key] = value.to_dict()
            else:
                result[key] = value

        if self._unrecognized_keys:
            result["_unrecognized_keys"] = self._unrecognized_keys

        return result

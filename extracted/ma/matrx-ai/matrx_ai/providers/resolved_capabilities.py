"""The single seam for model capability resolution.

"What can this model do" is decided by ONE source: the ``capabilities`` jsonb on
the model row (``ai.model_definition.capabilities``), optionally overlaid — per
top-level key — by the routing offering's ``capabilities_override``.

  ``resolve_model_capabilities(model_data, capabilities_override=...) -> ResolvedModelCapabilities``

The jsonb shape is ``{input, output, features, interaction, multilingual}``.
Every consumer (routing gates, tool injection, audio/vision preprocessing,
structured-output negotiation) reads the typed object, never the raw column.
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from matrx_ai.providers.capability_vocabulary import (
    INTERACTION_MODES,
    VOCABULARY_FILE,
    normalize_capabilities,
)

logger = logging.getLogger(__name__)

#: One scream per (model, problem) per process — this resolver runs on every
#: request against cached rows.
_reported_drift: set[str] = set()

# The known NATIVE / INTERNAL provider tools — provider-hosted capabilities the
# API exposes internally, NOT generic function-calling/tools. A model/provider can
# have SEVERAL, so this is modeled as a SET, never a single boolean (the correction
# behind this field): web search is just one member.
#   web_search     — hosted web search (OpenAI web_search_preview · Google googleSearch · xAI)
#   x_search       — xAI native X/Twitter search (xAI ONLY — the sole path to X data)
#   url_context    — Google URL-context grounding (Google only)
#   code_execution — provider-side code execution (Google)
# Tokens match the jsonb `features` vocabulary.
NATIVE_PROVIDER_CAPABILITIES: frozenset[str] = frozenset(
    {"web_search", "x_search", "url_context", "code_execution"}
)


class StructuredOutputMode(str, Enum):
    SCHEMA = "schema"  # json_schema (STRUCTURED_OUTPUT)
    JSON = "json"  # json_object (JSON_MODE)
    TEXT = "text"  # neither — free text only


class ResolvedModelCapabilities(BaseModel):
    # ``model_`` is a Pydantic-protected namespace; we deliberately use model_name.
    model_config = ConfigDict(frozen=True, protected_namespaces=())

    model_name: str
    # INPUT modalities
    supports_text_input: bool
    supports_vision: bool  # accepts image input
    supports_audio_input: bool  # accepts audio directly (vs transcribe-first)
    # OUTPUT modalities
    produces_text: bool
    produces_image: bool
    produces_video: bool
    produces_audio: bool  # TTS
    produces_embedding: bool
    # Multi-voice dialogue synthesis (ElevenLabs text_to_dialogue). Data-driven:
    # the model row declares "dialogue" in `features`; a TTS model WITHOUT it is
    # routed through the plain text-to-speech endpoint (eleven_flash_v2_5 rejects
    # the dialogue API outright). Never gate this on a model-name list in code.
    supports_dialogue: bool = False
    # tool / search axes
    supports_function_calling: bool  # THE gate for ALL tool injection
    supports_web_search: bool
    # The SET of native/internal provider tools this model declares (web_search,
    # x_search, url_context, code_execution). ``supports_web_search`` is just the
    # ``web_search`` member, surfaced as a boolean for the hot gate.
    native_capabilities: frozenset[str]
    # output-format negotiation: json_schema (SCHEMA) > json_object (JSON) > free text.
    structured_output_mode: StructuredOutputMode
    # The FULL live vocabulary. It was ["turn","realtime","extraction",
    # "embedding"] until 2026-09-12, which silently coerced the 9 rows declaring
    # "single" (one-shot image/video generation) or "agent" (provider-managed
    # background agent) into "turn" — the same silent-narrowing class as the
    # features drift, found by census rather than by a report.
    interaction: Literal["turn", "single", "extraction", "realtime", "embedding", "agent"]
    multilingual: bool


class _DeclaredCapabilities(BaseModel):
    model_config = ConfigDict(frozen=True)

    input: frozenset[str]
    output: frozenset[str]
    features: frozenset[str]
    interaction: Literal["turn", "single", "extraction", "realtime", "embedding", "agent"]
    multilingual: bool


def _str_set(value: Any) -> frozenset[str]:
    if isinstance(value, list | tuple | set | frozenset):
        return frozenset(str(v).strip().lower() for v in value if isinstance(v, str))
    return frozenset()


def _report_drift(model_name: str, problems: list[str]) -> None:
    """SCREAM about a stored capabilities value outside the canonical vocabulary.

    The write path (the agent `sql`/`db_*` tools, `scripts/set_model_capabilities.py`)
    refuses these now, so anything reaching here predates the guard or arrived
    through a door we do not own — e.g. a direct Supabase write from an admin
    surface. Silently resolving around it is how `structured_outputs` turned
    schema output OFF for gpt-6-astra without a single server-side signal.
    """
    for problem in problems:
        key = f"{model_name}|{problem}"
        if key in _reported_drift:
            continue
        _reported_drift.add(key)
        logger.error(
            "ai.model_definition.capabilities drift on model %s: %s — not in the canonical "
            "vocabulary (%s). Fix the ROW; resolution below uses only what it recognizes.",
            model_name or "<unknown>",
            problem,
            VOCABULARY_FILE,
        )


def _parse_declared(raw: Any, model_name: str = "") -> _DeclaredCapabilities:
    # The jsonb is a structured dict {input,output,features,interaction,multilingual}.
    # A list (the OLD misinterpretation), None, or any non-dict contributes nothing —
    # tolerant by design (this exact mis-iteration masked the column for months).
    if not isinstance(raw, dict):
        raw = {}
    # Normalize provider spellings the same way the write path does, so a row
    # that predates the write guard still RESOLVES correctly instead of losing
    # the capability — and scream either way. Correcting on read is a stand-in,
    # never a substitute for repairing the row.
    checked = normalize_capabilities(raw, label=model_name)
    if checked.corrections or checked.rejections:
        _report_drift(model_name, checked.corrections + checked.rejections)
    normalized = checked.value if isinstance(checked.value, dict) else {}

    interaction = normalized.get("interaction")
    if interaction not in INTERACTION_MODES:
        interaction = "turn"
    return _DeclaredCapabilities(
        input=_str_set(normalized.get("input")),
        output=_str_set(normalized.get("output")),
        features=_str_set(normalized.get("features")),
        interaction=interaction,
        multilingual=bool(normalized.get("multilingual", False)),
    )


def _structured_mode(features: frozenset[str]) -> StructuredOutputMode:
    if "structured_output" in features:
        return StructuredOutputMode.SCHEMA
    if "json_mode" in features:
        return StructuredOutputMode.JSON
    return StructuredOutputMode.TEXT


def resolve_model_capabilities(
    model_data: Any, *, capabilities_override: dict[str, Any] | None = None
) -> ResolvedModelCapabilities:
    """Return the typed capability object for ``model_data``.

    ``capabilities_override`` is the routing offering's sparse override: a
    SHALLOW per-top-level-key merge (``input`` / ``output`` / ``features`` /
    ``interaction`` / ``multilingual``), offering wins. A key it does not name is
    taken from the model row untouched.
    """
    raw = getattr(model_data, "capabilities", None)
    merged: dict[str, Any] = dict(raw) if isinstance(raw, dict) else {}
    if capabilities_override:
        merged.update(capabilities_override)

    declared = _parse_declared(merged, getattr(model_data, "name", "") or "")
    return ResolvedModelCapabilities(
        model_name=getattr(model_data, "name", "") or "",
        supports_text_input="text" in declared.input,
        supports_vision="image" in declared.input,
        supports_audio_input="audio" in declared.input,
        produces_text="text" in declared.output,
        produces_image="image" in declared.output,
        produces_video="video" in declared.output,
        produces_audio="audio" in declared.output,
        produces_embedding="embedding" in declared.output,
        supports_dialogue="dialogue" in declared.features,
        supports_function_calling="function_calling" in declared.features,
        supports_web_search="web_search" in declared.features,
        native_capabilities=frozenset(declared.features & NATIVE_PROVIDER_CAPABILITIES),
        structured_output_mode=_structured_mode(declared.features),
        interaction=declared.interaction,
        multilingual=declared.multilingual,
    )


__all__ = [
    "StructuredOutputMode",
    "ResolvedModelCapabilities",
    "NATIVE_PROVIDER_CAPABILITIES",
    "resolve_model_capabilities",
]

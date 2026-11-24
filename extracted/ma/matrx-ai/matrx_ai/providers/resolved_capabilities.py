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

import asyncio
import inspect
import logging
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict

from matrx_ai.media.image_reference_roles import normalize_limits
from matrx_ai.media.video_reference_roles import normalize_video_limits
from matrx_ai.providers.capability_vocabulary import (
    INTERACTION_MODES,
    VOCABULARY_FILE,
    InteractionMode,
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
    # Accepts video input (a live model reads camera frames as video: Gemini Live). Separate from
    # ``supports_vision`` because a video-only model cannot take a still image in a chat turn.
    supports_video_input: bool = False
    # OUTPUT modalities
    produces_text: bool
    produces_image: bool
    produces_video: bool
    produces_audio: bool  # TTS
    produces_embedding: bool
    produces_decision: bool
    # Multi-voice dialogue synthesis (ElevenLabs text_to_dialogue). Data-driven:
    # the model row declares "dialogue" in `features`; a TTS model WITHOUT it is
    # routed through the plain text-to-speech endpoint (eleven_flash_v2_5 rejects
    # the dialogue API outright). Never gate this on a model-name list in code.
    supports_dialogue: bool = False
    # The model continues a trailing assistant message (response prefill).
    # Declared per model as the ``assistant_prefill`` feature — Anthropic removed
    # it on Sonnet 5 / Opus 5 / Fable / the 4.6-4.8 line (400 "This model does
    # not support assistant message prefill"), so it is data, never a name check.
    # Read by ``matrx_ai.config.message_flags``.
    supports_assistant_prefill: bool = False
    # The model REJECTS two user-role turns in a row — declared per model as the
    # ``strict_role_alternation`` feature only after a live probe proved it (lane
    # L29, 2026-10-18: every active Groq/Cerebras/Together/Moonshot chat offering
    # accepted user, user). Read by ``BaseTranslator.place_trailing_on_chat_messages``.
    requires_strict_role_alternation: bool = False
    # The provider continues an answer past one call's output limit (the ``long_decode``
    # feature; Gemini 4 Argon). Without it a Gemini call is always exactly one call.
    supports_long_decode: bool = False
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
    interaction: InteractionMode
    multilingual: bool
    # Image-generation reference roles this model takes: {role: max, "total": n}.
    # Empty = no roled reference image is accepted (the gate refuses).
    image_reference_limits: dict[str, int] = {}
    # Video-generation inputs this model takes: {extend|restyle|lip_sync|named: max}.
    video_reference_limits: dict[str, int] = {}
    # ``ai.model_definition.cost_rating`` (1..6, 6 the top tier; None = unrated). Read only by
    # the call-time layer's small-model tool limit (``small_model_tools.py``), never the core.
    model_cost_rating: int | None = None


def _model_cost_rating(model_data: Any) -> int | None:
    raw = (
        model_data.get("cost_rating")
        if isinstance(model_data, dict)
        else getattr(model_data, "cost_rating", None)  # orm-getattr-ok: generated model row
    )
    if raw is None or isinstance(raw, bool):
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


class _DeclaredCapabilities(BaseModel):
    model_config = ConfigDict(frozen=True)

    input: frozenset[str]
    output: frozenset[str]
    features: frozenset[str]
    interaction: InteractionMode
    multilingual: bool
    image_reference_limits: dict[str, int] = {}
    video_reference_limits: dict[str, int] = {}


def _str_set(value: Any) -> frozenset[str]:
    if isinstance(value, list | tuple | set | frozenset):
        return frozenset(str(v).strip().lower() for v in value if isinstance(v, str))
    return frozenset()


def _file_unknown_capability(model_name: str, problems: list[str]) -> None:
    """File ONE open system_error per model for capability values nobody has a word for.

    A row written around the server's write check (2026-11-18: rerank-v4.0-pro inserted by
    a migration applied through the Supabase MCP with interaction "rerank") was caught only
    by the frontend parser on admin pages. Every server process resolves every row on
    catalog load, so this is the scan: grouped per model across processes
    (``group_open``), never one row per process.
    """
    try:
        from matrx_ai._ext import get_ext, has_ext

        if not has_ext("record_error"):
            return
        record_error = get_ext("record_error")
        error = RuntimeError(
            f"ai.model_definition {model_name or '<unknown>'}: capabilities value(s) outside the "
            f"vocabulary, read as the default until named in {VOCABULARY_FILE} (and its TS twin) "
            f"or the row is fixed: {'; '.join(problems)}"
        )
        fields = {
            "kind": "ai_model_capability_drift",
            "route": f"matrx_ai.providers.resolved_capabilities/{model_name or '<unknown>'}",
            "error_type": "CapabilityVocabularyDrift",
            "payload": {"model": model_name, "problems": problems},
        }
        try:
            pending = record_error(error, group_open=True, **fields)
        except TypeError:
            pending = record_error(error, **fields)
        if inspect.isawaitable(pending):
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                pending.close()
                return
            from matrx_utils import detached_task

            detached_task(pending, name="ai_model_capability_drift")
    except Exception:  # noqa: BLE001 — a broken alarm never breaks a capability resolve
        return


def _report_drift(model_name: str, problems: list[str], *, unknown: list[str] | None = None) -> None:
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
    fresh = [p for p in (unknown or []) if f"{model_name}|filed|{p}" not in _reported_drift]
    if fresh:
        _reported_drift.update(f"{model_name}|filed|{p}" for p in fresh)
        _file_unknown_capability(model_name, fresh)


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
        _report_drift(model_name, checked.corrections + checked.rejections, unknown=checked.rejections)
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
        image_reference_limits=normalize_limits(normalized.get("image_reference_roles")),
        video_reference_limits=normalize_video_limits(normalized.get("video_reference_roles")),
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
        supports_video_input="video" in declared.input,
        produces_text="text" in declared.output,
        produces_image="image" in declared.output,
        produces_video="video" in declared.output,
        produces_audio="audio" in declared.output,
        produces_embedding="embedding" in declared.output,
        produces_decision="decision" in declared.output,
        supports_dialogue="dialogue" in declared.features,
        supports_assistant_prefill="assistant_prefill" in declared.features,
        requires_strict_role_alternation="strict_role_alternation" in declared.features,
        supports_long_decode="long_decode" in declared.features,
        supports_function_calling="function_calling" in declared.features,
        supports_web_search="web_search" in declared.features,
        native_capabilities=frozenset(declared.features & NATIVE_PROVIDER_CAPABILITIES),
        structured_output_mode=_structured_mode(declared.features),
        interaction=declared.interaction,
        multilingual=declared.multilingual,
        image_reference_limits=dict(declared.image_reference_limits),
        video_reference_limits=dict(declared.video_reference_limits),
        model_cost_rating=_model_cost_rating(model_data),
    )


__all__ = [
    "StructuredOutputMode",
    "ResolvedModelCapabilities",
    "NATIVE_PROVIDER_CAPABILITIES",
    "resolve_model_capabilities",
]

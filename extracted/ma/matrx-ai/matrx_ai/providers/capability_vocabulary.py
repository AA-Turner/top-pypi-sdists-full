"""THE canonical vocabulary for ``ai.model_definition.capabilities``.

One list, one place. Everything that WRITES the column validates through
``normalize_capabilities`` here; everything that READS it (
``resolved_capabilities.resolve_model_capabilities``, the frontend parser in
``matrx-frontend/features/ai-models/capabilities/types.ts``) shares this
vocabulary.

Why this module exists (2026-09-12): the model-sync agent inserted four new
rows carrying provider-documentation spellings —  ``structured_outputs``,
``reasoning``, ``code_interpreter``, ``batch``, ``pdf_input`` — straight into
``capabilities.features`` through the generic ``sql`` tool. Nothing on the
write path knew the vocabulary, so the rows landed. The damage was NOT
cosmetic: ``_structured_mode`` matches the literal ``structured_output``, so
``gpt-6-astra`` resolved to ``StructuredOutputMode.TEXT`` — schema-mode
structured output silently OFF for a flagship model — and the frontend
screamed "unknown value, ignored" eight times on the agent builder.

Two kinds of non-canonical value, two different answers:

* An ALIAS (a provider's own spelling of a capability we already have a word
  for) is NORMALIZED, loudly, and the correction is reported to the caller.
  Provider docs will keep producing these; rejecting them would just make the
  sync agent guess.
* A genuinely UNKNOWN value is REJECTED at the write. It means the platform
  has gained a capability nobody has named yet; the fix is to add the term
  here (and to the frontend list), never to let the column drift.

``pdf_input`` is a third class: a provider listing an INPUT MODALITY inside
its feature list. It is relocated to ``input`` as ``document``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# ── the vocabulary ────────────────────────────────────────────────────────

CONTENT_TYPES: frozenset[str] = frozenset(
    {"text", "image", "audio", "video", "document", "entities", "embedding"}
)

INTERACTION_MODES: frozenset[str] = frozenset(
    {"turn", "single", "extraction", "realtime", "embedding", "agent"}
)

#: Every feature token the canonical column may carry. Keep in lockstep with
#: ``FEATURE_KEYS`` in matrx-frontend/features/ai-models/capabilities/types.ts;
#: ``scripts/check_model_capability_vocabulary.py`` proves the live DB conforms.
FEATURE_KEYS: frozenset[str] = frozenset(
    {
        "streaming",
        "function_calling",
        "tool_calling",
        "thinking",
        "structured_output",
        "json_mode",
        "web_search",
        "x_search",
        "vision",
        "code_execution",
        "computer_use",
        "multi_turn",
        "system_prompt",
        "embeddings",
        "dimension_reduction",
        "fine_tuning",
        "batch_api",
        "prompt_caching",
        "context_caching",
        # Anthropic context editing / tool-result clearing: the model manages
        # what stays in its own context window. Distinct from the two caching
        # features, which are about billing and latency, not retention.
        "context_management",
        "partial_mode",
        # Extraction family (GLiNER2 / fastino models)
        "ner",
        "classification",
        "structured_extraction",
        "relation_extraction",
        "pii_detection",
        # Media generation / editing
        "image_generation",
        "image_editing",
        # Mask-based region editing. A model can edit a whole image without
        # accepting a mask, so this is not the same declaration as image_editing.
        "inpainting",
        "image_to_video",
        "video_generation",
        "video_editing",
        "audio_generation",
        "conversational_editing",
        "stateful_editing",
        "dialogue",
        # Provider-managed agents / hosted tools
        "file_search",
        "mcp",
        "background_execution",
        "collaborative_planning",
        "visualization",
        "citations",
        "sandboxed_execution",
        # Google live, grounding, embedding, and music families
        "live_api",
        "url_context",
        "grounding_maps",
        "multimodal_embedding",
        "music_generation",
        "real_time_translation",
    }
)

#: Provider spelling -> canonical feature token. Additive only: never map two
#: capabilities that genuinely differ onto one token.
FEATURE_ALIASES: dict[str, str] = {
    "structured_outputs": "structured_output",  # OpenAI docs
    "reasoning": "thinking",  # OpenAI / xAI docs
    "code_interpreter": "code_execution",  # OpenAI hosted tool
    "batch": "batch_api",  # Anthropic / OpenAI docs
    "websearch": "web_search",
    "web_search_preview": "web_search",  # OpenAI tool name
    "extended_thinking": "thinking",  # Anthropic docs
    "caching": "prompt_caching",
    "json_object": "json_mode",
    "tools": "function_calling",
}

#: A feature token that is really an INPUT modality -> the content type it means.
FEATURE_TO_INPUT_MODALITY: dict[str, str] = {
    "pdf_input": "document",
    "document_input": "document",
    "image_input": "image",
    "audio_input": "audio",
    "video_input": "video",
}

#: Provider spelling -> canonical content type (input and output alike).
CONTENT_TYPE_ALIASES: dict[str, str] = {
    "img": "image",
    "images": "image",
    "pdf": "document",
    "documents": "document",
    "txt": "text",
    "embeddings": "embedding",
}

INTERACTION_ALIASES: dict[str, str] = {
    "chat": "turn",
    "one_shot": "single",
    "oneshot": "single",
}

CANONICAL_KEYS: frozenset[str] = frozenset(
    {"input", "output", "features", "interaction", "multilingual"}
)

VOCABULARY_FILE = "matrx_ai/providers/capability_vocabulary.py"


# ── normalization ─────────────────────────────────────────────────────────


@dataclass
class CapabilitiesNormalization:
    """The result of validating one ``capabilities`` value.

    ``corrections`` are things we fixed and the caller must be told about;
    ``rejections`` are values nobody has a word for — the write must fail.
    """

    value: dict[str, Any]
    corrections: list[str] = field(default_factory=list)
    rejections: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.rejections

    def rejection_message(self) -> str:
        return (
            "capabilities holds value(s) outside the canonical vocabulary: "
            + "; ".join(self.rejections)
            + f". Add the term to {VOCABULARY_FILE} (and the matching FEATURE_KEYS "
            "list in matrx-frontend/features/ai-models/capabilities/types.ts), or "
            "use the canonical spelling. The column is never allowed to drift."
        )


def _tokens(
    raw: Any, *, field: str, where: str, rejections: list[str]
) -> list[str]:
    """Return normalized tokens without silently turning malformed data into none.

    A capability collection is persisted configuration, not permissive request
    input.  Dropping a scalar alias, nested object, or non-string member would
    make the generic write guard acknowledge a successful write while erasing
    a declared capability.  Keep processing valid siblings for diagnostics,
    but mark the whole value rejected so callers do not persist that partial
    projection.
    """
    if not isinstance(raw, (list, tuple, set, frozenset)):
        rejections.append(
            f"{field}{where} must be a collection of non-empty strings, got {type(raw).__name__}"
        )
        return []

    tokens: list[str] = []
    for index, value in enumerate(raw):
        if not isinstance(value, str):
            rejections.append(
                f"{field}[{index}]{where} must be a non-empty string, got {type(value).__name__}"
            )
            continue
        token = value.strip().lower()
        if not token:
            rejections.append(f"{field}[{index}]{where} must be a non-empty string")
            continue
        tokens.append(token)
    return tokens


def normalize_capabilities(raw: Any, *, label: str = "") -> CapabilitiesNormalization:
    """Validate and canonicalize a ``capabilities`` value.

    Returns the canonical dict plus what was corrected and what cannot be
    accepted. Never raises, never mutates ``raw``; callers decide whether a
    rejection blocks their write.
    """
    where = f" on {label}" if label else ""
    if not isinstance(raw, dict):
        # A non-dict is the pre-canonical shape class the 2026-07 backfill
        # killed; it is a rejection, not something to guess our way through.
        return CapabilitiesNormalization(
            value={},
            rejections=[
                f"capabilities{where} is {type(raw).__name__}, not the canonical "
                "{input, output, features, interaction, multilingual} object"
            ],
        )

    out: dict[str, Any] = dict(raw)
    corrections: list[str] = []
    rejections: list[str] = []

    for key in raw:
        if key not in CANONICAL_KEYS:
            rejections.append(f"unknown top-level key {key!r}{where}")

    # features — alias, relocate modalities, reject the rest
    extra_inputs: list[str] = []
    features: list[str] = []
    for token in _tokens(
        raw.get("features", []), field="features", where=where, rejections=rejections
    ):
        if token in FEATURE_KEYS:
            canonical = token
        elif token in FEATURE_ALIASES:
            canonical = FEATURE_ALIASES[token]
            corrections.append(f"features {token!r} -> {canonical!r}{where}")
        elif token in FEATURE_TO_INPUT_MODALITY:
            modality = FEATURE_TO_INPUT_MODALITY[token]
            extra_inputs.append(modality)
            corrections.append(
                f"features {token!r} is an input modality -> input {modality!r}{where}"
            )
            continue
        else:
            rejections.append(f"features {token!r}{where}")
            continue
        if canonical not in features:
            features.append(canonical)
    out["features"] = features

    for key in ("input", "output"):
        members: list[str] = []
        for token in _tokens(
            raw.get(key, []), field=key, where=where, rejections=rejections
        ):
            if token in CONTENT_TYPES:
                canonical = token
            elif token in CONTENT_TYPE_ALIASES:
                canonical = CONTENT_TYPE_ALIASES[token]
                corrections.append(f"{key} {token!r} -> {canonical!r}{where}")
            else:
                rejections.append(f"{key} {token!r}{where}")
                continue
            if canonical not in members:
                members.append(canonical)
        if key == "input":
            for modality in extra_inputs:
                if modality not in members:
                    members.append(modality)
        out[key] = members

    interaction = raw.get("interaction")
    if isinstance(interaction, str):
        token = interaction.strip().lower()
        if token in INTERACTION_MODES:
            out["interaction"] = token
        elif token in INTERACTION_ALIASES:
            out["interaction"] = INTERACTION_ALIASES[token]
            corrections.append(f"interaction {token!r} -> {out['interaction']!r}{where}")
        else:
            rejections.append(f"interaction {token!r}{where}")
    elif interaction is not None:
        rejections.append(f"interaction {interaction!r}{where}")

    multilingual = raw.get("multilingual")
    if multilingual is not None and not isinstance(multilingual, bool):
        rejections.append(f"multilingual {multilingual!r}{where} is not a boolean")

    return CapabilitiesNormalization(value=out, corrections=corrections, rejections=rejections)


__all__ = [
    "CONTENT_TYPES",
    "CONTENT_TYPE_ALIASES",
    "CANONICAL_KEYS",
    "FEATURE_ALIASES",
    "FEATURE_KEYS",
    "FEATURE_TO_INPUT_MODALITY",
    "INTERACTION_ALIASES",
    "INTERACTION_MODES",
    "VOCABULARY_FILE",
    "CapabilitiesNormalization",
    "normalize_capabilities",
]

"""Vision-class registry — the image RE-ENCODING profile, not a capability.

A "vision class" is a named bundle of image-processing parameters (long edge,
JPEG quality, byte ceiling, the provider's own resolution hint) used to re-encode
an arbitrary master screenshot/image for one LLM family. It answers "how should
these bytes be encoded for this model", NEVER "can this model see" — that is
capability DATA (``ResolvedModelCapabilities.supports_vision``, from the model's
``capabilities`` jsonb) and lives nowhere near this file.

Resolution order (highest to lowest priority):

1. Explicit ``MediaRef.vision_class`` set by the caller (e.g. eager render
   on /media/upload, or a frontend that pins a specific variant).
2. Per-model mapping (``MODEL_TO_VISION_CLASS``) — maps full model names
   like ``claude-opus-4-7`` to a class name; the per-model tier tuning.
3. Per-wire-route default (``WIRE_FORMAT_DEFAULT_VISION_CLASS``) — maps the
   catalog's ``ai.api.translator_key`` (the profile's ``wire_format``) to the provider family's profile.
4. ``unknown_default`` — the safest fallback (1568 / q=85, fits every
   provider's per-image cap).

Numbers below mirror the spec at
``packages/matrx-ai/matrx_ai/config/tool_config_image_processing_spec.md``
verbatim. Update both files together.
"""

from __future__ import annotations

from dataclasses import dataclass

_FIVE_MB = 5 * 1024 * 1024
_TWENTY_MB = 20 * 1024 * 1024


@dataclass(frozen=True)
class VisionApiClass:
    """A named bundle of image re-encoding parameters for one model family."""

    name: str
    long_edge: int
    quality: int
    format: str = "JPEG"
    subsampling: int = 2  # 0 = 4:4:4, 2 = 4:2:0
    progressive: bool = True
    optimize: bool = True
    provider_hint: str | None = None
    max_bytes: int = _FIVE_MB
    min_quality: int = 60


VISION_API_CLASSES: dict[str, VisionApiClass] = {
    "anthropic_opus_hires": VisionApiClass(
        name="anthropic_opus_hires",
        long_edge=2576,
        quality=88,
        provider_hint=None,
        max_bytes=_FIVE_MB,
    ),
    "anthropic_sonnet_default": VisionApiClass(
        name="anthropic_sonnet_default",
        long_edge=1568,
        quality=85,
        provider_hint=None,
        max_bytes=_FIVE_MB,
    ),
    "anthropic_haiku_default": VisionApiClass(
        name="anthropic_haiku_default",
        long_edge=1568,
        quality=85,
        provider_hint=None,
        max_bytes=_FIVE_MB,
    ),
    "openai_original": VisionApiClass(
        name="openai_original",
        long_edge=2048,
        quality=85,
        provider_hint="original",
        max_bytes=_TWENTY_MB,
    ),
    "openai_high": VisionApiClass(
        name="openai_high",
        long_edge=2048,
        quality=85,
        provider_hint="high",
        max_bytes=_TWENTY_MB,
    ),
    "openai_low": VisionApiClass(
        name="openai_low",
        long_edge=512,
        quality=75,
        provider_hint="low",
        max_bytes=_TWENTY_MB,
    ),
    "gemini3_high": VisionApiClass(
        name="gemini3_high",
        long_edge=1536,
        quality=85,
        provider_hint="MEDIA_RESOLUTION_HIGH",
        max_bytes=_TWENTY_MB,
    ),
    "gemini3_low": VisionApiClass(
        name="gemini3_low",
        long_edge=768,
        quality=80,
        provider_hint="MEDIA_RESOLUTION_LOW",
        max_bytes=_TWENTY_MB,
    ),
    "gemini25_default": VisionApiClass(
        name="gemini25_default",
        long_edge=1536,
        quality=85,
        provider_hint=None,
        max_bytes=_TWENTY_MB,
    ),
    "unknown_default": VisionApiClass(
        name="unknown_default",
        long_edge=1568,
        quality=85,
        provider_hint=None,
        max_bytes=_FIVE_MB,
    ),
}


# ---------------------------------------------------------------------------
# Per-model mapping. Match on canonical model names — the resolver lower-cases
# the input and tries (a) exact match, (b) a few well-known prefixes.
# ---------------------------------------------------------------------------
MODEL_TO_VISION_CLASS: dict[str, str] = {
    # Anthropic Claude family
    "claude-opus-4-7": "anthropic_opus_hires",
    "claude-opus-4-5": "anthropic_opus_hires",
    "claude-sonnet-4-6": "anthropic_sonnet_default",
    "claude-sonnet-4-5": "anthropic_sonnet_default",
    "claude-haiku-4-5": "anthropic_haiku_default",
    "claude-3-5-sonnet": "anthropic_sonnet_default",
    "claude-3-5-haiku": "anthropic_haiku_default",
    # OpenAI GPT-5 family
    "gpt-5.5": "openai_original",
    "gpt-5.4": "openai_original",
    "gpt-5.2": "openai_high",
    "gpt-5": "openai_high",
    "gpt-5-mini": "openai_high",
    "gpt-5-nano": "openai_low",
    "gpt-4o": "openai_high",
    "gpt-4o-mini": "openai_high",
    "o3": "openai_high",
    "o4": "openai_high",
    # Google Gemini 3
    "gemini-3-pro": "gemini3_high",
    "gemini-3-flash": "gemini3_high",
    # Google Gemini 2.5
    "gemini-2.5-pro": "gemini25_default",
    "gemini-2.5-flash": "gemini25_default",
    # The ONE vision-capable Cerebras model: Cerebras added native image input
    # exclusively for gemma-4-31b (base64 data URIs, up to 5 images/request).
    # Cerebras is OpenAI-compatible, so it re-encodes with the OpenAI profile
    # rather than the cerebras_chat default.
    # Source: cerebras.ai/blog/gemma-4-on-cerebras + inference-docs.cerebras.ai/capabilities/image-inputs
    "gemma-4-31b": "openai_high",
}


# ---------------------------------------------------------------------------
# Per-wire-route default. Keys are ``ai.api.translator_key`` values from the
# catalog (the same tokens as UnifiedAIClient's dispatch attrs). This is the
# provider family's encoding profile; a specific model overrides it above.
#
# Routes with no entry (tts / image / video / extraction / realtime) never carry
# image INPUT, so they fall through to ``unknown_default`` and nothing re-encodes.
# ---------------------------------------------------------------------------
WIRE_FORMAT_DEFAULT_VISION_CLASS: dict[str, str] = {
    "anthropic_chat": "anthropic_sonnet_default",
    "openai_chat": "openai_high",
    "google_chat": "gemini25_default",
    "cerebras_chat": "openai_high",  # OpenAI-compatible wire
    "xai_chat": "openai_high",
    "generic_openai_chat": "openai_high",
    "huggingface_chat": "openai_high",
    "groq_chat": "openai_high",
    "together_chat": "openai_high",
    "mock_chat": "unknown_default",
}


def _normalise_model_name(model: str | None) -> str | None:
    if not model:
        return None
    return model.strip().lower()


def resolve_vision_class(
    model: str | None,
    wire_format: str | None = None,
) -> VisionApiClass:
    """Resolve the image re-encoding profile for a model on a wire route.

    Callers gate on ``ResolvedModelCapabilities.supports_vision`` BEFORE reaching
    here — this function assumes bytes are going to be sent and only decides how
    to encode them.

    Resolution order:
      1. Exact match on ``MODEL_TO_VISION_CLASS``.
      2. Prefix match on ``MODEL_TO_VISION_CLASS`` (the longest prefix wins
         so ``claude-opus-4-7-20251201`` still hits ``claude-opus-4-7``).
      3. ``WIRE_FORMAT_DEFAULT_VISION_CLASS[wire_format]``.
      4. ``unknown_default``.
    """
    name = _normalise_model_name(model)

    if name and name in MODEL_TO_VISION_CLASS:
        return VISION_API_CLASSES[MODEL_TO_VISION_CLASS[name]]

    if name:
        prefix_hits = [k for k in MODEL_TO_VISION_CLASS if name.startswith(k)]
        if prefix_hits:
            best = max(prefix_hits, key=len)
            return VISION_API_CLASSES[MODEL_TO_VISION_CLASS[best]]

    wf = wire_format.strip().lower() if wire_format else None
    route_default = WIRE_FORMAT_DEFAULT_VISION_CLASS.get(wf) if wf else None
    if route_default is not None:
        return VISION_API_CLASSES[route_default]

    return VISION_API_CLASSES["unknown_default"]


def is_known_vision_class(name: str | None) -> bool:
    """True iff ``name`` is a registered vision-class key."""
    return bool(name) and name in VISION_API_CLASSES


__all__ = [
    "VisionApiClass",
    "VISION_API_CLASSES",
    "MODEL_TO_VISION_CLASS",
    "WIRE_FORMAT_DEFAULT_VISION_CLASS",
    "resolve_vision_class",
    "is_known_vision_class",
]

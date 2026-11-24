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

import re
from dataclasses import dataclass
from typing import Any

_FIVE_MB = 5 * 1024 * 1024
_SIXTEEN_MIB = 16 * 1024 * 1024
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
    #: Shortest side the provider ACCEPTS (0 = no floor). A route with a floor
    #: rejects smaller images instead of upscaling them, so
    #: ``fit_for_vision_class`` upscales, or pads when upscaling would break
    #: ``long_edge``.
    min_edge: int = 0


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
    # A Gemini 2.x COMPUTER-USE model (catalog ``capabilities.features`` holds ``computer_use``): it TILES a
    # picture instead of the flat 258 (CGU-10 AND-IMG11; ``countTokens`` on 25 sizes, 2026-11-11 —
    # 258 / 1,290 / 1,806 / 3,354 …; ``image_tokens._gemini_tiled_tokens`` is the rule). Like every 2.x it
    # refuses a per-picture ``mediaResolution``.
    "gemini25_tiled": VisionApiClass(
        name="gemini25_tiled",
        long_edge=1536,
        quality=85,
        provider_hint=None,
        max_bytes=_TWENTY_MB,
    ),
    # A picture-MAKING Gemini of any generation (Nano Banana, ``*-image``, omni video): it counts a
    # picture at a flat 258 like 2.5 and REFUSES a per-picture ``mediaResolution`` (400, measured
    # 2026-11-11 on gemini-3.1-flash-image, gemini-3-pro-image, gemini-nano-banana-2.1 and both omni).
    "gemini_media_maker": VisionApiClass(
        name="gemini_media_maker",
        long_edge=1536,
        quality=85,
        provider_hint=None,
        max_bytes=_TWENTY_MB,
    ),
    # TypeSafe Jev (docs.typesafe.ai/images.md): PNG/JPEG, each side 280-1568 px,
    # 16 MiB per file, metadata stripped and EXIF orientation NOT applied, and
    # an out-of-range image is rejected, never resized. Baseline JPEG is their
    # safest format.
    "typesafe_jev": VisionApiClass(
        name="typesafe_jev",
        long_edge=1568,
        quality=90,
        progressive=False,
        provider_hint=None,
        max_bytes=_SIXTEEN_MIB,
        min_edge=280,
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
    "claude-opus-4-8": "anthropic_opus_hires",
    "claude-opus-4-7": "anthropic_opus_hires",
    # Opus 4.5 is in the EARLIER (1.2 MP) tier — the high-resolution class sent pixels it throws away (AND-V IMG17 c).
    "claude-opus-4-5": "anthropic_sonnet_default",
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
    # Google Gemini: NOT by name — ``_gemini_class`` (generation + what the model makes).
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
    "typesafe_systemone": "typesafe_jev",
}


def _normalise_model_name(model: str | None) -> str | None:
    if not model:
        return None
    return model.strip().lower()


# ---------------------------------------------------------------------------
# Gemini (CGU-10 IMG8 #1). A prefix list went stale the day it was written: every name past
# gemini-3-pro / gemini-3-flash (3.1, 3.5–3.8, 4, ``*-latest``) fell to the 2.5 class, and a picture
# on gemini-3.5-flash was estimated 258 and billed 1,089. Measured with ``countTokens`` on every
# live picture-reading Gemini (2026-11-11):
#   * text-making Gemini 3 and later (and an un-numbered one: robotics-er-2, ``*-latest``) count by
#     media resolution (256 / 529 / 1,089 / 2,209; gemini-4-argon 280 / 560 / 1,120 / 2,240) and
#     take a per-picture ``mediaResolution``;
#   * Gemini 2.x, and a picture- or video-MAKING Gemini of any generation, count a flat 258 and
#     refuse a per-picture ``mediaResolution`` with a 400.
# So the class is decided by the generation (the leading major version, after a ``-latest`` alias
# resolves) and by what the catalog says the model makes — never by a list of names.
# ---------------------------------------------------------------------------
_GEMINI_NAME = re.compile(r"^(?:models/|google/)?(gemini-.+)$")
_GEMINI_MAJOR = re.compile(r"^gemini-(\d+)(?:\.\d+)?-")
_MEDIA_OUTPUTS = frozenset({"image", "video"})


def _catalog() -> Any:
    try:
        from matrx_ai.catalog.manager import ai_catalog_manager

        return ai_catalog_manager
    except Exception:  # noqa: BLE001 — a client host or a bare import has no catalog
        return None


def resolved_gemini_name(model: str | None) -> str | None:
    """The concrete Gemini a name runs as: ``models/``/``google/`` stripped, an ``ai.model_alias`` row
    followed through the catalog, then a probed ``*-latest`` pointer (``gemini_mode_truth``).
    ``None`` when ``model`` is not a Gemini name."""
    match = _GEMINI_NAME.match((model or "").strip().lower())
    if match is None:
        return None
    name = match.group(1)
    catalog = _catalog()
    if catalog is not None:
        try:
            target = catalog.canonical_model_name(name)
        except Exception:  # noqa: BLE001 — the catalog must never break a send
            target = None
        if isinstance(target, str) and target.lower().startswith("gemini-"):
            name = target.lower()
    from matrx_ai.catalog.gemini_mode_truth import resolved_gemini_id

    return resolved_gemini_id(name)


def gemini_major_version(model: str | None) -> int | None:
    """The generation a Gemini name runs as (``gemini-3.5-flash`` → 3, ``gemini-flash-latest`` → 3,
    ``gemini-2.5-pro`` → 2). ``None`` when not a Gemini name or the name carries no version."""
    name = resolved_gemini_name(model)
    match = _GEMINI_MAJOR.match(name or "")
    return int(match.group(1)) if match else None


#: CGU-10 IMG9 #5 — the maker words in a Gemini's OWN name, read only when no catalog answers (a client
#: host, a server before its catalog loads). Every live picture/video maker carries one: ``*-image``
#: (2.5-flash-image, 3-pro-image, 3.1-flash-image, 3.1-flash-lite-image), ``nano-banana``, ``omni``;
#: ``veo`` / ``imagen`` are Google's maker families. The catalog's ``capabilities.output`` always wins.
_GEMINI_MAKER_WORDS = re.compile(r"(?:^|-)(?:image|nano-banana|omni|veo|imagen)(?:-|$|\d)")


def _catalog_outputs(model: str | None) -> frozenset[str] | None:
    """What the catalog says this Gemini makes; ``None`` when no catalog answers for it."""
    catalog = _catalog()
    if catalog is None or not model:
        return None
    try:
        return catalog.model_outputs(model) or catalog.model_outputs(resolved_gemini_name(model))
    except Exception:  # noqa: BLE001 — the catalog must never break a send
        return None


def gemini_makes_media(model: str | None) -> bool:
    """True when this Gemini MAKES pictures or video: the catalog's ``capabilities.output`` when it
    answers, else the maker words in the model's own name (``-image``, ``nano-banana``, ``omni`` …) —
    never "no" just because no catalog was there to say yes."""
    outputs = _catalog_outputs(model)
    if outputs is not None:
        return bool(outputs & _MEDIA_OUTPUTS)
    name = resolved_gemini_name(model) or ""
    return bool(_GEMINI_MAKER_WORDS.search(name))


#: CGU-10 AND-IMG11 — read only when no catalog answers, like the maker words: a computer-use Gemini's
#: own name says so (``gemini-2.5-computer-use-preview-10-2025``). The catalog's ``capabilities.features``
#: always wins.
_GEMINI_COMPUTER_USE_WORDS = re.compile(r"(?:^|-)computer-use(?:-|$)")


def _catalog_features(model: str | None) -> frozenset[str] | None:
    """What the catalog says this Gemini can do; ``None`` when no catalog answers for it."""
    catalog = _catalog()
    if catalog is None or not model:
        return None
    try:
        reader = getattr(catalog, "model_features", None)
        if reader is None:
            return None
        return reader(model) or reader(resolved_gemini_name(model))
    except Exception:  # noqa: BLE001 — the catalog must never break a send
        return None


def gemini_tiles_pictures(model: str | None) -> bool:
    """True when this Gemini counts a picture by TILES (CGU-10 AND-IMG11): a 2.x Gemini that makes text
    and is built for computer use — the catalog's ``capabilities.features`` holds ``computer_use``
    (else, with no catalog row, the words in its own name). A Gemini 3+ with ``computer_use``
    (3.5-flash-lite, 3.8-flash, robotics-er-2) still counts by resolution — measured — so the
    generation decides first."""
    if gemini_makes_media(model) or gemini_reads_by_resolution(model):
        return False
    features = _catalog_features(model)
    if features is not None:
        return "computer_use" in features
    name = resolved_gemini_name(model) or ""
    return bool(_GEMINI_COMPUTER_USE_WORDS.search(name))


def gemini_reads_by_resolution(model: str | None) -> bool:
    """THE estimate's answer: does this Gemini count a picture by media resolution? (Gemini 3+ that
    makes text — and an un-numbered current Gemini.) False for 2.x and for a picture/video maker."""
    if gemini_makes_media(model):
        return False
    major = gemini_major_version(model)
    return major is None or major >= 3


def gemini_takes_part_media_resolution(model: str | None) -> bool:
    """THE wire's answer: may a per-picture ``mediaResolution`` ride to this Gemini? Only when it is
    KNOWN to count by resolution — the catalog answers that it makes no pictures or video and the
    generation reads by resolution. Unknown (no catalog) → no: Google 400s the whole call on a model
    that refuses it, while leaving it off only sends the picture at the model's own resolution."""
    if _catalog_outputs(model) is None:
        return False
    return gemini_reads_by_resolution(model)


def _gemini_class(model: str | None) -> VisionApiClass | None:
    if resolved_gemini_name(model) is None:
        return None
    if gemini_reads_by_resolution(model):
        return VISION_API_CLASSES["gemini3_high"]
    if gemini_makes_media(model):
        return VISION_API_CLASSES["gemini_media_maker"]
    if gemini_tiles_pictures(model):
        return VISION_API_CLASSES["gemini25_tiled"]
    return VISION_API_CLASSES["gemini25_default"]


def resolve_vision_class(
    model: str | None,
    wire_format: str | None = None,
) -> VisionApiClass:
    """Resolve the image re-encoding profile for a model on a wire route.

    Callers gate on ``ResolvedModelCapabilities.supports_vision`` BEFORE reaching
    here — this function assumes bytes are going to be sent and only decides how
    to encode them.

    Resolution order:
      0. A Gemini name: by generation and what it makes (``_gemini_class``), never by name list.
      1. Exact match on ``MODEL_TO_VISION_CLASS``.
      2. Prefix match on ``MODEL_TO_VISION_CLASS`` (the longest prefix wins
         so ``claude-opus-4-7-20251201`` still hits ``claude-opus-4-7``).
      3. Any other ``claude-*`` name: the Claude default class, whatever the wire.
      4. ``WIRE_FORMAT_DEFAULT_VISION_CLASS[wire_format]``.
      5. ``unknown_default``.
    """
    name = _normalise_model_name(model)

    gemini = _gemini_class(name)
    if gemini is not None:
        return gemini

    if name and name in MODEL_TO_VISION_CLASS:
        return VISION_API_CLASSES[MODEL_TO_VISION_CLASS[name]]

    if name:
        prefix_hits = [k for k in MODEL_TO_VISION_CLASS if name.startswith(k)]
        if prefix_hits:
            best = max(prefix_hits, key=len)
            return VISION_API_CLASSES[MODEL_TO_VISION_CLASS[best]]

    if name and name.startswith("claude-"):
        # Any other Claude is a Claude whatever wire names it (AND-V IMG17 c): on wire ``anthropic`` or none it
        # fell to ``unknown_default`` and skipped Claude's own picture rule (opus-4-6: 2,459 against ~1,600).
        return VISION_API_CLASSES["anthropic_sonnet_default"]

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
    "gemini_major_version",
    "gemini_makes_media",
    "gemini_reads_by_resolution",
    "gemini_takes_part_media_resolution",
    "gemini_tiles_pictures",
    "resolved_gemini_name",
]

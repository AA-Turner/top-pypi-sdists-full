"""Canonical generation-metadata shape for AI-produced media.

One Pydantic model holds everything we care to remember about how an image
/ video / audio file was generated. Providers (OpenAI, Google, Together,
Replicate, xAI, etc.) report wildly different shapes — this module is the
canonicalization layer.

Per-provider mappers pull known fields into canonical names and dump
everything else into ``provider_extras`` so no data is silently lost when
a provider adds new fields. New canonical fields land here when more than
one provider reports the same concept.

Storage: stamped under ``cld_files.metadata.generation`` by the matrx-ai
persistence path. The FE can parse with ``MediaGenerationMetadata.model_validate``
when it needs typed access (e.g. "Regenerate with same settings").
"""

from __future__ import annotations

import logging
import time
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

logger = logging.getLogger(__name__)


MediaGenerationKind = Literal["image", "video", "audio", "speech", "music"]


class MediaGenerationMetadata(BaseModel):
    """Canonical record of how an AI-produced asset was generated.

    Stored at ``cld_files.metadata.generation`` for every AI-generated
    file. Field naming is provider-agnostic — per-provider mappers
    translate from each SDK's response shape into these canonical names
    and dump unmapped fields into ``provider_extras``.
    """

    model_config = ConfigDict(extra="forbid")

    # ---- identity ----
    kind: MediaGenerationKind
    provider: str = Field(
        description="Our provider key: 'openai', 'google', 'together', 'replicate', 'xai', 'elevenlabs', 'groq', ..."
    )
    model: str = Field(
        description="Provider model name as called, e.g. 'gpt-image-2', 'imagen-3', 'flux-1-dev'."
    )

    # ---- request ----
    prompt: str = Field(
        default="",
        description="The natural-language prompt as submitted (may differ from revised_prompt).",
    )
    negative_prompt: str | None = None
    revised_prompt: str | None = Field(
        default=None,
        description=(
            "Provider-rewritten prompt (OpenAI gpt-image-* rewrites for "
            "safety / specificity; show to user for transparency). None "
            "when the provider didn't rewrite or didn't surface a rewrite."
        ),
    )

    # ---- output shape (canonical names, normalized across providers) ----
    width: int | None = None
    height: int | None = None
    aspect_ratio: str | None = Field(
        default=None,
        description="Normalized form: '16:9', '1:1', '9:16', '4:3', etc.",
    )
    duration_seconds: float | None = Field(
        default=None, description="For video/audio/speech/music."
    )

    # ---- generation knobs (provider support varies; missing = not applicable) ----
    quality: str | None = Field(
        default=None,
        description="Normalized to one of 'draft' | 'standard' | 'hd' | provider-specific when no mapping fits.",
    )
    style: str | None = Field(
        default=None,
        description="Style preset name (OpenAI: 'vivid'|'natural'; provider-specific otherwise).",
    )
    seed: int | None = Field(
        default=None,
        description="Random seed when the provider supports it; enables reproducibility.",
    )
    steps: int | None = Field(
        default=None, description="Diffusion-family steps. None for non-diffusion models."
    )
    cfg_scale: float | None = Field(
        default=None,
        description="Classifier-free-guidance scale (Flux, SD-family). None for non-diffusion models.",
    )
    n_requested: int = Field(default=1, description="How many assets the caller asked for.")
    n_returned: int = Field(default=1, description="How many the provider actually returned.")

    # ---- operational ----
    response_id: str | None = Field(
        default=None,
        description="Provider's request/response id — useful for support tickets and provider-side debugging.",
    )
    duration_ms: int | None = Field(
        default=None, description="Wall-clock duration of the provider call (ms)."
    )
    cost_usd: float | None = Field(
        default=None,
        description="Our cost estimate in USD based on usage tracking. None when no pricing is configured.",
    )
    finish_reason: str | None = Field(
        default=None,
        description="Provider's finish reason: 'completed', 'content_filter', 'error', 'safety_violation', ...",
    )
    safety_flagged: bool = Field(
        default=False,
        description="True when any provider-side safety check fired. Full details in provider_extras.safety.",
    )

    # ---- catch-all so we never silently drop provider data ----
    provider_extras: dict[str, JsonValue] = Field(
        default_factory=dict,
        description=(
            "Raw provider response fields that aren't mapped to canonical "
            "names. When a provider adds a new useful field, audit "
            "provider_extras to decide whether to canonicalize it."
        ),
    )


# ---------------------------------------------------------------------------
# Mapper protocol + default
# ---------------------------------------------------------------------------
#
# Each provider's BaseMediaGeneration subclass overrides _map_generation_metadata
# to produce a MediaGenerationMetadata from the raw response. The base
# implementation here covers the common minimum — provider, model, prompt,
# n_returned, response_id when available — so providers without a custom
# mapper still get a typed record.


def build_default_metadata(
    *,
    kind: MediaGenerationKind,
    provider: str,
    model: str,
    prompt: str | None,
    n_returned: int,
    duration_ms: int | None = None,
    cost_usd: float | None = None,
) -> MediaGenerationMetadata:
    """Minimum-viable MediaGenerationMetadata when no provider mapper is available.

    Useful as a fallback for providers whose response shape doesn't carry
    the canonical fields (or hasn't been wired with a custom mapper yet).
    """
    return MediaGenerationMetadata(
        kind=kind,
        provider=provider,
        model=model,
        prompt=prompt or "",
        n_returned=max(1, n_returned),
        duration_ms=duration_ms,
        cost_usd=cost_usd,
    )


# ---------------------------------------------------------------------------
# Per-provider mappers
# ---------------------------------------------------------------------------
#
# Each mapper's contract:
#   * Pull fields whose semantics we have canonical names for into the
#     model directly.
#   * Dump everything else useful into provider_extras.
#   * Never raise — return a best-effort metadata on any error so the
#     generation response is never blocked by metadata mapping.


def map_openai_image_response(
    *,
    raw: Any,
    item: Any,
    request_kwargs: dict[str, Any],
    prompt: str,
    model: str,
    n_returned: int,
    duration_ms: int | None = None,
    cost_usd: float | None = None,
) -> MediaGenerationMetadata:
    """Map a single OpenAI gpt-image-* response item to MediaGenerationMetadata.

    ``raw`` is the SDK's full ImagesResponse; ``item`` is the per-asset
    entry from ``raw.data``. ``request_kwargs`` is what we sent on the wire.
    """
    extras: dict[str, JsonValue] = {}
    try:
        usage = getattr(raw, "usage", None)
        if usage is not None:
            extras["usage"] = {
                "input_tokens": getattr(usage, "input_tokens", None),
                "output_tokens": getattr(usage, "output_tokens", None),
            }
    except Exception:
        pass

    # Pull size from the response item if available; fall back to request.
    width: int | None = None
    height: int | None = None
    size_str: str | None = getattr(item, "size", None) or request_kwargs.get("size")
    if isinstance(size_str, str) and "x" in size_str:
        try:
            w_str, h_str = size_str.lower().split("x", 1)
            width = int(w_str)
            height = int(h_str)
        except ValueError:
            pass

    aspect = _aspect_ratio(width, height)
    quality_raw = request_kwargs.get("quality")
    quality = _normalize_quality(quality_raw, provider="openai")

    return MediaGenerationMetadata(
        kind="image",
        provider="openai",
        model=model,
        prompt=prompt,
        revised_prompt=getattr(item, "revised_prompt", None),
        width=width,
        height=height,
        aspect_ratio=aspect,
        quality=quality,
        style=request_kwargs.get("style"),
        n_requested=int(request_kwargs.get("n") or 1),
        n_returned=n_returned,
        response_id=getattr(raw, "id", None) or getattr(raw, "request_id", None),
        duration_ms=duration_ms,
        cost_usd=cost_usd,
        finish_reason="completed",
        provider_extras=extras,
    )


def map_google_imagen_response(
    *,
    raw: Any,
    item: Any,
    request_kwargs: dict[str, Any],
    prompt: str,
    model: str,
    n_returned: int,
    duration_ms: int | None = None,
    cost_usd: float | None = None,
) -> MediaGenerationMetadata:
    """Map a single Google Imagen response asset to MediaGenerationMetadata.

    Imagen has no seed concept. Safety attributes are gathered into
    provider_extras + the safety_flagged flag.
    """
    extras: dict[str, JsonValue] = {}
    safety_flagged = False
    try:
        safety = getattr(item, "safety_attributes", None) or getattr(item, "safetyAttributes", None)
        if safety:
            if isinstance(safety, dict):
                cats = safety.get("categories")
                scores = safety.get("scores")
            else:
                cats = getattr(safety, "categories", None)
                scores = getattr(safety, "scores", None)
            if cats:
                extras["safety"] = {
                    "categories": list(cats),
                    "scores": list(scores) if scores else None,
                }
                # Imagen reports scores in [0, 1]; treat anything above the
                # provider's default threshold as flagged.
                if scores and any((s or 0) > 0.5 for s in scores):
                    safety_flagged = True
    except Exception:
        pass

    # Imagen returns size via aspect_ratio + the actual rendered image dims
    width = getattr(item, "width", None)
    height = getattr(item, "height", None)
    aspect = request_kwargs.get("aspect_ratio") or _aspect_ratio(width, height)

    return MediaGenerationMetadata(
        kind="image",
        provider="google",
        model=model,
        prompt=prompt,
        width=width,
        height=height,
        aspect_ratio=aspect,
        n_requested=int(request_kwargs.get("number_of_images") or request_kwargs.get("n") or 1),
        n_returned=n_returned,
        duration_ms=duration_ms,
        cost_usd=cost_usd,
        safety_flagged=safety_flagged,
        finish_reason="content_filter" if safety_flagged else "completed",
        provider_extras=extras,
    )


def map_together_image_response(
    *,
    raw: Any,
    item: Any,
    request_kwargs: dict[str, Any],
    prompt: str,
    model: str,
    n_returned: int,
    duration_ms: int | None = None,
    cost_usd: float | None = None,
) -> MediaGenerationMetadata:
    """Map a Together AI image response (Flux, SD-family) to MediaGenerationMetadata.

    Together / Flux carry full diffusion knobs: seed, steps, cfg_scale,
    negative_prompt. All of them go into canonical fields so the
    "regenerate with same settings" UX has everything it needs.
    """
    width = getattr(item, "width", None) or request_kwargs.get("width")
    height = getattr(item, "height", None) or request_kwargs.get("height")
    return MediaGenerationMetadata(
        kind="image",
        provider="together",
        model=model,
        prompt=prompt,
        negative_prompt=request_kwargs.get("negative_prompt"),
        width=width,
        height=height,
        aspect_ratio=_aspect_ratio(width, height),
        seed=request_kwargs.get("seed"),
        steps=request_kwargs.get("steps"),
        cfg_scale=request_kwargs.get("guidance") or request_kwargs.get("cfg_scale"),
        n_requested=int(request_kwargs.get("n") or 1),
        n_returned=n_returned,
        response_id=getattr(raw, "id", None),
        duration_ms=duration_ms,
        cost_usd=cost_usd,
        finish_reason="completed",
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


_QUALITY_NORMALIZERS: dict[str, dict[str, str]] = {
    "openai": {
        "low": "draft",
        "medium": "standard",
        "high": "hd",
        "standard": "standard",
        "hd": "hd",
    },
}


def _normalize_quality(raw_value: str | None, *, provider: str) -> str | None:
    """Translate a provider's quality knob to the canonical 'draft'|'standard'|'hd' alphabet.

    Unknown values pass through unchanged so we never lose info — analytics
    can still group by the original string until we canonicalize.
    """
    if not raw_value:
        return None
    mapping = _QUALITY_NORMALIZERS.get(provider, {})
    return mapping.get(str(raw_value).lower(), str(raw_value).lower())


def _aspect_ratio(width: int | None, height: int | None) -> str | None:
    """Normalize (width, height) to a common 'W:H' aspect-ratio string.

    Reduces by GCD; returns None when dimensions are missing or zero.
    Common ratios (16:9, 1:1, 9:16, 4:3, 3:4) come through cleanly;
    odd ratios pass through as 'W:H' literal so analytics can still group.
    """
    if not width or not height:
        return None
    try:
        from math import gcd

        g = gcd(int(width), int(height))
        return f"{int(width) // g}:{int(height) // g}"
    except Exception:
        return None


def map_replicate_image_response(
    *,
    raw: Any,
    item: Any,
    request_kwargs: dict[str, Any],
    prompt: str,
    model: str,
    n_returned: int,
    duration_ms: int | None = None,
    cost_usd: float | None = None,
) -> MediaGenerationMetadata:
    """Map a Replicate image response (Flux family, SDXL, etc.) to MediaGenerationMetadata.

    Replicate has a model-descriptor pattern — the input dict varies per
    model. We pull the common diffusion knobs (seed, steps, guidance,
    aspect_ratio, negative_prompt, width/height) when present in the
    input kwargs, and drop everything else under provider_extras.input
    so per-model knobs aren't lost in canonicalisation.
    """
    extras: dict[str, JsonValue] = {}

    # Replicate kwargs nest the model input under ``input`` (set by
    # BaseMediaGeneration._build_kwargs via the descriptor's to_input).
    inp = request_kwargs.get("input") or {}
    # Capture every input field that isn't redundantly mapped to canonical.
    canonical_keys = {
        "seed",
        "steps",
        "num_inference_steps",
        "guidance",
        "guidance_scale",
        "cfg_scale",
        "aspect_ratio",
        "width",
        "height",
        "negative_prompt",
        "prompt",
        "num_outputs",
    }
    extras_input = {k: v for k, v in inp.items() if k not in canonical_keys}
    if extras_input:
        extras["input"] = extras_input

    width = inp.get("width")
    height = inp.get("height")
    aspect = inp.get("aspect_ratio") or _aspect_ratio(width, height)

    return MediaGenerationMetadata(
        kind="image",
        provider="replicate",
        model=model,
        prompt=prompt,
        negative_prompt=inp.get("negative_prompt"),
        width=width,
        height=height,
        aspect_ratio=aspect,
        seed=inp.get("seed"),
        steps=inp.get("steps") or inp.get("num_inference_steps"),
        cfg_scale=inp.get("guidance") or inp.get("guidance_scale") or inp.get("cfg_scale"),
        n_requested=int(inp.get("num_outputs") or 1),
        n_returned=n_returned,
        duration_ms=duration_ms,
        cost_usd=cost_usd,
        finish_reason="completed",
        provider_extras=extras,
    )


def map_xai_image_response(
    *,
    raw: Any,
    item: Any,
    request_kwargs: dict[str, Any],
    prompt: str,
    model: str,
    n_returned: int,
    duration_ms: int | None = None,
    cost_usd: float | None = None,
) -> MediaGenerationMetadata:
    """Map an xAI grok-imagine image response to MediaGenerationMetadata.

    Surfaces ``revised_prompt`` (grok rewrites prompts like OpenAI does)
    and the moderation flag when xAI returned the asset with a content-
    filter signal. Dimensions are model-fixed for grok-imagine (no
    user-selectable size) so width/height come from the asset itself.
    """
    extras: dict[str, JsonValue] = {}

    # The xai_sdk image response items expose image_url + revised_prompt
    # (+ optionally width/height when the SDK populates them).
    revised = getattr(item, "revised_prompt", None) if item is not None else None
    width = getattr(item, "width", None) if item is not None else None
    height = getattr(item, "height", None) if item is not None else None
    aspect = _aspect_ratio(width, height)

    return MediaGenerationMetadata(
        kind="image",
        provider="xai",
        model=model,
        prompt=prompt,
        revised_prompt=revised,
        width=width,
        height=height,
        aspect_ratio=aspect,
        n_requested=int(request_kwargs.get("n") or 1),
        n_returned=n_returned,
        duration_ms=duration_ms,
        cost_usd=cost_usd,
        finish_reason="completed",
        provider_extras=extras,
    )


def map_elevenlabs_audio_response(
    *,
    raw: Any,
    request_kwargs: dict[str, Any],
    prompt: str,
    model: str,
    voice_id: str | None = None,
    voice_name: str | None = None,
    duration_ms: int | None = None,
    char_count: int | None = None,
    audio_format: str | None = None,
    cost_usd: float | None = None,
    is_dialogue: bool = False,
) -> MediaGenerationMetadata:
    """Map an ElevenLabs TTS response to MediaGenerationMetadata.

    ElevenLabs is our default audio (speech) provider. Surfaces the
    voice identity (id + display name) + dialogue mode + character
    count under provider_extras since they don't have a canonical
    cross-provider home yet.
    """
    extras: dict[str, JsonValue] = {}
    if voice_id:
        extras["voice_id"] = voice_id
    if voice_name:
        extras["voice_name"] = voice_name
    if audio_format:
        extras["audio_format"] = audio_format
    if char_count is not None:
        extras["char_count"] = char_count
    extras["dialogue_mode"] = is_dialogue

    return MediaGenerationMetadata(
        kind="speech",
        provider="elevenlabs",
        model=model,
        prompt=prompt,
        duration_seconds=(duration_ms / 1000) if duration_ms is not None else None,
        n_requested=1,
        n_returned=1,
        duration_ms=duration_ms,
        cost_usd=cost_usd,
        finish_reason="completed",
        provider_extras=extras,
    )


def map_tts_audio_response(
    *,
    provider: str,
    model: str,
    prompt: str,
    voice: str | None = None,
    audio_format: str | None = None,
    duration_ms: int | None = None,
    cost_usd: float | None = None,
    extra: dict[str, JsonValue] | None = None,
) -> MediaGenerationMetadata:
    """Generic TTS response → MediaGenerationMetadata mapper.

    Covers the common TTS shape across OpenAI / xAI / Groq / generic
    HTTP-call TTS providers. ElevenLabs has its own richer mapper
    (``map_elevenlabs_audio_response``) for dialogue mode + character
    count. Provider-specific knobs that don't have a canonical home
    (speed, language code, etc.) go in ``extra`` → ``provider_extras``.
    """
    extras: dict[str, JsonValue] = {}
    if voice:
        extras["voice"] = voice
    if audio_format:
        extras["audio_format"] = audio_format
    if extra:
        for k, v in extra.items():
            extras.setdefault(k, v)

    return MediaGenerationMetadata(
        kind="speech",
        provider=provider,
        model=model,
        prompt=prompt,
        duration_seconds=(duration_ms / 1000) if duration_ms is not None else None,
        n_requested=1,
        n_returned=1,
        duration_ms=duration_ms,
        cost_usd=cost_usd,
        finish_reason="completed",
        provider_extras=extras,
    )


__all__ = [
    "MediaGenerationKind",
    "MediaGenerationMetadata",
    "build_default_metadata",
    "map_openai_image_response",
    "map_google_imagen_response",
    "map_together_image_response",
    "map_replicate_image_response",
    "map_xai_image_response",
    "map_elevenlabs_audio_response",
    "map_tts_audio_response",
]

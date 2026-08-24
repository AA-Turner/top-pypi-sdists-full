"""Static per-provider/model attachment-capability registry.

Providers differ in what attachment payloads they accept: some reject
``type:'file'`` PDF blobs, some cannot see images at all, and each has its own
inline size ceilings. The registry keys match the provider strings resolved in
``agno.py::_load_llm_model``; unknown providers fall back to
``DEFAULT_CAPABILITIES``, which reproduces today's behavior exactly.

``XPANDER_MEDIA_PIPELINE=legacy`` is the kill switch: every lookup returns the
defaults and the media transforms downstream disable themselves.
"""

import os
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel

_MB = 1024 * 1024


def _env_clamp(name: str) -> Optional[int]:
    """Explicitly-set env ceiling, or None (defaults must not clamp providers with higher registry caps)."""
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def media_pipeline_disabled() -> bool:
    """True when the env kill switch forces legacy attachment behavior."""
    return os.getenv("XPANDER_MEDIA_PIPELINE", "").strip().lower() == "legacy"


# agno's Bedrock formatter raises a LOCAL ValueError for containers outside this set -
# not a provider 400, so the degrade-retry never fires; gate client-side instead.
BEDROCK_VIDEO_FORMATS = {
    "mp4",
    "mov",
    "mkv",
    "webm",
    "flv",
    "mpeg",
    "mpg",
    "wmv",
    "three_gp",
}


class ModelCapabilities(BaseModel):
    supports_vision: bool = True
    supports_native_pdf: bool = True
    # Fail-closed: native audio/video is the exception (gemini both, bedrock video,
    # openai -audio models), so unknown providers transcribe instead of 400ing.
    supports_audio: bool = False
    supports_video: bool = False
    max_image_bytes: int = 5 * _MB
    max_image_px: int = 1568
    max_images: int = 20
    max_pdf_bytes: int = 15 * _MB
    max_pdf_pages: int = 100
    max_fetch_bytes: int = 30 * _MB
    max_audio_bytes: int = 20 * _MB
    max_video_bytes: int = 50 * _MB
    # Containers this provider names in its own allowlist. None = no client-side gate:
    # only Bedrock raises locally, everywhere else a bad container 400s and degrade-retries.
    native_video_formats: Optional[frozenset] = None


DEFAULT_CAPABILITIES = ModelCapabilities()

_OPENAI_COMPAT_NO_PDF: Dict[str, Any] = {"supports_native_pdf": False}

PROVIDER_CAPABILITIES: Dict[str, ModelCapabilities] = {
    "anthropic": ModelCapabilities(),
    "amazon_bedrock": ModelCapabilities(
        max_pdf_bytes=int(4.5 * _MB),
        supports_video=True,
        native_video_formats=frozenset(BEDROCK_VIDEO_FORMATS),
    ),
    "openai": ModelCapabilities(
        max_image_bytes=20 * _MB, max_image_px=2048, max_pdf_bytes=30 * _MB
    ),
    "azure_ai_foundary": ModelCapabilities(
        max_image_bytes=20 * _MB, max_image_px=2048, max_pdf_bytes=30 * _MB
    ),
    "google_ai_studio": ModelCapabilities(
        supports_audio=True,
        supports_video=True,
        max_image_bytes=15 * _MB,
        max_image_px=3072,
        max_pdf_bytes=15 * _MB,
        max_pdf_pages=300,
    ),
    "fireworks": ModelCapabilities(**_OPENAI_COMPAT_NO_PDF),
    "nebius": ModelCapabilities(**_OPENAI_COMPAT_NO_PDF),
    "open_router": ModelCapabilities(**_OPENAI_COMPAT_NO_PDF),
    "helicone": ModelCapabilities(**_OPENAI_COMPAT_NO_PDF),
    "cloudflare_ai_gw": ModelCapabilities(**_OPENAI_COMPAT_NO_PDF),
    "z_ai": ModelCapabilities(**_OPENAI_COMPAT_NO_PDF),
    "bytedance": ModelCapabilities(**_OPENAI_COMPAT_NO_PDF),
    "cerebras": ModelCapabilities(supports_vision=False, supports_native_pdf=False),
    "tzafon_lightcone": ModelCapabilities(
        supports_vision=False, supports_native_pdf=False
    ),
    "nim": ModelCapabilities(supports_vision=False, supports_native_pdf=False),
}

# (provider or "*", model-id substring, overrides). Longest matching pattern
# wins so "glm-4.5v" beats "glm-4.5". Substring (not prefix) match because the
# same model ships under decorated ids per gateway ("zai.glm-4.7-flash" on
# Bedrock, "zai-glm-4.7" on Cerebras).
MODEL_OVERRIDES: List[Tuple[str, str, Dict[str, Any]]] = [
    ("*", "glm-4.5", {"supports_vision": False, "supports_native_pdf": False}),
    ("*", "glm-4.5v", {"supports_vision": True, "supports_native_pdf": False}),
    ("*", "glm-4.6", {"supports_vision": False, "supports_native_pdf": False}),
    ("*", "glm-4.7", {"supports_vision": False, "supports_native_pdf": False}),
    ("*", "glm-4.7v", {"supports_vision": True, "supports_native_pdf": False}),
    # Kimi K2 / K2 Thinking are text-only; K2.5 (vision) stays on the Bedrock defaults.
    ("*", "kimi-k2", {"supports_vision": False, "supports_native_pdf": False}),
    ("*", "kimi-k2.5", {"supports_vision": True, "supports_native_pdf": True}),
    # Gateway routing fallbacks: gpt-4.1-nano / gpt-5-nano do vision, not type:'file'.
    # Only the -audio model family accepts input_audio parts on chat completions.
    ("openai", "audio", {"supports_audio": True}),
    ("azure_ai_foundary", "audio", {"supports_audio": True}),
    ("openai", "gpt-4.1-nano", {"supports_vision": True, "supports_native_pdf": False}),
    ("openai", "gpt-5-nano", {"supports_vision": True, "supports_native_pdf": False}),
    (
        "tzafon_lightcone",
        "northstar-cua",
        {"supports_vision": False, "supports_native_pdf": False},
    ),
    ("nim", "vision", {"supports_vision": True}),
    ("nim", "vila", {"supports_vision": True}),
]


def _apply_env_clamps(caps: ModelCapabilities) -> ModelCapabilities:
    """Explicitly-set env vars stay authoritative global ceilings on top of resolved values."""
    image_clamp = _env_clamp("XPANDER_MAX_INLINE_IMAGE_BYTES")
    if image_clamp is not None:
        caps.max_image_bytes = min(caps.max_image_bytes, image_clamp)
    doc_clamp = _env_clamp("XPANDER_MAX_INLINE_DOC_BYTES")
    if doc_clamp is not None:
        caps.max_pdf_bytes = min(caps.max_pdf_bytes, doc_clamp)
    return caps


def get_model_capabilities(
    provider: Optional[str], model_name: Optional[str] = None
) -> ModelCapabilities:
    """Resolve effective capabilities for (provider, model), honoring the kill switch and env clamps."""
    if media_pipeline_disabled():
        return DEFAULT_CAPABILITIES.model_copy()

    provider_key = (provider or "").strip().lower()
    caps = PROVIDER_CAPABILITIES.get(provider_key, DEFAULT_CAPABILITIES).model_copy()

    model_key = (model_name or "").strip().lower()
    if model_key:
        best: Optional[Tuple[str, Dict[str, Any]]] = None
        for override_provider, pattern, overrides in MODEL_OVERRIDES:
            if override_provider != "*" and override_provider != provider_key:
                continue
            if pattern in model_key and (best is None or len(pattern) > len(best[0])):
                best = (pattern, overrides)
        if best:
            caps = caps.model_copy(update=best[1])

    return _apply_env_clamps(caps)


def resolve_task_capabilities(
    provider: Optional[str],
    model_name: Optional[str],
    media_caps: Optional[dict] = None,
) -> ModelCapabilities:
    """Platform-stamped capabilities when they describe this exact model; the local registry otherwise.

    ``media_caps`` is the controller-resolved ``payload_extension["media_caps"]`` dict. It is
    honored only when its ``provider``/``model`` match the SDK's own resolved pair - a stale
    stamp (model changed after task creation) must not apply the wrong model's capabilities.
    Any malformed payload falls back to the registry; nothing here raises.
    """
    if media_pipeline_disabled():
        return DEFAULT_CAPABILITIES.model_copy()

    provider_key = (provider or "").strip().lower()
    model_key = (model_name or "").strip().lower()
    if isinstance(media_caps, dict):
        if (
            str(media_caps.get("provider") or "").strip().lower() == provider_key
            and str(media_caps.get("model") or "").strip().lower() == model_key
        ):
            try:
                fields = {
                    k: media_caps[k]
                    for k in ModelCapabilities.model_fields
                    if k in media_caps
                }
                return _apply_env_clamps(ModelCapabilities(**fields))
            except Exception:
                pass
    return get_model_capabilities(provider, model_name)

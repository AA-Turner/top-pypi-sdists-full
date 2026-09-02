"""Per-model descriptors for the Replicate provider.

Replicate hosts dozens of frontier models with **incompatibly-shaped**
``input`` schemas. Since the B2-media flip the split is:

  * SCALAR params (aspect gates/fallbacks, num_outputs, output_format
    vocabularies, moderation defaults, FLUX safety_tolerance, duration
    renames, size derivation, ...) live in the CATALOG — each offering's
    ``ai.offering.override`` (db/migrations/_ai_029_seed_media_family_rules.py).
  * STRUCTURAL wiring stays here as pure data: the prompt key, and which
    input keys carry the start / end / reference image URLs (these differ
    per model: ``image`` vs ``start_image`` vs ``prompt_image`` vs
    ``first_frame_image`` vs one combined ``input_images`` list).

Each descriptor:

  - ``slug``: the ``owner/name`` (or pinned hash) used in
    ``replicate.run(slug, input=...)``
  - ``modality``: "image" | "video"
  - prompt/media key spec (below) consumed by :meth:`ModelDescriptor.build_input`
  - ``from_output(raw, descriptor) -> list[GeneratedAsset]`` — defaults
    to the universal "URL or list of URLs" shape; rare models override

Add a model: append a descriptor entry AND seed its offering override in a
follow-up _ai_ migration (the _ai_029 seed FAILS loudly on an offering with no
transcribed override, so a missing seed can't slip through silently).
Drop a model: remove both.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from matrx_ai.config import UnifiedConfig
from matrx_ai.providers.base_media import BaseMediaGeneration, GeneratedAsset

# ---------------------------------------------------------------------------
# Universal structural helpers (message-role + MediaRef -> URL resolution)
# ---------------------------------------------------------------------------


def _prompt(config: UnifiedConfig) -> str:
    """Main user prompt — skips role-tagged TextContent (negative_prompt etc.)."""
    from matrx_ai.config.message_config import pick_text_by_role

    return pick_text_by_role(config.messages, None) or ""


def _tagged_negative_prompt(config: UnifiedConfig) -> str | None:
    """User-message-tagged negative prompt (the settings-field fallback rides
    the canonical dict already)."""
    from matrx_ai.config.message_config import pick_text_by_role

    return pick_text_by_role(config.messages, "negative_prompt") or None


def _mediaref_url(ref: Any) -> str | None:
    if ref is None:
        return None
    url = (
        getattr(ref, "resolved_url", None)
        or getattr(ref, "url", None)
        or (ref.get("resolved_url") or ref.get("url") if isinstance(ref, dict) else None)
    )
    if url:
        return url
    b64 = getattr(ref, "base64_data", None) or (
        ref.get("base64_data") if isinstance(ref, dict) else None
    )
    mime = (
        getattr(ref, "mime_type", None)
        or (ref.get("mime_type") if isinstance(ref, dict) else None)
        or "image/png"
    )
    if b64:
        return f"data:{mime};base64,{b64}"
    return None


def _ref_urls(refs: list[Any] | None) -> list[str]:
    if not refs:
        return []
    out = []
    for r in refs:
        u = _mediaref_url(r)
        if u:
            out.append(u)
    return out


def _start_image_url(config: UnifiedConfig) -> str | None:
    """Resolve the start/primary image URL.

    Order: user-message-tagged ``start_image`` role > first un-tagged user
    image > settings ``image_input``.
    """
    from matrx_ai.config.message_config import pick_image_by_role

    img = pick_image_by_role(config.messages, "start_image") or pick_image_by_role(
        config.messages, None
    )
    if img is not None:
        return _mediaref_url(img)
    return _mediaref_url(config.image_input)


def _end_image_url(config: UnifiedConfig) -> str | None:
    """Resolve the end/last-frame image URL.

    Order: user-message-tagged ``end_image`` or ``last_frame_image`` role >
    settings ``last_frame_image``.
    """
    from matrx_ai.config.message_config import pick_image_by_role

    img = pick_image_by_role(config.messages, "end_image") or pick_image_by_role(
        config.messages, "last_frame_image"
    )
    if img is not None:
        return _mediaref_url(img)
    return _mediaref_url(config.last_frame_image)


def _reference_urls(config: UnifiedConfig) -> list[str]:
    """All reference image URLs.

    Order: user-message-tagged ``reference`` roles > settings
    ``image_inputs`` > settings ``reference_images``.
    """
    from matrx_ai.config.message_config import iter_images_by_role

    out: list[str] = []
    for r in iter_images_by_role(config.messages, "reference"):
        u = _mediaref_url(r)
        if u:
            out.append(u)
    if not out:
        out.extend(_ref_urls(config.image_inputs))
        out.extend(_ref_urls(config.reference_images))
    return out


def _default_from_output(raw: Any, desc: "ModelDescriptor") -> list[GeneratedAsset]:
    """Universal handler — Replicate models return a string URL, list of
    URLs, or ``FileOutput`` objects with ``.url`` and ``.read()``."""
    items = raw if isinstance(raw, (list, tuple)) else [raw]
    assets: list[GeneratedAsset] = []
    mime = desc.default_mime or ("image/png" if desc.modality == "image" else "video/mp4")
    for item in items:
        if hasattr(item, "url"):
            url = item.url() if callable(item.url) else item.url
            assets.append(GeneratedAsset(url=url, mime_type=mime))
        elif isinstance(item, str):
            assets.append(GeneratedAsset(url=item, mime_type=mime))
        elif hasattr(item, "read"):
            try:
                data = item.read()
                if isinstance(data, bytes):
                    assets.append(GeneratedAsset(data=data, mime_type=mime))
            except Exception:
                continue
        elif isinstance(item, dict):
            url = item.get("url") or item.get("output_url")
            if url:
                assets.append(GeneratedAsset(url=url, mime_type=mime))
    return assets


# ---------------------------------------------------------------------------
# Descriptor primitive — structural spec only; params come from the catalog.
# ---------------------------------------------------------------------------


@dataclass
class ModelDescriptor:
    slug: str
    modality: str  # "image" | "video"
    # Structural input-key spec — WHERE this model's schema puts each thing.
    prompt_key: str = "prompt"
    start_key: str | None = None  # single start/primary image
    end_key: str | None = None  # end/last-frame image
    refs_key: str | None = None  # reference-image list
    refs_max: int | None = None
    # gpt-image / nano-banana take start + references in ONE list (refs_key).
    start_in_refs: bool = False
    # Optional overrides — defaults below cover URL-only output.
    from_output: Callable[[Any, "ModelDescriptor"], list[GeneratedAsset]] | None = None
    notes: str = ""
    default_mime: str = ""

    def build_input(self, config: UnifiedConfig, controls: Any) -> dict[str, Any]:
        """Model input dict = structural media wiring + catalog params."""
        start = _start_image_url(config) if (self.start_key or self.start_in_refs) else None
        end = _end_image_url(config) if self.end_key else None
        refs = _reference_urls(config) if self.refs_key else []

        params = BaseMediaGeneration._outbound_params(
            controls,
            config,
            context={"has_image_input": bool(start or refs)},
            extra_canonical={"negative_prompt": _tagged_negative_prompt(config)},
        )

        out: dict[str, Any] = {self.prompt_key: _prompt(config)}
        out.update(params)

        if self.start_in_refs:
            images: list[str] = ([start] if start else []) + refs
            if images and self.refs_key:
                out[self.refs_key] = images[: self.refs_max] if self.refs_max else images
        else:
            if start and self.start_key:
                out[self.start_key] = start
            if refs and self.refs_key:
                out[self.refs_key] = refs[: self.refs_max] if self.refs_max else refs
        if end and self.end_key:
            out[self.end_key] = end
        return out


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


_IMAGE_MODELS: list[ModelDescriptor] = [
    # FLUX 2: start image under ``image_input``, refs under
    # ``reference_images`` (max 8). safety_tolerance is a catalog processor
    # (has_image_input context caps it at 2).
    ModelDescriptor(
        "black-forest-labs/flux-2-pro", "image",
        start_key="image_input", refs_key="reference_images", refs_max=8,
    ),
    ModelDescriptor(
        "black-forest-labs/flux-2-max", "image",
        start_key="image_input", refs_key="reference_images", refs_max=8,
    ),
    ModelDescriptor(
        "black-forest-labs/flux-2-flex", "image",
        start_key="image_input", refs_key="reference_images", refs_max=8,
    ),
    # gpt-image: start + references ride ONE ``input_images`` list (max 16).
    ModelDescriptor(
        "openai/gpt-image-2", "image",
        refs_key="input_images", refs_max=16, start_in_refs=True,
    ),
    ModelDescriptor(
        "openai/gpt-image-1.5", "image",
        refs_key="input_images", refs_max=16, start_in_refs=True,
    ),
    # Imagen 4 is text-only on Replicate.
    ModelDescriptor("google/imagen-4", "image"),
    ModelDescriptor("google/imagen-4-fast", "image"),
    ModelDescriptor("google/imagen-4-ultra", "image"),
    # nano-banana: start + references ride ONE ``image_input`` list (max 14).
    ModelDescriptor(
        "google/nano-banana-2", "image",
        refs_key="image_input", refs_max=14, start_in_refs=True,
    ),
    ModelDescriptor(
        "google/nano-banana-pro", "image",
        refs_key="image_input", refs_max=14, start_in_refs=True,
    ),
    ModelDescriptor("ideogram-ai/ideogram-v3-turbo", "image"),
    ModelDescriptor("ideogram-ai/ideogram-v3", "image"),
    ModelDescriptor("ideogram-ai/ideogram-v3-balanced", "image"),
    ModelDescriptor("ideogram-ai/ideogram-v3-quality", "image"),
    ModelDescriptor("recraft-ai/recraft-v4", "image"),
    ModelDescriptor("recraft-ai/recraft-v4-svg", "image", default_mime="image/svg+xml"),
    ModelDescriptor(
        "bytedance/seedream-4.5", "image",
        start_key="image", refs_key="reference_images",
    ),
]


_VIDEO_MODELS: list[ModelDescriptor] = [
    ModelDescriptor(
        "google/veo-3.1", "video", start_key="image", end_key="last_frame_image"
    ),
    ModelDescriptor(
        "google/veo-3.1-fast", "video", start_key="image", end_key="last_frame_image"
    ),
    ModelDescriptor(
        "runwayml/gen-4.5", "video", prompt_key="prompt_text", start_key="prompt_image"
    ),
    ModelDescriptor(
        "bytedance/seedance-2.0", "video",
        start_key="image", refs_key="reference_images", refs_max=9,
    ),
    ModelDescriptor(
        "kwaivgi/kling-v3-video", "video", start_key="start_image", end_key="end_image"
    ),
    ModelDescriptor("wan-video/wan-2.7-t2v", "video", start_key="image"),
    ModelDescriptor("wan-video/wan-2.7-i2v", "video", start_key="image"),
    ModelDescriptor(
        "luma/ray-3", "video", start_key="start_image_url", end_key="end_image_url"
    ),
    ModelDescriptor(
        "minimax/hailuo-2.3", "video",
        start_key="first_frame_image", end_key="last_frame_image",
    ),
]


# Keyed by canonical slug. Public.
MODEL_DESCRIPTORS: dict[str, ModelDescriptor] = {d.slug: d for d in (_IMAGE_MODELS + _VIDEO_MODELS)}


def get_descriptor(slug: str) -> ModelDescriptor | None:
    """Look up a descriptor by exact slug, then by ``owner/name`` prefix
    (so ``owner/name:hash`` pinned versions still resolve)."""
    if slug in MODEL_DESCRIPTORS:
        return MODEL_DESCRIPTORS[slug]
    base = slug.split(":", 1)[0]
    return MODEL_DESCRIPTORS.get(base)

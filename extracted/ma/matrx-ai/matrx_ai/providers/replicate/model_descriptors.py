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
from dataclasses import dataclass, field
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
    # Image-generation reference roles -> the input key that carries each.
    # A key in ``list_keys`` takes a list; several roles may share one list
    # (the prompt then carries an "Image N is the ..." legend). A role not
    # named here is refused by name before the paid call.
    role_keys: dict[str, str] = field(default_factory=dict)
    list_keys: frozenset[str] = frozenset()
    # Video models: the input key carrying each video-side role (first_frame,
    # last_frame, asset, style, extend, restyle, lip_sync). Keys in
    # ``list_keys`` take lists. ``named`` = the prompt may address references
    # as @name (a legend maps each to its list position). ``camera_key`` names
    # the input that takes structured camera moves (Luma ``concepts``).
    video_role_keys: dict[str, str] = field(default_factory=dict)
    named: bool = False
    camera_key: str | None = None

    def video_transport(self) -> frozenset[str]:
        out = set(self.video_role_keys)
        if self.named:
            out.add("named")
        if self.camera_key:
            out.add("camera_control")
        return frozenset(out)

    def build_video_input(self, config: UnifiedConfig, controls: Any) -> dict[str, Any]:
        """Video input dict = typed video roles on their native keys + catalog
        params. The gate (BaseMediaGeneration) has already refused anything
        this descriptor cannot carry, so every roled block lands somewhere."""
        from matrx_ai.config.message_config import pick_image_by_role
        from matrx_ai.media.video_reference_roles import (
            VIDEO_REFERENCE_ROLES,
            camera_to_luma_concepts,
            collect_video_references,
            named_legend,
            named_references,
            with_named_legend,
        )

        refs = collect_video_references(config.messages)
        if "first_frame" not in refs and "first_frame" in self.video_role_keys:
            untagged = pick_image_by_role(config.messages, None) or config.image_input
            if untagged is not None:
                refs = {**refs, "first_frame": [untagged]}

        params = BaseMediaGeneration._outbound_params(
            controls,
            config,
            context={"has_image_input": bool(refs.get("first_frame") or refs.get("asset"))},
            extra_canonical={"negative_prompt": _tagged_negative_prompt(config)},
        )
        out: dict[str, Any] = {self.prompt_key: _prompt(config)}
        out.update(params)

        positions: dict[int, int] = {}
        for role, key in self.video_role_keys.items():
            items = refs.get(role) or []
            if not items:
                continue
            urls: list[str] = []
            for block in items:
                url = _mediaref_url(block)
                if not url:
                    noun = "video" if role in VIDEO_REFERENCE_ROLES else (
                        "audio" if role == "lip_sync" else "image"
                    )
                    raise ValueError(
                        f"The {role.replace('_', ' ')} {noun} could not be read. "
                        "Re-upload it and run again."
                    )
                urls.append(url)
            if key in self.list_keys:
                existing = out.get(key) or []
                for block, url in zip(items, urls, strict=True):
                    existing.append(url)
                    positions[id(block)] = len(existing)
                out[key] = existing
            else:
                out[key] = urls[-1]

        named = named_references(refs)
        if named:
            out[self.prompt_key] = with_named_legend(
                out.get(self.prompt_key) or "", named_legend(named, positions)
            )
        camera = getattr(config, "camera_control", None)
        if camera and self.camera_key:
            out[self.camera_key] = camera_to_luma_concepts(camera)
        return out

    def build_input(self, config: UnifiedConfig, controls: Any) -> dict[str, Any]:
        """Model input dict = structural media wiring + catalog params."""
        if self.modality == "video" and self.video_role_keys:
            return self.build_video_input(config, controls)
        from matrx_ai.media.image_reference_roles import (
            collect_role_images,
            ordered_role_images,
            resolve_roled,
            with_legend,
        )

        roled = resolve_roled(
            ordered_role_images(collect_role_images(config.messages), self.role_keys),
            _mediaref_url,
        )
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
        if roled:
            legend: list[tuple[str, Any]] = []
            lists: dict[str, list[str]] = {}
            for role, url in roled:
                key = self.role_keys[role]
                if key in self.list_keys:
                    lists.setdefault(key, []).append(url)
                    if key == self.refs_key and self.start_in_refs:
                        legend.append((role, url))
                else:
                    out[key] = url
            for key, urls in lists.items():
                existing = out.get(key) or []
                out[key] = urls + [u for u in existing if u not in urls]
            if legend:
                out[self.prompt_key] = with_legend(out.get(self.prompt_key) or "", legend)
        return out


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


_FLAT_ROLES = ("edit_target", "subject", "character", "style")


def _flat(key: str) -> dict[str, Any]:
    """Every flat-list reference role rides one input list (legend in prompt)."""
    return {"role_keys": dict.fromkeys(_FLAT_ROLES, key), "list_keys": frozenset({key})}


# Ideogram v3 on Replicate: native inpainting (image + mask) and a native
# style-reference list (schema read 2026-09-22 from the Replicate model API).
_IDEOGRAM_ROLES: dict[str, Any] = {
    "role_keys": {
        "edit_target": "image",
        "mask": "mask",
        "style": "style_reference_images",
    },
    "list_keys": frozenset({"style_reference_images"}),
}


_IMAGE_MODELS: list[ModelDescriptor] = [
    # FLUX 2: ONE ``input_images`` list (max 8) — schema read 2026-09-22; the
    # earlier ``image_input`` / ``reference_images`` keys do not exist on
    # these models and were silently ignored by Replicate.
    ModelDescriptor(
        "black-forest-labs/flux-2-pro", "image",
        refs_key="input_images", refs_max=8, start_in_refs=True, **_flat("input_images"),
    ),
    ModelDescriptor(
        "black-forest-labs/flux-2-max", "image",
        refs_key="input_images", refs_max=8, start_in_refs=True, **_flat("input_images"),
    ),
    ModelDescriptor(
        "black-forest-labs/flux-2-flex", "image",
        refs_key="input_images", refs_max=8, start_in_refs=True, **_flat("input_images"),
    ),
    # gpt-image: start + references ride ONE ``input_images`` list (max 16).
    ModelDescriptor(
        "openai/gpt-image-2", "image",
        refs_key="input_images", refs_max=16, start_in_refs=True, **_flat("input_images"),
    ),
    ModelDescriptor(
        "openai/gpt-image-1.5", "image",
        refs_key="input_images", refs_max=16, start_in_refs=True, **_flat("input_images"),
    ),
    # Imagen 4 is text-only on Replicate.
    ModelDescriptor("google/imagen-4", "image"),
    ModelDescriptor("google/imagen-4-fast", "image"),
    ModelDescriptor("google/imagen-4-ultra", "image"),
    # nano-banana: start + references ride ONE ``image_input`` list (max 14).
    ModelDescriptor(
        "google/nano-banana-2", "image",
        refs_key="image_input", refs_max=14, start_in_refs=True, **_flat("image_input"),
    ),
    ModelDescriptor(
        "google/nano-banana-pro", "image",
        refs_key="image_input", refs_max=14, start_in_refs=True, **_flat("image_input"),
    ),
    ModelDescriptor("ideogram-ai/ideogram-v3-turbo", "image", **_IDEOGRAM_ROLES),
    ModelDescriptor("ideogram-ai/ideogram-v3", "image", **_IDEOGRAM_ROLES),
    ModelDescriptor("ideogram-ai/ideogram-v3-balanced", "image", **_IDEOGRAM_ROLES),
    ModelDescriptor("ideogram-ai/ideogram-v3-quality", "image", **_IDEOGRAM_ROLES),
    ModelDescriptor("recraft-ai/recraft-v4", "image"),
    ModelDescriptor("recraft-ai/recraft-v4-svg", "image", default_mime="image/svg+xml"),
    # Seedream 4.5: ONE ``image_input`` list (schema read 2026-09-22).
    ModelDescriptor(
        "bytedance/seedream-4.5", "image",
        refs_key="image_input", refs_max=14, start_in_refs=True, **_flat("image_input"),
    ),
]


# Video input keys: schemas read 2026-09-22 from the Replicate model API
# (GET /v1/models/{owner}/{name} -> latest_version.openapi_schema). The earlier
# keys ``last_frame_image`` (Veo), ``prompt_text``/``prompt_image`` (Runway)
# and ``last_frame_image`` (Hailuo) do not exist on those models and were
# silently ignored by Replicate.
_VEO_REPLICATE = {
    "video_role_keys": {
        "first_frame": "image",
        "last_frame": "last_frame",
        "asset": "reference_images",
    },
    "list_keys": frozenset({"reference_images"}),
    "named": True,
}

_VIDEO_MODELS: list[ModelDescriptor] = [
    ModelDescriptor("google/veo-3.1", "video", **_VEO_REPLICATE),
    ModelDescriptor("google/veo-3.1-fast", "video", **_VEO_REPLICATE),
    ModelDescriptor(
        "runwayml/gen-4.5", "video",
        video_role_keys={"first_frame": "image"},
    ),
    # Runway Aleph: re-renders an input clip (restyle) with an optional
    # style/content reference image.
    ModelDescriptor(
        "runwayml/gen4-aleph", "video",
        video_role_keys={"restyle": "video", "style": "reference_image"},
    ),
    # Seedance 2.0: first/last frame OR up to 9 reference images, 3 reference
    # videos (motion/style/edit) and 3 reference audios (lip sync); the prompt
    # addresses references by position, so names ride a legend.
    ModelDescriptor(
        "bytedance/seedance-2.0", "video",
        video_role_keys={
            "first_frame": "image",
            "last_frame": "last_frame_image",
            "asset": "reference_images",
            "style": "reference_images",
            "restyle": "reference_videos",
            "lip_sync": "reference_audios",
        },
        list_keys=frozenset({"reference_images", "reference_videos", "reference_audios"}),
        named=True,
    ),
    ModelDescriptor(
        "kwaivgi/kling-v3-video", "video",
        video_role_keys={"first_frame": "start_image", "last_frame": "end_image"},
    ),
    # Kling lip sync: a clip plus the speech its face mouths.
    ModelDescriptor(
        "kwaivgi/kling-lip-sync", "video", prompt_key="text",
        video_role_keys={"restyle": "video_url", "lip_sync": "audio_file"},
    ),
    ModelDescriptor(
        "wan-video/wan-2.7-t2v", "video", video_role_keys={"first_frame": "image"}
    ),
    ModelDescriptor(
        "wan-video/wan-2.7-i2v", "video", video_role_keys={"first_frame": "image"}
    ),
    # Luma Ray: keyframes frame0/frame1 = start_image/end_image; camera moves
    # ride ``concepts`` (the canonical move vocabulary is Luma's own).
    ModelDescriptor(
        "luma/ray-2-720p", "video",
        video_role_keys={"first_frame": "start_image", "last_frame": "end_image"},
        camera_key="concepts",
    ),
    ModelDescriptor(
        "luma/ray-flash-2-720p", "video",
        video_role_keys={"first_frame": "start_image", "last_frame": "end_image"},
        camera_key="concepts",
    ),
    # luma/ray-3 is NOT a Replicate model ("Model not found", 2026-09-22); the
    # descriptor stays so the catalog row fails by name, not by KeyError.
    ModelDescriptor(
        "luma/ray-3", "video",
        video_role_keys={"first_frame": "start_image", "last_frame": "end_image"},
        camera_key="concepts",
    ),
    ModelDescriptor(
        "minimax/hailuo-2.3", "video",
        video_role_keys={"first_frame": "first_frame_image"},
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

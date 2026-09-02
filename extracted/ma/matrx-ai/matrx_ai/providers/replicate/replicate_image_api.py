"""Replicate image generation — thin transport + per-model descriptors.

Calls ``replicate.async_run(slug, input=...)`` with the model's slug
exactly as registered in ``MODEL_DESCRIPTORS``. The descriptor's
``to_input(config)`` builds the model-specific input dict.
"""

from __future__ import annotations

from typing import Any

import replicate

from matrx_ai.config import UnifiedConfig
from matrx_ai.providers.base_media import (
    BaseMediaGeneration,
    GeneratedAsset,
)

from .model_descriptors import (
    ModelDescriptor,
    _default_from_output,
    get_descriptor,
)


class ReplicateImageGeneration(BaseMediaGeneration):
    provider = "replicate"
    modality = "image"
    starting_message = "Generating image (Replicate)..."
    # Enforceable per-model IF the model exposes a safety knob
    # (disable_safety_checker / safety_tolerance); otherwise the override blocks
    # the minor's request (WP13).
    supports_minor_safe_image = True

    def __init__(self):
        self._pending_descriptor: ModelDescriptor | None = None

    def _build_kwargs(
        self, unified_config: UnifiedConfig, profile: Any
    ) -> dict[str, Any]:
        descriptor = self._lookup_descriptor(unified_config.model)
        # Stash for _extract_assets — base.execute() runs the request
        # serially so this is safe per-instance.
        self._pending_descriptor = descriptor
        return {
            "ref": descriptor.slug,
            "input": descriptor.build_input(unified_config, profile.controls),
        }

    def _apply_minor_image_overrides(
        self, kwargs: dict[str, Any], unified_config: UnifiedConfig, profile: Any
    ) -> None:
        # Re-enable the NSFW safety checker (our catalog default disables it) and
        # tighten any safety_tolerance for a minor. If the model exposes NEITHER
        # knob we cannot guarantee filtering — block (the base converts a raise
        # here into MinorImageBlockedError).
        image_input = kwargs.get("input")
        if not isinstance(image_input, dict):
            raise ValueError("replicate image kwargs missing dict 'input' for minor safety")
        has_knob = False
        if "disable_safety_checker" in image_input:
            image_input["disable_safety_checker"] = False
            has_knob = True
        if "safety_tolerance" in image_input:
            # FLUX safety_tolerance: 1 (strictest) .. 6 (most permissive).
            image_input["safety_tolerance"] = 1
            has_knob = True
        if not has_knob:
            raise ValueError(
                f"replicate model {kwargs.get('ref')!r} exposes no safety knob "
                f"(disable_safety_checker/safety_tolerance) — cannot enforce a "
                f"minor content-safety filter"
            )

    def _lookup_descriptor(self, slug: str) -> ModelDescriptor:
        d = get_descriptor(slug)
        if d is None:
            raise ValueError(
                f"No Replicate model descriptor for slug {slug!r}. Add one "
                f"to packages/matrx-ai/matrx_ai/providers/replicate/"
                f"model_descriptors.py."
            )
        if d.modality != "image":
            raise ValueError(
                f"Model {slug!r} is registered as {d.modality}, not image"
            )
        return d

    def _telemetry_url(self, unified_config: UnifiedConfig, kwargs: dict[str, Any]) -> str:
        return f"https://api.replicate.com/v1/models/{kwargs.get('ref')}/predictions"

    async def _call_provider(self, kwargs: dict[str, Any]) -> Any:
        from matrx_ai.providers.replicate.rate_limit import acquire_replicate_slot

        await acquire_replicate_slot()
        return await replicate.async_run(
            kwargs["ref"], input=kwargs["input"], use_file_output=True
        )

    def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        descriptor = self._descriptor_for_kwargs() or _UnknownDescriptor("image")
        if descriptor.from_output is not None:
            return descriptor.from_output(raw, descriptor)
        return _default_from_output(raw, descriptor)

    def _descriptor_for_kwargs(self) -> ModelDescriptor | None:
        # Stash the descriptor on self in _build_kwargs so _extract_assets
        # can read it. We do that with a tiny override.
        return getattr(self, "_pending_descriptor", None)

    def _classify_error(self, exc: Exception) -> Any:
        from matrx_ai.providers.errors import classify_provider_error

        return classify_provider_error("replicate", exc)

    def _map_generation_metadata(
        self,
        *,
        raw: Any,
        asset,
        asset_index: int,
        request_kwargs: dict[str, Any],
        unified_config,
        prompt,
        n_returned: int,
        duration_ms,
        cost_usd,
    ):
        """Phase 2b — pull Replicate input knobs (seed/steps/guidance/
        negative_prompt/aspect_ratio + width/height) into canonical
        MediaGenerationMetadata. Everything else lives under
        ``provider_extras.input`` so per-model knobs survive."""
        from matrx_ai.media.generation_metadata import (
            build_default_metadata, map_replicate_image_response,
        )

        try:
            return map_replicate_image_response(
                raw=raw, item=None, request_kwargs=request_kwargs,
                prompt=prompt or "",
                model=unified_config.model or request_kwargs.get("ref", ""),
                n_returned=n_returned,
                duration_ms=duration_ms, cost_usd=cost_usd,
            )
        except Exception:
            return build_default_metadata(
                kind="image", provider="replicate",
                model=unified_config.model or "",
                prompt=prompt, n_returned=n_returned,
                duration_ms=duration_ms, cost_usd=cost_usd,
            )


class _UnknownDescriptor:
    """Minimal descriptor stub for fallback handling."""
    from_output = None

    def __init__(self, modality: str):
        self.modality = modality
        self.slug = ""
        self.default_mime = ""

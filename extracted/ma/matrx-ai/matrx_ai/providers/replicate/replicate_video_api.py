"""Replicate video generation — same transport as image, video descriptors."""

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
from .replicate_image_api import _UnknownDescriptor


class ReplicateVideoGeneration(BaseMediaGeneration):
    provider = "replicate"
    modality = "video"
    starting_message = "Starting video generation (Replicate)..."

    def __init__(self):
        self._pending_descriptor: ModelDescriptor | None = None

    def _build_kwargs(
        self, unified_config: UnifiedConfig, profile: Any
    ) -> dict[str, Any]:
        descriptor = self._lookup_descriptor(unified_config.model)
        self._pending_descriptor = descriptor
        return {
            "ref": descriptor.slug,
            "input": descriptor.build_input(unified_config, profile.controls),
        }

    def _lookup_descriptor(self, slug: str) -> ModelDescriptor:
        d = get_descriptor(slug)
        if d is None:
            raise ValueError(
                f"No Replicate model descriptor for slug {slug!r}. Add one "
                f"to packages/matrx-ai/matrx_ai/providers/replicate/"
                f"model_descriptors.py."
            )
        if d.modality != "video":
            raise ValueError(
                f"Model {slug!r} is registered as {d.modality}, not video"
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
        descriptor = self._pending_descriptor or _UnknownDescriptor("video")
        if descriptor.from_output is not None:
            return descriptor.from_output(raw, descriptor)
        return _default_from_output(raw, descriptor)

    def _classify_error(self, exc: Exception) -> Any:
        from matrx_ai.providers.errors import classify_provider_error

        return classify_provider_error("replicate", exc)

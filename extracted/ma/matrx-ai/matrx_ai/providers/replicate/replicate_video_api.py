"""Replicate video generation — same transport as image, video descriptors."""

from __future__ import annotations

from typing import Any

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

    def video_role_transport(self, unified_config: UnifiedConfig) -> frozenset[str]:
        """What this model's Replicate schema can carry (descriptor data)."""
        descriptor = get_descriptor(unified_config.model or "")
        return descriptor.video_transport() if descriptor is not None else frozenset()

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
        from matrx_ai.providers.replicate.client import create_prediction, get_replicate_client

        # Create only (no ``Prefer: wait``): the POST returns once queued. The wait
        # happens in ``_poll_if_long_running`` under the video deadline knob.
        return await create_prediction(get_replicate_client(), kwargs["ref"], kwargs["input"])

    async def _poll_if_long_running(self, raw: Any) -> Any:
        from matrx_ai.providers.replicate.client import await_prediction

        return await await_prediction(raw, modality="video", ref=str(getattr(raw, "model", "") or ""))

    def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        descriptor = self._pending_descriptor or _UnknownDescriptor("video")
        if descriptor.from_output is not None:
            return descriptor.from_output(raw, descriptor)
        return _default_from_output(raw, descriptor)

    def _classify_error(self, exc: Exception) -> Any:
        from matrx_ai.providers.errors import classify_provider_error

        return classify_provider_error("replicate", exc)

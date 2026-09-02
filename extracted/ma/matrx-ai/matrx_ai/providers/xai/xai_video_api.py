"""xAI grok-imagine video generation — full 5-operation stack on a single
``grok-imagine-video`` model:

  - text-to-video        → ``client.video.generate(prompt, model)``
  - image-to-video       → ``client.video.generate(prompt, model, image_url=)``
  - reference-to-video   → ``client.video.generate(prompt, model, reference_image_urls=[...])``
  - video edit           → ``client.video.generate(prompt, model, video_url=)``
  - video extension      → ``client.video.extend(prompt, model, video_url, duration=)``

The xai_sdk handles polling internally — `generate` and `extend` block
until the job finishes (or raises). Native synced audio is bundled.

Routing: ``UnifiedConfig.video_action == "extend"`` → extend; everything else
rides generate (text/image/ref/edit chosen by which fields are set).
"""

from __future__ import annotations

from typing import Any

import xai_sdk

from matrx_ai.config import ProviderCharge, UnifiedConfig
from matrx_ai.config.message_config import (
    iter_images_by_role,
    pick_image_by_role,
    pick_text_by_role,
)
from matrx_ai.providers.base_media import (
    BaseMediaGeneration,
    GeneratedAsset,
)
from matrx_ai.providers.keys import keyed_provider_client


class XAIVideoGeneration(BaseMediaGeneration):
    provider = "xai"
    modality = "video"
    starting_message = "Starting video generation (Grok Imagine)..."

    def _provider_charge(self, raw: Any) -> ProviderCharge | None:
        from matrx_ai.providers.xai.translator import provider_charge_from_xai_usage

        usage = getattr(raw, "usage", None)
        return provider_charge_from_xai_usage(usage) if usage is not None else None

    # Built lazily on first ACCESS and memoized on the RESOLVED KEY VALUE —
    # a host-side key rotation builds a fresh SDK client on the next request.
    client = keyed_provider_client(
        "XAI_API_KEY",
        factory=lambda api_key: xai_sdk.AsyncClient(api_key=api_key),
    )

    def __init__(self):
        # "extend" routes to client.video.extend; anything else generates
        # (text/image/ref/edit-by-video_url all ride generate). Set per call
        # from UnifiedConfig.video_action — the field that replaced the dead
        # xai_video_extend api_class routing.
        self._is_extend: bool = False

    def _build_kwargs(
        self, unified_config: UnifiedConfig, profile: Any
    ) -> dict[str, Any]:
        self._is_extend = unified_config.video_action == "extend"
        prompt = self._extract_prompt(unified_config)

        # aspect_ratio / resolution enum gates + duration rename are catalog
        # rules (translator_key ``xai_video`` — _ai_029).
        params = self._outbound_params(profile.controls, unified_config)
        kwargs: dict[str, Any] = {
            "prompt": prompt,
            "model": unified_config.model or "grok-imagine-video",
            **params,
        }

        # Image-to-video. Prefer user-message-tagged start_image (or first
        # un-tagged image), fall back to settings image_input.
        start = (
            pick_image_by_role(unified_config.messages, "start_image")
            or pick_image_by_role(unified_config.messages, None)
        )
        if start is not None:
            u = self._mediaref_url(start)
        elif unified_config.image_input is not None:
            u = self._mediaref_url(unified_config.image_input)
        else:
            u = None
        if u:
            kwargs["image_url"] = u

        # Reference-to-video. User-message-tagged refs take precedence.
        refs: list[str] = []
        for ref in iter_images_by_role(unified_config.messages, "reference"):
            u = self._mediaref_url(ref)
            if u:
                refs.append(u)
        if not refs:
            for ref in unified_config.image_inputs or []:
                u = self._mediaref_url(ref)
                if u:
                    refs.append(u)
            for ref in unified_config.reference_images or []:
                u = self._mediaref_url(ref)
                if u:
                    refs.append(u)
        if refs:
            kwargs["reference_image_urls"] = refs[:3]

        # Video input — for edit (top-level) or extend (separate kwarg path).
        if unified_config.video_input is not None:
            u = self._mediaref_url(unified_config.video_input)
            if u:
                kwargs["video_url"] = u

        return kwargs

    def _telemetry_url(self, unified_config: UnifiedConfig, kwargs: dict[str, Any]) -> str:
        if self._is_extend:
            return "https://api.x.ai/v1/videos/extensions"
        return "https://api.x.ai/v1/videos/generations"

    async def _call_provider(self, kwargs: dict[str, Any]) -> Any:
        prompt = kwargs.pop("prompt")
        model = kwargs.pop("model")
        if self._is_extend:
            video_url = kwargs.pop("video_url", None)
            if not video_url:
                raise ValueError("video_action='extend' requires video_input on UnifiedConfig")
            duration = kwargs.pop("duration", None)
            return await self.client.video.extend(
                prompt, model, video_url, duration=duration
            )
        return await self.client.video.generate(prompt, model, **kwargs)

    def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        """``VideoResponse``: ``video.url``, ``video.duration``,
        ``video.respect_moderation``."""
        # The structure depends on the SDK version: `raw.video.url` or
        # `raw.url`. Try both.
        url = (
            getattr(getattr(raw, "video", None), "url", None)
            or getattr(raw, "url", None)
        )
        if not url:
            return []
        mime = getattr(getattr(raw, "video", None), "mime_type", None) or "video/mp4"
        metadata: dict[str, Any] = {}
        duration = getattr(getattr(raw, "video", None), "duration", None)
        if duration is not None:
            metadata["duration_seconds"] = duration
        return [GeneratedAsset(url=url, mime_type=mime, metadata=metadata)]

    def _classify_error(self, exc: Exception) -> Any:
        from matrx_ai.providers.errors import classify_xai_error

        return classify_xai_error(exc)

    @staticmethod
    def _extract_prompt(config: UnifiedConfig) -> str:
        return pick_text_by_role(config.messages, None) or ""

    @staticmethod
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

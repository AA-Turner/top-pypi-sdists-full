"""Together AI image generation — single adapter across all flagship models.

The Together API exposes one body shape for image generation
(``client.images.generate``). Per-model param support lives in the CATALOG —
ai.api.rules (translator_key ``together_image``) + each offering's override
(seeded by db/migrations/_ai_029_seed_media_family_rules.py). This class owns
only the STRUCTURAL parts: prompt extraction and media-ref -> URL resolution;
the resolved URLs are handed to the rules as canonical values so per-model
support (FLUX vs imagen vs gemini on Together) is data, not code.
"""

from __future__ import annotations

import asyncio
import base64
import threading
import time
from typing import Any

from together import AsyncTogether

from matrx_ai.config import UnifiedConfig
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

# Together applies dynamic per-model request limits in one-second windows and
# explicitly rewards steady traffic over bursts. Reserve image request starts
# process-wide so concurrent podcast/user tasks cannot stampede the endpoint.
TOGETHER_IMAGE_MIN_START_INTERVAL_SECONDS = 2.0
_together_image_pacing_lock = threading.Lock()
_together_image_next_start_at = 0.0


async def _pace_together_image_request() -> None:
    global _together_image_next_start_at

    now = time.monotonic()
    with _together_image_pacing_lock:
        start_at = max(now, _together_image_next_start_at)
        _together_image_next_start_at = (
            start_at + TOGETHER_IMAGE_MIN_START_INTERVAL_SECONDS
        )
    delay = start_at - now
    if delay > 0:
        await asyncio.sleep(delay)


class TogetherImageGeneration(BaseMediaGeneration):
    provider = "together"
    modality = "image"
    starting_message = "Generating image (Together)..."
    # No enforceable provider-side NSFW filter → supports_minor_safe_image stays
    # False (base default): a minor's image request on Together is REFUSED before
    # the paid call (WP13, "block if filtering can't be guaranteed").

    client = keyed_provider_client(
        "TOGETHER_API_KEY",
        factory=lambda api_key: AsyncTogether(api_key=api_key),
    )

    def _build_kwargs(
        self, unified_config: UnifiedConfig, profile: Any
    ) -> dict[str, Any]:
        prompt = self._extract_prompt(unified_config)

        # Structural canonical enrichments — message-tagged negative prompt and
        # resolved media URLs. Whether THIS model accepts each of them is
        # catalog data (offering.override supported flags), not code.
        extra: dict[str, Any] = {}
        neg = pick_text_by_role(unified_config.messages, "negative_prompt")
        if neg:
            extra["negative_prompt"] = neg

        # image-to-image (single). Prefer user-message-tagged start_image
        # (or first un-tagged image), fall back to settings image_input.
        start = pick_image_by_role(unified_config.messages, "start_image") or pick_image_by_role(
            unified_config.messages, None
        )
        start_url = (
            self._mediaref_url(start)
            if start is not None
            else self._mediaref_url(unified_config.image_input)
        )
        if start_url:
            extra["image_url"] = start_url

        # multi-reference. User-message-tagged refs take precedence.
        refs: list[str] = []
        for r in iter_images_by_role(unified_config.messages, "reference"):
            ref_url = self._mediaref_url(r)
            if ref_url:
                refs.append(ref_url)
        if not refs:
            for r in unified_config.image_inputs or []:
                ref_url = self._mediaref_url(r)
                if ref_url:
                    refs.append(ref_url)
        if refs:
            extra["reference_images"] = refs

        if unified_config.image_loras:
            # Together expects [{"path": str, "scale": float}]. Pass as-is.
            extra["image_loras"] = unified_config.image_loras

        params = self._outbound_params(profile.controls, unified_config, extra_canonical=extra)
        return {"model": unified_config.model, "prompt": prompt, **params}

    def _telemetry_url(self, unified_config: UnifiedConfig, kwargs: dict[str, Any]) -> str:
        return "https://api.together.xyz/v1/images/generations"

    async def _call_provider(self, kwargs: dict[str, Any]) -> Any:
        await _pace_together_image_request()
        return await self.client.images.generate(**kwargs)

    def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        data = getattr(raw, "data", None) or []
        assets: list[GeneratedAsset] = []
        for item in data:
            b64 = getattr(item, "b64_json", None)
            url = getattr(item, "url", None)
            mime = "image/jpeg"
            if b64:
                try:
                    bytes_ = base64.b64decode(b64)
                except Exception:
                    continue
                assets.append(GeneratedAsset(data=bytes_, mime_type=mime))
            elif url:
                assets.append(GeneratedAsset(url=url, mime_type=mime))
        return assets

    def _classify_error(self, exc: Exception) -> Any:
        from matrx_ai.providers.errors import classify_provider_error

        return classify_provider_error("together", exc)

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
        """Phase 2 — Together Flux / SD-family canonical metadata mapper.
        Surfaces seed / steps / cfg_scale (guidance) for "regenerate with
        same settings" reproducibility.
        """
        from matrx_ai.media.generation_metadata import (
            build_default_metadata,
            map_together_image_response,
        )

        try:
            data = getattr(raw, "data", None) or []
            item = data[asset_index] if asset_index < len(data) else None
            if item is None:
                raise IndexError("no per-asset item")
            return map_together_image_response(
                raw=raw, item=item, request_kwargs=request_kwargs,
                prompt=prompt or "",
                model=unified_config.model or "",
                n_returned=n_returned,
                duration_ms=duration_ms, cost_usd=cost_usd,
            )
        except Exception:
            return build_default_metadata(
                kind="image", provider="together",
                model=unified_config.model or "",
                prompt=prompt, n_returned=n_returned,
                duration_ms=duration_ms, cost_usd=cost_usd,
            )

    @staticmethod
    def _extract_prompt(config: UnifiedConfig) -> str:
        prompt = ""
        for msg in reversed(list(config.messages)):
            if msg.role == "user":
                for part in msg.content:
                    if hasattr(part, "text") and part.text:
                        prompt = part.text
                        break
            if prompt:
                break
        return prompt

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

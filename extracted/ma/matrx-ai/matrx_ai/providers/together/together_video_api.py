"""Together AI video generation — single adapter across all flagship video
models with async submit + poll lifecycle.

The Together video API (``client.videos.create`` → ``client.videos.retrieve``)
exposes one body shape across Veo 3, Sora 2, Kling 2.1, Seedance 1.0,
Wan 2.7 and others. Per-model param gating lives in the CATALOG —
ai.api.rules (translator_key ``together_video``) + per-offering overrides
(db/migrations/_ai_029_seed_media_family_rules.py); this class owns only the
structural media wiring (start image, frame list, references).

Async pattern: create returns a ``VideoJob`` with ``id``; poll
``client.videos.retrieve(id)`` until ``status == 'completed'``, then
read ``result.video.url`` (or similar — varies by model).
"""

from __future__ import annotations

import asyncio
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

class TogetherVideoGeneration(BaseMediaGeneration):
    provider = "together"
    modality = "video"
    starting_message = "Starting video generation (Together)..."

    client = keyed_provider_client(
        "TOGETHER_API_KEY",
        factory=lambda api_key: AsyncTogether(api_key=api_key),
    )

    def _build_kwargs(
        self, unified_config: UnifiedConfig, profile: Any
    ) -> dict[str, Any]:
        prompt = self._extract_prompt(unified_config)

        # Structural canonical enrichments — the catalog rules gate per-model
        # support for each of these (offering.override supported flags).
        extra: dict[str, Any] = {}
        neg = pick_text_by_role(unified_config.messages, "negative_prompt")
        if neg:
            extra["negative_prompt"] = neg

        # Image-to-video: media={"image": <url>}
        # Prefer user-message-tagged start_image (or first un-tagged image),
        # fall back to settings-level image_input.
        start = pick_image_by_role(unified_config.messages, "start_image") or pick_image_by_role(
            unified_config.messages, None
        )
        start_url = (
            self._mediaref_url(start)
            if start is not None
            else self._mediaref_url(unified_config.image_input)
        )
        if start_url:
            extra["media"] = {"image": start_url}

        # frame_images: Kling multi-shot. Build from explicit settings list
        # OR from user-message end_image / last_frame_image roles.
        frames: list[dict[str, Any]] = []
        if unified_config.frame_images:
            for idx, fi in enumerate(unified_config.frame_images):
                frame_url = self._mediaref_url(fi)
                if frame_url:
                    frames.append({"image": frame_url, "frame_number": idx})
        else:
            end = pick_image_by_role(unified_config.messages, "end_image") or pick_image_by_role(
                unified_config.messages, "last_frame_image"
            )
            if end is not None:
                frame_url = self._mediaref_url(end)
                if frame_url:
                    frames.append({"image": frame_url, "frame_number": -1})
        if frames:
            extra["frame_images"] = frames

        refs: list[str] = []
        # Prefer user-message-tagged refs first.
        for r in iter_images_by_role(unified_config.messages, "reference"):
            ref_url = self._mediaref_url(r)
            if ref_url:
                refs.append(ref_url)
        if not refs:
            for r in unified_config.image_inputs or []:
                ref_url = self._mediaref_url(r)
                if ref_url:
                    refs.append(ref_url)
            for r in unified_config.reference_images or []:
                ref_url = self._mediaref_url(r)
                if ref_url:
                    refs.append(ref_url)
        if refs:
            extra["reference_images"] = refs

        params = self._outbound_params(profile.controls, unified_config, extra_canonical=extra)
        return {"model": unified_config.model, "prompt": prompt, **params}

    def _telemetry_url(self, unified_config: UnifiedConfig, kwargs: dict[str, Any]) -> str:
        return "https://api.together.xyz/v1/videos/generations"

    async def _call_provider(self, kwargs: dict[str, Any]) -> Any:
        return await self.client.videos.create(**kwargs)

    async def _poll_if_long_running(self, raw: Any) -> Any:
        # raw is a VideoJob with .id; poll until status=='completed'.
        job_id = getattr(raw, "id", None)
        if not job_id:
            return raw

        # If the job already finished synchronously, accept it.
        status = getattr(raw, "status", None)
        if status in ("completed", "succeeded"):
            return raw
        if status in ("failed", "cancelled"):
            raise RuntimeError(
                f"Together video job ended with status={status}"
            )

        for _ in range(180):  # up to ~30 minutes
            await asyncio.sleep(10)
            updated = await self.client.videos.retrieve(job_id)
            status = getattr(updated, "status", None)
            if status in ("completed", "succeeded"):
                return updated
            if status in ("failed", "cancelled"):
                raise RuntimeError(
                    f"Together video job {job_id} ended with status={status}"
                )
        raise RuntimeError(f"Together video job {job_id} timed out after 30min")

    def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        # Result shape varies by SDK version. Probe common locations.
        candidates: list[Any] = []
        if hasattr(raw, "result") and raw.result:
            candidates.append(raw.result)
        if hasattr(raw, "data") and raw.data:
            candidates.extend(raw.data if isinstance(raw.data, list) else [raw.data])
        if hasattr(raw, "video") and raw.video:
            candidates.append(raw.video)
        if hasattr(raw, "url") and raw.url:
            return [GeneratedAsset(url=raw.url, mime_type="video/mp4",
                                   metadata={"together_job_id": getattr(raw, "id", None)})]

        assets: list[GeneratedAsset] = []
        for c in candidates:
            url = getattr(c, "url", None)
            if not url and isinstance(c, dict):
                url = c.get("url")
            if url:
                assets.append(
                    GeneratedAsset(
                        url=url,
                        mime_type="video/mp4",
                        metadata={"together_job_id": getattr(raw, "id", None)},
                    )
                )
        return assets

    def _classify_error(self, exc: Exception) -> Any:
        from matrx_ai.providers.errors import classify_provider_error

        return classify_provider_error("together", exc)

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
        return url if url else None

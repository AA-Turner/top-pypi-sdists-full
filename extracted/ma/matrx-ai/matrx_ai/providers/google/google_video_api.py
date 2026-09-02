"""Google Veo video generation — long-polling lifecycle through the unified
``BaseMediaGeneration`` scaffold.

Veo is fully separate from ``generate_content``: submit a job, poll until
``op.done``, then download each generated video and persist via
``save_media_async``. The base class handles persistence + emitter + error
classification; this subclass owns the SDK call, the polling loop, and the
asset extraction step (which itself blocks on ``client.files.download``).
"""

from __future__ import annotations

from typing import Any

from google import genai

from matrx_ai.config import UnifiedConfig
from matrx_ai.providers.base_media import (
    BaseMediaGeneration,
    GeneratedAsset,
)
from matrx_ai.providers.keys import keyed_provider_client

from .translator import GoogleTranslator


class GoogleVideoGeneration(BaseMediaGeneration):
    provider = "google"
    modality = "video"
    starting_message = "Starting video generation (Veo)..."

    client = keyed_provider_client(
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "GOOGLE_AI_STUDIO",
        factory=lambda api_key: genai.Client(
            api_key=api_key,
            http_options={"api_version": "v1beta"},
        ),
    )

    def __init__(self):
        self.translator = GoogleTranslator()

    def _build_kwargs(
        self, unified_config: UnifiedConfig, profile: Any
    ) -> dict[str, Any]:
        """Structural SDK-object nesting for Veo; every scalar param (aspect
        gate + 16:9 default, count clamp, resolution gate + 720p default,
        duration/audio/seed passthrough) comes from the catalog rules —
        translator_key ``google_video`` (_ai_029). Media refs (first frame,
        last frame, references) and the message-tagged negative prompt are
        structural."""
        from google.genai import types

        from matrx_ai.config.message_config import (
            iter_images_by_role,
            pick_image_by_role,
            pick_text_by_role,
        )

        prompt = self.translator._extract_prompt(unified_config)
        neg = pick_text_by_role(unified_config.messages, "negative_prompt")
        video_config_kwargs = self._outbound_params(
            profile.controls,
            unified_config,
            extra_canonical={"negative_prompt": neg},
        )
        # Veo generates an 8-second clip when duration is omitted. Make that
        # provider default explicit so the wire request and billing agree.
        video_config_kwargs.setdefault("duration_seconds", 8)

        # last_frame interpolation — prefer user-message "end_image"
        # (or untagged "last_frame_image" alias), fall back to settings.
        last_frame_block = pick_image_by_role(
            unified_config.messages, "end_image"
        ) or pick_image_by_role(unified_config.messages, "last_frame_image")
        last_frame_ref = (
            last_frame_block if last_frame_block is not None else unified_config.last_frame_image
        )
        last_frame = self.translator._mediaref_to_genai_image(last_frame_ref)
        if last_frame is not None:
            video_config_kwargs["last_frame"] = last_frame

        # reference_images — character / scene refs (multi).
        ref_blocks = list(iter_images_by_role(unified_config.messages, "reference"))
        ref_sources = ref_blocks if ref_blocks else (unified_config.reference_images or [])
        if ref_sources:
            ref_images = []
            for ref in ref_sources:
                genai_image = self.translator._mediaref_to_genai_image(ref)
                if genai_image is not None:
                    ref_images.append(genai_image)
            if ref_images:
                video_config_kwargs["reference_images"] = ref_images

        # Image-to-video first frame: prefer user-message "start_image"
        # (or untagged image_input), fall back to settings.
        start_block = pick_image_by_role(
            unified_config.messages, "start_image"
        ) or pick_image_by_role(unified_config.messages, None)
        start_ref = start_block if start_block is not None else unified_config.image_input
        if start_ref is None and unified_config.frame_images:
            start_ref = unified_config.frame_images[0]
        first_image = self.translator._mediaref_to_genai_image(start_ref)

        # Google exposes no adjustable Veo content-safety threshold. Its one
        # permissiveness control is personGeneration: current Veo models only
        # accept ALLOW_ALL for text-to-video and ALLOW_ADULT for image-driven
        # modes. Pin those least-restrictive supported values instead of
        # accepting a provider default or a stricter catalog override.
        video_config_kwargs["person_generation"] = (
            "ALLOW_ADULT" if first_image is not None else "ALLOW_ALL"
        )

        kwargs: dict[str, Any] = {
            "model": unified_config.model,
            "source": types.GenerateVideosSource(prompt=prompt),
            "config": types.GenerateVideosConfig(**video_config_kwargs),
        }
        if first_image is not None:
            kwargs["image"] = first_image

        return kwargs

    def _telemetry_url(self, unified_config: UnifiedConfig, kwargs: dict[str, Any]) -> str:
        model = kwargs.get("model") or unified_config.model or "unknown"
        return (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateVideos"
        )

    def _call_provider(self, kwargs: dict[str, Any]) -> Any:
        return self.client.models.generate_videos(**kwargs)

    def _poll_if_long_running(self, raw: Any) -> Any:
        import time

        from matrx_utils import vcprint

        op = raw
        while not op.done:
            vcprint(
                "[Google Video] Waiting for video... polling in 10s",
                color="cyan",
            )
            time.sleep(10)
            op = self.client.operations.get(op)
        return op

    def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        result = getattr(raw, "result", None) or getattr(raw, "response", None)
        if not result or not getattr(result, "generated_videos", None):
            return []

        assets: list[GeneratedAsset] = []
        for generated_video in result.generated_videos:
            # client.files.download returns raw bytes AND mutates the object
            # to set .video.video_bytes. Either is fine for us.
            video_bytes = self.client.files.download(file=generated_video.video)
            mime = getattr(generated_video.video, "mime_type", None) or "video/mp4"
            assets.append(GeneratedAsset(data=video_bytes, mime_type=mime))
        return assets

    def _classify_error(self, exc: Exception) -> Any:
        from matrx_ai.providers.errors import classify_google_error

        return classify_google_error(exc)

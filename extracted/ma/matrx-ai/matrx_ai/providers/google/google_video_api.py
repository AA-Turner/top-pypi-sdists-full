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
from matrx_ai.providers.sdk_drift import route_undeclared_params

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

    def video_role_transport(self, unified_config: UnifiedConfig) -> frozenset[str]:
        """Veo takes a first frame (``image``), a last frame
        (``config.last_frame``), asset/style references
        (``config.reference_images`` with ``reference_type``), and a clip to
        extend (``source.video``). Named references ride the asset list with an
        "@name is reference image N" legend. No structured camera control."""
        return frozenset(
            {"first_frame", "last_frame", "asset", "style", "extend", "named"}
        )

    def _genai_image_or_raise(self, ref: Any, label: str) -> Any:
        image = self.translator._mediaref_to_genai_image(ref)
        if image is None:
            raise ValueError(
                f"The {label} image could not be read. Re-upload it and run again."
            )
        return image

    def _build_kwargs(self, unified_config: UnifiedConfig, profile: Any) -> dict[str, Any]:
        """Structural SDK-object nesting for Veo; every scalar param (aspect
        gate + 16:9 default, count clamp, resolution gate + 720p default,
        duration/audio/seed passthrough) comes from the catalog rules —
        translator_key ``google_video`` (_ai_029). Media refs are structural
        and ride the typed video roles (media/video_reference_roles.py; legacy
        ``metadata.role`` tags fold in): first_frame -> ``image``, last_frame
        -> ``config.last_frame``, asset|style -> ``config.reference_images``
        (``reference_type`` ASSET|STYLE), extend -> ``source.video``."""
        from google.genai import types

        from matrx_ai.config.message_config import (
            pick_image_by_role,
            pick_text_by_role,
        )
        from matrx_ai.media.video_reference_roles import (
            collect_video_references,
            first_of,
            named_legend,
            named_references,
            with_named_legend,
        )

        refs = collect_video_references(unified_config.messages)
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

        # Last frame (interpolation): typed role, else settings.
        last_ref = first_of(refs, "last_frame")
        if last_ref is not None:
            video_config_kwargs["last_frame"] = self._genai_image_or_raise(last_ref, "Last frame")
        elif unified_config.last_frame_image is not None:
            last_frame = self.translator._mediaref_to_genai_image(unified_config.last_frame_image)
            if last_frame is not None:
                video_config_kwargs["last_frame"] = last_frame

        # Asset / style references, in authored order; settings fallback.
        reference_images: list[Any] = []
        positions: dict[int, int] = {}
        for role, ref_type in (("asset", "ASSET"), ("style", "STYLE")):
            for block in refs.get(role) or []:
                reference_images.append(
                    types.VideoGenerationReferenceImage(
                        image=self._genai_image_or_raise(block, role.capitalize()),
                        reference_type=ref_type,
                    )
                )
                positions[id(block)] = len(reference_images)
        if not reference_images:
            for ref in unified_config.reference_images or []:
                genai_image = self.translator._mediaref_to_genai_image(ref)
                if genai_image is not None:
                    reference_images.append(
                        types.VideoGenerationReferenceImage(
                            image=genai_image, reference_type="ASSET"
                        )
                    )
        if reference_images:
            video_config_kwargs["reference_images"] = reference_images

        named = named_references(refs)
        if named:
            prompt = with_named_legend(prompt, named_legend(named, positions))

        # First frame: typed role, else the first un-tagged image, else settings.
        start_ref = first_of(refs, "first_frame")
        if start_ref is not None:
            first_image = self._genai_image_or_raise(start_ref, "First frame")
        else:
            start_block = pick_image_by_role(unified_config.messages, None)
            fallback = start_block if start_block is not None else unified_config.image_input
            if fallback is None and unified_config.frame_images:
                fallback = unified_config.frame_images[0]
            first_image = self.translator._mediaref_to_genai_image(fallback)

        # Extend: the clip Veo continues.
        source_kwargs: dict[str, Any] = {"prompt": prompt}
        extend_ref = first_of(refs, "extend")
        if extend_ref is not None:
            source_kwargs["video"] = self._genai_video_or_raise(extend_ref)

        # Google exposes no adjustable Veo content-safety threshold. Its one
        # permissiveness control is personGeneration: current Veo models only
        # accept ALLOW_ALL for text-to-video and ALLOW_ADULT for image-driven
        # modes. Pin those least-restrictive supported values instead of
        # accepting a provider default or a stricter catalog override.
        video_config_kwargs["person_generation"] = (
            "ALLOW_ADULT" if (first_image is not None or reference_images) else "ALLOW_ALL"
        )

        # The SDK refuses `source` beside a top-level prompt/image/video
        # ("mutually exclusive — only use source"), so the first frame rides
        # INSIDE the source with the prompt (and the clip to extend).
        if first_image is not None:
            source_kwargs["image"] = first_image
        return {
            "model": unified_config.model,
            "source": types.GenerateVideosSource(**source_kwargs),
            "config": types.GenerateVideosConfig(**video_config_kwargs),
        }

    @staticmethod
    def _genai_video_or_raise(ref: Any) -> Any:
        """A ``types.Video`` for the clip to extend: inline bytes when the
        boundary pre-fetched them, else its URI. Nothing usable RAISES."""
        import base64

        from google.genai import types

        b64 = getattr(ref, "base64_data", None)
        mime = getattr(ref, "mime_type", None) or "video/mp4"
        if b64:
            return types.Video(video_bytes=base64.b64decode(b64), mime_type=mime)
        uri = getattr(ref, "file_uri", None) or getattr(ref, "resolved_url", None) or getattr(
            ref, "url", None
        )
        if uri:
            return types.Video(uri=uri, mime_type=mime)
        raise ValueError("The video to extend could not be read. Re-upload it and run again.")

    def _telemetry_url(self, unified_config: UnifiedConfig, kwargs: dict[str, Any]) -> str:
        model = kwargs.get("model") or unified_config.model or "unknown"
        return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateVideos"

    def _call_provider(self, kwargs: dict[str, Any]) -> Any:
        return self.client.models.generate_videos(
            **route_undeclared_params(self.client.models.generate_videos, kwargs, provider="google")
        )

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

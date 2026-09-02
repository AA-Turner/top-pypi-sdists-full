"""OpenAI video generation — Sora 2 / Sora 2 Pro.

Lifecycle on ``/v1/videos``:
  - ``client.videos.create_and_poll(...)`` for create (handles polling)
  - ``client.videos.create(...)`` + ``/v1/videos/extensions`` for extend
  - ``/v1/videos/edits`` for remix

Routing: ``UnifiedConfig.video_action`` — "extend" → extensions endpoint,
"edit" → edits endpoint, anything else → create_and_poll.
"""

from __future__ import annotations

from typing import Any

from openai import AsyncOpenAI

from matrx_ai.config import UnifiedConfig
from matrx_ai.providers.base_media import (
    BaseMediaGeneration,
    GeneratedAsset,
)
from matrx_ai.providers.keys import keyed_provider_client
from matrx_ai.providers.outbound_capture import make_capture_http_client

from .translator import OpenAITranslator


class OpenAIVideoGeneration(BaseMediaGeneration):
    provider = "openai"
    modality = "video"
    starting_message = "Starting video generation (Sora)..."

    client = keyed_provider_client(
        "OPENAI_API_KEY",
        factory=lambda api_key: AsyncOpenAI(
            api_key=api_key,
            http_client=make_capture_http_client(),
        ),
    )

    def __init__(self):
        self.translator = OpenAITranslator()
        # "extend" / "edit" route to the dedicated Sora endpoints; anything
        # else generates. Set per call from UnifiedConfig.video_action — the
        # field that replaced the dead openai_video_extend/_edit api_classes.
        self._video_action: str = "generate"

    def _build_kwargs(
        self, unified_config: UnifiedConfig, profile: Any
    ) -> dict[str, Any]:
        self._video_action = unified_config.video_action or "generate"
        if self._video_action == "extend":
            return self.translator.to_openai_video_extend(unified_config)
        if self._video_action == "edit":
            return self.translator.to_openai_video_edit(unified_config)

        # Generate: size derivation + seconds stringify are catalog rules
        # (translator_key ``openai_video`` — _ai_029); the first-frame image is
        # structural.
        from matrx_ai.config.message_config import pick_image_by_role

        prompt = self.translator._extract_prompt(unified_config)
        params = self._outbound_params(profile.controls, unified_config)
        kwargs: dict[str, Any] = {
            "model": unified_config.model,
            "prompt": prompt,
            **params,
        }
        start = (
            pick_image_by_role(unified_config.messages, "start_image")
            or pick_image_by_role(unified_config.messages, None)
            or unified_config.image_input
        )
        if start is not None:
            ref = self.translator._mediaref_to_file_tuple(start)
            if ref is not None:
                kwargs["input_reference"] = ref
        return kwargs

    def _telemetry_url(self, unified_config: UnifiedConfig, kwargs: dict[str, Any]) -> str:
        if self._video_action == "extend":
            return "https://api.openai.com/v1/videos/extensions"
        if self._video_action == "edit":
            return "https://api.openai.com/v1/videos/edits"
        return "https://api.openai.com/v1/videos"

    async def _call_provider(self, kwargs: dict[str, Any]) -> Any:
        # videos.create_and_poll handles the long-poll for us; the
        # extensions / edits endpoints currently live under a different
        # SDK surface — fall back to raw POST through the client.
        if self._video_action == "extend":
            return await self.client.post(
                "/videos/extensions", body=kwargs, cast_to=Any
            )
        if self._video_action == "edit":
            return await self.client.post("/videos/edits", body=kwargs, cast_to=Any)
        # Default: create + poll. The SDK exposes either create_and_poll
        # or create (we have to poll manually) depending on version.
        if hasattr(self.client.videos, "create_and_poll"):
            return await self.client.videos.create_and_poll(**kwargs)
        return await self.client.videos.create(**kwargs)

    async def _poll_if_long_running(self, raw: Any) -> Any:
        """Poll if the SDK didn't already do it for us."""
        import asyncio

        # If we got a finished video (status='completed'), nothing to do.
        status = getattr(raw, "status", None)
        if status in ("completed", "succeeded"):
            return raw
        if status in ("failed", "cancelled"):
            raise RuntimeError(f"OpenAI video job ended with status={status}")
        if status is None:
            return raw  # extension/edit endpoints return without polling

        video_id = getattr(raw, "id", None)
        if not video_id:
            return raw

        for _ in range(180):  # up to ~30 minutes at 10s
            await asyncio.sleep(10)
            updated = await self.client.videos.retrieve(video_id)
            status = getattr(updated, "status", None)
            if status == "completed":
                return updated
            if status in ("failed", "cancelled"):
                raise RuntimeError(
                    f"OpenAI video job {video_id} ended with status={status}"
                )
        raise RuntimeError(f"OpenAI video job {video_id} timed out after 30min")

    async def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        """Sora returns a video record; download its content."""
        video_id = getattr(raw, "id", None)
        if not video_id:
            return []
        # download_content returns either bytes or a stream-like object —
        # consume to bytes either way.
        try:
            content = await self.client.videos.download_content(video_id)
        except AttributeError:
            # Fallback: hit the content endpoint directly.
            content = await self.client.get(
                f"/videos/{video_id}/content", cast_to=Any
            )
        if hasattr(content, "read"):
            data = await self._read_async(content)
        elif isinstance(content, (bytes, bytearray)):
            data = bytes(content)
        else:
            # Last-resort: treat as URL.
            return [GeneratedAsset(url=str(content), mime_type="video/mp4",
                                   metadata={"openai_video_id": video_id})]
        return [
            GeneratedAsset(
                data=data,
                mime_type="video/mp4",
                metadata={"openai_video_id": video_id},
            )
        ]

    @staticmethod
    async def _read_async(stream: Any) -> bytes:
        chunks: list[bytes] = []
        # support both async iterators and sync .read()
        try:
            async for chunk in stream:  # type: ignore[union-attr]
                chunks.append(chunk if isinstance(chunk, bytes) else bytes(chunk))
        except TypeError:
            data = stream.read()
            return data if isinstance(data, bytes) else bytes(data)
        return b"".join(chunks)

    def _classify_error(self, exc: Exception) -> Any:
        from matrx_ai.providers.errors import classify_openai_error

        return classify_openai_error(exc)

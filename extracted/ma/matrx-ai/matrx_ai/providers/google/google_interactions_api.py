"""Google Interactions API adapter for Gemini Omni video generation/editing."""

from __future__ import annotations

import base64
import re
import time
import warnings
from typing import Any

from google import genai

from matrx_ai.config import ImageContent, TextContent, UnifiedConfig, VideoContent
from matrx_ai.providers.base_media import BaseMediaGeneration, GeneratedAsset
from matrx_ai.providers.keys import keyed_provider_client


class GoogleInteractionsVideoGeneration(BaseMediaGeneration):
    provider = "google"
    modality = "video"
    starting_message = "Generating conversational video..."

    client = keyed_provider_client(
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "GOOGLE_AI_STUDIO",
        factory=lambda api_key: genai.Client(
            api_key=api_key,
            http_options={"api_version": "v1beta"},
        ),
    )

    def _build_kwargs(self, unified_config: UnifiedConfig, profile: Any) -> dict[str, Any]:
        request_input = self._interaction_input(unified_config)
        if not request_input:
            raise ValueError(
                "Google Interactions requires at least one text, image, or video input."
            )

        response_format: dict[str, str] = {"type": "video", "delivery": "uri"}
        if unified_config.aspect_ratio:
            response_format["aspect_ratio"] = unified_config.aspect_ratio

        kwargs: dict[str, Any] = {
            "model": unified_config.model,
            "input": request_input,
            "background": False,
            "stream": False,
            "response_format": response_format,
        }
        if unified_config.previous_interaction_id:
            kwargs["previous_interaction_id"] = unified_config.previous_interaction_id
        if unified_config.task:
            kwargs["generation_config"] = {"video_config": {"task": unified_config.task}}
        if unified_config.store is not None:
            kwargs["store"] = unified_config.store
        return kwargs

    @staticmethod
    def _interaction_input(unified_config: UnifiedConfig) -> list[dict[str, Any]]:
        user_messages = [message for message in unified_config.messages if message.role == "user"]
        if not user_messages:
            return []

        output: list[dict[str, Any]] = []
        for item in user_messages[-1].content:
            if isinstance(item, TextContent) and item.text:
                text = item.text
                if unified_config.duration_seconds is not None:
                    text = f"{text}\n\nGenerate a {unified_config.duration_seconds}-second video."
                output.append({"type": "text", "text": text})
                continue
            if isinstance(item, ImageContent):
                media = GoogleInteractionsVideoGeneration._media_input("image", item)
                if media:
                    output.append(media)
                continue
            if isinstance(item, VideoContent):
                media = GoogleInteractionsVideoGeneration._media_input("video", item)
                if media:
                    output.append(media)
        return output

    @staticmethod
    def _media_input(kind: str, item: ImageContent | VideoContent) -> dict[str, Any] | None:
        result: dict[str, Any] = {"type": kind}
        if item.base64_data:
            result["data"] = item.base64_data
        else:
            uri = item.resolved_url or item.file_uri or item.url
            if not uri:
                return None
            result["uri"] = uri
        if item.mime_type:
            result["mime_type"] = item.mime_type
        return result

    def _telemetry_url(self, unified_config: UnifiedConfig, kwargs: dict[str, Any]) -> str:
        return "https://generativelanguage.googleapis.com/v1beta/interactions"

    def _call_provider(self, kwargs: dict[str, Any]) -> Any:
        # google-genai labels this SDK property experimental even though Google
        # documents Interactions as the public Omni surface. Suppress only that
        # exact vendor warning at the boundary; every provider error still raises.
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="Interactions usage is experimental.*",
                category=UserWarning,
            )
            return self.client.interactions.create(**kwargs)

    def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        status = str(getattr(raw, "status", "") or "")
        if status in {"failed", "cancelled", "incomplete"}:
            raise RuntimeError(f"Google interaction ended with status={status!r}")

        interaction_id = str(getattr(raw, "id", "") or "")
        previous_id = str(getattr(raw, "previous_interaction_id", "") or "")
        assets: list[GeneratedAsset] = []
        outputs = list(getattr(raw, "outputs", None) or [])
        output_video = getattr(raw, "output_video", None)
        if output_video is not None and not outputs:
            outputs.append(output_video)
        for output in outputs:
            if getattr(output, "type", None) != "video":
                continue
            data = getattr(output, "data", None)
            if isinstance(data, str) and data:
                video_bytes = base64.b64decode(data)
            else:
                uri = getattr(output, "uri", None)
                if not uri:
                    continue
                video_bytes = self._download_uri_video(str(uri))
            metadata = {
                key: value
                for key, value in {
                    "interaction_id": interaction_id,
                    "previous_interaction_id": previous_id,
                }.items()
                if value
            }
            assets.append(
                GeneratedAsset(
                    data=video_bytes,
                    mime_type=getattr(output, "mime_type", None) or "video/mp4",
                    metadata=metadata or None,
                )
            )
        return assets

    def _download_uri_video(self, uri: str) -> bytes:
        match = re.search(r"/files/([^/:?]+)", uri)
        if match is None:
            raise RuntimeError(f"Google returned an invalid video URI: {uri!r}")
        file_id = match.group(1)

        deadline = time.monotonic() + 600
        file_info = self.client.files.get(name=f"files/{file_id}")
        while self._file_state(file_info) not in {"ACTIVE", "FAILED"}:
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Google video file {file_id!r} was not ready after 600s")
            time.sleep(2)
            file_info = self.client.files.get(name=f"files/{file_id}")
        if self._file_state(file_info) == "FAILED":
            raise RuntimeError(f"Google video file {file_id!r} failed processing")
        return self.client.files.download(file=file_info)

    @staticmethod
    def _file_state(file_info: Any) -> str:
        state = getattr(file_info, "state", None)
        return str(getattr(state, "name", state) or "").upper()

    def _provider_usage(self, raw: Any) -> tuple[int, int, int] | None:
        usage = getattr(raw, "usage", None)
        if usage is None:
            return None
        input_tokens = getattr(usage, "total_input_tokens", None)
        output_tokens = getattr(usage, "total_output_tokens", None)
        if input_tokens is None and output_tokens is None:
            return None
        thought_tokens = int(getattr(usage, "total_thought_tokens", 0) or 0)
        return (
            int(input_tokens or 0),
            int(output_tokens or 0) + thought_tokens,
            int(getattr(usage, "total_cached_tokens", 0) or 0),
        )

    def _classify_error(self, exc: Exception) -> Any:
        from matrx_ai.providers.errors import classify_google_error

        return classify_google_error(exc)

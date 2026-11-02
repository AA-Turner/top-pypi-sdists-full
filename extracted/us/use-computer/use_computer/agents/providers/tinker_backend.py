"""Image-aware Tinker sampling backend for the generic CUA agent.

harbor's TinkerLLM forwards text only, so a vision agent loses its screenshots
on the tinker path. This backend builds the generation prompt through a
tinker-cookbook renderer with the model's image processor attached, so the
OpenAI-style `image_url` parts the generic agent emits reach the model.
"""

from __future__ import annotations

import asyncio
import base64
import importlib
import io
from typing import Any, cast

from PIL import Image


class TinkerBackend:
    """Vision-capable tinker sampler that consumes OpenAI chat messages."""

    def __init__(
        self,
        *,
        model_name: str,
        model_path: str | None = None,
        renderer_name: str | None = None,
        temperature: float = 1.0,
        top_p: float = 0.95,
        top_k: int = -1,
        max_tokens: int = 2048,
        retry_times: int = 5,
        retry_interval: float = 5.0,
    ) -> None:
        self.model_name = model_name
        self.model_path = model_path
        self.renderer_name = renderer_name
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.max_tokens = max_tokens
        self.retry_times = retry_times
        self.retry_interval = retry_interval
        self._sampling_client = None
        self._renderer = None

    async def _ensure_ready(self) -> None:
        if self._sampling_client is not None and self._renderer is not None:
            return
        try:
            tinker = importlib.import_module("tinker")
            get_image_processor = importlib.import_module(
                "tinker_cookbook.image_processing_utils"
            ).get_image_processor
            get_model_attributes = importlib.import_module(
                "tinker_cookbook.model_info"
            ).get_model_attributes
            get_renderer = importlib.import_module("tinker_cookbook.renderers").get_renderer
            get_tokenizer = importlib.import_module("tinker_cookbook.tokenizer_utils").get_tokenizer
        except ImportError as exc:
            raise ImportError(
                "TinkerBackend requires `tinker` and `tinker-cookbook`. "
                "Install them with `uv pip install harbor[tinker]`."
            ) from exc

        service_client = tinker.ServiceClient()
        if self.model_path:
            self._sampling_client = await service_client.create_sampling_client_async(
                model_path=self.model_path
            )
        else:
            self._sampling_client = await service_client.create_sampling_client_async(
                base_model=self.model_name
            )

        tokenizer = get_tokenizer(self.model_name)
        attrs = get_model_attributes(self.model_name)
        image_processor = get_image_processor(self.model_name) if attrs.is_vl else None
        renderer_name = self.renderer_name or _default_renderer(self.model_name)
        self._renderer = get_renderer(
            renderer_name,
            tokenizer,
            image_processor=image_processor,
            model_name=self.model_name,
        )

    async def complete(
        self, messages: list[dict[str, Any]], max_tokens: int
    ) -> tuple[str, int, int]:
        """Sample one response; returns (text, prompt_tokens, completion_tokens)."""
        await self._ensure_ready()
        assert self._sampling_client is not None
        assert self._renderer is not None

        tinker = importlib.import_module("tinker")
        get_text_content = importlib.import_module("tinker_cookbook.renderers").get_text_content

        model_input = self._renderer.build_generation_prompt(
            cast(Any, _to_tinker_messages(messages))
        )
        stop = self._renderer.get_stop_sequences()

        last_error: Exception | None = None
        for attempt in range(self.retry_times):
            try:
                response = await self._sampling_client.sample_async(
                    prompt=model_input,
                    num_samples=1,
                    sampling_params=tinker.SamplingParams(
                        temperature=self.temperature,
                        top_p=self.top_p,
                        top_k=self.top_k,
                        max_tokens=max_tokens,
                        stop=stop,
                    ),
                )
                sequence = response.sequences[0]
                parsed_message, _termination = self._renderer.parse_response(sequence.tokens)
                return get_text_content(parsed_message), model_input.length, len(sequence.tokens)
            except Exception as exc:
                last_error = exc
                if attempt == self.retry_times - 1:
                    break
                await asyncio.sleep(self.retry_interval)
        assert last_error is not None
        raise last_error


def _to_tinker_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert OpenAI chat messages to tinker-cookbook messages (text + PIL images)."""
    converted: list[dict[str, Any]] = []
    for message in messages:
        content = message.get("content")
        if isinstance(content, str):
            converted.append({"role": message["role"], "content": content})
            continue

        parts: list[dict[str, Any]] = []
        for part in content or []:
            if part.get("type") == "text":
                parts.append({"type": "text", "text": part.get("text", "")})
            elif part.get("type") == "image_url":
                url = part.get("image_url", {}).get("url", "")
                b64 = url.split(",", 1)[1] if "," in url else url
                image = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")
                parts.append({"type": "image", "image": image})
        if len(parts) == 1 and parts[0]["type"] == "text":
            converted.append({"role": message["role"], "content": parts[0]["text"]})
        else:
            converted.append({"role": message["role"], "content": parts})
    return converted


def _default_renderer(model_name: str) -> str:
    get_recommended_renderer_names = importlib.import_module(
        "tinker_cookbook.model_info"
    ).get_recommended_renderer_names

    recommended = get_recommended_renderer_names(model_name)
    if "qwen3_5_disable_thinking" in recommended:
        return "qwen3_5_disable_thinking"
    return recommended[0]

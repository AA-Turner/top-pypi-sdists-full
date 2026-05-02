# Copyright 2024 KugelAudio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""KugelAudio TTS service for Pipecat.

Internally delegates to the core KugelAudio Python SDK for WebSocket
connection management, pooling, keepalive, and streaming. This avoids
duplicating low-level transport logic and ensures the PipeCat integration
inherits all SDK-level performance optimisations (connection reuse,
pre-warming, language-skip, etc.).
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Optional

from pipecat.frames.frames import (
    ErrorFrame,
    Frame,
    TTSAudioRawFrame,
    TTSStartedFrame,
    TTSStoppedFrame,
)
from pipecat.services.tts_service import TTSService

from kugelaudio import KugelAudio
from kugelaudio.client import REGION_URLS, _parse_api_key
from kugelaudio.models import AudioChunk

from .models import (
    DEFAULT_CFG_SCALE,
    DEFAULT_MAX_NEW_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_SAMPLE_RATE,
    SUPPORTED_SAMPLE_RATES,
    TTSModels,
)

logger = logging.getLogger("kugelaudio.pipecat")


@dataclass
class _TTSOptions:
    model: TTSModels | str
    voice_id: int
    sample_rate: int
    cfg_scale: float
    max_new_tokens: int
    api_key: str
    base_url: str
    language: str | None = None
    normalize: bool = True


class KugelAudioTTSService(TTSService):
    """KugelAudio Text-to-Speech service for Pipecat.

    Integrates KugelAudio's TTS API with Pipecat's pipeline framework,
    providing high-quality voice synthesis via WebSocket streaming.

    Internally uses the core KugelAudio Python SDK for all WebSocket
    transport, connection pooling, and streaming logic.

    Example:
        ```python
        from kugelaudio.pipecat import KugelAudioTTSService

        tts = KugelAudioTTSService(
            api_key="your-api-key",
            voice_id=280,
            model="kugel-1-turbo",
            sample_rate=24000,
        )

        # Use in a Pipecat pipeline
        pipeline = Pipeline([..., tts, ...])
        ```
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: TTSModels | str = DEFAULT_MODEL,
        voice_id: int,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        cfg_scale: float = DEFAULT_CFG_SCALE,
        max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS,
        language: Optional[str] = None,
        normalize: bool = True,
        region: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Create a new KugelAudio TTS service for Pipecat.

        Args:
            api_key: KugelAudio API key. If not provided, reads from
                KUGELAUDIO_API_KEY environment variable. Region-prefixed keys
                (e.g. ``"us-ka_..."`` or ``"global-ka_..."``) are supported —
                the prefix selects the region and is stripped before auth.
            model: TTS model to use. "kugel-1-turbo" (fast) or
                "kugel-1" (premium).
            voice_id: Voice ID to use for synthesis.
            sample_rate: Output sample rate in Hz. Supported rates: 24000 (native),
                22050, 16000, 8000. Lower rates use server-side resampling.
            cfg_scale: CFG scale for generation quality. Defaults to 2.0.
            max_new_tokens: Maximum tokens to generate. Defaults to 2048.
            language: ISO 639-1 language code (e.g., 'en', 'de'). Setting this
                skips server-side auto-detection and saves ~60-150ms per request.
            normalize: Apply text normalization. Defaults to True.
            region: Region for the API endpoint — ``"eu"`` (default), ``"us"``,
                or ``"global"``. Overrides any prefix detected from the API key.
                Ignored when *base_url* is set.
            base_url: API base URL. Overrides region selection entirely. Defaults
                to the URL for the resolved region (EU if unspecified).
            **kwargs: Additional arguments passed to Pipecat TTSService.
        """
        super().__init__(sample_rate=sample_rate, **kwargs)

        kugelaudio_api_key = api_key or os.environ.get("KUGELAUDIO_API_KEY")
        if not kugelaudio_api_key:
            raise ValueError(
                "KUGELAUDIO_API_KEY must be set or api_key must be provided"
            )

        if sample_rate not in SUPPORTED_SAMPLE_RATES:
            raise ValueError(
                f"Unsupported sample rate: {sample_rate}. "
                f"Supported rates: {SUPPORTED_SAMPLE_RATES}"
            )

        clean_key, detected_region = _parse_api_key(kugelaudio_api_key)

        if base_url:
            resolved_url = base_url.rstrip("/")
        else:
            effective_region = region or detected_region or "eu"
            if effective_region not in REGION_URLS:
                raise ValueError(
                    f"Invalid region '{effective_region}'. "
                    f"Must be one of: {', '.join(REGION_URLS)}"
                )
            resolved_url = REGION_URLS[effective_region]

        self._opts = _TTSOptions(
            model=model,
            voice_id=voice_id,
            sample_rate=sample_rate,
            cfg_scale=cfg_scale,
            max_new_tokens=max_new_tokens,
            language=language,
            normalize=normalize,
            api_key=clean_key,
            base_url=resolved_url,
        )

        self._client = KugelAudio(
            api_key=clean_key,
            tts_url=resolved_url,
        )
        self._closed = False

    def can_generate_metrics(self) -> bool:
        """Check if this service can generate processing metrics.

        Returns:
            True, as KugelAudio service supports metrics generation.
        """
        return True

    def prewarm(self) -> None:
        """Pre-establish the WebSocket connection to reduce TTFB on first synthesis.

        Call this during pipeline setup to eagerly establish the connection,
        eliminating ~100-220ms of handshake latency from the first request.

        Example:
            ```python
            tts = KugelAudioTTSService(api_key="your-api-key", language="en")
            tts.prewarm()
            ```
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            logger.warning("prewarm() called outside event loop, skipping")
            return

        async def _do_prewarm() -> None:
            try:
                await self._client.tts.connect_async(model=self._opts.model)
                logger.info("KugelAudio PipeCat TTS connection pre-warmed")
            except Exception:
                logger.warning(
                    "Failed to prewarm KugelAudio connection, "
                    "will retry on first synthesis",
                    exc_info=True,
                )

        loop.create_task(_do_prewarm())

    async def set_model(self, model: str) -> None:
        """Set the TTS model.

        Closes any existing connection since the model is part of the
        WebSocket URL routing.

        Args:
            model: The model identifier to use.
        """
        if model != self._opts.model:
            await self._client.tts._close_ws_connection()
        self._opts.model = model
        await super().set_model(model)

    def set_voice(self, voice: str) -> None:
        """Set the voice ID.

        Args:
            voice: The voice identifier (integer as string).
        """
        self._opts.voice_id = int(voice) if voice else None
        super().set_voice(voice)

    async def cleanup(self) -> None:
        """Clean up resources when the service is stopped."""
        self._closed = True
        self._client.close()

    async def run_tts(self, text: str) -> AsyncGenerator[Frame, None]:
        """Synthesize text to speech via the core KugelAudio SDK.

        Delegates to ``client.tts.stream_async()`` which handles connection
        pooling, keepalive pings, and reconnection transparently.

        Args:
            text: The text to synthesize into speech.

        Yields:
            Frame: TTSStartedFrame, TTSAudioRawFrame chunks, and TTSStoppedFrame.
        """
        logger.debug(f"Generating TTS [{text}]")

        try:
            await self.start_ttfb_metrics()
            await self.start_tts_usage_metrics(text)

            yield TTSStartedFrame()

            t0 = time.perf_counter()
            first_chunk = True

            async for item in self._client.tts.stream_async(
                text=text,
                model_id=self._opts.model,
                voice_id=self._opts.voice_id,
                cfg_scale=self._opts.cfg_scale,
                max_new_tokens=self._opts.max_new_tokens,
                sample_rate=self._opts.sample_rate,
                normalize=self._opts.normalize,
                language=self._opts.language,
                reuse_connection=True,
            ):
                if isinstance(item, AudioChunk):
                    if first_chunk:
                        ttfa_ms = (time.perf_counter() - t0) * 1000
                        logger.info(f"KugelAudio TTFA: {ttfa_ms:.0f}ms")
                        first_chunk = False
                    await self.stop_ttfb_metrics()
                    yield TTSAudioRawFrame(
                        audio=item.audio,
                        sample_rate=self._opts.sample_rate,
                        num_channels=1,
                    )
                elif isinstance(item, dict) and item.get("final"):
                    break

        except Exception as e:
            logger.error(f"TTS error: {e}")
            yield ErrorFrame(error=f"KugelAudio error: {e}")
        finally:
            await self.stop_ttfb_metrics()
            yield TTSStoppedFrame()
            logger.debug(f"Finished TTS [{text}]")

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
import inspect
import logging
import os
import time
import uuid
from dataclasses import dataclass
from functools import lru_cache
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
from kugelaudio.client import _parse_api_key, _resolve_region_url
from kugelaudio.exceptions import (
    ConnectionError as KugelAudioConnectionError,
    ValidationError,
)
from kugelaudio.streaming import MultiContextSession

from .models import (
    DEFAULT_CFG_SCALE,
    DEFAULT_MAX_NEW_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_SAMPLE_RATE,
    SUPPORTED_SAMPLE_RATES,
    TTSModels,
)

logger = logging.getLogger("kugelaudio.pipecat")


# Pipecat 1.x introduced TTSSettings + AIService.start().validate_complete(),
# which logs ERROR for any TTSSettings field still set to the NOT_GIVEN
# sentinel. Subclasses are expected to pass an initialized TTSSettings via
# super().__init__(settings=...). On Pipecat 0.x this module/class doesn't
# exist; we fall back to the old kwarg-only path. See
# pipecat/services/settings.py:TTSSettings.validate_complete.
try:  # noqa: SIM105 — explicit branch is clearer than contextlib.suppress
    from pipecat.services.settings import TTSSettings as _PipecatTTSSettings
except ImportError:  # Pipecat < 1.0
    _PipecatTTSSettings = None  # type: ignore[assignment]


@lru_cache(maxsize=None)
def _frame_supports_context_id(frame_type: type[Frame]) -> bool:
    """Return whether the installed Pipecat frame accepts context_id."""
    try:
        return "context_id" in inspect.signature(frame_type).parameters
    except (TypeError, ValueError):
        return False


def _tts_started_frame(context_id: Optional[str]) -> TTSStartedFrame:
    if context_id and _frame_supports_context_id(TTSStartedFrame):
        return TTSStartedFrame(context_id=context_id)
    return TTSStartedFrame()


def _tts_stopped_frame(context_id: Optional[str]) -> TTSStoppedFrame:
    if context_id and _frame_supports_context_id(TTSStoppedFrame):
        return TTSStoppedFrame(context_id=context_id)
    return TTSStoppedFrame()


def _tts_audio_frame(
    *,
    audio: bytes,
    sample_rate: int,
    num_channels: int,
    context_id: Optional[str],
) -> TTSAudioRawFrame:
    kwargs: dict[str, Any] = {
        "audio": audio,
        "sample_rate": sample_rate,
        "num_channels": num_channels,
    }
    if context_id and _frame_supports_context_id(TTSAudioRawFrame):
        kwargs["context_id"] = context_id
    return TTSAudioRawFrame(**kwargs)


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
                KUGELAUDIO_API_KEY environment variable. Prefix with
                ``"eu-"`` to select the direct EU endpoint; the prefix is
                stripped before auth.
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
            region: API endpoint region. Use ``"eu"`` for the direct EU endpoint.
                Overrides any prefix detected from the API key. Ignored when
                *base_url* is set.
            base_url: API base URL. Overrides region selection entirely. Defaults
                to the default geo-routed API endpoint if no region is specified.
            **kwargs: Additional arguments passed to Pipecat TTSService.
        """
        # On Pipecat 1.x the parent expects an initialized TTSSettings; if we
        # leave model / voice / language as NOT_GIVEN, AIService.start() logs
        # an ERROR per field. Build it from our typed wrapper params here so
        # the user doesn't have to construct one themselves. On Pipecat 0.x
        # _PipecatTTSSettings is None and we fall back to the legacy path.
        super_kwargs: dict[str, Any] = dict(kwargs)
        if _PipecatTTSSettings is not None and "settings" not in super_kwargs:
            # Drop a stray ``voice=`` kwarg if the caller passed both ways —
            # we already cover voice via the dedicated ``voice_id`` param,
            # and Pipecat 1.x routes voice through TTSSettings, not kwargs.
            super_kwargs.pop("voice", None)
            super_kwargs["settings"] = _PipecatTTSSettings(
                model=str(model) if model else None,
                voice=str(voice_id) if voice_id is not None else None,
                language=language,
            )
        super().__init__(sample_rate=sample_rate, **super_kwargs)

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
            effective_region = region or detected_region
            try:
                resolved_url = _resolve_region_url(effective_region)
            except ValidationError as exc:
                raise ValueError(str(exc)) from exc

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
        self._multi_session: Optional[MultiContextSession] = None
        self._multi_session_lock = asyncio.Lock()
        self._multi_session_needs_reset = False
        self._closed = False

    def _create_multi_session(self) -> MultiContextSession:
        return self._client.tts.multi_context_session(
            default_voice_id=self._opts.voice_id,
            model_id=self._opts.model,
            sample_rate=self._opts.sample_rate,
            cfg_scale=self._opts.cfg_scale,
            max_new_tokens=self._opts.max_new_tokens,
            normalize=self._opts.normalize,
            language=self._opts.language,
        )

    async def _get_multi_session(self) -> MultiContextSession:
        if self._multi_session_needs_reset:
            await self._close_multi_session()
            self._multi_session_needs_reset = False
        # An idle WS may have been silently dropped by an upstream proxy / NAT
        # between turns of a voice conversation. Detect that here so we don't
        # ride a corpse forever; without this check, every subsequent run_tts
        # raises ConnectionClosedError("no close frame received or sent").
        if self._multi_session is not None and not self._multi_session.is_alive:
            logger.info(
                "KugelAudio multi-context session WS is dead; reconnecting"
            )
            await self._close_multi_session()
        if self._multi_session is None:
            session = self._create_multi_session()
            await session.connect()
            self._multi_session = session
        return self._multi_session

    async def _close_multi_session(self) -> None:
        session = self._multi_session
        self._multi_session = None
        self._multi_session_needs_reset = False
        if session is not None:
            await session.close()

    async def _close_multi_session_locked(self) -> None:
        async with self._multi_session_lock:
            await self._close_multi_session()

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
                async with self._multi_session_lock:
                    await self._get_multi_session()
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
            async with self._multi_session_lock:
                await self._close_multi_session()
        self._opts.model = model
        await super().set_model(model)

    def set_voice(self, voice: str) -> None:
        """Set the voice ID.

        Args:
            voice: The voice identifier (integer as string).
        """
        previous_voice_id = self._opts.voice_id
        self._opts.voice_id = int(voice) if voice else None
        if self._opts.voice_id != previous_voice_id:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                if self._multi_session is not None:
                    logger.warning(
                        "set_voice() changed voice outside an event loop; "
                        "existing Pipecat multi-context session will be reset on next use"
                    )
                self._multi_session_needs_reset = True
            else:
                loop.create_task(self._close_multi_session_locked())
        super().set_voice(voice)

    async def cleanup(self) -> None:
        """Clean up resources when the service is stopped."""
        self._closed = True
        async with self._multi_session_lock:
            await self._close_multi_session()
        self._client.close()

    async def run_tts(
        self, text: str, context_id: Optional[str] = None
    ) -> AsyncGenerator[Frame, None]:
        """Synthesize text to speech via the core KugelAudio SDK.

        Delegates to ``client.tts.multi_context_session()`` so Pipecat context
        IDs map onto KugelAudio's ``/ws/tts/multi`` endpoint.

        Args:
            text: The text to synthesize into speech.
            context_id: Pipecat TTS context ID. Pipecat 0.x calls this method
                with only ``text``; Pipecat 1.x passes this second argument for
                context tracking.

        Yields:
            Frame: TTSStartedFrame, TTSAudioRawFrame chunks, and TTSStoppedFrame.
        """
        logger.debug(f"Generating TTS [{text}]")
        effective_context_id = context_id or f"kugelaudio-{uuid.uuid4()}"
        error_frame: Optional[ErrorFrame] = None

        await self.start_ttfb_metrics()
        await self.start_tts_usage_metrics(text)
        yield _tts_started_frame(context_id)

        # Try once, then retry once on a connection drop. The retry path
        # exists because a NAT/proxy can quietly drop the WS during the
        # user's think-time between turns, and we'd rather give the
        # conversation one transparent reconnect than a hard error frame.
        for attempt in (1, 2):
            t0 = time.perf_counter()
            first_chunk = True
            yielded_audio = False
            try:
                async with self._multi_session_lock:
                    session = await self._get_multi_session()
                    async for item in session.send(
                        effective_context_id,
                        text,
                        flush=True,
                        chunk_complete_idle_timeout=0.0,
                    ):
                        if first_chunk:
                            ttfa_ms = (time.perf_counter() - t0) * 1000
                            logger.info(f"KugelAudio TTFA: {ttfa_ms:.0f}ms")
                            first_chunk = False
                        await self.stop_ttfb_metrics()
                        yielded_audio = True
                        yield _tts_audio_frame(
                            audio=item.audio,
                            sample_rate=self._opts.sample_rate,
                            num_channels=1,
                            context_id=context_id,
                        )
                error_frame = None
                break
            except KugelAudioConnectionError as e:
                # WS is dead. If nothing was streamed yet on this attempt and
                # we have a retry budget, drop the cached session and try once
                # more with a fresh connection. After that, give up loudly.
                if attempt == 1 and not yielded_audio:
                    logger.warning(
                        "KugelAudio WS dropped; reconnecting and retrying once"
                    )
                    self._multi_session_needs_reset = True
                    continue
                logger.error(f"TTS error: {e}")
                error_frame = ErrorFrame(error=f"KugelAudio error: {e}")
                break
            except Exception as e:
                logger.error(f"TTS error: {e}")
                error_frame = ErrorFrame(error=f"KugelAudio error: {e}")
                break

        await self.stop_ttfb_metrics()
        logger.debug(f"Finished TTS [{text}]")
        if error_frame is not None:
            yield error_frame
        yield _tts_stopped_frame(context_id)
